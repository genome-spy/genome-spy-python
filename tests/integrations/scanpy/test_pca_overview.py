"""PCA overview composes its existing parent charts without repeating analysis."""

from copy import deepcopy
import inspect

import anndata as ad
import numpy as np
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import units
from tests.integrations.scanpy.pca_fixture import make_pca_adata

sc = pytest.importorskip("scanpy")


def test_signature_retains_upstream_kwargs_with_explicit_native_delivery():
    upstream = inspect.signature(sc.pl.pca_overview).parameters
    native = inspect.signature(gsc.pl.pca_overview).parameters
    for name, parameter in upstream.items():
        assert native[name].kind == parameter.kind
        assert native[name].default == parameter.default
    assert set(native) - set(upstream) == {"show", "save"}
    assert all(
        native[name].kind is inspect.Parameter.KEYWORD_ONLY
        and native[name].default is None
        for name in ("show", "save")
    )


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
        gsc.pl.pca_loadings(a, show=False),
        gsc.pl.pca_variance_ratio(a, show=False),
    ]
    assert len(overview["vconcat"]) == 3
    assert overview["resolve"] == {
        "scale": {"x": "independent", "y": "independent", "color": "independent"},
        "legend": {"default": "independent"},
    }
    for child, parent in zip(overview["vconcat"], parents, strict=True):
        assert len(child["hconcat"]) == 1
        child = child["hconcat"][0]
        expected = parent.to_dict(include_schema=False)
        datasets = expected.pop("datasets")
        assert child == expected
        for name, records in datasets.items():
            assert overview["datasets"][name] == records
    assert "config" not in overview
    assert "legend" in overview["vconcat"][0]["hconcat"][0]["config"]
    loadings = units(overview["vconcat"][1])
    assert [panel["title"] for panel in loadings] == ["PC1", "PC2", "PC3"]
    assert all(panel["width"] == panel["height"] == 300 for panel in loadings)
    variance = overview["vconcat"][2]["hconcat"][0]
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
