"""Registered matrix colors/labels, native hover and standalone HTML delivery."""

import json
import re
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    pointer,
    position,
    svg_root,
)
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.expression_fixtures import matrix_cases
from tests.integrations.scanpy.paga_fixtures import make_adjacency

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "matrix.json").read_text())["cases"]


@pytest.mark.parametrize("family", ["matrix", "paga_adjacency"])
@pytest.mark.parametrize("zoom", [True, "xy"])
def test_composition_keeps_native_matrix_navigation_independent(
    page, tmp_path, family, zoom
):
    source = make_adjacency()
    if family == "matrix":
        source = source.uns["connectivities"].toarray()
    chart = getattr(gsc.pl, family)(
        source, zoom=zoom, show_values=True, width=280, height=240, show=False
    )
    combined = (
        (chart | chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    bounds = render(page, combined)

    def rectangles():
        """Read tile geometry relative to each panel so guide resizing cannot mimic zoom."""
        groups = [
            g
            for g in svg_root(page).iter()
            if g.get("data-mark-type") == "rect" and g.get("clip-path")
        ]
        assert len(groups) == 2
        result = []
        for i, group in enumerate(groups):
            panel = page.evaluate(
                "i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i
            )
            values = np.array(
                [
                    [float(e.get(k)) for k in ("x", "y", "width", "height")]
                    for e in group
                ]
            )
            values[:, :2] -= [panel["x"], panel["y"]]
            result.append(values)
        return result

    before = rectangles()
    assert all(len(rows) == 9 for rows in before)
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -120)
    page.wait_for_timeout(700)
    zoomed = rectangles()
    assert not np.array_equal(zoomed[0], before[0])
    np.testing.assert_allclose(zoomed[1], before[1], atol=0.01)
    assert bool(zoomed[0][0, 2] > before[0][0, 2] + 1) is (zoom == "xy")
    assert zoomed[0][0, 3] > before[0][0, 3] + 1
    page.mouse.down()
    page.mouse.move(px + 8, py + 8, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    panned = rectangles()
    assert not np.array_equal(panned[0], zoomed[0])
    np.testing.assert_allclose(panned[1], before[1], atol=0.01)
    other = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
    hover_at(
        page, other["x"] + other["width"] * 5 / 6, other["y"] + other["height"] / 6
    )
    values = [
        v.strip() for v in page.locator("table.attributes td").all_text_contents()
    ]
    assert values[:2] == ["0", "2"]
    assert float(values[2]) == pytest.approx(0.6)
    output = tmp_path / f"{family}-composition.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("page", [1, 2], indirect=True)
@pytest.mark.parametrize("zoom", [True, "xy"])
def test_matrix_side_labels_follow_zoom_pan_and_resize(page, zoom):
    spec = gsc.pl.matrix(
        np.arange(144).reshape(12, 12),
        xticks=[f"gene{i}" for i in range(12)],
        yticks=[f"group{i}" for i in range(12)],
        zoom=zoom,
        show=False,
    ).to_dict()
    for side in ("bottom", "left"):
        spec["surround"][side][0]["name"] = f"test-{side}"
    for axis in ("x", "y"):
        spec["scales"][axis]["name"] = f"matrix-{axis}"
    for width, height in ((240, 200), (400, 280)):
        spec["spec"].update(width=width, height=height)
        bounds = render(page, gs.TopLevelSpec.from_dict(spec))
        original = page.evaluate("api.getScaleResolutionByName('matrix-x').getDomain()")
        for navigated in (False, True):
            if navigated:
                px, py = pointer(page, bounds)
                page.mouse.wheel(0, -250)
                page.wait_for_timeout(250)
                page.mouse.down()
                page.mouse.move(px + 15, py + 15, steps=5)
                page.mouse.up()
                page.wait_for_timeout(700)
            root = svg_root(page)
            for axis, side, prefix in (("x", "bottom", "gene"), ("y", "left", "group")):
                track = page.evaluate(
                    "view=>api.views.getLayoutBounds({scope:[],view})", f"test-{side}"
                )
                assert track["width" if axis == "x" else "height"] == pytest.approx(
                    bounds["width" if axis == "x" else "height"]
                )
                centers = page.evaluate(
                    """axis=>{const s=api.getScaleResolutionByName(`matrix-${axis}`).getScale();
                    return Array.from({length:12},(_,i)=>axis==='x'
                        ?s(i)+s.bandwidth()/2:1-s(i)+s.bandwidth()/2)}""",
                    axis,
                )
                labels = [
                    e
                    for e in root.iter()
                    if e.tag.endswith("text") and (e.text or "").startswith(prefix)
                ]
                assert labels
                for label in labels:
                    slot = int(label.text.removeprefix(prefix))
                    xy = position(label)
                    value = xy[0 if axis == "x" else 1]
                    assert value == pytest.approx(
                        bounds[axis]
                        + centers[slot] * bounds["width" if axis == "x" else "height"],
                        abs=0.6,
                    ), (
                        label.text,
                        navigated,
                        bounds,
                        centers[slot],
                        ET.tostring(label),
                    )
                    # Native clipping can retain a partly visible label's outside anchor.
                    cross, extent = ("y", "height") if axis == "x" else ("x", "width")
                    assert (
                        track[cross]
                        <= xy[1 if axis == "x" else 0]
                        <= track[cross] + track[extent]
                    )
        assert (
            page.evaluate("api.getScaleResolutionByName('matrix-x').getDomain()")
            != original
        ) is (zoom == "xy")


@pytest.mark.parametrize("explicit_labels", [False, True])
@pytest.mark.parametrize("titles", ["both", "x", "y"])
def test_axis_titles_do_not_duplicate_outer_label_space(page, explicit_labels, titles):
    labels = ["CD4+/CD45RA+/CD25- Naive T", "CD8+/CD45RA+ Naive Cytotoxic"]
    chart = gsc.pl.matrix(
        [[0, 1], [2, 3]],
        xticks=labels if explicit_labels else None,
        yticks=labels if explicit_labels else None,
        xlabel="Columns" if titles in ("both", "x") else None,
        ylabel="Rows" if titles in ("both", "y") else None,
        width=400,
        height=350,
        show=False,
    )
    bounds = render(page, chart)
    assert abs(bounds["width"] - 400) < 1
    assert abs(bounds["height"] - 350) < 1
    root = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    positions = {
        e.text: [
            float(v)
            for v in re.search(r"translate\(([^)]+)\)", e.get("transform"))
            .group(1)
            .split()
        ]
        for e in root.iter()
        if e.tag.endswith("text") and e.text in ("Rows", "Columns")
    }
    canvas_height = page.evaluate("api.getLogicalCanvasSize().height")
    if "Rows" in positions:
        assert 0 < positions["Rows"][0] < 35
    if "Columns" in positions:
        assert 0 < canvas_height - positions["Columns"][1] < 35


@pytest.mark.reference
@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", matrix_cases())
def test_complete_matrix_tiles_and_labels(page, tmp_path, reference_images, case):
    values, options = matrix_cases()[case]
    reference = REFERENCE[case]
    chart = gsc.pl.matrix(
        values,
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        show=False,
        **options,
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": canvas["x"] + bounds["x"],
                    "y": canvas["y"] + bounds["y"],
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    expected = Image.open(
        reference_images("matrix") / f"matrix-{case}-panel.png"
    ).convert("RGB")
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    pixels, target = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    for row, column in np.ndindex(values.shape):
        for fraction in (0.25, 0.75):
            x, y = (
                (column + fraction) / values.shape[1],
                (row + fraction) / values.shape[0],
            )
            np.testing.assert_allclose(
                pixels[int(y * actual.height), int(x * actual.width)],
                target[int(y * expected.height), int(x * expected.width)],
                atol=12,
            )
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    (tmp_path / f"{case}.svg").write_text(svg)
    gradients = [
        element
        for element in ET.fromstring(svg).iter()
        if element.tag.endswith("rect") and element.get("fill", "").startswith("url(")
    ]
    assert gradients, svg[-2000:]
    assert (
        abs(
            float(gradients[0].get("height"))
            - reference["plot_size"][1] * options.get("colorbar_shrink", 0.5)
        )
        < 2
    )
    assert float(gradients[0].get("x")) > bounds["x"] + bounds["width"]
    assert float(gradients[0].get("y")) + float(
        gradients[0].get("height")
    ) / 2 == pytest.approx(bounds["y"] + bounds["height"] / 2, abs=1)
    for label in (
        list(options.get("xticks", []))
        + list(options.get("yticks", []))
        + [reference["title"], reference["xlabel"], reference["ylabel"]]
    ):
        if label:
            assert f">{label}<" in svg
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


def test_matrix_hover_resize_and_offline_delivery(page, tmp_path):
    chart = gsc.pl.matrix(
        [[0, 1, 2], [3, 4, 5]],
        xticks=["A", "B", "C"],
        yticks=["first", "last"],
        show=False,
    )
    for size in (300, 450):
        bounds = render(page, chart.properties(width=size, height=size * 2 / 3))
        canvas = page.locator("canvas").first.bounding_box()
        px = canvas["x"] + bounds["x"] + bounds["width"] / 2
        py = canvas["y"] + bounds["y"] + bounds["height"] * 0.75
        page.mouse.move(px - 2, py - 2)
        page.wait_for_timeout(450)
        for dx in (0, 1, -1):
            page.mouse.move(px + dx, py)
            page.wait_for_timeout(80)
            if page.locator("table.attributes").is_visible():
                break
        page.locator("table.attributes").wait_for(state="visible")
        hover_values = [
            row.locator("td").inner_text().strip()
            for row in page.locator("table.attributes tr").all()
        ]
        assert hover_values[:2] == ["last", "B"]
        assert float(hover_values[2]) == 4
    output = tmp_path / "matrix.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
