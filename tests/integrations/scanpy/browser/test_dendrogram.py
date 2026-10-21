"""Observed tree geometry, complete labels/guides, hover and offline delivery."""

from io import BytesIO
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
import genome_spy as gs
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.helpers import (
    leaf_marks,
    tree_paths,
    tree_segments,
    index_position,
)
from tests.integrations.scanpy.dendrogram_fixture import (
    make_tree_adata,
    tree_plot_cases,
)
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.clustermap_fixture import make_cluster_adata

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "dendrogram.json").read_text())


@pytest.mark.parametrize("family", ["dotplot", "matrixplot", "heatmap", "clustermap"])
@pytest.mark.parametrize("horizontal", [False, True])
def test_tree_height_fits_visible_branches_after_zoom(
    page, tmp_path, family, horizontal
):
    if family == "clustermap":
        chart = gsc.pl.clustermap(
            make_cluster_adata(), zoom="xy", width=360, height=300, show=False
        )
    else:
        chart = getattr(gsc.pl, family)(
            make_heatmap_adata(),
            ["g1", "g2"],
            "group",
            dendrogram=True,
            swap_axes=horizontal,
            zoom="xy",
            width=360,
            height=300,
            show=False,
        )
    spec = chart.to_dict()
    height_axis = "y" if horizontal else "x"
    tree = next(
        mark
        for mark in leaf_marks(spec)
        if mark.get("mark", {}).get("color") == "#555555"
        and mark["mark"]["orient"] == ("vertical" if horizontal else "horizontal")
    )
    # A test-only name exposes the native domain without changing production specs.
    tree["encoding"][height_axis]["scale"]["name"] = "test-tree-height"
    rows = spec["datasets"][tree["data"]["name"]]
    full_height = max(row["distance"] for row in rows)
    root_slot = next(row["leaf"] for row in rows if row["distance"] == full_height)
    edge = max(
        (row for row in rows if 0 < row["distance"] < full_height),
        key=lambda row: (abs(row["leaf"] - root_slot), row["leaf"]),
    )
    interval = [
        min(edge["leaf"], edge["leaf2"]) - 0.05,
        max(edge["leaf"], edge["leaf2"]) + 0.05,
    ]
    render(page, gs.TopLevelSpec.from_dict(spec))
    before = page.evaluate(
        "api.getScaleResolutionByName('test-tree-height').getDomain()"
    )
    slot_axis = "x" if horizontal else "y"
    # Native navigation targets a known subtree, independently of wheel speed/animation.
    page.evaluate(
        f"async domain => api.getScaleResolutionByName('{family}-{slot_axis}').zoomTo(domain)",
        interval,
    )
    slots = page.evaluate(
        f"api.getScaleResolutionByName('{family}-{slot_axis}').getDomain()"
    )
    visible_height = max(
        max(row["distance"], row["distance2"])
        for row in rows
        if all(slots[0] <= row[field] <= slots[1] for field in ("leaf", "leaf2"))
    )
    assert 0 < visible_height < full_height
    page.wait_for_function(
        "height => Math.abs(api.getScaleResolutionByName('test-tree-height').getDomain()[1] - height) < 1e-8",
        arg=visible_height * 1.05,
    )
    after = page.evaluate(
        "api.getScaleResolutionByName('test-tree-height').getDomain()"
    )
    page.screenshot(path=str(tmp_path / f"{family}-tree-zoom.png"))
    assert after[0] == pytest.approx(0)
    assert after[1] == pytest.approx(visible_height * 1.05)
    page.evaluate(f"api.getScaleResolutionByName('{family}-{slot_axis}').resetZoom()")
    page.wait_for_function(
        "Math.abs(api.getScaleResolutionByName('test-tree-height').getDomain()[1] - "
        + str(before[1])
        + ") < 1e-8"
    )


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", tree_plot_cases())
def test_registered_branches_and_complete_charts(
    page, tmp_path, reference_images, case
):
    reference = REFERENCE["charts"][case]
    family, options = tree_plot_cases()[case]
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        groupby="group",
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        show=False,
        **options,
    )
    if family in ("dotplot", "matrixplot"):
        chart = chart.properties(title="Grouped markers")
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for text in set(reference["x_labels"] + reference["y_labels"]):
        if text:
            assert f">{text}<" in svg
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    width, height = bounds["width"], bounds["height"]
    n = 4
    swapped = options.get("swap_axes", False)
    maximum = (
        max(
            (
                point[1 if swapped else 0]
                for path in reference["tree_paths"]
                for point in path
            ),
            default=1,
        )
        or 1
    )

    def project(point):
        x, y = point
        if family == "dendrogram":
            xd, yd = reference["x_domain"], reference["y_domain"]
            return left + (x - xd[0]) / (xd[1] - xd[0]) * width, top + (
                1 - (y - yd[0]) / (yd[1] - yd[0])
            ) * height
        if family == "correlation_matrix":
            return left - x / maximum * 180, top + height - y / n * height
        if swapped:
            pad = 0.3 if family == "dotplot" else 0
            return left + index_position(x, n, pad, width), top - y / (
                maximum * 1.05
            ) * 80
        pad = 0.5 if family == "dotplot" else 0
        return left + width + x / (maximum * 1.05) * 80, top + index_position(
            y, n, pad, height
        )

    for path in reference["tree_paths"]:
        for start, end in zip(path[:-1], path[1:], strict=True):
            for fraction in (0.25, 0.5, 0.75):
                point = np.array(start) + (np.array(end) - start) * fraction
                x, y = project(point)
                px, py = round(x * 1.5), round(y * 1.5)
                region = pixels[py - 3 : py + 4, px - 3 : px + 4].astype(int)
                assert region.size and np.any(np.abs(region - 85).max(axis=2) < 40), (
                    case,
                    point,
                )
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={"x": left, "y": top, "width": width, "height": height}
            )
        )
    ).convert("RGB")
    expected = Image.open(
        reference_images("dendrogram") / f"dendrogram-{case}-panel.png"
    ).convert("RGB")
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    if family in ("matrixplot", "correlation_matrix"):
        values = np.array(reference["values"])
        for row, column in np.ndindex(values.shape):
            # Stay clear of numeric labels and antialiased tile borders.
            x = round((column + 0.2) / values.shape[1] * actual.width)
            y = round((row + 0.2) / values.shape[0] * actual.height)
            np.testing.assert_allclose(
                np.asarray(actual)[y, x].astype(int),
                np.asarray(expected)[y, x].astype(int),
                atol=12,
            )
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    (tmp_path / f"{case}-complete.svg").write_text(svg)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("size", [(240, 180), (480, 300)])
def test_tree_alignment_survives_resizing_and_wheel(page, family, swapped, size):
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        ["g1", "g2"],
        "group",
        dendrogram=True,
        swap_axes=swapped,
        width=size[0],
        height=size[1],
        show=False,
    )
    bounds = render(page, chart)
    before = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(
        canvas["x"] + bounds["x"] + bounds["width"] / 2,
        canvas["y"] + bounds["y"] + bounds["height"] / 2,
    )
    page.mouse.wheel(0, -300)
    page.evaluate(
        "async () => { await new Promise(requestAnimationFrame); await new Promise(requestAnimationFrame); }"
    )
    assert (
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()") == before
    )
    # Leaves meet the plot edge at the same centers as summary marks.
    svg = tree_segments(
        ET.fromstring(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
    )
    assert len(svg) == 12
    points = np.array(svg).reshape(-1, 2)
    pad = (0.3 if swapped else 0.5) if family == "dotplot" else 0
    axis = 0 if swapped else 1
    targets = (np.arange(4) + 0.5 + pad) / (4 + 2 * pad) * bounds[
        "width" if swapped else "height"
    ] + bounds["x" if swapped else "y"]
    edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
    # SVG coordinates are rounded while layout bounds retain subpixel values.
    leaves = points[np.isclose(points[:, 1 - axis], edge, atol=0.5)]
    assert leaves.shape == (4, 2), (edge, points.tolist(), bounds)
    np.testing.assert_allclose(sorted(leaves[:, axis]), targets, atol=0.5)


def test_correlation_hover_palette_direction_and_offline_output(page, tmp_path):
    chart = gsc.pl.correlation_matrix(
        make_tree_adata(), "group", width=240, height=240, show=False
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    px = canvas["x"] + bounds["x"] + bounds["width"] / 8
    py = canvas["y"] + bounds["y"] + bounds["height"] * 7 / 8
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.get_by_text("Correlation", exact=True).wait_for(state="visible")
    assert (
        page.locator("table.attributes tr").last.locator("td").inner_text().strip()
        == "1.000"
    )
    pixel = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))[
        round(py), round(px)
    ]
    assert int(pixel[0]) > int(pixel[2]) + 80
    output = tmp_path / "correlation.html"
    chart.save(output, inline=True, controls=False)
    requests = []
    page.on(
        "request",
        lambda r: (
            requests.append(r.url) if r.url.startswith(("http:", "https:")) else None
        ),
    )
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not requests and not page.locator(".message-box").count()


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_attached_tree_keeps_summary_hover_aligned(page, family, swapped):
    chart = getattr(gsc.pl, family)(
        make_tree_adata(),
        ["g4"],
        "group",
        dendrogram=True,
        swap_axes=swapped,
        width=240,
        height=180,
        show=False,
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    columns, rows = (4, 1) if swapped else (1, 4)
    xpad, ypad = (0.3, 0.5) if family == "dotplot" else (0, 0)
    px = (
        canvas["x"]
        + bounds["x"]
        + (0.5 + xpad) / (columns + 2 * xpad) * bounds["width"]
    )
    py = canvas["y"] + bounds["y"] + (0.5 + ypad) / (rows + 2 * ypad) * bounds["height"]
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.get_by_text("Mean expression", exact=True).wait_for(state="visible")
    values = [
        row.locator("td").inner_text().strip()
        for row in page.locator("table.attributes tr").all()
    ]
    assert values[:3] == [
        "g4",
        REFERENCE["computations"]["default"]["categories_ordered"][0],
        "2.000",
    ]


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Core 1.2 SVG export moves straight-link control points twice; WebGL is unaffected.",
)
def test_native_straight_link_export_keeps_control_points_on_the_line(page):
    import re

    import genome_spy as gs

    chart = (
        gs.Chart([{"start": 0.2, "end": 0.8}])
        .mark_link(linkShape="line")
        .encode(
            x=gs.X("start:Q").scale(domain=[0, 1]).axis(None),
            x2=gs.X2("end:Q"),
            y=gs.value(0.5),
            y2=gs.value(0.5),
        )
        .properties(width=200, height=100)
    )
    render(page, chart)
    root = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    path = next(e for e in root.iter() if e.tag.endswith("path"))
    vertices = np.array(
        list(map(float, re.findall(r"[-+]?\d*\.?\d+", path.get("d"))))
    ).reshape(-1, 2)
    assert len(vertices) in (2, 4)
    assert np.max(np.abs(vertices[:, 1] - vertices[0, 1])) <= 0.2


@pytest.mark.parametrize("orientation", ["top", "bottom", "left", "right"])
@pytest.mark.parametrize("case", ["ties", "identical"])
def test_zero_height_merges_stay_native_and_connected(page, orientation, case):
    bounds = render(
        page,
        gsc.pl.dendrogram(
            make_tree_adata(case),
            "group",
            orientation=orientation,
            width=240,
            height=180,
            show=False,
        ),
    )
    paths = tree_paths(
        ET.fromstring(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
    )
    assert len(paths) == 6
    assert any(path[1] == path[2] for path in paths)
    if case == "identical":
        axis = 1 if orientation in ("top", "bottom") else 0
        start, extent = ("y", "height") if axis else ("x", "width")
        points = np.asarray(paths).reshape(-1, 2)
        np.testing.assert_allclose(
            points[:, axis], bounds[start] + bounds[extent] / 2, atol=0.6
        )
        assert np.ptp(points[:, 1 - axis]) > bounds["width" if axis else "height"] / 2


@pytest.mark.parametrize("horizontal", [False, True])
def test_zero_height_attached_tree_stays_at_matrix_edge(page, horizontal):
    chart = gsc.pl.matrixplot(
        make_tree_adata("identical"),
        ["g1", "g2"],
        "group",
        dendrogram=True,
        swap_axes=horizontal,
        zoom="xy",
        show=False,
        width=240,
        height=180,
    )
    bounds = render(page, chart)
    paths = tree_paths(
        ET.fromstring(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
    )
    assert len(paths) == 6
    axis = 1 if horizontal else 0
    edge = bounds["y"] if horizontal else bounds["x"] + bounds["width"]
    np.testing.assert_allclose(np.asarray(paths)[:, :, axis], edge, atol=0.6)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Core 1.2 centers zero in a viewport-derived [0, 0] height domain (C13).",
)
def test_native_zero_height_viewport_keeps_zero_at_leaf_edge(page):
    chart = (
        gs.Chart([{"a": 0, "b": 1, "h": 0, "k": 0}, {"a": 2, "b": 3, "h": 10, "k": 0}])
        .mark_link(linkShape="orthogonal", orient="vertical")
        .encode(
            x=gs.X("a:I", band=0.5).scale(domain=[0, 3], zoom=True, name="slots"),
            x2="b:I",
            y=gs.Y("h:Q").scale(
                domain=gs.ViewportDomainRef(source="viewport", mode="contain"),
                domainMin=0,
                zero=True,
                nice=False,
                name="height",
            ),
            y2="k:Q",
        )
    )
    render(page, chart)
    page.evaluate("async () => api.getScaleResolutionByName('slots').zoomTo([0, 1])")
    # Let native fitting settle without requiring the broken domain value.
    page.wait_for_timeout(700)
    assert page.evaluate("api.getScaleResolutionByName('height').getScale()(0)") == 0
