"""Grouped builders share chaining, totals, display and detached snapshots."""

import inspect
import json

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._expression import grouped_data as _grouped_data
from genome_spy.integrations.scanpy._expression import (
    matrixplot_builder as _matrixplot_builder,
)
from tests.integrations.scanpy.expression_fixtures import make_tree_adata
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


@pytest.mark.reference
@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("standard_scale", ["var", "group"])
@pytest.mark.parametrize("supplied", [False, True])
def test_displayed_color_values_match_installed_scanpy(
    adata, swapped, standard_scale, supplied
):
    import matplotlib.pyplot as plt
    from matplotlib import colormaps

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


@pytest.mark.reference
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
        spec, data = (actual.to_dict(), table(actual))
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
    original, reads = (sc.get.obs_df, [])

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


@pytest.mark.reference
@pytest.mark.parametrize("swapped", [False, True])
def test_actual_scanpy_chain_matches_values_labels_edges_and_bounds(adata, swapped):
    import matplotlib.pyplot as plt

    markers = {"C": "g1", "A": "g2", "D": "g1", "B": "g3"}
    native = gsc.pl.MatrixPlot(adata, markers, "group", standard_scale="var")
    reference = sc.pl.MatrixPlot(adata, markers, "group", standard_scale="var")
    for plot in (native, reference):
        plot.add_dendrogram(size=0.6).swap_axes(swap_axes=swapped).style(
            cmap="viridis", edge_color="navy", edge_lw=0.7
        ).legend(title="Scaled mean", width=1.8)
    try:
        reference.make_figure()
        ax = reference.get_axes()["mainplot_ax"]
        chart = native.to_chart()
        spec, data = (chart.to_dict(), table(chart))
        collection = ax.collections[0]
        np.testing.assert_allclose(data["_mean"], collection.get_array().ravel())
        np.testing.assert_allclose(
            points(spec)["encoding"]["color"]["scale"]["domain"],
            [collection.norm.vmin, collection.norm.vmax],
        )
        for side, ticks in [
            ("bottom", ax.get_xticklabels()),
            ("left", ax.get_yticklabels()),
        ]:
            labels = spec["surround"][side][0]
            assert [r["label"] for r in spec["datasets"][labels["data"]["name"]]] == [
                tick.get_text() for tick in ticks
            ]
        assert points(spec)["mark"]["stroke"] == "navy"
        assert points(spec)["mark"]["strokeWidth"] == pytest.approx(0.7 * 100 / 72)
        assert points(spec)["encoding"]["color"]["legend"]["gradientLength"] == 180
        assert (
            spec["surround"]["top" if swapped else "right"][0][
                "height" if swapped else "width"
            ]
            == 60
        )
    finally:
        plt.close("all")


def test_means_are_computed_once_and_snapshots_do_not_reread_expression(
    adata, monkeypatch
):
    original, reads = (sc.get.obs_df, [])
    means, calls = (_grouped_data.group_means, [])

    def read(*args, **kwargs):
        reads.append(kwargs["keys"])
        return original(*args, **kwargs)

    def compute(*args, **kwargs):
        calls.append(True)
        return means(*args, **kwargs)

    monkeypatch.setattr(sc.get, "obs_df", read)
    monkeypatch.setattr(_grouped_data, "group_means", compute)
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2", "g1"], "group", standard_scale="group")
    first = plot.to_chart()
    frozen = first.to_dict()
    adata.X[:] = 999
    assert plot.to_chart().to_dict() == frozen
    plot.add_dendrogram().swap_axes().style(cmap="Blues").legend(show=False)
    plot.to_chart()
    plot.add_totals().to_chart()
    assert reads == [["group", "g1", "g2"]]
    assert calls == [True]
    assert first.to_dict() == frozen


@pytest.mark.parametrize("swapped", [False, True])
def test_supplied_values_preserve_repeated_slots_and_skip_expression_reads(
    adata, monkeypatch, swapped
):
    from scipy import sparse

    adata.X = sparse.csr_matrix(adata.X)
    supplied = pd.DataFrame(
        np.arange(12).reshape(4, 3),
        index=["B", "D", "A", "C"],
        columns=["g2", "g1", "g2"],
    )
    before = supplied.copy()
    original, shapes = (sparse.csr_matrix.toarray, [])

    def selected(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
    monkeypatch.setattr(
        _grouped_data,
        "group_means",
        lambda *a, **k: pytest.fail("Averaged supplied values"),
    )
    plot = gsc.pl.MatrixPlot(
        adata,
        ["g2", "g1", "g2"],
        "group",
        values_df=supplied,
        log=True,
        standard_scale="var",
    ).swap_axes(swap_axes=swapped)
    first = plot.to_chart()
    np.testing.assert_array_equal(
        table(first)["_mean"], (supplied.T if swapped else supplied).to_numpy().ravel()
    )
    assert shapes == [(0, 2)]
    pd.testing.assert_frame_equal(supplied, before)
    frozen = first.to_dict()
    supplied[:] = 999
    assert plot.to_chart().to_dict() == frozen
    spec = plot.add_totals().to_chart().to_dict()
    track = spec["surround"]["top" if swapped else "right"][0]
    totals = spec["datasets"][track["layer"][0]["data"]["name"]]
    assert [r["group"] for r in totals] == ["B", "D", "A", "C"]
    assert [r["count"] for r in totals] == [2, 2, 2, 2]
    assert shapes == [(0, 2)]


def test_guide_visibility_width_titles_and_style_resets(adata):
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2"], "group", figsize=(6, 3))
    assert plot.style(cmap="Blues").style(edge_color="none") is plot
    assert plot.legend(title="Scaled\nmean", width=2) is plot
    spec = plot.to_chart().to_dict()
    assert spec["spec"]["width"] == 400
    tiles = points(spec)
    assert tiles["encoding"]["color"]["legend"]["gradientLength"] == 200
    assert tiles["encoding"]["color"]["legend"]["title"] == "Scaled mean"
    assert tiles["mark"]["strokeOpacity"] == 0
    assert tiles["encoding"]["color"]["scale"]["scheme"] == "blues"
    plot.style(cmap=None, edge_color=None, edge_lw=None).legend(show=False)
    spec = plot.to_chart().to_dict()
    assert spec["spec"]["width"] == 600
    tiles = points(spec)
    assert tiles["encoding"]["color"]["legend"] is None
    assert tiles["encoding"]["color"]["scale"]["scheme"] == "viridis"
    assert tiles["mark"]["stroke"] == "black"
    assert tiles["mark"]["strokeWidth"] == pytest.approx(1.5 * 100 / 72)
    plot.legend(title=None)
    assert (
        points(plot.to_chart().to_dict())["encoding"]["color"]["legend"]["title"]
        is None
    )


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"vcenter": 0}, NotImplementedError, "vcenter"),
        ({"norm": object()}, NotImplementedError, "norm"),
        ({"shading": "auto"}, TypeError, "shading"),
        ({"standard_scale": "obs"}, ValueError, "standard_scale"),
        ({"zoom": "x"}, TypeError, "zoom"),
        ({"show_values": 1}, TypeError, "show_values"),
    ],
)
def test_constructor_errors_precede_dependencies_and_data(
    monkeypatch, options, error, match
):
    monkeypatch.setattr(
        _matrixplot_builder, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
    )
    with pytest.raises(error, match=match):
        gsc.pl.MatrixPlot(object(), ["g1"], "group", **options)


@pytest.mark.parametrize(
    "method,options,error,match",
    [
        ("swap_axes", {"swap_axes": 1}, TypeError, "swap_axes"),
        ("add_dendrogram", {"dendrogram_key": ""}, TypeError, "dendrogram_key"),
        ("add_totals", {"sort": "wrong"}, ValueError, "sort"),
        ("add_totals", {"color": ["red"]}, ValueError, "color"),
        ("legend", {"show": "yes"}, TypeError, "show"),
        ("legend", {"width": 0}, ValueError, "show=False"),
    ],
)
def test_matrixplot_invalid_chain_options_have_context(
    adata, method, options, error, match
):
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2"], "group")
    with pytest.raises(error, match=match):
        getattr(plot, method)(**options)


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
@pytest.mark.parametrize(
    "swapped,scale,tree",
    [
        (False, None, False),
        (True, None, False),
        (False, "var", True),
        (True, "group", True),
    ],
)
def test_chain_and_function_agree(adata, family, swapped, scale, tree):
    markers = {"First": ["g2", "g1"], "Again": ["g2", "g3"]}
    plot = getattr(gsc.pl, family)(adata, markers, "group", standard_scale=scale)
    style = (
        {"dot_min": 0.2, "dot_max": 0.9, "smallest_dot": 10}
        if family == "DotPlot"
        else {"edge_color": "navy", "edge_lw": 0.7}
    )
    legend = (
        {"size_title": "Cells", "colorbar_title": "Expression"}
        if family == "DotPlot"
        else {"title": "Mean"}
    )
    assert plot.swap_axes(swap_axes=swapped) is plot
    assert plot.style(cmap="viridis", **style) is plot
    assert plot.legend(**legend) is plot
    if tree:
        assert plot.add_dendrogram() is plot
    options = style if family == "DotPlot" else {"edgecolor": "navy", "linewidth": 0.7}
    titles = legend if family == "DotPlot" else {"colorbar_title": "Mean"}
    expected = getattr(gsc.pl, family.lower())(
        adata,
        markers,
        "group",
        standard_scale=scale,
        swap_axes=swapped,
        dendrogram=tree,
        cmap="viridis",
        show=False,
        **options,
        **titles,
    )
    assert plot.to_chart().to_dict() == expected.to_dict()


@pytest.mark.reference
@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
@pytest.mark.parametrize("sort", [None, "ascending", "descending"])
@pytest.mark.parametrize("swapped", [False, True])
def test_totals_match_scanpy_and_replace_tree(adata, family, sort, swapped):
    import matplotlib.pyplot as plt

    a = adata[[0, 0, 0, 1, 2, 2, 3]].copy()
    a.obs_names = [f"cell{i}" for i in range(a.n_obs)]
    colors = ["red", "blue", "green", "orange"]
    native = getattr(gsc.pl, family)(a, ["g1", "g2"], "group").add_dendrogram()
    reference = getattr(sc.pl, family)(a, ["g1", "g2"], "group").add_dendrogram()
    for plot in (native, reference):
        plot.add_totals(sort=sort, color=colors).swap_axes(swap_axes=swapped)
    try:
        reference.make_figure()
        spec = native.to_chart().to_dict()
        side = "top" if swapped else "right"
        track = spec["surround"][side][0]
        assert track["name"] == f"{family.lower()}-totals"
        rows = spec["datasets"][track["layer"][0]["data"]["name"]]
        axes = reference.get_axes()
        np.testing.assert_array_equal(
            [r["count"] for r in rows],
            [
                p.get_height() if swapped else p.get_width()
                for p in axes["group_extra_ax"].patches
            ],
        )
        ticks = (
            axes["mainplot_ax"].get_xticklabels()
            if swapped
            else axes["mainplot_ax"].get_yticklabels()
        )
        assert [r["group"] for r in rows] == [t.get_text() for t in ticks]
        assert [r["color"] for r in rows] == colors
        native.add_totals(show=False)
        assert f"{family.lower()}-totals" not in json.dumps(native.to_chart().to_dict())
        native.add_dendrogram()
        assert (
            native.to_chart().to_dict()["surround"][side][0]["name"]
            == f"{family.lower()}-tree"
        )
    finally:
        plt.close("all")


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
def test_hidden_tree_keeps_order_and_swapping_is_idempotent(adata, family):
    plot = getattr(gsc.pl, family)(adata, ["g1", "g2"], "group").add_dendrogram()
    displayed = table(plot.to_chart())
    plot.add_dendrogram(show=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)
    assert f"{family.lower()}-tree" not in json.dumps(plot.to_chart().to_dict())
    plot.swap_axes()
    swapped = plot.to_chart().to_dict()
    plot.swap_axes()
    assert plot.to_chart().to_dict() == swapped
    np.testing.assert_allclose(
        table(plot.to_chart())["_mean"],
        displayed["_mean"].to_numpy().reshape(4, 2).T.ravel(),
    )
    plot.swap_axes(swap_axes=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
def test_show_displays_once_and_ignores_autosave(adata, monkeypatch, family):
    monkeypatch.setattr(sc.settings, "_autosave", True)
    shown = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda chart: shown.append(chart))
    plot = getattr(gsc.pl, family)(adata, ["g1", "g2"], "group")
    assert not shown
    assert plot.show() is None
    assert len(shown) == 1
    with pytest.raises(TypeError, match="to_chart"):
        plot.show(return_axes=True)
    assert len(shown) == 1


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
@pytest.mark.parametrize(
    "method", ["swap_axes", "add_dendrogram", "add_totals", "legend"]
)
def test_method_signatures_match_scanpy(family, method):
    actual = inspect.signature(getattr(getattr(gsc.pl, family), method)).parameters
    reference = inspect.signature(getattr(getattr(sc.pl, family), method)).parameters
    assert actual.keys() == reference.keys()
    titles = (
        {"colorbar_title": "Mean expression", "size_title": "Cells expressing (%)"}
        if family == "DotPlot" and method == "legend"
        else {}
    )
    for name in reference:
        assert actual[name].default == titles.get(name, reference[name].default)
        assert actual[name].kind == reference[name].kind
