"""Headless native DotPlot chains, totals alignment, composition and export."""

from io import BytesIO
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_grid_interactions import pointer
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata
from tests.integrations.scanpy.helpers import index_position


def builder():
    return gsc.pl.DotPlot(
        make_tree_adata(),
        {"First": ["g2", "g1"], "Again": "g2"},
        "group",
        zoom="xy",
        hover=True,
        width=360,
        height=260,
    ).style(
        cmap="viridis",
        dot_edge_color="navy",
        dot_edge_lw=0.7,
        largest_dot=120,
        size_exponent=2,
        grid=True,
    )


@pytest.mark.parametrize("swapped", [False, True])
def test_tree_chain_renders_complete_labels_guides_and_native_styling(page, swapped):
    chart = (
        builder()
        .add_dendrogram(size=0.6)
        .swap_axes(swap_axes=swapped)
        .legend(
            size_title="Expressing cells",
            colorbar_title="Group mean",
            width=1.8,
        )
        .to_chart()
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(360, abs=1)
    assert bounds["height"] == pytest.approx(260, abs=1)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert all(
        label in svg
        for label in (
            "First",
            "Again",
            "g1",
            "g2",
            "C",
            "A",
            "D",
            "B",
            "Expressing cells",
            "Group mean",
        )
    )
    track = page.evaluate("api.views.getLayoutBounds({scope:[],view:'dotplot-tree'})")
    assert track["height" if swapped else "width"] == pytest.approx(60, abs=1)
    root = ET.fromstring(svg)
    assert any(element.get("stroke") == "navy" for element in root.iter())
    assert any(element.get("stroke") == "gray" for element in root.iter())
    pointer(page, bounds)
    page.mouse.wheel(0, -250)
    page.wait_for_timeout(300)
    assert page.locator(".message-box").count() == 0


@pytest.mark.parametrize("swapped", [False, True])
def test_totals_paint_counts_and_remain_aligned_while_zooming(page, swapped, tmp_path):
    chart = (
        builder()
        .add_totals(sort="descending", color="steelblue", size=1)
        .swap_axes(swap_axes=swapped)
        .legend(show=False)
        .to_chart()
    )
    spec = chart.to_dict()
    bounds = render(page, chart, scale_prefix="counts")
    track = page.evaluate("api.views.getLayoutBounds({scope:[],view:'dotplot-totals'})")
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


def test_native_snapshots_compose_and_navigate_independently(page, tmp_path):
    plot = builder()
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
