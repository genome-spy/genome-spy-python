"""Registered heatmap tiles, complete annotations, unequal trees and cell hover."""

from io import BytesIO
import json
from pathlib import Path
import re
import warnings
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render as render_chart
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata, heatmap_cases
from tests.integrations.scanpy.helpers import tree_segments

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "heatmap.json").read_text())


def render(page, chart):
    """Wait for native track sizing before measuring exported geometry."""
    render_chart(page, chart)
    page.wait_for_timeout(200)
    return page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")


def slot_bounds(slot, count, cuts, origin, extent):
    """Compute expected band edges independently from the native exported marks."""
    step = (extent - 4 * len(cuts)) / count
    start = origin + slot * step + 4 * sum(cut <= slot for cut in cuts)
    return start, start + step


def tile_rects(root):
    """Read the matrix's exported tile rectangles in measurement order."""
    return list(next(e for e in root.iter() if e.get("data-mark-type") == "rect"))


def hover_at(page, x, y, *, probe=True):
    """Pause then move within the native tooltip's small picking neighborhood."""
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + x - 2, canvas["y"] + y - 2)
    page.wait_for_timeout(450)
    offsets = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)) if probe else ((0, 0),)
    for dx, dy in offsets:
        page.mouse.move(canvas["x"] + x + dx, canvas["y"] + y + dy)
        page.wait_for_timeout(80)


@pytest.mark.parametrize("page", [1, 1.5], indirect=True)
@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("hover", [False, True])
@pytest.mark.parametrize("group_gap", [0, 4, 7])
def test_native_tracks_gaps_hover_and_navigation(page, swapped, hover, group_gap):
    chart = gsc.pl.heatmap(
        make_heatmap_adata(),
        {"First": ["g1", "g2"], "Last": ["g3"]},
        "group",
        dendrogram=True,
        swap_axes=swapped,
        hover=hover,
        group_gap=group_gap,
        zoom="xy",
        width=450,
        height=300,
        show=False,
    )
    bounds = render(page, chart)
    cell_axis = "x" if swapped else "y"
    cell_extent = "width" if swapped else "height"
    for navigated in (False, True):
        if navigated:
            canvas = page.locator("canvas").first.bounding_box()
            page.mouse.move(
                canvas["x"] + bounds["x"] + 225, canvas["y"] + bounds["y"] + 150
            )
            before = page.evaluate(
                "api.getScaleResolutionByName('heatmap-y').getDomain()"
            )
            page.mouse.wheel(0, -220)
            page.wait_for_timeout(200)
            page.mouse.down()
            page.mouse.move(
                canvas["x"] + bounds["x"] + 235,
                canvas["y"] + bounds["y"] + 160,
                steps=5,
            )
            page.mouse.up()
            page.evaluate("""async()=>{
                const sample=()=>['x','y'].flatMap(axis=>{
                    const s=api.getScaleResolutionByName(`heatmap-${axis}`).getScale();
                    return [...s.domain(),s(0),s(4)];
                });
                let previous=sample(), stable=0;
                const deadline=performance.now()+3000;
                while(performance.now()<deadline){
                    await new Promise(requestAnimationFrame);
                    const current=sample();
                    stable=current.every((v,i)=>Math.abs(v-previous[i])<1e-7) ? stable+1 : 0;
                    if(stable>=3) return;
                    previous=current;
                }
                throw Error('Navigation did not settle');
            }""")
            assert (
                page.evaluate("api.getScaleResolutionByName('heatmap-y').getDomain()")
                != before
            )
        root = ET.fromstring(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
        strip_bounds = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'heatmap-category-strip'})"
        )
        tree_bounds = page.evaluate(
            "api.views.getLayoutBounds({scope:[],view:'heatmap-tree'})"
        )
        assert strip_bounds[cell_axis] == pytest.approx(bounds[cell_axis], abs=0.2)
        assert strip_bounds[cell_extent] == pytest.approx(bounds[cell_extent], abs=0.2)
        assert tree_bounds[cell_axis] == pytest.approx(bounds[cell_axis], abs=0.2)
        assert tree_bounds[cell_extent] == pytest.approx(bounds[cell_extent], abs=0.2)
        edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
        assert (
            tree_bounds["y"] + tree_bounds["height"] if swapped else tree_bounds["x"]
        ) == pytest.approx(edge, abs=0.2)
        across = "y" if swapped else "x"
        strip_group = next(
            e
            for e in root.iter()
            if e.get("data-mark-type") == "rect"
            and len(e)
            and abs(float(e[0].get(across)) - strip_bounds[across]) < 1
        )
        tiles = tile_rects(root)
        for cell, strip in enumerate(strip_group):
            for field in (cell_axis, cell_extent):
                tile = next(
                    tile
                    for tile in tiles
                    if abs(float(tile.get(cell_axis)) - float(strip.get(cell_axis)))
                    < 0.2
                )
                assert float(strip.get(field)) == pytest.approx(
                    float(tile.get(field)), abs=0.2
                )
        groups = {
            e.text: e
            for e in root.iter()
            if e.tag.endswith("text") and e.text in {"A", "B", "C", "D"}
        }
        tree = next(e for e in root.iter() if e.get("stroke") == "#555555")
        segments = [(row[:2], row[2:]) for row in tree_segments(tree)]
        endpoints = [xy for segment in segments for xy in segment]
        for i, (start, stop) in enumerate(segments):
            for xy in (start, stop):
                if abs(xy[1 if swapped else 0] - edge) < 1:
                    continue
                if (
                    not bounds[cell_axis]
                    < xy[0 if swapped else 1]
                    < bounds[cell_axis] + bounds[cell_extent]
                ):
                    continue
                assert any(
                    j != i
                    and all(
                        min(a[k], b[k]) - 0.2 <= xy[k] <= max(a[k], b[k]) + 0.2
                        for k in (0, 1)
                    )
                    for j, (a, b) in enumerate(segments)
                ), (xy, segments)
        leaves = [
            xy[0 if swapped else 1]
            for xy in endpoints
            if abs(xy[1 if swapped else 0] - edge) < 1
        ]
        for label in groups.values():
            position = [
                float(v)
                for v in re.search(r"translate\(([^)]+)\)", label.get("transform"))
                .group(1)
                .split()
            ]
            assert any(
                abs(leaf - position[0 if swapped else 1]) < 0.2 for leaf in leaves
            )
        # Read the live gapped scale for pointer targets, independently of SVG export.
        live = page.evaluate(
            """axis=>{
            const scale=api.getScaleResolutionByName(`heatmap-${axis}`).getScale();
            const width=scale.bandwidth();
            const sign=axis==='x' ? 1 : -1;
            const pixel=v=>axis==='x' ? v : 1-v;
            return {
                centers:Array.from({length:9},(_,i)=>pixel(scale(i)+sign*width/2)),
                gaps:[3,4,7].map(cut=>pixel((scale(cut-1)+sign*width+scale(cut))/2)),
            };
        }""",
            cell_axis,
        )
        visible = [
            i for i, fraction in enumerate(live["centers"]) if 0.05 < fraction < 0.95
        ]
        cell = visible[len(visible) // 2]
        fraction = live["centers"][cell]
        x = strip_bounds["x"] + strip_bounds["width"] * (fraction if swapped else 0.5)
        y = strip_bounds["y"] + strip_bounds["height"] * (0.5 if swapped else fraction)
        hover_at(page, x, y)
        if hover:
            page.locator("table.attributes").wait_for(state="visible", timeout=2000)
            expected_group = ["C", "C", "C", "A", "D", "D", "D", "B", "B"][cell]
            assert (
                page.locator("table.attributes td").inner_text().strip()
                == expected_group
            )
        else:
            assert not page.locator("table.attributes").is_visible()
        # Empty native gaps must not pick an adjacent category or measurement.
        ordered = sorted(strip_group, key=lambda r: float(r.get(cell_axis)))
        if group_gap == 0:
            assert all(
                abs(
                    float(b.get(cell_axis))
                    - float(a.get(cell_axis))
                    - float(a.get(cell_extent))
                )
                < 0.31
                for a, b in zip(ordered[:-1], ordered[1:], strict=True)
            )
            continue
        gaps = [
            (a, b)
            for a, b in zip(ordered[:-1], ordered[1:], strict=True)
            if float(b.get(cell_axis))
            - float(a.get(cell_axis))
            - float(a.get(cell_extent))
            > group_gap / 2
            and bounds[cell_axis]
            < float(b.get(cell_axis))
            < bounds[cell_axis] + bounds[cell_extent]
        ]
        assert gaps
        a, b = gaps[0]
        assert float(b.get(cell_axis)) - float(a.get(cell_axis)) - float(
            a.get(cell_extent)
        ) == pytest.approx(group_gap, abs=0.31)
        fraction = next(f for f in live["gaps"] if 0.05 < f < 0.95)
        middle = bounds[cell_axis] + fraction * bounds[cell_extent]
        hover_at(page, middle if swapped else x, y if swapped else middle, probe=False)
        assert not page.locator("table.attributes").is_visible(), (navigated, middle)
        hover_at(
            page,
            middle if swapped else bounds["x"] + 30,
            bounds["y"] + 30 if swapped else middle,
            probe=False,
        )
        assert not page.locator("table.attributes").is_visible()


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", heatmap_cases())
def test_complete_registered_heatmaps(page, tmp_path, reference_images, case):
    reference = REFERENCE["cases"][case]
    options = heatmap_cases()[case].copy()
    names = options.pop("var_names", ["g1", "g2", "g3"])
    groupby = options.pop("groupby", "group")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.heatmap(
            make_heatmap_adata(case),
            names,
            groupby,
            group_gap=4,
            width=reference["plot_size"][0],
            height=reference["plot_size"][1],
            show=False,
            **options,
        )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for text in set(
        reference["x_labels"] + reference["y_labels"] + reference["group_labels"]
    ):
        if text:
            assert f">{text}<" in svg, (case, text)
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": left,
                    "y": top,
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    expected = Image.open(
        reference_images("heatmap") / f"heatmap-{case}-panel.png"
    ).convert("RGB")
    values = np.array(reference["values"], dtype=float)
    scales = chart.to_dict()["scales"]
    cuts_x, cuts_y = [scales[axis]["gapPositions"] for axis in ("x", "y")]
    rects = tile_rects(ET.fromstring(svg))
    registered = Image.new("RGB", actual.size, "white")
    for row, column in np.ndindex(values.shape):
        x0, x1 = slot_bounds(column, values.shape[1], cuts_x, 0, bounds["width"])
        y0, y1 = slot_bounds(row, values.shape[0], cuts_y, 0, bounds["height"])
        px = int((x0 + (x1 - x0) / 4) / bounds["width"] * actual.width)
        py = int((y0 + (y1 - y0) / 4) / bounds["height"] * actual.height)
        ex = int((column + 0.25) / values.shape[1] * expected.width)
        ey = int((row + 0.25) / values.shape[0] * expected.height)
        np.testing.assert_allclose(
            np.asarray(actual)[py, px].astype(int),
            np.asarray(expected)[ey, ex].astype(int),
            atol=12,
            err_msg=case,
        )
        # Register the frozen upstream tiles with only the intentional blank gaps added.
        crop = expected.crop(
            (
                round(column / values.shape[1] * expected.width),
                round(row / values.shape[0] * expected.height),
                round((column + 1) / values.shape[1] * expected.width),
                round((row + 1) / values.shape[0] * expected.height),
            )
        )
        box = tuple(round(v * actual.width / bounds["width"]) for v in (x0, x1))
        rows = tuple(round(v * actual.height / bounds["height"]) for v in (y0, y1))
        registered.paste(
            crop.resize((box[1] - box[0], rows[1] - rows[0])), (box[0], rows[0])
        )
    # The rendered rectangles must occupy the independently calculated gapped slots.
    records = next(
        rows for rows in chart.to_dict()["datasets"].values() if "_value" in rows[0]
    )
    expected_rects = []
    for record in records:
        if record["_value"] is None:
            continue
        x0, x1 = slot_bounds(
            record["_x"], values.shape[1], cuts_x, bounds["x"], bounds["width"]
        )
        y0, y1 = slot_bounds(
            record["_y"], values.shape[0], cuts_y, bounds["y"], bounds["height"]
        )
        expected_rects.append([x0, y0, x1 - x0, y1 - y0])
    actual_rects = sorted(
        [float(rect.get(k)) for k in ("x", "y", "width", "height")] for rect in rects
    )
    np.testing.assert_allclose(actual_rects, sorted(expected_rects), atol=1)
    # Register stored upstream branches through the same expected slot mapping.
    swapped = options.get("swap_axes", False)
    paths = reference["tree_paths"]
    maximum = (
        max((point[1 if swapped else 0] for path in paths for point in path), default=1)
        or 1
    ) * 1.05
    screenshot = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    tree_bounds = (
        page.evaluate("api.views.getLayoutBounds({scope:[],view:'heatmap-tree'})")
        if paths
        else None
    )
    for path in paths:
        projected = []
        for point in path:
            leaf = point[0 if swapped else 1] - 0.5
            start, stop = slot_bounds(
                int(np.floor(leaf)),
                values.shape[1 if swapped else 0],
                cuts_x if swapped else cuts_y,
                left if swapped else top,
                bounds["width" if swapped else "height"],
            )
            along = start + (leaf % 1 + 0.5) * (stop - start)
            projected.append(
                (along, top - point[1] / maximum * tree_bounds["height"])
                if swapped
                else (
                    left + bounds["width"] + point[0] / maximum * tree_bounds["width"],
                    along,
                )
            )
        for start, stop in zip(projected[:-1], projected[1:], strict=True):
            for fraction in (0.25, 0.5, 0.75):
                px, py = np.round(
                    (np.array(start) + (np.array(stop) - start) * fraction) * 1.5
                ).astype(int)
                region = screenshot[py - 3 : py + 4, px - 3 : px + 4].astype(int)
                assert region.size and np.any(np.abs(region - 85).max(axis=2) < 40), (
                    case,
                    start,
                    stop,
                )
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    (tmp_path / f"{case}.svg").write_text(svg)
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), registered.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("swapped", [False, True])
def test_cell_hover_after_tree_reordering_and_resize(page, tmp_path, swapped):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.heatmap(
            make_heatmap_adata(),
            ["g1", "g2"],
            "group",
            dendrogram=True,
            swap_axes=swapped,
            width=450,
            height=300,
            show=False,
        )
    spec = chart.to_dict()
    first = next(rows for rows in spec["datasets"].values() if "_value" in rows[0])[0]
    for width, height in ((450, 300), (600, 420)):
        bounds = render(page, chart.properties(width=width, height=height))
        canvas = page.locator("canvas").first.bounding_box()
        columns, rows = (9, 2) if swapped else (2, 9)
        px = canvas["x"] + bounds["x"] + bounds["width"] / columns / 2
        py = canvas["y"] + bounds["y"] + bounds["height"] / rows / 2
        page.mouse.move(px - 2, py - 2)
        page.wait_for_timeout(450)
        for dx in (0, 1, -1):
            page.mouse.move(px + dx, py)
            page.wait_for_timeout(80)
            if page.locator("table.attributes").is_visible():
                break
        page.locator("table.attributes").wait_for(state="visible")
        values = [
            row.locator("td").inner_text().strip()
            for row in page.locator("table.attributes tr").all()
        ]
        assert values[:4] == [
            first["_obs_id"],
            first["_obs_label"],
            first["_gene"],
            first["_group"],
        ]
        assert float(values[4]) == first["_value"]
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        page.mouse.wheel(0, -200)
        page.wait_for_timeout(80)
        assert (
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
            == svg
        )
    output = tmp_path / "heatmap.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
