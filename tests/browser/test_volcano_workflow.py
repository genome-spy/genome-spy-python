"""Real pointer selection and application-owned shortlist exports."""

import asyncio
import csv
import importlib.util
import json
from pathlib import Path

import pytest

playwright = pytest.importorskip("playwright.async_api")
ROOT = Path(__file__).resolve().parents[2]
module_spec = importlib.util.spec_from_file_location(
    "docs_workflows", ROOT / "tools/docs_workflows.py"
)
assert module_spec and module_spec.loader
workflows = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(workflows)


def test_volcano_shortlist(tmp_path):
    async def run():
        spec = workflows.load_spec("volcano")
        rows = spec["datasets"][spec["data"]["name"]]
        markup = workflows.embed_html(
            "volcano", "/spec.json", "/core.js", "/workflows.js"
        )
        markup = markup.replace(
            "  mountVolcano", "  window.testApi = api;\n  mountVolcano"
        )
        assets = {
            "/": (
                "text/html",
                '<meta charset="utf-8"><link rel="stylesheet" href="/workflows.css"><div style="width:1100px;font:14px system-ui">'
                + markup
                + "</div>",
            ),
            "/spec.json": ("application/json", json.dumps(spec)),
            "/core.js": (
                "text/javascript",
                (ROOT / "src/genome_spy/static/genome-spy.js").read_text(),
            ),
            "/workflows.js": (
                "text/javascript",
                (ROOT / "docs/_static/workflows.js").read_text(),
            ),
            "/workflows.css": (
                "text/css",
                (ROOT / "docs/_static/workflows.css").read_text(),
            ),
        }
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page(viewport={"width": 1150, "height": 800})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            async def route(request):
                mime, body = assets[
                    request.request.url.removeprefix("http://volcano.test")
                ]
                await request.fulfill(content_type=mime, body=body)

            await page.route("http://volcano.test/**", route)
            await page.goto("http://volcano.test/")
            await page.wait_for_function(
                "!document.querySelector('[data-save]').closest('fieldset').disabled || document.querySelector('[data-status]').textContent.startsWith('Unable')",
                timeout=60000,
            )
            assert await page.locator("[data-save]").locator("..").is_enabled(), (
                await page.locator("[data-status]").inner_text()
            )
            await page.wait_for_timeout(600)
            assert not errors
            sliders = page.locator('input[type="range"]')
            assert await sliders.count() == 2
            await page.evaluate("""() => {
                window.chartRows = name => [...testApi.debug.getViewRoot().getDescendants()
                    .find(view => view.name === name).getCollector().getData()];
            }""")
            before = await page.evaluate(
                "chartRows('volcano').filter(row => row.direction !== 'n.s.').length"
            )
            await sliders.nth(0).focus()
            await sliders.nth(0).press("End")
            await sliders.nth(1).focus()
            await sliders.nth(1).press("End")
            await page.wait_for_function(
                "chartRows('volcano-fc-rules').every(row => Math.abs(row.x) === 3) && chartRows('volcano-p-rule')[0].y === 5"
            )
            assert (
                await page.evaluate(
                    "chartRows('volcano').filter(row => row.direction !== 'n.s.').length"
                )
                < before
            )
            await sliders.nth(0).evaluate(
                "el => {el.value = '1'; el.dispatchEvent(new Event('input', {bubbles:true}));}"
            )
            await sliders.nth(1).evaluate(
                "el => {el.value = '2'; el.dispatchEvent(new Event('input', {bubbles:true}));}"
            )
            await page.wait_for_function(
                "chartRows('volcano-fc-rules').every(row => Math.abs(row.x) === 1) && chartRows('volcano-p-rule')[0].y === 2"
            )
            canvas = await page.locator("canvas").first.bounding_box()
            bounds = await page.evaluate(
                "testApi.views.getLayoutBounds({scope: [], view: 'volcano'})"
            )
            assert canvas and bounds
            assert bounds["y"] + bounds["height"] <= canvas["height"]

            def point(x, y):
                return (
                    canvas["x"] + bounds["x"] + (x + 6) / 12 * bounds["width"],
                    canvas["y"] + bounds["y"] + (1 - y / 5) * bounds["height"],
                )

            await page.keyboard.down("Shift")
            await page.mouse.move(*point(1, 2))
            await page.mouse.down()
            await page.mouse.move(*point(5, 4), steps=12)
            await page.wait_for_function(
                "document.querySelector('[data-selected] tbody').rows.length > 0"
            )
            live_table = await page.locator("[data-selected]").bounding_box()
            assert live_table and live_table["y"] < 400
            assert live_table["x"] >= canvas["x"] + canvas["width"]
            assert await page.evaluate("window.scrollY") == 0
            await page.mouse.up()
            await page.keyboard.up("Shift")
            await page.wait_for_timeout(300)
            assert await page.locator("[data-save]").is_enabled(), (
                errors,
                await page.locator("[data-status]").inner_text(),
                await page.evaluate("testApi.params.getSelection('brush').getValue()"),
            )
            snapshot = await page.evaluate(
                "testApi.params.getSelection('brush').getValue()"
            )
            x, y = snapshot["intervals"]["x"], snapshot["intervals"]["y"]
            expected = [
                r
                for r in rows
                if min(x) <= r["log2fc"] <= max(x)
                and min(y) <= r["neglog10_pvalue_plot"] <= max(y)
            ]
            assert len(expected) > 20
            await page.locator("[data-save]").click()
            assert await page.locator("[data-results] tbody tr").count() == len(
                expected
            )
            await page.locator("[data-results] input").first.fill(
                'Check "paired" response, next'
            )
            await page.locator("[data-clear]").click()
            assert await page.locator("[data-selected] tbody tr").count() == 0
            assert await page.locator("[data-results] tbody tr").count() == len(
                expected
            )
            await page.locator("canvas").first.scroll_into_view_if_needed()
            canvas = await page.locator("canvas").first.bounding_box()
            gene = next(r for r in rows if r["symbol"] == "FKBP5")
            px, py = point(gene["log2fc"], gene["neglog10_pvalue_plot"])
            hit = await page.evaluate(
                "point => testApi.views.get({scope: [], view: 'volcano'}).marks.pick(point)",
                {"x": px - canvas["x"], "y": py - canvas["y"]},
            )
            assert hit["status"] == "hit", (hit, bounds, gene, errors)
            await page.mouse.move(px, py)
            await page.wait_for_timeout(250)
            await page.mouse.click(*point(gene["log2fc"], gene["neglog10_pvalue_plot"]))
            await page.wait_for_function(
                "document.querySelector('[data-selected] tbody').rows.length === 1"
            )
            assert "FKBP5" in await page.locator("[data-selected]").inner_text()
            assert await page.locator("[data-expression]").count() == 0
            await page.locator("[data-save]").click()
            assert await page.locator("[data-results] tbody tr").count() == len(
                expected
            )
            async with page.expect_download() as download_event:
                await page.locator("[data-export-shortlist]").click()
            download = await download_event.value
            path = tmp_path / download.suggested_filename
            await download.save_as(path)
            with path.open() as stream:
                exported = list(csv.DictReader(stream))
            assert {r["gene_id"] for r in exported} == {r["gene_id"] for r in expected}
            assert exported[0]["note"] == 'Check "paired" response, next'
            assert float(exported[0]["padj"]) == expected[0]["padj"]
            assert float(exported[0]["SRR1039508"]) == expected[0]["SRR1039508"]
            async with page.expect_download() as download_event:
                await page.locator("[data-download]").click()
            download = await download_event.value
            path = tmp_path / download.suggested_filename
            await download.save_as(path)
            with path.open() as stream:
                assert [r["gene_id"] for r in csv.DictReader(stream)] == [
                    gene["gene_id"]
                ]
            await page.locator("[data-results] button", has_text="Remove").first.click()
            assert (
                await page.locator("[data-results] tbody tr").count()
                == len(expected) - 1
            )
            await page.screenshot(path=str(tmp_path / "volcano.png"), full_page=True)
            assert not errors
            await browser.close()

    asyncio.run(run())
