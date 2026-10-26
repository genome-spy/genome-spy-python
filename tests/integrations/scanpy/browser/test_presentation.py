"""Observe native controls and zoom sizing without changing stored analysis."""

import numpy as np
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_grid_interactions import pointer, svg_root
from tests.integrations.scanpy.browser.test_timeseries import point_coordinates
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.hvg_fixture import make_hvg_result
from tests.integrations.scanpy.paga_fixture import make_adjacency
from tests.integrations.scanpy.paga_fixture import make_paga, POSITIONS
from tests.integrations.scanpy.paga_path_fixture import make_path
from tests.integrations.scanpy.test_paga_compare import make_compare
from tests.integrations.scanpy.sim_fixture import make_sim
from tests.integrations.scanpy.helpers import leaf_marks


def plot_points(page):
    """Return exported plot circles, excluding legend symbols."""
    return [
        circle
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == "point" and group.get("clip-path")
        for circle in group
    ]


def test_hvg_slider_changes_both_panels_and_count_and_keeps_saved_flags(page):
    result = make_hvg_result()
    before = result.copy(deep=True)
    chart = gsc.pl.highly_variable_genes(
        result, threshold_slider=True, zoom=True, show=False
    )
    render(page, chart)
    slider = page.locator('input[type="range"]')
    assert slider.count() == 1
    for cutoff in [-1, 1.0, 2.5]:
        slider.evaluate(
            "(el, value) => {el.value=value; el.dispatchEvent(new Event('input', {bubbles:true}));}",
            cutoff,
        )
        expected = int((result.dispersions_norm >= cutoff).sum())
        page.wait_for_function(
            "async count => (await (await api.imageExport.svg()).blob.text()).includes(count + ' genes above cutoff (preview)')",
            arg=expected,
        )
        circles = plot_points(page)
        assert len(circles) == 2 * len(result)
        assert sum(c.get("fill") == "#2563a6" for c in circles) == 2 * expected
    np.testing.assert_array_equal(result.highly_variable, before.highly_variable)


@pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
def test_profile_dropdown_dims_other_series_without_dropping_points(page, family):
    chart = getattr(gsc.pl, family)(
        [[1, 3], [2, 4], [3, 5]],
        var_names=["A", "B"],
        series_select=True,
        ruler=True,
        zoom=True,
        show=False,
    )
    render(page, chart)
    before = point_coordinates(page)[0]
    page.locator("select").select_option(label="A")
    circles = plot_points(page)
    assert len(circles) == 6
    assert (
        sorted(float(c.get("fill-opacity", "1")) for c in circles)
        == [0.12] * 3 + [0.85] * 3
    )
    np.testing.assert_array_equal(point_coordinates(page)[0], before)
    page.locator("select").select_option(label="All")
    assert all(float(c.get("fill-opacity", "1")) == 0.85 for c in plot_points(page))
    bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
    pointer(page, bounds)
    assert any(group.get("stroke") == "#64748b" for group in svg_root(page).iter())


@pytest.mark.parametrize("as_heatmap", [False, True])
def test_adjacency_points_grow_on_y_zoom_and_stay_bounded(page, as_heatmap):
    chart = gsc.pl.paga_adjacency(
        make_adjacency(),
        as_heatmap=as_heatmap,
        labels=["A", "B", "C"],
        zoom=True,
        width=360,
        height=300,
        show=False,
    )
    bounds = render(page, chart)
    before = [float(c.get("r")) for c in plot_points(page)]
    assert before
    point = plot_points(page)[0]
    pointer(
        page,
        bounds,
        (float(point.get("cx")) - bounds["x"]) / bounds["width"],
        (float(point.get("cy")) - bounds["y"]) / bounds["height"],
    )
    page.mouse.wheel(0, -500)
    page.wait_for_timeout(700)
    after = [float(c.get("r")) for c in plot_points(page)]
    assert after and min(after) > max(before)
    assert max(after) <= 2 * min(before) + 0.01


@pytest.mark.parametrize("as_heatmap", [False, True])
def test_path_uses_native_group_track_and_gene_focus(page, as_heatmap):
    chart = gsc.pl.paga_path(
        make_path(),
        ["beta", "alpha"],
        ["g1", "g2"],
        as_heatmap=as_heatmap,
        series_select=True,
        ruler=True,
        zoom="xy",
        show=False,
    )
    render(page, chart)
    page.locator("select").select_option(label="g1")
    root = svg_root(page)
    text = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert "beta" in text and "alpha" in text
    if not as_heatmap:
        assert "Value" in text


def test_two_profile_controls_remain_independent_in_a_composition(page):
    left = gsc.pl.timeseries(
        [[1, 2], [3, 4]], var_names=["A", "B"], series_select=True, show=False
    )
    right = gsc.pl.timeseries(
        [[1, 2], [3, 4]], var_names=["A", "B"], series_select=True, show=False
    )
    render(page, gs.hconcat(left, right).resolve_scale(default="independent"))
    controls = page.locator("select")
    assert controls.count() == 2
    controls.nth(0).select_option(label="A")
    circles = plot_points(page)
    assert sum(float(c.get("fill-opacity", "1")) == 0.12 for c in circles) == 2


def test_compare_embedding_points_grow_but_graph_node_sizes_keep_their_meaning(page):
    chart = gsc.pl.paga_compare(
        make_compare(), legend_fontweight="normal", zoom=True, add_pos=False, show=False
    )
    bounds = render(page, chart)
    groups = [
        g
        for g in svg_root(page).iter()
        if g.get("data-mark-type") == "point" and g.get("clip-path")
    ]
    before = [[float(c.get("r")) for c in group] for group in groups]
    assert len(before) == 2 and before[0] and before[1]
    cell = list(groups[0])[0]
    pointer(
        page,
        bounds,
        (float(cell.get("cx")) - bounds["x"]) / bounds["width"],
        (float(cell.get("cy")) - bounds["y"]) / bounds["height"],
    )
    page.mouse.wheel(0, -200)
    page.wait_for_timeout(700)
    after = [
        [float(c.get("r")) for c in group]
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == "point" and group.get("clip-path")
    ]
    assert after[0] and min(after[0]) > max(before[0])
    assert max(after[0]) <= 2 * max(before[0]) + 0.01
    assert all(radius in before[1] for radius in after[1])


def test_paga_edge_slider_filters_rules_without_changing_nodes(page):
    chart = gsc.pl.paga(
        make_paga(),
        pos=POSITIONS,
        edge_slider=True,
        show_node_labels=False,
        add_pos=False,
        show=False,
    )
    render(page, chart)
    before = point_coordinates(page)[0]
    root = svg_root(page)
    assert (
        sum(
            len(g)
            for g in root.iter()
            if g.get("data-mark-type") == "rule" and g.get("clip-path")
        )
        > 0
    )
    assert {"A", "B", "C", "D"}.issubset(
        e.text for e in root.iter() if e.tag.endswith("text")
    )
    assert not any(
        g.get("clip-path") and len(g)
        for g in root.iter()
        if g.get("data-mark-type") == "text"
    )
    page.locator('input[type="range"]').evaluate(
        "el => {el.value=1; el.dispatchEvent(new Event('input', {bubbles:true}));}"
    )
    page.wait_for_function("""async () => {
        const svg = new DOMParser().parseFromString(await (await api.imageExport.svg()).blob.text(), 'image/svg+xml');
        return [...svg.querySelectorAll('[data-mark-type="rule"][clip-path]')].every(g=>g.children.length === 0);
    }""")
    root = svg_root(page)
    assert (
        sum(
            len(g)
            for g in root.iter()
            if g.get("data-mark-type") == "rule" and g.get("clip-path")
        )
        == 0
    )
    np.testing.assert_array_equal(point_coordinates(page)[0], before)


@pytest.mark.parametrize("as_heatmap", [False, True])
def test_simulation_gene_and_run_dropdowns_emphasize_their_intersection(
    page, as_heatmap
):
    chart = gsc.pl.sim(
        make_sim(),
        as_heatmap=as_heatmap,
        series_select=True,
        run_select=True,
        ruler=True,
        show=False,
    )
    render(page, chart)
    controls = page.locator("select")
    assert controls.count() == 2
    controls.nth(0).select_option(label="A")
    controls.nth(1).select_option(label="2")
    marks = [
        child
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == ("rect" if as_heatmap else "point")
        and group.get("clip-path")
        for child in group
    ]
    assert len(marks) == 14
    assert sum(float(mark.get("fill-opacity", "1")) == 0.85 for mark in marks) == 3
    assert sum(float(mark.get("fill-opacity", "1")) == 0.12 for mark in marks) == 11


def test_simulation_lines_keep_missing_values_and_run_boundaries(page):
    simulation = make_sim()
    simulation.X[1, 0] = np.nan
    chart = gsc.pl.sim(simulation, connect=True, show=False)
    spec = chart.to_dict()
    points = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
    domain = points["encoding"]["x"]["scale"]["domain"]
    bounds = render(page, chart)
    segments = [
        line
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == "rule"
        and group.get("clip-path")
        and not group.get("stroke-dasharray")
        for line in group
    ]
    assert len(segments) == 6
    for line in segments:
        times = [
            (float(line.get(k)) - bounds["x"]) / bounds["width"] * np.ptp(domain)
            + domain[0]
            for k in ("x1", "x2")
        ]
        np.testing.assert_allclose(times, np.round(times), atol=0.01)
        assert np.floor(round(times[0]) / 3) == np.floor(round(times[1]) / 3)
    assert len(plot_points(page)) == 13
