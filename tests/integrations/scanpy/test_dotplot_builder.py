"""DotPlot chains share summaries/rendering and preserve detached native snapshots."""

import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata
from tests.integrations.scanpy.helpers import points

sc = pytest.importorskip("scanpy")


@pytest.fixture
def adata():
    a = make_tree_adata()
    sc.tl.dendrogram(a, "group", use_rep="X")
    return a


def table(chart):
    spec = chart.to_dict()
    return pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("standard_scale", ["var", "group"])
@pytest.mark.parametrize("supplied", [False, True])
def test_displayed_color_values_match_installed_scanpy(
    adata, swapped, standard_scale, supplied
):
    from matplotlib import colormaps
    import matplotlib.pyplot as plt

    options = {"standard_scale": standard_scale, "cmap": "viridis"}
    if supplied:
        options["dot_color_df"] = pd.DataFrame(
            [[1, 2, 3], [2, 3, 9], [4, 7, 8], [6, 1, 2]],
            index=adata.obs["group"].cat.categories,
            columns=["g1", "g2", "g3"],
        )
    native = gsc.pl.DotPlot(adata, ["g1", "g2", "g3"], "group", **options).swap_axes(
        swap_axes=swapped
    )
    reference = sc.pl.DotPlot(adata, ["g1", "g2", "g3"], "group", **options).swap_axes(
        swap_axes=swapped
    )
    try:
        reference.make_figure()
        expected = reference.get_axes()["mainplot_ax"].collections[0].get_facecolors()
        values = table(native.to_chart())["_mean"].to_numpy()
        np.testing.assert_allclose(colormaps["viridis"](values), expected)
    finally:
        plt.close("all")


def test_constructor_preserves_the_pinned_signature():
    reference = json.loads(
        Path(__file__).with_name("fixtures").joinpath("api.json").read_text()
    )["entries"]["DotPlot"]["parameters"]
    actual = inspect.signature(gsc.pl.DotPlot).parameters
    for parameter in reference:
        name = parameter["name"]
        if name == "ax":
            assert name not in actual
            continue
        assert actual[name].kind.name == parameter["kind"]
        assert (
            None
            if actual[name].default is inspect.Parameter.empty
            else repr(actual[name].default)
        ) == parameter["default"]
    assert set(actual) - {p["name"] for p in reference} == {
        "hover",
        "zoom",
        "highlight",
        "group_gap",
        "width",
        "height",
    }


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("standard_scale", [None, "var", "group"])
@pytest.mark.parametrize("dendrogram", [False, True])
def test_chain_and_function_share_the_entire_native_spec(
    adata, swapped, standard_scale, dendrogram
):
    markers = {"first": ["g2", "g1"], "again": ["g2", "g3"]}
    builder = gsc.pl.DotPlot(adata, markers, "group", standard_scale=standard_scale)
    assert builder.swap_axes(swap_axes=swapped) is builder
    assert (
        builder.style(cmap="viridis", dot_min=0.2, dot_max=0.9, smallest_dot=10)
        is builder
    )
    assert builder.legend(size_title="Cells", colorbar_title="Expression") is builder
    if dendrogram:
        assert builder.add_dendrogram() is builder
    expected = gsc.pl.dotplot(
        adata,
        markers,
        "group",
        standard_scale=standard_scale,
        swap_axes=swapped,
        dendrogram=dendrogram,
        cmap="viridis",
        dot_min=0.2,
        dot_max=0.9,
        smallest_dot=10,
        size_title="Cells",
        colorbar_title="Expression",
        show=False,
    )
    assert builder.to_chart().to_dict() == expected.to_dict()


@pytest.mark.parametrize("swapped", [False, True])
def test_actual_scanpy_chains_match_order_positions_sizes_and_padding(adata, swapped):
    import matplotlib.pyplot as plt

    markers = {"C": ["g1", "g2"], "A": "g2", "D": "g3", "B": "g4"}
    options = dict(
        dot_min=0.1,
        dot_max=0.9,
        smallest_dot=5,
        largest_dot=120,
        size_exponent=2,
        dot_edge_color="navy",
        dot_edge_lw=0.7,
        x_padding=1.1,
        y_padding=0.7,
        grid=True,
    )
    native = gsc.pl.DotPlot(adata, markers, "group", standard_scale="var")
    native.add_dendrogram().swap_axes(swap_axes=swapped).style(**options)
    reference = sc.pl.DotPlot(adata, markers, "group", standard_scale="var")
    reference.add_dendrogram().swap_axes(swap_axes=swapped).style(**options)
    try:
        reference.make_figure()
        ax = reference.get_axes()["mainplot_ax"]
        actual = native.to_chart()
        spec, data = actual.to_dict(), table(actual)
        np.testing.assert_allclose(
            data[["_x", "_y"]] + 0.5, ax.collections[0].get_offsets()
        )
        scale = points(spec)["encoding"]["size"]["scale"]
        areas = dict(zip(scale["domain"], scale["range"], strict=True))
        np.testing.assert_allclose(
            [areas[value] for value in data["_percent"]],
            ax.collections[0].get_sizes() * (100 / 72) ** 2,
        )
        for side, ticks in [
            ("left", ax.get_yticklabels()),
            ("bottom", ax.get_xticklabels()),
        ]:
            label_spec = spec["surround"][side][0]
            labels = [
                row["label"] for row in spec["datasets"][label_spec["data"]["name"]]
            ]
            assert labels == [tick.get_text() for tick in ticks]
        assert spec["scales"]["x"]["paddingOuter"] == pytest.approx(0.6)
        assert spec["scales"]["y"]["paddingOuter"] == pytest.approx(0.2)
        assert points(spec)["encoding"]["x"]["axis"]["grid"] is True
        assert points(spec)["mark"]["stroke"] == "navy"
        assert points(spec)["mark"]["strokeWidth"] == pytest.approx(0.7 * 100 / 72)
    finally:
        plt.close("all")


def test_selected_expression_is_read_once_and_rendered_charts_stay_detached(
    adata, monkeypatch
):
    original, reads = sc.get.obs_df, []

    def read(*args, **kwargs):
        reads.append(kwargs["keys"])
        return original(*args, **kwargs)

    monkeypatch.setattr(sc.get, "obs_df", read)
    builder = gsc.pl.DotPlot(adata, ["g1", "g2", "g1"], "group")
    assert len(reads) == 1
    first = builder.to_chart()
    frozen = first.to_dict()
    adata.X[:] = 999
    assert builder.to_chart().to_dict() == frozen
    builder.style(cmap="viridis").swap_axes().legend(show=False)
    second = builder.to_chart().to_dict()
    assert len(reads) == 1
    assert first.to_dict() == frozen
    assert second != frozen
    assert points(second)["encoding"]["color"]["legend"] is None
    assert points(second)["encoding"]["size"]["legend"] is None


@pytest.mark.parametrize("swapped", [False, True])
def test_authoritative_sizes_and_colors_are_copied_and_follow_slot_order(
    adata, swapped
):
    sizes = pd.DataFrame(
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9], [1, 0, 0.5]],
        index=["B", "D", "A", "C"],
        columns=["g2", "g1", "g2"],
    )
    colors = sizes * 2
    before = sizes.copy()
    plot = gsc.pl.DotPlot(
        adata, ["g2", "g1", "g2"], "group", dot_size_df=sizes, dot_color_df=colors
    )
    plot.swap_axes(swap_axes=swapped).add_dendrogram()
    chart = plot.to_chart()
    data = table(chart)
    expected = sizes.loc[list(adata.uns["dendrogram_group"]["categories_ordered"])]
    np.testing.assert_allclose(
        data["_percent"], (expected.T if swapped else expected).to_numpy().ravel() * 100
    )
    pd.testing.assert_frame_equal(sizes, before)
    frozen = chart.to_dict()
    sizes[:] = 0
    colors[:] = 0
    assert plot.to_chart().to_dict() == frozen


@pytest.mark.parametrize("sort", [None, "ascending", "descending"])
@pytest.mark.parametrize("swapped", [False, True])
def test_totals_match_scanpy_counts_order_colors_and_replace_tree(adata, sort, swapped):
    import matplotlib.pyplot as plt

    a = adata[[0, 0, 0, 1, 2, 2, 3]].copy()
    a.obs_names = [f"cell{i}" for i in range(a.n_obs)]
    colors = ["red", "blue", "green", "orange"]
    native = gsc.pl.DotPlot(a, ["g1", "g2"], "group").add_dendrogram()
    native.add_totals(sort=sort, color=colors).swap_axes(swap_axes=swapped)
    reference = sc.pl.DotPlot(a, ["g1", "g2"], "group").add_dendrogram()
    reference.add_totals(sort=sort, color=colors).swap_axes(swap_axes=swapped)
    try:
        reference.make_figure()
        spec = native.to_chart().to_dict()
        track = spec["surround"]["top" if swapped else "right"][0]
        assert track["name"] == "dotplot-totals"
        rows = spec["datasets"][track["layer"][0]["data"]["name"]]
        ax = reference.get_axes()["group_extra_ax"]
        np.testing.assert_array_equal(
            [row["count"] for row in rows],
            [
                patch.get_height() if swapped else patch.get_width()
                for patch in ax.patches
            ],
        )
        group_labels = (
            reference.get_axes()["mainplot_ax"].get_xticklabels()
            if swapped
            else reference.get_axes()["mainplot_ax"].get_yticklabels()
        )
        assert [row["group"] for row in rows] == [
            tick.get_text() for tick in group_labels
        ]
        assert [row["color"] for row in rows] == colors
        native.add_totals(show=False)
        assert "dotplot-totals" not in json.dumps(native.to_chart().to_dict())
        native.add_dendrogram()
        tree = native.to_chart().to_dict()["surround"]["top" if swapped else "right"][0]
        assert tree["name"] == "dotplot-tree"
    finally:
        plt.close("all")


def test_hiding_tree_keeps_its_order_and_transpose_is_idempotent(adata):
    plot = gsc.pl.DotPlot(adata, ["g1", "g2"], "group").add_dendrogram()
    displayed = table(plot.to_chart())
    plot.add_dendrogram(show=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)
    assert "dotplot-tree" not in json.dumps(plot.to_chart().to_dict())
    plot.swap_axes().swap_axes()
    swapped = plot.to_chart().to_dict()
    assert swapped == plot.to_chart().to_dict()
    plot.swap_axes(swap_axes=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)


def test_legend_visibility_titles_and_native_width(adata):
    plot = gsc.pl.DotPlot(adata, ["g1", "g2"], "group", figsize=(6, 3))
    assert plot.style(cmap="viridis").style(dot_edge_color=None) is plot
    plot.legend(show_size_legend=False, colorbar_title="Scaled\nmean", width=2)
    spec = plot.to_chart().to_dict()
    assert spec["spec"]["width"] == 400
    point = points(spec)
    assert point["encoding"]["size"]["legend"] is None
    assert point["encoding"]["color"]["legend"]["title"] == "Scaled mean"
    assert point["encoding"]["color"]["legend"]["gradientLength"] == 200
    assert point["mark"]["strokeOpacity"] == 0
    assert point["encoding"]["color"]["scale"]["scheme"] == "viridis"
    plot.legend(show=False)
    assert plot.to_chart().to_dict()["spec"]["width"] == 600
    plot.legend(show_colorbar=False, size_title="Cells")
    point = points(plot.to_chart().to_dict())
    assert point["encoding"]["color"]["legend"] is None
    assert point["encoding"]["size"]["legend"]["title"] == "Cells"


def test_default_legends_match_the_function_before_and_after_a_chain(adata):
    expected = gsc.pl.dotplot(adata, ["g1", "g2"], "group", show=False).to_dict()
    plot = gsc.pl.DotPlot(adata, ["g1", "g2"], "group")
    assert plot.to_chart().to_dict() == expected
    assert plot.legend().to_chart().to_dict() == expected
    point = points(expected)
    assert point["encoding"]["size"]["legend"]["title"] == "Cells expressing (%)"
    assert point["encoding"]["color"]["legend"]["title"] == "Mean expression"
    legend = expected["config"]["legend"]
    assert legend["layout"] == {
        "anchor": "middle",
        "direction": "horizontal",
        "wrap": True,
    }
    assert legend["spacing"] == 16
    assert legend["labelFont"] == legend["titleFont"] == "Lato"
    assert legend["labelFontSize"] == legend["titleFontSize"]


def test_show_uses_one_native_display_and_does_not_follow_autosave(adata, monkeypatch):
    monkeypatch.setattr(sc.settings, "_autosave", True)
    shown = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda chart: shown.append(chart))
    builder = gsc.pl.DotPlot(adata, ["g1", "g2"], "group")
    assert not shown
    assert builder.show() is None
    assert len(shown) == 1
    with pytest.raises(TypeError, match="to_chart"):
        builder.show(return_axes=True)
    assert len(shown) == 1


@pytest.mark.parametrize(
    "method,options,error,match",
    [
        ("style", {"color_on": "square"}, NotImplementedError, "square"),
        ("swap_axes", {"swap_axes": 1}, TypeError, "swap_axes"),
        ("add_dendrogram", {"dendrogram_key": ""}, TypeError, "dendrogram_key"),
        ("add_totals", {"sort": "wrong"}, ValueError, "sort"),
        ("add_totals", {"color": ["red"]}, ValueError, "color"),
        ("legend", {"show": "yes"}, TypeError, "show"),
        ("legend", {"width": 0}, ValueError, "show=False"),
    ],
)
def test_invalid_chain_options_have_context(adata, method, options, error, match):
    plot = gsc.pl.DotPlot(adata, ["g1", "g2"], "group")
    with pytest.raises(error, match=match):
        getattr(plot, method)(**options)


@pytest.mark.parametrize(
    "change,error",
    [
        (lambda sizes: sizes.rename(index={"A": "missing"}), ValueError),
        (lambda sizes: sizes.rename(columns={"g1": "missing"}), ValueError),
        (lambda sizes: sizes * -1, ValueError),
        (lambda sizes: sizes * np.nan, ValueError),
        (lambda sizes: sizes.astype(str), TypeError),
    ],
)
def test_supplied_sizes_reject_invalid_fractions_and_slots(adata, change, error):
    sizes = pd.DataFrame(0.5, index=["C", "A", "D", "B"], columns=["g1", "g2"])
    with pytest.raises(error, match="dot_size_df"):
        gsc.pl.DotPlot(adata, ["g1", "g2"], "group", dot_size_df=change(sizes))
