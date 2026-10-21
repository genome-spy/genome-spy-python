"""Dotplot contract, displayed statistics, sizing and detached native output."""

import inspect
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.dotplot_fixture import dotplot_cases
from tests.integrations.scanpy.grouped_fixture import make_grouped_adata
from tests.integrations.scanpy.helpers import points

sc = pytest.importorskip("scanpy")


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_grouped_adata()


def chart(a, **options):
    return gsc.pl.dotplot(
        a,
        options.pop("var_names", ["g1", "g2", "g3"]),
        "group",
        use_raw=False,
        show=False,
        **options,
    )


def table(result):
    spec = result.to_dict()
    return pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])


def test_signature_preserves_scanpy_defaults_and_native_boundary():
    reference = json.loads(
        Path(__file__).with_name("fixtures").joinpath("api.json").read_text()
    )["entries"]["dotplot"]["parameters"]
    native = inspect.signature(gsc.pl.dotplot).parameters
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
        "width",
        "height",
        "hover",
        "zoom",
        "highlight",
    }
    assert native["hover"].default is True


@pytest.mark.parametrize("case", dotplot_cases())
def test_displayed_geometry_matches_frozen_scanpy_exports(adata, case):
    reference = json.loads(
        Path(__file__).with_name("fixtures").joinpath("dotplot.json").read_text()
    )["cases"][case]
    result = chart(adata, **dotplot_cases()[case])
    spec, data = result.to_dict(), table(result)
    assert spec["spec"]["view"] == {
        "stroke": "black",
        "strokeWidth": pytest.approx(1.5 * 100 / 72),
    }
    assert spec["config"]["view"] == {"stroke": "transparent", "strokeWidth": 0}
    unit = points(spec)
    np.testing.assert_allclose(data[["_x", "_y"]] + 0.5, reference["positions"])
    size = unit["encoding"]["size"]["scale"]
    area_map = dict(zip(size["domain"], size["range"], strict=True))
    np.testing.assert_allclose(
        [area_map[p] for p in data["_percent"]],
        np.array(reference["sizes"]) * (100 / 72) ** 2,
    )
    for channel, padding in [("x", 0.3), ("y", 0.5)]:
        encoding = unit["encoding"][channel]
        assert encoding["type"] == "index"
        assert spec["scales"][channel]["domain"] == [0, int(data[f"_{channel}"].max())]
        assert spec["scales"][channel]["paddingOuter"] == padding
        assert spec["scales"][channel]["zoom"] is False
    assert spec["scales"]["y"]["reverse"] is True
    size_labels = [
        str(round(value)) for value in unit["encoding"]["size"]["legend"]["values"]
    ]
    assert size_labels == reference["size_labels"]


def test_hand_calculated_means_fractions_and_exact_area_mapping(adata):
    result = chart(adata)
    data = table(result)
    np.testing.assert_allclose(data["_mean"], [1, 1, 4, 0.5, 1.5, 4])
    np.testing.assert_allclose(data["_percent"], [100 / 3, 200 / 3, 100, 50, 50, 100])
    unit = points(result.to_dict())
    scale = unit["encoding"]["size"]["scale"]
    for percent, area in zip(scale["domain"], scale["range"], strict=True):
        assert area == pytest.approx((percent / 100) ** 1.5 * 200 * (100 / 72) ** 2)
    assert unit["mark"]["stroke"] == "black"
    assert unit["mark"]["strokeWidth"] == pytest.approx(0.2 * 100 / 72)
    assert unit["mark"]["tooltip"] == {"handler": "default"}


def test_swapped_scaling_preserves_both_scanpy_scaling_passes(adata):
    data = table(chart(adata, standard_scale="var", swap_axes=True))
    # First scale columns, transpose, then scale the displayed columns again.
    np.testing.assert_allclose(data["_mean"], [1, 0, 0, 1, 0, 0])
    np.testing.assert_allclose(data["_percent"], [100 / 3, 50, 200 / 3, 50, 100, 100])


def test_supplied_colors_align_labels_scale_once_and_do_not_mutate(adata):
    supplied = pd.DataFrame(
        [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
    )
    original = supplied.copy(deep=True)
    np.testing.assert_allclose(
        table(chart(adata, dot_color_df=supplied))["_mean"], [2, 6, 8, 8, 2, 4]
    )
    scaled = table(chart(adata, dot_color_df=supplied, standard_scale="group"))
    np.testing.assert_allclose(scaled["_mean"], [0, 2 / 3, 1, 1, 0, 1 / 3])
    pd.testing.assert_frame_equal(supplied, original)


def test_repeated_feature_slots_keep_distinct_coordinates_and_labels(adata):
    result = chart(adata, var_names={"first": ["g2", "g1"], "again": "g2"})
    data = table(result)
    assert data["_x"].tolist() == [0, 1, 2] * 2
    np.testing.assert_allclose(data["_mean"], [1, 1, 1, 1.5, 0.5, 1.5])
    spec = result.to_dict()
    labels = spec["datasets"][spec["surround"]["bottom"][0]["data"]["name"]]
    assert [v["label"] for v in labels] == ["g2", "g1", "g2"]
    assert spec["surround"]["top"][0]["layer"][0]["mark"]["type"] == "rule"


@pytest.mark.parametrize("swapped", [False, True])
def test_hover_preserves_gene_group_and_unclipped_fraction(adata, swapped):
    result = chart(
        adata,
        var_names=["g2", "g1", "g2"],
        swap_axes=swapped,
        dot_min=0.4,
        dot_max=0.8,
    )
    data = table(result)
    assert data["_gene"].tolist() == (
        ["g2", "g2", "g1", "g1", "g2", "g2"] if swapped else ["g2", "g1", "g2"] * 2
    )
    assert data["_group"].tolist() == (
        ["B", "A"] * 3 if swapped else ["B"] * 3 + ["A"] * 3
    )
    np.testing.assert_allclose(
        data["_percent"],
        [200 / 3, 50, 100 / 3, 50, 200 / 3, 50]
        if swapped
        else [200 / 3, 100 / 3, 200 / 3, 50, 50, 50],
    )
    tooltip = points(result.to_dict())["encoding"]["tooltip"]
    assert [item["field"] for item in tooltip] == [
        "_gene",
        "_group",
        "_mean",
        "_percent",
    ]
    assert tooltip[2]["title"] == "Mean expression"


@pytest.mark.parametrize(
    "supplied,scaled", [(False, True), (True, False), (True, True)]
)
def test_hover_names_displayed_color_values(adata, supplied, scaled):
    options = {"standard_scale": "var"} if scaled else {}
    if supplied:
        options["dot_color_df"] = pd.DataFrame(
            4.0, index=["B", "A"], columns=["g1", "g2", "g3"]
        )
    tooltip = points(chart(adata, **options).to_dict())["encoding"]["tooltip"]
    assert tooltip[2]["title"] == ("Color value" if supplied else "Mean expression") + (
        " (scaled)" if scaled else ""
    )


def test_hover_can_be_disabled_without_changing_geometry(adata):
    enabled = points(chart(adata).to_dict())
    disabled = points(chart(adata, hover=False).to_dict())
    assert disabled["mark"]["tooltip"] is None
    assert "tooltip" not in disabled["encoding"]
    assert {k: v for k, v in enabled["encoding"].items() if k != "tooltip"} == disabled[
        "encoding"
    ]


def test_dot_limits_clip_then_power_and_guides_use_percentages(adata):
    spec = chart(adata, dot_min=0.4, dot_max=0.8, smallest_dot=10).to_dict()
    size = points(spec)["encoding"]["size"]
    for percent, area in zip(
        size["scale"]["domain"], size["scale"]["range"], strict=True
    ):
        fraction = np.clip(percent / 100, 0.4, 0.8)
        assert area == pytest.approx(
            (10 + ((fraction - 0.4) / 0.4) ** 1.5 * 190) * (100 / 72) ** 2
        )
    np.testing.assert_allclose(size["legend"]["values"], [50, 60, 70, 80])


def test_no_analysis_or_mutation_and_chart_is_a_snapshot(adata, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Upstream plotting/analysis ran")

    monkeypatch.setattr(sc.pl, "dotplot", forbidden)
    monkeypatch.setattr(sc.pl, "DotPlot", forbidden)
    for name in ("umap", "pca", "dendrogram", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, forbidden)
    before = adata.copy()
    result = chart(adata)
    frozen = result.to_dict()
    pd.testing.assert_frame_equal(adata.obs, before.obs)
    np.testing.assert_allclose(adata.X, before.X)
    assert adata.uns == before.uns
    adata.X[:] = 9
    assert result.to_dict() == frozen


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"ax": None}, TypeError, "ax"),
        ({"return_fig": False}, TypeError, "return_fig"),
        ({"norm": object()}, NotImplementedError, "norm"),
        ({"vcenter": 0}, NotImplementedError, "vcenter"),
        ({"save": "dots.png"}, NotImplementedError, "save"),
        ({"color_on": "square"}, TypeError, "color_on"),
        ({"dot_size_df": object()}, TypeError, "dot_size_df"),
        ({"cmap": "coolwarm"}, NotImplementedError, "cmap"),
        ({"dot_min": 0.8, "dot_max": 0.2}, ValueError, "dot_min"),
        ({"dot_max": 2}, ValueError, "dot_max"),
        ({"smallest_dot": 201}, ValueError, "smallest_dot"),
        ({"width": 0}, ValueError, "width"),
        ({"height": float("nan")}, ValueError, "height"),
        ({"figsize": (5, 4), "width": 200}, TypeError, "figsize"),
        ({"standard_scale": "obs"}, ValueError, "standard_scale"),
        ({"mean_only_expressed": "yes"}, TypeError, "mean_only_expressed"),
        ({"hover": "yes"}, TypeError, "hover"),
    ],
)
def test_unsupported_or_invalid_options_are_named(adata, options, error, match):
    with pytest.raises(error, match=match):
        chart(adata, **options)


def test_empty_groups_zero_fractions_and_constant_colors(adata):
    adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
    with pytest.raises(ValueError, match="unused categories"):
        chart(adata)
    adata.obs["group"] = adata.obs["group"].cat.remove_unused_categories()
    adata.X[:] = 0
    with pytest.raises(ValueError, match="dot_max=1"):
        chart(adata)
    spec = chart(adata, dot_max=1).to_dict()
    size = points(spec)["encoding"]["size"]["scale"]
    assert size["range"][size["domain"].index(0)] == 0
    assert points(spec)["encoding"]["color"]["scale"]["domain"] == [-0.1, 0.1]


def test_nullable_missing_group_statistic_retains_its_slot(adata):
    adata.obs["nullable"] = pd.array([None, 1, None, 0, 2, None], dtype="Float64")
    result = chart(adata, var_names="nullable")
    data = table(result)
    assert data["_x"].tolist() == [0, 0]
    assert data["_y"].tolist() == [0, 1]
    assert pd.isna(data["_mean"].iloc[0]) and pd.isna(data["_percent"].iloc[0])
    assert data["_mean"].iloc[1] == 0.5 and data["_percent"].iloc[1] == 50


def test_native_dimensions_and_figsize(adata):
    for options, expected in [
        ({}, (111, 70)),
        ({"width": 400, "height": 200}, (400, 200)),
        ({"figsize": (6, 3)}, (450, 300)),
    ]:
        spec = chart(adata, **options).to_dict()
        assert (spec["spec"]["width"], spec["spec"]["height"]) == expected


def test_default_raw_lookup_and_selected_sparse_columns(adata, monkeypatch):
    from scipy import sparse

    result = gsc.pl.dotplot(adata, ["g1", "g2"], "group", show=False)
    np.testing.assert_allclose(table(result)["_mean"], [23 / 3, 100 / 3, 7, 30])
    assert table(result)["_percent"].tolist() == [100] * 4
    adata.X = sparse.csr_matrix(adata.X)
    original, shapes = sparse.csr_matrix.toarray, []

    def selected(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
    chart(adata, var_names=["g1", "g2", "g1"])
    assert shapes == [(6, 2)]


@pytest.mark.parametrize("kind", ["missing", "duplicates", "nonnumeric"])
def test_supplied_color_tables_reject_ambiguous_inputs(adata, kind):
    colors = pd.DataFrame(
        [[1, 2, 3], [4, 5, 6]], index=["B", "A"], columns=["g1", "g2", "g3"]
    )
    if kind == "missing":
        colors = colors.drop(columns="g1")
    elif kind == "duplicates":
        colors.index = ["A", "A"]
    else:
        colors = colors.astype(str)
    with pytest.raises((ValueError, TypeError), match="dot_color_df"):
        chart(adata, dot_color_df=colors)
