"""Check documentation chart loading and theme behavior in the browser."""

import importlib
import io
from pathlib import Path

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")
ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("width", [1200, 430])
def test_docs_charts_load_nearby_and_render_again_after_scrolling(monkeypatch, width):
    """A long page must not retain every canvas or leave returning charts blank."""
    from PIL import Image

    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    extension = importlib.import_module("genomespy_gallery")
    spec = (
        gs.Chart([{"x": 1, "y": 1}])
        .mark_point(size=500, color="#d61f1f")
        .encode(x="x:Q", y="y:Q")
        .properties(width=200, height=120)
        .to_dict()
    )
    markup = (
        "<style>body{margin:0}.gs-doc-embed{margin-bottom:600px}</style>"
        + "".join(
            extension._tutorial_embed_html(
                str(i),
                spec,
                bundle_url="/core.js",
                height=240,
                title=f"Chart {i}",
                identity=str(i),
            )
            for i in range(12)
        )
    )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch(args=["--max-active-webgl-contexts=4"])
        try:
            page = browser.new_page(viewport={"width": width, "height": 640})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on(
                "console",
                lambda m: errors.append(m.text) if m.type == "error" else None,
            )
            page.route(
                "http://docs.test/core.js",
                lambda r: r.fulfill(
                    content_type="text/javascript",
                    body=(ROOT / "src/genome_spy/static/genome-spy.js").read_bytes(),
                ),
            )
            page.route(
                "http://docs.test/",
                lambda r: r.fulfill(content_type="text/html", body=markup),
            )
            page.goto("http://docs.test/")
            hosts = page.locator(".gs-doc-embed")
            hosts.first.locator("canvas").wait_for()
            assert hosts.last.locator("canvas").count() == 0
            initial_height = hosts.first.bounding_box()["height"]
            first_canvas = hosts.first.locator("canvas").element_handle()
            for index in [*range(12), 0]:
                host = hosts.nth(index)
                host.scroll_into_view_if_needed()
                host.locator("canvas").wait_for()
                page.wait_for_function(
                    "document.querySelectorAll('canvas').length <= 2"
                )
                assert host.locator("canvas").evaluate(
                    "c => !c.getContext('webgl2').isContextLost()"
                )
                if index == 2:
                    assert first_canvas.evaluate(
                        "c => c.getContext('webgl2').isContextLost()"
                    )
                image = Image.open(
                    io.BytesIO(host.locator("canvas").screenshot())
                ).convert("RGB")
                assert (
                    sum(
                        count
                        for count, (r, g, b) in image.getcolors(
                            image.width * image.height
                        )
                        if r > 150 and g < 100 and b < 100
                    )
                    > 30
                )
            assert hosts.first.bounding_box()["height"] == initial_height
            assert not errors
        finally:
            browser.close()


@pytest.mark.parametrize("cleanup_error", [False, True])
def test_docs_pending_load_is_disposed_with_its_controls(monkeypatch, cleanup_error):
    """Scroll changes during async loading must use the latest visibility state."""
    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    extension = importlib.import_module("genomespy_gallery")
    markup = extension._tutorial_embed_html(
        "pending",
        {},
        bundle_url="/core.js",
        height=240,
        title="Pending chart",
        identity="pending",
        controls=("png",),
        control_definitions={"png": {"module": "core", "export": "pngButton"}},
        control_module_urls={"core": "/controls.js"},
    )
    assets = {
        "/": (
            "text/html",
            "<script>window.events=[];</script>"
            + markup
            + '<div style="height:3000px"></div>',
        ),
        "/core.js": (
            "text/javascript",
            """
            export async function embed(c, spec) {
                if (spec.used) throw new Error('Reused a mutated specification');
                spec.used = true;
                events.push('start');
                await new Promise(resolve => window.finishEmbed = resolve);
                c.appendChild(document.createElement('canvas'));
                return {finalize() { events.push('finalize'); c.replaceChildren(); }};
            }
        """,
        ),
        "/controls.js": (
            "text/javascript",
            """
            await new Promise(resolve => window.finishControls = resolve);
            export const pngButton = () => ({});
            export function attachControls(c) {
                events.push('controls');
                const button = c.appendChild(document.createElement('button'));
                return {dispose() {events.push('dispose controls'); button.remove();}};
            }
        """,
        ),
    }
    if cleanup_error:
        mime, source = assets["/controls.js"]
        assets["/controls.js"] = (
            mime,
            source.replace(
                "button.remove();",
                "button.remove(); throw new Error('Control cleanup failed');",
            ),
        )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 430, "height": 640})
            errors = []
            page.on(
                "console",
                lambda m: errors.append(m.text) if m.type == "error" else None,
            )
            page.route(
                "http://docs.test/**",
                lambda r: r.fulfill(
                    content_type=assets[r.request.url.removeprefix("http://docs.test")][
                        0
                    ],
                    body=assets[r.request.url.removeprefix("http://docs.test")][1],
                ),
            )
            page.goto("http://docs.test/", wait_until="domcontentloaded")
            page.wait_for_function("typeof window.finishEmbed === 'function'")
            page.evaluate("finishEmbed()")
            page.wait_for_function("typeof window.finishControls === 'function'")
            page.evaluate("window.scrollTo(0, 2000)")
            page.wait_for_function(
                "document.querySelector('.gs-doc-embed').getBoundingClientRect().bottom < -300"
            )
            # Wait for the observer before resolving the slow controls import.
            page.wait_for_timeout(100)
            page.evaluate("finishControls()")
            page.wait_for_function("events.includes('finalize')")
            assert page.evaluate("events") == [
                "start",
                "controls",
                "dispose controls",
                "finalize",
            ]
            assert page.locator("canvas, button").count() == 0
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_function("events.filter(e => e === 'start').length === 2")
            page.evaluate("finishEmbed()")
            page.locator("button").wait_for(state="attached")
            assert page.locator("canvas, button").count() == 2
            assert page.evaluate("events.filter(e => e === 'finalize').length") == 1
            assert len(errors) == int(cleanup_error)
            if cleanup_error:
                assert "Control cleanup failed" in errors[0]
        finally:
            browser.close()


@pytest.mark.parametrize("system_theme", ["light", "dark"])
def test_chart_text_follows_selected_docs_theme(
    system_theme: str, tmp_path: Path
) -> None:
    chart = (
        gs.Chart([{}])
        .mark_text(text="Readable chart labels", size=30)
        .encode(x=gs.value(0.5), y=gs.value(0.5))
        .properties(width=400, height=100)
    )
    css = (ROOT / "docs" / "_static" / "genomespy.css").read_text()
    html = chart.to_html(
        inline=True, controls=False, embed_options={"renderer": "canvas"}
    )
    output = tmp_path / "theme.html"
    output.write_text(
        "<!doctype html><html><head><style>:root {color-scheme: light dark;}"
        + css
        + '</style></head><body data-theme="light">'
        + "".join(
            f"<button onclick=\"document.body.dataset.theme='{theme}'\">{theme}</button>"
            for theme in ("light", "dark", "auto")
        )
        + '<div class="gs-doc-embed">'
        + html
        + "</div></body></html>"
    )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(offline=True, color_scheme=system_theme)
            page.goto(output.as_uri())
            for theme in ("light", "dark", "auto", "light"):
                page.get_by_role("button", name=theme, exact=True).click()
                dark = theme == "dark" or (theme == "auto" and system_theme == "dark")
                assert page.locator(".gs-doc-embed").evaluate(
                    "element => getComputedStyle(element).colorScheme"
                ) == ("dark" if dark else "light")
                page.wait_for_function(
                    """dark => {
                        const canvas = document.querySelector('canvas');
                        if (!canvas) return false;
                        const pixels = canvas.getContext('2d')
                            .getImageData(0, 0, canvas.width, canvas.height).data;
                        let contrasting = 0;
                        for (let i = 0; i < pixels.length; i += 4) {
                            if (pixels[i + 3] < 128) continue;
                            const rgb = [pixels[i], pixels[i + 1], pixels[i + 2]];
                            if (dark ? Math.min(...rgb) > 200 : Math.max(...rgb) < 50)
                                contrasting++;
                        }
                        return contrasting > 100;
                    }""",
                    arg=dark,
                )
        finally:
            browser.close()
