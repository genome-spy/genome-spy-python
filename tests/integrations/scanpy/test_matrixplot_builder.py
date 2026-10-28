"""MatrixPlot chains reuse detached means, group layout and native tiles."""

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


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("standard_scale", [None, "var", "group"])
@pytest.mark.parametrize("dendrogram", [False, True])
def test_chain_and_function_share_the_entire_native_spec(
    adata, swapped, standard_scale, dendrogram
):
    markers = {"First": ["g2", "g1"], "Again": ["g2", "g3"]}
    plot = gsc.pl.MatrixPlot(adata, markers, "group", standard_scale=standard_scale)
    assert plot.swap_axes(swap_axes=swapped) is plot
    assert plot.style(cmap="Blues", edge_color="navy", edge_lw=0.7) is plot
    assert plot.legend(title="Mean") is plot
    if dendrogram:
        assert plot.add_dendrogram() is plot
    expected = gsc.pl.matrixplot(
        adata,
        markers,
        "group",
        standard_scale=standard_scale,
        swap_axes=swapped,
        dendrogram=dendrogram,
        cmap="Blues",
        edgecolor="navy",
        linewidth=0.7,
        colorbar_title="Mean",
        show=False,
    )
    assert plot.to_chart().to_dict() == expected.to_dict()


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
        spec, data = chart.to_dict(), table(chart)
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
    original, reads = sc.get.obs_df, []
    means, calls = _grouped_data.group_means, []

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
    original, shapes = sparse.csr_matrix.toarray, []

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
        table(first)["_mean"],
        (supplied.T if swapped else supplied).to_numpy().ravel(),
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


@pytest.mark.reference
@pytest.mark.parametrize("sort", [None, "ascending", "descending"])
@pytest.mark.parametrize("swapped", [False, True])
def test_totals_match_scanpy_and_replace_tree(adata, sort, swapped):
    import matplotlib.pyplot as plt

    a = adata[[0, 0, 0, 1, 2, 2, 3]].copy()
    a.obs_names = [f"cell{i}" for i in range(a.n_obs)]
    colors = ["red", "blue", "green", "orange"]
    native = gsc.pl.MatrixPlot(a, ["g1", "g2"], "group").add_dendrogram()
    native.add_totals(sort=sort, color=colors).swap_axes(swap_axes=swapped)
    reference = sc.pl.MatrixPlot(a, ["g1", "g2"], "group").add_dendrogram()
    reference.add_totals(sort=sort, color=colors).swap_axes(swap_axes=swapped)
    try:
        reference.make_figure()
        spec = native.to_chart().to_dict()
        track = spec["surround"]["top" if swapped else "right"][0]
        assert track["name"] == "matrixplot-totals"
        rows = spec["datasets"][track["layer"][0]["data"]["name"]]
        ax = reference.get_axes()["group_extra_ax"]
        np.testing.assert_array_equal(
            [row["count"] for row in rows],
            [
                patch.get_height() if swapped else patch.get_width()
                for patch in ax.patches
            ],
        )
        labels = reference.get_axes()["mainplot_ax"]
        ticks = labels.get_xticklabels() if swapped else labels.get_yticklabels()
        assert [row["group"] for row in rows] == [tick.get_text() for tick in ticks]
        assert [row["color"] for row in rows] == colors
        native.add_totals(show=False)
        assert "matrixplot-totals" not in json.dumps(native.to_chart().to_dict())
        native.add_dendrogram()
        assert (
            native.to_chart().to_dict()["surround"]["top" if swapped else "right"][0][
                "name"
            ]
            == "matrixplot-tree"
        )
    finally:
        plt.close("all")


def test_hiding_tree_preserves_order_and_swapping_does_not_toggle(adata):
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2"], "group").add_dendrogram()
    displayed = table(plot.to_chart())
    plot.add_dendrogram(show=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)
    assert "matrixplot-tree" not in json.dumps(plot.to_chart().to_dict())
    plot.swap_axes().swap_axes()
    np.testing.assert_allclose(
        table(plot.to_chart())["_mean"],
        displayed["_mean"].to_numpy().reshape(4, 2).T.ravel(),
    )
    plot.swap_axes(swap_axes=False)
    pd.testing.assert_frame_equal(table(plot.to_chart()), displayed)


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


def test_show_displays_once_independently_of_scanpy_autosave(adata, monkeypatch):
    monkeypatch.setattr(sc.settings, "_autosave", True)
    shown = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda chart: shown.append(chart))
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2"], "group")
    assert not shown
    assert plot.show() is None
    assert len(shown) == 1
    with pytest.raises(TypeError, match="to_chart"):
        plot.show(return_axes=True)
    assert len(shown) == 1


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"ax": None}, TypeError, "ax"),
        ({"return_fig": True}, TypeError, "return_fig"),
        ({"vcenter": 0}, NotImplementedError, "vcenter"),
        ({"norm": object()}, NotImplementedError, "norm"),
        ({"shading": "auto"}, TypeError, "shading"),
        ({"standard_scale": "obs"}, ValueError, "standard_scale"),
        ({"zoom": "x"}, TypeError, "zoom"),
        ({"width": 0}, ValueError, "width"),
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
def test_invalid_chain_options_have_context(adata, method, options, error, match):
    plot = gsc.pl.MatrixPlot(adata, ["g1", "g2"], "group")
    with pytest.raises(error, match=match):
        getattr(plot, method)(**options)


@pytest.mark.parametrize(
    "method", ["swap_axes", "add_dendrogram", "add_totals", "legend"]
)
def test_shared_method_arguments_and_defaults_match_scanpy(method):
    actual = inspect.signature(getattr(gsc.pl.MatrixPlot, method)).parameters
    reference = inspect.signature(getattr(sc.pl.MatrixPlot, method)).parameters
    assert actual.keys() == reference.keys()
    for name in reference:
        assert actual[name].default == reference[name].default
        assert actual[name].kind == reference[name].kind
