"""Registered DPT expression charts and observed shared native interactions."""

import warnings
from io import BytesIO

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    point_coordinates,
    point_spacing,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.browser.rendering import render_heatmap as render
from tests.integrations.scanpy.browser.rendering import style_profile_reference
from tests.integrations.scanpy.profile_fixtures import (
    dpt_profile_cases,
    make_dpt_profiles,
)


@pytest.mark.reference
@pytest.mark.parametrize("case", dpt_profile_cases())
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_dpt_expression_matches_scanpy_paint_labels_and_boundaries(
    page, tmp_path, case
):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    adata, options = make_dpt_profiles(case), dpt_profile_cases()[case]
    with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sc.pl.dpt_timeseries(adata, show=False, **options)
        fig, ax = plt.gcf(), plt.gcf().axes[0]
        style_profile_reference(ax)
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        limits = [ax.get_xlim(), ax.get_ylim()]
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
        heatmap = bool(ax.images)
        xy = (
            None
            if heatmap
            else np.ma.concatenate([c.get_offsets() for c in ax.collections])
        )
        plt.close(fig)
    chart = gsc.pl.dpt_timeseries(adata, show=False, **options)
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.6)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.6)
    root = svg_root(page)
    texts = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert "dpt order" in texts
    assert set(adata.var_names) <= set(texts)
    rules = [
        line
        for group in root.iter()
        if group.get("data-mark-type") == "rule" and group.get("stroke-dasharray")
        for line in group
    ]
    assert len(rules) == len(adata.uns["dpt_changepoints"])
    for line, x in zip(rules, adata.uns["dpt_changepoints"], strict=True):
        assert float(line.get("x1")) == pytest.approx(
            bounds["x"] + (x - limits[0][0]) / np.ptp(limits[0]) * bounds["width"],
            abs=1,
        )
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
    a, b = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    checked = 0
    if heatmap:
        for fx in np.linspace(0.07, 0.93, 17):
            x = limits[0][0] + fx * np.ptp(limits[0])
            if any(abs(x - h) < 0.1 for h in adata.uns["dpt_changepoints"]):
                continue
            if abs(x - (round(x - 0.5) + 0.5)) < 0.06:
                continue
            for fy in (0.2, 0.8):
                np.testing.assert_allclose(
                    a[int(fy * actual.height), int(fx * actual.width)],
                    b[int(fy * expected.height), int(fx * expected.width)],
                    atol=12,
                )
                checked += 1
    else:
        for x, y in xy:
            if x in adata.uns["dpt_changepoints"]:
                continue
            fx, fy = (
                (x - limits[0][0]) / np.ptp(limits[0]),
                1 - (y - limits[1][0]) / np.ptp(limits[1]),
            )
            if not (0.02 < fx < 0.98 and 0.02 < fy < 0.98):
                continue
            ap = a[
                int(fy * actual.height) - 5 : int(fy * actual.height) + 6,
                int(fx * actual.width) - 5 : int(fx * actual.width) + 6,
            ]
            bp = b[
                int(fy * expected.height) - 5 : int(fy * expected.height) + 6,
                int(fx * expected.width) - 5 : int(fx * expected.width) + 6,
            ]
            assert (
                abs(
                    np.count_nonzero(np.min(ap, axis=2) < 220)
                    - np.count_nonzero(np.min(bp, axis=2) < 220)
                )
                <= 15
            )
            assert np.min(np.linalg.norm(ap.reshape(-1, 3) - bp[5, 5], axis=1)) < 35
            checked += 1
    assert checked > 0
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


@pytest.mark.parametrize("heatmap", [False, True])
def test_hover_zoom_pan_values_and_offline_delivery_use_shared_paths(
    page, tmp_path, heatmap
):
    import pandas as pd
    from anndata import AnnData

    adata = AnnData(
        np.arange(60, dtype=float).reshape(30, 2),
        obs=pd.DataFrame(
            {"dpt_order_indices": np.roll(np.arange(30), 5)},
            index=[f"cell-{i}" for i in range(30)],
        ),
        var=pd.DataFrame(index=["A", "B"]),
        uns={"dpt_changepoints": [10, 20]},
    )
    chart = gsc.pl.dpt_timeseries(
        adata,
        as_heatmap=heatmap,
        marker="o",
        hover=True,
        zoom="xy",
        show_values=heatmap,
        width=500,
        height=300,
        show=False,
    )
    spec = chart.to_dict()
    if heatmap:
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"dpt_timeseries-{axis}"
    bounds = render(page, spec)
    x = (
        bounds["x"] + bounds["width"] * 10 / 29
        if heatmap
        else bounds["x"] + bounds["width"] * 10 / 39
    )
    if heatmap:
        y = bounds["y"] + bounds["height"] * 0.8
    else:
        point = next(m for m in spec["layer"] if m["mark"]["type"] == "point")
        dy = point["encoding"]["y"]["scale"]["domain"]
        y = bounds["y"] + bounds["height"] * (1 - (10 - dy[0]) / np.ptp(dy))
    hover_at(page, x, y)
    page.locator("table.attributes").wait_for(state="visible")
    cells = [s.strip() for s in page.locator("table.attributes td").all_text_contents()]
    assert cells == (["A", "10", "10.00"] if heatmap else ["A", "10", "10.00", "10.00"])
    before = (
        page.evaluate("api.getScaleResolutionByName('dpt_timeseries-x').getDomain()")
        if heatmap
        else point_coordinates(page)[0]
    )
    page.mouse.wheel(0, -500)
    page.wait_for_timeout(700)
    zoomed = (
        page.evaluate("api.getScaleResolutionByName('dpt_timeseries-x').getDomain()")
        if heatmap
        else point_coordinates(page)[0]
    )
    assert not np.array_equal(zoomed, before)
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + x, canvas["y"] + y)
    page.mouse.down()
    page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
    page.mouse.up()
    page.wait_for_timeout(300)
    after = (
        page.evaluate("api.getScaleResolutionByName('dpt_timeseries-x').getDomain()")
        if heatmap
        else point_coordinates(page)[0]
    )
    assert not np.array_equal(after, zoomed)
    if heatmap:
        assert value_texts(svg_root(page))
    else:
        assert all(
            a > b
            for a, b in zip(point_spacing(after), point_spacing(before), strict=True)
        )
    path = tmp_path / "dpt.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
