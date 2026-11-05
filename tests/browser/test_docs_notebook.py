"""Observe live notebook guides using the released native renderer."""

import importlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pytest

playwright = pytest.importorskip("playwright.sync_api")
ROOT = Path(__file__).resolve().parents[2]


def _expose_guide_api(markup, index):
    """Track the current native API in tests, clearing it on disposal."""
    return markup.replace(
        "{ bare: true }) : null;",
        f"""{{ bare: true }}) : null;
        window.guideApis[{index}] = api;
        const finalize = api.finalize;
        api.finalize = () => {{
            window.guideApis[{index}] = null;
            finalize();
        }};""",
    )


def _show_guide_chart(page, index):
    """Scroll to a chart and wait for its current render before inspecting it."""
    host = page.locator(".gs-doc-embed").nth(index)
    host.scroll_into_view_if_needed()
    page.wait_for_function("i => Boolean(window.guideApis[i])", arg=index)
    host.locator("canvas").wait_for()
    page.evaluate("i => {window.api = guideApis[i];}", index)
    page.evaluate(
        "async () => {await document.fonts.ready; await new Promise(requestAnimationFrame);}"
    )
    # Native entry animation changes pointer coordinates until its scale settles.
    page.wait_for_function(
        """i => {
        const canvas = document.querySelectorAll('.gs-doc-embed')[i].querySelector('canvas');
        return Math.abs(canvas.getBoundingClientRect().width - guideApis[i].getLogicalCanvasSize().width) < 0.1;
    }""",
        arg=index,
    )
    return host


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
    embeds = [_expose_guide_api(embed, index) for index, embed in enumerate(embeds)]
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
    _show_guide_chart(page, 0)
    return specs


def test_tracks_guide_fits_and_preserves_shared_navigation(monkeypatch, page):
    pytest.importorskip("scanpy")
    specs = _render_guide(page, monkeypatch, "tracks.ipynb")
    assert len(specs) == 3
    assert page.locator(".message-box").count() == 0
    for index in range(3):
        _show_guide_chart(page, index)
        size = page.evaluate("i => guideApis[i].getLogicalCanvasSize()", index)
        assert size["width"] <= 786
        assert (
            size["height"]
            <= page.locator(".gs-doc-embed").nth(index).bounding_box()["height"]
        )
        svg = page.evaluate(
            "async i => (await guideApis[i].imageExport.svg()).blob.text()", index
        )
        root = ET.fromstring(svg)
        labels = [e.text for e in root.iter() if e.tag.endswith("}text")]
        genes = (
            [
                "CD79A",
                "MS4A1",
                "CST3",
                "LYZ",
                "CD3D",
                "IL32",
            ]
            if index < 2
            else [
                "IL7R",
                "CD14",
                "LYZ",
                "MS4A1",
                "CD8A",
                "GNLY",
                "NKG7",
                "FCGR3A",
                "MS4A7",
                "FCER1A",
                "CST3",
                "PPBP",
            ]
        )
        assert all(
            label in labels
            for label in [*genes, "bulk_labels" if index < 2 else "louvain"]
        )
    assert specs[2]["scales"]["x"]["gapWidth"] == 3
    assert specs[2]["spacing"] == 6
    canvas = page.locator(".gs-doc-embed").nth(2).locator("canvas")
    canvas.scroll_into_view_if_needed()
    page.evaluate("""() => {
        window.track = guideApis[2].debug.getViewRoot().getDescendants()
            .find(view => view.spec.encoding?.y?.field === '_value_0');
        window.cellScale = track.getScaleResolution('x');
    }""")
    bounds = page.evaluate(
        "() => {const {x,y,width,height} = track.coords; return {x,y,width,height};}"
    )
    scroller = page.locator(".gs-doc-embed").nth(2).locator(".canvas-wrapper")
    scroller.evaluate(
        "(el, x) => el.scrollLeft = Math.max(0, x - el.clientWidth / 2)",
        bounds["x"] + bounds["width"] / 2,
    )
    box = canvas.bounding_box()
    before = page.evaluate("cellScale.getDomain()")
    page.mouse.move(
        box["x"] + bounds["x"] + bounds["width"] / 2,
        box["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -250)
    page.wait_for_function(
        "before => {const d=cellScale.getDomain(); return d[1]-d[0] < before[1]-before[0];}",
        arg=before,
    )
    navigation = page.evaluate("""() => {
        const views = guideApis[2].debug.getViewRoot().getDescendants()
            .filter(view => ['_cell', 'leaf'].includes(view.spec.encoding?.x?.field)
                || view.spec.name === 'heatmap-category-strip');
        return {
            count: views.length,
            trees: views.filter(view => view.spec.encoding?.x?.field === 'leaf').length,
            shared: views.every(view => view.getScaleResolution('x') === cellScale),
        };
    }""")
    # All 12 gene tracks, the category strip and the dendrogram must follow zoom.
    assert navigation == {"count": 14, "trees": 1, "shared": True}
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_paga_guide_legends_edge_cutoff_and_path_focus(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.interactions import (
        click_legend,
        point_coordinates,
        svg_root,
        value_texts,
    )

    specs = _render_guide(page, monkeypatch, "paga.ipynb")
    assert len(specs) == 10
    _show_guide_chart(page, 0)
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
        _show_guide_chart(page, index)
        assert sum(e.tag.endswith("linearGradient") for e in svg_root(page).iter()) == 1
        assert page.evaluate("api.getLogicalCanvasSize().width") <= 786
    _show_guide_chart(page, 5)
    assert not value_texts(svg_root(page))
    _show_guide_chart(page, 6)
    from tests.integrations.scanpy.browser.rendering import guide_geometry

    boxes = guide_geometry(page)["text"]
    title = next(box for box in boxes if box["label"] == "Source group")
    legend = [box for box in boxes if box["label"] in ("Adjacency", "Tree")]
    names = specs[6]["encoding"]["x"]["scale"]["domain"]
    ticks = [box for box in boxes if box["label"] in names]
    assert ticks and len(legend) == 2
    assert max(box["y"] + box["height"] for box in ticks) < title["y"]
    assert min(box["y"] for box in legend) > title["y"] + title["height"]
    assert (
        page.evaluate("api.getLogicalCanvasSize().height")
        <= page.locator(".gs-doc-embed").nth(6).bounding_box()["height"]
    )
    host = _show_guide_chart(page, 9)
    click_legend(page, "LYZ", canvas=host.locator("canvas"))
    opacity = {float(r.get("stroke-opacity", "1")) for r in edges()}
    assert len(opacity) == 2 and min(opacity) < max(opacity)
    _show_guide_chart(page, 7)
    assert page.evaluate("api.getLogicalCanvasSize().width") <= 786


def test_profiles_guide_run_gene_focus_and_heatmap_zoom(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.interactions import (
        click_legend,
        svg_root,
        value_texts,
    )

    specs = _render_guide(page, monkeypatch, "profiles.ipynb")
    assert len(specs) == 7
    for index in (0, 4):
        _show_guide_chart(page, index)
        label_view = specs[index]["surround"]["left"][0]
        mark = label_view["mark"]
        assert mark["align"] == "right" and mark["xOffset"] == -8
        assert mark["clip"] == "x" and mark["cullByVisibleRange"] is False
        source = label_view["data"]
        labels = source.get(
            "values", specs[index].get("datasets", {}).get(source.get("name"))
        )
        names = [row["label"] for row in labels]
        boxes = page.evaluate(
            """async names => {
            const svg = new DOMParser().parseFromString(
                await (await api.imageExport.svg()).blob.text(), 'image/svg+xml').documentElement;
            svg.style.cssText='position:fixed;left:0;top:0;visibility:hidden';
            document.body.append(svg);
            const boxes=[...svg.querySelectorAll('text')].filter(n=>names.includes(n.textContent)).map(n=>{
                const b=n.getBoundingClientRect();
                const group=n.closest('[clip-path]');
                const clip=group && svg.querySelector(group.getAttribute('clip-path').slice(4,-1)+' rect');
                const c=clip ? {
                    left:+clip.getAttribute('x'), top:+clip.getAttribute('y'),
                    right:+clip.getAttribute('x') + +clip.getAttribute('width'),
                    bottom:+clip.getAttribute('y') + +clip.getAttribute('height')
                } : svg.getBoundingClientRect();
                return {label:n.textContent,left:b.left,right:b.right,top:b.top,bottom:b.bottom,
                    clipLeft:c.left,clipRight:c.right,clipTop:c.top,clipBottom:c.bottom};
            });
            svg.remove();return boxes;
        }""",
            names,
        )
        assert {box["label"] for box in boxes} == set(names)
        for box in boxes:
            assert box["left"] >= box["clipLeft"] - 1, box
            assert box["right"] <= box["clipRight"] + 1, box
            assert box["top"] >= box["clipTop"] - 1, box
            assert box["bottom"] <= box["clipBottom"] + 1, box
    host = _show_guide_chart(page, 3)
    controls = host.locator("select")
    assert controls.count() == 1
    click_legend(page, "Gata1", canvas=host.locator("canvas"))
    controls.select_option(label="2")
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
    _show_guide_chart(page, 4)
    assert not value_texts(svg_root(page))
    chart = page.locator(".gs-doc-embed").nth(4).locator("canvas")
    chart.scroll_into_view_if_needed()
    bounds = page.evaluate("""() => {
        const view = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.encoding?.color?.field === '_value' && v.spec.mark?.type === 'rect');
        window.simGrid = view;
        const {x,y,width,height} = view.coords; return {x,y,width,height};
    }""")
    scroller = page.locator(".gs-doc-embed").nth(4).locator(".canvas-wrapper")
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
    host = _show_guide_chart(page, 1)
    slider = host.locator('input[type="range"]')
    assert slider.count() == 1
    saved = sc.read_h5ad(ROOT / "tmp/scanpy-guide-data/quality/hvg.h5ad")
    before = saved.var["highly_variable"].copy()
    slider.evaluate(
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

    host = _show_guide_chart(page, 2)
    original = bins()
    host.locator('input[type="range"]').evaluate(
        "(el) => {el.value=0.7; el.dispatchEvent(new Event('input', {bubbles:true}));}"
    )
    updated = bins()
    assert [r.get("fill") for r in original] != [r.get("fill") for r in updated]
    assert [[r.get(k) for k in ["x", "y", "width", "height"]] for r in original] == [
        [r.get(k) for k in ["x", "y", "width", "height"]] for r in updated
    ]
    reloaded = sc.read_h5ad(ROOT / "tmp/scanpy-guide-data/quality/hvg.h5ad")
    assert reloaded.var["highly_variable"].equals(before)


def test_umap_grid_native_legend_controls_and_linked_selection(monkeypatch, page):
    sc = pytest.importorskip("scanpy")
    specs = _render_guide(page, monkeypatch, "umap.ipynb")
    # Every grid panel stays square, including the categorical panel with a legend.
    host = _show_guide_chart(page, 13)
    grid = page.evaluate("""() => guideApis[13].debug.getViewRoot().getDescendants()
        .filter(v => v.spec.mark?.type === 'point'
            && v.spec.encoding?.x?.field?.startsWith('_coord_'))
        .map(v => ({x:v.coords.x, y:v.coords.y, width:v.coords.width, height:v.coords.height}))
    """)
    assert len(grid) == 9
    assert all(abs(p["width"] - p["height"]) < 0.1 for p in grid)
    assert len({round(p["x"]) for p in grid}) == 3
    assert len({round(p["y"]) for p in grid}) == 3
    assert specs[13]["resolve"]["legend"]["default"] == "collected"
    assert specs[13]["config"]["legend"]["orient"] == "right"
    from tests.integrations.scanpy.browser.interactions import click_legend, svg_root

    def legend_titles(orient=None):
        names = (
            {f"legend_region_{orient}"}
            if orient
            else {"legend_region_right", "legend_region_bottom"}
        )
        return {
            e.text
            for region in svg_root(page).iter()
            if region.get("data-name") in names
            for e in region.iter()
            if e.tag.endswith("text")
        }

    genes = {"CD79A", "MS4A1", "IGJ", "CD3D", "FCER1A", "FCGR3A", "LYZ"}
    select = host.locator("select")
    checkboxes = host.locator('input[type="checkbox"]')
    assert select.count() == 1 and checkboxes.count() == 2
    assert legend_titles() & genes == {"CD79A"}
    assert "bulk_labels" in legend_titles("bottom")
    assert "bulk_labels" not in legend_titles("right")
    assert "n_counts" not in legend_titles()
    select.select_option("MS4A1")
    checkboxes.nth(0).check()
    page.evaluate("()=>new Promise(requestAnimationFrame)")
    assert legend_titles() & genes == {"MS4A1"}
    assert {"n_counts", "bulk_labels"} <= legend_titles()
    legend_bounds = page.evaluate("""async () => {
        const svg=new DOMParser().parseFromString(await (await api.imageExport.svg()).blob.text(),'image/svg+xml').documentElement;
        svg.style.cssText='position:fixed;left:0;top:0;visibility:hidden';
        document.body.append(svg);
        const legend=svg.querySelector('[data-name="legend_region_right"]');
        const {x,y,width,height}=legend.getBoundingClientRect();
        const bottom=svg.querySelector('[data-name="legend_region_bottom"]').getBoundingClientRect();
        const category={x:bottom.x,y:bottom.y,width:bottom.width,height:bottom.height};
        svg.remove();return {legend:{x,y,width,height},category,canvas:api.getLogicalCanvasSize()};
    }""")
    legend = legend_bounds["legend"]
    assert legend["x"] >= max(p["x"] + p["width"] for p in grid)
    assert legend["x"] + legend["width"] <= legend_bounds["canvas"]["width"] + 1
    assert legend["y"] + legend["height"] <= legend_bounds["canvas"]["height"] + 1
    category = legend_bounds["category"]
    assert category["y"] >= max(p["y"] + p["height"] for p in grid)
    assert category["x"] >= -1
    assert category["x"] + category["width"] <= legend_bounds["canvas"]["width"] + 1
    assert category["y"] + category["height"] <= legend_bounds["canvas"]["height"] + 1
    assert legend_bounds["canvas"]["height"] <= page.locator(".gs-doc-embed").nth(
        13
    ).evaluate("el=>el.clientHeight")

    select.select_option(label="None")
    checkboxes.nth(0).uncheck()
    checkboxes.nth(1).uncheck()
    page.evaluate("()=>new Promise(requestAnimationFrame)")
    assert not legend_titles()
    checkboxes.nth(1).check()
    select.select_option("CD79A")
    page.evaluate("()=>new Promise(requestAnimationFrame)")
    assert legend_titles() & genes == {"CD79A"}
    assert "bulk_labels" in legend_titles() and "n_counts" not in legend_titles()
    host.locator(".canvas-wrapper").evaluate("el => el.scrollLeft = 0")
    click_legend(page, "CD19+ B", canvas=host.locator("canvas"))
    selected_count = int(
        (sc.datasets.pbmc68k_reduced().obs["bulk_labels"] == "CD19+ B").sum()
    )
    groups = [
        g
        for g in svg_root(page).iter()
        if g.get("data-mark-type") == "point" and g.get("clip-path")
    ]
    assert len(groups) == 9
    for group in groups:
        assert len(group) == 700
        assert (
            sum(float(point.get("fill-opacity", "1")) == 1 for point in group)
            == selected_count
        )
    click_legend(page, "CD19+ B", shift=True, canvas=host.locator("canvas"))


def test_umap_guide_interactions_and_horizontal_scroll(monkeypatch, page):
    sc = pytest.importorskip("scanpy")
    import genome_spy.integrations.scanpy as gsc

    specs = _render_guide(page, monkeypatch, "umap.ipynb")
    width = page.viewport_size["width"]
    _show_guide_chart(page, 0)
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

    linked = _show_guide_chart(page, 1).locator("canvas")
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
        _show_guide_chart(page, 0)
        scroller = page.locator(".canvas-wrapper").first
        assert scroller.evaluate("el => getComputedStyle(el).overflowX") == "auto"
        assert scroller.evaluate("el => el.scrollWidth > el.clientWidth")
        before = canvas.bounding_box()["x"]
        scroller.evaluate("el => el.scrollLeft = el.scrollWidth")
        offset = scroller.evaluate("el => el.scrollLeft")
        assert offset > 0
        assert canvas.bounding_box()["x"] == pytest.approx(before - offset)


@pytest.mark.parametrize(
    "index,labels",
    [
        (2, ["UMAP1", "UMAP2"]),
        (7, ["PC1", "PC2"]),
        (11, ["tSNE1", "tSNE2"]),
        (12, ["DC2", "DC3"]),
    ],
)
def test_prepared_embedding_guide_hover_and_zoom(monkeypatch, page, index, labels):
    pytest.importorskip("scanpy")
    from scipy.spatial import cKDTree

    from tests.integrations.scanpy.browser.interactions import hover_at

    specs = _render_guide(page, monkeypatch, "umap.ipynb")
    assert len(specs) == 14
    _show_guide_chart(page, index)
    bounds = page.evaluate("""() => {
        window.embedding = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.mark?.type === 'point'
                && v.spec.encoding?.x?.field?.startsWith('_coord_'));
        const {x,y,width,height} = embedding.coords;
        return {x,y,width,height};
    }""")
    chart = page.locator(".gs-doc-embed").nth(index).locator("canvas")
    chart.scroll_into_view_if_needed()
    host = page.locator(".gs-doc-embed").nth(index)
    size = page.evaluate("api.getLogicalCanvasSize()")
    assert size["width"] <= 736
    assert size["height"] <= host.bounding_box()["height"]
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    texts = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
    if index == 2:
        assert "VWF expression (36,785 cells)" in texts
        radius = max(
            float(e.get("r"))
            for e in ET.fromstring(svg).iter()
            if e.tag.endswith("circle")
        )
    else:
        assert all(
            any(
                text == label or (text or "").startswith(label + " (") for text in texts
            )
            for label in labels
        )
    rows = next(
        rows for rows in specs[index]["datasets"].values() if "_obs_id" in rows[0]
    )
    assert len(rows) == {2: 36785, 7: 2638, 11: 2638}.get(index, 700)
    fields = page.evaluate("['x','y'].map(c => embedding.spec.encoding[c].field)")
    before = page.evaluate(
        "['x','y'].map(c => embedding.getScaleResolution(c).getDomain())"
    )
    coordinates = np.array([[row[field] for field in fields] for row in rows])
    low, high = np.array(before).T
    normalized = (coordinates - low) / (high - low)
    distances, _ = cKDTree(normalized).query(normalized, k=2)
    selected = int(distances[:, 1].argmax())
    x, y = normalized[selected]
    page.locator(".gs-doc-embed").nth(index).locator(".canvas-wrapper").evaluate(
        "(el, x) => {el.scrollLeft = Math.max(0, x-el.clientWidth/2);}",
        bounds["x"] + x * bounds["width"],
    )
    tooltip = (
        page.locator("table.attributes")
        .get_by_text(rows[selected]["_obs_label"], exact=True)
        .first
    )
    hover_at(
        page,
        bounds["x"] + x * bounds["width"],
        bounds["y"] + (1 - y) * bounds["height"],
        canvas=chart,
        target=tooltip,
    )
    tooltip.wait_for(state="visible")
    # Tiny overview points need a closer zoom before their growth is visible.
    page.mouse.wheel(0, -1600 if index == 2 else -350)
    page.wait_for_function(
        """({before, fraction}) => ['x','y'].every((c,i) => {
            const d=embedding.getScaleResolution(c).getDomain();
            return d[1]-d[0] < fraction*(before[i][1]-before[i][0]);
        })""",
        arg={"before": before, "fraction": 0.4 if index == 2 else 1},
    )
    if index == 2:
        zoomed = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        grown = max(
            float(e.get("r"))
            for e in ET.fromstring(zoomed).iter()
            if e.tag.endswith("circle")
        )
        assert radius < grown <= 2 * radius
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_export_guide_buttons_download_native_images(monkeypatch, page):
    pytest.importorskip("scanpy")
    from PIL import Image

    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    extension = importlib.import_module("genomespy_notebook")
    definitions, _ = extension.core.default_control_config()
    monkeypatch.setattr(
        extension.core,
        "default_control_config",
        lambda: (definitions, {"core": "/controls.js"}),
    )
    page.route(
        "http://guide.test/controls.js",
        lambda route: route.fulfill(
            content_type="text/javascript",
            body=(ROOT / "src/genome_spy/static/controls.js").read_text(),
        ),
    )
    specs = _render_guide(page, monkeypatch, "export.ipynb")
    assert len(specs) == 1
    page.get_by_role("button", name="PNG", exact=True).wait_for(state="attached")
    page.keyboard.press("Tab")
    for format in ("PNG", "SVG"):
        with page.expect_download() as pending:
            page.get_by_role("button", name=format, exact=True).click()
        download = pending.value
        assert download.suggested_filename == f"genomespy.{format.lower()}"
        path = download.path()
        if format == "PNG":
            image = Image.open(path).convert("RGB")
            assert min(image.size) >= 300
            assert len(image.getcolors(maxcolors=1_000_000)) > 10
        else:
            root = ET.parse(path).getroot()
            assert sum(e.tag.endswith("circle") for e in root.iter()) >= 700


def test_expression_guide_hover_zoom_and_fitted_values(monkeypatch, page):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.interactions import value_texts

    specs = _render_guide(page, monkeypatch, "expression.ipynb")
    for index in range(len(specs)):
        host = _show_guide_chart(page, index)
        assert page.evaluate("api.getLogicalCanvasSize().height") <= host.evaluate(
            "el => el.clientHeight"
        )
        param = {
            0: "grid_cursor",
            1: "grid_hover",
            2: "grid_cursor",
            3: "grid_hover",
            6: "grid_cursor",
            7: "grid_cursor",
            8: "grid_hover",
        }.get(index)
        if param:
            assert page.evaluate("name => Boolean(api.getParam(name))", param)
    _show_guide_chart(page, 0)
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
        const value = scale(row[plot(0).spec.encoding[channel].field]);
        const offset = scale.bandwidth() / 2;
        return channel === 'x' ? value + offset : 1 - value + (scale.type === 'band' ? -offset : offset);
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
    _show_guide_chart(page, 2)
    overview = ET.fromstring(
        page.evaluate("async () => (await guideApis[2].imageExport.svg()).blob.text()")
    )
    assert not value_texts(overview)
    for index in [0, 1, 7, 8, 2]:
        host = _show_guide_chart(page, index)
        chart = host.locator("canvas")
        bounds = page.evaluate("gridBounds", index)
        # Bring the plot into view before using its center on a narrow page.
        scroller = page.locator(".gs-doc-embed").nth(index).locator(".canvas-wrapper")
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
        if index != 2:
            page.wait_for_timeout(180)
            assert page.evaluate("domains", index) == before
            continue
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
    sizes = []
    exports = []
    for index in range(len(specs)):
        host = _show_guide_chart(page, index)
        assert host.locator("canvas").count() == 1
        sizes.append(
            {
                "height": host.evaluate("el => el.clientHeight"),
                "canvas": page.evaluate("api.getLogicalCanvasSize().height"),
            }
        )
        exports.append(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
    overflow = [
        (index, size)
        for index, size in enumerate(sizes)
        if size["canvas"] > size["height"]
    ]
    assert not overflow, overflow
    assert page.locator(".message-box").count() == 0
    assert all("<svg" in svg and "<text" in svg for svg in exports)
    if name == "ranked.ipynb":
        gene = sc.datasets.pbmc68k_reduced().uns["rank_genes_groups"]["names"][
            "CD19+ B"
        ][0]
        assert gene in exports[0]
        assert "CD19+ B" in exports[0]
        assert len(specs) == 6
        assert all(gene in svg for svg in exports[1:4])
        assert "Log2 fold change" in exports[4]
        assert "−log10 adjusted p-value" in exports[5]
    else:
        assert "PC1" in exports[0] and "PC2" in exports[0]
        assert all(size["height"] - size["canvas"] <= 40 for size in sizes), sizes
        _show_guide_chart(page, 2)
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


@pytest.mark.parametrize("index", [1, 2, 4, 5])
def test_ranked_summary_guide_hover_without_zoom(monkeypatch, page, index):
    pytest.importorskip("scanpy")
    from tests.integrations.scanpy.browser.interactions import hover_at

    specs = _render_guide(page, monkeypatch, "ranked.ipynb")
    _show_guide_chart(page, index)
    bounds = page.evaluate("""() => {
        window.rankGrid = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.encoding?.color?.field === '_mean');
        const {x,y,width,height} = rankGrid.coords;
        return {x,y,width,height};
    }""")
    rows = next(
        rows for rows in specs[index]["datasets"].values() if "_gene" in rows[0]
    )
    row = max((r for r in rows if r["_x"] == 2), key=lambda r: r.get("_percent", 1))
    fractions = page.evaluate(
        """row => ['x', 'y'].map(channel => {
            const scale = rankGrid.getScaleResolution(channel).getScale();
            const value = scale(row[`_${channel}`]);
            return (channel === 'x' ? value : 1 - value) + scale.bandwidth() / 2;
        })""",
        row,
    )
    chart = page.locator(".gs-doc-embed").nth(index).locator("canvas")
    chart.scroll_into_view_if_needed()
    page.locator(".gs-doc-embed").nth(index).locator(".canvas-wrapper").evaluate(
        "(el, x) => {el.scrollLeft = Math.max(0, x-el.clientWidth/2);}",
        bounds["x"] + bounds["width"] * fractions[0],
    )
    hover_at(
        page,
        bounds["x"] + bounds["width"] * fractions[0],
        bounds["y"] + bounds["height"] * fractions[1],
        canvas=chart,
    )
    tooltip = page.locator("table.attributes")
    tooltip.get_by_text(row["_gene"], exact=True).wait_for(state="visible")
    tooltip.get_by_text(row["_group"], exact=True).wait_for(state="visible")
    before = page.evaluate(
        "['x','y'].map(c => rankGrid.getScaleResolution(c).getDomain())"
    )
    page.mouse.wheel(0, -450)
    page.wait_for_timeout(180)
    assert (
        page.evaluate("['x','y'].map(c => rankGrid.getScaleResolution(c).getDomain())")
        == before
    )
