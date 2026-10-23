"""Registered adjacency tiles/tree points and observed native matrix interactions."""

from io import BytesIO

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import svg_root, pointer
from tests.integrations.scanpy.browser.test_timeseries import point_coordinates
from tests.integrations.scanpy.paga_fixture import make_adjacency


@pytest.mark.parametrize(
    "case", ["default", "empty_tree", "missing", "constant", "singleton"]
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_registered_complete_chart_matches_scanpy(page, tmp_path, case):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_adjacency(case=case)
    plt.close("all")
    with mpl.rc_context({"figure.dpi": 100}):
        sc.pl.paga_adjacency(a, color_map="viridis", show=False)
        fig = plt.gcf()
        ax = fig.axes[0]
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        points = np.concatenate([c.get_offsets() for c in ax.collections])
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
    chart = gsc.pl.paga_adjacency(a, width=bbox.width, height=bbox.height, show=False)
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.5)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.5)
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
    assert abs(actual.width - expected.width) <= 2
    assert abs(actual.height - expected.height) <= 2
    pixels, target = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    count = a.uns["connectivities"].shape[0]
    for row, col in np.ndindex(count, count):
        for fraction in (0.25, 0.75):
            x, y = (col + fraction) / count, (row + fraction) / count
            np.testing.assert_allclose(
                pixels[int(y * actual.height), int(x * actual.width)],
                target[int(y * expected.height), int(x * expected.width)],
                atol=12,
            )
    point_groups = point_coordinates(page)
    assert len(point_groups) == bool(len(points))
    centers = point_groups[0] if len(points) else []
    expected_centers = [
        (
            bounds["x"] + (x + 0.5) / count * bounds["width"],
            bounds["y"] + (y + 0.5) / count * bounds["height"],
        )
        for x, y in points
    ]
    np.testing.assert_allclose(
        np.asarray(centers).reshape(-1, 2),
        np.asarray(expected_centers).reshape(-1, 2),
        atol=0.6,
    )
    for x, y in points:
        sizes = []
        for image in (actual, expected):
            cx, cy = (
                int((x + 0.5) / count * image.width),
                int((y + 0.5) / count * image.height),
            )
            patch = np.asarray(image)[cy - 5 : cy + 6, cx - 5 : cx + 6]
            sizes.append(np.count_nonzero((patch < 40).all(axis=2)))
        assert sizes[0] > 0 and sizes[1] > 0
        assert abs(sizes[0] - sizes[1]) <= 8
    root = svg_root(page)
    gradients = [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
    ]
    assert len(gradients) == 1
    assert float(gradients[0].get("height")) == pytest.approx(
        bounds["height"] * 0.5, abs=2
    )
    labels = {e.text for e in root.iter() if e.tag.endswith("text")}
    assert {str(i) for i in range(count)} <= labels
    page.screenshot(path=str(tmp_path / "native-complete.png"), full_page=True)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "registered-overlay.png"
    )


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_tree_points_follow_matrix_zoom_pan_with_hover_and_values(page, tmp_path, zoom):
    chart = gsc.pl.paga_adjacency(
        make_adjacency(), zoom=zoom, show_values=True, width=360, height=360, show=False
    )
    bounds = render(page, chart)
    xname, yname = "paga_adjacency-x", "paga_adjacency-y"
    xbefore = page.evaluate(
        "name=>api.getScaleResolutionByName(name).getDomain()", xname
    )
    ybefore = page.evaluate(
        "name=>api.getScaleResolutionByName(name).getDomain()", yname
    )
    canvas = page.locator("canvas").first.bounding_box()
    # A tree point at (x=0,y=2) is deliberately transposed from matrix row zero.
    hover_at(
        page,
        canvas["x"] + bounds["x"] + bounds["width"] / 6,
        canvas["y"] + bounds["y"] + bounds["height"] * 5 / 6,
    )
    table = page.locator("table.attributes")
    assert table.get_by_text("Source group", exact=True).is_visible()
    assert [
        r.locator("td").inner_text().strip() for r in table.locator("tr").all()
    ] == ["0", "2"]
    hover_at(
        page,
        canvas["x"] + bounds["x"] + bounds["width"] * 5 / 6,
        canvas["y"] + bounds["y"] + bounds["height"] / 6,
    )
    values = [r.locator("td").inner_text().strip() for r in table.locator("tr").all()]
    assert values[:2] == ["0", "2"]
    assert float(values[2]) == pytest.approx(0.6)
    before_points = point_coordinates(page)[0]
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -180)
    page.wait_for_timeout(250)
    page.mouse.down()
    page.mouse.move(px + 12, py + 12, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    assert (
        page.evaluate("name=>api.getScaleResolutionByName(name).getDomain()", xname)
        != xbefore
    ) is (zoom == "xy")
    assert (
        page.evaluate("name=>api.getScaleResolutionByName(name).getDomain()", yname)
        != ybefore
    )
    after_points = point_coordinates(page)[0]
    assert not np.array_equal(after_points, before_points)
    projected = page.evaluate(
        """()=>{const x=api.getScaleResolutionByName('paga_adjacency-x').getScale();
        const y=api.getScaleResolutionByName('paga_adjacency-y').getScale();
        return [[0,2],[1,0]].map(([a,b])=>[
            x(a)+x.bandwidth()/2, 1-y(b)+y.bandwidth()/2]);}"""
    )
    projected = np.asarray(projected)
    # Native culling omits point centers outside the zoomed viewport.
    visible = ((projected >= 0) & (projected <= 1)).all(axis=1)
    expected = projected[visible] * [bounds["width"], bounds["height"]]
    expected += [bounds["x"], bounds["y"]]
    np.testing.assert_allclose(after_points, expected, atol=0.6)
    root = svg_root(page)
    assert any(e.tag.endswith("text") and e.text == "0.20" for e in root.iter())
    output = tmp_path / "paga-adjacency.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


def test_hover_false_disables_matrix_and_tree_tooltips(page):
    bounds = render(
        page, gsc.pl.paga_adjacency(make_adjacency(), hover=False, show=False)
    )
    canvas = page.locator("canvas").first.bounding_box()
    for x, y in [(1 / 6, 5 / 6), (0.5, 1 / 6)]:
        hover_at(
            page,
            canvas["x"] + bounds["x"] + x * bounds["width"],
            canvas["y"] + bounds["y"] + y * bounds["height"],
        )
        assert not page.locator("table.attributes").is_visible()
