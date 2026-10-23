"""Native MatrixPlot tree/style/guide chains render complete aligned tiles."""

import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
from PIL import Image
import pytest

from tests.integrations.scanpy.browser.test_dotplot_builder import builder
from tests.integrations.scanpy.browser.test_grid_interactions import pointer
from tests.integrations.scanpy.browser.test_umap import render


@pytest.mark.parametrize("swapped", [False, True])
def test_tree_chain_renders_styles_guides_and_complete_labels(page, swapped):
    chart = (
        builder("MatrixPlot")
        .add_dendrogram(size=0.6)
        .swap_axes(swap_axes=swapped)
        .legend(title="Scaled mean", width=1.8)
        .to_chart()
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(360, abs=1)
    assert bounds["height"] == pytest.approx(260, abs=1)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert all(
        label in svg
        for label in ("First", "Again", "g1", "g2", "C", "A", "D", "B", "Scaled mean")
    )
    track = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'matrixplot-tree'})"
    )
    assert track["height" if swapped else "width"] == pytest.approx(60, abs=1)
    root = ET.fromstring(svg)
    tiles = [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("rgb(")
    ]
    assert len(tiles) == 12
    columns, rows = (4, 3) if swapped else (3, 4)
    assert all(
        float(e.get("width")) == pytest.approx(360 / columns, abs=0.1) for e in tiles
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
