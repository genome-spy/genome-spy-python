"""Check notebook container sizing against the packaged GenomeSpy runtime."""

import json
from urllib.parse import quote

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.parametrize(
    ("fixed_height", "layout_height", "expected"),
    [(None, None, 760), (240, None, 260), (None, 400, 400)],
)
def test_widget_height_respects_chart_and_layout_sizes(
    fixed_height, layout_height, expected
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
            assert page.locator(".message-box").count() == 0
        finally:
            browser.close()
