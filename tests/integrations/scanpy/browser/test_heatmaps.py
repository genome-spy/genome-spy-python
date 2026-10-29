"""Heatmaps behavior and regressions."""

import json
import re
import warnings
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    pointer,
    position,
    svg_root,
    value_texts,
    wait_for_navigation,
)
from tests.integrations.scanpy.browser.rendering import (
    panel_image,
)
from tests.integrations.scanpy.browser.rendering import (
    render as matrix_render,
)
from tests.integrations.scanpy.browser.rendering import render as tracksplot_render
from tests.integrations.scanpy.browser.rendering import (
    render_heatmap as clustermap_render,
)
from tests.integrations.scanpy.browser.rendering import render_heatmap as heatmap_render
from tests.integrations.scanpy.expression_fixtures import (
    clustermap_cases,
    heatmap_cases,
    make_cluster_adata,
    make_heatmap_adata,
    matrix_cases,
)
from tests.integrations.scanpy.helpers import tree_paths, tree_segments, units
from tests.integrations.scanpy.paga_fixtures import make_adjacency

HEATMAP_FIXTURES = Path(__file__).parents[1] / "fixtures"
HEATMAP_REFERENCE = json.loads((HEATMAP_FIXTURES / "heatmap.json").read_text())


def heatmap_slot_bounds(slot, count, cuts, origin, extent):
    """Compute expected band edges independently from the native exported marks."""
    step = (extent - 4 * len(cuts)) / count
    start = origin + slot * step + 4 * sum((cut <= slot for cut in cuts))
    return (start, start + step)


def heatmap_tile_rects(root):
    """Read the matrix's exported tile rectangles in measurement order."""
    return list(next((e for e in root.iter() if e.get("data-mark-type") == "rect")))


class TestHeatmap:
    """Registered heatmap tiles, complete annotations, unequal trees and cell hover."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("swapped", [False, True])
    def test_small_terminal_group_label_is_whole_and_culls_on_zoom(self, page, swapped):
        from anndata import AnnData

        data = AnnData(
            np.arange(100, dtype=float).reshape(-1, 1),
            obs=pd.DataFrame(
                {
                    "group": pd.Categorical(
                        ["Other"] * 99 + ["CD34+"], categories=["Other", "CD34+"]
                    )
                },
                index=[f"cell-{i}" for i in range(100)],
            ),
            var=pd.DataFrame(index=["gene"]),
        )
        chart = gsc.pl.heatmap(
            data,
            ["gene"],
            "group",
            use_raw=False,
            swap_axes=swapped,
            group_gap=1,
            zoom="xy",
            width=200,
            height=200,
            show=False,
        )
        bounds = heatmap_render(page, chart)
        box = page.evaluate(
            "async () => {\n        const host = document.createElement('div');\n        host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        host.innerHTML = await (await api.imageExport.svg()).blob.text();\n        document.body.append(host);\n        const text = [...host.querySelectorAll('text')].find(e => e.textContent === 'CD34+');\n        const {x, y, width, height} = text.getBoundingClientRect();\n        host.remove();\n        return {x, y, width, height};\n    }"
        )
        canvas = page.locator("canvas").first.bounding_box()
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        # The last group's glyphs cross the matrix edge, but must remain fully painted.
        x0, y0 = (int(canvas["x"] + box["x"]), int(canvas["y"] + box["y"]))
        x1, y1 = (int(x0 + box["width"] + 1), int(y0 + box["height"] + 1))
        if swapped:
            x0 = int(np.ceil(canvas["x"] + bounds["x"] + bounds["width"]))
        else:
            y0 = int(np.ceil(canvas["y"] + bounds["y"] + bounds["height"]))
        assert (pixels[y0:y1, x0:x1].max(axis=2) < 100).sum() > 8
        axis = "x" if swapped else "y"
        page.evaluate(
            f"async () => api.getScaleResolutionByName('heatmap-{axis}').zoomTo([0, 60])"
        )
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        assert ">Other<" in svg
        assert ">CD34+<" not in svg

    @pytest.mark.parametrize(
        "page,swapped,hover,group_gap",
        [
            (1, False, True, 0),
            (1.5, False, True, 4),
            (1, True, True, 4),
            (1.5, True, False, 0),
            (1, False, False, 7),
            (1.5, True, True, 7),
        ],
        indirect=["page"],
    )
    def test_native_tracks_gaps_hover_and_navigation(
        self, page, swapped, hover, group_gap
    ):
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
        bounds = heatmap_render(page, chart)
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
                wait_for_navigation(page, "heatmap", probe=4)
                assert (
                    page.evaluate(
                        "api.getScaleResolutionByName('heatmap-y').getDomain()"
                    )
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
            assert strip_bounds[cell_extent] == pytest.approx(
                bounds[cell_extent], abs=0.2
            )
            assert tree_bounds[cell_axis] == pytest.approx(bounds[cell_axis], abs=0.2)
            assert tree_bounds[cell_extent] == pytest.approx(
                bounds[cell_extent], abs=0.2
            )
            edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
            assert (
                tree_bounds["y"] + tree_bounds["height"]
                if swapped
                else tree_bounds["x"]
            ) == pytest.approx(edge, abs=0.2)
            across = "y" if swapped else "x"
            strip_group = next(
                (
                    e
                    for e in root.iter()
                    if e.get("data-mark-type") == "rect"
                    and len(e)
                    and (abs(float(e[0].get(across)) - strip_bounds[across]) < 1)
                )
            )
            tiles = heatmap_tile_rects(root)
            for cell, strip in enumerate(strip_group):
                for field in (cell_axis, cell_extent):
                    tile = next(
                        (
                            tile
                            for tile in tiles
                            if abs(
                                float(tile.get(cell_axis)) - float(strip.get(cell_axis))
                            )
                            < 0.2
                        )
                    )
                    assert float(strip.get(field)) == pytest.approx(
                        float(tile.get(field)), abs=0.2
                    )
            groups = {
                e.text: e
                for e in root.iter()
                if e.tag.endswith("text") and e.text in {"A", "B", "C", "D"}
            }
            tree = next((e for e in root.iter() if e.get("stroke") == "#555555"))
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
                        (
                            j != i
                            and all(
                                (
                                    min(a[k], b[k]) - 0.2
                                    <= xy[k]
                                    <= max(a[k], b[k]) + 0.2
                                    for k in (0, 1)
                                )
                            )
                            for j, (a, b) in enumerate(segments)
                        )
                    ), (xy, segments)
            leaves = [
                xy[0 if swapped else 1]
                for xy in endpoints
                if abs(xy[1 if swapped else 0] - edge) < 1
            ]
            for label in groups.values():
                position = [
                    float(v)
                    for v in re.search("translate\\(([^)]+)\\)", label.get("transform"))
                    .group(1)
                    .split()
                ]
                assert any(
                    (abs(leaf - position[0 if swapped else 1]) < 0.2 for leaf in leaves)
                )
            # Read the live gapped scale for pointer targets, independently of SVG export.
            live = page.evaluate(
                "axis=>{\n            const scale=api.getScaleResolutionByName(`heatmap-${axis}`).getScale();\n            const width=scale.bandwidth();\n            const sign=axis==='x' ? 1 : -1;\n            const pixel=v=>axis==='x' ? v : 1-v;\n            return {\n                centers:Array.from({length:9},(_,i)=>pixel(scale(i)+sign*width/2)),\n                gaps:[3,4,7].map(cut=>pixel((scale(cut-1)+sign*width+scale(cut))/2)),\n            };\n        }",
                cell_axis,
            )
            visible = [
                i
                for i, fraction in enumerate(live["centers"])
                if 0.05 < fraction < 0.95
            ]
            cell = visible[len(visible) // 2]
            fraction = live["centers"][cell]
            x = strip_bounds["x"] + strip_bounds["width"] * (
                fraction if swapped else 0.5
            )
            y = strip_bounds["y"] + strip_bounds["height"] * (
                0.5 if swapped else fraction
            )
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
                    (
                        abs(
                            float(b.get(cell_axis))
                            - float(a.get(cell_axis))
                            - float(a.get(cell_extent))
                        )
                        < 0.31
                        for a, b in zip(ordered[:-1], ordered[1:], strict=True)
                    )
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
            fraction = next((f for f in live["gaps"] if 0.05 < f < 0.95))
            middle = bounds[cell_axis] + fraction * bounds[cell_extent]
            hover_at(
                page, middle if swapped else x, y if swapped else middle, probe=False
            )
            assert not page.locator("table.attributes").is_visible(), (
                navigated,
                middle,
            )
            hover_at(
                page,
                middle if swapped else bounds["x"] + 30,
                bounds["y"] + 30 if swapped else middle,
                probe=False,
            )
            assert not page.locator("table.attributes").is_visible()

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", heatmap_cases())
    def test_complete_registered_heatmaps(self, page, tmp_path, reference_images, case):
        reference = HEATMAP_REFERENCE["cases"][case]
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
        bounds = heatmap_render(page, chart)
        canvas = page.locator("canvas").first.bounding_box()
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        for text in set(
            reference["x_labels"] + reference["y_labels"] + reference["group_labels"]
        ):
            if text:
                assert f">{text}<" in svg, (case, text)
        left, top = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
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
        rects = heatmap_tile_rects(ET.fromstring(svg))
        registered = Image.new("RGB", actual.size, "white")
        for row, column in np.ndindex(values.shape):
            x0, x1 = heatmap_slot_bounds(
                column, values.shape[1], cuts_x, 0, bounds["width"]
            )
            y0, y1 = heatmap_slot_bounds(
                row, values.shape[0], cuts_y, 0, bounds["height"]
            )
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
            box = tuple((round(v * actual.width / bounds["width"]) for v in (x0, x1)))
            rows = tuple(
                (round(v * actual.height / bounds["height"]) for v in (y0, y1))
            )
            registered.paste(
                crop.resize((box[1] - box[0], rows[1] - rows[0])), (box[0], rows[0])
            )
        # The rendered rectangles must occupy the independently calculated gapped slots.
        records = next(
            (
                rows
                for rows in chart.to_dict()["datasets"].values()
                if "_value" in rows[0]
            )
        )
        expected_rects = []
        for record in records:
            if record["_value"] is None:
                continue
            x0, x1 = heatmap_slot_bounds(
                record["_x"], values.shape[1], cuts_x, bounds["x"], bounds["width"]
            )
            y0, y1 = heatmap_slot_bounds(
                record["_y"], values.shape[0], cuts_y, bounds["y"], bounds["height"]
            )
            expected_rects.append([x0, y0, x1 - x0, y1 - y0])
        actual_rects = sorted(
            (
                [float(rect.get(k)) for k in ("x", "y", "width", "height")]
                for rect in rects
            )
        )
        np.testing.assert_allclose(actual_rects, sorted(expected_rects), atol=1)
        # Register stored upstream branches through the same expected slot mapping.
        swapped = options.get("swap_axes", False)
        paths = reference["tree_paths"]
        maximum = (
            max(
                (point[1 if swapped else 0] for path in paths for point in path),
                default=1,
            )
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
                start, stop = heatmap_slot_bounds(
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
                        left
                        + bounds["width"]
                        + point[0] / maximum * tree_bounds["width"],
                        along,
                    )
                )
            for start, stop in zip(projected[:-1], projected[1:], strict=True):
                for fraction in (0.25, 0.5, 0.75):
                    px, py = np.round(
                        (np.array(start) + (np.array(stop) - start) * fraction) * 1.5
                    ).astype(int)
                    region = screenshot[py - 3 : py + 4, px - 3 : px + 4].astype(int)
                    assert region.size and np.any(
                        np.abs(region - 85).max(axis=2) < 40
                    ), (case, start, stop)
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
    def test_cell_hover_after_tree_reordering_and_resize(self, page, tmp_path, swapped):
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
        first = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )[0]
        for width, height in ((450, 300), (600, 420)):
            bounds = heatmap_render(page, chart.properties(width=width, height=height))
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


MATRIX_FIXTURES = Path(__file__).parents[1] / "fixtures"
MATRIX_REFERENCE = json.loads((MATRIX_FIXTURES / "matrix.json").read_text())["cases"]


class TestMatrix:
    """Registered matrix colors/labels, native hover and standalone HTML delivery."""

    @pytest.mark.parametrize("family", ["matrix", "paga_adjacency"])
    @pytest.mark.parametrize("zoom", [True, "xy"])
    def test_composition_keeps_native_matrix_navigation_independent(
        self, page, tmp_path, family, zoom
    ):
        source = make_adjacency()
        if family == "matrix":
            source = source.uns["connectivities"].toarray()
        chart = getattr(gsc.pl, family)(
            source, zoom=zoom, show_values=True, width=280, height=240, show=False
        )
        combined = (
            (chart | chart)
            .resolve_scale(default="independent")
            .resolve_legend(default="independent")
        )
        bounds = matrix_render(page, combined)

        def rectangles():
            """Read tile geometry relative to each panel so guide resizing cannot mimic zoom."""
            groups = [
                g
                for g in svg_root(page).iter()
                if g.get("data-mark-type") == "rect" and g.get("clip-path")
            ]
            assert len(groups) == 2
            result = []
            for i, group in enumerate(groups):
                panel = page.evaluate(
                    "i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i
                )
                values = np.array(
                    [
                        [float(e.get(k)) for k in ("x", "y", "width", "height")]
                        for e in group
                    ]
                )
                values[:, :2] -= [panel["x"], panel["y"]]
                result.append(values)
            return result

        before = rectangles()
        assert all((len(rows) == 9 for rows in before))
        px, py = pointer(page, bounds)
        page.mouse.wheel(0, -120)
        page.wait_for_timeout(700)
        zoomed = rectangles()
        assert not np.array_equal(zoomed[0], before[0])
        np.testing.assert_allclose(zoomed[1], before[1], atol=0.01)
        assert bool(zoomed[0][0, 2] > before[0][0, 2] + 1) is (zoom == "xy")
        assert zoomed[0][0, 3] > before[0][0, 3] + 1
        page.mouse.down()
        page.mouse.move(px + 8, py + 8, steps=5)
        page.mouse.up()
        page.wait_for_timeout(700)
        panned = rectangles()
        assert not np.array_equal(panned[0], zoomed[0])
        np.testing.assert_allclose(panned[1], before[1], atol=0.01)
        other = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
        hover_at(
            page, other["x"] + other["width"] * 5 / 6, other["y"] + other["height"] / 6
        )
        values = [
            v.strip() for v in page.locator("table.attributes td").all_text_contents()
        ]
        assert values[:2] == ["0", "2"]
        assert float(values[2]) == pytest.approx(0.6)
        output = tmp_path / f"{family}-composition.html"
        combined.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    @pytest.mark.parametrize("page", [1, 2], indirect=True)
    @pytest.mark.parametrize("zoom", [True, "xy"])
    def test_matrix_side_labels_follow_zoom_pan_and_resize(self, page, zoom):
        spec = gsc.pl.matrix(
            np.arange(144).reshape(12, 12),
            xticks=[f"gene{i}" for i in range(12)],
            yticks=[f"group{i}" for i in range(12)],
            zoom=zoom,
            show=False,
        ).to_dict()
        for side in ("bottom", "left"):
            spec["surround"][side][0]["name"] = f"test-{side}"
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"matrix-{axis}"
        for width, height in ((240, 200), (400, 280)):
            spec["spec"].update(width=width, height=height)
            bounds = matrix_render(page, gs.TopLevelSpec.from_dict(spec))
            original = page.evaluate(
                "api.getScaleResolutionByName('matrix-x').getDomain()"
            )
            for navigated in (False, True):
                if navigated:
                    px, py = pointer(page, bounds)
                    page.mouse.wheel(0, -250)
                    page.wait_for_timeout(250)
                    page.mouse.down()
                    page.mouse.move(px + 15, py + 15, steps=5)
                    page.mouse.up()
                    page.wait_for_timeout(700)
                root = svg_root(page)
                for axis, side, prefix in (
                    ("x", "bottom", "gene"),
                    ("y", "left", "group"),
                ):
                    track = page.evaluate(
                        "view=>api.views.getLayoutBounds({scope:[],view})",
                        f"test-{side}",
                    )
                    assert track["width" if axis == "x" else "height"] == pytest.approx(
                        bounds["width" if axis == "x" else "height"]
                    )
                    centers = page.evaluate(
                        "axis=>{const s=api.getScaleResolutionByName(`matrix-${axis}`).getScale();\n                    return Array.from({length:12},(_,i)=>axis==='x'\n                        ?s(i)+s.bandwidth()/2:1-s(i)+s.bandwidth()/2)}",
                        axis,
                    )
                    labels = [
                        e
                        for e in root.iter()
                        if e.tag.endswith("text") and (e.text or "").startswith(prefix)
                    ]
                    assert labels
                    for label in labels:
                        slot = int(label.text.removeprefix(prefix))
                        xy = position(label)
                        value = xy[0 if axis == "x" else 1]
                        assert value == pytest.approx(
                            bounds[axis]
                            + centers[slot]
                            * bounds["width" if axis == "x" else "height"],
                            abs=0.6,
                        ), (
                            label.text,
                            navigated,
                            bounds,
                            centers[slot],
                            ET.tostring(label),
                        )
                        # Native clipping can retain a partly visible label's outside anchor.
                        cross, extent = (
                            ("y", "height") if axis == "x" else ("x", "width")
                        )
                        assert (
                            track[cross]
                            <= xy[1 if axis == "x" else 0]
                            <= track[cross] + track[extent]
                        )
            assert (
                page.evaluate("api.getScaleResolutionByName('matrix-x').getDomain()")
                != original
            ) is (zoom == "xy")

    @pytest.mark.parametrize("explicit_labels", [False, True])
    @pytest.mark.parametrize("titles", ["both", "x", "y"])
    def test_axis_titles_do_not_duplicate_outer_label_space(
        self, page, explicit_labels, titles
    ):
        labels = ["CD4+/CD45RA+/CD25- Naive T", "CD8+/CD45RA+ Naive Cytotoxic"]
        chart = gsc.pl.matrix(
            [[0, 1], [2, 3]],
            xticks=labels if explicit_labels else None,
            yticks=labels if explicit_labels else None,
            xlabel="Columns" if titles in ("both", "x") else None,
            ylabel="Rows" if titles in ("both", "y") else None,
            width=400,
            height=350,
            show=False,
        )
        bounds = matrix_render(page, chart)
        assert abs(bounds["width"] - 400) < 1
        assert abs(bounds["height"] - 350) < 1
        root = ET.fromstring(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
        positions = {
            e.text: [
                float(v)
                for v in re.search("translate\\(([^)]+)\\)", e.get("transform"))
                .group(1)
                .split()
            ]
            for e in root.iter()
            if e.tag.endswith("text") and e.text in ("Rows", "Columns")
        }
        canvas_height = page.evaluate("api.getLogicalCanvasSize().height")
        if "Rows" in positions:
            assert 0 < positions["Rows"][0] < 35
        if "Columns" in positions:
            assert 0 < canvas_height - positions["Columns"][1] < 35

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", matrix_cases())
    def test_complete_matrix_tiles_and_labels(
        self, page, tmp_path, reference_images, case
    ):
        values, options = matrix_cases()[case]
        reference = MATRIX_REFERENCE[case]
        chart = gsc.pl.matrix(
            values,
            width=reference["plot_size"][0],
            height=reference["plot_size"][1],
            show=False,
            **options,
        )
        bounds = matrix_render(page, chart)
        actual = panel_image(page, bounds)
        expected = Image.open(
            reference_images("matrix") / f"matrix-{case}-panel.png"
        ).convert("RGB")
        assert (
            abs(actual.width - expected.width) <= 2
            and abs(actual.height - expected.height) <= 2
        )
        pixels, target = (
            np.asarray(actual).astype(int),
            np.asarray(expected).astype(int),
        )
        for row, column in np.ndindex(values.shape):
            for fraction in (0.25, 0.75):
                x, y = (
                    (column + fraction) / values.shape[1],
                    (row + fraction) / values.shape[0],
                )
                np.testing.assert_allclose(
                    pixels[int(y * actual.height), int(x * actual.width)],
                    target[int(y * expected.height), int(x * expected.width)],
                    atol=12,
                )
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        (tmp_path / f"{case}.svg").write_text(svg)
        gradients = [
            element
            for element in ET.fromstring(svg).iter()
            if element.tag.endswith("rect")
            and element.get("fill", "").startswith("url(")
        ]
        assert gradients, svg[-2000:]
        assert (
            abs(
                float(gradients[0].get("height"))
                - reference["plot_size"][1] * options.get("colorbar_shrink", 0.5)
            )
            < 2
        )
        assert float(gradients[0].get("x")) > bounds["x"] + bounds["width"]
        assert float(gradients[0].get("y")) + float(
            gradients[0].get("height")
        ) / 2 == pytest.approx(bounds["y"] + bounds["height"] / 2, abs=1)
        for label in (
            list(options.get("xticks", []))
            + list(options.get("yticks", []))
            + [reference["title"], reference["xlabel"], reference["ylabel"]]
        ):
            if label:
                assert f">{label}<" in svg
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

    def test_matrix_hover_resize_and_offline_delivery(self, page, tmp_path):
        chart = gsc.pl.matrix(
            [[0, 1, 2], [3, 4, 5]],
            xticks=["A", "B", "C"],
            yticks=["first", "last"],
            show=False,
        )
        for size in (300, 450):
            bounds = matrix_render(
                page, chart.properties(width=size, height=size * 2 / 3)
            )
            canvas = page.locator("canvas").first.bounding_box()
            px = canvas["x"] + bounds["x"] + bounds["width"] / 2
            py = canvas["y"] + bounds["y"] + bounds["height"] * 0.75
            page.mouse.move(px - 2, py - 2)
            page.wait_for_timeout(450)
            for dx in (0, 1, -1):
                page.mouse.move(px + dx, py)
                page.wait_for_timeout(80)
                if page.locator("table.attributes").is_visible():
                    break
            page.locator("table.attributes").wait_for(state="visible")
            hover_values = [
                row.locator("td").inner_text().strip()
                for row in page.locator("table.attributes tr").all()
            ]
            assert hover_values[:2] == ["last", "B"]
            assert float(hover_values[2]) == 4
        output = tmp_path / "matrix.html"
        chart.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


CLUSTERMAP_REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/clustermap.json").read_text()
)["cases"]


class TestClustermap:
    """Registered clustermap tiles, branches, labels, color tracks and native hover."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", clustermap_cases())
    def test_complete_registered_tiles_trees_and_labels(
        self, page, tmp_path, reference_images, case
    ):
        reference = CLUSTERMAP_REFERENCE[case]
        chart = gsc.pl.clustermap(
            make_cluster_adata(),
            show=False,
            cmap="viridis",
            width=reference["plot_size"][0],
            height=reference["plot_size"][1],
            **clustermap_cases()[case],
        )
        bounds = clustermap_render(page, chart)
        canvas = page.locator("canvas").first.bounding_box()
        left, top = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        width, height = (bounds["width"], bounds["height"])
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
        pixels, target = (
            np.asarray(actual).astype(int),
            np.asarray(expected).astype(int),
        )
        for row, column in np.ndindex(6, 4):
            x, y = ((column + 0.3) / 4, (row + 0.3) / 6)
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
            maximum = 1.05 * (max((max(branch) for branch in tree["dcoord"])) or 1)
            track = (
                width * 0.03 / 0.77 if case == "row_annotation" and axis == "row" else 0
            )
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
                    px, py = (round(x * 1.5), round(y * 1.5))
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
                        [parent[0], target[1]]
                        if axis == "row"
                        else [target[0], parent[1]]
                    )
                    expected_paths.append([parent, elbow, target])
        actual_paths = tree_paths(svg_root(page))
        np.testing.assert_allclose(
            sorted(actual_paths), sorted(expected_paths), atol=0.6
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

    def test_hover_tracks_supplied_order_resize_and_offline_html(self, page, tmp_path):
        data = make_cluster_adata()
        chart = gsc.pl.clustermap(
            data, obs_keys="group", show=False, width=300, height=240, cmap="viridis"
        )
        for size in (300, 450):
            bounds = clustermap_render(
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
            ref = CLUSTERMAP_REFERENCE["default"]
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
    def test_native_category_legend_matches_strip_and_stays_visible_during_zoom(
        self, page, zoom
    ):
        from PIL import ImageColor

        data = make_cluster_adata()
        data.obs.loc["cell-0", "group"] = np.nan
        chart = gsc.pl.clustermap(
            data, obs_keys="group", zoom=zoom, width=300, height=240, show=False
        )
        bounds = clustermap_render(page, chart)
        guide_bounds = page.evaluate(
            "async () => {\n        const host = document.createElement('div');\n        host.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        host.innerHTML = await (await api.imageExport.svg()).blob.text();\n        document.body.append(host);\n        const chart = host.querySelector('svg').getBoundingClientRect();\n        const legend = host.querySelector('[data-name=\"legend_region_right\"]')\n            .getBoundingClientRect();\n        host.remove();\n        return {top: legend.top-chart.top, bottom: chart.bottom-legend.bottom,\n                left: legend.left-chart.left};\n    }"
        )
        assert guide_bounds["left"] > bounds["x"] + bounds["width"]
        assert guide_bounds["top"] > 0
        assert guide_bounds["top"] == pytest.approx(guide_bounds["bottom"], abs=10)
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
                and any((t.tag.endswith("text") and t.text == "C" for t in e.iter()))
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
                (
                    bounds["x"] + bounds["width"] < x < size["width"]
                    and 0 <= y < size["height"]
                    for x, y in labels
                )
            )
            if not navigated:
                canvas = page.locator("canvas").first.bounding_box()
                pixels = np.asarray(
                    Image.open(BytesIO(page.screenshot())).convert("RGB")
                )
                slot = CLUSTERMAP_REFERENCE["default"]["row_order"].index(0)
                x = round(canvas["x"] + bounds["x"] - bounds["width"] * 0.03 / 0.77 / 2)
                y = round(
                    canvas["y"] + bounds["y"] + (slot + 0.5) / 6 * bounds["height"]
                )
                np.testing.assert_array_equal(pixels[y, x], [255, 255, 255])

    @pytest.mark.parametrize("named", [False, True])
    def test_multiple_positional_and_indexed_tracks_on_both_axes(self, page, named):
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
        bounds = clustermap_render(page, chart)
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        if named:
            labels = ["Long observation annotation", "second", "Long gene annotation"]
            assert all((f">{label}<" in svg for label in labels))
            boxes = page.evaluate(
                "async (labels) => {\n            const host=document.createElement('div');\n            host.innerHTML=await (await api.imageExport.svg()).blob.text();\n            document.body.append(host);\n            const root=host.querySelector('svg').getBoundingClientRect();\n            const result=[...host.querySelectorAll('text')].filter(t=>labels.includes(t.textContent)).map(t=>{\n                const b=t.getBoundingClientRect();\n                return {left:b.left-root.left,top:b.top-root.top,right:b.right-root.left,bottom:b.bottom-root.top};\n            });\n            host.remove(); return result;\n        }",
                labels,
            )
            size = page.evaluate("api.getLogicalCanvasSize()")
            assert len(boxes) == 3
            assert all(
                (
                    b["left"] >= 0
                    and b["top"] >= 0
                    and (b["right"] <= size["width"] + 1)
                    and (b["bottom"] <= size["height"] + 1)
                    for b in boxes
                )
            )
        canvas = page.locator("canvas").first.bounding_box()
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        left, top = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        # Check the original-color identity after both permutations, away from borders.
        from PIL import ImageColor

        for slot, original in enumerate(CLUSTERMAP_REFERENCE["default"]["row_order"]):
            x = round(left - bounds["width"] * 0.03 / 0.74 * 1.5)
            y = round(top + (slot + 0.5) / 6 * bounds["height"])
            np.testing.assert_allclose(
                pixels[y, x].astype(int), ImageColor.getrgb(rows[original]), atol=2
            )
        for slot, original in enumerate(CLUSTERMAP_REFERENCE["default"]["col_order"]):
            x = round(left + (slot + 0.5) / 4 * bounds["width"])
            y = round(top - bounds["height"] * 0.03 / 0.77 / 2)
            np.testing.assert_allclose(
                pixels[y, x].astype(int), ImageColor.getrgb(columns[original]), atol=2
            )

    @pytest.mark.parametrize("zoom", [True, "xy"])
    def test_navigation_keeps_both_trees_strips_and_labels_aligned(
        self, page, zoom, tmp_path
    ):
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
        bounds = clustermap_render(page, chart)
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
            centers = page.evaluate(
                "() => ['y','x'].map(axis=>{\n            const s=api.getScaleResolutionByName(`clustermap-${axis}`).getScale();\n            return Array.from({length:axis==='y'?6:4},(_,i)=>axis==='y'?1-s(i)+s.bandwidth()/2:s(i)+s.bandwidth()/2);\n        })"
            )
            trees, strips = ([], [])
            for side in ("left", "top"):
                tree_view = next(
                    (
                        e
                        for e in root.iter()
                        if e.get("data-view-path", "").endswith(
                            f"/clustermap-{side}-tree"
                        )
                    )
                )
                strip_view = next(
                    (
                        e
                        for e in root.iter()
                        if e.get("data-view-path", "").endswith(
                            f"/clustermap-{side}-colors-0"
                        )
                    )
                )
                trees.append(
                    next((e for e in tree_view.iter() if e.get("stroke") == "#555555"))
                )
                strips.append(
                    list(
                        next(
                            (
                                e
                                for e in strip_view.iter()
                                if e.get("data-mark-type") == "rect"
                            )
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
                assert any((e.get("clip-path") for e in root.iter()))
                order = CLUSTERMAP_REFERENCE["default"][
                    "row_order" if axis else "col_order"
                ]
                visible = 0
                for slot, original in enumerate(order):
                    fraction = centers[0 if axis else 1][slot]
                    if not 0 < fraction < 1:
                        continue
                    visible += 1
                    center = start + fraction * extent
                    label = next(
                        (
                            e
                            for e in root.iter()
                            if e.tag.endswith("text") and e.text == labels[original]
                        )
                    )
                    assert position(label)[axis] == pytest.approx(center, abs=1)
                    assert any(
                        (abs(leaf - position(label)[axis]) < 1 for leaf in leaves)
                    )
                    rectangle = next(
                        (
                            r
                            for r in strip
                            if float(r.get(channel))
                            <= center
                            <= float(r.get(channel))
                            + float(r.get("height" if axis else "width"))
                        )
                    )
                    from PIL import ImageColor

                    assert ImageColor.getrgb(
                        rectangle.get("fill")
                    ) == ImageColor.getrgb(colors[original])
                assert visible > 0
        # The declarative chart must also render in offline HTML.
        output = tmp_path / "clustermap-navigation.html"
        chart.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestTracksplot:
    """Observed native track registration, hover, legends and linked navigation."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("log", [False, True])
    @pytest.mark.parametrize("group_gap", [0, 5])
    @pytest.mark.parametrize("page", [1, 1.5], indirect=True)
    def test_tracks_tree_hover_and_linked_x_zoom(self, page, log, group_gap):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            a = make_heatmap_adata()
        chart = gsc.pl.tracksplot(
            a,
            {"First": ["g1", "g2"], "Last": ["g3"]},
            "group",
            dendrogram=True,
            log=log,
            zoom=True,
            group_gap=group_gap,
            spacing=7 if group_gap else 0,
            width=540,
            height=180,
            show=False,
        )
        spec = chart.to_dict()
        spec["scales"]["x"]["name"] = "cells"
        tracksplot_render(page, spec)
        boxes = [
            page.evaluate(f"api.views.getLayoutBounds({{scope:[],view:'panel-{i}'}})")
            for i in range(5)
        ]
        assert all((box["width"] == pytest.approx(540) for box in boxes)), boxes
        assert len({round(box["x"], 2) for box in boxes}) == 1
        for previous, current in zip(boxes, boxes[1:]):
            assert current["y"] - previous["y"] - previous["height"] == pytest.approx(
                7 if group_gap else 0
            )
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        labels = [
            element.text for element in root.iter() if element.tag.endswith("}text")
        ]
        assert all(
            (
                label in labels
                for label in ["g1", "g2", "g3", "group", "C", "A", "D", "B"]
            )
        )
        assert tree_segments(root)
        # Native SVG rects expose actual cell footprints, not just a generated spec.
        rect_groups = [
            element
            for element in root.iter()
            if element.get("data-mark-type") == "rect"
        ]
        profiles = [group for group in rect_groups if len(list(group)) > 1][:3]
        assert len(profiles) == 3
        cells = spec["datasets"][spec["data"]["name"]]
        cuts = [3, 4, 7]
        step = (540 - len(cuts) * group_gap) / 9

        def cell_left(row):
            return row["_cell"] * step + group_gap * sum(
                (cut <= row["_cell"] for cut in cuts)
            )

        for slot, (group, bounds) in enumerate(zip(profiles, boxes[1:4], strict=True)):
            domain = units(spec)[slot + 1]["layer"][0]["encoding"]["y"]["scale"][
                "domain"
            ]
            low, high = np.log(domain) if log else domain
            visible = [row for row in cells if not log or row[f"_value_{slot}"] > 0]
            rects = list(group)
            assert len(rects) == len(visible)
            for rect, row in zip(rects, visible, strict=True):
                value = row[f"_value_{slot}"]
                transformed = np.log(value) if log else value
                top = (
                    bounds["y"] + (high - transformed) / (high - low) * bounds["height"]
                )
                baseline = (
                    bounds["y"] + (1 if log else high / (high - low)) * bounds["height"]
                )
                # Native SVG rects include a subpixel overlap to avoid seams.
                assert float(rect.get("x")) == pytest.approx(
                    bounds["x"] + cell_left(row), abs=0.25
                )
                assert float(rect.get("y")) == pytest.approx(top, abs=0.25)
                assert float(rect.get("width")) == pytest.approx(step, abs=0.31)
                assert float(rect.get("height")) == pytest.approx(
                    baseline - top, abs=0.31
                )
        probe = max(cells, key=lambda row: row["_value_0"])
        bounds = boxes[1]
        hover_at(page, bounds["x"] + cell_left(probe) + step / 2, bounds["y"] + 30)
        tooltip = page.locator("table.attributes")
        assert probe["_obs_id"] in tooltip.inner_text()
        assert "g1 expression" in tooltip.inner_text()
        strip = boxes[-1]
        hover_at(page, strip["x"] + 30, strip["y"] + 7)
        assert page.locator("table.attributes").is_visible()
        assert "group" in page.locator("table.attributes").inner_text()
        canvas = page.locator("canvas").first.bounding_box()
        track = boxes[1]
        page.mouse.move(canvas["x"] + track["x"] + 270, canvas["y"] + track["y"] + 30)
        before = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
        page.mouse.wheel(0, -250)
        # Finish native wheel animation before measuring the pan.
        page.evaluate(
            "async () => {\n        const scale = api.getScaleResolutionByName('cells');\n        let previous = scale.getDomain().slice(), stable = 0;\n        while (stable < 3) {\n            await new Promise(requestAnimationFrame);\n            const current = scale.getDomain();\n            stable = current.every((value, i) => value === previous[i]) ? stable + 1 : 0;\n            previous = current.slice();\n        }\n    }"
        )
        after = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
        assert np.ptp(after) < np.ptp(before)
        page.mouse.down()
        page.mouse.move(
            canvas["x"] + track["x"] + 320, canvas["y"] + track["y"] + 30, steps=5
        )
        page.mouse.up()
        page.wait_for_timeout(100)
        panned = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
        assert panned[0] < after[0] and panned[1] < after[1]
        assert np.ptp(panned) < np.ptp(before)
        # Fixed pixel gaps entering/leaving the viewport can change the data span.
        if not group_gap:
            assert np.ptp(panned) == pytest.approx(np.ptp(after))
        assert "NaN" not in page.evaluate(
            "async () => (await api.imageExport.svg()).blob.text()"
        )
