"""Observe native ruler and point-outline feedback on existing grid marks."""

import pytest

from tests.integrations.scanpy.browser.interactions import (
    pointer,
    ruler_lines,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.grid_fixture_support import FAMILIES, make_chart


def mark_centers(root, bounds):
    centers = []
    for e in root.iter():
        if e.tag.endswith("circle") and e.get("fill", "").startswith("rgb"):
            x, y = float(e.get("cx")), float(e.get("cy"))
        elif e.tag.endswith("rect") and e.get("fill", "").startswith("rgb"):
            x = float(e.get("x")) + float(e.get("width")) / 2
            y = float(e.get("y")) + float(e.get("height")) / 2
        else:
            continue
        fx, fy = (
            (x - bounds["x"]) / bounds["width"],
            (y - bounds["y"]) / bounds["height"],
        )
        if 0 < fx < 1 and 0 < fy < 1:
            centers.append((fx, fy))
    return sorted(centers)


def outlines(root):
    return [
        e
        for e in root.iter()
        if e.tag.endswith(("rect", "circle"))
        and e.get("stroke", "").replace(" ", "") in ("#0f172a", "rgb(15,23,42)")
        and float(e.get("stroke-width", 0)) == 1.5
    ]


@pytest.mark.parametrize("family", FAMILIES)
def test_native_ruler_is_opt_in_and_clears_on_leave(page, family):
    from io import BytesIO

    import numpy as np
    from PIL import Image

    chart = make_chart(family, highlight=True, hover=False)
    bounds = render(page, chart, scale_prefix=family)
    before = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
    pointer(page, bounds)
    page.wait_for_function("api.getParam('grid_cursor').getValue().values.x !== null")
    page.evaluate(
        "() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))"
    )
    after = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
    canvas = page.locator("canvas").first.bounding_box()
    dpr = page.evaluate("devicePixelRatio")
    x, y = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    changed = (np.abs(after - before).max(axis=2) > 12)[
        round(y * dpr) : round((y + bounds["height"]) * dpr),
        round(x * dpr) : round((x + bounds["width"]) * dpr),
    ]
    assert changed.any(axis=0).mean() > 0.8
    assert changed.any(axis=1).mean() > 0.8
    assert len(ruler_lines(svg_root(page))) == 2
    page.mouse.move(1790, 1390)
    page.wait_for_function("api.getParam('grid_cursor').getValue().values.x === null")
    assert not ruler_lines(svg_root(page))


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("hover", [False, True])
def test_native_outline_export_follows_one_mark_without_affecting_values(
    page, family, hover
):
    chart = make_chart(
        family,
        highlight="outline",
        hover=hover,
        zoom="xy",
        **({"show_values": True} if family != "dotplot" else {}),
    )
    try:
        bounds = render(page, chart, scale_prefix=family)
    except Exception as error:
        pytest.fail(f"{error}\n{page.locator('body').inner_text()[:2500]}")
    assert not outlines(svg_root(page))
    initial_labels = sorted(e.text for e in value_texts(svg_root(page)))
    selected = []
    centers = mark_centers(svg_root(page), bounds)
    assert len(centers) >= 2
    for center in centers[:2]:
        pointer(page, bounds, *center)
        page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId != null")
        root = svg_root(page)
        assert len(outlines(root)) == 1
        selected.append(page.evaluate("api.getParam('grid_hover').getValue().uniqueId"))
        assert sorted(e.text for e in value_texts(root)) == initial_labels
        assert all(float(e.get("stroke-width", 0)) == 0 for e in value_texts(root))
    assert selected[0] != selected[1]
    page.mouse.wheel(0, -220)
    page.wait_for_timeout(180)
    pointer(page, bounds, *mark_centers(svg_root(page), bounds)[0])
    page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId != null")
    assert len(outlines(svg_root(page))) == 1


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("hover", [False, True])
def test_outline_clears_when_leaving_the_live_plot(page, family, hover):
    chart = make_chart(
        family,
        highlight="outline",
        hover=hover,
        **({"show_values": True} if family != "dotplot" else {}),
    )
    bounds = render(page, chart, scale_prefix=family)
    centers = mark_centers(svg_root(page), bounds)[:2]
    selected = []
    for center in centers:
        pointer(page, bounds, *center)
        page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId != null")
        selected.append(page.evaluate("api.getParam('grid_hover').getValue().uniqueId"))
    assert selected[0] != selected[1]
    page.mouse.move(1790, 1390)
    page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId == null")
    assert not outlines(svg_root(page))


def test_outline_clears_after_native_svg_export(page):
    chart = make_chart("dotplot", highlight="outline", hover=False)
    bounds = render(page, chart, scale_prefix="dotplot")
    pointer(page, bounds, *mark_centers(svg_root(page), bounds)[0])
    page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId != null")
    assert len(outlines(svg_root(page))) == 1
    page.mouse.move(1790, 1390)
    page.wait_for_timeout(100)
    assert page.evaluate("api.getParam('grid_hover').getValue().uniqueId") is None


@pytest.mark.parametrize("page", [3], indirect=True)
@pytest.mark.parametrize("show_values", [False, True])
def test_hovered_tile_has_equal_visible_strokes_on_all_four_edges(page, show_values):
    from io import BytesIO

    import numpy as np
    from PIL import Image

    import genome_spy.integrations.scanpy as gsc

    chart = gsc.pl.matrix(
        np.ones((3, 3)),
        highlight="outline",
        hover=False,
        show_values=show_values,
        width=240,
        height=240,
        show=False,
    )
    bounds = render(page, chart, scale_prefix="matrix")
    root = svg_root(page)
    rects = [
        e
        for e in root.iter()
        if e.tag.endswith("rect")
        and e.get("fill", "").startswith("rgb")
        and bounds["x"] - 0.5 <= float(e.get("x")) < bounds["x"] + bounds["width"]
        and bounds["y"] - 0.5 <= float(e.get("y")) < bounds["y"] + bounds["height"]
    ]
    assert len(rects) == 9
    tile = sorted(rects, key=lambda e: (float(e.get("x")), float(e.get("y"))))[4]
    x, y, width, height = (
        float(tile.get(key)) for key in ("x", "y", "width", "height")
    )
    before = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
    pointer(
        page,
        bounds,
        (x + width / 2 - bounds["x"]) / bounds["width"],
        (y + height / 2 - bounds["y"]) / bounds["height"],
    )
    page.wait_for_function("api.getParam('grid_hover').getValue().uniqueId != null")
    page.evaluate(
        "() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))"
    )
    after = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
    changed = np.abs(after - before).max(axis=2) > 12
    canvas = page.locator("canvas").first.bounding_box()
    dpr = page.evaluate("devicePixelRatio")
    x, y = x + canvas["x"], y + canvas["y"]

    def edge_width(left, top, right, bottom, *, vertical):
        region = changed[
            round(top * dpr) : round(bottom * dpr),
            round(left * dpr) : round(right * dpr),
        ]
        return region.sum() / (region.shape[0 if vertical else 1] * dpr)

    edges = {
        "left": edge_width(
            x - 3, y + height * 0.25, x + 3, y + height * 0.75, vertical=True
        ),
        "right": edge_width(
            x + width - 3,
            y + height * 0.25,
            x + width + 3,
            y + height * 0.75,
            vertical=True,
        ),
        "top": edge_width(
            x + width * 0.25, y - 3, x + width * 0.75, y + 3, vertical=False
        ),
        "bottom": edge_width(
            x + width * 0.25,
            y + height - 3,
            x + width * 0.75,
            y + height + 3,
            vertical=False,
        ),
    }
    assert min(edges.values()) >= 1, edges
    assert max(edges.values()) - min(edges.values()) <= 1 / dpr + 0.1, edges
