"""Observed native placement, missing values and scoped brush updates."""

from io import BytesIO
import re

import numpy as np
from PIL import Image, ImageColor
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.test_embedding_summary import adata as adata
from tests.integrations.scanpy.test_embedding_summary import (
    metadata_adata as metadata_adata,
)
from tests.integrations.scanpy.helpers import units, leaf_marks
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_grid_interactions import (
    svg_root,
    position,
    value_texts,
)


def render_summary(page, chart):
    spec = chart.to_dict()
    names = {view.get("name"): f"panel-{i}" for i, view in enumerate(units(spec))}
    for view in units(spec):
        for leaf in leaf_marks(view):
            if leaf.get("name"):
                names.setdefault(leaf["name"], leaf["name"])
    render(page, spec)
    return names


def rows(page, name):
    return page.evaluate(
        "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows",
        name,
    )


def set_brush(page, intervals):
    page.evaluate(
        "intervals => api.params.get('cells').setValue({type:'interval', intervals})",
        intervals,
    )
    page.evaluate("() => new Promise(requestAnimationFrame)")


@pytest.mark.parametrize("cmap", ["seurat", "viridis"])
def test_fitted_heatmap_values_follow_brush_means_contrast_and_clear(page, adata, cmap):
    adata.X[1, 0] = 1
    chart = (
        gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
        .add_heatmap(show_values=True, cmap=cmap, vmin=-1, vmax=2)
        .to_chart()
    )
    names = render_summary(page, chart)
    assert not value_texts(svg_root(page))
    set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
    labels = value_texts(svg_root(page))
    assert sorted(e.text for e in labels) == ["0.00", "1.17"]
    assert {e.text: e.get("fill") for e in labels} == {"0.00": "white", "1.17": "black"}
    means = rows(page, names["selected-expression"])
    assert all(row["gene"] == "HLA-DRA" for row in means)
    assert {row["_group"]: row["mean"] for row in means} == pytest.approx(
        {"A": 0, "B": 3.5 / 3}
    )
    set_brush(page, {"x": [-1, 1.5], "y": [-1, 0.5]})
    assert [e.text for e in value_texts(svg_root(page))] == ["0.00"]
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
        names["umap-brush-cells"],
    )
    assert not value_texts(svg_root(page))


@pytest.mark.parametrize("hidden", [False, True])
def test_panel_titles_render_custom_text_or_hide_without_fallback(
    page, metadata_adata, hidden
):
    titles = ["Cell map", "Marker means", "QC distribution", "Sample mix"]
    selected = [None] * 4 if hidden else titles
    chart = (
        gsc.pl.EmbeddingSummary(
            metadata_adata,
            "HLA-DRA",
            "type",
            obs_keys=["sample.label", "qc.score"],
            title=selected[0],
        )
        .add_heatmap(title=selected[1])
        .add_histogram(obs="qc.score", title=selected[2])
        .add_composition("sample.label", title=selected[3])
        .to_chart()
    )
    render_summary(page, chart)
    text = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
    for title in titles:
        assert (title in text) is not hidden
    assert not set(text).intersection(
        {
            "Selected cells: mean expression",
            "qc.score: selection vs all cells",
            "sample.label: composition",
        }
    )
    assert text.count("type") == 1  # The heatmap axis retains the grouping label.


def test_composition_and_numeric_metadata_match_source_and_keep_reference(
    page, metadata_adata
):
    chart = (
        gsc.pl.EmbeddingSummary(
            metadata_adata, "HLA-DRA", "type", obs_keys=["sample.label", "qc.score"]
        )
        .add_composition("sample.label")
        .add_histogram(obs="qc.score")
        .to_chart()
    )
    names = render_summary(page, chart)
    reference = rows(page, "all-composition")
    histogram = rows(page, "all-observation-histogram")
    assert {row["_obs_1"]: row["count"] for row in reference} == {
        "D1": 2,
        "D2": 2,
        "D3": 1,
        "NA": 1,
    }
    assert all(row["total"] == 6 for row in reference)
    assert sum(row["percent"] for row in reference) == pytest.approx(100)
    assert rows(page, "selected-composition") == []
    assert rows(page, "selected-observation-histogram") == []
    set_brush(page, {"x": [-0.1, 3.1], "y": [-0.1, 1.1]})
    selected = rows(page, "selected-composition")
    assert {row["_obs_1"]: row["count"] for row in selected} == {
        "D1": 2,
        "D2": 1,
        "NA": 1,
    }
    for row in selected:
        assert row["total"] == 4
        assert row["percent"] == pytest.approx(100 * row["count"] / 4)
    bins = rows(page, "selected-observation-histogram")
    assert {row["bin_start"]: row["count"] for row in bins} == {-0.5: 1, 0: 1, 0.5: 1}
    assert all(
        row["total"] == 3 and row["percent"] == pytest.approx(100 / 3) for row in bins
    )
    coverage = rows(page, names["selected-observation-coverage"])[0]
    assert (coverage["valid"], coverage["missing"]) == (3, 1)
    root = svg_root(page)
    labels = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert "Unused" in labels and "NA" in labels
    assert "Selected: 3 valid, 1 missing" in labels
    rectangles = [
        e
        for g in root.iter()
        if g.get("data-name") in ("all-composition", "selected-composition")
        for e in g.iter()
        if e.tag.endswith("rect")
    ]
    assert len(rectangles) == 7
    assert all(float(e.get("height")) > 0 for e in rectangles)
    cohort_rectangles = {
        name: [
            e
            for g in root.iter()
            if g.get("data-name") == name
            for e in g.iter()
            if e.tag.endswith("rect")
        ]
        for name in ("all-composition", "selected-composition")
    }
    for category in ("D1", "D2", "NA"):
        a = cohort_rectangles["all-composition"][
            next(i for i, row in enumerate(reference) if row["_obs_1"] == category)
        ]
        b = cohort_rectangles["selected-composition"][
            next(i for i, row in enumerate(selected) if row["_obs_1"] == category)
        ]
        assert abs(float(a.get("y")) - float(b.get("y"))) >= min(
            float(a.get("height")), float(b.get("height"))
        )
    set_brush(page, {"x": [20, 21], "y": [20, 21]})
    assert rows(page, "selected-composition") == []
    assert rows(page, "selected-observation-histogram") == []
    assert rows(page, names["selected-observation-coverage"]) == []
    assert rows(page, "all-composition") == reference
    assert rows(page, "all-observation-histogram") == histogram


def test_count_is_visible_inside_brush_and_moves_during_drag(page, adata):
    chart = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").to_chart()
    names = render_summary(page, chart)
    bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["umap-brush-cells"],
    )
    canvas = page.locator("canvas").first.bounding_box()
    origin = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
    before = rows(page, "umap-points")

    def label_geometry():
        root = svg_root(page)
        label = next(
            e
            for e in root.iter()
            if e.tag.endswith("text") and re.fullmatch(r"[\d,]+ cells", e.text or "")
        )
        rect = next(
            e
            for g in root.iter()
            if g.get("data-name") == "selectionRectRect"
            for e in g.iter()
            if e.tag.endswith("rect")
        )
        x, y = position(label)
        left, top = float(rect.get("x")), float(rect.get("y"))
        assert left < x < left + float(rect.get("width"))
        assert top < y < top + float(rect.get("height"))
        image = np.asarray(
            Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
                "RGB"
            )
        )
        region = image[int(y) : int(y) + 16, int(x) : int(x) + 65]
        assert np.sum(np.all(region < 80, axis=2)) > 5
        assert label.text == f"{rows(page, 'umap-count-cells')[0]['count']} cells"
        return x, y

    page.mouse.move(origin[0] + bounds["width"] * 0.5, origin[1] + 30)
    page.mouse.down()
    page.mouse.move(
        origin[0] + bounds["width"] - 10, origin[1] + bounds["height"] - 10, steps=6
    )
    first = label_geometry()
    page.mouse.move(origin[0] + 5, origin[1] + bounds["height"] - 10, steps=6)
    second = label_geometry()
    assert second[0] < first[0]
    assert rows(page, "umap-points") == before
    page.mouse.move(origin[0] + bounds["width"] * 0.5 + 2, origin[1] + 32)
    assert not any(
        e.tag.endswith("text") and re.fullmatch(r"[\d,]+ cells", e.text or "")
        for e in svg_root(page).iter()
    )
    page.mouse.up()
    set_brush(page, {"x": [0, 2], "y": [2.5, 3.5]})
    assert rows(page, "umap-count-cells")[0]["count"] == 0
    label_geometry()
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
        names["umap-brush-cells"],
    )
    assert not any(
        e.tag.endswith("text") and re.fullmatch(r"[\d,]+ cells", e.text or "")
        for e in svg_root(page).iter()
    )


@pytest.mark.parametrize("show_count", [False, True])
def test_show_count_changes_only_the_label_not_the_brush_or_histogram(
    page, adata, show_count
):
    chart = (
        gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", show_count=show_count)
        .add_tracks(width=250, height=80)
        .add_histogram()
        .to_chart()
    )
    names = render_summary(page, chart)
    points = rows(page, "umap-points")
    reference = rows(page, "all-expression-histogram")
    bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["umap-brush-cells"],
    )
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + bounds["x"] + 8, canvas["y"] + bounds["y"] + 8)
    page.mouse.down()
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] - 8,
        canvas["y"] + bounds["y"] + bounds["height"] - 8,
        steps=8,
    )
    page.mouse.up()
    intervals = page.evaluate("api.params.get('cells').getValue().intervals")
    assert intervals["x"] is not None
    labels = [
        e.text
        for e in svg_root(page).iter()
        if e.tag.endswith("text") and re.fullmatch(r"[\d,]+ cells", e.text or "")
    ]
    assert labels == (["6 cells"] if show_count else [])
    assert sum(row["count"] for row in rows(page, "selected-expression-histogram")) == 5
    assert {row["_obs_id"] for row in rows(page, "tracks-selected-0")} == {
        f"cell-{i}" for i in range(5)
    }
    assert rows(page, "umap-points") == points
    assert rows(page, "all-expression-histogram") == reference
    assert page.evaluate("api.params.get('cells').getValue().intervals") == intervals
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
        names["umap-brush-cells"],
    )
    assert rows(page, "selected-expression-histogram") == []


@pytest.mark.parametrize("side", ["left", "right", "top", "bottom"])
def test_real_brush_in_every_panel_position_and_unchanged_points(page, adata, side):
    chart = (
        gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
        .add_heatmap(position=side, height=360)
        .add_histogram("HLA-DRA", position=side)
        .style(umap_size=240)
        .legend(position=side)
        .to_chart()
    )
    names = render_summary(page, chart)
    bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["umap-brush-cells"],
    )
    assert bounds["width"] == pytest.approx(bounds["height"], abs=0.1)
    heatmap_bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["selected-expression"],
    )
    assert heatmap_bounds["width"] >= 300
    assert heatmap_bounds["height"] >= 360
    reference = rows(page, "all-expression-histogram")
    points_before = rows(page, "umap-points")
    assert rows(page, names["selected-expression"]) == []
    canvas = page.locator("canvas").first.bounding_box()
    x, y = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    page.mouse.move(x + 2, y + 2)
    page.mouse.down()
    page.mouse.move(x + bounds["width"] - 2, y + bounds["height"] - 2, steps=10)
    page.mouse.up()
    page.wait_for_function(
        "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows.length === 2",
        arg=names["selected-expression"],
    )
    actual = rows(page, names["selected-expression"])
    assert {row["gene"] for row in actual} == {"HLA-DRA"}
    assert {row["_group"]: row["cells"] for row in actual} == {"A": 2, "B": 3}
    assert {row["_group"]: row["mean"] for row in actual} == pytest.approx(
        {"A": -0.5, "B": 3.5 / 3}
    )
    assert rows(page, "all-expression-histogram") == reference
    assert rows(page, "umap-points") == points_before
    bins = rows(page, "selected-expression-histogram")
    assert {row["bin_start"]: row["count"] for row in bins} == {
        -1: 1,
        0: 1,
        0.5: 1,
        1: 1,
        2: 1,
    }
    assert all(row["percent"] == 20 for row in bins)
    count = rows(page, "umap-count-cells")
    assert count[0]["count"] == 6

    set_brush(page, {"x": [20, 21], "y": [20, 21]})
    assert rows(page, names["selected-expression"]) == []
    assert rows(page, "selected-expression-histogram") == []
    assert rows(page, "umap-count-cells")[0]["count"] == 0
    assert page.evaluate("api.params.get('cells').getValue().intervals.x") == [20, 21]
    set_brush(page, {"x": [1, 1], "y": [-1, 3]})
    assert rows(page, names["selected-expression"]) == []
    assert rows(page, "umap-count-cells")[0]["count"] == 0
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
        names["umap-brush-cells"],
    )
    assert page.evaluate("api.params.get('cells').getValue().intervals.x") is None
    assert rows(page, "all-expression-histogram") == reference


def test_all_missing_gene_has_no_heatmap_mean_or_histogram_zero_bin(page, adata):
    chart = (
        gsc.pl.EmbeddingSummary(adata, "missing.gene", "type")
        .add_heatmap()
        .add_histogram()
        .to_chart()
    )
    names = render_summary(page, chart)
    set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
    assert rows(page, "umap-count-cells")[0]["count"] == 6
    assert rows(page, names["selected-expression"]) == []
    assert rows(page, "selected-expression-histogram") == []
    assert rows(page, "all-expression-histogram") == []


def test_two_composed_builders_keep_independent_brush_values(page, adata):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_heatmap()
    first = plot.to_chart().properties(name="first")
    second = plot.to_chart().properties(name="second")
    spec = (
        gs.hconcat(first, second)
        .resolve_scale(x="independent", y="independent", color="independent")
        .to_dict()
    )
    views = units(spec)
    first_summary = next(
        i for i, v in enumerate(views) if v.get("name") == "selected-expression"
    )
    second_summary = max(
        i for i, v in enumerate(views) if v.get("name") == "selected-expression"
    )
    first_brush = next(
        i for i, v in enumerate(views) if v.get("name") == "umap-brush-cells"
    )
    render(page, spec)
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.get('cells').setValue({type:'interval',intervals:{x:[-1,6],y:[-1,3]}})",
        f"panel-{first_brush}",
    )
    page.wait_for_function(
        "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows.length === 2",
        arg=f"panel-{first_summary}",
    )
    assert rows(page, f"panel-{second_summary}") == []


@pytest.mark.xfail(
    strict=True,
    reason="Released Core interval filtering includes upper boundaries; count and selection_mask are half-open",
)
def test_exact_brush_boundary_matches_count_summary_and_python_mask(page, adata):
    chart = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_heatmap().to_chart()
    names = render_summary(page, chart)
    snapshot = {"type": "interval", "intervals": {"x": [0, 2], "y": [-1, 2]}}
    set_brush(page, snapshot["intervals"])
    expected = gsc.selection_mask(adata, snapshot)
    np.testing.assert_array_equal(expected, [True, True, False, False, False, False])
    assert rows(page, "umap-count-cells")[0]["count"] == expected.sum()
    summary = rows(page, names["selected-expression"])
    assert sum(row["cells"] for row in summary) == expected.sum()


@pytest.mark.parametrize("gene_controls", [False, True])
def test_multiple_histograms_and_optional_gene_controls_keep_the_shared_brush(
    page, adata, gene_controls
):
    adata.X[:, 1] = [-2, -1, 0, 1, 2, 3]
    chart = (
        gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
        .add_heatmap(gene_controls=gene_controls, show_values=True, vmin=-3, vmax=3)
        .add_histogram(
            ["HLA-DRA", "missing.gene"], gene_controls=gene_controls, height=80
        )
        .to_chart()
    )
    names = render_summary(page, chart)
    intervals = {"x": [-1, 1.5], "y": [-1, 0.5]}
    assert [e.text for e in svg_root(page).iter()].count("Distribution") == 1
    set_brush(page, intervals)
    assert sum(r["count"] for r in rows(page, "all-expression-histogram-0")) == 5
    assert sum(r["count"] for r in rows(page, "all-expression-histogram-1")) == 6
    assert {r["bin_start"] for r in rows(page, "selected-expression-histogram-0")} == {
        -1,
        0,
    }
    assert {r["bin_start"] for r in rows(page, "selected-expression-histogram-1")} == {
        -2,
        -1,
    }

    if not gene_controls:
        assert page.locator("select").count() == 0
        assert {
            r["gene"]: r["mean"] for r in rows(page, names["selected-expression"])
        } == pytest.approx({"HLA-DRA": -0.5, "missing.gene": -1.5})
        set_brush(page, {"x": None, "y": None})
        for i in range(2):
            assert rows(page, f"selected-expression-histogram-{i}") == []
        return

    page.get_by_label("Histogram gene 1", exact=True).select_option("missing.gene")
    page.get_by_label("Heatmap gene 1", exact=True).select_option("missing.gene")
    page.wait_for_function(
        "api.views.get({scope:[],view:'selected-expression-histogram-0'}).data.read({scope:'all',limit:100}).rows.every(r => r.variable === 'missing.gene')"
    )
    assert {r["bin_start"] for r in rows(page, "selected-expression-histogram-0")} == {
        -2,
        -1,
    }
    assert sum(r["count"] for r in rows(page, "all-expression-histogram-0")) == 6
    means = rows(page, names["selected-expression"])
    assert len(means) == 1
    assert means[0]["gene"] == "missing.gene"
    assert means[0]["mean"] == pytest.approx(-1.5)
    assert [float(e.text.replace("−", "-")) for e in value_texts(svg_root(page))] == [
        -1.5
    ]
    assert page.evaluate("api.params.get('cells').getValue().intervals") == intervals
    assert rows(page, "umap-count-cells")[0]["count"] == 2
    page.evaluate(
        "name => api.views.get({scope:[],view:name}).params.getSelection('cells').clear()",
        names["umap-brush-cells"],
    )
    assert rows(page, names["selected-expression"]) == []
    for i in range(2):
        assert rows(page, f"selected-expression-histogram-{i}") == []
        assert sum(r["count"] for r in rows(page, f"all-expression-histogram-{i}")) == 6


@pytest.mark.parametrize("show_values", [False, True])
@pytest.mark.xfail(
    strict=True,
    reason="Core 1.2 GPU categorical positions retain removed slots; upstream PR #595 is unreleased",
)
def test_heatmap_gene_changes_keep_rows_inside_the_plot(page, adata, show_values):
    adata.X[:, 1] = [-2, -1, 0, 1, 2, 3]
    chart = (
        gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
        .add_heatmap(gene_controls=True, show_values=show_values, height=160)
        .legend(position="bottom")
        .to_chart()
    )
    names = render_summary(page, chart)
    set_brush(page, {"x": [-1, 6], "y": [-1, 3]})
    bounds = page.evaluate(
        "name => api.views.getLayoutBounds({scope:[],view:name})",
        names["selected-expression"],
    )
    for choice in ["HLA-DRA", "missing.gene", "HLA-DRA", "missing.gene"]:
        page.get_by_label("Heatmap gene 1", exact=True).select_option(choice)
        page.evaluate("() => new Promise(requestAnimationFrame)")
        expected = {"missing.gene", choice}
        actual = rows(page, names["selected-expression"])
        assert len(actual) == 2 * len(expected)
        assert {row["gene"] for row in actual} == expected
        root = svg_root(page)
        rectangles = [
            element
            for group in root.iter()
            if group.get("data-name") == names["selected-expression"]
            for element in group.iter()
            if element.tag.endswith("rect")
        ]
        assert len(rectangles) == len(actual)
        image = Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
            "RGB"
        )
        for rect in rectangles:
            assert float(rect.get("y")) >= bounds["y"] - 0.25
            assert float(rect.get("y")) + float(rect.get("height")) <= (
                bounds["y"] + bounds["height"] + 0.25
            )
            x = float(rect.get("x")) + float(rect.get("width")) * 0.25
            y = float(rect.get("y")) + float(rect.get("height")) * 0.25
            np.testing.assert_allclose(
                image.getpixel((int(x), int(y))),
                ImageColor.getrgb(rect.get("fill")),
                atol=2,
            )
