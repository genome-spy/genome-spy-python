"""Observe live notebook guides using the released native renderer."""

import importlib
import json
import re
from xml.etree import ElementTree as ET
from pathlib import Path

import numpy as np
import pytest

playwright = pytest.importorskip("playwright.sync_api")
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(params=[1200, 430])
def page(request):
    """Open a clean browser at each supported guide width and check its errors."""
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": request.param, "height": 1400})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error).splitlines()[0]))
        yield page
        assert not errors
        browser.close()


def _render_guide(page, monkeypatch, name):
    """Render a notebook's charts with the shipped bundle for observed checks."""
    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    extension = importlib.import_module("genomespy_notebook")
    markdown = extension._notebook_markdown(
        ROOT / "integrations/scanpy/guides" / name,
        download_path=name,
        bundle_url="/core.js",
    )
    embeds = re.findall(r"```\{raw\} html\n(.*?)\n```", markdown, re.S)
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    # Test-only access to the native APIs; the documentation exposes no globals.
    embeds = [
        embed.replace(
            "{ bare: true }) : null;",
            f"{{ bare: true }}) : null; window.guideApis[{index}] = api;",
        )
        for index, embed in enumerate(embeds)
    ]
    css = (ROOT / "docs/_static/genomespy.css").read_text()
    markup = (
        f"<style>{css}\nbody{{margin:16px}} main{{max-width:786px;margin:auto}}</style>"
        '<script>window.guideApis = [];</script><main class="gs-notebook">'
        + "".join(embeds)
        + "</main>"
    )
    page.route(
        "http://guide.test/core.js",
        lambda route: route.fulfill(
            content_type="text/javascript",
            body=(ROOT / "src/genome_spy/static/genome-spy.js").read_text(),
        ),
    )
    page.route(
        "http://guide.test/",
        lambda route: route.fulfill(content_type="text/html", body=markup),
    )
    page.goto("http://guide.test/")
    page.wait_for_function(
        "count => guideApis.filter(Boolean).length === count", arg=len(specs)
    )
    page.evaluate(
        "async () => { await document.fonts.ready; await new Promise(requestAnimationFrame); }"
    )
    page.wait_for_function("""() => [...document.querySelectorAll('canvas')].every((c, i) =>
        Math.abs(c.getBoundingClientRect().width - guideApis[i].getLogicalCanvasSize().width) < 0.1)
    """)
    return specs


def test_umap_guide_interactions_and_horizontal_scroll(monkeypatch, page):
    sc = pytest.importorskip("scanpy")
    import genome_spy.integrations.scanpy as gsc

    specs = _render_guide(page, monkeypatch, "umap.ipynb")
    width = page.viewport_size["width"]
    page.evaluate("""() => {
        window.points = index => guideApis[index].debug.getViewRoot()
            .getDescendants().find(view => view.spec.mark?.type === 'point'
                && view.spec.encoding?.x?.field?.startsWith('_coord_'));
        window.domain = channel => points(0).getScaleResolution(channel).getDomain();
        window.bounds = index => {
            const {x, y, width, height} = points(index).coords;
            return {x, y, width, height};
        };
    }""")
    canvas = page.locator("canvas").first
    box = canvas.bounding_box()
    bounds = page.evaluate("bounds(0)")
    rows = next(iter(specs[0]["datasets"].values()))
    coordinates = np.array([[r["_coord_0"], r["_coord_1"]] for r in rows])
    distances = ((coordinates[:, None] - coordinates[None, :]) ** 2).sum(axis=2)
    np.fill_diagonal(distances, np.inf)
    isolated = rows[int(distances.min(axis=1).argmax())]
    domains = page.evaluate("['x','y'].map(domain)")
    position = [
        (isolated[f"_coord_{i}"] - low) / (high - low)
        for i, (low, high) in enumerate(domains)
    ]
    x = box["x"] + bounds["x"] + position[0] * bounds["width"]
    y = box["y"] + bounds["y"] + (1 - position[1]) * bounds["height"]
    page.mouse.move(x - 1, y - 1)
    page.wait_for_timeout(450)
    # Allow one pixel for picking small symbols after the native tooltip delay.
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        page.mouse.move(x + dx, y + dy)
        page.wait_for_timeout(100)
        if (
            page.locator("table.attributes")
            .get_by_text(isolated["_obs_label"], exact=True)
            .first.is_visible()
        ):
            break
    page.locator("table.attributes").get_by_text(
        isolated["_obs_label"], exact=True
    ).first.wait_for(state="visible")

    page.mouse.move(
        box["x"] + bounds["x"] + bounds["width"] / 2,
        box["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -300)
    page.wait_for_function(
        """before => ['x','y'].every((channel, i) => {
        const after = domain(channel);
        return after[1]-after[0] < before[i][1]-before[i][0];
    })""",
        arg=domains,
    )

    linked = page.locator("canvas").nth(1)
    linked.scroll_into_view_if_needed()
    box = linked.bounding_box()
    bounds = page.evaluate("bounds(1)")
    x, y = box["x"] + bounds["x"], box["y"] + bounds["y"]
    page.mouse.move(x + 0.2 * bounds["width"], y + 0.2 * bounds["height"])
    page.mouse.down()
    page.mouse.move(x + 0.7 * bounds["width"], y + 0.7 * bounds["height"], steps=12)
    page.mouse.up()
    snapshot = page.evaluate("guideApis[1].getParam('cells').getValue()")
    mask = gsc.selection_mask(sc.datasets.pbmc68k_reduced(), snapshot)
    assert 0 < mask.sum() < 700
    svg = page.evaluate(
        "async () => (await guideApis[1].imageExport.svg()).blob.text()"
    )
    assert f"{mask.sum()} cells selected" in svg
    page.mouse.dblclick(x + bounds["width"] / 2, y + bounds["height"] / 2)
    page.wait_for_function(
        "guideApis[1].getParam('cells').getValue().intervals.x === null"
    )
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    if width == 430:
        scroller = page.locator(".canvas-wrapper").first
        assert scroller.evaluate("el => getComputedStyle(el).overflowX") == "auto"
        assert scroller.evaluate("el => el.scrollWidth > el.clientWidth")
        before = canvas.bounding_box()["x"]
        scroller.evaluate("el => el.scrollLeft = el.scrollWidth")
        offset = scroller.evaluate("el => el.scrollLeft")
        assert offset > 0
        assert canvas.bounding_box()["x"] == pytest.approx(before - offset)


def test_expression_guide_hover_zoom_and_fitted_values(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.test_grid_interactions import value_texts

    specs = _render_guide(page, monkeypatch, "expression.ipynb")
    page.evaluate("""() => {
        window.plot = index => guideApis[index].debug.getViewRoot().getDescendants()
            .find(view => view.spec.encoding?.color?.field === (index === 2 ? '_value' : '_mean'));
        window.domains = index => ['x', 'y'].map(c => plot(index).getScaleResolution(c).getDomain());
        window.gridBounds = index => {
            const {x, y, width, height} = plot(index).coords;
            return {x, y, width, height};
        };
    }""")
    rows = next(rows for rows in specs[0]["datasets"].values() if "_gene" in rows[0])
    dot = max((r for r in rows if r["_x"] == 0), key=lambda r: r["_percent"])
    fractions = page.evaluate(
        """row => ['x', 'y'].map(channel => {
        const scale = plot(0).getScaleResolution(channel).getScale();
        const value = scale(row[`_${channel}`]);
        return (channel === 'x' ? value : 1 - value) + scale.bandwidth() / 2;
    })""",
        dot,
    )
    canvas = page.locator("canvas").first.bounding_box()
    bounds = page.evaluate("gridBounds(0)")
    x = canvas["x"] + bounds["x"] + fractions[0] * bounds["width"]
    y = canvas["y"] + bounds["y"] + fractions[1] * bounds["height"]
    page.mouse.move(x - 1, y - 1)
    page.wait_for_timeout(450)
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        page.mouse.move(x + dx, y + dy)
        page.wait_for_timeout(100)
        if (
            page.locator("table.attributes")
            .get_by_text(dot["_gene"], exact=True)
            .is_visible()
        ):
            break
    page.locator("table.attributes").get_by_text(dot["_gene"], exact=True).wait_for(
        state="visible"
    )
    page.locator("table.attributes").get_by_text(dot["_group"], exact=True).wait_for(
        state="visible"
    )
    overview = ET.fromstring(
        page.evaluate("async () => (await guideApis[2].imageExport.svg()).blob.text()")
    )
    assert not value_texts(overview)
    for index in range(3):
        chart = page.locator("canvas").nth(index)
        chart.scroll_into_view_if_needed()
        bounds = page.evaluate("gridBounds", index)
        # Bring the plot into view before using its center on a narrow page.
        scroller = page.locator(".canvas-wrapper").nth(index)
        scroller.evaluate(
            "(el, center) => el.scrollLeft = Math.max(0, center - el.clientWidth / 2)",
            bounds["x"] + bounds["width"] / 2,
        )
        canvas = chart.bounding_box()
        before = page.evaluate("domains", index)
        page.mouse.move(
            canvas["x"] + bounds["x"] + bounds["width"] / 2,
            canvas["y"] + bounds["y"] + bounds["height"] / 2,
        )
        page.mouse.wheel(0, -800)
        page.wait_for_function(
            """({index, before}) => {
            const after = domains(index)[1];
            return Math.abs(after[1]-after[0]) < Math.abs(before[1][1]-before[1][0]);
        }""",
            arg={"index": index, "before": before},
        )
        assert page.evaluate("domains", index)[0] == before[0]
    for _ in range(5):
        exported = ET.fromstring(
            page.evaluate(
                "async () => (await guideApis[2].imageExport.svg()).blob.text()"
            )
        )
        if value_texts(exported):
            break
        page.mouse.wheel(0, -800)
        page.wait_for_timeout(180)
    assert value_texts(exported)
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


@pytest.mark.parametrize("name", ["pca.ipynb", "ranked.ipynb"])
def test_diagnostic_guide_charts_render(monkeypatch, page, name):
    sc = pytest.importorskip("scanpy")
    specs = _render_guide(page, monkeypatch, name)
    assert page.locator("canvas").count() == len(specs)
    assert page.locator(".message-box").count() == 0
    exports = page.evaluate("""async () => Promise.all(guideApis.map(async api =>
        (await api.imageExport.svg()).blob.text()))""")
    assert all("<svg" in svg and "<text" in svg for svg in exports)
    if name == "ranked.ipynb":
        gene = sc.datasets.pbmc68k_reduced().uns["rank_genes_groups"]["names"][
            "CD19+ B"
        ][0]
        assert gene in exports[0]
        assert "CD19+ B" in exports[0]
        assert all(gene in svg for svg in exports[1:])
    else:
        assert "PC1" in exports[0] and "PC2" in exports[0]
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
