"""Registered clustermap tiles, branches, labels, color tracks and native hover."""

from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.clustermap_fixture import (
    make_cluster_adata,
    clustermap_cases,
)

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/clustermap.json").read_text()
)["cases"]


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", clustermap_cases())
def test_complete_registered_tiles_trees_and_labels(
    page, tmp_path, reference_images, case
):
    reference = REFERENCE[case]
    chart = gsc.pl.clustermap(
        make_cluster_adata(),
        show=False,
        cmap="viridis",
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        **clustermap_cases()[case],
    )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    width, height = bounds["width"], bounds["height"]
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={"x": left, "y": top, "width": width, "height": height}
            )
        )
    ).convert("RGB")
    expected = Image.open(
        reference_images("clustermap") / f"clustermap-{case}-panel.png"
    ).convert("RGB")
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    pixels, target = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    for row, column in np.ndindex(6, 4):
        x, y = (column + 0.3) / 4, (row + 0.3) / 6
        np.testing.assert_allclose(
            pixels[int(y * actual.height), int(x * actual.width)],
            target[int(y * expected.height), int(x * expected.width)],
            atol=12,
        )
    # SVG checks positions exactly; raster checks visibility of the thin 0.5pt strokes.
    full = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    expected_segments = []
    for axis, count in (("row", 6), ("col", 4)):
        tree = reference[axis + "_tree"]
        if tree is None:
            continue
        maximum = max(max(branch) for branch in tree["dcoord"]) or 1
        track = width * 0.03 / 0.77 if case == "row_annotation" and axis == "row" else 0
        extent = (
            (width if axis == "row" else height)
            * 0.2
            / (0.77 if case == "row_annotation" and axis == "row" else 0.8)
        )
        for leaves, distances in zip(tree["icoord"], tree["dcoord"], strict=True):
            for i in range(3):
                leaf = (leaves[i] + leaves[i + 1]) / 2 / 10 / count
                distance = (
                    distances[i] + distances[i + 1]
                ) / 2 / maximum * extent + track
                x, y = (
                    (left - distance, top + leaf * height)
                    if axis == "row"
                    else (left + leaf * width, top - distance)
                )
                px, py = round(x * 1.5), round(y * 1.5)
                region = full[py - 2 : py + 3, px - 2 : px + 3].astype(int)
                assert region.size and np.any(region.max(axis=2) < 230), (
                    case,
                    axis,
                    leaf,
                    distance,
                )
                endpoints = []
                for j in (i, i + 1):
                    center = leaves[j] / 10 / count
                    depth = distances[j] / maximum * extent + track
                    endpoints.extend(
                        (bounds["x"] - depth, bounds["y"] + center * height)
                        if axis == "row"
                        else (bounds["x"] + center * width, bounds["y"] - depth)
                    )
                expected_segments.append(endpoints)
    actual_segments = page.evaluate("""async () => {
        const host=document.createElement('div');
        host.innerHTML=await (await api.imageExport.svg()).blob.text();
        return [...host.querySelectorAll('line')].filter(e=>e.closest('[stroke]')?.getAttribute('stroke')==='#555555').map(e=>['x1','y1','x2','y2'].map(k=>+e.getAttribute(k)));
    }""")
    np.testing.assert_allclose(actual_segments, expected_segments, atol=0.6)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for label in reference["x_labels"] + reference["y_labels"]:
        assert f">{label}<" in svg
    assert "linearGradient" in svg
    if case == "row_annotation":
        assert ">group<" in svg
        track = width * 0.03 / 0.77
        palette = {
            "C": np.array([0, 153, 0]),
            "B": np.array([153, 0, 0]),
            "A": np.array([0, 0, 153]),
        }
        data = make_cluster_adata()
        for slot, original in enumerate(reference["row_order"]):
            x = round((left - track / 2) * 1.5)
            y = round((top + (slot + 0.5) / 6 * height) * 1.5)
            np.testing.assert_allclose(
                full[y, x].astype(int),
                palette[data.obs["group"].iloc[original]],
                atol=2,
            )
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


def test_hover_tracks_supplied_order_resize_and_offline_html(page, tmp_path):
    data = make_cluster_adata()
    chart = gsc.pl.clustermap(
        data, obs_keys="group", show=False, width=300, height=240, cmap="viridis"
    )
    for size in (300, 450):
        bounds = render(page, chart.properties(width=size, height=size * 0.8))
        canvas = page.locator("canvas").first.bounding_box()
        px = canvas["x"] + bounds["x"] + bounds["width"] * 0.125
        py = canvas["y"] + bounds["y"] + bounds["height"] / 12
        page.mouse.move(px - 2, py - 2)
        page.wait_for_timeout(450)
        page.mouse.move(px, py)
        page.locator("table.attributes").wait_for(state="visible")
        rows = [
            row.locator("td").inner_text().strip()
            for row in page.locator("table.attributes tr").all()
        ]
        ref = REFERENCE["default"]
        assert rows[:2] == [
            f"cell-{ref['row_order'][0]}",
            str(data.var_names[ref["col_order"][0]]),
        ]
        assert float(rows[2]) == pytest.approx(ref["values"][0][0])
    output = tmp_path / "clustermap.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("named", [False, True])
def test_multiple_positional_and_indexed_tracks_on_both_axes(page, named):
    data = make_cluster_adata()
    rows = ["red", "blue", "green", "gold", "black", "purple"]
    columns = ["red", "green", "blue", "black"]
    row_colors = [rows, ["white"] * 6]
    col_colors = columns
    if named:
        row_colors = pd.DataFrame(
            {"Long observation annotation": rows, "second": ["white"] * 6},
            index=data.obs_names,
        ).iloc[::-1]
        col_colors = pd.Series(
            columns, index=data.var_names, name="Long gene annotation"
        ).iloc[::-1]
    chart = gsc.pl.clustermap(
        data,
        row_colors=row_colors,
        col_colors=col_colors,
        width=320,
        height=240,
        cmap="viridis",
        show=False,
    )
    bounds = render(page, chart)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    if named:
        labels = ["Long observation annotation", "second", "Long gene annotation"]
        assert all(f">{label}<" in svg for label in labels)
        boxes = page.evaluate(
            """async (labels) => {
            const host=document.createElement('div');
            host.innerHTML=await (await api.imageExport.svg()).blob.text();
            document.body.append(host);
            const root=host.querySelector('svg').getBoundingClientRect();
            const result=[...host.querySelectorAll('text')].filter(t=>labels.includes(t.textContent)).map(t=>{
                const b=t.getBoundingClientRect();
                return {left:b.left-root.left,top:b.top-root.top,right:b.right-root.left,bottom:b.bottom-root.top};
            });
            host.remove(); return result;
        }""",
            labels,
        )
        size = page.evaluate("api.getLogicalCanvasSize()")
        assert len(boxes) == 3
        assert all(
            b["left"] >= 0
            and b["top"] >= 0
            and b["right"] <= size["width"] + 1
            and b["bottom"] <= size["height"] + 1
            for b in boxes
        )
    canvas = page.locator("canvas").first.bounding_box()
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    # Check the original-color identity after both permutations, away from borders.
    from PIL import ImageColor

    for slot, original in enumerate(REFERENCE["default"]["row_order"]):
        x = round(left - bounds["width"] * 0.03 / 0.74 * 1.5)
        y = round(top + (slot + 0.5) / 6 * bounds["height"])
        np.testing.assert_allclose(
            pixels[y, x].astype(int), ImageColor.getrgb(rows[original]), atol=2
        )
    for slot, original in enumerate(REFERENCE["default"]["col_order"]):
        x = round(left + (slot + 0.5) / 4 * bounds["width"])
        y = round(top - bounds["height"] * 0.03 / 0.77 / 2)
        np.testing.assert_allclose(
            pixels[y, x].astype(int), ImageColor.getrgb(columns[original]), atol=2
        )
