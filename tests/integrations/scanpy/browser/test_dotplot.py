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


@pytest.mark.parametrize("swapped,rotation", [(False, None), (False, 0), (True, None)])
def test_complete_dotplot_labels_guides_and_brackets(
    page, adata, tmp_path, swapped, rotation
):
    chart = gsc.pl.dotplot(
        adata,
        {"first markers": ["g2", "g1"], "again": "g2"},
        "group",
        use_raw=False,
        swap_axes=swapped,
        var_group_rotation=rotation,
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
        "first markers",
        "again",
        "B",
        "A",
        "Mean expression",
        "Fraction of cells",
    ]:
        assert label in svg
    labels = page.evaluate(
        """async svg => {
        const host = document.createElement('div');
        host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
        host.innerHTML = svg;
        document.body.append(host);
        await document.fonts.ready;
        const labels = [...host.querySelectorAll('text')].map(element => {
            const rect = element.getBoundingClientRect();
            return {text:element.textContent, x:rect.x, y:rect.y,
                    width:rect.width, height:rect.height};
        });
        host.remove();
        return labels;
    }""",
        svg,
    )
    bottom = bounds["y"] + bounds["height"]
    right = bounds["x"] + bounds["width"]
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    assert [label["text"] for label in labels].count("g2") == 2
    for text in ["first markers", "again"]:
        assert [label["text"] for label in labels].count(text) == 1
    for title, tick in [
        ("Fraction of cells in group (%)", "30"),
        ("Mean expression in group", "1.0"),
    ]:
        heading = next(label for label in labels if label["text"] == title)
        entry = next(label for label in labels if label["text"] == tick)
        assert entry["y"] >= heading["y"] + heading["height"]
    for label in labels:
        if label["text"] in (["B", "A"] if swapped else ["g1", "g2"]):
            assert label["y"] >= bottom + 6
        if label["text"] in (["g1", "g2"] if swapped else ["B", "A"]):
            assert label["x"] + label["width"] <= bounds["x"] - 6
        if label["text"] in {"first markers", "again"}:
            # Bracket centers follow the covered slots, independent of text length.
            slot = 0.95 if label["text"] == "first markers" else 2.45
            if swapped:
                expected = bounds["y"] + (slot + 0.5) / 4 * bounds["height"]
                assert label["y"] + label["height"] / 2 == pytest.approx(
                    expected, abs=2
                )
                assert label["x"] >= right + 6
                px, py = round(right + 4), round(expected)
            else:
                expected = bounds["x"] + (slot + 0.3) / 3.6 * bounds["width"]
                assert label["x"] + label["width"] / 2 == pytest.approx(expected, abs=2)
                assert label["y"] + label["height"] <= bounds["y"] - 6
                px, py = round(expected), round(bounds["y"] - 4)
            assert pixels[py - 1 : py + 2, px - 1 : px + 2].min() < 64
    page.screenshot(
        path=str(tmp_path / f"dotplot-{swapped}-complete.png"), full_page=True
    )
    (tmp_path / f"dotplot-{swapped}-complete.svg").write_text(svg)


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("hover", [False, True])
def test_dotplot_hover_reports_summary_values(page, adata, swapped, hover):
    chart = gsc.pl.dotplot(
        adata,
        ["g2"],
        "group",
        use_raw=False,
        swap_axes=swapped,
        dot_max=0.4,
        hover=hover,
        width=240,
        height=180,
        show=False,
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    columns, rows = (2, 1) if swapped else (1, 2)
    px = canvas["x"] + bounds["x"] + 0.8 / (columns + 0.6) * bounds["width"]
    py = canvas["y"] + bounds["y"] + 1 / (rows + 1) * bounds["height"]
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    page.mouse.move(px, py)
    if hover:
        page.get_by_text("Expressing cells (%)", exact=True).wait_for(state="visible")
        rows = page.locator("table.attributes tr").all()
        assert [
            (row.locator("th").inner_text(), row.locator("td").inner_text().strip())
            for row in rows
        ] == [
            ("Gene", "g2"),
            ("Group", "B"),
            ("Mean expression", "1.000"),
            ("Expressing cells (%)", "66.7"),
        ]
    else:
        page.wait_for_timeout(150)
        assert page.locator("table.attributes").count() == 0


def test_pbmc_marker_brackets_paint_single_and_multiple_gene_spans(page):
    import scanpy as sc

    markers = {
        "B-cell": ["CD79A", "MS4A1"],
        "Dendritic": ["FCER1A", "CST3"],
        "Monocytes": ["FCGR3A"],
        "NK": ["GNLY", "NKG7"],
        "Other": ["IGLL1"],
        "Plasma": ["IGJ"],
        "T-cell": ["CD3D"],
    }
    chart = gsc.pl.dotplot(
        sc.datasets.pbmc68k_reduced(),
        markers,
        "bulk_labels",
        width=400,
        height=350,
        show=False,
    )
    bounds = render(page, chart)
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    start = 0
    for genes in markers.values():
        midpoint = start + (len(genes) - 1) / 2 + 0.45
        px = round(bounds["x"] + (midpoint + 0.3) / 10.6 * bounds["width"])
        py = round(bounds["y"] - 4)
        assert pixels[py - 1 : py + 2, px - 1 : px + 2].min() < 64, genes
        start += len(genes)


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
