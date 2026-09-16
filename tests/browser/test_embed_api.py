"""The same thin API over a plain browser host and the anywidget adapter."""

import asyncio
import base64
from importlib.resources import files
from typing import Any

import pytest

from genome_spy._embed import bundled_module_url
from genome_spy._widget import JupyterChart
from genome_spy.embed import EmbedError, attach_embed

playwright = pytest.importorskip("playwright.async_api")
STATIC = files("genome_spy").joinpath("static")


def module_url(name: str) -> str:
    return (
        "data:text/javascript;base64,"
        + base64.b64encode((STATIC / name).read_bytes()).decode()
    )


@pytest.mark.parametrize("host", ["browser", "widget"])
def test_live_embed_api(host: str) -> None:
    async def run() -> None:
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page()
            spec = {
                "width": 400,
                "height": 200,
                "datasets": {"table": [{"x": 1, "y": 2}, {"x": 2, "y": 3}]},
                "data": {"name": "table"},
                "mark": "point",
                "params": [
                    {"name": "threshold", "value": 1},
                    {"name": "doubled", "expr": "threshold * 2"},
                    {
                        "name": "brush",
                        "select": {"type": "interval", "encodings": ["x"]},
                    },
                    {"name": "selected", "select": "point"},
                ],
                "encoding": {
                    "x": {"field": "x", "type": "quantitative"},
                    "y": {"field": "y", "type": "quantitative"},
                },
            }
            queue: asyncio.Queue[Any] = asyncio.Queue()
            listeners: list[Any] = []

            def subscribe(callback: Any) -> Any:
                listeners.append(callback)
                return lambda: listeners.remove(callback)

            def receive(_source: Any, message: Any) -> None:
                for callback in list(listeners):
                    callback(message)

            await page.expose_binding("toPython", receive)
            await page.set_content('<div id="chart"></div>')
            widget = None
            if host == "browser":
                await page.evaluate(
                    """async ({core, bridge, spec}) => {
                  const {embed} = await import(core);
                  const {createEmbedBridge} = await import(bridge);
                  window.api = await embed(document.querySelector('#chart'), spec, {renderer: 'canvas'});
                  window.bridge = createEmbedBridge(window.api, m => window.toPython(m));
                  window.receive = m => window.bridge.receive(m);
                  window.dispose = () => { window.bridge.dispose(); window.api.finalize(); };
                }""",
                    {
                        "core": bundled_module_url("embed"),
                        "bridge": module_url("embed-bridge.js"),
                        "spec": spec,
                    },
                )
            else:
                widget = JupyterChart(
                    spec,
                    inline=True,
                    controls=False,
                    embed_options={"renderer": "canvas"},
                )
                widget.send = queue.put_nowait
                listeners.append(lambda m: widget._handle_custom_msg(m, []))
                await page.evaluate(
                    """async ({module, state}) => {
                  const handlers = new Map();
                  const model = {
                    get: name => state[name], set: (name, value) => state[name] = value,
                    save_changes: () => {}, send: m => window.toPython(m),
                    on: (name, fn) => { if (!handlers.has(name)) handlers.set(name, new Set()); handlers.get(name).add(fn); },
                    off: (name, fn) => handlers.get(name)?.delete(fn),
                  };
                  const controller = new AbortController();
                  window.receive = m => { for (const fn of handlers.get('msg:custom') ?? []) fn(m); };
                  window.dispose = () => controller.abort();
                  const {renderChart} = await import(module);
                  await renderChart({model, el: document.querySelector('#chart'), signal: controller.signal});
                }""",
                    {"module": module_url("widget.js"), "state": widget.get_state()},
                )

            async def pump() -> None:
                while True:
                    message = await queue.get()
                    await page.evaluate("m => window.receive(m)", message)

            worker = asyncio.create_task(pump())
            try:
                async with asyncio.timeout(20):
                    api = (
                        await widget.get_embed_api()
                        if widget
                        else await attach_embed(queue.put_nowait, subscribe)
                    )
                    parameter = await api.params.get("threshold")
                    doubled = await api.params.get("doubled")
                    await parameter.set_value(3)
                    assert await parameter.get_value() == 3
                    assert await doubled.get_value() == 6
                    with pytest.raises(EmbedError, match="computed"):
                        await doubled.set_value(7)
                    with pytest.raises(EmbedError, match="not found"):
                        await api.params.get("missing")

                    brush = await api.params.get_selection("brush")
                    assert brush.type == "interval"
                    assert (await brush.get_value())["active"] is False
                    point = await api.params.get_selection("selected")
                    assert point.type == "point"
                    assert (await point.get_value())["data"] == []
                    events: asyncio.Queue[Any] = asyncio.Queue()
                    stop = await brush.subscribe(
                        events.put_nowait, {"delivery": "commit"}
                    )
                    assert events.empty()
                    brush_param = await api.params.get("brush")
                    await brush_param.set_value(
                        {"type": "interval", "intervals": {"x": [0.5, 1.5]}}
                    )
                    snapshot = await events.get()
                    assert snapshot["active"] is True
                    assert snapshot["intervals"]["x"] == [0.5, 1.5]
                    assert snapshot["complexIntervals"]["x"] == [0.5, 1.5]
                    await brush.clear()
                    assert (await events.get())["active"] is False
                    await stop()

                    canvas = page.locator("canvas").first
                    await page.evaluate("() => new Promise(requestAnimationFrame)")
                    before = await canvas.screenshot()
                    await api.datasets.set("table", [{"x": 0.25, "y": 8}])
                    await page.evaluate("() => new Promise(requestAnimationFrame)")
                    assert await canvas.screenshot() != before
                    with pytest.raises(EmbedError):
                        await api.datasets.set("missing", [])
                    await api.datasets.reset("table")
                    await page.evaluate("() => window.dispose()")
                    await asyncio.sleep(0)
                    with pytest.raises(EmbedError):
                        await parameter.get_value()
            finally:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    pass
                if widget:
                    widget.close()
                await browser.close()

    asyncio.run(run())
