"""Observe aligned PAGA comparison panels, default labels and linked navigation."""

import numpy as np
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import svg_root
from tests.integrations.scanpy.helpers import points
from tests.integrations.scanpy.test_paga_compare import make_compare


def point_coordinates(page, names=("panel-0", "panel-1")):
    """Read plot circles inside named panels, excluding their sibling legend views."""
    root = svg_root(page)
    result = []
    for name in names:
        panel = next(group for group in root.iter() if group.get("data-name") == name)
        group = next(
            group for group in panel.iter() if group.get("data-mark-type") == "point"
        )
        result.append(
            np.array([[float(p.get("cx")), float(p.get("cy"))] for p in group])
        )
    return result


@pytest.mark.parametrize("palette", [["red", "blue", "green", "orange"], "set1"])
@pytest.mark.parametrize("component", [False, True])
def test_category_colors_match_between_cells_and_nodes_including_filtered_graphs(
    page, palette, component
):
    a = make_compare()
    chart = gsc.pl.paga_compare(
        a,
        palette=palette,
        single_component=component,
        threshold=0.2,
        legend_fontweight="normal",
        size=36,
        width=380,
        height=300,
        show=False,
    )
    spec = chart.to_dict()
    render(page, chart)
    root = svg_root(page)
    panels = [
        next(g for g in root.iter() if g.get("data-name") == f"panel-{i}")
        for i in (0, 1)
    ]
    dots = [
        next(g for g in panel.iter() if g.get("data-mark-type") == "point")
        for panel in panels
    ]
    boxes = [
        page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i)
        for i in (0, 1)
    ]
    domains = [
        points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
        for axis in ("x", "y")
    ]
    coordinates = point_coordinates(page)
    nodes = next(
        rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0]
    )
    colors = []
    for node in nodes:
        row = np.flatnonzero(a.obs["cluster"] == node["_group"])[0]
        positions = [a.obsm["X_umap"][row, :2], [node["_x"], node["_y"]]]
        fills = []
        for i, (x, y) in enumerate(positions):
            box = boxes[i]
            target = [
                box["x"] + (x - domains[0][0]) / np.ptp(domains[0]) * box["width"],
                box["y"] + (domains[1][1] - y) / np.ptp(domains[1]) * box["height"],
            ]
            index = np.argmin(np.linalg.norm(coordinates[i] - target, axis=1))
            assert np.linalg.norm(coordinates[i][index] - target) < 1
            fills.append(dots[i][index].get("fill", dots[i].get("fill")))
        assert fills[0] == fills[1] and fills[0] is not None
        colors.append(fills[0])
    assert len(set(colors)) == len(nodes)


@pytest.mark.parametrize("color", [None, "score"])
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_comparison_has_matched_domains_labels_and_native_guides(
    page, tmp_path, color
):
    a = make_compare()
    # Stored non-group layouts can extend beyond the embedding without expanding its limits.
    options = (
        {"color": color, "pos": [[1, 0.1], [2, 0.2], [3, 0.3], [40, 40]]}
        if color
        else {}
    )
    chart = gsc.pl.paga_compare(
        a,
        legend_fontweight="normal",
        show_node_labels=True,
        width=380,
        height=300,
        show=False,
        **options,
    )
    spec = chart.to_dict()
    first = render(page, chart)
    second = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
    assert first["width"] == second["width"] == 380
    assert first["height"] == second["height"] == 300
    assert first["y"] == second["y"]
    assert first["x"] + first["width"] < second["x"]
    domain = [
        points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
        for axis in ("x", "y")
    ]
    root = svg_root(page)
    texts = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert ("score" if color else "cluster") in texts
    assert all(group in texts for group in ("A", "B", "C"))
    circles = point_coordinates(page)
    assert len(circles) == 2
    expected = a.uns["paga"]["pos"]
    expected = expected[
        (expected[:, 0] >= domain[0][0])
        & (expected[:, 0] <= domain[0][1])
        & (expected[:, 1] >= domain[1][0])
        & (expected[:, 1] <= domain[1][1])
    ]
    centers = np.column_stack(
        [
            second["x"]
            + (expected[:, 0] - domain[0][0]) / np.ptp(domain[0]) * second["width"],
            second["y"]
            + (domain[1][1] - expected[:, 1]) / np.ptp(domain[1]) * second["height"],
        ]
    )
    assert len(circles[1]) == len(centers)
    for center in centers:
        assert np.min(np.linalg.norm(circles[1] - center, axis=1)) < 1
    gradients = [e for e in root.iter() if e.tag.endswith("linearGradient")]
    assert bool(gradients) == bool(color)
    page.screenshot(path=str(tmp_path / "comparison.png"), full_page=True)


def test_observation_and_group_hover_shared_zoom_pan_and_offline_html(page, tmp_path):
    a = make_compare()
    chart = gsc.pl.paga_compare(
        a,
        legend_fontweight="normal",
        zoom=True,
        legend_loc="right margin",
        size=144,
        width=380,
        height=300,
        show=False,
    )
    spec = chart.to_dict()
    first = render(page, chart)
    second = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
    domains = [
        points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
        for axis in ("x", "y")
    ]
    xy = a.obsm["X_umap"][3]
    move_to(page, first, *xy[:2], *domains, "cell-3")
    assert page.get_by_text("cell-3", exact=True).first.is_visible()
    node = a.uns["paga"]["pos"][1]
    projected = [
        second["x"] + (node[0] - domains[0][0]) / np.ptp(domains[0]) * second["width"],
        second["y"] + (domains[1][1] - node[1]) / np.ptp(domains[1]) * second["height"],
    ]
    hover_at(page, *projected)
    page.locator("table.attributes").get_by_text("Cells", exact=True).wait_for(
        state="visible"
    )
    assert [
        value.strip()
        for value in page.locator("table.attributes td").all_text_contents()[:3]
    ] == [
        "B",
        "B",
        "4",
    ]
    before = point_coordinates(page)
    canvas = page.locator("canvas").first.bounding_box()
    x, y = canvas["x"] + second["x"] + 190, canvas["y"] + second["y"] + 150
    page.mouse.move(x, y)
    page.mouse.wheel(0, -20)
    page.wait_for_timeout(500)
    zoomed = point_coordinates(page)
    assert all(
        np.ptp(after[:, 0]) > np.ptp(prior[:, 0])
        for prior, after in zip(before, zoomed, strict=True)
    ), (
        before,
        zoomed,
    )
    page.mouse.down()
    page.mouse.move(x + 12, y + 10, steps=5)
    page.mouse.up()
    page.wait_for_timeout(300)
    panned = point_coordinates(page)
    assert all(
        not np.array_equal(left, right)
        for left, right in zip(zoomed, panned, strict=True)
    )
    output = tmp_path / "compare.html"
    chart.save(output, inline=True, controls=False)
    page.route("https://**", lambda route: route.abort())
    page.goto(output.as_uri())
    page.locator("canvas").wait_for(state="visible")
    assert page.locator(".message-box").count() == 0


def test_composed_comparisons_keep_navigation_inside_their_own_pair(page, tmp_path):
    chart = gsc.pl.paga_compare(
        make_compare(),
        legend_fontweight="normal",
        zoom=True,
        width=280,
        height=220,
        show=False,
    )
    combined = (
        gs.vconcat(chart, chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    bounds = render(page, combined)
    names = tuple(f"panel-{i}" for i in range(4))

    def positions():
        locations = point_coordinates(page, names)
        boxes = [
            page.evaluate("name=>api.views.getLayoutBounds({scope:[],view:name})", name)
            for name in names
        ]
        return [
            rows - [box["x"], box["y"]]
            for rows, box in zip(locations, boxes, strict=True)
        ]

    before = positions()
    canvas = page.locator("canvas").first.bounding_box()
    x, y = canvas["x"] + bounds["x"] + 140, canvas["y"] + bounds["y"] + 110
    page.mouse.move(x, y)
    page.mouse.wheel(0, -20)
    page.wait_for_timeout(350)
    zoomed = positions()
    for i in (0, 1):
        assert np.ptp(zoomed[i][:, 0]) > np.ptp(before[i][:, 0])
    for i in (2, 3):
        np.testing.assert_allclose(zoomed[i], before[i], atol=0.2)
    page.mouse.down()
    page.mouse.move(x + 10, y + 8, steps=5)
    page.mouse.up()
    page.wait_for_timeout(250)
    panned = positions()
    assert all(not np.array_equal(panned[i], zoomed[i]) for i in (0, 1))
    for i in (2, 3):
        np.testing.assert_allclose(panned[i], before[i], atol=0.2)
    output = tmp_path / "independent-comparisons.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").wait_for(state="visible")
    assert not page.locator(".message-box").count()


def test_on_data_labels_displace_and_reflow_on_zoom(page):
    from tests.integrations.scanpy.browser.test_grid_interactions import (
        pointer,
        position,
    )
    from tests.integrations.scanpy.helpers import name_embedding_scales

    a = make_compare()
    names = ["Alpha cells", "Beta cells", "Gamma cells", "Delta cells"]
    a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
    xy = np.column_stack(
        [a.obs["cluster"].cat.codes.to_numpy() * 0.1, np.zeros(a.n_obs)]
    )
    xy[:2, 0] = [-10, 10]
    a.obsm["X_umap"] = xy
    chart = gsc.pl.paga_compare(
        a,
        legend_fontweight="normal",
        legend_fontsize=12,
        width=400,
        height=300,
        zoom=True,
        show=False,
    )
    bounds = render(page, name_embedding_scales(chart.to_dict(), "labels"))
    page.wait_for_timeout(1200)

    def label_offsets():
        """Read native label offsets from their median anchors in the current viewport."""
        root = svg_root(page)
        group = next(
            g
            for g in root.iter()
            if g.get("data-mark-type") == "text"
            and g.get("clip-path")
            and {e.text for e in g} == set(names)
        )
        clip_id = group.get("clip-path").removeprefix("url(#").removesuffix(")")
        box = next(e[0] for e in root.iter() if e.get("id") == clip_id)
        domains = page.evaluate(
            "['x-0', 'y-1'].map(n=>api.getScaleResolutionByName('labels-'+n).getDomain())"
        )
        offsets = {}
        for element in group:
            i = names.index(element.text)
            anchor = np.array(
                [
                    float(box.get("x"))
                    + (i * 0.1 - domains[0][0])
                    / np.ptp(domains[0])
                    * float(box.get("width")),
                    float(box.get("y"))
                    + domains[1][1] / np.ptp(domains[1]) * float(box.get("height")),
                ]
            )
            offsets[element.text] = np.array(position(element)) - anchor
        return offsets

    before = label_offsets()
    assert set(before) == set(names)
    assert max(np.linalg.norm(value) for value in before.values()) > 10
    pointer(page, bounds)
    page.mouse.wheel(0, -600)
    page.wait_for_timeout(1200)
    after = label_offsets()
    assert set(after) == set(before)
    assert any(np.linalg.norm(after[key] - before[key]) > 1 for key in names)


def test_long_group_key_fits_below_a_notebook_sized_comparison(page):
    from tests.integrations.scanpy.browser.test_grid_interactions import position

    a = make_compare()
    names = [
        "CD4+/CD45RA+/CD25- Naive T",
        "CD4+/CD45RO+ Memory",
        "CD8+ Cytotoxic T",
        "CD14+ Monocyte",
    ]
    a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
    chart = gsc.pl.paga_compare(
        a, legend_fontweight="normal", width=300, height=300, show=False
    )
    render(page, chart)
    assert page.evaluate("api.getLogicalCanvasSize().width") <= 786
    root = svg_root(page)
    key = [
        e
        for g in root.iter()
        if g.get("data-mark-type") == "text" and not g.get("clip-path")
        for e in g
        if e.text in names
    ]
    assert {e.text for e in key} == set(names)
    bottom = max(
        float(e[0].get("y")) + float(e[0].get("height"))
        for e in root.iter()
        if e.tag.endswith("clipPath")
    )
    assert all(position(e)[1] > bottom for e in key)
