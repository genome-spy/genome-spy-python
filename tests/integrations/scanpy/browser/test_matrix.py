"""Registered matrix colors/labels, native hover and standalone HTML delivery."""

from io import BytesIO
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.matrix_fixture import matrix_cases

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "matrix.json").read_text())["cases"]


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
