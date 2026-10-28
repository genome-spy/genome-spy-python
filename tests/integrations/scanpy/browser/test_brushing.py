"""Observe native brush counts and ordinary widget trait delivery."""

import base64
import json
import xml.etree.ElementTree as ET
from io import BytesIO
from urllib.parse import quote

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy._embed import bundled_module_url
from genome_spy.integrations.scanpy._embedding.interactions import (
    brush_count,
    brush_owner,
)
from tests.browser.test_embed_api import module_url
from tests.integrations.scanpy.helpers import points, units

ad = pytest.importorskip("anndata")
pytest.importorskip("scanpy")
Image = pytest.importorskip("PIL.Image")


def test_native_count_updates_during_drag_without_changing_points(page):
    from tests.integrations.scanpy.browser.rendering import render

    brush = gs.selection_interval("cells", encodings=["x", "y"])
    points = (
        gs.Chart()
        .mark_point(filled=True, fillOpacity=0.85, strokeWidth=0)
        .encode(
            x=gs.X("x:Q").scale(domain=[0, 4], nice=False, zoom=True),
            y=gs.Y("y:Q").scale(domain=[0, 4], nice=False, zoom=True),
            size=gs.value(49),
        )
        .properties(width=240, height=240)
        .configure_view(strokeWidth=0)
    )
    data = [{"x": x, "y": y} for x, y in [(1, 1), (1, 1), (2, 2), (3, 1)]]
    chart = (
        gs.vconcat(
            brush_owner(points, brush, "plain"),
            brush_count(brush, ("x", "y"), name="count", width=240),
        )
        .resolve_scale(x="independent", y="independent")
        .properties(
            data=gs.Data(
                url="data:application/json," + quote(json.dumps(data)),
                format=gs.DataFormat(type="json"),
            )
        )
        .add_params(
            gs.param(
                "cells", value={"type": "interval", "intervals": {"x": None, "y": None}}
            )
        )
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()

    def position(x, y):
        return (
            canvas["x"] + bounds["x"] + bounds["width"] * x / 4,
            canvas["y"] + bounds["y"] + bounds["height"] * (1 - y / 4),
        )

    def observe(expected):
        svg = page.evaluate("async()=>(await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert f"{expected} cells selected" in texts, texts

        def point_states(element, opacity=1):
            opacity = float(element.get("fill-opacity", opacity))
            if element.tag.endswith("circle"):
                yield element.attrib, opacity
            for child in element:
                yield from point_states(child, opacity)

        circles = list(point_states(root))
        assert len(circles) == 4
        assert {opacity for _, opacity in circles} == {0.85}
        return circles

    original = observe(0)
    page.keyboard.down("Shift")
    page.mouse.move(*position(0.5, 0.5))
    page.mouse.down()
    page.mouse.move(*position(1.5, 1.5), steps=3)
    assert observe(2) == original
    page.mouse.move(*position(3.5, 2.5), steps=3)
    assert observe(4) == original
    page.mouse.up()
    page.keyboard.up("Shift")
    page.mouse.dblclick(*position(3.8, 3.8))
    assert observe(0) == original
    for intervals in (
        {"x": [3.5, 3.8], "y": [3.5, 3.8]},
        {"x": [1, 1], "y": [0, 4]},
        {"x": [0, 4], "y": None},
    ):
        page.evaluate(
            "intervals => api.getParam('cells').setValue({type:'interval',intervals})",
            intervals,
        )
        assert observe(0) == original


@pytest.mark.smoke
@pytest.mark.parametrize("zoom", [False, True])
def test_linked_brush_widget_traits_count_and_offline_html(tmp_path, zoom, page):
    adata = ad.AnnData(
        obs=pd.DataFrame(
            {
                "cell_type": pd.Categorical(["A", "A", "B", "A"]),
                "score": [0.0, 4.0, 1.0, 9.0],
            },
            index=["a", "coincident", "b", "c"],
        ),
        obsm={"X_umap": np.array([[1.0, 1.0], [1.0, 1.0], [2.0, 2.0], [3.0, 1.0]])},
    )
    brush = gs.selection_interval("cells", encodings=["x", "y"])
    chart = gsc.pl.umap(
        adata,
        color=["cell_type", "score"],
        selection=brush,
        size=200,
        width=280,
        height=240,
        zoom=zoom,
        hover=False,
        show=False,
    )
    spec = chart.to_dict()
    panels = units(spec["vconcat"][0])
    panels[1]["name"] = "expression-panel"
    widget = gs.JupyterChart(
        spec, inline=True, controls=False, parameter_names=[brush.name]
    )
    try:
        page.set_viewport_size({"width": 1200, "height": 700})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error).splitlines()[0]))
        page.set_content('<style>body{margin:0}</style><div id="chart"></div>')
        received = []

        def sync(_source, values):
            received.append(values)
            widget.parameter_values = values

        page.expose_binding("syncTraits", sync)
        # Capture only the public native API for layout/export assertions.
        # The rendered widget uses the shipped bundle without modification.
        wrapper = (
            f"import {{embed}} from {bundled_module_url('embed')!r};"
            "export async function embedChart(...args){window.api=await embed(...args);return window.api;}"
            "export {embedChart as embed};"
        )
        state = widget.get_state()
        state["bundle_url"] = (
            "data:text/javascript;base64," + base64.b64encode(wrapper.encode()).decode()
        )
        page.evaluate(
            """async ({module,state}) => {
            const handlers = new Map();
            window.hostDrags = 0;
            document.addEventListener('mousedown', () => window.hostDrags++);
            const model = {
              get: name => state[name], set: (name,value) => state[name]=value,
              save_changes: () => window.syncTraits(state.parameter_values), send() {},
              on: (name,fn) => {if (!handlers.has(name)) handlers.set(name,new Set()); handlers.get(name).add(fn);},
              off: (name,fn) => handlers.get(name)?.delete(fn),
            };
            const controller = new AbortController();
            window.dispose = () => controller.abort();
            const {renderChart} = await import(module);
            await renderChart({model,el:document.querySelector('#chart'),signal:controller.signal});
            window.widgetError = () => state.error;
            }""",
            {"module": module_url("widget.js"), "state": state},
        )
        assert page.evaluate("widgetError()") == ""
        page.wait_for_function("window.api && document.querySelector('canvas')")
        page.wait_for_function(
            "Math.abs(document.querySelector('canvas').getBoundingClientRect().width-api.getLogicalCanvasSize().width)<0.1"
        )
        bounds = page.evaluate(
            "['umap-brush-cells','expression-panel'].map(view=>api.views.getLayoutBounds({scope:[],view}))"
        )
        canvas = page.locator("canvas").first
        box = canvas.bounding_box()

        def position(panel, x, y):
            xd, yd = [
                points(panels[panel])["encoding"][c]["scale"]["domain"]
                for c in ("x", "y")
            ]
            b = bounds[panel]
            return (
                b["x"] + b["width"] * (x - xd[0]) / (xd[1] - xd[0]),
                b["y"] + b["height"] * (1 - (y - yd[0]) / (yd[1] - yd[0])),
            )

        def samples():
            pixels = Image.open(BytesIO(canvas.screenshot())).convert("RGB")
            return np.array(
                [
                    [
                        pixels.getpixel(tuple(round(v) for v in position(panel, *xy)))
                        for xy in [(1, 1), (2, 2), (3, 1)]
                    ]
                    for panel in range(2)
                ]
            )

        def count():
            return page.evaluate("""async () => {
              const result = await api.imageExport.svg();
              const svg = new DOMParser().parseFromString(await result.blob.text(),'image/svg+xml');
              return [...svg.querySelectorAll('text')].map(t=>t.textContent).find(t=>t.endsWith(' cells selected'));
            }""")

        def drag(panel, start, end, *, count_during_drag=False):
            if zoom:
                page.keyboard.down("Shift")
            x, y = position(panel, *start)
            page.mouse.move(box["x"] + x, box["y"] + y)
            page.mouse.down()
            x, y = position(panel, *end)
            page.mouse.move(box["x"] + x, box["y"] + y, steps=15)
            if count_during_drag:
                assert count() == "3 cells selected"
            page.mouse.up()
            if zoom:
                page.keyboard.up("Shift")

        assert count() == "0 cells selected"
        assert not gsc.selection_mask(
            adata, widget.parameter_values.get(brush.name)
        ).any()
        before = samples()
        # Start inside the plot; its lower y boundary is exactly 0.95.
        drag(0, (0.98, 0.98), (2.4, 2.05), count_during_drag=True)
        page.screenshot(path=str(tmp_path / "brush-gesture.png"))
        assert page.evaluate("api.getParam('cells').getValue().intervals.x !== null"), (
            bounds,
            box,
            errors,
        )
        page.wait_for_timeout(100)
        snapshot = widget.parameter_values[brush.name]
        assert adata.obs_names[gsc.selection_mask(adata, snapshot)].tolist() == [
            "a",
            "coincident",
            "b",
        ]
        assert "data" not in snapshot
        assert count() == "3 cells selected"
        assert page.evaluate("hostDrags") == 0
        after = samples()
        np.testing.assert_allclose(after, before, atol=15)
        page.screenshot(path=str(tmp_path / "linked-brush.png"))
        drag(1, (2.6, 0.98), (3.05, 1.4))
        assert page.evaluate("api.getParam('cells').getValue()") == snapshot
        # Exact lower/upper edges agree across the native count and Python.
        page.evaluate(
            "api.getParam('cells').setValue({type:'interval',intervals:{x:[1,3],y:[1,3]}})"
        )
        page.wait_for_timeout(50)
        assert count() == "3 cells selected"
        assert gsc.selection_mask(
            adata, widget.parameter_values[brush.name]
        ).tolist() == [True, True, True, False]
        page.evaluate(
            "api.getParam('cells').setValue({type:'interval',intervals:{x:null,y:null}})"
        )
        assert count() == "0 cells selected"
        np.testing.assert_array_equal(samples(), before)
        # Double-click is the user-facing clear gesture.
        drag(0, (0.98, 0.98), (2.4, 2.05))
        x, y = position(0, 2.7, 1.7)
        page.mouse.dblclick(box["x"] + x, box["y"] + y)
        assert count() == "0 cells selected"
        assert not gsc.selection_mask(adata, widget.parameter_values[brush.name]).any()
        updates = len(received)
        page.evaluate("dispose()")
        page.wait_for_timeout(50)
        assert len(received) == updates
        assert not errors
        # Standalone HTML keeps the native count and linked highlighting.
        output = tmp_path / "linked-umap.html"
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
        canvas.wait_for(state="visible")
        page.wait_for_function("""() => {
          const c = document.querySelector('canvas');
          return Math.abs(c.getBoundingClientRect().width - c.width/devicePixelRatio) < 1;
        }""")
        box = canvas.bounding_box()
        offline_before = samples()
        box = canvas.bounding_box()
        drag(0, (0.98, 0.98), (2.4, 2.05))
        offline_after = samples()
        page.screenshot(path=str(tmp_path / "offline-brush.png"))
        np.testing.assert_allclose(offline_after, offline_before, atol=15)
        assert not requests
        assert not errors
    finally:
        widget.close()
