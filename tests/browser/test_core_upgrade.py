"""Exercise the new grammar through the bundled, offline browser runtime."""

from pathlib import Path

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.parametrize("kind", ["facet", "surround", "dendrogram"])
def test_core_1_2_grammar_renders_offline(kind: str, tmp_path: Path) -> None:
    from docs.tutorials.composition import facet_chart, surround_chart

    if kind == "facet":
        chart = facet_chart
    elif kind == "surround":
        chart = surround_chart
    else:
        chart = (
            gs.Chart(
                [
                    {"id": "a", "parent": "root", "height": 0, "index": 0},
                    {"id": "b", "parent": "root", "height": 0, "index": 1},
                    {"id": "root", "parent": None, "height": 1, "index": None},
                ]
            )
            .transform_dendrogram(
                height="height", key="id", parentKey="parent", leafIndex="index"
            )
            .mark_link(linkShape="orthogonal", orient="horizontal")
            .encode(
                x="sourceHeight:Q",
                x2="targetHeight",
                y=gs.Y("sourceIndex:I").scale(domain=[-0.5, 1.5]),
                y2="targetIndex",
                yOffset=gs.YOffset("sourceOffset:Q").scale(
                    domain=[-0.5, 0.5], range=[-12, 12]
                ),
                y2Offset=gs.Y2Offset(field="targetOffset"),
            )
        )
    output = tmp_path / f"{kind}.html"
    chart.save(
        output, inline=True, controls=False, embed_options={"renderer": "canvas"}
    )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(offline=True)
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on(
                "console",
                lambda message: (
                    errors.append(message.text) if message.type == "error" else None
                ),
            )
            page.goto(output.as_uri())
            page.locator("canvas").first.wait_for(state="visible")
            page.locator(".canvas-wrapper.loading").wait_for(state="hidden")
            page.get_by_text("Loading...", exact=True).wait_for(state="hidden")
            assert page.locator(".message-box").count() == 0
            assert not errors, errors
            assert page.locator("canvas").first.evaluate(
                "canvas => canvas.width > 0 && canvas.height > 0"
            )
        finally:
            browser.close()
