"""Observed tree geometry, complete labels/guides, hover and offline delivery."""

from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.dendrogram_fixture import (
    make_tree_adata,
    tree_plot_cases,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "dendrogram.json").read_text())


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", tree_plot_cases())
def test_registered_branches_and_complete_charts(page, tmp_path, case):
    reference = REFERENCE["charts"][case]
    family, options = tree_plot_cases()[case]
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        groupby="group",
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        show=False,
        **options,
    )
    if family in ("dotplot", "matrixplot"):
        chart = chart.properties(title="Grouped markers")
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for text in set(reference["x_labels"] + reference["y_labels"]):
        if text:
            assert f">{text}<" in svg
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    width, height = bounds["width"], bounds["height"]
    n = 4
    swapped = options.get("swap_axes", False)

    def project(point):
        x, y = point
        if family == "dendrogram":
            xd, yd = reference["x_domain"], reference["y_domain"]
            return left + (x - xd[0]) / (xd[1] - xd[0]) * width, top + (
                1 - (y - yd[0]) / (yd[1] - yd[0])
            ) * height
        if family == "correlation_matrix":
            low, high = sorted(reference["tree_x_domain"])
            return left - 8 - (x - low) / (
                high - low
            ) * 180, top + height - y / n * height
        if swapped:
            low, high = sorted(reference["tree_y_domain"])
            pad = 0.3 if family == "dotplot" else 0
            return left + (x + pad) / (n + 2 * pad) * width, top - 8 - (y - low) / (
                high - low
            ) * 80
        low, high = sorted(reference["tree_x_domain"])
        pad = 0.5 if family == "dotplot" else 0
        return left + width + 8 + (x - low) / (high - low) * 80, top + (y + pad) / (
            n + 2 * pad
        ) * height

    for path in reference["tree_paths"]:
        for start, end in zip(path[:-1], path[1:], strict=True):
            for fraction in (0.25, 0.5, 0.75):
                point = np.array(start) + (np.array(end) - start) * fraction
                x, y = project(point)
                px, py = round(x * 1.5), round(y * 1.5)
                region = pixels[py - 3 : py + 4, px - 3 : px + 4].astype(int)
                assert region.size and np.any(np.abs(region - 85).max(axis=2) < 40), (
                    case,
                    point,
                )
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={"x": left, "y": top, "width": width, "height": height}
            )
        )
    ).convert("RGB")
    expected = Image.open(FIXTURES / f"dendrogram-{case}-panel.png").convert("RGB")
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    if family in ("matrixplot", "correlation_matrix"):
        values = np.array(reference["values"])
        for row, column in np.ndindex(values.shape):
            # Stay clear of numeric labels and antialiased tile borders.
            x = round((column + 0.2) / values.shape[1] * actual.width)
            y = round((row + 0.2) / values.shape[0] * actual.height)
            np.testing.assert_allclose(
                np.asarray(actual)[y, x].astype(int),
                np.asarray(expected)[y, x].astype(int),
                atol=12,
            )
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    (tmp_path / f"{case}-complete.svg").write_text(svg)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("size", [(240, 180), (480, 300)])
def test_tree_alignment_survives_resizing_and_wheel(page, family, swapped, size):
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        ["g1", "g2"],
        "group",
        dendrogram=True,
        swap_axes=swapped,
        width=size[0],
        height=size[1],
        show=False,
    )
    bounds = render(page, chart)
    before = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] / 2,
        canvas["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -300)
    page.evaluate(
        "async () => { await new Promise(requestAnimationFrame); await new Promise(requestAnimationFrame); }"
    )
    assert (
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()") == before
    )
    # Endpoints at distance zero land at the same centers as summary marks.
    svg = page.evaluate("""async () => {
        const text=await (await api.imageExport.svg()).blob.text();
        const host=document.createElement('div');host.innerHTML=text;
        return [...host.querySelectorAll('line')].filter(e=>e.closest('[stroke]')?.getAttribute('stroke')==='#555555').map(e=>[+e.getAttribute('x1'),+e.getAttribute('y1'),+e.getAttribute('x2'),+e.getAttribute('y2')]);
    }""")
    assert len(svg) == 9
    points = np.array(svg).reshape(-1, 2)
    pad = (0.3 if swapped else 0.5) if family == "dotplot" else 0
    axis = 0 if swapped else 1
    targets = (np.arange(4) + 0.5 + pad) / (4 + 2 * pad) * bounds[
        "width" if swapped else "height"
    ] + bounds["x" if swapped else "y"]
    for position in targets:
        assert np.abs(points[:, axis] - position).min() < 1.5


def test_correlation_hover_palette_direction_and_offline_output(page, tmp_path):
    chart = gsc.pl.correlation_matrix(
        make_tree_adata(), "group", width=240, height=240, show=False
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    px = canvas["x"] + bounds["x"] + bounds["width"] / 8
    py = canvas["y"] + bounds["y"] + bounds["height"] * 7 / 8
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.get_by_text("Correlation", exact=True).wait_for(state="visible")
    assert (
        page.locator("table.attributes tr").last.locator("td").inner_text().strip()
        == "1.000"
    )
    pixel = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))[
        round(py), round(px)
    ]
    assert int(pixel[0]) > int(pixel[2]) + 80
    output = tmp_path / "correlation.html"
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
    assert not requests and not page.locator(".message-box").count()


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_attached_tree_keeps_summary_hover_aligned(page, family, swapped):
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        ["g4"],
        "group",
        dendrogram=True,
        swap_axes=swapped,
        width=240,
        height=180,
        show=False,
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    columns, rows = (4, 1) if swapped else (1, 4)
    xpad, ypad = (0.3, 0.5) if family == "dotplot" else (0, 0)
    px = (
        canvas["x"]
        + bounds["x"]
        + (0.5 + xpad) / (columns + 2 * xpad) * bounds["width"]
    )
    py = canvas["y"] + bounds["y"] + (0.5 + ypad) / (rows + 2 * ypad) * bounds["height"]
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.get_by_text("Mean expression", exact=True).wait_for(state="visible")
    values = [
        row.locator("td").inner_text().strip()
        for row in page.locator("table.attributes tr").all()
    ]
    assert values[:3] == [
        "g4",
        REFERENCE["computations"]["default"]["categories_ordered"][0],
        "2.000",
    ]
