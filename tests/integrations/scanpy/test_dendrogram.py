"""Scanpy delegation, stored tree, ordering, storage and public-contract checks."""

from copy import deepcopy
import inspect
import json
from pathlib import Path
import pickle

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import points
from genome_spy.integrations.scanpy import pl
from genome_spy.integrations.scanpy._dendrogram_data import prepare_dendrogram
from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata, tree_cases

sc = pytest.importorskip("scanpy")
REFERENCE = Path(__file__).with_name("fixtures") / "dendrogram.json"


def cache(adata, case="default", key="dendrogram_group"):
    result = deepcopy(json.loads(REFERENCE.read_text())["computations"][case])
    adata.uns[key] = result
    return result


def test_hand_calculated_correlations_and_complete_linkage():
    import anndata as ad

    a = ad.AnnData(
        np.array([[0.0, 1, 0], [1, 0, 0], [0, 0, 1]]),
        obs=pd.DataFrame(
            {"group": pd.Categorical(["A", "B", "C"])}, index=["a", "b", "c"]
        ),
    )
    tree = prepare_dendrogram(a, "group")
    np.testing.assert_allclose(
        tree.correlation, [[1, -0.5, -0.5], [-0.5, 1, -0.5], [-0.5, -0.5, 1]]
    )
    np.testing.assert_allclose(tree.linkage[:, 2], [1.5, 1.5])
    assert sorted(tree.order) == ["A", "B", "C"]
    assert a.uns == {}


@pytest.mark.parametrize("case", tree_cases())
def test_delegated_tree_matches_frozen_scanpy_computations(case):
    reference = json.loads(REFERENCE.read_text())["computations"][case]
    a = make_tree_adata(case)
    if case in ("custom", "optimal"):
        cache(a, case)
    tree = prepare_dendrogram(a, tree_cases()[case].get("groupby", "group"))
    assert list(map(str, tree.order)) == reference["categories_ordered"]
    for actual, expected in [
        (tree.linkage, reference["linkage"]),
        (tree.correlation, reference["correlation_matrix"]),
        (tree.icoord, reference["dendrogram_info"]["icoord"]),
        (tree.dcoord, reference["dendrogram_info"]["dcoord"]),
    ]:
        np.testing.assert_allclose(actual, expected, atol=1e-12)


def test_cached_results_are_verified_without_rerunning_linkage_or_mutating(monkeypatch):
    from anndata import AnnData
    from scipy.cluster import hierarchy

    a = make_tree_adata()
    stored = cache(a)
    before = pickle.dumps(a.uns)

    def forbidden(*args, **kwargs):
        pytest.fail("Stored tree triggered data access or computation")

    monkeypatch.setattr(AnnData, "X", property(forbidden))
    monkeypatch.setattr(sc.tl, "dendrogram", forbidden)
    monkeypatch.setattr(hierarchy, "linkage", forbidden)
    monkeypatch.setattr(hierarchy, "dendrogram", forbidden)
    result = prepare_dendrogram(a, "group")
    np.testing.assert_array_equal(result.icoord, stored["dendrogram_info"]["icoord"])
    np.testing.assert_array_equal(result.dcoord, stored["dendrogram_info"]["dcoord"])
    assert pickle.dumps(a.uns) == before
    stored["dendrogram_info"]["icoord"][0][0] = 999
    assert result.icoord[0, 0] != 999


@pytest.mark.parametrize(
    "kind",
    [
        "groupby",
        "labels",
        "indices",
        "geometry",
        "linkage",
        "correlation",
    ],
)
def test_malformed_and_incompatible_caches_fail_explicitly(kind):
    a = make_tree_adata()
    stored = cache(a)
    if kind == "groupby":
        stored["groupby"] = ["batch"]
    elif kind == "labels":
        stored["categories_ordered"][0] = "unknown"
    elif kind == "indices":
        stored["categories_idx_ordered"] = [0, 0, 2, 3]
    elif kind == "geometry":
        stored["dendrogram_info"]["icoord"][0][0] = np.nan
    elif kind == "linkage":
        stored["linkage"][0][0] = 999
    else:
        stored["correlation_matrix"][0][1] = np.nan
    before = pickle.dumps(a.uns)
    with pytest.raises(ValueError, match="cache.*malformed or incompatible"):
        prepare_dendrogram(a, "group")
    assert pickle.dumps(a.uns) == before


def test_reordered_categories_preserve_cached_leaves_and_align_correlations():
    a = make_tree_adata()
    stored = cache(a)
    a.obs["group"] = a.obs["group"].cat.reorder_categories(["B", "D", "A", "C"])
    result = prepare_dendrogram(a, "group")
    assert result.categories == ("B", "D", "A", "C")
    assert list(result.order) == stored["categories_ordered"]
    np.testing.assert_allclose(
        result.correlation, np.array(stored["correlation_matrix"])[::-1, ::-1]
    )


@pytest.mark.parametrize(
    "storage",
    [sparse.csr_matrix, sparse.csc_matrix, sparse.csr_array, sparse.csc_array],
)
def test_stored_trees_work_with_sparse_expression_without_densifying(
    storage, monkeypatch
):
    a = make_tree_adata()
    cache(a)
    expected = prepare_dendrogram(a, "group")
    a.X = storage(a.X)

    def forbidden(*args, **kwargs):
        pytest.fail("Stored tree densified expression")

    for cls in (
        sparse.csr_matrix,
        sparse.csc_matrix,
        sparse.csr_array,
        sparse.csc_array,
    ):
        monkeypatch.setattr(cls, "toarray", forbidden)
    actual = prepare_dendrogram(a, "group")
    np.testing.assert_allclose(actual.correlation, expected.correlation)


def test_missing_tree_delegates_to_scanpy_once_without_mutation(monkeypatch):
    original = sc.tl.dendrogram
    calls = []

    def compute(adata, groupby, **kwargs):
        calls.append((groupby, kwargs))
        return original(adata, groupby, **kwargs)

    monkeypatch.setattr(sc.tl, "dendrogram", compute)
    a = make_tree_adata("pca")
    before = pickle.dumps((a.obs, a.uns, a.obsm))
    result = prepare_dendrogram(a, "group")
    assert calls == [(["group"], {"use_rep": "X_pca", "inplace": False})]
    assert pickle.dumps((a.obs, a.uns, a.obsm)) == before
    np.testing.assert_allclose(
        result.linkage,
        json.loads(REFERENCE.read_text())["computations"]["pca"]["linkage"],
    )


def test_scanpy_component_subset_and_custom_methods_are_rendered_as_stored(monkeypatch):
    a = make_tree_adata("pca")
    sc.tl.dendrogram(
        a,
        "group",
        n_pcs=3,
        cor_method="spearman",
        linkage_method="average",
        optimal_ordering=True,
    )
    stored = deepcopy(a.uns["dendrogram_group"])
    a.X[:] = np.nan
    del a.obsm["X_pca"]
    monkeypatch.setattr(
        sc.tl, "dendrogram", lambda *args, **kwargs: pytest.fail("Tree recomputed")
    )
    tree = prepare_dendrogram(a, "group")
    np.testing.assert_array_equal(tree.linkage, stored["linkage"])
    np.testing.assert_array_equal(tree.correlation, stored["correlation_matrix"])
    np.testing.assert_array_equal(tree.icoord, stored["dendrogram_info"]["icoord"])
    assert list(tree.order) == stored["categories_ordered"]


def test_missing_sparse_tree_fails_without_densifying(monkeypatch):
    a = make_tree_adata()
    a.X = sparse.csr_matrix(a.X)
    monkeypatch.setattr(
        sparse.csr_matrix, "toarray", lambda *args, **kwargs: pytest.fail("Densified X")
    )
    with pytest.raises(TypeError, match="resident dense representation"):
        prepare_dendrogram(a, "group")


def test_pca_guard_views_and_resident_backed_representation(monkeypatch, tmp_path):
    import anndata as ad

    def forbidden(*args, **kwargs):
        pytest.fail("Analysis or upstream plotting ran")

    for name in ("pca", "umap", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, forbidden)
    monkeypatch.setattr(sc.pp, "pca", forbidden)
    a = make_tree_adata("pca")
    expected = prepare_dendrogram(a, "group")
    np.testing.assert_allclose(
        prepare_dendrogram(a[:, :], "group").correlation, expected.correlation
    )
    sc.tl.dendrogram(a, "group")
    path = tmp_path / "backed.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        np.testing.assert_allclose(
            prepare_dendrogram(backed, "group").correlation, expected.correlation
        )
    finally:
        backed.file.close()
    del a.uns["dendrogram_group"]
    del a.obsm["X_pca"]
    with pytest.raises(ValueError, match="Plotting never fits PCA"):
        prepare_dendrogram(a, "group")
    assert a.uns == {} and "X_pca" not in a.obsm


@pytest.mark.parametrize(
    "kind",
    [
        "unused",
        "single",
        "constant",
        "missing_profile",
        "not_categorical",
        "missing_multi",
        "collision",
    ],
)
def test_invalid_group_profiles_have_actionable_errors(kind):
    a = make_tree_adata()
    groupby = "group"
    if kind == "unused":
        a.obs["group"] = a.obs["group"].cat.add_categories(["unused"])
    elif kind == "single":
        a.obs["group"] = pd.Categorical(["one"] * len(a))
    elif kind == "constant":
        a.X[:2] = 1
        a.X[4:6] = 1
    elif kind == "missing_profile":
        a.X[[0, 4]] = np.nan
    elif kind == "not_categorical":
        a.obs["group"] = a.obs["group"].astype(str)
    elif kind == "missing_multi":
        a.obs.loc["cell0", "batch"] = None
        groupby = ["group", "batch"]
    else:
        a.obs["group"] = pd.Categorical([1, "1", "D", "B"] * 2)
    with pytest.raises((ValueError, TypeError), match="Dendrogram|Grouped plotting"):
        prepare_dendrogram(a, groupby)


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_summary_rows_features_brackets_and_values_share_tree_order(family, swapped):
    a = make_tree_adata()
    order = list(prepare_dendrogram(a, "group").order)
    markers = {"C": ["g1", "g2"], "A": ["g2"], "D": ["g3"], "B": ["g4", "g1"]}
    c = getattr(gsc.pl, family)(
        a,
        markers,
        "group",
        dendrogram=True,
        swap_axes=swapped,
        categories_order=["B", "D", "A", "C"],
        show=False,
    )
    spec = c.to_dict()
    records = spec["datasets"][points(spec)["data"]["name"]]
    assert list(dict.fromkeys(row["_group"] for row in records)) == order
    expected_genes = [gene for category in order for gene in markers[category]]
    assert list(dict.fromkeys(row["_gene"] for row in records)) == list(
        dict.fromkeys(expected_genes)
    )
    bracket = spec["datasets"][
        spec["surround"]["right" if swapped else "top"][0]["layer"][0]["data"]["name"]
    ]
    assert [row["label"] for row in bracket] == order
    for row in records:
        expected = a[a.obs["group"] == row["_group"], row["_gene"]].X.mean()
        assert row["_mean"] == pytest.approx(expected)
    assert a.uns == {}


def test_two_group_attachment_matches_scanpy_skip_and_standalone_tree_works():
    a = make_tree_adata()
    a = a[a.obs["group"].isin(["A", "B"])].copy()
    for family in ("dotplot", "matrixplot"):
        with pytest.warns(UserWarning, match="more than two categories"):
            c = getattr(gsc.pl, family)(
                a, ["g1", "g2"], "group", dendrogram=True, show=False
            )
        assert set(c.to_dict()["surround"]) == {"left", "bottom"}
    assert len(gsc.pl.dendrogram(a, "group", show=False).to_dict()["datasets"])


@pytest.mark.parametrize("family", ["dendrogram", "correlation_matrix"])
def test_new_signatures_preserve_defaults_and_optional_imports(family):
    reference = json.loads(REFERENCE.with_name("api.json").read_text())["entries"][
        family
    ]["parameters"]
    native = inspect.signature(getattr(gsc.pl, family)).parameters
    for parameter in reference:
        if parameter["name"] == "ax":
            assert "ax" not in native
            continue
        actual = native[parameter["name"]]
        assert actual.kind.name == parameter["kind"]
        assert (
            None if actual.default is inspect.Parameter.empty else repr(actual.default)
        ) == parameter["default"]


@pytest.mark.parametrize(
    "family,options,error",
    [
        ("dendrogram", {"orientation": "diagonal"}, ValueError),
        ("dendrogram", {"ax": None}, TypeError),
        ("dendrogram", {"remove_labels": "yes"}, TypeError),
        ("correlation_matrix", {"ax": None}, TypeError),
        ("correlation_matrix", {"norm": object()}, NotImplementedError),
        ("correlation_matrix", {"vcenter": 0}, NotImplementedError),
        ("correlation_matrix", {"shading": "auto"}, TypeError),
        ("correlation_matrix", {"hover": "yes"}, TypeError),
        ("correlation_matrix", {"dendrogram": 1}, TypeError),
    ],
)
def test_invalid_render_options_fail_before_dependencies(
    monkeypatch, family, options, error
):
    monkeypatch.setattr(
        pl, "_require_scanpy", lambda *a: pytest.fail("Validation loaded Scanpy")
    )
    with pytest.raises(error):
        getattr(gsc.pl, family)(object(), "group", show=False, **options)


def test_correlation_numbers_and_native_defaults():
    a = make_tree_adata()
    spec = gsc.pl.correlation_matrix(
        a, "group", show_correlation_numbers=True, show=False
    ).to_dict()
    color = spec["layer"][0]["encoding"]["color"]["scale"]
    assert color["domain"] == [-1, 1]
    assert color["scheme"] == {"name": "redblue", "extent": [1, 0]}
    assert not color.get("reverse", False)
    assert spec["layer"][3]["mark"]["type"] == "text"
