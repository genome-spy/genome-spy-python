"""Exercise the shipped inline modules in the browser CI environment."""

import json
from pathlib import Path

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


def test_inline_html_renders_and_opens_inspector_offline(tmp_path: Path) -> None:
    chart = (
        gs.Chart([{"x": 1, "y": 2}, {"x": 2, "y": 3}])
        .mark_point()
        .encode(x="x:Q", y="y:Q")
    )
    output = tmp_path / "chart.html"
    chart.save(output, inline=True)
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(offline=True)
            errors: list[str] = []
            requests: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on(
                "request",
                lambda request: (
                    requests.append(request.url)
                    if request.url.startswith(("http:", "https:"))
                    else None
                ),
            )
            # A host AMD loader must not intercept the packaged ESM runtime.
            page.add_init_script(
                "globalThis.define = () => { throw Error('AMD called'); };"
                "globalThis.define.amd = {};"
            )
            page.goto(output.as_uri())
            page.locator("canvas").first.wait_for(state="visible")
            inspector = page.get_by_role("button", name="Inspector", exact=True)
            inspector.wait_for(state="attached")
            inspector.evaluate("(button) => button.click()")
            page.get_by_role("dialog", name="GenomeSpy Inspector").wait_for(
                state="visible"
            )
            page.locator("gs-inspector-panel").wait_for(state="attached")
            assert page.locator(".message-box").count() == 0
            assert not errors, errors
            assert not requests, requests
        finally:
            browser.close()


@pytest.mark.parametrize("painted", [False, True])
def test_notebook_canvas_check_keeps_blank_failure_and_records_state(tmp_path, painted):
    from tools.check_notebook_rendering import _check_canvas, _observe_rendering

    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page()
            console = []
            _observe_rendering(page, console)
            page.goto("""data:text/html,<div class="jp-CodeCell">
                <div class="jp-InputArea">chart.display()</div>
                <div class="jp-OutputArea"><canvas width="100" height="80"></canvas></div>
                </div>""")
            canvas = page.locator("canvas")
            canvas.evaluate(
                """(canvas, painted) => {
                canvas.dispatchEvent(new WebGLContextEvent('webglcontextlost'));
                console.warn('test-secret');
                const ctx = canvas.getContext('2d');
                const fill = ctx.createLinearGradient(0, 0, 100, 0);
                fill.addColorStop(0, 'red'); fill.addColorStop(1, 'blue');
                ctx.fillStyle = painted ? fill : 'white';
                ctx.fillRect(0, 0, 100, 80);
            }""",
                painted,
            )
            screenshot = tmp_path / "chart.png"
            if painted:
                _check_canvas(page, canvas, screenshot, console, [], "test-secret")
                assert not screenshot.with_suffix(".json").exists()
            else:
                with pytest.raises(AssertionError, match="canvas is blank"):
                    _check_canvas(page, canvas, screenshot, console, [], "test-secret")
                report = screenshot.with_suffix(".json").read_text()
                assert "test-secret" not in report
                state = json.loads(report)
                assert state["cellIndex"] == 0
                assert state["source"] == "chart.display()"
                assert state["canvas"]["bufferWidth"] == 100
                assert state["colorCount"] == 1
                assert state["contextEvents"][0]["type"] == "webglcontextlost"
                assert state["console"] == [{"type": "warning", "text": "<redacted>"}]
                assert screenshot.with_suffix(".page.png").is_file()
            assert screenshot.is_file()
        finally:
            browser.close()
