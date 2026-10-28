"""Stored PCA loadings reuse rank preparation and rendering without analysis."""

from copy import deepcopy
import inspect

import anndata as ad
import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import scanpy_rank_labels, units

sc = pytest.importorskip("scanpy")


def loadings_data():
    """Return six named genes with signed, tied and zero loadings in three PCs."""
    a = ad.AnnData(sparse.csr_matrix((4, 6)), var=pd.DataFrame(index=list("abcdef")))
    a.varm["PCs"] = np.array(
        [[3, -2, 5], [-4, 2, 1], [3, 0, -3], [0, 1, 0], [1, -4, 2], [-2, 5, -2]],
        dtype=float,
    )
    return a


def rows(spec, index=0):
    """Return the serialized rank labels for one panel."""
    return spec["datasets"][units(spec)[index]["data"]["name"]]


def test_signature_matches_scanpy_with_only_keyword_native_controls():
    upstream = inspect.signature(sc.pl.pca_loadings).parameters
    native = inspect.signature(gsc.pl.pca_loadings).parameters
    for name, parameter in upstream.items():
        assert native[name].kind == parameter.kind
        assert native[name].default == parameter.default
    assert set(native) - set(upstream) == {"hover", "width", "height"}
    assert all(
        native[key].kind is inspect.Parameter.KEYWORD_ONLY
        for key in set(native) - set(upstream)
    )


@pytest.mark.parametrize("include_lowest", [False, True])
def test_loadings_is_the_existing_ranking_chart_without_analysis_or_expression(
    monkeypatch, include_lowest
):
    a = loadings_data()
    before = deepcopy(a.varm["PCs"])
    for module, method in [
        (sc.pp, "pca"),
        (sc.tl, "pca"),
        (sc.pl, "ranking"),
        (sc.pl, "pca_loadings"),
    ]:
        monkeypatch.setattr(
            module,
            method,
            lambda *a, **k: pytest.fail("Ran upstream analysis/plotting"),
        )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda _: pytest.fail("Read expression"))
    )
    options = {
        "n_points": 3,
        "include_lowest": include_lowest,
        "hover": False,
        "width": 240,
        "height": 210,
        "show": False,
    }
    actual = gsc.pl.pca_loadings(a, components=np.array([3, 1]), **options)
    expected = gsc.pl.ranking(a, "varm", "PCs", indices=[2, 0], **options)
    actual_spec, expected_spec = actual.to_dict(), expected.to_dict()
    for panel, reference in zip(units(actual_spec), units(expected_spec), strict=True):
        low, high = reference["encoding"]["y"]["scale"]["domain"]
        reference["encoding"]["y"]["scale"]["domain"] = [low, high + 0.3 * (high - low)]
        reference["padding"] = {"top": 0}
    assert actual_spec == expected_spec
    np.testing.assert_array_equal(a.varm["PCs"], before)
    assert not a.uns


def test_signed_tied_extremes_keep_numpy_order_odd_split_and_omitted_rank_gap():
    spec = gsc.pl.pca_loadings(loadings_data(), "1", n_points=3, show=False).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
    # Two upstream panels avoid Scanpy's single-component shape bug.
    assert (
        actual
        == scanpy_rank_labels("pca_loadings", loadings_data(), "1,2", n_points=3)[0]
    )
    assert [(rank, score) for rank, _, score in actual] == [
        (0, 3),
        (1, 0.5),
        (3, -2),
        (4, -4),
    ]
    assert spec["encoding"]["x"]["scale"]["domain"] == [-0.9, 4.9]
    np.testing.assert_allclose(spec["encoding"]["y"]["scale"]["domain"], [-4.2, 5.355])
    assert spec["encoding"]["x"]["axis"]["labels"] is False


def test_top_only_includes_scanpys_extra_label():
    spec = gsc.pl.pca_loadings(
        loadings_data(), "1", include_lowest=False, n_points=2, show=False
    ).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
    # Two upstream panels avoid Scanpy's single-component shape bug.
    assert (
        actual
        == scanpy_rank_labels(
            "pca_loadings", loadings_data(), "1,2", include_lowest=False, n_points=2
        )[0]
    )
    assert [(rank, score) for rank, _, score in actual] == [(0, 3), (1, 3), (2, 1)]
    assert spec["encoding"]["x"]["axis"]["labels"] is True


def test_label_padding_accounts_for_its_score_position():
    a = loadings_data()
    a.var_names = ["a", "LOWEST_LOADING", "c", "d", "e", "f"]
    low = gsc.pl.pca_loadings(a, "1", n_points=6, height=210, show=False).to_dict()
    assert 0 <= low["padding"]["top"] < 15
    a.var_names = ["HIGHEST_LOADING", "b", "c", "d", "e", "f"]
    high = gsc.pl.pca_loadings(a, "1", n_points=6, height=210, show=False).to_dict()
    assert high["padding"]["top"] > 100


def test_defaults_cap_rank_count_at_variables_and_keep_the_first_three_components():
    spec = gsc.pl.pca_loadings(loadings_data(), show=False).to_dict()
    assert [p["title"] for p in units(spec)] == ["PC1", "PC2", "PC3"]
    assert all(len(rows(spec, i)) == 6 for i in range(3))
    assert all(r["_label"] != "⋮" for i in range(3) for r in rows(spec, i))


def test_duplicate_labels_and_repeated_components_remain_separate_panels():
    a = loadings_data()
    a.var_names = ["same"] * a.n_vars
    spec = gsc.pl.pca_loadings(a, [2, 1, 2], n_points=6, show=False).to_dict()
    assert [p["title"] for p in units(spec)] == ["PC2", "PC1", "PC2"]
    assert all(r["_label"] == "same" for r in rows(spec))
    assert rows(spec, 0) == rows(spec, 2)


@pytest.mark.parametrize(
    "components", [[], "", "all", "1,2.5", 1, [True], [0], [-1], [1.5], [4]]
)
def test_invalid_components_fail_with_the_plot_and_option_named(components):
    with pytest.raises(ValueError, match="gsc.pl.pca_loadings: components"):
        gsc.pl.pca_loadings(loadings_data(), components, show=False)


@pytest.mark.parametrize("count", [0, -1, True, 2.5, 7, 1])
def test_invalid_rank_counts_fail_clearly(count):
    with pytest.raises(ValueError, match="gsc.pl.pca_loadings:.*n_points"):
        gsc.pl.pca_loadings(loadings_data(), "1,2", n_points=count, show=False)


def test_missing_loadings_requires_explicit_analysis(monkeypatch):
    a = loadings_data()
    del a.varm["PCs"]
    monkeypatch.setattr(sc.pp, "pca", lambda *a, **k: pytest.fail("Ran PCA"))
    with pytest.raises(
        ValueError, match=r"gsc.pl.pca_loadings: missing.*sc.pp.pca explicitly"
    ):
        gsc.pl.pca_loadings(a, show=False)


def test_only_selected_loading_columns_are_checked_and_nonfinite_values_reject():
    a = loadings_data()
    a.varm["PCs"][:, 2] = np.nan
    assert gsc.pl.pca_loadings(a, "1,2", show=False) is not None
    with pytest.raises(ValueError, match="gsc.pl.pca_loadings:.*finite"):
        gsc.pl.pca_loadings(a, "3", show=False)
    a.varm["PCs"] = sparse.csr_matrix(np.ones((6, 3)))
    with pytest.raises(TypeError, match="gsc.pl.pca_loadings:.*resident"):
        gsc.pl.pca_loadings(a, show=False)


def test_backed_data_and_views_use_resident_loadings_without_modification(tmp_path):
    path = tmp_path / "pca.h5ad"
    loadings_data().write_h5ad(path)
    a = ad.read_h5ad(path, backed="r")
    try:
        for data in (a, a[:, :4]):
            before = data.varm["PCs"].copy()
            spec = gsc.pl.pca_loadings(data, "2,1", n_points=2, show=False).to_dict()
            assert [p["title"] for p in units(spec)] == ["PC2", "PC1"]
            np.testing.assert_array_equal(data.varm["PCs"], before)
        assert a.isbacked and not a.uns
    finally:
        a.file.close()
