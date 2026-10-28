"""Observed native dotplot guides, brackets, complete layout and offline output."""

import json
from io import BytesIO
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.expression_fixtures import dotplot_cases
from tests.integrations.scanpy.helpers import index_position

REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((REFERENCE_DIR / "dotplot.json").read_text())


@pytest.mark.smoke
@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("family", ["dotplot", "matrixplot", "DotPlot", "MatrixPlot"])
def test_native_grouped_legends_are_centered_below_labels(page, adata, swapped, family):
    options = dict(
        use_raw=False,
        width=300,
        height=350,
    )
    args = (
        adata,
        {"First": ["g1", "g2"], "Last": ["g3"]},
        "group",
    )
    if family[0].isupper():
        plot = getattr(gsc.pl, family)(*args, **options)
        if swapped:
            plot.swap_axes()
        chart = plot.to_chart()
    else:
        chart = getattr(gsc.pl, family)(*args, **options, swap_axes=swapped, show=False)
    render(page, chart)
    geometry = page.evaluate(
        """async () => {
            const host = document.createElement('div');
            host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
            host.innerHTML = await (await api.imageExport.svg()).blob.text();
            document.body.append(host);
            await document.fonts.ready;
            const chart = host.querySelector('svg').getBoundingClientRect();
            const legend = host.querySelector('[data-name="legend_region_bottom"]');
            const bounds = legend.getBoundingClientRect();
            const labels = [...host.querySelectorAll('text')].filter(e =>
                ['g1', 'g2', 'g3', 'A', 'B'].includes(e.textContent));
            const result = {
                top: bounds.top - chart.top,
                bottom: chart.bottom - bounds.bottom,
                left: bounds.left - chart.left,
                right: chart.right - bounds.right,
                labelBottom: Math.max(...labels.map(e =>
                    e.getBoundingClientRect().bottom - chart.top)),
                hasRightLegend: !!host.querySelector('[data-name="legend_region_right"]'),
                titles: [...legend.querySelectorAll('[data-name="title"] text')]
                    .map(e => e.textContent),
            };
            host.remove();
            return result;
        }"""
    )
    assert geometry["titles"] == (
        ["Cells expressing (%)", "Mean expression"]
        if family.lower() == "dotplot"
        else ["Mean expression in group"]
    )
    assert not geometry["hasRightLegend"]
    assert geometry["top"] > 0 and geometry["bottom"] > 0
    assert geometry["top"] > geometry["labelBottom"]
    assert geometry["left"] >= 0 and geometry["right"] >= 0
    assert geometry["left"] == pytest.approx(geometry["right"], abs=10)


@pytest.mark.parametrize("swapped,rotation", [(False, None), (False, 0), (True, None)])
@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_complete_grouped_labels_guides_and_brackets(
    page, adata, tmp_path, swapped, rotation, family
):
    chart = getattr(gsc.pl, family)(
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
        *(["Cells expressing (%)"] if family == "dotplot" else []),
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
    guides = [
        (
            "Mean expression" if family == "dotplot" else "Mean expression in group",
            "1.0",
        )
    ]
    if family == "dotplot":
        guides.append(("Cells expressing (%)", "30"))
    for title, tick in guides:
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
                padding = 0.5 if family == "dotplot" else 0
                expected = bounds["y"] + index_position(
                    slot, 3, padding, bounds["height"]
                )
                assert label["y"] + label["height"] / 2 == pytest.approx(
                    expected, abs=2
                )
                assert label["x"] >= right + 6
                px, py = round(right + 10), round(expected)
            else:
                padding = 0.3 if family == "dotplot" else 0
                expected = bounds["x"] + index_position(
                    slot, 3, padding, bounds["width"]
                )
                assert label["x"] + label["width"] / 2 == pytest.approx(expected, abs=2)
                assert label["y"] + label["height"] <= bounds["y"] - 6
                px, py = round(expected), round(bounds["y"] - 10)
            assert pixels[py - 1 : py + 2, px - 1 : px + 2].min() < 64
    page.screenshot(
        path=str(tmp_path / f"{family}-{swapped}-complete.png"), full_page=True
    )
    (tmp_path / f"{family}-{swapped}-complete.svg").write_text(svg)


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
        # Match the one-pixel picking neighborhood used by the UMAP checks.
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            page.mouse.move(px + dx, py + dy)
            page.wait_for_timeout(80)
            if page.locator("table.attributes").is_visible():
                break
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
        group_gap=4,
        show=False,
    )
    bounds = render(page, chart)
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    start = 0
    for i, genes in enumerate(markers.values()):
        midpoint = start + (len(genes) - 1) / 2 + 0.45
        px = round(
            bounds["x"] + (midpoint + 0.3) / 10.6 * (bounds["width"] - 24) + 4 * i
        )
        py = round(bounds["y"] - 10)
        assert pixels[py - 1 : py + 2, px - 1 : px + 2].min() < 64, genes
        start += len(genes)


@pytest.mark.reference
@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", dotplot_cases())
def test_registered_dotplot_positions_paints_and_footprints(
    page, adata, tmp_path, reference_images, case
):
    reference = REFERENCE["cases"][case]
    options = dotplot_cases()[case].copy()
    names = options.pop("var_names", ["g1", "g2", "g3"])
    chart = gsc.pl.dotplot(
        adata,
        names,
        "group",
        use_raw=False,
        group_gap=4,
        show=False,
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        **options,
    )
    bounds = render(page, chart)
    actual = panel_image(page, bounds)
    expected = Image.open(
        reference_images("dotplot") / f"dotplot-{case}-panel.png"
    ).convert("RGB")
    assert abs(actual.width - expected.width) <= 2
    assert abs(actual.height - expected.height) <= 2
    registered = expected.copy()
    registered.paste("white", (2, 2, expected.width - 2, expected.height - 2))
    for (x, y), color, area in zip(
        reference["positions"], reference["colors"], reference["sizes"], strict=True
    ):
        xd, yd = reference["x_domain"], reference["y_domain"]
        px = round((x - xd[0]) / (xd[1] - xd[0]) * bounds["width"] * 1.5)
        py = round((1 - (y - yd[0]) / (yd[1] - yd[0])) * bounds["height"] * 1.5)
        original = (px, py)
        scales = chart.to_dict()["scales"]
        px = round(
            index_position(
                x,
                scales["x"]["domain"][1] + 1,
                0.3,
                bounds["width"],
                scales["x"]["gapPositions"],
            )
            * 1.5
        )
        py = round(
            index_position(
                y,
                scales["y"]["domain"][1] + 1,
                0.5,
                bounds["height"],
                scales["y"]["gapPositions"],
            )
            * 1.5
        )
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
        def diameter(image, center):
            pixels = np.asarray(
                image.crop(
                    (center[0] - 20, center[1] - 20, center[0] + 21, center[1] + 21)
                )
            ).astype(int)
            ink = (pixels.max(axis=2) - pixels.min(axis=2) > 5) | (
                pixels.min(axis=2) < 220
            )
            yy, xx = np.where(ink)
            assert len(xx) > 0
            return np.array([xx.max() - xx.min() + 1, yy.max() - yy.min() + 1])

        np.testing.assert_allclose(
            diameter(actual, (px, py)), diameter(expected, original), atol=2
        )
        # Move the reference footprint without resizing it when groups gain gaps.
        ox, oy = original
        registered.paste(
            expected.crop((ox - 20, oy - 20, ox + 21, oy + 21)), (px - 20, py - 20)
        )
        np.testing.assert_allclose(
            diameter(actual, (px, py)),
            np.sqrt(area) * 150 / 72 + 0.2 * 150 / 72,
            atol=2,
        )
    actual.save(tmp_path / f"{case}-native.png")
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), registered.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


def test_dotplot_offline_html_and_plain_navigation(page, adata, tmp_path):
    chart = gsc.pl.dotplot(adata, ["g1", "g2"], "group", use_raw=False, show=False)
    spec = chart.to_dict()
    for channel in ("x", "y"):
        spec["scales"][channel]["name"] = f"dotplot-{channel}"
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
