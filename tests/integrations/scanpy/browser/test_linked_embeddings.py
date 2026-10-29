"""Linked embeddings behavior and regressions."""

import base64
import json
import re
import xml.etree.ElementTree as ET
from io import BytesIO
from urllib.parse import quote

import numpy as np
import pandas as pd
import pytest
from PIL import Image, ImageColor

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy._embed import bundled_module_url
from genome_spy.integrations.scanpy._embedding.interactions import (
    brush_count,
    brush_owner,
)
from tests.browser.test_embed_api import module_url
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    position,
    render_summary,
    rows,
    set_brush,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.embedding_fixtures import adata as adata
from tests.integrations.scanpy.embedding_fixtures import (
    metadata_adata as metadata_adata,
)
from tests.integrations.scanpy.helpers import points, units

ad = pytest.importorskip("anndata")
pytest.importorskip("scanpy")
pytest.importorskip("PIL.Image")


class TestBrushing:
    """Observe native brush counts and ordinary widget trait delivery."""

    def test_native_count_updates_during_drag_without_changing_points(self, page):
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
                    "cells",
                    value={"type": "interval", "intervals": {"x": None, "y": None}},
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
                    yield (element.attrib, opacity)
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
    def test_linked_brush_widget_traits_count_and_offline_html(
        self, tmp_path, zoom, page
    ):
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
            page.on(
                "pageerror", lambda error: errors.append(str(error).splitlines()[0])
            )
            page.set_content('<style>body{margin:0}</style><div id="chart"></div>')
            received = []

            def sync(_source, values):
                received.append(values)
                widget.parameter_values = values

            page.expose_binding("syncTraits", sync)
            # Capture only the public native API for layout/export assertions.
            # The rendered widget uses the shipped bundle without modification.
            wrapper = f"import {{embed}} from {bundled_module_url('embed')!r};export async function embedChart(...args){{window.api=await embed(...args);return window.api;}}export {{embedChart as embed}};"
            state = widget.get_state()
            state["bundle_url"] = (
                "data:text/javascript;base64,"
                + base64.b64encode(wrapper.encode()).decode()
            )
            page.evaluate(
                "async ({module,state}) => {\n            const handlers = new Map();\n            window.hostDrags = 0;\n            document.addEventListener('mousedown', () => window.hostDrags++);\n            const model = {\n              get: name => state[name], set: (name,value) => state[name]=value,\n              save_changes: () => window.syncTraits(state.parameter_values), send() {},\n              on: (name,fn) => {if (!handlers.has(name)) handlers.set(name,new Set()); handlers.get(name).add(fn);},\n              off: (name,fn) => handlers.get(name)?.delete(fn),\n            };\n            const controller = new AbortController();\n            window.dispose = () => controller.abort();\n            const {renderChart} = await import(module);\n            await renderChart({model,el:document.querySelector('#chart'),signal:controller.signal});\n            window.widgetError = () => state.error;\n            }",
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
                            pixels.getpixel(
                                tuple((round(v) for v in position(panel, *xy)))
                            )
                            for xy in [(1, 1), (2, 2), (3, 1)]
                        ]
                        for panel in range(2)
                    ]
                )

            def count():
                return page.evaluate(
                    "async () => {\n              const result = await api.imageExport.svg();\n              const svg = new DOMParser().parseFromString(await result.blob.text(),'image/svg+xml');\n              return [...svg.querySelectorAll('text')].map(t=>t.textContent).find(t=>t.endsWith(' cells selected'));\n            }"
                )

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
            assert page.evaluate(
                "api.getParam('cells').getValue().intervals.x !== null"
            ), (bounds, box, errors)
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
            assert not gsc.selection_mask(
                adata, widget.parameter_values[brush.name]
            ).any()
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
            page.wait_for_function(
                "() => {\n          const c = document.querySelector('canvas');\n          return Math.abs(c.getBoundingClientRect().width - c.width/devicePixelRatio) < 1;\n        }"
            )
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


class TestEmbeddingSummary:
    """Observed native placement, missing values and scoped brush updates."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("cmap", ["seurat", "viridis"])
    def test_fitted_heatmap_values_follow_brush_means_contrast_and_clear(
        self, page, adata, cmap
    ):
        adata.X[1, 0] = 1
        chart = (
            gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
            .add_heatmap(show_values=True, cmap=cmap, vmin=-1, vmax=2)
            .to_chart()
        )
        names = render_summary(page, chart)
        assert not value_texts(svg_root(page))
        set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
        labels = value_texts(svg_root(page))
        assert sorted((e.text for e in labels)) == ["0.00", "1.17"]
        assert {e.text: e.get("fill") for e in labels} == {
            "0.00": "white",
            "1.17": "black",
        }
        means = rows(page, names["selected-expression"])
        assert all((row["gene"] == "HLA-DRA" for row in means))
        assert {row["_group"]: row["mean"] for row in means} == pytest.approx(
            {"A": 0, "B": 3.5 / 3}
        )
        set_brush(page, {"x": [-1, 1.5], "y": [-1, 0.5]})
        assert [e.text for e in value_texts(svg_root(page))] == ["0.00"]
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
            names["umap-brush-cells"],
        )
        assert not value_texts(svg_root(page))

    @pytest.mark.parametrize("hidden", [False, True])
    def test_panel_titles_render_custom_text_or_hide_without_fallback(
        self, page, metadata_adata, hidden
    ):
        titles = ["Cell map", "Marker means", "QC distribution", "Sample mix"]
        selected = [None] * 4 if hidden else titles
        chart = (
            gsc.pl.EmbeddingSummary(
                metadata_adata,
                "HLA-DRA",
                "type",
                obs_keys=["sample.label", "qc.score"],
                title=selected[0],
            )
            .add_heatmap(title=selected[1])
            .add_histogram(obs="qc.score", title=selected[2])
            .add_composition("sample.label", title=selected[3])
            .to_chart()
        )
        render_summary(page, chart)
        text = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
        for title in titles:
            assert (title in text) is not hidden
        assert not set(text).intersection(
            {
                "Selected cells: mean expression",
                "qc.score: selection vs all cells",
                "sample.label: composition",
            }
        )
        # The heatmap axis retains the grouping label.
        assert text.count("type") == 1

    @pytest.mark.smoke
    def test_composition_and_numeric_metadata_match_source_and_keep_reference(
        self, page, metadata_adata
    ):
        chart = (
            gsc.pl.EmbeddingSummary(
                metadata_adata, "HLA-DRA", "type", obs_keys=["sample.label", "qc.score"]
            )
            .add_composition("sample.label")
            .add_histogram(obs="qc.score")
            .to_chart()
        )
        names = render_summary(page, chart)
        reference = rows(page, "all-composition")
        histogram = rows(page, "all-observation-histogram")
        assert {row["_obs_1"]: row["count"] for row in reference} == {
            "D1": 2,
            "D2": 2,
            "D3": 1,
            "NA": 1,
        }
        assert all((row["total"] == 6 for row in reference))
        assert sum((row["percent"] for row in reference)) == pytest.approx(100)
        assert rows(page, "selected-composition") == []
        assert rows(page, "selected-observation-histogram") == []
        set_brush(page, {"x": [-0.1, 3.1], "y": [-0.1, 1.1]})
        selected = rows(page, "selected-composition")
        assert {row["_obs_1"]: row["count"] for row in selected} == {
            "D1": 2,
            "D2": 1,
            "NA": 1,
        }
        for row in selected:
            assert row["total"] == 4
            assert row["percent"] == pytest.approx(100 * row["count"] / 4)
        bins = rows(page, "selected-observation-histogram")
        assert {row["bin_start"]: row["count"] for row in bins} == {
            -0.5: 1,
            0: 1,
            0.5: 1,
        }
        assert all(
            (
                row["total"] == 3 and row["percent"] == pytest.approx(100 / 3)
                for row in bins
            )
        )
        coverage = rows(page, names["selected-observation-coverage"])[0]
        assert (coverage["valid"], coverage["missing"]) == (3, 1)
        root = svg_root(page)
        labels = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert "Unused" in labels and "NA" in labels
        assert "Selected: 3 valid, 1 missing" in labels
        rectangles = [
            e
            for g in root.iter()
            if g.get("data-name") in ("all-composition", "selected-composition")
            for e in g.iter()
            if e.tag.endswith("rect")
        ]
        assert len(rectangles) == 7
        assert all((float(e.get("height")) > 0 for e in rectangles))
        cohort_rectangles = {
            name: [
                e
                for g in root.iter()
                if g.get("data-name") == name
                for e in g.iter()
                if e.tag.endswith("rect")
            ]
            for name in ("all-composition", "selected-composition")
        }
        for category in ("D1", "D2", "NA"):
            a = cohort_rectangles["all-composition"][
                next(
                    (i for i, row in enumerate(reference) if row["_obs_1"] == category)
                )
            ]
            b = cohort_rectangles["selected-composition"][
                next((i for i, row in enumerate(selected) if row["_obs_1"] == category))
            ]
            assert abs(float(a.get("y")) - float(b.get("y"))) >= min(
                float(a.get("height")), float(b.get("height"))
            )
        set_brush(page, {"x": [20, 21], "y": [20, 21]})
        assert rows(page, "selected-composition") == []
        assert rows(page, "selected-observation-histogram") == []
        assert rows(page, names["selected-observation-coverage"]) == []
        assert rows(page, "all-composition") == reference
        assert rows(page, "all-observation-histogram") == histogram

    @pytest.mark.smoke
    def test_count_is_visible_inside_brush_and_moves_during_drag(self, page, adata):
        chart = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").to_chart()
        names = render_summary(page, chart)
        bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-brush-cells"],
        )
        canvas = page.locator("canvas").first.bounding_box()
        origin = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        before = rows(page, "umap-points")

        def label_geometry():
            root = svg_root(page)
            label = next(
                (
                    e
                    for e in root.iter()
                    if e.tag.endswith("text")
                    and re.fullmatch("[\\d,]+ cells", e.text or "")
                )
            )
            rect = next(
                (
                    e
                    for g in root.iter()
                    if g.get("data-name") == "selectionRectRect"
                    for e in g.iter()
                    if e.tag.endswith("rect")
                )
            )
            x, y = position(label)
            left, top = (float(rect.get("x")), float(rect.get("y")))
            assert left < x < left + float(rect.get("width"))
            assert top < y < top + float(rect.get("height"))
            image = np.asarray(
                Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
                    "RGB"
                )
            )
            region = image[int(y) : int(y) + 16, int(x) : int(x) + 65]
            assert np.sum(np.all(region < 80, axis=2)) > 5
            assert label.text == f"{rows(page, 'umap-count-cells')[0]['count']} cells"
            return (x, y)

        page.mouse.move(origin[0] + bounds["width"] * 0.5, origin[1] + 30)
        page.mouse.down()
        page.mouse.move(
            origin[0] + bounds["width"] - 10, origin[1] + bounds["height"] - 10, steps=6
        )
        first = label_geometry()
        page.mouse.move(origin[0] + 5, origin[1] + bounds["height"] - 10, steps=6)
        second = label_geometry()
        assert second[0] < first[0]
        assert rows(page, "umap-points") == before
        page.mouse.move(origin[0] + bounds["width"] * 0.5 + 2, origin[1] + 32)
        assert not any(
            (
                e.tag.endswith("text") and re.fullmatch("[\\d,]+ cells", e.text or "")
                for e in svg_root(page).iter()
            )
        )
        page.mouse.up()
        set_brush(page, {"x": [0, 2], "y": [2.5, 3.5]})
        assert rows(page, "umap-count-cells")[0]["count"] == 0
        label_geometry()
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
            names["umap-brush-cells"],
        )
        assert not any(
            (
                e.tag.endswith("text") and re.fullmatch("[\\d,]+ cells", e.text or "")
                for e in svg_root(page).iter()
            )
        )

    @pytest.mark.parametrize("show_count", [False, True])
    def test_show_count_changes_only_the_label_not_the_brush_or_histogram(
        self, page, adata, show_count
    ):
        chart = (
            gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", show_count=show_count)
            .add_tracks(width=250, height=80)
            .add_histogram()
            .to_chart()
        )
        names = render_summary(page, chart)
        points = rows(page, "umap-points")
        reference = rows(page, "all-expression-histogram")
        bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-brush-cells"],
        )
        canvas = page.locator("canvas").first.bounding_box()
        page.mouse.move(canvas["x"] + bounds["x"] + 8, canvas["y"] + bounds["y"] + 8)
        page.mouse.down()
        page.mouse.move(
            canvas["x"] + bounds["x"] + bounds["width"] - 8,
            canvas["y"] + bounds["y"] + bounds["height"] - 8,
            steps=8,
        )
        page.mouse.up()
        intervals = page.evaluate("api.params.get('cells').getValue().intervals")
        assert intervals["x"] is not None
        labels = [
            e.text
            for e in svg_root(page).iter()
            if e.tag.endswith("text") and re.fullmatch("[\\d,]+ cells", e.text or "")
        ]
        assert labels == (["6 cells"] if show_count else [])
        assert (
            sum((row["count"] for row in rows(page, "selected-expression-histogram")))
            == 5
        )
        assert {row["_obs_id"] for row in rows(page, "tracks-selected-0")} == {
            f"cell-{i}" for i in range(5)
        }
        assert rows(page, "umap-points") == points
        assert rows(page, "all-expression-histogram") == reference
        assert (
            page.evaluate("api.params.get('cells').getValue().intervals") == intervals
        )
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
            names["umap-brush-cells"],
        )
        assert rows(page, "selected-expression-histogram") == []

    @pytest.mark.parametrize("side", ["left", "right", "top", "bottom"])
    def test_real_brush_in_every_panel_position_and_unchanged_points(
        self, page, adata, side
    ):
        chart = (
            gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
            .add_heatmap(position=side, height=360)
            .add_histogram("HLA-DRA", position=side)
            .style(umap_size=240)
            .legend(position=side)
            .to_chart()
        )
        names = render_summary(page, chart)
        bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-brush-cells"],
        )
        assert bounds["width"] == pytest.approx(bounds["height"], abs=0.1)
        heatmap_bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["selected-expression"],
        )
        assert heatmap_bounds["width"] >= 300
        assert heatmap_bounds["height"] >= 360
        reference = rows(page, "all-expression-histogram")
        points_before = rows(page, "umap-points")
        assert rows(page, names["selected-expression"]) == []
        canvas = page.locator("canvas").first.bounding_box()
        x, y = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        page.mouse.move(x + 2, y + 2)
        page.mouse.down()
        page.mouse.move(x + bounds["width"] - 2, y + bounds["height"] - 2, steps=10)
        page.mouse.up()
        page.wait_for_function(
            "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows.length === 2",
            arg=names["selected-expression"],
        )
        actual = rows(page, names["selected-expression"])
        assert {row["gene"] for row in actual} == {"HLA-DRA"}
        assert {row["_group"]: row["cells"] for row in actual} == {"A": 2, "B": 3}
        assert {row["_group"]: row["mean"] for row in actual} == pytest.approx(
            {"A": -0.5, "B": 3.5 / 3}
        )
        assert rows(page, "all-expression-histogram") == reference
        assert rows(page, "umap-points") == points_before
        bins = rows(page, "selected-expression-histogram")
        assert {row["bin_start"]: row["count"] for row in bins} == {
            -1: 1,
            0: 1,
            0.5: 1,
            1: 1,
            2: 1,
        }
        assert all((row["percent"] == 20 for row in bins))
        count = rows(page, "umap-count-cells")
        assert count[0]["count"] == 6
        set_brush(page, {"x": [20, 21], "y": [20, 21]})
        assert rows(page, names["selected-expression"]) == []
        assert rows(page, "selected-expression-histogram") == []
        assert rows(page, "umap-count-cells")[0]["count"] == 0
        assert page.evaluate("api.params.get('cells').getValue().intervals.x") == [
            20,
            21,
        ]
        set_brush(page, {"x": [1, 1], "y": [-1, 3]})
        assert rows(page, names["selected-expression"]) == []
        assert rows(page, "umap-count-cells")[0]["count"] == 0
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
            names["umap-brush-cells"],
        )
        assert page.evaluate("api.params.get('cells').getValue().intervals.x") is None
        assert rows(page, "all-expression-histogram") == reference

    def test_all_missing_gene_has_no_heatmap_mean_or_histogram_zero_bin(
        self, page, adata
    ):
        chart = (
            gsc.pl.EmbeddingSummary(adata, "missing.gene", "type")
            .add_heatmap()
            .add_histogram()
            .to_chart()
        )
        names = render_summary(page, chart)
        set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
        assert rows(page, "umap-count-cells")[0]["count"] == 6
        assert rows(page, names["selected-expression"]) == []
        assert rows(page, "selected-expression-histogram") == []
        assert rows(page, "all-expression-histogram") == []

    def test_two_composed_builders_keep_independent_brush_values(self, page, adata):
        plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_heatmap()
        first = plot.to_chart().properties(name="first")
        second = plot.to_chart().properties(name="second")
        spec = (
            gs.hconcat(first, second)
            .resolve_scale(x="independent", y="independent", color="independent")
            .to_dict()
        )
        views = units(spec)
        first_summary = next(
            (i for i, v in enumerate(views) if v.get("name") == "selected-expression")
        )
        second_summary = max(
            (i for i, v in enumerate(views) if v.get("name") == "selected-expression")
        )
        first_brush = next(
            (i for i, v in enumerate(views) if v.get("name") == "umap-brush-cells")
        )
        render(page, spec)
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.get('cells').setValue({type:'interval',intervals:{x:[-1,6],y:[-1,3]}})",
            f"panel-{first_brush}",
        )
        page.wait_for_function(
            "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows.length === 2",
            arg=f"panel-{first_summary}",
        )
        assert rows(page, f"panel-{second_summary}") == []

    @pytest.mark.xfail(
        strict=True,
        reason="Released Core interval filtering includes upper boundaries; count and selection_mask are half-open",
    )
    def test_exact_brush_boundary_matches_count_summary_and_python_mask(
        self, page, adata
    ):
        chart = (
            gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_heatmap().to_chart()
        )
        names = render_summary(page, chart)
        snapshot = {"type": "interval", "intervals": {"x": [0, 2], "y": [-1, 2]}}
        set_brush(page, snapshot["intervals"])
        expected = gsc.selection_mask(adata, snapshot)
        np.testing.assert_array_equal(
            expected, [True, True, False, False, False, False]
        )
        assert rows(page, "umap-count-cells")[0]["count"] == expected.sum()
        summary = rows(page, names["selected-expression"])
        assert sum((row["cells"] for row in summary)) == expected.sum()

    @pytest.mark.parametrize("gene_controls", [False, True])
    def test_multiple_histograms_and_optional_gene_controls_keep_the_shared_brush(
        self, page, adata, gene_controls
    ):
        adata.X[:, 1] = [-2, -1, 0, 1, 2, 3]
        chart = (
            gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
            .add_heatmap(gene_controls=gene_controls, show_values=True, vmin=-3, vmax=3)
            .add_histogram(
                ["HLA-DRA", "missing.gene"], gene_controls=gene_controls, height=80
            )
            .to_chart()
        )
        names = render_summary(page, chart)
        intervals = {"x": [-1, 1.5], "y": [-1, 0.5]}
        assert [e.text for e in svg_root(page).iter()].count("Distribution") == 1
        set_brush(page, intervals)
        assert sum((r["count"] for r in rows(page, "all-expression-histogram-0"))) == 5
        assert sum((r["count"] for r in rows(page, "all-expression-histogram-1"))) == 6
        assert {
            r["bin_start"] for r in rows(page, "selected-expression-histogram-0")
        } == {-1, 0}
        assert {
            r["bin_start"] for r in rows(page, "selected-expression-histogram-1")
        } == {-2, -1}
        if not gene_controls:
            assert page.locator("select").count() == 0
            assert {
                r["gene"]: r["mean"] for r in rows(page, names["selected-expression"])
            } == pytest.approx({"HLA-DRA": -0.5, "missing.gene": -1.5})
            set_brush(page, {"x": None, "y": None})
            for i in range(2):
                assert rows(page, f"selected-expression-histogram-{i}") == []
            return
        page.get_by_label("Histogram gene 1", exact=True).select_option("missing.gene")
        page.get_by_label("Heatmap gene 1", exact=True).select_option("missing.gene")
        page.wait_for_function(
            "api.views.get({scope:[],view:'selected-expression-histogram-0'}).data.read({scope:'all',limit:100}).rows.every(r => r.variable === 'missing.gene')"
        )
        assert {
            r["bin_start"] for r in rows(page, "selected-expression-histogram-0")
        } == {-2, -1}
        assert sum((r["count"] for r in rows(page, "all-expression-histogram-0"))) == 6
        means = rows(page, names["selected-expression"])
        assert len(means) == 1
        assert means[0]["gene"] == "missing.gene"
        assert means[0]["mean"] == pytest.approx(-1.5)
        assert [
            float(e.text.replace("−", "-")) for e in value_texts(svg_root(page))
        ] == [-1.5]
        assert (
            page.evaluate("api.params.get('cells').getValue().intervals") == intervals
        )
        assert rows(page, "umap-count-cells")[0]["count"] == 2
        page.evaluate(
            "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
            names["umap-brush-cells"],
        )
        assert rows(page, names["selected-expression"]) == []
        for i in range(2):
            assert rows(page, f"selected-expression-histogram-{i}") == []
            assert (
                sum((r["count"] for r in rows(page, f"all-expression-histogram-{i}")))
                == 6
            )

    @pytest.mark.parametrize("show_values", [False, True])
    @pytest.mark.xfail(
        strict=True,
        reason="Core 1.2 GPU categorical positions retain removed slots; upstream PR #595 is unreleased",
    )
    def test_heatmap_gene_changes_keep_rows_inside_the_plot(
        self, page, adata, show_values
    ):
        adata.X[:, 1] = [-2, -1, 0, 1, 2, 3]
        chart = (
            gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
            .add_heatmap(gene_controls=True, show_values=show_values, height=160)
            .legend(position="bottom")
            .to_chart()
        )
        names = render_summary(page, chart)
        set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
        bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["selected-expression"],
        )
        for choice in ["HLA-DRA", "missing.gene", "HLA-DRA", "missing.gene"]:
            page.get_by_label("Heatmap gene 1", exact=True).select_option(choice)
            page.evaluate("() => new Promise(requestAnimationFrame)")
            expected = {"missing.gene", choice}
            actual = rows(page, names["selected-expression"])
            assert len(actual) == 2 * len(expected)
            assert {row["gene"] for row in actual} == expected
            root = svg_root(page)
            rectangles = [
                element
                for group in root.iter()
                if group.get("data-name") == names["selected-expression"]
                for element in group.iter()
                if element.tag.endswith("rect")
            ]
            assert len(rectangles) == len(actual)
            image = Image.open(
                BytesIO(page.locator("canvas").first.screenshot())
            ).convert("RGB")
            for rect in rectangles:
                assert float(rect.get("y")) >= bounds["y"] - 0.25
                assert (
                    float(rect.get("y")) + float(rect.get("height"))
                    <= bounds["y"] + bounds["height"] + 0.25
                )
                x = float(rect.get("x")) + float(rect.get("width")) * 0.25
                y = float(rect.get("y")) + float(rect.get("height")) * 0.25
                np.testing.assert_allclose(
                    image.getpixel((int(x), int(y))),
                    ImageColor.getrgb(rect.get("fill")),
                    atol=2,
                )


class TestEmbeddingSummaryTracks:
    """Observe linked cell identity, native track opacity and independent navigation."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("page", [1, 1.5], indirect=True)
    def test_brush_dims_tracks_by_cell_identity_and_survives_zoom_and_clear(
        self, page, adata
    ):
        adata.X[:, 1] = [1, 2, 3, 4, 5, 6]
        chart = (
            gsc.pl.EmbeddingSummary(
                adata,
                ["HLA-DRA", "missing.gene"],
                "type",
                categories_order=["B", "A"],
                palette={"A": "#1f77b4", "B": "#ff7f0e"},
            )
            .add_tracks(["missing.gene", "HLA-DRA"], width=480, height=180, group_gap=4)
            .style(umap_size=240)
            .to_chart()
        )
        names = render_summary(page, chart)
        reference = rows(page, "tracks-all-0")
        assert [row["_obs_id"] for row in reference] == [
            f"cell-{i}" for i in (2, 3, 4, 0, 1, 5)
        ]
        assert [row["_cell"] for row in reference] == list(range(6))
        assert rows(page, "tracks-selected-0") == reference
        points = rows(page, "umap-points")
        intervals = {"x": [-0.5, 1.5], "y": [-0.5, 0.5]}
        set_brush(page, intervals)
        for slot in (0, 1):
            assert {
                row["_obs_id"] for row in rows(page, f"tracks-selected-{slot}")
            } == {"cell-0", "cell-1"}
        assert rows(page, "umap-count-cells")[0]["count"] == 2
        assert rows(page, "tracks-all-0") == reference
        assert rows(page, "umap-points") == points
        root = svg_root(page)
        rectangles = next(
            (group for group in root.iter() if group.get("data-name") == "tracks-all-0")
        )
        rectangles = [
            element for element in rectangles.iter() if element.tag.endswith("rect")
        ]
        assert len(rectangles) == 6
        image = Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
            "RGB"
        )
        dpr = page.evaluate("devicePixelRatio")
        for row, rect in zip(reference, rectangles, strict=True):
            x = float(rect.get("x")) + float(rect.get("width")) * 0.25
            y = float(rect.get("y")) + float(rect.get("height")) * 0.25
            color = np.array([31, 119, 180] if row["_group"] == "A" else [255, 127, 14])
            if row["_obs_id"] not in ("cell-0", "cell-1"):
                color = color * 0.15 + 255 * 0.85
            np.testing.assert_allclose(
                image.getpixel((int(x * dpr), int(y * dpr))), color, atol=2
            )
        selected = rows(page, "tracks-selected-0")
        probe = rectangles[3]
        hover_at(page, float(probe.get("x")) + 20, float(probe.get("y")) + 5)
        assert "cell-0" in page.locator("table.attributes").inner_text()
        assert (
            "missing.gene expression" in page.locator("table.attributes").inner_text()
        )
        track = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'tracks-all-0'})"
        )
        canvas = page.locator("canvas").first.bounding_box()
        scale = "api.debug.getViewRoot().getDescendants().find(v => v.spec.name === 'tracks-all-0').getScaleResolution('x')"
        before = page.evaluate(f"{scale}.getDomain()")
        embedding_bounds = page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-brush-cells"],
        )
        page.mouse.move(
            canvas["x"] + track["x"] + track["width"] / 2, canvas["y"] + track["y"] + 30
        )
        page.mouse.wheel(0, -350)
        page.wait_for_function(
            f"() => {{ const d={scale}.getDomain(); return d[1]-d[0] < {np.ptp(before)} * .9; }}"
        )
        assert rows(page, "tracks-selected-0") == selected
        assert rows(page, "tracks-all-0") == reference
        assert (
            page.evaluate("api.params.get('cells').getValue().intervals") == intervals
        )
        assert page.evaluate(
            "name => {\n        const views=api.debug.getViewRoot().getDescendants();\n        const tracks=views.filter(v=>v.spec.name?.startsWith('tracks-'));\n        const strip=views.find(v=>v.spec.name===name);\n        return {count:tracks.length, shared:tracks.every(v=>v.getScaleResolution('x')===strip.getScaleResolution('x'))};\n    }",
            names["heatmap-category-strip"],
        ) == {"count": 4, "shared": True}
        assert (
            page.evaluate(
                "name => api.views.getLayoutBounds({scope:[],view:name})",
                names["umap-brush-cells"],
            )
            == embedding_bounds
        )
        set_brush(page, {"x": [20, 21], "y": [20, 21]})
        assert rows(page, "tracks-selected-0") == []
        assert rows(page, "tracks-all-0") == reference
        set_brush(page, {"x": None, "y": None})
        assert rows(page, "tracks-selected-0") == reference

    @pytest.mark.parametrize("show_count", [False, True])
    def test_embedding_zoom_pan_and_shift_brush_keep_linked_cells(
        self, page, adata, show_count
    ):
        chart = (
            gsc.pl.EmbeddingSummary(
                adata, "HLA-DRA", "type", zoom=True, show_count=show_count
            )
            .add_tracks(width=320, height=100)
            .add_histogram(width=180, height=100)
            .style(umap_size=240)
            .to_chart()
        )
        names = render_summary(page, chart)
        bounds = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'umap-points'})"
        )
        canvas = page.locator("canvas").first.bounding_box()
        page.evaluate(
            "() => {\n        window.embedding = api.debug.getViewRoot().getDescendants()\n            .find(v => v.spec.name === 'umap-points');\n        window.domains = () => ['x','y'].map(c => embedding.getScaleResolution(c).getDomain());\n    }"
        )
        original = rows(page, "umap-points")
        track_scale = "api.debug.getViewRoot().getDescendants().find(v => v.spec.name === 'tracks-all-0').getScaleResolution('x')"
        track_domain = page.evaluate(f"{track_scale}.getDomain()")

        def pointer(x, y):
            position = (
                canvas["x"] + bounds["x"] + x * bounds["width"],
                canvas["y"] + bounds["y"] + y * bounds["height"],
            )
            page.mouse.move(*position)
            return position

        def select(x, y, x2, y2):
            pointer(x, y)
            page.keyboard.down("Shift")
            page.mouse.down()
            pointer(x2, y2)
            page.mouse.up()
            page.keyboard.up("Shift")
            snapshot = page.evaluate("api.params.get('cells').getValue()")
            mask = gsc.selection_mask(adata, snapshot)
            assert 0 < mask.sum() < len(adata)
            valid = mask & np.isfinite(adata.X[:, 0])
            assert {row["_obs_id"] for row in rows(page, "tracks-selected-0")} == set(
                adata.obs_names[valid]
            )
            assert (
                sum(
                    (
                        row["count"]
                        for row in rows(page, "selected-expression-histogram")
                    )
                )
                == valid.sum()
            )
            if show_count:
                assert rows(page, "umap-count-cells")[0]["count"] == mask.sum()
            return snapshot

        before = page.evaluate("domains()")
        selection = select(0.1, 0.3, 0.45, 0.8)
        assert page.evaluate("domains()") == before
        selected = rows(page, "tracks-selected-0")
        pointer(0.85, 0.15)
        page.mouse.wheel(0, -350)
        page.wait_for_function(
            "before => domains().every((d,i) => d[1]-d[0] < before[i][1]-before[i][0])",
            arg=before,
        )
        page.wait_for_timeout(300)
        zoomed = page.evaluate("domains()")
        assert np.ptp(zoomed[0]) == pytest.approx(np.ptp(zoomed[1]))
        assert page.evaluate("api.params.get('cells').getValue()") == selection
        assert rows(page, "tracks-selected-0") == selected
        assert page.evaluate(f"{track_scale}.getDomain()") == track_domain
        pointer(0.85, 0.1)
        page.mouse.down()
        pointer(0.9, 0.15)
        page.mouse.up()
        page.wait_for_function(
            "before => domains().every((d,i) => Math.abs(d[0]-before[i][0]) > 0.01)",
            arg=zoomed,
        )
        panned = page.evaluate("domains()")
        assert np.ptp(panned[0]) == pytest.approx(np.ptp(panned[1]))
        assert page.evaluate("api.params.get('cells').getValue()") == selection
        assert rows(page, "tracks-selected-0") == selected
        assert rows(page, "umap-points") == original
        page.mouse.dblclick(*pointer(0.85, 0.85))
        assert page.evaluate("api.params.get('cells').getValue().intervals.x") is None
        select(0.1, 0.1, 0.8, 0.8)
        assert page.evaluate(f"{track_scale}.getDomain()") == track_domain
        assert (
            page.evaluate(
                "name => api.views.getLayoutBounds({scope:[],view:name})",
                names["umap-points"],
            )
            == bounds
        )
