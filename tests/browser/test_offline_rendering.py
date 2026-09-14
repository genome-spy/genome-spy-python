"""Exercise the shipped inline modules in the browser CI environment."""

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
