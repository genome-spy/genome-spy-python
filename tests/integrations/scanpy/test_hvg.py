"""Stored variable-gene data, Scanpy defaults and native chart semantics."""

import inspect
import json
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import units
from tests.integrations.scanpy.hvg_fixture import make_hvg_result

sc = pytest.importorskip("scanpy")


@pytest.mark.parametrize("family", ["highly_variable_genes", "filter_genes_dispersion"])
def test_signatures_preserve_scanpy_defaults_and_add_native_options(family):
    actual = inspect.signature(getattr(gsc.pl, family)).parameters
    expected = inspect.signature(getattr(sc.pl, family)).parameters
    for name, parameter in expected.items():
        assert actual[name].kind == parameter.kind
        assert actual[name].default == parameter.default
    assert set(actual) - set(expected) == {
        "hover",
        "zoom",
        "threshold_slider",
        "width",
        "height",
    }
    assert all(
        actual[name].kind == inspect.Parameter.KEYWORD_ONLY
        for name in set(actual) - set(expected)
    )


@pytest.mark.reference
@pytest.mark.parametrize(
    "storage,flavor",
    [
        ("frame", "seurat"),
        ("adata", "seurat"),
        ("records", "seurat"),
        ("frame", "seurat_v3"),
        ("adata", "seurat_v3"),
    ],
)
@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("selected", [False, True])
def test_points_limits_labels_order_and_selection_match_scanpy(
    storage, flavor, log, selected
):
    import matplotlib.pyplot as plt

    result = make_hvg_result(storage, flavor)
    snapshot = deepcopy(result)
    with plt.rc_context({"figure.dpi": 100}):
        sc.pl.highly_variable_genes(
            result, log=log, highly_variable_genes=selected, show=False
        )
        axes = plt.gcf().axes
        spec = gsc.pl.highly_variable_genes(
            result, log=log, highly_variable_genes=selected, show=False
        ).to_dict()
        assert len(spec["datasets"]) == 1
        rows = next(iter(spec["datasets"].values()))
        for panel, ax in zip(units(spec), axes, strict=True):
            encoding = panel["encoding"]
            for axis in ("x", "y"):
                np.testing.assert_allclose(
                    encoding[axis]["scale"]["domain"],
                    getattr(ax, f"get_{axis}lim")(),
                    rtol=1e-7,
                )
                assert encoding[axis]["axis"]["title"] == (
                    "Mean expression"
                    if axis == "x"
                    else (
                        "Normalized "
                        if encoding[axis]["field"].endswith("_norm")
                        else ""
                    )
                    + ("variance" if flavor == "seurat_v3" else "dispersion")
                )
                assert encoding[axis]["scale"]["type"] == ("log" if log else "linear")
            for artist, flag in zip(ax.collections, (True, False), strict=True):
                expected = artist.get_offsets()
                actual = [
                    [r[encoding[axis]["field"]] for axis in ("x", "y")]
                    for r in rows
                    if r["_selected"] == flag
                ]
                np.testing.assert_allclose(actual, expected, rtol=1e-7)
                assert panel["mark"]["size"] == 9
                assert panel["mark"]["strokeWidth"] == 0
            assert panel["transform"][-1]["sort"] == {
                "field": "_selected",
                "order": "ascending",
            }
        plt.close("all")
    if storage == "frame":
        pd.testing.assert_frame_equal(result, snapshot)
    elif storage == "adata":
        pd.testing.assert_frame_equal(result.var, snapshot.var)
        assert result.uns == snapshot.uns
    else:
        np.testing.assert_array_equal(result, snapshot)


def test_legacy_wrapper_reuses_the_same_native_chart():
    result = make_hvg_result("records")
    with pytest.deprecated_call(match="highly_variable_genes"):
        actual = gsc.pl.filter_genes_dispersion(result, show=False).to_dict()
    assert (
        actual
        == gsc.pl.highly_variable_genes(
            result, highly_variable_genes=False, show=False
        ).to_dict()
    )


def test_chart_keeps_a_snapshot_when_the_supplied_results_change():
    result = make_hvg_result()
    chart = gsc.pl.highly_variable_genes(result, show=False)
    before = chart.to_dict()
    result.loc[:, "means"] = 99
    result.loc[:, "highly_variable"] = False
    assert chart.to_dict() == before


def test_duplicate_gene_labels_keep_distinct_shared_point_ids():
    result = make_hvg_result()
    result.index = ["same"] * len(result)
    spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
    rows = next(iter(spec["datasets"].values()))
    assert [r["_obs_label"] for r in rows] == list(result.index)
    assert len({r["_obs_id"] for r in rows}) == len(result)
    assert len({panel["data"]["name"] for panel in units(spec)}) == 1


def test_missing_values_are_filtered_per_panel_without_changing_stored_values():
    result = make_hvg_result()
    result.loc["gene-0", "dispersions_norm"] = np.nan
    spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
    rows = next(iter(spec["datasets"].values()))
    assert rows[0]["dispersions_norm"] is None
    assert rows[0]["dispersions"] == result.loc["gene-0", "dispersions"]
    first, second = units(spec)
    assert (
        first["transform"][0]["expr"]
        == "isValid(datum.means) && isValid(datum.dispersions_norm)"
    )
    assert (
        second["transform"][0]["expr"]
        == "isValid(datum.means) && isValid(datum.dispersions)"
    )

    assert spec["resolve"]["scale"]["x"] == "independent"


@pytest.mark.reference
def test_missing_value_panel_bounds_match_scanpy():
    import matplotlib.pyplot as plt

    result = make_hvg_result()
    result.loc["gene-0", "dispersions_norm"] = np.nan
    spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
    sc.pl.highly_variable_genes(result, show=False)
    for panel, ax in zip(units(spec), plt.gcf().axes, strict=True):
        np.testing.assert_allclose(
            panel["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
        )
        np.testing.assert_allclose(
            panel["encoding"]["y"]["scale"]["domain"], ax.get_ylim()
        )
    assert spec["resolve"]["scale"]["x"] == "independent"
    plt.close("all")


def test_log_limits_follow_raw_statistics_including_negative_normalized_values():
    result = make_hvg_result()
    result.loc["gene-0", ["dispersions", "dispersions_norm"]] = [-1, -3]
    spec = gsc.pl.highly_variable_genes(result, log=True, show=False).to_dict()
    for panel in units(spec):
        np.testing.assert_allclose(
            panel["encoding"]["y"]["scale"]["domain"],
            [0.1, 1.05 * result.dispersions.max()],
        )
        assert "> 0" in panel["transform"][0]["expr"]
    assert next(iter(spec["datasets"].values()))[0]["dispersions_norm"] == -3
    assert all(
        type(v) is float
        for panel in units(spec)
        for axis in ("x", "y")
        for v in panel["encoding"][axis]["scale"]["domain"]
    )
    json.dumps(spec)


def test_backed_metadata_never_reads_expression_or_reruns_analysis(
    tmp_path, monkeypatch
):
    from anndata import AnnData, read_h5ad

    a = make_hvg_result("adata")
    path = tmp_path / "hvg.h5ad"
    a.write_h5ad(path)
    backed = read_h5ad(path, backed="r")

    def forbidden(*args, **kwargs):
        pytest.fail("Accessed expression or reran gene selection/plotting")

    for owner, name in [
        (sc.pp, "highly_variable_genes"),
        (sc.pp, "filter_genes_dispersion"),
        (sc.pl, "highly_variable_genes"),
        (sc.pl, "filter_genes_dispersion"),
    ]:
        monkeypatch.setattr(owner, name, forbidden)
    monkeypatch.setattr(AnnData, "X", property(forbidden))
    try:
        assert gsc.pl.highly_variable_genes(backed, show=False) is not None
        assert gsc.pl.highly_variable_genes(a[:, [1, 0]], show=False) is not None
    finally:
        backed.file.close()


@pytest.mark.parametrize(
    "change,error,match",
    [
        (lambda x: x.drop(columns="means"), ValueError, "means"),
        (lambda x: x.assign(highly_variable=1), TypeError, "boolean"),
        (lambda x: x.assign(means=np.inf), ValueError, "finite"),
        (lambda x: x.assign(means="x"), TypeError, "real"),
        (lambda x: x.iloc[:0], ValueError, "one gene"),
        (
            lambda x: x.assign(
                highly_variable=pd.array([True] * 7 + [None], dtype="boolean")
            ),
            TypeError,
            "nonmissing",
        ),
    ],
)
def test_invalid_stored_results_fail_clearly(change, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.highly_variable_genes(change(make_hvg_result()), show=False)


def test_missing_analysis_metadata_is_not_invented():
    a = make_hvg_result("adata")
    del a.uns["hvg"]
    with pytest.raises(ValueError, match="flavor.*explicitly"):
        gsc.pl.highly_variable_genes(a, show=False)


@pytest.mark.parametrize("family", ["highly_variable_genes", "filter_genes_dispersion"])
@pytest.mark.parametrize(
    "options,error",
    [
        ({"hover": 1}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"log": None}, TypeError),
        ({"width": 0}, ValueError),
        ({"height": np.inf}, ValueError),
    ],
)
def test_native_options_fail_before_optional_imports(
    monkeypatch, family, options, error
):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    with pytest.raises(error):
        getattr(gsc.pl, family)(object(), show=False, **options)


@pytest.mark.parametrize("means", [0, -1, np.nan])
def test_unsupported_log_bounds_fail_clearly(means):
    result = make_hvg_result().assign(means=means)
    with pytest.raises(NotImplementedError, match="log=True"):
        gsc.pl.highly_variable_genes(result, log=True, show=False)
