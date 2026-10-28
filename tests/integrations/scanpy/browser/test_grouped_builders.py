"""Headless native grouped-builder chains, totals, composition and export."""

import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from tests.integrations.scanpy.browser.interactions import hover_at, pointer
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.grid_fixture_support import builder
from tests.integrations.scanpy.helpers import index_position


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_tree_chain_renders_complete_labels_guides_and_native_styling(
    page, family, swapped
):
    legend = (
        {"size_title": "Expressing cells", "colorbar_title": "Group mean"}
        if family == "DotPlot"
        else {"title": "Group mean"}
    )
    chart = (
        builder(family)
        .add_dendrogram(size=0.6)
        .swap_axes(swap_axes=swapped)
        .legend(width=1.8, **legend)
        .to_chart()
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(360, abs=1)
    assert bounds["height"] == pytest.approx(260, abs=1)
    root = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    labels = {e.text for e in root.iter() if e.tag.endswith("text")}
    assert {
        "First",
        "Again",
        "g1",
        "g2",
        "C",
        "A",
        "D",
        "B",
        *legend.values(),
    } <= labels
    track = page.evaluate(
        "name=>api.views.getLayoutBounds({scope:[],view:name})",
        f"{family.lower()}-tree",
    )
    assert track["height" if swapped else "width"] == pytest.approx(60, abs=1)
    if family == "DotPlot":
        assert any(e.get("stroke") == "navy" for e in root.iter())
        assert any(e.get("stroke") == "gray" for e in root.iter())
    else:
        tiles = [
            e
            for e in root.iter()
            if e.tag.endswith("rect") and e.get("fill", "").startswith("rgb(")
        ]
        assert len(tiles) == 12
        columns, rows = (4, 3) if swapped else (3, 4)
        assert all(
            float(e.get("width")) == pytest.approx(360 / columns, abs=0.1)
            for e in tiles
        )
        assert all(
            float(e.get("height")) == pytest.approx(260 / rows, abs=0.1) for e in tiles
        )
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        x = round(bounds["x"] + bounds["width"] / columns)
        y = round(bounds["y"] + bounds["height"] / rows / 2)
        assert (
            np.abs(pixels[y, x - 1 : x + 2].astype(int) - [0, 0, 128]).max(axis=1).min()
            <= 8
        )
    pointer(page, bounds)
    page.mouse.wheel(0, -250)
    page.wait_for_timeout(300)
    assert page.locator(".message-box").count() == 0


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
def test_totals_paint_counts_and_remain_aligned_while_zooming(
    page, swapped, tmp_path, family
):
    chart = (
        builder(family)
        .add_totals(sort="descending", color="steelblue", size=1)
        .swap_axes(swap_axes=swapped)
        .legend(show=False)
        .to_chart()
    )
    spec = chart.to_dict()
    bounds = render(page, chart, scale_prefix="counts")
    track = page.evaluate(
        "name=>api.views.getLayoutBounds({scope:[],view:name})",
        f"{family.lower()}-totals",
    )
    assert track["height" if swapped else "width"] == pytest.approx(100, abs=1)
    assert track["width" if swapped else "height"] == pytest.approx(
        bounds["width" if swapped else "height"], abs=0.01
    )
    # Every fixture group has two cells, so a point halfway along a bar is inside it.
    slot_axis = "x" if swapped else "y"
    slot = index_position(
        0.5,
        4,
        spec["scales"][slot_axis]["paddingOuter"],
        bounds["width" if swapped else "height"],
    )
    px = bounds["x"] + slot if swapped else track["x"] + track["width"] / 3
    py = track["y"] + track["height"] * 2 / 3 if swapped else bounds["y"] + slot
    page.screenshot(path=str(tmp_path / "totals.png"))
    (tmp_path / "totals.svg").write_text(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    np.testing.assert_allclose(pixels[round(py), round(px)], [70, 130, 180], atol=2)
    hover_at(page, px, py)
    page.locator("table.attributes").wait_for(state="visible")
    assert [
        text.strip() for text in page.locator("table.attributes td").all_text_contents()
    ] == ["C", "2"]
    root = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    assert (
        sum(
            element.text == "2"
            for element in root.iter()
            if element.tag.endswith("text")
        )
        == 4
    )
    domains = "['x','y'].map(a=>api.getScaleResolutionByName('counts-'+a).getDomain())"
    before = page.evaluate(domains)
    pointer(page, bounds)
    page.mouse.wheel(0, -280)
    page.wait_for_timeout(300)
    after = page.evaluate(domains)
    assert all(a[1] - a[0] < b[1] - b[0] for a, b in zip(after, before, strict=True))
    # Native side tracks inherit the same slot resolution after navigation.
    root = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    texts = [element for element in root.iter() if element.tag.endswith("text")]
    assert any(element.text in {"C", "A", "D", "B"} for element in texts)
    assert any(element.text == "2" for element in texts)


@pytest.mark.parametrize("family", ["DotPlot", "MatrixPlot"])
def test_native_snapshots_compose_and_navigate_independently(page, tmp_path, family):
    plot = builder(family)
    left = plot.legend(show=False).to_chart()
    right = plot.swap_axes().legend(show=False).to_chart()
    assert all(
        "name" not in axis
        for chart in (left, right)
        for axis in chart.to_dict()["scales"].values()
    )
    combined = (
        (left | right)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    spec = combined.to_dict()
    for prefix, child in zip(("first", "second"), spec["hconcat"], strict=True):
        for axis in ("x", "y"):
            child["scales"][axis]["name"] = f"{prefix}-{axis}"
    bounds = render(page, spec)
    domains = "['first-x','first-y','second-x','second-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
    before = page.evaluate(domains)
    pointer(page, bounds)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(300)
    after = page.evaluate(domains)
    assert after[0] != before[0] and after[1] != before[1]
    assert after[2:] == before[2:]
    # Export the untouched production composition too, with no test scale names.
    output = tmp_path / "dotplot-builders.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert page.locator(".message-box").count() == 0
