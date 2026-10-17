"""Observed native dotplot guides, brackets, complete layout and offline output."""

from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.dotplot_fixture import dotplot_cases
from tests.integrations.scanpy.helpers import points

REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((REFERENCE_DIR / "dotplot.json").read_text())


@pytest.mark.parametrize("swapped", [False, True])
def test_complete_dotplot_labels_guides_and_brackets(page, adata, tmp_path, swapped):
    chart = gsc.pl.dotplot(
        adata,
        {"first": ["g2", "g1"], "again": "g2"},
        "group",
        use_raw=False,
        swap_axes=swapped,
        title="Grouped markers",
        width=300,
        height=180,
        show=False,
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(300, abs=1)
    assert bounds["height"] == pytest.approx(180, abs=1)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for label in [
        "Grouped markers",
        "g2",
        "g1",
        "first",
        "again",
        "B",
        "A",
        "Mean expression",
        "Fraction of cells",
    ]:
        assert label in svg
    page.screenshot(
        path=str(tmp_path / f"dotplot-{swapped}-complete.png"), full_page=True
    )
    (tmp_path / f"dotplot-{swapped}-complete.svg").write_text(svg)


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", dotplot_cases())
def test_registered_dotplot_positions_paints_and_footprints(
    page, adata, tmp_path, case
):
    reference = REFERENCE["cases"][case]
    options = dotplot_cases()[case].copy()
    names = options.pop("var_names", ["g1", "g2", "g3"])
    chart = gsc.pl.dotplot(
        adata,
        names,
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
    expected = Image.open(REFERENCE_DIR / f"dotplot-{case}-panel.png").convert("RGB")
    assert abs(actual.width - expected.width) <= 2
    assert abs(actual.height - expected.height) <= 2
    for (x, y), color, area in zip(
        reference["positions"], reference["colors"], reference["sizes"], strict=True
    ):
        xd, yd = reference["x_domain"], reference["y_domain"]
        px = round((x - xd[0]) / (xd[1] - xd[0]) * bounds["width"] * 1.5)
        py = round((1 - (y - yd[0]) / (yd[1] - yd[0])) * bounds["height"] * 1.5)
        expected_color = np.round(np.array(color[:3]) * 255)
        native = np.asarray(actual).astype(int)
        if area == 0:
            assert np.all(native[py - 1 : py + 2, px - 1 : px + 2] == 255)
            continue
        assert (
            np.abs(native[py - 1 : py + 2, px - 1 : px + 2] - expected_color)
            .max(axis=2)
            .min()
            <= 12
        )

        # Isolated dots occupy at most 31 backing pixels at 150 DPI.
        def diameter(image):
            pixels = np.asarray(
                image.crop((px - 20, py - 20, px + 21, py + 21))
            ).astype(int)
            ink = (pixels.max(axis=2) - pixels.min(axis=2) > 5) | (
                pixels.min(axis=2) < 220
            )
            yy, xx = np.where(ink)
            assert len(xx) > 0
            return np.array([xx.max() - xx.min() + 1, yy.max() - yy.min() + 1])

        np.testing.assert_allclose(diameter(actual), diameter(expected), atol=2)
        np.testing.assert_allclose(
            diameter(actual), np.sqrt(area) * 150 / 72 + 0.2 * 150 / 72, atol=2
        )
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


def test_dotplot_offline_html_and_plain_navigation(page, adata, tmp_path):
    chart = gsc.pl.dotplot(adata, ["g1", "g2"], "group", use_raw=False, show=False)
    spec = chart.to_dict()
    for channel in ("x", "y"):
        points(spec)["encoding"][channel]["scale"]["name"] = f"dotplot-{channel}"
    bounds = render(page, TopLevelSpec.from_dict(spec))
    domains = page.evaluate(
        "['dotplot-x','dotplot-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
    )
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
        page.evaluate(
            "['dotplot-x','dotplot-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
        )
        == domains
    )
    output = tmp_path / "dotplot.html"
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
