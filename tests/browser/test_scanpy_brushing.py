"""Native WebGL brush gestures, Python deliveries, and notebook membership."""

import asyncio
from io import BytesIO

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.scanpy as gsc
from genome_spy._embed import bundled_module_url
from genome_spy.embed import EmbedError, attach_embed
from tests.browser.test_embed_api import module_url
from tests.test_scanpy_brushing_notebook import selection_namespace
from tests.test_scanpy_umap import units

ad = pytest.importorskip("anndata")
pytest.importorskip("scanpy")
playwright = pytest.importorskip("playwright.async_api")
Image = pytest.importorskip("PIL.Image")


@pytest.mark.parametrize("zoom", [False, True])
def test_linked_brush_debounces_python_ids_and_releases_subscriptions(tmp_path, zoom):
    async def run():
        adata = ad.AnnData(
            np.zeros((4, 1)),
            obs=pd.DataFrame(
                {
                    "cell_id": ["a", "duplicate-coordinate", "b", "c"],
                    "cell_type": pd.Categorical(["A", "A", "B", "A"]),
                    "score": [0.0, 4.0, 1.0, 9.0],
                },
                index=["a", "duplicate-coordinate", "b", "c"],
            ),
            obsm={"X_umap": np.array([[1.0, 1.0], [1.0, 1.0], [2.0, 2.0], [3.0, 1.0]])},
        )
        brush = gs.selection_interval("cells", encodings=["x", "y"])
        settled = gs.param("settled_cells", expr=brush.name, debounce=150)
        chart = gsc.pl.umap(
            adata,
            color=["cell_type", "score"],
            obs_id="cell_id",
            selection=brush,
            size=200,
            width=280,
            height=240,
            zoom=zoom,
            hover=False,
            show=False,
        ).add_params(settled)
        spec = chart.to_dict()
        panels = units(spec)
        panels[1]["name"] = "expression-panel"
        namespace = selection_namespace(adata)
        async with playwright.async_playwright() as runtime:
            browser = await runtime.chromium.launch()
            page = await browser.new_page(viewport={"width": 1200, "height": 600})
            errors = []
            page.on(
                "pageerror", lambda error: errors.append(str(error).splitlines()[0])
            )
            await page.set_content(
                '<style>body{margin:0}</style><div id="chart"></div>'
            )
            listeners = []
            queue = asyncio.Queue()
            events = asyncio.Queue()

            def subscribe(callback):
                listeners.append(callback)
                return lambda: listeners.remove(callback)

            await page.expose_binding(
                "toPython",
                lambda source, message: [cb(message) for cb in list(listeners)],
            )
            await page.evaluate(
                """async ({core,bridge,spec}) => {
                const {embed}=await import(core);
                const {createEmbedBridge}=await import(bridge);
                window.api=await embed(document.querySelector('#chart'),spec,{renderer:'webgl'});
                window.bridge=createEmbedBridge(api,m=>window.toPython(m));
                window.receive=m=>window.bridge.receive(m);
            }""",
                {
                    "core": bundled_module_url("embed"),
                    "bridge": module_url("embed-bridge.js"),
                    "spec": spec,
                },
            )

            async def pump():
                while True:
                    await page.evaluate("m=>window.receive(m)", await queue.get())

            worker = asyncio.create_task(pump())
            try:
                async with asyncio.timeout(30):
                    api = await attach_embed(queue.put_nowait, subscribe)
                    owner = await api.views.get(
                        {"scope": [], "view": "umap-brush-cells"}
                    )
                    selection = await owner.params.get_selection(brush.name)

                    def observe(snapshot):
                        namespace["show_selection"](snapshot)
                        events.put_nowait(snapshot)

                    updates = await api.params.get(settled.name)
                    stop = await updates.subscribe(observe)
                    namespace["show_selection"](await selection.get_value())
                    assert namespace["selected_ids"] == []
                    await page.wait_for_function(
                        "Math.abs(document.querySelector('canvas').getBoundingClientRect().width-api.getLogicalCanvasSize().width)<0.1"
                    )
                    bounds = await page.evaluate(
                        "['umap-brush-cells','expression-panel'].map(view=>api.views.getLayoutBounds({scope:[],view}))"
                    )
                    canvas = page.locator("canvas").first
                    box = await canvas.bounding_box()

                    def position(panel, x, y):
                        xd, yd = [
                            panels[panel]["layer"][0]["encoding"][c]["scale"]["domain"]
                            for c in ("x", "y")
                        ]
                        b = bounds[panel]
                        return (
                            b["x"] + b["width"] * (x - xd[0]) / (xd[1] - xd[0]),
                            b["y"] + b["height"] * (1 - (y - yd[0]) / (yd[1] - yd[0])),
                        )

                    async def samples():
                        pixels = Image.open(BytesIO(await canvas.screenshot())).convert(
                            "RGB"
                        )
                        return np.array(
                            [
                                [
                                    pixels.getpixel(
                                        tuple(round(v) for v in position(panel, *xy))
                                    )
                                    for xy in [(1, 1), (2, 2), (3, 1)]
                                ]
                                for panel in range(2)
                            ]
                        )

                    before = await samples()
                    await page.wait_for_timeout(200)
                    while not events.empty():
                        events.get_nowait()
                    if zoom:
                        await page.keyboard.down("Shift")
                    x, y = position(0, 0.95, 0.95)
                    await page.mouse.move(box["x"] + x, box["y"] + y)
                    await page.mouse.down()
                    x, y = position(0, 2.4, 2.05)
                    await page.mouse.move(box["x"] + x, box["y"] + y, steps=20)
                    await page.wait_for_timeout(100)
                    assert events.empty(), (
                        "Debounced delivery published before the quiet period"
                    )
                    await page.mouse.up()
                    if zoom:
                        await page.keyboard.up("Shift")
                    await page.screenshot(path=str(tmp_path / "brush-gesture.png"))
                    assert (await selection.get_value())["active"], (
                        bounds,
                        box,
                        errors,
                    )
                    snapshot = await asyncio.wait_for(events.get(), timeout=3)
                    assert events.empty()
                    assert namespace["selected_ids"] == [
                        "a",
                        "duplicate-coordinate",
                        "b",
                    ]
                    assert "3 cells selected" in namespace["status"].value
                    assert (
                        len(adata[adata.obs["cell_id"].isin(namespace["selected_ids"])])
                        == 3
                    )
                    assert (
                        "data" not in snapshot
                    )  # Only interval bounds cross to Python.
                    after = await samples()
                    assert np.max(np.abs(before[:, :2] - after[:, :2])) < 15
                    for panel in range(2):
                        assert (255 - after[panel, 2]).sum() < 0.3 * (
                            255 - before[panel, 2]
                        ).sum()
                    await page.screenshot(path=str(tmp_path / "linked-brush.png"))
                    # Starting a gesture in the read-only panel cannot replace
                    # the first panel's brush or publish another Python update.
                    if zoom:
                        await page.keyboard.down("Shift")
                    x, y = position(1, 2.6, 0.95)
                    await page.mouse.move(box["x"] + x, box["y"] + y)
                    await page.mouse.down()
                    x, y = position(1, 3.05, 1.4)
                    await page.mouse.move(box["x"] + x, box["y"] + y, steps=10)
                    await page.mouse.up()
                    if zoom:
                        await page.keyboard.up("Shift")
                    assert (await selection.get_value())["intervals"] == snapshot[
                        "intervals"
                    ]
                    assert events.empty()
                    await selection.clear()
                    assert (await events.get())["intervals"] == {"x": None, "y": None}
                    assert namespace["selected_ids"] == []
                    np.testing.assert_array_equal(await samples(), before)
                    # Exact bounds agree in Python and in the native shader:
                    # duplicate observations on the lower edge are included;
                    # C, on the upper x edge, is excluded.
                    parameter = await api.params.get(brush.name)
                    await parameter.set_value(
                        {"type": "interval", "intervals": {"x": [1, 3], "y": [1, 3]}}
                    )
                    await events.get()
                    assert namespace["selected_ids"] == [
                        "a",
                        "duplicate-coordinate",
                        "b",
                    ]
                    edge_pixels = await samples()
                    # The owning panel's brush border covers this exact-edge
                    # point. Its unobscured copy tests native membership.
                    assert (255 - edge_pixels[1, 2]).sum() < 0.3 * (
                        255 - before[1, 2]
                    ).sum()
                    await selection.clear()
                    await events.get()
                    await stop()
                    await parameter.set_value(
                        {"type": "interval", "intervals": {"x": [0, 4], "y": [0, 3]}}
                    )
                    await asyncio.sleep(0.25)
                    assert events.empty()
                    await page.evaluate("bridge.dispose(); api.finalize()")
                    with pytest.raises(EmbedError):
                        await selection.get_value()
                    assert not listeners
                    assert not errors
                output = tmp_path / "linked-umap.html"
                chart.save(output, inline=True, controls=False)
                requests = []
                page.on(
                    "request",
                    lambda request: (
                        requests.append(request.url)
                        if request.url.startswith(("http:", "https:"))
                        else None
                    ),
                )
                await page.context.set_offline(True)
                await page.goto(output.as_uri())
                await canvas.wait_for(state="visible")
                await page.wait_for_timeout(300)
                offline_before = await samples()
                box = await canvas.bounding_box()
                if zoom:
                    await page.keyboard.down("Shift")
                x, y = position(0, 0.95, 0.95)
                await page.mouse.move(box["x"] + x, box["y"] + y)
                await page.mouse.down()
                x, y = position(0, 2.4, 2.05)
                await page.mouse.move(box["x"] + x, box["y"] + y, steps=20)
                await page.mouse.up()
                if zoom:
                    await page.keyboard.up("Shift")
                offline_after = await samples()
                for panel in range(2):
                    assert (255 - offline_after[panel, 2]).sum() < 0.3 * (
                        255 - offline_before[panel, 2]
                    ).sum()
                assert not requests
                assert not errors
            finally:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    pass
                await browser.close()

    asyncio.run(run())
