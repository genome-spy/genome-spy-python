"""Keep chart defaults aligned with the documentation theme selector."""

from pathlib import Path

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")
ROOT = Path(__file__).resolve().parents[2]


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
