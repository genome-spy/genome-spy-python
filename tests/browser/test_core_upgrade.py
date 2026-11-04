"""Exercise the new grammar through the bundled, offline browser runtime."""

from pathlib import Path

import genome_spy as gs
import pytest

playwright = pytest.importorskip("playwright.sync_api")


def test_core_1_3_branch_publishes_values_and_preserves_main_rows() -> None:
    from genome_spy._embed import bundled_module_url

    chart = (
        gs.Chart([{"x": 2}, {"x": 1}, {"x": 2}])
        .mark_point()
        .encode(x=gs.X("x:Q").axis(None))
        .properties(name="source")
        .transform_branch(
            transform=[gs.ValuesParams(type="values", field="x", param="observed")]
        )
    )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(offline=True)
            page.set_content('<div id="chart"></div>')
            page.evaluate(
                """async args => {
                    const {embed} = await import(args.url);
                    window.api = await embed(document.querySelector('#chart'), args.spec);
                }""",
                {"url": bundled_module_url("embed"), "spec": chart.to_dict()},
            )
            assert page.evaluate("api.params.get('observed').getValue()") == [2, 1, 2]
            rows = page.evaluate(
                "api.views.get({scope:[],view:'source'}).data.read({scope:'all', limit:10}).rows"
            )
            assert [row["x"] for row in rows] == [2, 1, 2]
        finally:
            browser.close()


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
    chart = chart.configure_point(color="#4c78a8").configure_link(color="#4c78a8")
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
            page.wait_for_function("""() => {
              const canvas = document.querySelector('canvas');
              const pixels = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
              let colored = 0;
              for (let i = 0; i < pixels.length; i += 4) {
                if (Math.abs(pixels[i] - 76) <= 3 && Math.abs(pixels[i + 1] - 120) <= 3 &&
                    Math.abs(pixels[i + 2] - 168) <= 3 && pixels[i + 3] > 20) colored++;
              }
              return colored > 10;
            }""")
            assert page.locator(".message-box").count() == 0
            assert not errors, errors
            assert page.locator("canvas").first.evaluate(
                "canvas => canvas.width > 0 && canvas.height > 0"
            )
        finally:
            browser.close()


def test_shared_point_hover_survives_panel_transitions_and_clears():
    from genome_spy._embed import bundled_module_url

    hovered = gs.selection_point(
        "cellHover",
        on="pointerover",
        clear="mouseleave",
        toggle=False,
        persist=False,
        empty=False,
    )
    points = (
        gs.Chart()
        .transform_project(fields=["cell", "x", "y", "__uniqueId"])
        .mark_point(filled=True, size=100)
        .encode(
            x=gs.X("x:Q").scale(domain=[0, 2]),
            y=gs.Y("y:Q").scale(domain=[0, 2]),
            key=gs.Key("cell"),
            strokeWidth=gs.when(hovered).then(gs.value(2)).otherwise(gs.value(0)),
        )
        .properties(width=200, height=200)
        .add_params(hovered.copy(push="outer"))
    )
    chart = (
        gs.hconcat(points.properties(name="left"), points.properties(name="right"))
        .properties(data=[{"cell": "A", "x": 1, "y": 1}])
        .transform_identifier()
        .add_params(gs.param("cellHover", value=None))
    )
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.set_content('<div id="chart"></div>')
            page.evaluate(
                """async args => {
                const {embed} = await import(args.url);
                window.api = await embed(document.querySelector('#chart'), args.spec);
            }""",
                {"url": bundled_module_url("embed"), "spec": chart.to_dict()},
            )
            page.locator(".canvas-wrapper.loading").wait_for(state="hidden")
            page.wait_for_function("""() => {
                const canvas = document.querySelector('canvas');
                return Math.abs(canvas.getBoundingClientRect().width - canvas.clientWidth) < 0.1;
            }""")
            canvas = page.locator("canvas").bounding_box()
            for name in ("left", "right", "left"):
                bounds = page.evaluate(
                    "name => api.views.getLayoutBounds({scope:[],view:name})", name
                )
                page.mouse.move(
                    canvas["x"] + bounds["x"] + 100, canvas["y"] + bounds["y"] + 100
                )
                page.wait_for_timeout(100)
                assert not errors, errors
                assert (
                    page.evaluate("api.params.get('cellHover').getValue().datum?.cell")
                    == "A"
                ), name
            page.mouse.move(0, 0)
            page.wait_for_timeout(100)
            assert not errors, errors
            assert page.evaluate("api.params.get('cellHover').getValue().datum") is None
        finally:
            browser.close()
