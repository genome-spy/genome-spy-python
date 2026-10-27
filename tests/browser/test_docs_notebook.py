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
    notebook = json.loads((ROOT / "integrations/scanpy/guides" / name).read_text())
    if extension._prepared_paths(notebook, ROOT) and not extension._preparation_current(
        notebook, ROOT
    ):
        pytest.skip("Run integrations/scanpy/prepare_guide_data.py first")
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


def test_paga_guide_legends_edge_cutoff_and_path_focus(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.test_grid_interactions import (
        position,
        svg_root,
        value_texts,
    )
    from tests.integrations.scanpy.browser.test_timeseries import point_coordinates

    specs = _render_guide(page, monkeypatch, "paga.ipynb")
    assert len(specs) == 10
    page.evaluate("window.api = guideApis[0]")
    root = svg_root(page)
    symbols = [
        p
        for g in root.iter()
        if g.get("data-mark-type") == "point" and not g.get("clip-path")
        for p in g
    ]
    assert len(symbols) == 10
    before = point_coordinates(page)[0]

    def edges():
        return [
            r
            for g in svg_root(page).iter()
            if g.get("data-mark-type") == "rule" and g.get("clip-path")
            for r in g
        ]

    count = len(edges())
    assert count > 0
    page.locator('input[type="range"]').evaluate(
        "el => {el.value=1; el.dispatchEvent(new Event('input', {bubbles:true}));}"
    )
    assert len(edges()) < count
    np.testing.assert_array_equal(point_coordinates(page)[0], before)
    for index in [1, 2, 3]:
        page.evaluate("i => window.api = guideApis[i]", index)
        assert sum(e.tag.endswith("linearGradient") for e in svg_root(page).iter()) == 1
        assert page.evaluate("api.getLogicalCanvasSize().width") <= 786
    page.evaluate("window.api = guideApis[5]")
    assert not value_texts(svg_root(page))
    page.evaluate("window.api = guideApis[6]")
    text = [e for e in svg_root(page).iter() if e.tag.endswith("text")]
    title = next(e for e in text if e.text == "Source group")
    legend = [e for e in text if e.text in ["Adjacency", "Tree"]]
    assert len(legend) == 2
    label_bottom = page.evaluate("""() => {
        const view = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.encoding?.x?.field === 'slot');
        return view.coords.y + view.coords.height;
    }""")
    assert position(title)[1] > label_bottom
    assert min(position(e)[1] for e in legend) > position(title)[1]
    assert (
        page.evaluate("api.getLogicalCanvasSize().height")
        <= page.locator(".gs-doc-embed").nth(6).bounding_box()["height"]
    )
    page.evaluate("window.api = guideApis[9]")
    page.locator("select").select_option(label="LYZ")
    opacity = {float(r.get("stroke-opacity", "1")) for r in edges()}
    assert len(opacity) == 2 and min(opacity) < max(opacity)
    assert page.evaluate("guideApis[7].getLogicalCanvasSize().width") <= 786


def test_profiles_guide_run_gene_focus_and_heatmap_zoom(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.test_grid_interactions import (
        svg_root,
        value_texts,
    )

    specs = _render_guide(page, monkeypatch, "profiles.ipynb")
    assert len(specs) == 7
    controls = page.locator("select")
    assert controls.count() == 5
    # The first control belongs to the supplied profiles; the next pair to simulation points.
    controls.nth(1).select_option(label="Gata1")
    controls.nth(2).select_option(label="2")
    page.evaluate("window.api = guideApis[3]")
    root = svg_root(page)
    points = [
        p
        for g in root.iter()
        if g.get("data-mark-type") == "point" and g.get("clip-path")
        for p in g
    ]
    assert len(points) == 3200
    assert sum(float(p.get("fill-opacity", "1")) == 0.85 for p in points) == 160
    assert sum(float(p.get("fill-opacity", "1")) == 0.12 for p in points) == 3040
    page.evaluate("window.api = guideApis[4]")
    assert not value_texts(svg_root(page))
    chart = page.locator("canvas").nth(4)
    chart.scroll_into_view_if_needed()
    bounds = page.evaluate("""() => {
        const view = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.encoding?.color?.field === '_value' && v.spec.mark?.type === 'rect');
        window.simGrid = view;
        const {x,y,width,height} = view.coords; return {x,y,width,height};
    }""")
    scroller = page.locator(".canvas-wrapper").nth(4)
    scroller.evaluate(
        "(el, x) => el.scrollLeft = Math.max(0, x-el.clientWidth/2)",
        bounds["x"] + bounds["width"] / 2,
    )
    canvas = chart.bounding_box()
    before = page.evaluate("simGrid.getScaleResolution('x').getDomain()")
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] / 2,
        canvas["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -2400)
    page.wait_for_function(
        "before => {const d=simGrid.getScaleResolution('x').getDomain(); return d[1]-d[0] < before[1]-before[0];}",
        arg=before,
    )
    for _ in range(6):
        if value_texts(svg_root(page)):
            break
        page.mouse.wheel(0, -800)
        page.wait_for_timeout(200)
    assert value_texts(svg_root(page))


def test_data_check_guide_sliders_update_saved_results_preview(monkeypatch, page):
    sc = pytest.importorskip("scanpy")
    specs = _render_guide(page, monkeypatch, "quality.ipynb")
    assert len(specs) == 3
    sliders = page.locator('input[type="range"]')
    assert sliders.count() == 2
    saved = sc.read_h5ad(ROOT / "tmp/scanpy-guide-data/quality/hvg.h5ad")
    before = saved.var["highly_variable"].copy()
    sliders.nth(0).evaluate(
        "(el) => {el.value=1; el.dispatchEvent(new Event('input', {bubbles:true}));}"
    )
    count = int((saved.var["dispersions_norm"] >= 1).sum())
    page.wait_for_function(
        "async count => (await (await guideApis[1].imageExport.svg()).blob.text()).includes(count + ' genes above cutoff (preview)')",
        arg=count,
    )

    def bins():
        root = ET.fromstring(
            page.evaluate(
                "async () => (await guideApis[2].imageExport.svg()).blob.text()"
            )
        )
        return [
            r
            for g in root.iter()
            if g.get("data-mark-type") == "rect" and g.get("clip-path")
            for r in g
        ]

    original = bins()
    sliders.nth(1).evaluate(
        "(el) => {el.value=0.7; el.dispatchEvent(new Event('input', {bubbles:true}));}"
    )
    updated = bins()
    assert [r.get("fill") for r in original] != [r.get("fill") for r in updated]
    assert [[r.get(k) for k in ["x", "y", "width", "height"]] for r in original] == [
        [r.get(k) for k in ["x", "y", "width", "height"]] for r in updated
    ]
    reloaded = sc.read_h5ad(ROOT / "tmp/scanpy-guide-data/quality/hvg.h5ad")
    assert reloaded.var["highly_variable"].equals(before)


def test_larger_data_guide_hover_zoom_and_point_growth(monkeypatch, page):
    pytest.importorskip("scanpy")
    from scipy.spatial import cKDTree

    specs = _render_guide(page, monkeypatch, "larger_data.ipynb")
    assert len(specs) == 4
    rows = next(iter(specs[2]["datasets"].values()))
    assert len(rows) == 11537
    coordinates = np.array([[r["_coord_0"], r["_coord_1"]] for r in rows])
    nearest, _ = cKDTree(coordinates).query(coordinates, k=2)
    isolated = rows[int(nearest[:, 1].argmax())]
    page.evaluate("""() => {
        window.largePoints = () => guideApis[2].debug.getViewRoot().getDescendants()
            .find(v => v.spec.mark?.type === 'point' && v.spec.encoding?.x?.field === '_coord_0');
        window.largeDomains = () => ['x','y'].map(c => largePoints().getScaleResolution(c).getDomain());
    }""")
    chart = page.locator("canvas").nth(2)
    chart.scroll_into_view_if_needed()
    bounds = page.evaluate("""() => {
        const {x,y,width,height} = largePoints().coords; return {x,y,width,height};
    }""")
    domains = page.evaluate("largeDomains()")
    fraction = [
        (isolated[f"_coord_{i}"] - low) / (high - low)
        for i, (low, high) in enumerate(domains)
    ]
    local_x = bounds["x"] + fraction[0] * bounds["width"]
    page.locator(".canvas-wrapper").nth(2).evaluate(
        "(el, x) => el.scrollLeft = Math.max(0, x - el.clientWidth / 2)", local_x
    )
    canvas = chart.bounding_box()
    x = canvas["x"] + local_x
    y = canvas["y"] + bounds["y"] + (1 - fraction[1]) * bounds["height"]
    page.mouse.move(x - 1, y - 1)
    page.wait_for_timeout(400)
    tooltip_id = (
        page.locator("table.attributes")
        .get_by_text(isolated["_obs_id"], exact=True)
        .first
    )
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        page.mouse.move(x + dx, y + dy)
        page.wait_for_timeout(100)
        if tooltip_id.is_visible():
            break
    tooltip_id.wait_for(state="visible", timeout=2000)

    def radii():
        root = ET.fromstring(
            page.evaluate(
                "async () => (await guideApis[2].imageExport.svg()).blob.text()"
            )
        )
        return [
            float(p.get("r"))
            for g in root.iter()
            if g.get("data-mark-type") == "point" and g.get("clip-path")
            for p in g
            if p.tag.endswith("circle")
        ]

    before = radii()
    assert len(before) == 2 * len(rows)
    page.mouse.wheel(0, -450)
    page.wait_for_function(
        "before => largeDomains()[0][1]-largeDomains()[0][0] < before[0][1]-before[0][0]",
        arg=domains,
    )
    assert min(radii()) > max(before)


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
    sizes = page.evaluate("""() => [...document.querySelectorAll('.gs-doc-embed')]
        .map((host, i) => ({height:host.clientHeight,
            canvas:guideApis[i].getLogicalCanvasSize().height}))""")
    for index, size in enumerate(sizes):
        assert size["canvas"] <= size["height"], (index, size)
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
    sizes = page.evaluate("""() => [...document.querySelectorAll('.gs-doc-embed')]
        .map((host, i) => ({height:host.clientHeight,
            canvas:guideApis[i].getLogicalCanvasSize().height}))""")
    overflow = [
        (index, size)
        for index, size in enumerate(sizes)
        if size["canvas"] > size["height"]
    ]
    assert not overflow, overflow
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
        assert all(size["height"] - size["canvas"] <= 40 for size in sizes), sizes
        overview = page.evaluate("""() => {
            const api = guideApis[2];
            return {canvas:api.getLogicalCanvasSize(),
                panels:api.debug.getViewRoot().getDescendants()
                    .filter(v => v.spec.encoding?.y?.field === '_score')
                    .map(v => {const {x,y,width,height} = v.coords;
                        return {x,y,width,height};})};
        }""")
        assert len(overview["panels"]) == 4
        if page.viewport_size["width"] >= 1200:
            assert overview["canvas"]["width"] <= 736
        assert overview["canvas"]["height"] <= 1200
        assert overview["panels"][2]["y"] == pytest.approx(
            overview["panels"][3]["y"], abs=1
        )
        for box in overview["panels"]:
            assert (
                0 <= box["x"] < box["x"] + box["width"] <= overview["canvas"]["width"]
            ), overview
        assert all(
            title in exports[2]
            for title in (
                "variance ratio",
                "PC1",
                "PC2",
                "PC3",
            )
        )
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
