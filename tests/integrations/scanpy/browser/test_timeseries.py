"""Native time-series point footprints, guides, hover, zoom and offline delivery."""

from io import BytesIO
import warnings
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import svg_root
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.timeseries_fixture import timeseries_cases


@pytest.mark.parametrize("case", timeseries_cases())
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_time_series_native_points_and_guides(page, tmp_path, case):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    values, options = timeseries_cases()[case]
    with (
        mpl.rc_context({"figure.dpi": 100, "font.size": 10}),
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore")
        sc.pl.timeseries(values, **options)
        fig, ax = plt.gcf(), plt.gcf().axes[0]
        # Fixed plot dimensions register the renderer's pixels independently of outer fonts.
        fig.set_size_inches(6, 4)
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        expected = Image.open(reference).convert("RGB")
        expected = expected.crop(
            (
                round(bbox.x0 * 1.5),
                round(expected.height - bbox.y1 * 1.5),
                round(bbox.x1 * 1.5),
                round(expected.height - bbox.y0 * 1.5),
            )
        )
        xy = np.ma.concatenate([c.get_offsets() for c in ax.collections])
        visible = ~np.ma.getmaskarray(xy).any(axis=1)
        xy = np.asarray(xy)[visible]
        domains = [ax.get_xlim(), ax.get_ylim()]
        labels = (
            [t.get_text() for t in ax.get_legend().texts] if ax.get_legend() else []
        )
        plt.close(fig)
    chart = gsc.pl.timeseries(
        values, width=bbox.width, height=bbox.height, show=False, **options
    )
    bounds = render(page, chart)
    root = svg_root(page)
    ET.ElementTree(root).write(tmp_path / "native.svg", encoding="unicode")
    point_groups = [
        e
        for e in root.iter()
        if e.get("data-mark-type") == "point" and e.get("clip-path")
    ]
    assert len(point_groups) == 1 and len(point_groups[0]) == len(xy)
    if case == "masked_legend_key":
        keys = [
            e
            for e in root.iter()
            if e.get("data-mark-type") == "point" and not e.get("clip-path")
        ]
        assert len(keys) == 1
        assert keys[0].get("fill-opacity") == keys[0].get("stroke-opacity") == "0"
    texts = [e.text for e in root.iter() if e.tag.endswith("text")]
    for label in labels + [
        options.get("xlabel", ""),
        options.get("ylabel", "gene expression"),
    ]:
        if label:
            assert label in texts
    # The numeric-color mode has a series key, never an invented gradient guide.
    assert not [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
    ]
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
    target, pixels = np.asarray(expected).astype(int), np.asarray(actual).astype(int)
    for time, value in xy:
        x = (time - domains[0][0]) / (domains[0][1] - domains[0][0])
        y = 1 - (value - domains[1][0]) / (domains[1][1] - domains[1][0])
        if not (0.02 < x < 0.98 and 0.02 < y < 0.98):
            continue
        # Compare local paint areas as well as centers to catch incorrect marker sizes.
        xp, yp = int(x * actual.width), int(y * actual.height)
        xq, yq = int(x * expected.width), int(y * expected.height)
        a = pixels[yp - 5 : yp + 6, xp - 5 : xp + 6]
        b = target[yq - 5 : yq + 6, xq - 5 : xq + 6]
        assert (
            abs(
                np.count_nonzero(np.min(a, axis=2) < 220)
                - np.count_nonzero(np.min(b, axis=2) < 220)
            )
            <= 15
        )
        assert np.min(np.linalg.norm(a.reshape(-1, 3) - b[5, 5], axis=1)) < 35
    actual.save(tmp_path / "native-panel.png")
    expected.save(tmp_path / "reference-panel.png")
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


def test_hover_and_both_native_axes_navigate_and_export_offline(page, tmp_path):
    values = np.arange(60, dtype=float).reshape(30, 2)
    chart = gsc.pl.timeseries(
        values,
        var_names=["A", "B"],
        time=np.arange(30) * 2,
        marker="o",
        highlights_x=[20],
        zoom=True,
        width=500,
        height=300,
        show=False,
    )
    bounds = render(page, chart)
    point = next(
        m
        for m in leaf_marks(chart.to_dict())
        if m.get("mark", {}).get("type") == "point"
    )
    domains = {axis: point["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")}
    x = bounds["x"] + bounds["width"] * (20 - domains["x"][0]) / np.ptp(domains["x"])
    y = bounds["y"] + bounds["height"] * (
        1 - (20 - domains["y"][0]) / np.ptp(domains["y"])
    )
    hover_at(page, x, y)
    page.locator("table.attributes").wait_for(state="visible")
    cells = [s.strip() for s in page.locator("table.attributes td").all_text_contents()]
    assert cells == ["A", "10", "20.00", "20.00"]
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(700)
    moved = {
        axis: page.evaluate(
            "a=>api.getScaleResolutionByName(`timeseries-${a}`).getDomain()", axis
        )
        for axis in ("x", "y")
    }
    assert all(np.ptp(moved[a]) < np.ptp(domains[a]) for a in ("x", "y"))
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + x, canvas["y"] + y)
    page.mouse.down()
    page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    assert (
        page.evaluate("api.getScaleResolutionByName('timeseries-x').getDomain()")
        != moved["x"]
    )
    path = tmp_path / "timeseries.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
