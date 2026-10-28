"""Matrixplot statistics, authoritative tables, contract and detached native tiles."""

import inspect
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import pl
from genome_spy.integrations.scanpy._expression import grouped_data as _grouped_data
from tests.integrations.scanpy.grouped_fixture import make_grouped_adata
from tests.integrations.scanpy.helpers import points
from tests.integrations.scanpy.matrixplot_fixture import matrixplot_cases

sc = pytest.importorskip("scanpy")


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_grouped_adata()


def chart(adata, **options):
    return gsc.pl.matrixplot(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        "group",
        use_raw=False,
        show=False,
        **options,
    )


def table(chart):
    spec = chart.to_dict()
    return pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])


def test_signature_preserves_pinned_defaults_and_native_boundary():
    reference = json.loads(
        Path(__file__).with_name("fixtures").joinpath("api.json").read_text()
    )["entries"]["matrixplot"]["parameters"]
    native = inspect.signature(gsc.pl.matrixplot).parameters
    for parameter in reference:
        name = parameter["name"]
        if name in {"ax", "return_fig"}:
            assert name not in native
            continue
        actual = native[name]
        assert actual.kind.name == parameter["kind"]
        assert (
            None if actual.default is inspect.Parameter.empty else repr(actual.default)
        ) == parameter["default"]
    assert set(native) - {p["name"] for p in reference} == {
        "hover",
        "width",
        "height",
        "zoom",
        "show_values",
        "highlight",
    }


@pytest.mark.parametrize("case", matrixplot_cases())
def test_displayed_table_and_labels_match_frozen_scanpy(adata, case):
    reference = json.loads(
        Path(__file__).with_name("fixtures").joinpath("matrixplot.json").read_text()
    )["cases"][case]
    spec = chart(adata, **matrixplot_cases()[case]).to_dict()
    data = pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])
    np.testing.assert_allclose(
        data["_mean"].to_numpy(dtype=float),
        np.array(reference["values"], dtype=float).ravel(),
        equal_nan=True,
    )
    for side, axis in [("bottom", "x"), ("left", "y")]:
        labels = spec["datasets"][spec["surround"][side][0]["data"]["name"]]
        assert [row["label"] for row in labels] == reference[f"{axis}_labels"]
    np.testing.assert_allclose(
        points(spec)["encoding"]["color"]["scale"]["domain"],
        reference["color_domain"],
    )


@pytest.mark.parametrize(
    "options,expected",
    [
        ({}, [1, 1, 4, 0.5, 1.5, 4]),
        ({"standard_scale": "var"}, [1, 0, 0, 0, 1, 0]),
        ({"standard_scale": "group"}, [0, 0, 1, 0, 2 / 7, 1]),
        ({"standard_scale": "var", "swap_axes": True}, [1, 0, 0, 1, 0, 0]),
        (
            {"log": True},
            [
                (np.log(3) / 2),
                np.log(6) / 3,
                np.log(5),
                np.log(2) / 2,
                np.log(4) / 2,
                np.log(5),
            ],
        ),
    ],
)
def test_hand_calculated_means_and_one_scaling_pass(adata, options, expected):
    np.testing.assert_allclose(table(chart(adata, **options))["_mean"], expected)


def test_supplied_table_preserves_values_and_order_without_aggregation(
    adata, monkeypatch
):
    supplied = matrixplot_cases()["supplied"]["values_df"]
    original = supplied.copy(deep=True)
    monkeypatch.setattr(
        _grouped_data,
        "group_means",
        lambda *a, **kw: pytest.fail("Supplied table was recomputed"),
    )
    adata.X[:] = -2
    result = chart(adata, values_df=supplied, log=True, standard_scale="group")
    data = table(result)
    assert data["_group"].tolist() == ["A"] * 3 + ["B"] * 3
    assert data["_gene"].tolist() == ["g3", "g1", "g2"] * 2
    np.testing.assert_array_equal(data["_mean"], [4, 8, 2, 8, 2, 6])
    reordered = table(chart(adata, values_df=supplied, categories_order=["B", "A"]))
    np.testing.assert_array_equal(reordered["_mean"], [8, 2, 6, 4, 8, 2])
    frozen = result.to_dict()
    pd.testing.assert_frame_equal(supplied, original)
    supplied.iloc[:, :] = 99
    assert result.to_dict() == frozen


def test_repeated_supplied_feature_slots_keep_distinct_values(adata):
    values = pd.DataFrame(
        [[1, 2, 3], [4, 5, 6]], index=["B", "A"], columns=["g2", "g1", "g2"]
    )
    data = table(chart(adata, var_names=["g2", "g1", "g2"], values_df=values))
    assert data["_gene"].tolist() == ["g2", "g1", "g2"] * 2
    assert data["_mean"].tolist() == [1, 2, 3, 4, 5, 6]


def test_no_plotting_analysis_mutation_or_fraction_computation(adata, monkeypatch):
    def forbidden(*a, **kw):
        pytest.fail("Unneeded upstream plotting/analysis/statistics ran")

    for name in ("matrixplot", "MatrixPlot"):
        monkeypatch.setattr(sc.pl, name, forbidden)
    for name in ("umap", "pca", "dendrogram", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, forbidden)
    monkeypatch.setattr(_grouped_data, "expression_fractions", forbidden)
    obs, values, uns = adata.obs.copy(deep=True), adata.X.copy(), adata.uns.copy()
    result = chart(adata)
    frozen = result.to_dict()
    pd.testing.assert_frame_equal(adata.obs, obs)
    np.testing.assert_allclose(adata.X, values)
    assert adata.uns == uns
    adata.X[:] = 99
    assert result.to_dict() == frozen


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"ax": None}, TypeError, "ax"),
        ({"return_fig": False}, TypeError, "return_fig"),
        ({"norm": object()}, NotImplementedError, "norm"),
        ({"vcenter": 0}, NotImplementedError, "vcenter"),
        ({"save": "tiles.png"}, NotImplementedError, "save"),
        ({"shading": "auto"}, TypeError, "shading"),
        ({"edgecolor": "red", "edgecolors": "blue"}, TypeError, "edgecolor"),
        ({"linewidth": 1, "linewidths": 2}, TypeError, "linewidth"),
        ({"standard_scale": "obs"}, ValueError, "standard_scale"),
        ({"log": "yes"}, TypeError, "log"),
        ({"hover": "yes"}, TypeError, "hover"),
        ({"swap_axes": None}, TypeError, "swap_axes"),
        ({"show": 1}, TypeError, "show"),
    ],
)
def test_unsupported_options_fail_before_dependencies(
    options, error, match, monkeypatch
):
    monkeypatch.setattr(
        pl, "_require_scanpy", lambda *a: pytest.fail("Validation loaded Scanpy")
    )
    with pytest.raises(error, match=match):
        chart(object(), **options)


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"cmap": "coolwarm"}, NotImplementedError, "cmap"),
        ({"edgecolor": (1, 0, 0)}, NotImplementedError, "edgecolor"),
        ({"linewidth": -1}, ValueError, "linewidth"),
        ({"width": 0}, ValueError, "width"),
        ({"height": float("nan")}, ValueError, "height"),
        ({"figsize": (5, 4), "width": 200}, TypeError, "figsize"),
        ({"vmin": 2, "vmax": 1}, ValueError, "vmin"),
    ],
)
def test_invalid_native_style_is_named(adata, options, error, match):
    with pytest.raises(error, match=match):
        chart(adata, **options)


@pytest.mark.parametrize(
    "kind",
    [
        "missing_group",
        "missing_gene",
        "extra_gene",
        "duplicate_group",
        "duplicate_gene",
        "nonnumeric",
        "infinite",
    ],
)
def test_supplied_tables_reject_ambiguous_or_invalid_inputs(adata, kind):
    values = matrixplot_cases()["supplied"]["values_df"].astype(float)
    if kind == "missing_group":
        values = values.iloc[:1]
    elif kind == "missing_gene":
        values = values.iloc[:, :2]
    elif kind == "extra_gene":
        values["extra"] = 1
    elif kind == "duplicate_group":
        values.index = ["B", "B"]
    elif kind == "duplicate_gene":
        values.columns = ["g1", "g1", "g2"]
    elif kind == "nonnumeric":
        values = values.astype(str)
    else:
        values.iloc[0, 0] = np.inf
    with pytest.raises((ValueError, TypeError), match="values_df"):
        chart(adata, values_df=values)


def test_raw_default_sparse_selected_columns_and_view(adata, monkeypatch):
    from scipy import sparse

    raw = gsc.pl.matrixplot(adata, ["g1", "g2"], "group", show=False)
    np.testing.assert_allclose(table(raw)["_mean"], [23 / 3, 100 / 3, 7, 30])
    adata.X = sparse.csr_matrix(adata.X)
    original, shapes = sparse.csr_matrix.toarray, []

    def selected(matrix, *a, **kw):
        shapes.append(matrix.shape)
        return original(matrix, *a, **kw)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
    np.testing.assert_allclose(
        table(chart(adata[:, :], var_names=["g1", "g2", "g1"]))["_mean"],
        [1, 1, 1, 0.5, 1.5, 0.5],
    )
    assert shapes == [(6, 2)]


def test_missing_cells_constant_color_and_unused_categories(adata):
    values = pd.DataFrame(
        [[4, np.nan, 4], [4, 4, 4]], index=["B", "A"], columns=["g1", "g2", "g3"]
    )
    spec = chart(adata, values_df=values).to_dict()
    assert pd.isna(table(chart(adata, values_df=values))["_mean"].iloc[1])
    assert points(spec)["encoding"]["color"]["scale"]["domain"] == [3.6, 4.4]
    assert "_paint" not in table(chart(adata, values_df=values))
    adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
    with pytest.raises(ValueError, match="unused categories"):
        chart(adata)


def test_dimensions_edges_and_hover(adata):
    for options, expected in [
        ({}, (111, 70)),
        ({"swap_axes": True}, (70, 111)),
        ({"width": 400, "height": 200}, (400, 200)),
        ({"figsize": (6, 3)}, (450, 300)),
    ]:
        spec = chart(adata, **options).to_dict()
        assert (spec["spec"]["width"], spec["spec"]["height"]) == expected
    spec = chart(adata, edgecolor="none", linewidth=2, hover=False).to_dict()
    tiles = points(spec)
    assert tiles["mark"]["strokeOpacity"] == 0
    assert tiles["mark"]["strokeWidth"] == pytest.approx(2 * 100 / 72)
    assert tiles["mark"]["tooltip"] is None and "tooltip" not in tiles["encoding"]
