"""Check notebook container sizing against the packaged GenomeSpy runtime."""

import json
from pathlib import Path
from urllib.parse import quote

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.parametrize(
    (
        "kind",
        "width",
        "height",
        "host_width",
        "host_height",
        "layout_height",
        "expected",
    ),
    [
        ("unit", None, None, 500, None, None, None),
        ("unit", 200, 120, 800, None, None, [220, 140]),
        ("unit", None, 240, 800, None, None, [800, 260]),
        ("step", None, None, 500, None, None, [500, 80]),
        ("vconcat", None, None, 500, None, None, [500, 330]),
        ("unit", None, None, 500, 350, None, [500, 350]),
        ("unit", None, None, 900, 600, None, [900, 600]),
        ("unit", None, None, 800, None, 400, [800, 400]),
    ],
)
def test_widget_uses_native_plot_and_container_dimensions(
    kind, width, height, host_width, host_height, layout_height, expected
):
    chart = (
        gs.Chart([{"x": i, "y": i} for i in range(3)])
        .mark_point()
        .encode(x=gs.X("x:Q").axis(None), y=gs.Y("y:Q").axis(None))
    )
    if kind == "step":
        chart = chart.encode(
            y=gs.Y("y:O").scale(paddingInner=0, paddingOuter=0).axis(None)
        ).properties(height=gs.step(20))
    elif kind == "vconcat":
        chart = gs.vconcat(
            chart.properties(height=100), chart.properties(height=200), spacing=10
        )
    else:
        if width is not None:
            chart = chart.properties(width=width)
        if height is not None:
            chart = chart.properties(height=height)
    widget = chart.widget(inline=True, controls=False)
    state = {
        name: getattr(widget, name)
        for name in (
            "spec",
            "bundle_url",
            "embed_options",
            "controls",
            "dataset_manifest",
        )
    }
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page()
            page.set_content(f'<div id="widget" style="width: {host_width}px"></div>')
            if host_height is not None:
                page.locator("#widget").evaluate(
                    """(el, height) => {
                        const parent = document.createElement('div');
                        parent.style.cssText = `display: flex; height: ${height}px`;
                        el.before(parent);
                        parent.append(el);
                    }""",
                    host_height,
                )
            if css := getattr(widget, "_css", ""):
                page.add_style_tag(content=str(css))
            if layout_height is not None:
                page.locator("#widget").evaluate(
                    "(el, height) => el.style.height = `${height}px`", layout_height
                )
            page.add_script_tag(
                type="module",
                content=f"""
                const {{renderChart}} = await import({json.dumps("data:text/javascript," + quote(str(widget._esm)))});
                const values = {json.dumps(state)};
                const model = {{get: name => values[name], set() {{}},
                    save_changes() {{}}, on() {{}}, off() {{}}}};
                window.controller = new AbortController();
                await renderChart({{model, el: document.querySelector('#widget'),
                    signal: controller.signal}});
                if ({json.dumps(expected is None)}) {{
                    const reference = document.createElement('div');
                    reference.style.width = '{host_width}px';
                    document.body.append(reference);
                    const core = await import(values.bundle_url);
                    await core.embed(reference, structuredClone(values.spec), values.embed_options);
                    const canvas = reference.querySelector('canvas');
                    window.nativeSize = [canvas.width, canvas.height];
                }}
                window.rendered = true;
                """,
            )
            page.wait_for_function("window.rendered")
            if expected is None:
                expected = page.evaluate("window.nativeSize")
            page.wait_for_function(
                """size => {
                    const canvas = document.querySelector('canvas');
                    return canvas.width === size[0] && canvas.height === size[1];
                }""",
                arg=expected,
            )
            assert page.locator("#widget").bounding_box()["width"] == host_width
            assert page.locator("#widget").bounding_box()["height"] == expected[1]
            if host_height is not None:
                assert (
                    page.locator("#widget").evaluate(
                        "el => el.parentElement.getBoundingClientRect().height"
                    )
                    == host_height
                )
            assert page.locator(".message-box").count() == 0
        finally:
            browser.close()


@pytest.mark.parametrize("plot", ["hbox", "clustered_heatmap"])
def test_widget_dimensions_in_real_jupyter(tmp_path, monkeypatch, plot):
    import sys

    import nbformat

    from tools import check_notebook_rendering

    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell("""import genome_spy as gs
from ipywidgets import HBox, Layout

chart = gs.Chart([
    {"x": x, "y": y, "value": x + 10 * y}
    for x in range(10) for y in range(10)
]).mark_rect().encode(
    x=gs.X("x:O").axis(None), y=gs.Y("y:O").axis(None), color="value:Q"
)
widget = chart.widget(inline=True, controls=False)
display(HBox([widget], layout=Layout(height="400px")))
""")
        ],
        metadata={
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3",
                "language": "python",
            }
        },
    )
    if plot == "clustered_heatmap":
        example = (
            Path(__file__).resolve().parents[2] / "docs/examples/clustered_heatmap.py"
        )
        notebook.cells[0].source = f"""import runpy
chart = runpy.run_path({str(example)!r})["chart"]
widget = chart.widget(inline=True, controls=False)
widget.layout.width = "900px"
display(widget)
"""
    source = tmp_path / "hbox.ipynb"
    source.write_text(nbformat.writes(notebook))
    check_canvas = check_notebook_rendering._check_canvas

    def check_hbox(page, canvas, *args):
        if plot == "clustered_heatmap":
            initial_height = canvas.evaluate("el => el.height")
            assert initial_height > 480 + 96
            assert canvas.evaluate("el => el.width") == 900
            bounds = canvas.bounding_box()
            page.mouse.move(
                bounds["x"] + bounds["width"] * 0.55,
                bounds["y"] + bounds["height"] * 0.5,
            )
            page.mouse.wheel(0, -180)
            page.wait_for_timeout(500)
            assert canvas.evaluate("el => el.height") == initial_height
            check_notebook_rendering._run_kernel(page, 'widget.layout.width = "600px"')
            page.wait_for_function("document.querySelector('canvas').width === 600")
            assert canvas.evaluate("el => el.height") > 480 + 96
            assert (
                abs(
                    canvas.evaluate("""el => el.height -
                el.closest('.genome-spy').getBoundingClientRect().height""")
                )
                < 1
            )
            check_canvas(page, canvas, *args)
            return
        heights = canvas.evaluate("""canvas => {
            const widget = canvas.closest('.genome-spy');
            const parent = widget.closest('.widget-hbox');
            return [parent.getBoundingClientRect().height,
                widget.getBoundingClientRect().height, canvas.height];
        }""")
        assert heights == [400, 400, 400]
        check_canvas(page, canvas, *args)

    monkeypatch.setattr(check_notebook_rendering, "_check_canvas", check_hbox)
    monkeypatch.setattr(
        sys, "argv", ["check", str(source), "--screenshot", str(tmp_path / "hbox.png")]
    )
    check_notebook_rendering.main()
