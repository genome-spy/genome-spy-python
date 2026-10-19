"""Observed matrixplot tiles, color bounds, missing cells, hover and HTML delivery."""

from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.matrixplot_fixture import matrixplot_cases

REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((REFERENCE_DIR / "matrixplot.json").read_text())


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", matrixplot_cases())
def test_registered_matrixplot_tiles_paint_and_grid(
    page, adata, tmp_path, reference_images, case
):
    reference = REFERENCE["cases"][case]
    options = matrixplot_cases()[case].copy()
    chart = gsc.pl.matrixplot(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        "group",
        use_raw=False,
        show=False,
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
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
        reference_images("matrixplot") / f"matrixplot-{case}-panel.png"
    ).convert("RGB")
    assert abs(actual.width - expected.width) <= 2
    assert abs(actual.height - expected.height) <= 2
    values = np.array(reference["values"], dtype=float)
    pixels = np.array(actual).astype(int)
    rows, columns = values.shape
    for row, column in np.ndindex(values.shape):
        px, py = (
            round((column + 0.5) / columns * actual.width),
            round((row + 0.5) / rows * actual.height),
        )
        target = np.asarray(expected)[py, px].astype(int)
        # Palette bins/interpolation differ slightly; missing cells remain white.
        assert np.abs(pixels[py, px] - target).max() <= 12
        if np.isnan(values[row, column]):
            assert pixels[py, px].tolist() == [255, 255, 255]
        # Sample both tile interiors to catch gaps and incorrect band endpoints.
        for fraction in (0.1, 0.9):
            x = round((column + fraction) / columns * actual.width)
            y = round((row + fraction) / rows * actual.height)
            assert np.abs(pixels[y, x] - target).max() <= 12
    if case == "bounds_edges":
        # Compare one isolated vertical grid stroke at the reference export DPI.
        px, py = round(actual.width / columns), round(actual.height / (2 * rows))
        for image in (actual, expected):
            strip = np.asarray(image)[py, px - 5 : px + 6]
            black = (strip.max(axis=1) < 64).sum()
            assert 2 <= black <= 4, (image is actual, strip.tolist())
    actual.save(tmp_path / f"{case}-native.png")
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("hover", [False, True])
def test_matrixplot_hover_identifies_summary_in_both_orientations(
    page, adata, swapped, hover
):
    chart = gsc.pl.matrixplot(
        adata,
        ["g2"],
        "group",
        use_raw=False,
        standard_scale="var",
        swap_axes=swapped,
        hover=hover,
        width=240,
        height=180,
        show=False,
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    columns, rows = (2, 1) if swapped else (1, 2)
    px = canvas["x"] + bounds["x"] + bounds["width"] / (2 * columns)
    py = canvas["y"] + bounds["y"] + bounds["height"] / (2 * rows)
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    page.mouse.move(px, py)
    if hover:
        # Match the one-pixel picking neighborhood used by the UMAP checks.
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            page.mouse.move(px + dx, py + dy)
            page.wait_for_timeout(80)
            if page.locator("table.attributes").is_visible():
                break
        page.get_by_text("Mean expression (scaled)", exact=True).wait_for(
            state="visible"
        )
        assert [
            (row.locator("th").inner_text(), row.locator("td").inner_text().strip())
            for row in page.locator("table.attributes tr").all()
        ] == [
            ("Gene", "g2"),
            ("Group", "B"),
            ("Mean expression (scaled)", "0.000"),
        ]
    else:
        page.wait_for_timeout(150)
        assert page.locator("table.attributes").count() == 0


def test_matrixplot_plain_navigation_and_offline_html(page, adata, tmp_path):
    chart = gsc.pl.matrixplot(adata, ["g1", "g2"], "group", use_raw=False, show=False)
    spec = chart.to_dict()
    for axis in ("x", "y"):
        spec["layer"][0]["encoding"][axis]["scale"]["name"] = f"matrix-{axis}"
    bounds = render(page, TopLevelSpec.from_dict(spec))
    expression = (
        "['matrix-x','matrix-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
    )
    domains = page.evaluate(expression)
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] / 2,
        canvas["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -300)
    page.evaluate(
        "async () => { await new Promise(requestAnimationFrame); await new Promise(requestAnimationFrame); }"
    )
    assert page.evaluate(expression) == domains
    output = tmp_path / "matrixplot.html"
    chart.save(output, inline=True, controls=False)
    requests = []
    page.on(
        "request",
        lambda r: (
            requests.append(r.url) if r.url.startswith(("http:", "https:")) else None
        ),
    )
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not requests
    assert page.locator(".message-box").count() == 0
