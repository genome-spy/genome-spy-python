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

from tests.integrations.scanpy.helpers import tree_segments

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
    actual_segments = tree_segments(svg_root(page))
    np.testing.assert_allclose(
        sorted(actual_segments), sorted(expected_segments), atol=0.6
    )
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


@pytest.mark.parametrize("page", [1, 1.5], indirect=True)
@pytest.mark.parametrize("hover", [False, True])
def test_native_cluster_gaps_keep_tracks_aligned_and_empty_during_navigation(
    page, hover
):
    from tests.integrations.scanpy.helpers import index_position

    data = make_cluster_adata()
    for width in (320, 480):
        chart = gsc.pl.clustermap(
            data,
            obs_keys="group",
            row_gap_threshold=3,
            col_gap_threshold=10,
            width=width,
            height=240,
            zoom="xy",
            show_values=True,
            hover=hover,
            show=False,
        )
        bounds = render(page, chart)
        for navigated in (False, True):
            if navigated:
                px, py = pointer(page, bounds)
                page.mouse.wheel(0, -120)
                page.wait_for_timeout(700)
                page.mouse.down()
                page.mouse.move(px + 5, py + 5, steps=3)
                page.mouse.up()
                page.wait_for_timeout(700)
            projected = page.evaluate("""() => ['x','y'].map(axis=>{
                const s=api.getScaleResolutionByName(`clustermap-${axis}`).getScale();
                const start=i=>axis==='x'?s(i):1-s(i);
                return {centers:Array.from({length:axis==='x'?4:6},(_,i)=>start(i)+s.bandwidth()/2),
                    gaps:(axis==='x'?[1]:[2,4]).map(i=>[start(i-1)+s.bandwidth(),start(i)])};
            })""")
            root = svg_root(page)
            segments = np.array(tree_segments(root)).reshape(-1, 2)
            for axis, count, cuts, labels, order in (
                (0, 4, (1,), data.var_names, REFERENCE["default"]["col_order"]),
                (1, 6, (2, 4), data.obs_names, REFERENCE["default"]["row_order"]),
            ):
                channel, extent = ("x", "width") if axis == 0 else ("y", "height")
                centers = projected[axis]["centers"]
                if not navigated:
                    expected = [
                        index_position(i + 0.5, count, 0, bounds[extent], cuts)
                        for i in range(count)
                    ]
                    np.testing.assert_allclose(
                        np.array(centers) * bounds[extent], expected, atol=0.1
                    )
                for slot, original in enumerate(order):
                    if not 0 < centers[slot] < 1:
                        continue
                    center = bounds[channel] + centers[slot] * bounds[extent]
                    label = next(
                        e
                        for e in root.iter()
                        if e.tag.endswith("text") and e.text == labels[original]
                    )
                    assert position(label)[axis] == pytest.approx(center, abs=1)
                    assert np.any(np.abs(segments[:, axis] - center) < 1)
                visible_gaps = [
                    (a, b) for a, b in projected[axis]["gaps"] if 0 < a < b < 1
                ]
                assert visible_gaps
                for start, stop in visible_gaps:
                    assert (stop - start) * bounds[extent] == pytest.approx(4, abs=0.01)
                    fractions = [0.5, 0.5]
                    fractions[axis] = (start + stop) / 2
                    pointer(page, bounds, *fractions)
                    page.wait_for_timeout(450)
                    assert not page.locator("table.attributes").is_visible()
                    pixels = np.asarray(
                        Image.open(BytesIO(page.screenshot())).convert("RGB")
                    )
                    canvas = page.locator("canvas").first.bounding_box()
                    dpr = page.evaluate("devicePixelRatio")
                    x = round(
                        (canvas["x"] + bounds["x"] + fractions[0] * bounds["width"])
                        * dpr
                    )
                    y = round(
                        (canvas["y"] + bounds["y"] + fractions[1] * bounds["height"])
                        * dpr
                    )
                    assert pixels[y, x].min() > 245
            # A row strip has exactly the same slot edges and gap widths as the tiles.
            rectangles = [
                [e for e in group if e.tag.endswith("rect")]
                for group in root.iter()
                if group.get("data-mark-type") == "rect"
            ]
            strip = next(group for group in rectangles if len(group) == 6)
            for slot, rectangle in enumerate(strip):
                expected = (
                    bounds["y"] + projected[1]["centers"][slot] * bounds["height"]
                )
                assert float(rectangle.get("y")) + float(
                    rectangle.get("height")
                ) / 2 == pytest.approx(expected, abs=1)

            # Check tile and strip hover in the same navigated slots.
            slots = [
                min(range(len(p["centers"])), key=lambda i: abs(p["centers"][i] - 0.5))
                for p in projected
            ]
            fractions = [projected[i]["centers"][slot] for i, slot in enumerate(slots)]
            x, y = pointer(page, bounds, *fractions)
            page.wait_for_timeout(450)
            page.mouse.move(x + 0.5, y + 0.5)
            page.wait_for_timeout(100)
            if hover:
                page.locator("table.attributes").wait_for(state="visible", timeout=2000)
                text = [
                    t.strip()
                    for t in page.locator("table.attributes td").all_text_contents()
                ]
                assert text[:2] == [
                    str(data.obs_names[REFERENCE["default"]["row_order"][slots[1]]]),
                    str(data.var_names[REFERENCE["default"]["col_order"][slots[0]]]),
                ]
            else:
                assert not page.locator("table.attributes").is_visible()
            track = page.evaluate(
                "api.views.getLayoutBounds({scope:[],view:'clustermap-left-colors-0'})"
            )
            hover_at(
                page,
                track["x"] + track["width"] / 2,
                bounds["y"] + fractions[1] * bounds["height"],
            )
            if hover:
                expected = data.obs["group"].iloc[
                    REFERENCE["default"]["row_order"][slots[1]]
                ]
                assert [
                    s.strip()
                    for s in page.locator("table.attributes td").all_text_contents()
                ] == [expected]
            else:
                assert not page.locator("table.attributes").is_visible()
            for start, stop in projected[1]["gaps"]:
                if 0 < start < stop < 1:
                    hover_at(
                        page,
                        track["x"] + track["width"] / 2,
                        bounds["y"] + (start + stop) / 2 * bounds["height"],
                        probe=False,
                    )
                    assert not page.locator("table.attributes").is_visible()


def test_auto_labels_account_for_gap_space_without_enabling_zoom(page):
    chart = gsc.pl.clustermap(
        make_cluster_adata(),
        row_gap_threshold=3,
        width=300,
        height=30,
        yticklabels="auto",
        show=False,
    )
    render(page, chart)
    labels = [
        e
        for e in svg_root(page).iter()
        if e.tag.endswith("text") and (e.text or "").startswith("cell-")
    ]
    order = REFERENCE["default"]["row_order"]
    assert [e.text for e in labels] == [f"cell-{order[i]}" for i in (0, 4)]
    assert abs(position(labels[1])[1] - position(labels[0])[1]) >= 13
