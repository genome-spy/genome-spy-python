"""Exercise the documentation hosts with real pointer events and downloads."""

import asyncio
import csv
import importlib.util
import io
import json
from pathlib import Path

import pytest

playwright = pytest.importorskip("playwright.async_api")
ROOT = Path(__file__).resolve().parents[2]
module_spec = importlib.util.spec_from_file_location(
    "docs_workflows", ROOT / "tools" / "docs_workflows.py"
)
assert module_spec and module_spec.loader
workflows = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(workflows)


async def check_gene_zoom(page, canvas, spec):
    assert all(spec["encoding"][axis]["scale"]["zoom"] for axis in ("x", "y"))
    before = await page.evaluate(
        """expr => {
        const view = testApi.debug.getViewRoot().getDescendants().find(view => view.mark);
        window.testPointSize = () => view.paramRuntime.evaluateAndGet(expr);
        return testPointSize();
    }""",
        spec["mark"]["size"]["expr"],
    )
    bounds = await canvas.bounding_box()
    await page.mouse.move(
        bounds["x"] + bounds["width"] / 2, bounds["y"] + bounds["height"] / 2
    )
    await page.mouse.wheel(0, -400)
    await page.wait_for_function("before => testPointSize() > before", arg=before)
    assert before < await page.evaluate("testPointSize()") <= 180


@pytest.mark.parametrize("name", ["intervals", "genes", "points", "sequence"])
def test_browser_workflow(name, tmp_path):
    async def run():
        spec = workflows.load_spec(name)
        markup = workflows.embed_html(name, "/spec.json", "/core.js", "/workflows.js")
        # Test-only access to rendered bounds; production hosts expose no global API.
        markup = markup.replace("  mount", "  window.testApi = api;\n  mount")
        assets = {
            "/": ("text/html", '<div style="width:900px">' + markup + "</div>"),
            "/spec.json": ("application/json", json.dumps(spec, allow_nan=False)),
            "/core.js": (
                "text/javascript",
                (ROOT / "src/genome_spy/static/genome-spy.js").read_text(),
            ),
            "/workflows.js": (
                "text/javascript",
                (ROOT / "docs/_static/workflows.js").read_text(),
            ),
        }
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page(viewport={"width": 1100, "height": 1000})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            async def route(request):
                path = request.request.url.removeprefix("http://workflow.test")
                mime, body = assets[path]
                await request.fulfill(content_type=mime, body=body)

            await page.route("http://workflow.test/**", route)
            await page.goto("http://workflow.test/")
            await page.wait_for_function(
                "!document.querySelector('fieldset').disabled || document.querySelector('[data-status]').textContent.startsWith('Unable')",
                timeout=60000,
            )
            assert await page.locator("fieldset").is_enabled(), await page.locator(
                "[data-status]"
            ).inner_text()
            # Keep browser coordinate semantics consistent with the notebook.
            assert await page.evaluate("""async () => {
                const {bedInterval, selectGenes} = await import('/workflows.js');
                const region = bedInterval({active: true, complexIntervals: {x: [
                    {chrom: 'chr5', pos: 0}, {chrom: 'chr5', pos: 20}
                ]}});
                const selected = selectGenes([
                    {log2fc: 2, neglog10_pvalue: 9, neglog10_pvalue_plot: 5},
                    {log2fc: 4, neglog10_pvalue_plot: 5}
                ], {active: true, intervals: {x: [3, 1], y: [6, 4]}});
                return region.start === 0 && region.end === 20 && selected.length === 1;
            }""")
            canvas = page.locator("canvas").first
            # A tooltip table may precede the results in the embed subtree.
            # Keep one present deterministically, even before the first hover.
            await page.locator(".gs-doc-embed").evaluate("""chart => {
                const tooltip = document.createElement('table');
                tooltip.dataset.tooltipFixture = '';
                tooltip.hidden = true;
                tooltip.innerHTML = '<tbody><tr><td>Hover details</td></tr></tbody>';
                chart.append(tooltip);
            }""")
            bounds = await canvas.bounding_box()
            assert bounds
            if name in ("points", "sequence"):
                await page.wait_for_timeout(500)
                assert not errors
                await page.screenshot(path=str(tmp_path / f"{name}-initial.png"))
                bounds = await canvas.bounding_box()
                assert bounds
                if name == "sequence":
                    # First column, C row: replace the initial A with C.
                    grid = await page.evaluate(
                        "testApi.views.getLayoutBounds({scope: [], view: 'base-cells'})"
                    )
                    assert grid
                    cell_x = bounds["x"] + grid["x"] + grid["width"] / 48
                    cell_y = bounds["y"] + grid["y"] + grid["height"] * 3 / 8
                    hit = await page.evaluate(
                        """point => testApi.views.get({scope: [], view: 'base-cells'}).marks.pick(point)""",
                        {"x": cell_x - bounds["x"], "y": cell_y - bounds["y"]},
                    )
                    assert hit["status"] == "hit", (bounds, grid, hit)
                    assert hit["hit"]["datum"]["base"] == "C", hit
                    await page.mouse.move(cell_x - 2, cell_y - 2, steps=5)
                    await page.wait_for_timeout(100)
                    await page.mouse.move(cell_x, cell_y)
                    await page.wait_for_timeout(200)
                    await page.mouse.click(cell_x, cell_y)
                    await page.wait_for_function(
                        "document.querySelector('[data-results] tbody')?.rows.length === 1"
                    )
                    assert await page.locator(
                        "[data-results] tbody td"
                    ).all_text_contents() == [
                        "1",
                        "A",
                        "C",
                    ]
                else:
                    for dx in range(390, 450, 5):
                        await page.mouse.click(bounds["x"] + dx, bounds["y"] + 270)
                        if await page.locator("[data-results] tbody tr").count():
                            break
                    assert await page.locator("[data-results] tbody tr").count() == 1
                async with page.expect_download() as event:
                    await page.locator("[data-download]").click()
                downloaded = await event.value
                path = tmp_path / downloaded.suggested_filename
                await downloaded.save_as(path)
                if name == "sequence":
                    reference = "".join(
                        row["base"] for row in spec["datasets"]["reference"]
                    )
                    assert path.read_text().splitlines() == [
                        ">synthetic_reference",
                        reference,
                        ">edited_sequence",
                        "C" + reference[1:],
                    ]
                else:
                    rows = list(csv.DictReader(io.StringIO(path.read_text())))
                    assert len(rows) == 1
                    assert (
                        rows[0]["ensgene"]
                        == await page.locator(
                            "[data-results] tbody td"
                        ).first.inner_text()
                    )
                await page.locator("[data-clear]").click()
                assert await page.locator("[data-results] tbody tr").count() == 0
                assert not errors
                assert (
                    await page.locator("[data-tooltip-fixture]").text_content()
                    == "Hover details"
                )
                if name == "points":
                    await check_gene_zoom(page, canvas, spec)
                await page.screenshot(path=str(tmp_path / f"{name}.png"))
                await browser.close()
                return
            await page.mouse.move(bounds["x"] + bounds["width"] * 0.3, bounds["y"] + 30)
            await page.mouse.down()
            await page.mouse.move(
                bounds["x"] + bounds["width"] * 0.7,
                bounds["y"] + (100 if name == "intervals" else bounds["height"] * 0.9),
                steps=12,
            )
            await page.mouse.up()
            if name == "intervals":
                await page.locator("[data-save]:not([disabled])").wait_for()
                await page.locator('[name="name"]').fill("test-region")
                await page.locator('[name="note"]').fill("<b>literal note</b>")
                await page.locator("[data-save]").click()
                await page.wait_for_function(
                    "document.querySelector('[data-results] tbody')?.rows.length === 1"
                )
                assert await page.locator("[data-results] tbody b").count() == 0
                cells = await page.locator(
                    "[data-results] tbody td"
                ).all_text_contents()
                assert cells[3:] == ["test-region", "<b>literal note</b>"]
            else:
                await page.wait_for_function(
                    "document.querySelector('[data-results] tbody')?.rows.length === 20"
                )
            async with page.expect_download() as event:
                await page.locator("[data-download]").click()
            downloaded = await event.value
            path = tmp_path / downloaded.suggested_filename
            await downloaded.save_as(path)
            if name == "intervals":
                assert path.read_text() == "\t".join(cells[:4]) + "\n"
                assert int(cells[1]) < int(cells[2])
            else:
                rows = list(csv.DictReader(io.StringIO(path.read_text())))
                count = int(
                    (await page.locator("[data-status]").inner_text()).split()[0]
                )
                assert len(rows) == count > 20
                assert rows[0]["ensgene"].startswith("ENSG")
            await page.locator("[data-clear]").click()
            if name == "intervals":
                assert await page.locator("[data-results] tbody tr").count() == 1
            else:
                assert await page.locator("[data-results] tbody tr").count() == 0
                assert await page.locator("[data-download]").is_disabled()
            assert not errors
            if name == "genes":
                await check_gene_zoom(page, canvas, spec)
            assert (
                await page.locator("[data-tooltip-fixture]").text_content()
                == "Hover details"
            )
            await browser.close()

    asyncio.run(run())
