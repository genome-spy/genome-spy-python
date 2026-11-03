"""Check notebook container sizing against the packaged GenomeSpy runtime."""

import json
from urllib.parse import quote

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.parametrize(
    ("fixed_height", "layout_height", "parent_height", "expected"),
    [
        (None, None, None, 760),
        (240, None, None, 260),
        (None, 400, None, 400),
        (None, None, 400, 400),
    ],
)
def test_widget_height_respects_chart_and_layout_sizes(
    fixed_height, layout_height, parent_height, expected
):
    chart = (
        gs.Chart([{"x": 1, "y": 2}])
        .mark_point()
        .encode(x=gs.X("x:Q").axis(None), y=gs.Y("y:Q").axis(None))
    )
    if fixed_height is not None:
        chart = chart.properties(height=fixed_height)
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
            page.set_content('<div id="widget" style="width: 800px"></div>')
            if parent_height is not None:
                page.locator("#widget").evaluate(
                    """(el, height) => {
                        const parent = document.createElement('div');
                        parent.style.cssText = `display: flex; height: ${height}px`;
                        el.before(parent);
                        parent.append(el);
                    }""",
                    parent_height,
                )
            page.add_style_tag(content=str(widget._css))
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
                window.rendered = true;
                """,
            )
            page.wait_for_function("window.rendered")
            page.wait_for_function(
                "height => document.querySelector('canvas').height === height",
                arg=expected,
            )
            assert page.locator("#widget").bounding_box()["height"] == expected
            if parent_height is not None:
                assert (
                    page.locator("#widget").evaluate(
                        "el => el.parentElement.getBoundingClientRect().height"
                    )
                    == parent_height
                )
            assert page.locator(".message-box").count() == 0
        finally:
            browser.close()


def test_widget_uses_real_jupyter_hbox_height(tmp_path, monkeypatch):
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
    source = tmp_path / "hbox.ipynb"
    source.write_text(nbformat.writes(notebook))
    check_canvas = check_notebook_rendering._check_canvas

    def check_hbox(page, canvas, *args):
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
