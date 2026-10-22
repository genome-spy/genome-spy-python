"""Registered native PAGA graph paint, labels, hover, navigation and HTML delivery."""

from io import BytesIO
import warnings

import numpy as np
from PIL import Image
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import svg_root
from tests.integrations.scanpy.browser.test_timeseries import point_coordinates
from tests.integrations.scanpy.paga_fixture import POSITIONS, make_paga, paga_cases
from tests.integrations.scanpy.helpers import leaf_marks


@pytest.mark.parametrize(
    "case",
    ["default", "supplied", "dashed", "sizing", "aliases", "empty", "asymmetric_csc"],
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_native_graph_matches_scanpy_paint_and_labels(page, tmp_path, case):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.collections import PathCollection, LineCollection
    import scanpy as sc

    adata, options = make_paga(case), paga_cases()[case]
    with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax = sc.pl.paga(adata, show=False, **options)
        fig = ax.figure
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        point = next(c for c in ax.collections if isinstance(c, PathCollection))
        xy, areas, colors = (
            point.get_offsets(),
            point.get_sizes(),
            point.get_facecolors(),
        )
        expected_lines = [c for c in ax.collections if isinstance(c, LineCollection)]
        domains = [ax.get_xlim(), ax.get_ylim()]
        labels = [t.get_text() for t in ax.texts]
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        full = Image.open(reference).convert("RGB")
        expected = full.crop(
            (
                round(bbox.x0 * 1.5),
                round(full.height - bbox.y1 * 1.5),
                round(bbox.x1 * 1.5),
                round(full.height - bbox.y0 * 1.5),
            )
        )
        plt.close(fig)
    chart = gsc.pl.paga(
        make_paga(case), width=bbox.width, height=bbox.height, show=False, **options
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.5)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.5)
    root = svg_root(page)
    (tmp_path / "native.svg").write_text(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    texts = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert set(labels) <= set(texts)
    if "title" in options:
        assert options["title"] in texts
    centers = point_coordinates(page)[0]
    expected_centers = np.column_stack(
        [
            bounds["x"]
            + (xy[:, 0] - domains[0][0]) / np.ptp(domains[0]) * bounds["width"],
            bounds["y"]
            + (1 - (xy[:, 1] - domains[1][0]) / np.ptp(domains[1])) * bounds["height"],
        ]
    )
    np.testing.assert_allclose(centers, expected_centers, atol=0.06)
    rules = [
        e
        for e in root.iter()
        if e.get("data-mark-type") == "rule" and e.get("clip-path")
    ]
    assert len(rules) == len(expected_lines)
    for group, reference_line in zip(rules, expected_lines, strict=True):
        assert len(group) == len(reference_line.get_segments())
        for line, width in zip(group, reference_line.get_linewidths(), strict=True):
            assert float(
                line.get("stroke-width", group.get("stroke-width", "1"))
            ) == pytest.approx(width * 100 / 72, abs=0.051)
    canvas = page.locator("canvas").first.bounding_box()
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": canvas["x"] + bounds["x"],
                    "y": canvas["y"] + bounds["y"],
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    pixels, target = (
        np.asarray(actual).astype(float),
        np.asarray(expected).astype(float),
    )
    for center, area, color in zip(centers, areas, colors, strict=True):
        x, y = (center - [bounds["x"], bounds["y"]]) * 1.5
        radius = int((np.sqrt(area) / 2 + 2) * 100 / 72 * 1.5) + 2
        a = pixels[
            round(y) - radius : round(y) + radius + 1,
            round(x) - radius : round(x) + radius + 1,
        ]
        b = target[
            round(y) - radius : round(y) + radius + 1,
            round(x) - radius : round(x) + radius + 1,
        ]
        # Count colored paint separately from the black labels and graph edges.
        paint_a = np.argwhere(np.linalg.norm(a - color[:3] * 255, axis=2) < 40)
        paint_b = np.argwhere(np.linalg.norm(b - color[:3] * 255, axis=2) < 40)
        assert len(paint_a) > 20 and len(paint_b) > 20
        # Fonts cover different parts of small nodes; measure the surviving outer radius.
        radius_a = np.linalg.norm(paint_a - radius, axis=1).max()
        radius_b = np.linalg.norm(paint_b - radius, axis=1).max()
        assert radius_a == pytest.approx(radius_b, abs=2)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "registered-overlay.png"
    )
    page.screenshot(path=str(tmp_path / "complete.png"), full_page=True)


def test_group_and_edge_hover_navigation_and_offline_html(page, tmp_path):
    chart = gsc.pl.paga(
        make_paga(), pos=POSITIONS, zoom=True, width=500, height=350, show=False
    )
    bounds = render(page, chart)
    centers = point_coordinates(page)[0]
    point = next(m for m in leaf_marks(chart.to_dict()) if m["mark"]["type"] == "point")
    dx, dy = [point["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
    # Native viewport culling may sort exported circles; project known group coordinates instead.
    projected = np.column_stack(
        [
            bounds["x"] + (POSITIONS[:, 0] - dx[0]) / np.ptp(dx) * bounds["width"],
            bounds["y"]
            + (1 - (POSITIONS[:, 1] - dy[0]) / np.ptp(dy)) * bounds["height"],
        ]
    )
    hover_at(page, *projected[0])
    page.locator("table.attributes").wait_for(state="visible")
    assert [
        t.strip() for t in page.locator("table.attributes td").all_text_contents()
    ] == ["A", "A", "9"]
    # B--C is a visible, isolated stored edge whose midpoint is outside either node.
    hover_at(page, *(projected[1] + projected[2]) / 2)
    page.locator("table.attributes").get_by_text("Connectivity", exact=True).wait_for(
        state="visible"
    )
    assert float(page.locator("table.attributes td").last.inner_text()) == 0.5
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + bounds["x"] + 250, canvas["y"] + bounds["y"] + 175)
    page.mouse.wheel(0, -10)
    page.wait_for_timeout(700)
    zoomed = point_coordinates(page)[0]
    assert all(np.ptp(zoomed[:, i]) > np.ptp(centers[:, i]) for i in (0, 1))
    canvas = page.locator("canvas").first.bounding_box()
    x, y = canvas["x"] + bounds["x"] + 250, canvas["y"] + bounds["y"] + 175
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + 20, y + 15, steps=5)
    page.mouse.up()
    page.wait_for_timeout(500)
    assert not np.array_equal(point_coordinates(page)[0], zoomed)
    # Ordinary composition must not create duplicate global scale names.
    combined = gs.hconcat(chart, chart).resolve_scale(default="independent")
    render(page, combined)
    assert len(point_coordinates(page)) == 2
    path = tmp_path / "paga.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


def test_zero_node_size_keeps_labels_without_point_paint(page):
    chart = gsc.pl.paga(make_paga(), pos=POSITIONS, node_size_scale=0, show=False)
    render(page, chart)
    assert not point_coordinates(page)
    texts = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
    assert set("ABCD") <= set(texts)


def test_disabled_hover_does_not_show_node_tooltips(page):
    render(page, gsc.pl.paga(make_paga(), pos=POSITIONS, hover=False, show=False))
    hover_at(page, *point_coordinates(page)[0][0])
    assert not page.locator("table.attributes").count()
