"""Keep documentation surround plots readable and stationary."""

import json
from pathlib import Path

import pytest

playwright = pytest.importorskip("playwright.sync_api")
ROOT = Path(__file__).resolve().parents[2]


def test_facet_headings_share_one_line(tmp_path: Path) -> None:
    from docs.tutorials.composition import facet_chart

    markup = """<div id="chart" style="width:100%;height:300px"></div>
<script type="module">
import {embed} from '/core.js';
window.api = await embed(document.querySelector('#chart'), SPEC, {bare:true});
</script>""".replace("SPEC", json.dumps(facet_chart.to_dict()))
    bundle = (ROOT / "src/genome_spy/static/genome-spy.js").read_text()
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page()
            page.route(
                "http://composition.test/",
                lambda route: route.fulfill(content_type="text/html", body=markup),
            )
            page.route(
                "http://composition.test/core.js",
                lambda route: route.fulfill(
                    content_type="text/javascript", body=bundle
                ),
            )
            page.goto("http://composition.test/")
            page.wait_for_function("window.api")
            page.locator(".canvas-wrapper.loading").wait_for(state="hidden")
            for loading in page.get_by_text("Loading...", exact=True).all():
                loading.wait_for(state="hidden")
            for width in (700, 1100):
                page.set_viewport_size({"width": width, "height": 450})
                page.wait_for_timeout(200)
                headings = page.evaluate("""() => {
                    const views = api.debug.getViewRoot().getDescendants();
                    const labels = views.find(v => v.spec?.encoding?.text?.field === 'text');
                    const title = views.find(v => v.spec?.mark?.text === 'group');
                    const headings = [...labels.getCollector().getData()].map(d => ({
                        text: d.text,
                        x: labels.coords.x + d.x * labels.coords.width,
                        y: labels.coords.y + (1 - d.y) * labels.coords.height,
                        baseline: labels.spec.mark.baseline,
                    }));
                    headings.push({text: 'group',
                        x: title.coords.x + title.spec.mark.x * title.coords.width,
                        y: title.coords.y + (1 - title.spec.mark.y) * title.coords.height
                            + title.spec.mark.yOffset,
                        baseline: title.spec.mark.baseline,
                    });
                    return headings.sort((a,b) => a.x - b.x);
                }""")
                assert [heading["text"] for heading in headings] == [
                    "control",
                    "group",
                    "treated",
                ]
                assert {heading["baseline"] for heading in headings} == {"middle"}
                assert (
                    max(heading["y"] for heading in headings)
                    - min(heading["y"] for heading in headings)
                    < 1
                )
            page.screenshot(path=str(tmp_path / "facet-headings.png"))
        finally:
            browser.close()


@pytest.mark.parametrize("chart_name", ["surround_chart", "matrix_summary_chart"])
def test_surround_wheel_keeps_plot_and_domains_unchanged(
    chart_name: str, tmp_path: Path
) -> None:
    from docs.tutorials import composition

    spec = getattr(composition, chart_name).to_dict()
    spec["spec"]["name"] = "center"
    spec["surround"]["top"][0]["name"] = "top"
    markup = """<div id="chart" style="width:700px;height:420px"></div>
<script type="module">
import {embed} from '/core.js';
window.api = await embed(document.querySelector('#chart'), SPEC, {bare:true});
</script>""".replace("SPEC", json.dumps(spec))
    bundle = (ROOT / "src/genome_spy/static/genome-spy.js").read_text()
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 900, "height": 600})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route(
                "http://composition.test/",
                lambda route: route.fulfill(content_type="text/html", body=markup),
            )
            page.route(
                "http://composition.test/core.js",
                lambda route: route.fulfill(
                    content_type="text/javascript", body=bundle
                ),
            )
            page.goto("http://composition.test/")
            page.wait_for_function("window.api")
            page.locator(".canvas-wrapper.loading").wait_for(state="hidden")
            for loading in page.get_by_text("Loading...", exact=True).all():
                loading.wait_for(state="hidden")
            page.evaluate("""() => {
                const views = api.debug.getViewRoot().getDescendants();
                window.center = views.find(view => view.spec?.name === 'center');
                window.topView = views.find(view => view.spec?.name === 'top');
                window.bounds = () => api.views.getLayoutBounds({scope: [], view: 'center'});
                window.domain = () => center.getScaleResolution('x').getDomain();
                window.domains = () => views.filter(view => view.mark).map(view => ({
                    x: view.getScaleResolution('x')?.getDomain(),
                    y: view.getScaleResolution('y')?.getDomain(),
                }));
            }""")
            initial = page.evaluate("bounds()")
            assert initial["width"] > 400
            assert initial["height"] > 150
            assert page.evaluate("domain()") == (
                [1, 4] if chart_name == "surround_chart" else [0, 3]
            )
            if chart_name == "surround_chart":
                top = page.evaluate(
                    "api.views.getLayoutBounds({scope: [], view: 'top'})"
                )
                for offset in (-8, 8):
                    hit = page.evaluate(
                        "point => api.views.get({scope: [], view: 'top'}).marks.pick(point)",
                        {
                            "x": top["x"] + top["width"] / 2 + offset,
                            "y": top["y"] + top["height"] * 0.75 + offset,
                        },
                    )
                    assert hit["status"] == "hit"
                    assert hit["hit"]["datum"]["meanSignal"] == pytest.approx(3.15)
            canvas = page.locator("canvas").first.bounding_box()
            assert canvas is not None
            page.mouse.move(
                canvas["x"] + initial["x"] + initial["width"] / 2,
                canvas["y"] + initial["y"] + initial["height"] / 2,
            )
            initial_domains = page.evaluate("domains()")
            for delta in (-250, -250, 250, 250):
                page.mouse.wheel(0, delta)
                page.wait_for_timeout(300)
                assert page.evaluate("domains()") == initial_domains
                current = page.evaluate("bounds()")
                for dimension in ("width", "height"):
                    assert current[dimension] == pytest.approx(
                        initial[dimension], abs=2
                    )
                assert page.evaluate(
                    "center.getScaleResolution('x') === topView.getScaleResolution('x')"
                )
            assert not errors
            assert page.locator(".message-box").count() == 0
            page.screenshot(path=str(tmp_path / f"{chart_name}.png"))
        finally:
            browser.close()


@pytest.mark.parametrize("example", ["pbmc_umap_genes", "pbmc_cell_heatmap"])
def test_gallery_legends_dim_the_same_cells_across_views(example: str) -> None:
    from importlib import import_module

    from genome_spy._embed import bundled_module_url

    chart = import_module(f"docs.examples.{example}").chart
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1100, "height": 1000})
            page.set_content(
                '<style>body{margin:0}</style><div id="chart" style="width:1000px;height:800px"></div>'
            )
            page.evaluate(
                """async ({url,spec}) => {
                    const {embed} = await import(url);
                    window.api = await embed(document.querySelector('#chart'),spec,{bare:true});
                }""",
                {"url": bundled_module_url("embed"), "spec": chart.to_dict()},
            )
            page.locator(".canvas-wrapper.loading").wait_for(state="hidden")
            page.evaluate(
                """async()=>{await document.fonts.ready;await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame)}"""
            )
            page.wait_for_timeout(500)
            entry = page.evaluate("""() => {
                const v=api.debug.getViewRoot().getDescendants().find(v=>v.spec.name==='symbols');
                const d=v.getCollector().getData()[0];
                return {x:v.coords.x+v.mark.encoders.x(d)*v.coords.width,y:v.coords.y+(1-v.mark.encoders.y(d))*v.coords.height,value:d.value};
            }""")
            page.mouse.move(entry["x"], entry["y"])
            page.wait_for_timeout(100)
            page.mouse.click(entry["x"], entry["y"])
            checks = """() => api.debug.getViewRoot().getDescendants()
                .filter(v=>v.spec.encoding?.opacity?.field==='legend_opacity')
                .map(v=>[...v.getCollector().getData()].map(d=>({
                    group:d.cell_type,opacity:d.legend_opacity,counts:d.n_counts,
                })))"""
            page.wait_for_function("""() => api.debug.getViewRoot().getDescendants()
                .filter(v=>v.spec.encoding?.opacity?.field==='legend_opacity')
                .every(v=>[...v.getCollector().getData()].some(d=>d.legend_opacity<.1))""")
            rows = page.evaluate(checks)
            assert len(rows) == (8 if example == "pbmc_umap_genes" else 1)
            for panel in rows:
                bright = [row for row in panel if row["group"] == entry["value"]]
                dim = [row for row in panel if row["group"] != entry["value"]]
                assert bright and dim
                assert min(row["opacity"] for row in bright) >= 0.9
                assert max(row["opacity"] for row in dim) <= 0.08

            # Both controls narrow the selection rather than replacing one another.
            if example == "pbmc_umap_genes":
                page.evaluate("""()=>{api.params.get('counts_range').setValue({
                    type:'interval',intervals:{color:[1000,2000]}})}""")
                expected = "d.n_counts>=1000 && d.n_counts<2000"
            else:
                page.evaluate("""()=>{api.views.get({scope:[],view:'expressionCells'})
                    .params.get('expression_range').setValue({
                    type:'interval',intervals:{color:[1,2]}})}""")
                expected = "d.expression>=1 && d.expression<2"
            page.wait_for_function(
                """group => api.debug.getViewRoot().getDescendants()
                .filter(v=>v.spec.encoding?.opacity?.field==='legend_opacity')
                .every(v=>[...v.getCollector().getData()].every(d=>
                    d.legend_opacity === (d.cell_type===group && (EXPRESSION) ? BRIGHT : DIM)))""".replace(
                    "EXPRESSION", expected
                )
                .replace("BRIGHT", "0.9" if example == "pbmc_umap_genes" else "1")
                .replace("DIM", "0.04" if example == "pbmc_umap_genes" else "0.08"),
                arg=entry["value"],
            )
            assert page.locator(".message-box").count() == 0
        finally:
            browser.close()
