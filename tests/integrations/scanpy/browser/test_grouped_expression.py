"""Grouped expression behavior and regressions."""

import json
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.browser.interactions import hover_at, svg_root
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.expression_fixtures import (
    dotplot_cases,
    make_heatmap_adata,
    matrixplot_cases,
)
from tests.integrations.scanpy.helpers import index_position
from tests.integrations.scanpy.paga_fixtures import POSITIONS, make_paga, make_path

DOTPLOT_REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
DOTPLOT_REFERENCE = json.loads((DOTPLOT_REFERENCE_DIR / "dotplot.json").read_text())


class TestDotplot:
    """Observed native dotplot guides, brackets, complete layout and offline output."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("swapped", [False, True])
    @pytest.mark.parametrize(
        "family", ["dotplot", "matrixplot", "DotPlot", "MatrixPlot"]
    )
    def test_native_grouped_legends_are_centered_below_labels(
        self, page, adata, swapped, family
    ):
        options = dict(use_raw=False, width=300, height=350)
        args = (adata, {"First": ["g1", "g2"], "Last": ["g3"]}, "group")
        if family[0].isupper():
            plot = getattr(gsc.pl, family)(*args, **options)
            if swapped:
                plot.swap_axes()
            chart = plot.to_chart()
        else:
            chart = getattr(gsc.pl, family)(
                *args, **options, swap_axes=swapped, show=False
            )
        render(page, chart)
        geometry = page.evaluate(
            "async () => {\n            const host = document.createElement('div');\n            host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n            host.innerHTML = await (await api.imageExport.svg()).blob.text();\n            document.body.append(host);\n            await document.fonts.ready;\n            const chart = host.querySelector('svg').getBoundingClientRect();\n            const legend = host.querySelector('[data-name=\"legend_region_bottom\"]');\n            const bounds = legend.getBoundingClientRect();\n            const labels = [...host.querySelectorAll('text')].filter(e =>\n                ['g1', 'g2', 'g3', 'A', 'B'].includes(e.textContent));\n            const result = {\n                top: bounds.top - chart.top,\n                bottom: chart.bottom - bounds.bottom,\n                left: bounds.left - chart.left,\n                right: chart.right - bounds.right,\n                labelBottom: Math.max(...labels.map(e =>\n                    e.getBoundingClientRect().bottom - chart.top)),\n                hasRightLegend: !!host.querySelector('[data-name=\"legend_region_right\"]'),\n                titles: [...legend.querySelectorAll('[data-name=\"title\"] text')]\n                    .map(e => e.textContent),\n            };\n            host.remove();\n            return result;\n        }"
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

    @pytest.mark.parametrize(
        "swapped,rotation", [(False, None), (False, 0), (True, None)]
    )
    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    def test_complete_grouped_labels_guides_and_brackets(
        self, page, adata, tmp_path, swapped, rotation, family
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
            "async svg => {\n        const host = document.createElement('div');\n        host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        host.innerHTML = svg;\n        document.body.append(host);\n        await document.fonts.ready;\n        const labels = [...host.querySelectorAll('text')].map(element => {\n            const rect = element.getBoundingClientRect();\n            return {text:element.textContent, x:rect.x, y:rect.y,\n                    width:rect.width, height:rect.height};\n        });\n        host.remove();\n        return labels;\n    }",
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
                "Mean expression"
                if family == "dotplot"
                else "Mean expression in group",
                "1.0",
            )
        ]
        if family == "dotplot":
            guides.append(("Cells expressing (%)", "30"))
        for title, tick in guides:
            heading = next((label for label in labels if label["text"] == title))
            entry = next((label for label in labels if label["text"] == tick))
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
                    px, py = (round(right + 10), round(expected))
                else:
                    padding = 0.3 if family == "dotplot" else 0
                    expected = bounds["x"] + index_position(
                        slot, 3, padding, bounds["width"]
                    )
                    assert label["x"] + label["width"] / 2 == pytest.approx(
                        expected, abs=2
                    )
                    assert label["y"] + label["height"] <= bounds["y"] - 6
                    px, py = (round(expected), round(bounds["y"] - 10))
                assert pixels[py - 1 : py + 2, px - 1 : px + 2].min() < 64
        page.screenshot(
            path=str(tmp_path / f"{family}-{swapped}-complete.png"), full_page=True
        )
        (tmp_path / f"{family}-{swapped}-complete.svg").write_text(svg)

    @pytest.mark.parametrize("swapped", [False, True])
    @pytest.mark.parametrize("hover", [False, True])
    def test_dotplot_hover_reports_summary_values(self, page, adata, swapped, hover):
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
            page.get_by_text("Expressing cells (%)", exact=True).wait_for(
                state="visible"
            )
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

    def test_pbmc_marker_brackets_paint_single_and_multiple_gene_spans(self, page):
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
        self, page, adata, tmp_path, reference_images, case
    ):
        reference = DOTPLOT_REFERENCE["cases"][case]
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
            xd, yd = (reference["x_domain"], reference["y_domain"])
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

    def test_dotplot_offline_html_and_plain_navigation(self, page, adata, tmp_path):
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
                requests.append(r.url)
                if r.url.startswith(("http:", "https:"))
                else None
            ),
        )
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not requests
        assert page.locator(".message-box").count() == 0


MATRIXPLOT_REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
MATRIXPLOT_REFERENCE = json.loads(
    (MATRIXPLOT_REFERENCE_DIR / "matrixplot.json").read_text()
)


class TestMatrixplot:
    """Observed matrixplot tiles, color bounds, missing cells, hover and HTML delivery."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", matrixplot_cases())
    def test_registered_matrixplot_tiles_paint_and_grid(
        self, page, adata, tmp_path, reference_images, case
    ):
        reference = MATRIXPLOT_REFERENCE["cases"][case]
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
        actual = panel_image(page, bounds)
        expected = Image.open(
            reference_images("matrixplot") / f"matrixplot-{case}-panel.png"
        ).convert("RGB")
        assert abs(actual.width - expected.width) <= 2
        assert abs(actual.height - expected.height) <= 2
        values = np.array(reference["values"], dtype=float)
        pixels = np.array(actual).astype(int)
        rows, columns = values.shape
        cuts = chart.to_dict()["scales"]
        registered = Image.new("RGB", actual.size, "white")
        for row, column in np.ndindex(values.shape):
            px, py = (
                round((column + 0.5) / columns * actual.width),
                round((row + 0.5) / rows * actual.height),
            )
            target = np.asarray(expected)[py, px].astype(int)
            px = round(
                index_position(
                    column + 0.5, columns, 0, bounds["width"], cuts["x"]["gapPositions"]
                )
                * 1.5
            )
            py = round(
                index_position(
                    row + 0.5, rows, 0, bounds["height"], cuts["y"]["gapPositions"]
                )
                * 1.5
            )
            # Palette bins/interpolation differ slightly; missing cells remain white.
            assert np.abs(pixels[py, px] - target).max() <= 12
            if np.isnan(values[row, column]):
                assert pixels[py, px].tolist() == [255, 255, 255]
            # Sample both tile interiors to catch gaps and incorrect band endpoints.
            for fraction in (0.1, 0.9):
                x = round(
                    index_position(
                        column + fraction,
                        columns,
                        0,
                        bounds["width"],
                        cuts["x"]["gapPositions"],
                    )
                    * 1.5
                )
                y = round(
                    index_position(
                        row + fraction,
                        rows,
                        0,
                        bounds["height"],
                        cuts["y"]["gapPositions"],
                    )
                    * 1.5
                )
                assert np.abs(pixels[y, x] - target).max() <= 12
            # Register each frozen tile with its gapped slot for the temporary overlay.
            left = (
                index_position(
                    column, columns, 0, bounds["width"], cuts["x"]["gapPositions"]
                )
                * 1.5
            )
            top = (
                index_position(
                    row, rows, 0, bounds["height"], cuts["y"]["gapPositions"]
                )
                * 1.5
            )
            tile_width = (
                (bounds["width"] - 4 * len(cuts["x"]["gapPositions"])) / columns * 1.5
            )
            tile_height = (
                (bounds["height"] - 4 * len(cuts["y"]["gapPositions"])) / rows * 1.5
            )
            box = (
                round(left),
                round(top),
                round(left + tile_width),
                round(top + tile_height),
            )
            source = expected.crop(
                (
                    round(column / columns * expected.width),
                    round(row / rows * expected.height),
                    round((column + 1) / columns * expected.width),
                    round((row + 1) / rows * expected.height),
                )
            )
            registered.paste(source.resize((box[2] - box[0], box[3] - box[1])), box)
        if case == "bounds_edges":
            # Compare one isolated vertical grid stroke at the reference export DPI.
            px, py = (round(actual.width / columns), round(actual.height / (2 * rows)))
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
        Image.blend(actual.crop(extent), registered.crop(extent), 0.5).save(
            tmp_path / f"{case}-registered-overlay.png"
        )

    @pytest.mark.parametrize("swapped", [False, True])
    @pytest.mark.parametrize("hover", [False, True])
    def test_matrixplot_hover_identifies_summary_in_both_orientations(
        self, page, adata, swapped, hover
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
            ] == [("Gene", "g2"), ("Group", "B"), ("Mean expression (scaled)", "0.000")]
        else:
            page.wait_for_timeout(150)
            assert page.locator("table.attributes").count() == 0

    def test_matrixplot_plain_navigation_and_offline_html(self, page, adata, tmp_path):
        chart = gsc.pl.matrixplot(
            adata, ["g1", "g2"], "group", use_raw=False, show=False
        )
        spec = chart.to_dict()
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"matrix-{axis}"
        bounds = render(page, TopLevelSpec.from_dict(spec))
        expression = "['matrix-x','matrix-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
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
                requests.append(r.url)
                if r.url.startswith(("http:", "https:"))
                else None
            ),
        )
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not requests
        assert page.locator(".message-box").count() == 0


class TestExpressionPresentation:
    """Observe native brackets, annotation spans, graph labels and path guides."""

    @pytest.mark.parametrize(
        "family,swapped",
        [
            ("dotplot", False),
            ("dotplot", True),
            ("matrixplot", False),
            ("matrixplot", True),
            ("heatmap", False),
        ],
    )
    def test_marker_brackets_clear_the_matrix_in_both_orientations(
        self, page, family, swapped
    ):
        chart = getattr(gsc.pl, family)(
            make_heatmap_adata(),
            {"First": ["g1", "g2"], "Last": ["g3"]},
            "group",
            swap_axes=swapped,
            width=380,
            height=260,
            show=False,
        )
        bounds = render(page, chart)
        view = next(
            (
                e
                for e in svg_root(page).iter()
                if e.get("data-name") == f"{family}-brackets"
            )
        )
        lines = [e for e in view.iter() if e.tag.endswith("line")]
        assert len(lines) == 6
        for line in lines[:2]:
            if swapped:
                assert float(line.get("x1")) == pytest.approx(
                    bounds["x"] + bounds["width"] + 10, abs=1
                )
            else:
                assert float(line.get("y1")) == pytest.approx(bounds["y"] - 10, abs=1)
        axis = "x" if swapped else "y"
        assert all(
            (
                abs(float(e.get(f"{axis}2")) - float(e.get(f"{axis}1")))
                == pytest.approx(10, abs=0.1)
                for e in lines[2:]
            )
        )
        assert {e.text for e in view.iter() if e.tag.endswith("text")} == {
            "First",
            "Last",
        }

    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_dense_category_strips_have_no_outline_and_keep_hover(self, page):
        a = AnnData(
            np.zeros((700, 2)),
            obs=pd.DataFrame(
                {"group": pd.Categorical(["A"] * 350 + ["B"] * 350)},
                index=[f"cell-{i}" for i in range(700)],
            ),
        )
        a.uns["group_colors"] = ["red", "blue"]
        chart = gsc.pl.clustermap(
            a,
            obs_keys="group",
            row_cluster=False,
            col_cluster=False,
            xticklabels=False,
            yticklabels=False,
            width=240,
            height=350,
            zoom=True,
            show=False,
        )
        render(page, chart)
        bounds = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'clustermap-left-colors-0'})"
        )
        view = next(
            (
                e
                for e in svg_root(page).iter()
                if e.get("data-name") == "clustermap-left-colors-0"
            )
        )
        group = next((e for e in view.iter() if e.get("data-mark-type") == "rect"))
        assert len(group) == 700 and group.get("stroke") == "none"
        assert float(group.get("stroke-width")) == 0
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        x = round((bounds["x"] + bounds["width"] / 2) * 1.5)
        for low, high, color, label in (
            (0.05, 0.45, [255, 0, 0], "A"),
            (0.55, 0.95, [0, 0, 255], "B"),
        ):
            strip = pixels[
                round((bounds["y"] + bounds["height"] * low) * 1.5) : round(
                    (bounds["y"] + bounds["height"] * high) * 1.5
                ),
                x,
            ]
            assert np.abs(strip.astype(int) - color).max() <= 3
            hover_at(
                page,
                bounds["x"] + bounds["width"] / 2,
                bounds["y"] + bounds["height"] * (low + high) / 2,
            )
            assert (
                page.locator("table.attributes")
                .get_by_text(label, exact=True)
                .is_visible()
            )

    def test_paga_labels_clear_nodes_and_colorbar_has_normal_width(self, page):
        chart = gsc.pl.paga(
            make_paga("gene_raw"),
            color="g1",
            pos=POSITIONS,
            width=500,
            height=350,
            show=False,
        )
        render(page, chart)
        root = svg_root(page)
        panel = next((e for e in root.iter() if e.get("data-name") == "panel-0"))
        rules = [e for e in panel.iter() if e.get("data-mark-type") == "rule"]
        assert rules and all((e.get("stroke") == "#999999" for e in rules))
        circles = list(
            next((e for e in panel.iter() if e.get("data-mark-type") == "point"))
        )
        labels = list(
            next((e for e in panel.iter() if e.get("data-mark-type") == "text"))
        )
        assert len(circles) == len(labels) == 4
        assert {label.text for label in labels} == {"A", "B", "C", "D"}
        boxes = page.evaluate(
            "async () => {\n        const host = document.createElement('div');\n        host.style.cssText = 'position:absolute;visibility:hidden';\n        host.innerHTML = await (await api.imageExport.svg()).blob.text();\n        document.body.append(host);\n        const panel = host.querySelector('[data-name=\"panel-0\"]');\n        const bounds = selector => [...panel.querySelectorAll(selector)].map(e => {\n            const {left, right, top, bottom} = e.getBoundingClientRect();\n            return {left, right, top, bottom};\n        });\n        const result = {nodes: bounds('circle'), labels: bounds('text')};\n        host.remove();\n        return result;\n    }"
        )
        assert len(boxes["nodes"]) == len(boxes["labels"]) == 4
        for label in boxes["labels"]:
            for node in boxes["nodes"]:
                assert (
                    label["right"] <= node["left"]
                    or label["left"] >= node["right"]
                    or label["bottom"] <= node["top"]
                    or (label["top"] >= node["bottom"])
                )
        gradients = [
            e
            for e in root.iter()
            if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
        ]
        assert len(gradients) == 1
        assert float(gradients[0].get("width")) == pytest.approx(15, abs=0.1)

    def test_path_labels_only_appear_when_their_visible_group_span_fits(self, page):
        a = make_path()
        names = {"beta": "Long category B", "alpha": "Long category A"}
        a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
        chart = gsc.pl.paga_path(
            a,
            list(names.values()),
            ["g1", "g2"],
            width=140,
            height=180,
            zoom="xy",
            show=False,
        )
        spec = chart.to_dict()
        spec["scales"]["x"]["name"] = "path-x"
        render(page, spec)

        def group_labels():
            """Read only visible band labels, excluding the native legend entries."""
            group = next(
                (
                    e
                    for e in svg_root(page).iter()
                    if e.get("data-name") == "paga-path-groups"
                )
            )
            return [e.text for e in group.iter() if e.tag.endswith("text")]

        texts = {e.text for e in svg_root(page).iter() if e.tag.endswith("text")}
        assert {"cluster", "dpt_pseudotime", *names.values()} <= texts
        assert group_labels() == []
        page.evaluate(
            "async () => api.getScaleResolutionByName('path-x').zoomTo([-0.5, 0.5])"
        )
        page.wait_for_timeout(300)
        assert group_labels() == ["Long category B"]
        bounds = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'paga-path-groups'})"
        )
        hover_at(
            page, bounds["x"] + bounds["width"] / 2, bounds["y"] + bounds["height"] / 2
        )
        assert (
            page.locator("table.attributes")
            .get_by_text("Long category B", exact=True)
            .is_visible()
        )
