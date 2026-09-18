"""Exercise the real WebSocket example, including per-browser isolation."""

import asyncio
import base64
from contextlib import suppress
from importlib.resources import files
import json
from pathlib import Path
import runpy

import pytest

playwright = pytest.importorskip("playwright.async_api")
web = pytest.importorskip("aiohttp.web")
test_utils = pytest.importorskip("aiohttp.test_utils")
EXAMPLE = Path(__file__).parents[2] / "docs" / "integration"


def test_python_web_annotations(monkeypatch):
    monkeypatch.syspath_prepend(str(EXAMPLE))
    server_module = runpy.run_path(str(EXAMPLE / "server.py"))

    async def run():
        async with test_utils.TestServer(server_module["create_app"]()) as server:
            async with playwright.async_playwright() as runtime:
                browser = await runtime.chromium.launch()
                first = await browser.new_page()
                second = await browser.new_page()
                errors = []
                first.on("pageerror", lambda error: errors.append(str(error)))
                url = str(server.make_url("/"))
                await first.goto(url)
                await second.goto(url)
                for page in (first, second):
                    await page.wait_for_function(
                        "document.querySelector('#status').textContent.startsWith('Ready')"
                    )
                # Actual mouse events go browser -> Python -> browser.
                bounds = await first.locator("canvas").first.bounding_box()
                await first.mouse.move(bounds["x"] + 140, bounds["y"] + 45)
                await first.mouse.down()
                await first.mouse.move(bounds["x"] + 330, bounds["y"] + 45, steps=8)
                await first.mouse.up()
                await first.wait_for_function(
                    "document.querySelector('#status').textContent.startsWith('Python saved 1 region')"
                )
                assert "chrDemo" in await first.locator("#status").inner_text()
                assert (await second.locator("#status").inner_text()).startswith(
                    "Ready"
                )
                await first.reload()
                await first.wait_for_function(
                    "document.querySelector('#status').textContent.startsWith('Ready')"
                )
                assert not errors
                # Reject connections initiated by unrelated websites.
                import aiohttp

                async with aiohttp.ClientSession() as client:
                    with pytest.raises(aiohttp.WSServerHandshakeError) as error:
                        await client.ws_connect(
                            server.make_url("/ws"), origin="https://unrelated.test"
                        )
                    assert error.value.status == 403
                await browser.close()

    asyncio.run(run())


def test_downloadable_notebook_widget(monkeypatch):
    """Run the actual notebook cell against a browser-rendered widget adapter."""
    import IPython.display

    monkeypatch.syspath_prepend(str(EXAMPLE))
    monkeypatch.setattr(IPython.display, "display", lambda *args: None)
    notebook = json.loads((EXAMPLE / "notebook.ipynb").read_text())
    source = next(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )

    async def run():
        namespace = {}
        exec(compile(source, "notebook.ipynb", "exec"), namespace)
        widget = namespace["widget"]
        outgoing = asyncio.Queue()
        widget.send = outgoing.put_nowait
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page()
            await page.expose_binding(
                "toPython",
                lambda source, message: widget._handle_custom_msg(message, []),
            )
            await page.set_content('<div id="chart"></div>')
            module = (
                "data:text/javascript;base64,"
                + base64.b64encode(
                    files("genome_spy").joinpath("static", "widget.js").read_bytes()
                ).decode()
            )
            await page.evaluate(
                """async ({module, state}) => {
                const handlers = new Map();
                const model = {
                    get: name => state[name], set: (name, value) => state[name] = value,
                    save_changes: () => {}, send: message => window.toPython(message),
                    on: (name, fn) => { if (!handlers.has(name)) handlers.set(name, new Set()); handlers.get(name).add(fn); },
                    off: (name, fn) => handlers.get(name)?.delete(fn),
                };
                window.receive = message => {
                    for (const fn of handlers.get('msg:custom') ?? []) fn(message);
                };
                const {renderChart} = await import(module);
                await renderChart({model, el: document.querySelector('#chart'), signal: new AbortController().signal});
            }""",
                {"module": module, "state": widget.get_state()},
            )

            async def pump():
                while True:
                    await page.evaluate(
                        "message => window.receive(message)", await outgoing.get()
                    )

            sender = asyncio.create_task(pump())
            try:
                async with asyncio.timeout(30):
                    while not namespace["status"].value.startswith("Ready"):
                        if namespace["connection_task"].done():
                            pytest.fail(namespace["status"].value)
                        await asyncio.sleep(0.05)
                    bounds = await page.locator("canvas").first.bounding_box()
                    await page.mouse.move(bounds["x"] + 140, bounds["y"] + 45)
                    await page.mouse.down()
                    await page.mouse.move(bounds["x"] + 330, bounds["y"] + 45, steps=8)
                    await page.mouse.up()
                    while not namespace["annotations"]:
                        await asyncio.sleep(0.05)
                assert namespace["annotations"][0]["chrom"] == "chrDemo"
                assert "Python saved 1 region" in namespace["status"].value
            finally:
                namespace["connection_task"].cancel()
                with suppress(asyncio.CancelledError):
                    await namespace["connection_task"]
                sender.cancel()
                with suppress(asyncio.CancelledError):
                    await sender
                widget.close()
                await browser.close()

    asyncio.run(run())
