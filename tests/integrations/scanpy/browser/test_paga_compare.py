"""Observe aligned PAGA comparison panels, default labels and linked navigation."""

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import svg_root
from tests.integrations.scanpy.helpers import points
from tests.integrations.scanpy.test_paga_compare import make_compare


def point_coordinates(page):
    """Read plot circles inside named panels, excluding their sibling legend views."""
    root = svg_root(page)
    result = []
    for name in ("panel-0", "panel-1"):
        panel = next(group for group in root.iter() if group.get("data-name") == name)
        group = next(
            group for group in panel.iter() if group.get("data-mark-type") == "point"
        )
        result.append(
            np.array([[float(p.get("cx")), float(p.get("cy"))] for p in group])
        )
    return result


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
        a, legend_fontweight="normal", width=380, height=300, show=False, **options
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
        page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()"),
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
