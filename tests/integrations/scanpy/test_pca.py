"""Stored PCA diagnostics reuse ranking and embedding charts without analysis."""

from copy import deepcopy

import anndata as ad
import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixtures import make_pca_adata
from tests.integrations.scanpy.helpers import scanpy_rank_labels, units
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata

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
    actual_spec, expected_spec = (actual.to_dict(), expected.to_dict())
    for panel, reference in zip(units(actual_spec), units(expected_spec), strict=True):
        low, high = reference["encoding"]["y"]["scale"]["domain"]
        reference["encoding"]["y"]["scale"]["domain"] = [low, high + 0.3 * (high - low)]
        reference["padding"] = {"top": 0}
    assert actual_spec == expected_spec
    np.testing.assert_array_equal(a.varm["PCs"], before)
    assert not a.uns


@pytest.mark.reference
def test_signed_tied_extremes_keep_numpy_order_odd_split_and_omitted_rank_gap():
    spec = gsc.pl.pca_loadings(loadings_data(), "1", n_points=3, show=False).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
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


@pytest.mark.reference
def test_top_only_includes_scanpys_extra_label():
    spec = gsc.pl.pca_loadings(
        loadings_data(), "1", include_lowest=False, n_points=2, show=False
    ).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
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
    assert all((len(rows(spec, i)) == 6 for i in range(3)))
    assert all((r["_label"] != "⋮" for i in range(3) for r in rows(spec, i)))


def test_duplicate_labels_and_repeated_components_remain_separate_panels():
    a = loadings_data()
    a.var_names = ["same"] * a.n_vars
    spec = gsc.pl.pca_loadings(a, [2, 1, 2], n_points=6, show=False).to_dict()
    assert [p["title"] for p in units(spec)] == ["PC2", "PC1", "PC2"]
    assert all((r["_label"] == "same" for r in rows(spec)))
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
        ValueError, match="gsc.pl.pca_loadings: missing.*sc.pp.pca explicitly"
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
        assert a.isbacked and (not a.uns)
    finally:
        a.file.close()


@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("storage", [np.array, list, tuple])
def test_variance_is_the_existing_ranking_chart_without_analysis_or_expression(
    monkeypatch, log, storage
):
    a = make_ranked_adata()
    source = storage([0.2, 0.4, 0.1, 0.2, 0.05])
    a.uns["pca"]["variance_ratio"] = source
    for module, name in [
        (sc.pp, "pca"),
        (sc.tl, "pca"),
        (sc.pl, "ranking"),
        (sc.pl, "pca_variance_ratio"),
    ]:
        monkeypatch.setattr(
            module, name, lambda *a, **k: pytest.fail("Ran upstream analysis/plotting")
        )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda _: pytest.fail("Read expression"))
    )
    options = {"log": log, "hover": False, "width": 240, "height": 210, "show": False}
    actual = gsc.pl.pca_variance_ratio(a, 2, **options)
    expected = gsc.pl.ranking(
        a, "uns", "variance_ratio", dictionary="pca", labels="PC", n_points=2, **options
    )
    reference = expected.to_dict()
    low, high = reference["encoding"]["y"]["scale"]["domain"]
    reference["encoding"]["y"]["scale"]["domain"] = [low, high + 0.3 * (high - low)]
    reference["padding"] = {"top": 0}
    assert actual.to_dict() == reference
    assert a.uns["pca"]["variance_ratio"] is source
    np.testing.assert_array_equal(source, [0.2, 0.4, 0.1, 0.2, 0.05])


@pytest.mark.reference
def test_tied_ratios_keep_original_pc_names_and_top_onlys_extra_label():
    spec = gsc.pl.pca_variance_ratio(make_ranked_adata(), 2, show=False).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
    assert actual == scanpy_rank_labels("pca_variance_ratio", make_ranked_adata(), 2)[0]
    assert [(rank, score) for rank, _, score in actual] == [
        (0, 0.4),
        (1, 0.2),
        (2, 0.2),
    ]
    assert spec["title"] == "variance ratio"
    assert spec["encoding"]["x"]["scale"]["domain"] == [-0.9, 2.9]
    assert spec["encoding"]["x"]["axis"]["title"] == "ranking"
    np.testing.assert_allclose(spec["encoding"]["y"]["scale"]["domain"], [0.19, 0.489])


def test_log_is_a_natural_log_score_transform_before_ranking():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.exp([-3.0, -1.0, -2.0, -4.0])
    spec = gsc.pl.pca_variance_ratio(a, 1, log=True, show=False).to_dict()
    assert [r["_label"] for r in rows(spec)] == ["PC2", "PC3"]
    np.testing.assert_allclose([r["_score"] for r in rows(spec)], [-1, -2])
    np.testing.assert_allclose(spec["encoding"]["y"]["scale"]["domain"], [-2.1, -0.605])
    assert spec["encoding"]["y"]["scale"].get("type", "linear") == "linear"


def test_rank_limits_preserve_default_extra_label_and_empty_space_for_short_results():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.linspace(0.9, 0.01, 50)
    default = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert len(rows(default)) == 31
    assert rows(default)[-1]["_label"] == "PC31"
    short = gsc.pl.pca_variance_ratio(a, 80, show=False).to_dict()
    assert len(rows(short)) == 50
    assert short["encoding"]["x"]["scale"]["domain"] == [-0.9, 80.9]


def test_float32_log_scores_retain_scanpys_input_precision():
    a = make_ranked_adata()
    source = np.array([0.1, 0.4, 0.2], dtype=np.float32)
    a.uns["pca"]["variance_ratio"] = source
    spec = gsc.pl.pca_variance_ratio(a, log=True, show=False).to_dict()
    np.testing.assert_array_equal(
        [r["_score"] for r in rows(spec)], np.log(source)[[1, 2, 0]]
    )


def test_linear_scores_are_never_renormalized_and_zero_is_allowed():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.array([-0.2, 0, 2.0])
    spec = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert [r["_score"] for r in rows(spec)] == [2, 0, -0.2]
    a.uns["pca"]["variance_ratio"] = [0.0]
    single = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert len(rows(single)) == 1 and rows(single)[0]["_label"] == "PC1"
    assert single["encoding"]["y"]["scale"]["domain"] == [-0.05, 0.05]


@pytest.mark.parametrize("count", [0, -1, True, 1.5, None])
def test_invalid_rank_counts_name_n_pcs(count):
    with pytest.raises(ValueError, match="gsc.pl.pca_variance_ratio: n_pcs"):
        gsc.pl.pca_variance_ratio(make_ranked_adata(), count, show=False)


@pytest.mark.parametrize("pca", [None, {}, {"variance": np.array([1.0])}])
def test_missing_results_require_explicit_scanpy_pca(pca):
    a = make_ranked_adata()
    a.uns["pca"] = pca
    with pytest.raises(
        ValueError, match="gsc.pl.pca_variance_ratio: missing.*sc.pp.pca explicitly"
    ):
        gsc.pl.pca_variance_ratio(a, show=False)


@pytest.mark.parametrize(
    "values,log,error,message",
    [
        ([], False, ValueError, "nonempty"),
        (np.array([[0.2, 0.4]]), False, TypeError, "one-dimensional"),
        ("0.2", False, TypeError, "one-dimensional"),
        ([[0.2], [0.4, 0.1]], False, TypeError, "real numbers"),
        ([float("nan")], False, ValueError, "finite"),
        ([float("inf")], False, ValueError, "finite"),
        ([1j], False, TypeError, "real numbers"),
        ([0.4, 0], True, ValueError, "positive"),
        ([0.4, -0.1], True, ValueError, "positive"),
    ],
)
def test_invalid_stored_vectors_fail_with_context(values, log, error, message):
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = values
    with pytest.raises(error, match=f"gsc.pl.pca_variance_ratio:.*{message}"):
        gsc.pl.pca_variance_ratio(a, log=log, show=False)


def test_lazy_vectors_reject_without_materialization():

    class Lazy:
        def __array__(self, *args):
            pytest.fail("Materialized lazy ratios")

    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = Lazy()
    with pytest.raises(TypeError, match="gsc.pl.pca_variance_ratio:.*resident"):
        gsc.pl.pca_variance_ratio(a, show=False)


def test_backed_data_and_views_read_the_stored_snapshot_without_reconstruction(
    tmp_path,
):
    a = ad.AnnData(sparse.csr_matrix((10, 100)))
    a.uns["pca"] = {"variance_ratio": np.array([0.2, 0.4, 0.1])}
    path = tmp_path / "variance.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        for data in (backed, backed[:2, :3]):
            spec = gsc.pl.pca_variance_ratio(data, 1, show=False).to_dict()
            assert [r["_label"] for r in rows(spec)] == ["PC2", "PC1"]
            np.testing.assert_array_equal(
                data.uns["pca"]["variance_ratio"], [0.2, 0.4, 0.1]
            )
    finally:
        backed.file.close()


@pytest.mark.parametrize("color", [None, "group", ["group", "g1"]])
def test_children_keep_parent_data_configuration_and_diagnostic_defaults(color):
    a = make_pca_adata()
    options = dict(
        color=color,
        components="2,3",
        annotate_var_explained=True,
        zoom=True,
        hover=False,
        width=210,
        height=180,
    )
    overview = gsc.pl.pca_overview(a, show=False, **options).to_dict()
    parents = [
        gsc.pl.pca(a, show=False, **options),
        gsc.pl.pca_loadings(a, components="1,2", width=280, show=False),
        gsc.pl.pca_loadings(a, components="3", width=280, show=False),
        gsc.pl.pca_variance_ratio(a, show=False),
    ]
    assert len(overview["vconcat"]) == 3
    assert overview["spacing"] == 4
    assert overview["resolve"] == {
        "scale": {"x": "independent", "y": "independent", "color": "independent"},
        "legend": {"default": "independent"},
    }
    children = [
        overview["vconcat"][0]["hconcat"][0],
        overview["vconcat"][1],
        *overview["vconcat"][2]["hconcat"],
    ]
    assert overview["vconcat"][2]["resolve"]["scale"] == {
        "x": "independent",
        "y": "independent",
    }
    for index, (child, parent) in enumerate(zip(children, parents, strict=True)):
        expected = parent.to_dict(include_schema=False)
        datasets = expected.pop("datasets")
        if index == 1:
            expected["spacing"] = 4
        assert child == expected
        for name, records in datasets.items():
            assert overview["datasets"][name] == records
    assert "config" not in overview
    assert "legend" in overview["vconcat"][0]["hconcat"][0]["config"]
    loadings = [*units(overview["vconcat"][1]), overview["vconcat"][2]["hconcat"][0]]
    assert [panel["title"] for panel in loadings] == ["PC1", "PC2", "PC3"]
    assert all((panel["width"] == 280 and panel["height"] == 300 for panel in loadings))
    variance = overview["vconcat"][2]["hconcat"][1]
    assert variance["encoding"]["x"]["scale"]["domain"] == [-0.9, 30.9]
    assert variance["width"] == variance["height"] == 300
    assert variance["mark"]["tooltip"] == {"handler": "default"}


def test_stored_results_are_not_recomputed_mutated_or_read_from_expression(monkeypatch):
    a = make_pca_adata()
    before = deepcopy(a)
    for module, name in [
        (sc.pp, "pca"),
        (sc.tl, "pca"),
        (sc.pl, "pca_overview"),
        (sc.pl, "pca"),
        (sc.pl, "pca_loadings"),
        (sc.pl, "pca_variance_ratio"),
    ]:
        monkeypatch.setattr(
            module, name, lambda *a, **k: pytest.fail("Ran upstream analysis/plotting")
        )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda _: pytest.fail("Read expression"))
    )
    spec = gsc.pl.pca_overview(a, color="group", show=False).to_dict()
    assert len(units(spec)) == 5
    np.testing.assert_array_equal(a.obsm["X_pca"], before.obsm["X_pca"])
    np.testing.assert_array_equal(a.varm["PCs"], before.varm["PCs"])
    np.testing.assert_array_equal(
        a.uns["pca"]["variance_ratio"], before.uns["pca"]["variance_ratio"]
    )
    assert a.obs.equals(before.obs) and a.var.equals(before.var)
    assert a.uns.keys() == before.uns.keys()


@pytest.mark.parametrize(
    "options,error,message",
    [
        ({"ax": object()}, TypeError, "ax is omitted"),
        ({"return_fig": True}, TypeError, "return_fig is omitted"),
        ({"n_points": 2}, TypeError, "n_points"),
        ({"n_pcs": 2}, TypeError, "n_pcs"),
        ({"edges": True}, ValueError, "neighbors"),
    ],
)
def test_unsupported_kwargs_fail_before_any_display(
    monkeypatch, options, error, message
):
    monkeypatch.setattr(
        gs.TopLevelSpec,
        "display",
        lambda *a, **k: pytest.fail("Displayed a partial overview"),
    )
    with pytest.raises(error, match=message):
        gsc.pl.pca_overview(make_pca_adata(), show=True, **options)


@pytest.mark.parametrize("missing", ["coordinates", "loadings", "variance", "finite"])
def test_missing_or_nonfinite_results_fail_without_partial_output(monkeypatch, missing):
    a = make_pca_adata()
    if missing == "coordinates":
        del a.obsm["X_pca"]
    elif missing == "loadings":
        del a.varm["PCs"]
    elif missing == "variance":
        del a.uns["pca"]
    else:
        a.varm["PCs"][0, 0] = np.nan
    monkeypatch.setattr(
        gs.TopLevelSpec,
        "display",
        lambda *a, **k: pytest.fail("Displayed a partial overview"),
    )
    with pytest.raises(ValueError, match="pca|finite"):
        gsc.pl.pca_overview(a, show=True)
