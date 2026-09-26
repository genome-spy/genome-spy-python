"""Exercise model-review annotations against the pinned real squid extract."""

import asyncio
import csv
import io
import importlib.util
import json
from pathlib import Path
from urllib.request import urlopen

import pytest

playwright = pytest.importorskip("playwright.async_api")
ROOT = Path(__file__).resolve().parents[2]
DATA = "https://data.genomespy.app/datasets/bpreveal-pisa/v3/"
module_spec = importlib.util.spec_from_file_location(
    "docs_workflows", ROOT / "tools/docs_workflows.py"
)
assert module_spec and module_spec.loader
workflows = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(workflows)


def test_squid_review_survives_selection_changes_and_exports(tmp_path):
    async def run():
        spec = workflows.load_spec("squid")
        markup = workflows.embed_html(
            "squid", "/spec.json", "/core.js", "/workflows.js"
        )
        markup = markup.replace("  mountSquid", "  window.testApi = api;\n  mountSquid")
        assets = {
            "/": (
                "text/html",
                '<meta charset="utf-8"><link rel="stylesheet" href="/workflows.css"><div style="width:1000px;font:16px system-ui">'
                + markup
                + "</div>",
            ),
            "/workflows.css": (
                "text/css",
                (ROOT / "docs/_static/workflows.css").read_text(),
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
        }
        # Real source tables: keep downloads small and independent of the docs server.
        tables = {}
        for name in (
            "fig2cd-atac-tracks.parquet",
            "fig2cd-atac-motifs.parquet",
            "fig2c-atac-links.parquet",
        ):
            with urlopen(DATA + name, timeout=30) as response:
                tables[DATA + name] = response.read()
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page(viewport={"width": 1200, "height": 1100})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            async def route(request):
                mime, body = assets[
                    request.request.url.removeprefix("http://squid.test")
                ]
                await request.fulfill(content_type=mime, body=body)

            async def data_route(request):
                await request.fulfill(
                    body=tables[request.request.url],
                    headers={"Access-Control-Allow-Origin": "*"},
                )

            await page.route("http://squid.test/**", route)
            await page.route(DATA + "*", data_route)
            await page.goto("http://squid.test/")
            await page.wait_for_function(
                "!document.querySelector('fieldset').disabled || document.querySelector('[data-status]').textContent.startsWith('Unable')",
                timeout=60000,
            )
            assert await page.locator("fieldset").evaluate("el => !el.disabled"), (
                await page.locator("[data-status]").inner_text()
            )
            canvas = await page.locator("canvas").first.bounding_box()
            assert canvas

            async def brush(view, left, right):
                bounds = await page.evaluate(
                    "name => testApi.views.getLayoutBounds({scope: [], view: name})",
                    view,
                )
                assert bounds
                y = canvas["y"] + bounds["y"] + bounds["height"] * 0.5
                await page.mouse.move(
                    canvas["x"] + bounds["x"] + bounds["width"] * left, y
                )
                await page.mouse.down()
                await page.mouse.move(
                    canvas["x"] + bounds["x"] + bounds["width"] * right, y, steps=10
                )
                await page.mouse.up()
                return (
                    canvas["x"] + bounds["x"] + bounds["width"] * (left + right) / 2,
                    y,
                )

            input_point = await brush("importance", 0.15, 0.3)
            await brush("prediction", 0.4, 0.6)
            frozen = await page.evaluate("""async () => {
                const {squidDraft} = await import('/workflows.js');
                return squidDraft(testApi.views.get({scope: [], view: 'importance'}).params.getSelection('contributionRegion').getValue(),
                    testApi.views.get({scope: [], view: 'prediction'}).params.getSelection('accessibilityRegion').getValue());
            }""")
            assert frozen["start"] < frozen["end"]
            assert frozen["output_start"] < frozen["output_end"]
            await page.mouse.click(*input_point, button="right")
            assert await page.get_by_role("menu").is_visible()
            await page.keyboard.press("Escape")
            assert not await page.get_by_role("menu").is_visible()
            await page.mouse.click(*input_point, button="right")
            await page.get_by_role("menuitem", name="Add annotation").click()
            assert await page.get_by_role("dialog").is_visible()
            assert await page.locator("dialog label").count() == 3
            await page.keyboard.press("Escape")
            assert not await page.get_by_role("dialog").is_visible()
            assert await page.locator("[data-results] tbody tr").count() == 0
            await page.mouse.click(*input_point, button="right")
            await page.get_by_role("menuitem", name="Add annotation").click()
            # The frozen draft survives an external selection update, too.
            await page.evaluate(
                "testApi.views.get({scope: [], view: 'importance'}).params.getSelection('contributionRegion').clear()"
            )
            await page.locator('[name="name"]').fill("motif-review")
            await page.locator('[name="color"]').fill("#224488")
            note = 'Inspect "motif", <b>reference</b>'
            await page.locator('[name="note"]').fill(note)
            await page.screenshot(path=str(tmp_path / "dialog.png"))
            await page.locator("[data-save]").click()
            assert not await page.get_by_role("dialog").is_visible()
            assert await page.locator("[data-results] tbody tr").count() == 1
            assert await page.locator("[data-results] tbody b").count() == 0
            cells = await page.locator("[data-results] tbody td").all_text_contents()
            assert cells[2:6] == [
                str(frozen[key])
                for key in ("start", "end", "output_start", "output_end")
            ]

            async def exported(selector):
                async with page.expect_download() as event:
                    await page.locator(selector).click()
                download = await event.value
                path = tmp_path / download.suggested_filename
                await download.save_as(path)
                return path.read_text()

            rows = list(csv.DictReader(io.StringIO(await exported("[data-download]"))))
            assert len(rows) == 1
            assert rows[0]["note"] == note
            assert rows[0]["assembly"] == "dm6"
            assert rows[0]["color"] == "#224488"
            assert rows[0]["source"] == "bpreveal-pisa/v3"
            assert (
                await exported("[data-bed]")
                == f"chrX\t{frozen['start']}\t{frozen['end']}\tmotif-review\n"
            )
            await page.get_by_role(
                "button", name="Edit motif-review", exact=True
            ).click()
            assert await page.locator('[name="color"]').input_value() == "#224488"
            await page.locator('[name="color"]').fill("#33cc99")
            await page.locator('[name="name"]').fill("revised")
            await page.locator("[data-save]").click()
            assert await page.locator("[data-results] tbody tr").count() == 1
            assert (
                await page.locator("[data-results] tbody td").nth(1).inner_text()
                == "revised"
            )
            revised = list(
                csv.DictReader(io.StringIO(await exported("[data-download]")))
            )
            assert revised[0]["color"] == "#33cc99"
            # Capture the working chart and external application table for visual QA.
            await page.screenshot(
                path=str(tmp_path / "squid-review.png"), full_page=True
            )
            await page.get_by_role("button", name="Remove revised", exact=True).click()
            assert await page.locator("[data-results] tbody tr").count() == 0
            assert await page.locator("[data-download]").is_disabled()
            assert not errors
            await browser.close()

    asyncio.run(run())
