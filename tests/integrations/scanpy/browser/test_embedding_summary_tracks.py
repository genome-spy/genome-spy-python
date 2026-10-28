"""Observe linked cell identity, native track opacity and independent navigation."""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    render_summary,
    rows,
    set_brush,
    svg_root,
)
from tests.integrations.scanpy.fixture_support import adata as adata


@pytest.mark.smoke
@pytest.mark.parametrize("page", [1, 1.5], indirect=True)
def test_brush_dims_tracks_by_cell_identity_and_survives_zoom_and_clear(page, adata):
    adata.X[:, 1] = [1, 2, 3, 4, 5, 6]
    chart = (
        gsc.pl.EmbeddingSummary(
            adata,
            ["HLA-DRA", "missing.gene"],
            "type",
            categories_order=["B", "A"],
            palette={"A": "#1f77b4", "B": "#ff7f0e"},
        )
        .add_tracks(["missing.gene", "HLA-DRA"], width=480, height=180, group_gap=4)
        .style(umap_size=240)
        .to_chart()
    )
    names = render_summary(page, chart)
    reference = rows(page, "tracks-all-0")
    assert [row["_obs_id"] for row in reference] == [
        f"cell-{i}" for i in (2, 3, 4, 0, 1, 5)
    ]
    assert [row["_cell"] for row in reference] == list(range(6))
    assert rows(page, "tracks-selected-0") == reference
    points = rows(page, "umap-points")
    intervals = {"x": [-0.5, 1.5], "y": [-0.5, 0.5]}
    set_brush(page, intervals)
    for slot in (0, 1):
        assert {row["_obs_id"] for row in rows(page, f"tracks-selected-{slot}")} == {
            "cell-0",
            "cell-1",
        }
    assert rows(page, "umap-count-cells")[0]["count"] == 2
    assert rows(page, "tracks-all-0") == reference
    assert rows(page, "umap-points") == points

    root = svg_root(page)
    rectangles = next(
        group for group in root.iter() if group.get("data-name") == "tracks-all-0"
    )
    rectangles = [
        element for element in rectangles.iter() if element.tag.endswith("rect")
    ]
    assert len(rectangles) == 6
    image = Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
        "RGB"
    )
    dpr = page.evaluate("devicePixelRatio")
    for row, rect in zip(reference, rectangles, strict=True):
        x = float(rect.get("x")) + float(rect.get("width")) * 0.25
        y = float(rect.get("y")) + float(rect.get("height")) * 0.25
        color = np.array([31, 119, 180] if row["_group"] == "A" else [255, 127, 14])
        if row["_obs_id"] not in ("cell-0", "cell-1"):
            color = color * 0.15 + 255 * 0.85
        np.testing.assert_allclose(
            image.getpixel((int(x * dpr), int(y * dpr))), color, atol=2
        )

    selected = rows(page, "tracks-selected-0")
    probe = rectangles[3]
    hover_at(page, float(probe.get("x")) + 20, float(probe.get("y")) + 5)
    assert "cell-0" in page.locator("table.attributes").inner_text()
    assert "missing.gene expression" in page.locator("table.attributes").inner_text()
    track = page.evaluate("api.views.getLayoutBounds({scope:[],view:'tracks-all-0'})")
    canvas = page.locator("canvas").first.bounding_box()
    scale = "api.debug.getViewRoot().getDescendants().find(v => v.spec.name === 'tracks-all-0').getScaleResolution('x')"
    before = page.evaluate(f"{scale}.getDomain()")
    embedding_bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["umap-brush-cells"],
    )
    page.mouse.move(
        canvas["x"] + track["x"] + track["width"] / 2, canvas["y"] + track["y"] + 30
    )
    page.mouse.wheel(0, -350)
    page.wait_for_function(
        f"() => {{ const d={scale}.getDomain(); return d[1]-d[0] < {np.ptp(before)} * .9; }}"
    )
    assert rows(page, "tracks-selected-0") == selected
    assert rows(page, "tracks-all-0") == reference
    assert page.evaluate("api.params.get('cells').getValue().intervals") == intervals
    assert page.evaluate(
        """name => {
        const views=api.debug.getViewRoot().getDescendants();
        const tracks=views.filter(v=>v.spec.name?.startsWith('tracks-'));
        const strip=views.find(v=>v.spec.name===name);
        return {count:tracks.length, shared:tracks.every(v=>v.getScaleResolution('x')===strip.getScaleResolution('x'))};
    }""",
        names["heatmap-category-strip"],
    ) == {"count": 4, "shared": True}
    assert (
        page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-brush-cells"],
        )
        == embedding_bounds
    )
    set_brush(page, {"x": [20, 21], "y": [20, 21]})
    assert rows(page, "tracks-selected-0") == []
    assert rows(page, "tracks-all-0") == reference
    set_brush(page, {"x": None, "y": None})
    assert rows(page, "tracks-selected-0") == reference


@pytest.mark.parametrize("show_count", [False, True])
def test_embedding_zoom_pan_and_shift_brush_keep_linked_cells(page, adata, show_count):
    chart = (
        gsc.pl.EmbeddingSummary(
            adata, "HLA-DRA", "type", zoom=True, show_count=show_count
        )
        .add_tracks(width=320, height=100)
        .add_histogram(width=180, height=100)
        .style(umap_size=240)
        .to_chart()
    )
    names = render_summary(page, chart)
    bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'umap-points'})")
    canvas = page.locator("canvas").first.bounding_box()
    page.evaluate("""() => {
        window.embedding = api.debug.getViewRoot().getDescendants()
            .find(v => v.spec.name === 'umap-points');
        window.domains = () => ['x','y'].map(c => embedding.getScaleResolution(c).getDomain());
    }""")
    original = rows(page, "umap-points")
    track_scale = "api.debug.getViewRoot().getDescendants().find(v => v.spec.name === 'tracks-all-0').getScaleResolution('x')"
    track_domain = page.evaluate(f"{track_scale}.getDomain()")

    def pointer(x, y):
        position = (
            canvas["x"] + bounds["x"] + x * bounds["width"],
            canvas["y"] + bounds["y"] + y * bounds["height"],
        )
        page.mouse.move(*position)
        return position

    def select(x, y, x2, y2):
        pointer(x, y)
        page.keyboard.down("Shift")
        page.mouse.down()
        pointer(x2, y2)
        page.mouse.up()
        page.keyboard.up("Shift")
        snapshot = page.evaluate("api.params.get('cells').getValue()")
        mask = gsc.selection_mask(adata, snapshot)
        assert 0 < mask.sum() < len(adata)
        valid = mask & np.isfinite(adata.X[:, 0])
        assert {row["_obs_id"] for row in rows(page, "tracks-selected-0")} == set(
            adata.obs_names[valid]
        )
        assert (
            sum(row["count"] for row in rows(page, "selected-expression-histogram"))
            == valid.sum()
        )
        if show_count:
            assert rows(page, "umap-count-cells")[0]["count"] == mask.sum()
        return snapshot

    before = page.evaluate("domains()")
    selection = select(0.1, 0.3, 0.45, 0.8)
    assert page.evaluate("domains()") == before
    selected = rows(page, "tracks-selected-0")
    pointer(0.85, 0.15)
    page.mouse.wheel(0, -350)
    page.wait_for_function(
        "before => domains().every((d,i) => d[1]-d[0] < before[i][1]-before[i][0])",
        arg=before,
    )
    page.wait_for_timeout(300)
    zoomed = page.evaluate("domains()")
    assert np.ptp(zoomed[0]) == pytest.approx(np.ptp(zoomed[1]))
    assert page.evaluate("api.params.get('cells').getValue()") == selection
    assert rows(page, "tracks-selected-0") == selected
    assert page.evaluate(f"{track_scale}.getDomain()") == track_domain

    pointer(0.85, 0.1)
    page.mouse.down()
    pointer(0.9, 0.15)
    page.mouse.up()
    page.wait_for_function(
        "before => domains().every((d,i) => Math.abs(d[0]-before[i][0]) > 0.01)",
        arg=zoomed,
    )
    panned = page.evaluate("domains()")
    assert np.ptp(panned[0]) == pytest.approx(np.ptp(panned[1]))
    assert page.evaluate("api.params.get('cells').getValue()") == selection
    assert rows(page, "tracks-selected-0") == selected
    assert rows(page, "umap-points") == original
    page.mouse.dblclick(*pointer(0.85, 0.85))
    assert page.evaluate("api.params.get('cells').getValue().intervals.x") is None
    select(0.1, 0.1, 0.8, 0.8)
    assert page.evaluate(f"{track_scale}.getDomain()") == track_domain
    assert (
        page.evaluate(
            "name => api.views.getLayoutBounds({scope:[],view:name})",
            names["umap-points"],
        )
        == bounds
    )
