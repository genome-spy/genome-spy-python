"""Check native brush-driven expression summaries against the source cells."""

import importlib
import io
import json
import mimetypes
import re
import shutil
from itertools import count
from pathlib import Path
from urllib.parse import urlsplit

import numpy as np
import pytest

from tests.browser.test_docs_notebook import ROOT
from tests.browser.test_docs_notebook import page as page
from tests.integrations.scanpy.browser.interactions import (
    position,
    svg_root,
    value_texts,
)

pytestmark = pytest.mark.docs


def _render_furo_guide(page, monkeypatch, tmp_path):
    """Exercise actual Sphinx sections and the theme's article width, not a mock wrapper."""
    pytest.importorskip("furo")
    from sphinx.testing.util import SphinxTestApp

    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    extension = importlib.import_module("genomespy_notebook")
    monkeypatch.setattr(extension.core, "default_bundle_url", lambda: "/core.js")
    source = tmp_path / "docs"
    (source / "_static").mkdir(parents=True)
    guide = tmp_path / "integrations/scanpy/guides/linked_expression.ipynb"
    guide.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / "integrations/scanpy/guides/linked_expression.ipynb", guide)
    notebook = json.loads(guide.read_text())
    if not extension._preparation_current(notebook, ROOT):
        pytest.skip(
            "Run integrations/scanpy/prepare_guide_data.py linked_expression first"
        )
    for cached in extension._prepared_paths(notebook, ROOT).values():
        target = tmp_path / cached.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, target)
        shutil.copyfile(cached.with_suffix(".sha256"), target.with_suffix(".sha256"))
    shutil.copyfile(
        ROOT / "docs/_static/genomespy.css", source / "_static/genomespy.css"
    )
    (source / "conf.py").write_text(
        'extensions = ["myst_parser", "genomespy_notebook"]\n'
        'myst_enable_extensions = ["colon_fence"]\n'
        'html_theme = "furo"\nhtml_static_path = ["_static"]\n'
        'html_css_files = ["genomespy.css"]\n'
    )
    (source / "index.md").write_text(
        "```{genomespy-notebook} integrations/scanpy/guides/linked_expression.ipynb\n```\n"
    )
    warnings = io.StringIO()
    app = SphinxTestApp(
        srcdir=source,
        builddir=tmp_path / "build",
        warning=warnings,
        status=io.StringIO(),
    )
    output = Path(app.outdir)
    try:
        app.build()
    finally:
        app.cleanup()
    assert not warnings.getvalue()
    markup = (
        (output / "index.html")
        .read_text()
        .replace("<head>", "<head><script>window.guideApis = [];</script>")
    )
    indices = count()
    markup = re.sub(
        re.escape("{ bare: true }) : null;"),
        lambda match: f"{match[0]} window.guideApis[{next(indices)}] = api;",
        markup,
    )

    def serve(route):
        path = urlsplit(route.request.url).path
        if path == "/":
            route.fulfill(content_type="text/html", body=markup)
        elif path == "/core.js":
            route.fulfill(
                content_type="text/javascript",
                body=(ROOT / "src/genome_spy/static/genome-spy.js").read_bytes(),
            )
        else:
            asset = (output / path.lstrip("/")).resolve()
            if asset.is_relative_to(output.resolve()) and asset.is_file():
                route.fulfill(
                    content_type=mimetypes.guess_type(asset.name)[0]
                    or "application/octet-stream",
                    body=asset.read_bytes(),
                )
            else:
                route.fulfill(status=404, body="Not found")

    page.route("http://guide.test/**", serve)
    page.goto("http://guide.test/")
    page.wait_for_function("window.guideApis?.filter(Boolean).length === 4")
    page.locator(".gs-doc-embed").first.scroll_into_view_if_needed()
    page.evaluate(
        "async () => {await document.fonts.ready; await new Promise(requestAnimationFrame);}"
    )


def test_linked_expression_means_histogram_and_clear(monkeypatch, page, tmp_path):
    sc = pytest.importorskip("scanpy")
    _render_furo_guide(page, monkeypatch, tmp_path)
    page.evaluate("window.api = guideApis[2]")
    size = page.evaluate("api.getLogicalCanvasSize()")
    assert size["width"] <= 736
    embed = page.locator(".gs-doc-embed").nth(2)
    assert embed.locator("select").count() == 0
    embed.scroll_into_view_if_needed()
    if page.viewport_size["width"] >= 1200:
        assert size["width"] <= embed.evaluate("el => el.clientWidth")
    assert size["height"] <= embed.bounding_box()["height"]
    assert embed.bounding_box()["height"] - size["height"] <= 16

    def rows(view):
        return page.evaluate(
            "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows",
            view,
        )

    assert rows("selected-expression") == []
    assert rows("selected-observation-histogram") == []
    assert rows("selected-composition") == []
    reference = rows("all-observation-histogram")
    composition_reference = rows("all-composition")
    assert sum(row["count"] for row in reference) == 700
    assert sum(row["percent"] for row in reference) == pytest.approx(100)

    # A real plot drag drives every consumer through the same native interval.
    bounds = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'umap-brush-cells'})"
    )
    heatmap_bounds = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'selected-expression'})"
    )
    histogram_bounds = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'all-observation-histogram'})"
    )
    assert heatmap_bounds["y"] > bounds["y"] + bounds["height"]
    assert heatmap_bounds["y"] > histogram_bounds["y"] + histogram_bounds["height"]
    assert histogram_bounds["x"] > bounds["x"] + bounds["width"]
    canvas = embed.locator("canvas").bounding_box()
    page.mouse.move(canvas["x"] + bounds["x"] + 5, canvas["y"] + bounds["y"] + 5)
    page.mouse.down()
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] * 0.5,
        canvas["y"] + bounds["y"] + bounds["height"] * 0.9,
        steps=12,
    )
    page.mouse.up()
    page.wait_for_function(
        "api.views.get({scope:[],view:'selected-expression'}).data.read({scope:'all',limit:100}).rows.length > 0"
    )
    selection = page.evaluate("api.params.get('cells').getValue().intervals")
    pbmc = sc.datasets.pbmc68k_reduced()
    x, y = pbmc.obsm["X_umap"].T
    mask = (
        (selection["x"][0] <= x)
        & (x < selection["x"][1])
        & (selection["y"][0] <= y)
        & (y < selection["y"][1])
    )
    assert 0 < mask.sum() < len(pbmc)
    genes = ["CD3D", "CD79A", "MS4A1", "NKG7", "LYZ", "FCER1A"]
    source = sc.get.obs_df(pbmc, keys=["bulk_labels", *genes], use_raw=False)
    expected = source.loc[mask].groupby("bulk_labels", observed=True)[genes].mean()
    actual = rows("selected-expression")
    assert len(actual) == len(expected) * len(genes)
    for row in actual:
        assert row["mean"] == pytest.approx(
            expected.loc[row["_group"], row["gene"]], abs=1e-6
        )
        assert row["cells"] == int(
            (source.loc[mask, "bulk_labels"] == row["_group"]).sum()
        )
    labels = value_texts(svg_root(page))
    assert len(labels) == len(actual)
    assert sorted(float(e.text.replace("−", "-")) for e in labels) == pytest.approx(
        sorted(row["mean"] for row in actual), abs=0.0051
    )

    selected_bins = rows("selected-observation-histogram")
    assert sum(row["count"] for row in selected_bins) == mask.sum()
    assert sum(row["percent"] for row in selected_bins) == pytest.approx(100)
    for bins, values in [
        (reference, pbmc.obs["S_score"].astype(float)),
        (selected_bins, pbmc.obs.loc[mask, "S_score"].astype(float)),
    ]:
        expected_bins = (np.floor(values.dropna() / 0.1) * 0.1).value_counts()
        assert len(bins) == len(expected_bins)
        for row in bins:
            assert row["bin_end"] == pytest.approx(row["bin_start"] + 0.1)
            assert row["count"] == expected_bins[row["bin_start"]]
            assert row["percent"] == pytest.approx(
                100 * expected_bins[row["bin_start"]] / values.notna().sum()
            )
    selected_composition = rows("selected-composition")
    expected_composition = pbmc.obs.loc[mask, "phase"].value_counts()
    assert sum(row["count"] for row in selected_composition) == mask.sum()
    for row in selected_composition:
        assert row["count"] == expected_composition[row["_obs_1"]]
        assert row["total"] == mask.sum()
        assert row["percent"] == pytest.approx(100 * row["count"] / mask.sum())
    assert rows("all-observation-histogram") == reference
    assert rows("all-composition") == composition_reference
    wrapper = embed.locator(".canvas-wrapper")
    assert wrapper.evaluate("el => getComputedStyle(el).overflowX") == "auto"
    assert (
        wrapper.bounding_box()["x"] + wrapper.bounding_box()["width"]
        <= page.viewport_size["width"]
    )
    assert embed.locator("canvas").bounding_box()["width"] == pytest.approx(
        size["width"]
    )
    wrapper.evaluate("el => {el.scrollLeft = el.scrollWidth - el.clientWidth;}")
    assert wrapper.evaluate(
        "el => el.querySelector('canvas').getBoundingClientRect().right <= el.getBoundingClientRect().right + 1"
    )

    page.screenshot(path=str(tmp_path / "linked-expression.png"), full_page=True)

    page.evaluate(
        "api.views.get({scope:[],view:'umap-brush-cells'}).params.getSelection('cells').clear()"
    )
    page.wait_for_function(
        "api.views.get({scope:[],view:'selected-expression'}).data.read({scope:'all',limit:100}).rows.length === 0"
    )
    assert rows("selected-observation-histogram") == []
    assert rows("selected-composition") == []
    assert rows("all-observation-histogram") == reference
    assert rows("all-composition") == composition_reference


@pytest.mark.parametrize("index", [1, 0])
def test_additional_layouts_keep_summaries_correct_and_brushes_independent(
    monkeypatch, page, tmp_path, index
):
    sc = pytest.importorskip("scanpy")
    _render_furo_guide(page, monkeypatch, tmp_path)
    page.evaluate("index => window.api = guideApis[index]", index)
    embed = page.locator(".gs-doc-embed").nth(index)
    embed.scroll_into_view_if_needed()
    size = page.evaluate("api.getLogicalCanvasSize()")
    assert size["width"] <= 736
    assert size["height"] <= embed.bounding_box()["height"]
    if index == 1:
        assert embed.bounding_box()["height"] - size["height"] <= 16
    assert embed.locator("select").count() == 0
    if page.viewport_size["width"] >= 1200:
        assert size["width"] <= embed.evaluate("el => el.clientWidth")
    wrapper = embed.locator(".canvas-wrapper")
    wrapper.evaluate("el => {el.scrollLeft = el.scrollWidth - el.clientWidth;}")
    assert wrapper.evaluate(
        "el => el.querySelector('canvas').getBoundingClientRect().right <= el.getBoundingClientRect().right + 1"
    )

    def rows(name):
        return page.evaluate(
            "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows",
            name,
        )

    def bounds(name):
        return page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})", name
        )

    embedding = bounds("umap-brush-cells")
    assert embedding["width"] == pytest.approx(embedding["height"], abs=0.1)
    kind = "expression" if index == 1 else "observation"
    suffix = "-0" if index == 1 else ""
    histogram = bounds(f"all-{kind}-histogram{suffix}")
    if index == 1:
        plots = [bounds(f"all-expression-histogram-{i}") for i in range(5)]
        assert all(p["x"] + p["width"] < embedding["x"] for p in plots[:2])
        assert plots[0]["y"] + plots[0]["height"] < plots[1]["y"]
        assert all(p["y"] > embedding["y"] + embedding["height"] for p in plots[2:])
        assert [p["y"] for p in plots[2:]] == pytest.approx([plots[2]["y"]] * 3)
        assert all(a["x"] + a["width"] < b["x"] for a, b in zip(plots[2:4], plots[3:]))
    else:
        heatmap = bounds("selected-expression")
        assert histogram["y"] + histogram["height"] < embedding["y"]
        assert heatmap["x"] > embedding["x"] + embedding["width"]

    references = {
        suffix: rows(f"all-{kind}-histogram{suffix}")
        for suffix in ([f"-{i}" for i in range(5)] if index == 1 else [""])
    }
    for suffix in references:
        assert rows(f"selected-{kind}-histogram{suffix}") == []
    pbmc = sc.datasets.pbmc68k_reduced()
    if index == 1:
        assert [e.text for e in svg_root(page).iter()].count("Distribution") == 1
        categories = set(pbmc.obs["bulk_labels"].cat.categories)
        labels = [e for e in svg_root(page).iter() if e.text in categories]
        assert {e.text for e in labels} == categories
        assert len(labels) == len(categories)
        for label in labels:
            x, y = position(label)
            assert 0 <= x < size["width"]
            assert 0 <= y < size["height"]
    x, y = pbmc.obsm["X_umap"].T
    intervals = {
        "x": np.quantile(x, [0.15, 0.65]).tolist(),
        "y": np.quantile(y, [0.1, 0.9]).tolist(),
    }
    mask = (
        (intervals["x"][0] <= x)
        & (x < intervals["x"][1])
        & (intervals["y"][0] <= y)
        & (y < intervals["y"][1])
    )
    page.evaluate(
        "intervals => api.params.get('cells').setValue({type:'interval',intervals})",
        intervals,
    )
    page.evaluate("() => new Promise(requestAnimationFrame)")
    assert 0 < mask.sum() < len(pbmc)
    assert rows("umap-count-cells")[0]["count"] == mask.sum()
    genes = ["LYZ", "CD3D", "MS4A1", "NKG7", "FCER1A"]
    expression = sc.get.obs_df(pbmc, keys=genes, use_raw=False)
    width = 0.5 if index == 1 else 100
    for suffix, reference in references.items():
        values = (
            expression[genes[int(suffix[1:])]].astype(float)
            if index == 1
            else pbmc.obs["n_genes"].astype(float)
        )
        for bins, cohort in [
            (reference, values),
            (rows(f"selected-{kind}-histogram{suffix}"), values.loc[mask]),
        ]:
            expected = (np.floor(cohort / width) * width).value_counts()
            assert len(bins) == len(expected)
            for row in bins:
                assert row["count"] == expected[row["bin_start"]]
                assert row["total"] == len(cohort)
                assert row["percent"] == pytest.approx(100 * row["count"] / len(cohort))
        assert rows(f"all-{kind}-histogram{suffix}") == reference
    if index == 0:
        genes = ["CD3D", "NKG7", "LYZ"]
        source = sc.get.obs_df(pbmc, keys=["phase", *genes], use_raw=False)
        expected = source.loc[mask].groupby("phase", observed=True)[genes].mean()
        actual = rows("selected-expression")
        assert len(actual) == len(expected) * len(genes)
        for row in actual:
            assert row["mean"] == pytest.approx(
                expected.loc[row["_group"], row["gene"]], abs=1e-6
            )
    for other in set(range(4)) - {index}:
        selection = page.evaluate(
            "index => guideApis[index].params.get('cells').getValue()", other
        )
        assert selection["intervals"] == {"x": None, "y": None}
    page.screenshot(path=str(tmp_path / f"linked-layout-{index}.png"), full_page=True)
    page.evaluate(
        "api.views.get({scope:[],view:'umap-brush-cells'}).params.getSelection('cells').clear()"
    )
    for suffix in references:
        assert rows(f"selected-{kind}-histogram{suffix}") == []
    if index == 0:
        assert rows("selected-expression") == []
    for suffix, reference in references.items():
        assert rows(f"all-{kind}-histogram{suffix}") == reference


def test_pbmc3k_tracks_follow_the_brush_without_moving_cells(
    monkeypatch, page, tmp_path
):
    sc = pytest.importorskip("scanpy")
    from anndata import read_h5ad

    _render_furo_guide(page, monkeypatch, tmp_path)
    page.evaluate("window.api = guideApis[3]")
    embed = page.locator(".gs-doc-embed").nth(3)
    embed.scroll_into_view_if_needed()
    size = page.evaluate("api.getLogicalCanvasSize()")
    assert size["width"] <= 736
    assert size["height"] <= embed.bounding_box()["height"]
    assert embed.locator("select").count() == 0
    wrapper = embed.locator(".canvas-wrapper")

    def rows(name):
        return page.evaluate(
            "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:3000}).rows",
            name,
        )

    pbmc = read_h5ad(ROOT / "tmp/scanpy-guide-data/linked-expression-pbmc3k.h5ad")
    assert pbmc.n_obs == 2638
    references = [rows(f"tracks-all-{i}") for i in range(5)]
    assert all(len(reference) == 2638 for reference in references)
    assert all(
        rows(f"tracks-selected-{i}") == reference
        for i, reference in enumerate(references)
    )
    assert sorted(row["_cell"] for row in references[0]) == list(range(2638))
    labels = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
    for category in pbmc.obs["louvain"].cat.categories:
        assert labels.count(category) == 1
    embedding = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'umap-brush-cells'})"
    )
    assert embedding["width"] == pytest.approx(embedding["height"])
    assert embedding["width"] == pytest.approx(480, abs=1)
    track = page.evaluate("api.views.getLayoutBounds({scope:[],view:'tracks-all-0'})")
    assert track["width"] == pytest.approx(embedding["width"], abs=1)
    assert track["x"] == pytest.approx(embedding["x"], abs=1)
    assert track["y"] > embedding["y"] + embedding["height"]
    wrapper.evaluate("(el, b) => {el.scrollLeft = Math.max(0, b.x - 35);}", embedding)
    canvas = embed.locator("canvas").bounding_box()
    page.mouse.move(
        canvas["x"] + embedding["x"] + 10, canvas["y"] + embedding["y"] + 20
    )
    page.keyboard.down("Shift")
    page.mouse.down()
    wrapper_box = wrapper.bounding_box()
    page.mouse.move(
        min(
            canvas["x"] + embedding["x"] + embedding["width"] * 0.8,
            wrapper_box["x"] + wrapper_box["width"] - 10,
        ),
        canvas["y"] + embedding["y"] + embedding["height"] * 0.8,
        steps=12,
    )
    page.mouse.up()
    page.keyboard.up("Shift")
    page.wait_for_function("api.params.get('cells').getValue().intervals.x !== null")
    intervals = page.evaluate("api.params.get('cells').getValue().intervals")
    x, y = pbmc.obsm["X_umap"].T
    mask = (
        (intervals["x"][0] <= x)
        & (x < intervals["x"][1])
        & (intervals["y"][0] <= y)
        & (y < intervals["y"][1])
    )
    assert 0 < mask.sum() < len(pbmc)
    assert rows("umap-count-cells")[0]["count"] == mask.sum()
    genes = ["CD3D", "MS4A1", "LYZ", "NKG7", "FCER1A"]
    source = sc.get.obs_df(pbmc, keys=genes, use_raw=True)
    selected = []
    for i, gene in enumerate(genes):
        actual = rows(f"tracks-selected-{i}")
        assert {row["_obs_id"] for row in actual} == set(pbmc.obs_names[mask])
        for row in actual:
            assert row[f"_expr_{i}"] == pytest.approx(source.loc[row["_obs_id"], gene])
        assert rows(f"tracks-all-{i}") == references[i]
        selected.append(actual)
    scale = "api.debug.getViewRoot().getDescendants().find(v => v.spec.name === 'tracks-all-0').getScaleResolution('x')"
    before = page.evaluate(f"{scale}.getDomain()")
    page.evaluate("""() => {
        window.embedding = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.name === 'umap-points');
        window.embeddingDomains = () => ['x','y'].map(c => embedding.getScaleResolution(c).getDomain());
    }""")
    embedding_domains = page.evaluate("embeddingDomains()")
    page.mouse.move(
        canvas["x"] + embedding["x"] + embedding["width"] * 0.3,
        canvas["y"] + embedding["y"] + embedding["height"] * 0.3,
    )
    page.mouse.wheel(0, -250)
    page.wait_for_function(
        "before => embeddingDomains().every((d,i) => d[1]-d[0] < before[i][1]-before[i][0])",
        arg=embedding_domains,
    )
    assert page.evaluate("api.params.get('cells').getValue().intervals") == intervals
    assert page.evaluate(f"{scale}.getDomain()") == before
    for i in range(5):
        assert rows(f"tracks-selected-{i}") == selected[i]
    wrapper.evaluate("el => {el.scrollLeft = 0;}")
    canvas = embed.locator("canvas").bounding_box()
    page.mouse.move(
        canvas["x"] + track["x"] + track["width"] * 0.3, canvas["y"] + track["y"] + 20
    )
    page.mouse.wheel(0, -300)
    page.wait_for_function(
        f"() => {{const d={scale}.getDomain(); return d[1]-d[0] < {np.ptp(before)} * .9;}}"
    )
    assert page.evaluate("api.params.get('cells').getValue().intervals") == intervals
    for i in range(5):
        assert rows(f"tracks-selected-{i}") == selected[i]
        assert rows(f"tracks-all-{i}") == references[i]
    for other in range(3):
        assert page.evaluate(
            "i => guideApis[i].params.get('cells').getValue().intervals", other
        ) == {"x": None, "y": None}
    page.screenshot(path=str(tmp_path / "linked-pbmc3k-tracks.png"), full_page=True)
    page.evaluate(
        "api.views.get({scope:[],view:'umap-brush-cells'}).params.getSelection('cells').clear()"
    )
    for i in range(5):
        assert rows(f"tracks-selected-{i}") == references[i]
