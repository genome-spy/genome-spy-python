"""Registered clustermap tiles, branches, labels, color tracks and native hover."""

from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_heatmap import render, hover_at
from tests.integrations.scanpy.browser.test_grid_interactions import (
    pointer,
    position,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.clustermap_fixture import (
    make_cluster_adata,
    clustermap_cases,
)

from tests.integrations.scanpy.helpers import tree_segments, tree_paths

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
    expected_paths = []
    for axis, count in (("row", 6), ("col", 4)):
        tree = reference[axis + "_tree"]
        if tree is None:
            continue
        maximum = 1.05 * (max(max(branch) for branch in tree["dcoord"]) or 1)
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
            parent_leaf = (leaves[1] + leaves[2]) / 2
            for child in (0, 3):
                vertices = []
                for leaf_position, merge_height in (
                    (parent_leaf, distances[1]),
                    (leaves[child], distances[child]),
                ):
                    center = leaf_position / 10 / count
                    depth = merge_height / maximum * extent + track
                    vertices.append(
                        [bounds["x"] - depth, bounds["y"] + center * height]
                        if axis == "row"
                        else [bounds["x"] + center * width, bounds["y"] - depth]
                    )
                parent, target = vertices
                elbow = (
                    [parent[0], target[1]] if axis == "row" else [target[0], parent[1]]
                )
                expected_paths.append([parent, elbow, target])
    actual_paths = tree_paths(svg_root(page))
    np.testing.assert_allclose(sorted(actual_paths), sorted(expected_paths), atol=0.6)
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
        bounds = render(
            page,
            gsc.pl.clustermap(
                data,
                obs_keys="group",
                show=False,
                width=size,
                height=size * 0.8,
                cmap="viridis",
            ),
        )
        canvas = page.locator("canvas").first.bounding_box()
        px = canvas["x"] + bounds["x"] + bounds["width"] * 0.125
        py = canvas["y"] + bounds["y"] + bounds["height"] / 12
        hover_at(page, px - canvas["x"], py - canvas["y"])
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


@pytest.mark.parametrize("zoom", [False, True])
def test_native_category_legend_matches_strip_and_stays_visible_during_zoom(page, zoom):
    from PIL import ImageColor

    data = make_cluster_adata()
    data.obs.loc["cell-0", "group"] = np.nan
    chart = gsc.pl.clustermap(
        data, obs_keys="group", zoom=zoom, width=300, height=240, show=False
    )
    bounds = render(page, chart)
    for navigated in (False, True):
        if navigated:
            pointer(page, bounds)
            page.mouse.wheel(0, -700)
            page.wait_for_timeout(700)
        root = svg_root(page)
        legends = [
            e
            for e in root.iter()
            if e.get("data-view-path", "").endswith("/legend_right")
            and any(t.tag.endswith("text") and t.text == "C" for t in e.iter())
        ]
        assert len(legends) == 1
        legend = legends[0]
        text = [e.text for e in legend.iter() if e.tag.endswith("text")]
        assert text == ["group", "C", "B", "A"]
        symbols = [
            e
            for group in legend.iter()
            if group.get("data-mark-type") == "point"
            for e in group
        ]
        assert [ImageColor.getrgb(e.get("fill")) for e in symbols] == [
            (0, 153, 0),
            (153, 0, 0),
            (0, 0, 153),
        ]
        # The legend is outside the matrix and inside the exported canvas.
        labels = [position(e) for e in legend.iter() if e.tag.endswith("text")]
        size = page.evaluate("api.getLogicalCanvasSize()")
        assert all(
            bounds["x"] + bounds["width"] < x < size["width"]
            and 0 <= y < size["height"]
            for x, y in labels
        )
        if not navigated:
            canvas = page.locator("canvas").first.bounding_box()
            pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
            slot = REFERENCE["default"]["row_order"].index(0)
            x = round(canvas["x"] + bounds["x"] - bounds["width"] * 0.03 / 0.77 / 2)
            y = round(canvas["y"] + bounds["y"] + (slot + 0.5) / 6 * bounds["height"])
            np.testing.assert_array_equal(pixels[y, x], [255, 255, 255])


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


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_navigation_keeps_both_trees_strips_and_labels_aligned(page, zoom, tmp_path):
    data = make_cluster_adata()
    row_colors = ["red", "blue", "green", "gold", "black", "purple"]
    col_colors = ["red", "green", "blue", "black"]
    chart = gsc.pl.clustermap(
        data,
        row_colors=pd.Series(row_colors, index=data.obs_names, name="Cell type"),
        col_colors=pd.Series(col_colors, index=data.var_names, name="Gene class"),
        zoom=zoom,
        show_values=True,
        width=320,
        height=240,
        show=False,
    )
    bounds = render(page, chart)
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -260)
    page.wait_for_timeout(700)
    for pan in (False, True):
        if pan:
            page.mouse.down()
            page.mouse.move(px + 20, py + 18, steps=5)
            page.mouse.up()
            page.wait_for_timeout(700)
        root = svg_root(page)
        assert value_texts(root)
        centers = page.evaluate("""() => ['y','x'].map(axis=>{
            const s=api.getScaleResolutionByName(`clustermap-${axis}`).getScale();
            return Array.from({length:axis==='y'?6:4},(_,i)=>axis==='y'?1-s(i)+s.bandwidth()/2:s(i)+s.bandwidth()/2);
        })""")
        trees, strips = [], []
        for side in ("left", "top"):
            tree_view = next(
                e
                for e in root.iter()
                if e.get("data-view-path", "").endswith(f"/clustermap-{side}-tree")
            )
            strip_view = next(
                e
                for e in root.iter()
                if e.get("data-view-path", "").endswith(f"/clustermap-{side}-colors-0")
            )
            trees.append(
                next(e for e in tree_view.iter() if e.get("stroke") == "#555555")
            )
            strips.append(
                list(
                    next(
                        e
                        for e in strip_view.iter()
                        if e.get("data-mark-type") == "rect"
                    )
                )
            )
        assert len(trees) == len(strips) == 2
        # Every visible label and zero-distance tree leaf uses the same slot center.
        for axis, labels, tree, strip, colors in (
            (1, data.obs_names, trees[0], strips[0], row_colors),
            (0, data.var_names, trees[1], strips[1], col_colors),
        ):
            channel, cross = ("y", "x") if axis else ("x", "y")
            start = bounds[channel]
            extent = bounds["height" if axis else "width"]
            cross_extent = bounds["width" if axis else "height"]
            edge = bounds[cross] - cross_extent * 0.03 / 0.77
            endpoints = np.array(tree_segments(tree)).reshape(-1, 2)
            leaves = endpoints[np.abs(endpoints[:, 1 - axis] - edge) < 1, axis]
            assert any(e.get("clip-path") for e in root.iter())
            order = REFERENCE["default"]["row_order" if axis else "col_order"]
            visible = 0
            for slot, original in enumerate(order):
                fraction = centers[0 if axis else 1][slot]
                if not 0 < fraction < 1:
                    continue
                visible += 1
                center = start + fraction * extent
                label = next(
                    e
                    for e in root.iter()
                    if e.tag.endswith("text") and e.text == labels[original]
                )
                assert position(label)[axis] == pytest.approx(center, abs=1)
                assert any(abs(leaf - position(label)[axis]) < 1 for leaf in leaves)
                rectangle = next(
                    r
                    for r in strip
                    if float(r.get(channel))
                    <= center
                    <= float(r.get(channel))
                    + float(r.get("height" if axis else "width"))
                )
                from PIL import ImageColor

                assert ImageColor.getrgb(rectangle.get("fill")) == ImageColor.getrgb(
                    colors[original]
                )
            assert visible > 0
    # The declarative chart must also render in offline HTML.
    output = tmp_path / "clustermap-navigation.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").wait_for(state="visible")
    assert not page.locator(".message-box").count()
