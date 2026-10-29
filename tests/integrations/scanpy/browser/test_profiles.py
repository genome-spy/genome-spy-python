"""Profiles behavior and regressions."""

import warnings
import xml.etree.ElementTree as ET

import numpy as np
import pytest
from PIL import Image

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    point_coordinates,
    point_spacing,
    pointer,
    position,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.browser.rendering import (
    panel_image,
    style_profile_reference,
)
from tests.integrations.scanpy.browser.rendering import render as presentation_render
from tests.integrations.scanpy.browser.rendering import (
    render as timeseries_heatmap_render,
)
from tests.integrations.scanpy.browser.rendering import (
    render as timeseries_render,
)
from tests.integrations.scanpy.browser.rendering import render_heatmap as sim_render
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.paga_fixtures import (
    POSITIONS,
    make_adjacency,
    make_compare,
    make_paga,
    make_path,
)
from tests.integrations.scanpy.profile_fixtures import (
    make_sim,
    sim_cases,
    timeseries_cases,
)
from tests.integrations.scanpy.qc_fixtures import make_hvg_result


class TestTimeseries:
    """Native time-series point footprints, guides, hover, zoom and offline delivery."""

    @pytest.mark.reference
    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    @pytest.mark.parametrize("case", timeseries_cases())
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_time_series_native_points_and_guides(
        self, page, tmp_path, case, family
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc

        values, options = timeseries_cases()[case]
        with (
            mpl.rc_context({"figure.dpi": 100, "font.size": 10}),
            warnings.catch_warnings(),
        ):
            warnings.simplefilter("ignore")
            getattr(sc.pl, family)(values, **options)
            fig, ax = (plt.gcf(), plt.gcf().axes[0])
            style_profile_reference(ax)
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
        chart = getattr(gsc.pl, family)(
            values, width=bbox.width, height=bbox.height, show=False, **options
        )
        bounds = timeseries_render(page, chart)
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
                if e.get("data-mark-type") == "point" and (not e.get("clip-path"))
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
        actual = panel_image(page, bounds)
        target, pixels = (
            np.asarray(expected).astype(int),
            np.asarray(actual).astype(int),
        )
        for time, value in xy:
            x = (time - domains[0][0]) / (domains[0][1] - domains[0][0])
            y = 1 - (value - domains[1][0]) / (domains[1][1] - domains[1][0])
            if not (0.02 < x < 0.98 and 0.02 < y < 0.98):
                continue
            # Compare local paint areas as well as centers to catch incorrect marker sizes.
            xp, yp = (int(x * actual.width), int(y * actual.height))
            xq, yq = (int(x * expected.width), int(y * expected.height))
            a = pixels[yp - 5 : yp + 6, xp - 5 : xp + 6]
            b = target[yq - 5 : yq + 6, xq - 5 : xq + 6]
            # Nearby overlapping points cannot measure one symbol's footprint reliably.
            projected = (xy - [domains[0][0], domains[1][0]]) / [
                np.ptp(domains[0]),
                np.ptp(domains[1]),
            ]
            isolated = (
                np.count_nonzero(
                    np.max(
                        np.abs(
                            (projected - [x, 1 - y]) * [actual.width, actual.height]
                        ),
                        axis=1,
                    )
                    < 10
                )
                == 1
            )
            if isolated:
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

    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    def test_hover_and_both_native_axes_navigate_and_export_offline(
        self, page, tmp_path, family
    ):
        values = np.arange(60, dtype=float).reshape(30, 2)
        chart = getattr(gsc.pl, family)(
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
        bounds = timeseries_render(page, chart)
        point = next(
            (
                m
                for m in leaf_marks(chart.to_dict())
                if m.get("mark", {}).get("type") == "point"
            )
        )
        domains = {
            axis: point["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")
        }
        x = bounds["x"] + bounds["width"] * (20 - domains["x"][0]) / np.ptp(
            domains["x"]
        )
        y = bounds["y"] + bounds["height"] * (
            1 - (20 - domains["y"][0]) / np.ptp(domains["y"])
        )
        hover_at(page, x, y)
        page.locator("table.attributes").wait_for(state="visible")
        cells = [
            s.strip() for s in page.locator("table.attributes td").all_text_contents()
        ]
        assert cells == ["A", "10", "20.00", "20.00"]
        before = point_coordinates(page)[0]
        page.mouse.wheel(0, -300)
        page.wait_for_timeout(700)
        moved = point_coordinates(page)[0]
        assert all((np.ptp(moved[:, i]) > np.ptp(before[:, i]) for i in (0, 1)))
        canvas = page.locator("canvas").first.bounding_box()
        page.mouse.move(canvas["x"] + x, canvas["y"] + y)
        page.mouse.down()
        page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
        page.mouse.up()
        page.wait_for_timeout(700)
        assert not np.array_equal(point_coordinates(page)[0], moved)
        path = tmp_path / "timeseries.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    def test_subplot_composition_keeps_colors_hover_and_navigation_independent(
        self, page, tmp_path
    ):
        values = np.arange(30, dtype=float)
        options = dict(marker="o", zoom=True, width=280, height=220, show=False)
        left = gsc.pl.timeseries_subplot(
            values,
            color=np.where(values % 2 == 0, "A", "B"),
            var_names=["A", "B"],
            **options,
        )
        right = gsc.pl.timeseries_subplot(
            values, color=values / 29, var_names=["Value"], **options
        )
        chart = (
            gs.hconcat(left, right, spacing=30)
            .resolve_scale(default="independent")
            .resolve_legend(default="independent")
        )
        bounds = timeseries_render(page, chart)
        other = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
        before = point_coordinates(page)
        assert len(before) == 2 and all((len(points) == 30 for points in before))
        fraction = (10 + 1.45) / 31.9
        x = bounds["x"] + fraction * bounds["width"]
        y = bounds["y"] + (1 - fraction) * bounds["height"]
        hover_at(page, x, y)
        page.locator("table.attributes").wait_for(state="visible")
        cells = [
            v.strip() for v in page.locator("table.attributes td").all_text_contents()
        ]
        assert cells == ["A", "10", "10.00", "10.00"]
        page.mouse.wheel(0, -300)
        page.wait_for_timeout(700)
        zoomed = point_coordinates(page)
        assert not np.array_equal(zoomed[0], before[0])
        np.testing.assert_allclose(zoomed[1], before[1])
        canvas = page.locator("canvas").first.bounding_box()
        page.mouse.move(canvas["x"] + x, canvas["y"] + y)
        page.mouse.down()
        page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
        page.mouse.up()
        page.wait_for_timeout(700)
        panned = point_coordinates(page)
        assert not np.array_equal(panned[0], zoomed[0])
        np.testing.assert_allclose(panned[1], before[1])
        hover_at(
            page,
            other["x"] + fraction * other["width"],
            other["y"] + (1 - fraction) * other["height"],
        )
        page.locator("table.attributes").wait_for(state="visible")
        cells = [
            v.strip() for v in page.locator("table.attributes td").all_text_contents()
        ]
        assert cells[:4] == ["Value", "10", "10.00", "10.00"]
        assert float(cells[4]) == pytest.approx(10 / 29, rel=0.001)
        path = tmp_path / "timeseries-subplots.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestTimeseriesHeatmap:
    """Observed native time-series heatmaps, including cropped edges and highlights."""

    @pytest.mark.reference
    @pytest.mark.parametrize("shape", [(5, 3), (1, 3), (5, 1), (1, 1)])
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_chart_matches_scanpy_crop_orientation_and_highlights(
        self, page, tmp_path, shape
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc

        values = np.arange(np.prod(shape), dtype=float).reshape(shape)
        names = np.array([f"variable-{i}" for i in range(shape[1])])
        highlights = [0.25] if shape[0] > 1 else [0.025]
        with mpl.rc_context({"figure.dpi": 100, "font.size": 10}):
            sc.pl.timeseries_as_heatmap(
                values, var_names=names, highlights_x=highlights
            )
            fig, ax = (plt.gcf(), plt.gcf().axes[0])
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
            limits = [ax.get_xlim(), ax.get_ylim()]
            line = ax.lines[0]
            expected_x = ax.transData.transform((highlights[0], 0))[0] - bbox.x0
            plt.close(fig)
        chart = gsc.pl.timeseries_as_heatmap(
            values, var_names=names, highlights_x=highlights, show=False
        )
        bounds = timeseries_heatmap_render(page, chart)
        assert bounds["width"] == pytest.approx(bbox.width, abs=0.6)
        assert bounds["height"] == pytest.approx(bbox.height, abs=0.6)
        actual = panel_image(page, bounds)
        # Register both exports on the actual plotting limits, away from glyph/edge antialiasing.
        for x in np.linspace(0.08, 0.92, 15):
            if abs(x - expected_x / bbox.width) < 0.015:
                continue
            for y in np.linspace(0.08, 0.92, 13):
                px, py = (
                    limits[0][0] + x * np.ptp(limits[0]),
                    limits[1][1] - y * np.ptp(limits[1]),
                )
                if any((abs(v - (round(v - 0.5) + 0.5)) < 0.04 for v in (px, py))):
                    continue
                np.testing.assert_allclose(
                    np.array(actual)[
                        int(y * actual.height), int(x * actual.width)
                    ].astype(int),
                    np.array(expected)[
                        int(y * expected.height), int(x * expected.width)
                    ].astype(int),
                    atol=12,
                )
        root = svg_root(page)
        ET.ElementTree(root).write(tmp_path / "native.svg", encoding="unicode")
        labels = {
            e.text: position(e)
            for e in root.iter()
            if e.tag.endswith("text") and (e.text or "").startswith("variable-")
        }
        assert set(labels) == set(names)
        sample_ticks = [
            e
            for e in root.iter()
            if e.tag.endswith("text")
            and e.get("transform")
            and (position(e)[1] > bounds["y"] + bounds["height"])
            and (bounds["x"] - 1 <= position(e)[0] <= bounds["x"] + bounds["width"] + 1)
        ]
        assert len(sample_ticks) >= 2
        for i, name in enumerate(names):
            assert labels[name][1] == pytest.approx(
                bounds["y"]
                + bounds["height"] * (1 - (i - limits[1][0]) / np.ptp(limits[1])),
                abs=0.6,
            )
            assert 0 <= labels[name][0] < bounds["x"]
        rules = [
            e
            for e in root.iter()
            if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
        ]
        assert len(rules) == 1 and len(rules[0]) == 1
        assert float(rules[0][0].get("x1")) == pytest.approx(
            bounds["x"] + expected_x, abs=0.6
        )
        assert float(rules[0].get("stroke-width")) == pytest.approx(
            line.get_linewidth() * 100 / 72, abs=0.06
        )
        assert list(
            map(float, rules[0].get("stroke-dasharray").split())
        ) == pytest.approx([round(v * 100 / 72) for v in line._dash_pattern[1]])
        gradients = [
            e
            for e in root.iter()
            if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
        ]
        assert len(gradients) == 1
        assert float(gradients[0].get("height")) == pytest.approx(
            bounds["height"] * 0.5, abs=2
        )
        assert float(gradients[0].get("x")) > bounds["x"] + bounds["width"]
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
        page.screenshot(path=str(tmp_path / "native-complete.png"), full_page=True)

    @pytest.mark.parametrize("zoom", [True, "xy"])
    def test_hover_values_labels_and_highlights_follow_native_zoom(
        self, page, tmp_path, zoom
    ):
        values = np.arange(2400).reshape(200, 12)
        names = [f"gene-{i}" for i in range(12)]
        chart = gsc.pl.timeseries_as_heatmap(
            values,
            var_names=names,
            highlights_x=[100.25],
            zoom=zoom,
            show_values=True,
            width=460,
            height=260,
            show=False,
        )
        spec = chart.to_dict()
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"timeseries_as_heatmap-{axis}"
        bounds = timeseries_heatmap_render(page, spec)
        initial = {
            axis: page.evaluate(
                "a=>api.getScaleResolutionByName(`timeseries_as_heatmap-${a}`).getDomain()",
                axis,
            )
            for axis in ("x", "y")
        }
        assert not value_texts(svg_root(page))
        px, py = pointer(page, bounds, 100 / 199, 1 - 5 / 11)
        for _ in range(4):
            page.mouse.wheel(0, -350)
            page.wait_for_timeout(250)
        page.wait_for_timeout(700)
        domains = {
            axis: page.evaluate(
                "a=>api.getScaleResolutionByName(`timeseries_as_heatmap-${a}`).getDomain()",
                axis,
            )
            for axis in ("x", "y")
        }
        assert (domains["x"] != initial["x"]) is (zoom == "xy")
        assert np.ptp(domains["y"]) < np.ptp(initial["y"])
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        root = svg_root(page)
        rules = [
            e
            for e in root.iter()
            if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
        ]
        assert len(rules) == 1
        assert float(rules[0][0].get("x1")) == pytest.approx(
            bounds["x"]
            + bounds["width"] * (100.25 - domains["x"][0]) / np.ptp(domains["x"]),
            abs=0.6,
        )
        if zoom == "xy":
            labels = value_texts(root)
            assert labels
            interior = 0
            for label in labels:
                value = float(label.text)
                row, col = next(
                    (
                        (r, c)
                        for r, c in np.ndindex(values.T.shape)
                        if values.T[r, c] == value
                    )
                )
                for i, (axis, slot, extent) in enumerate(
                    (("x", col, "width"), ("y", row, "height"))
                ):
                    edges = np.clip(
                        (np.array([slot - 0.5, slot + 0.5]) - domains[axis][0])
                        / np.ptp(domains[axis]),
                        0,
                        1,
                    )
                    if axis == "y":
                        edges = 1 - edges
                    edges = bounds[axis] + edges * bounds[extent]
                    # Full cells center their labels; partial cells use native text fitting.
                    if (
                        domains[axis][0] <= slot - 0.5
                        and slot + 0.5 <= domains[axis][1]
                    ):
                        assert position(label)[i] == pytest.approx(
                            float(np.mean(edges)), abs=0.6
                        )
                        interior += 1
            assert interior > 2
        col = int(round(domains["x"][0] + 0.3 * np.ptp(domains["x"])))
        row = int(round(np.mean(domains["y"])))
        x = (col - domains["x"][0]) / np.ptp(domains["x"])
        y = 1 - (row - domains["y"][0]) / np.ptp(domains["y"])
        pointer(page, bounds, x - 0.002, y - 0.002)
        page.wait_for_timeout(450)
        pointer(page, bounds, x, y)
        page.locator("table.attributes").wait_for(state="visible")
        hover = [
            text.strip()
            for text in page.locator("table.attributes td").all_text_contents()
        ]
        assert hover[:2] == [f"gene-{row}", str(col)]
        assert float(hover[2]) == values[col, row]
        # Panning updates native positions rather than rebuilding the chart in Python.
        page.mouse.down()
        page.mouse.move(px + 18, py + 12, steps=5)
        page.mouse.up()
        page.wait_for_timeout(700)
        moved = page.evaluate(
            "api.getScaleResolutionByName('timeseries_as_heatmap-y').getDomain()"
        )
        assert moved != domains["y"]
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        visible = [
            e
            for e in svg_root(page).iter()
            if e.tag.endswith("text") and (e.text or "").startswith("gene-")
        ]
        assert visible
        for label in visible:
            slot = int(label.text.removeprefix("gene-"))
            assert moved[0] <= slot <= moved[1]
            assert position(label)[1] == pytest.approx(
                bounds["y"]
                + bounds["height"] * (1 - (slot - moved[0]) / np.ptp(moved)),
                abs=0.6,
            )
        path = tmp_path / "timeseries.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestSim:
    """Complete simulation guides, registered marks and observed native navigation."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", sim_cases())
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_simulation_matches_scanpy_ticks_boundaries_and_paint(
        self, page, tmp_path, case
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc

        adata, options = (make_sim(), sim_cases()[case])
        state = np.random.get_state()
        try:
            with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sc.pl.sim(adata, show=False, **options)
                fig, ax = (plt.gcf(), plt.gcf().axes[0])
                style_profile_reference(ax)
                fig.canvas.draw()
                bbox = ax.get_window_extent()
                limits = [ax.get_xlim(), ax.get_ylim()]
                ticks = list(
                    zip(ax.get_xticks(), [t.get_text() for t in ax.get_xticklabels()])
                )
                heatmap = bool(ax.images)
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
                plt.close(fig)
        finally:
            np.random.set_state(state)
        chart = gsc.pl.sim(
            adata, width=bbox.width, height=bbox.height, show=False, **options
        )
        bounds = sim_render(page, chart)
        root = svg_root(page)
        (tmp_path / "native.svg").write_text(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
        for axis, extent in (("width", bbox.width), ("height", bbox.height)):
            assert bounds[axis] == pytest.approx(extent, abs=0.6)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert "A" in texts and "B" in texts
        boundaries = np.arange(
            options.get("tmax_realization", 3), 7, options.get("tmax_realization", 3)
        )
        rules = [
            e
            for e in root.iter()
            if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
        ]
        lines = list(rules[0]) if rules else []
        assert len(lines) == len(boundaries)
        for line, boundary in zip(lines, boundaries, strict=True):
            assert float(line.get("x1")) == pytest.approx(
                bounds["x"]
                + (boundary - limits[0][0]) / np.ptp(limits[0]) * bounds["width"],
                abs=1,
            )
        if not heatmap:
            assert (
                "index (arbitrary order)" if options.get("shuffle") else "realizations"
            ) in texts
        if not options.get("shuffle"):
            labels = [
                e
                for e in root.iter()
                if e.tag.endswith("text")
                and e.text in {label for _, label in ticks}
                and (position(e)[1] > bounds["y"] + bounds["height"])
            ]
            assert len(labels) == len(ticks), [
                (e.text, position(e)) for e in root.iter() if e.tag.endswith("text")
            ]
            for x, label in ticks:
                element = next((e for e in labels if e.text == label))
                assert position(element)[0] == pytest.approx(
                    bounds["x"]
                    + (x - limits[0][0]) / np.ptp(limits[0]) * bounds["width"],
                    abs=1,
                )
        actual = panel_image(page, bounds)
        a, b = (np.asarray(actual).astype(int), np.asarray(expected).astype(int))
        if heatmap:
            for fx in np.linspace(0.07, 0.93, 12):
                for fy in (0.2, 0.8):
                    # Stay away from realization rules and tile borders.
                    x = limits[0][0] + fx * np.ptp(limits[0])
                    if (
                        min(
                            (
                                abs(x - h)
                                for h in [
                                    0.5,
                                    1.5,
                                    2.5,
                                    3.5,
                                    4.5,
                                    5.5,
                                    *np.arange(
                                        options.get("tmax_realization", 3),
                                        7,
                                        options.get("tmax_realization", 3),
                                    ),
                                ]
                            )
                        )
                        < 0.08
                    ):
                        continue
                    np.testing.assert_allclose(
                        a[int(fy * actual.height), int(fx * actual.width)],
                        b[int(fy * expected.height), int(fx * expected.width)],
                        atol=12,
                    )
        else:
            spec = chart.to_dict()
            point = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
            for row in spec["datasets"][point["data"]["name"]]:
                # Whole-pixel native dashes can cover a different part of a tiny dot.
                if any((row["_time"] == boundary for boundary in boundaries)):
                    continue
                fx = (row["_time"] - limits[0][0]) / np.ptp(limits[0])
                fy = 1 - (row["_value"] - limits[1][0]) / np.ptp(limits[1])
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
        actual.save(tmp_path / "native-panel.png")
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

    @pytest.mark.parametrize("mode", ["points", "heatmap", "shuffle"])
    def test_hover_navigation_realization_labels_and_offline_delivery(
        self, page, tmp_path, mode
    ):
        adata = make_sim()
        adata = type(adata)(
            np.arange(60, dtype=float).reshape(30, 2),
            var=adata.var.copy(),
            uns={"tmax_write": 10},
        )
        chart = gsc.pl.sim(
            adata,
            as_heatmap=mode == "heatmap",
            shuffle=mode == "shuffle",
            marker="o",
            zoom="xy",
            show_values=mode == "heatmap",
            width=500,
            height=300,
            show=False,
        )
        spec = chart.to_dict()
        if mode == "heatmap":
            for axis in ("x", "y"):
                spec["scales"][axis]["name"] = f"sim-{axis}"
        bounds = sim_render(page, spec)
        mark = next(
            (
                m
                for m in leaf_marks(spec)
                if m["mark"]["type"] == ("rect" if mode == "heatmap" else "point")
            )
        )
        if mode == "heatmap":
            domains = [spec["scales"][axis]["domain"] for axis in ("x", "y")]
            tx, ty = (10, 0.2)
            expected = ["A", "10", "20.00"]
        else:
            domains = [mark["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
            rows = spec["datasets"][mark["data"]["name"]]
            sample = next(
                (r for r in rows if r["_sample"] == 10 and r["_series"] == "A")
            )
            tx, ty = (sample["_time"], sample["_value"])
            expected = ["A", "10", "10.00", f"{ty:.2f}"]
        x = bounds["x"] + (tx - domains[0][0]) / np.ptp(domains[0]) * bounds["width"]
        y = (
            bounds["y"]
            + (1 - (ty - domains[1][0]) / np.ptp(domains[1])) * bounds["height"]
        )
        hover_at(page, x, y)
        page.locator("table.attributes").wait_for(state="visible")
        assert [
            s.strip() for s in page.locator("table.attributes td").all_text_contents()
        ] == expected
        before = point_coordinates(page)[0] if mode != "heatmap" else None
        page.mouse.wheel(0, -500)
        page.wait_for_timeout(700)
        before_pan = (
            page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
            if mode == "heatmap"
            else point_coordinates(page)[0]
        )
        canvas = page.locator("canvas").first.bounding_box()
        page.mouse.move(canvas["x"] + x, canvas["y"] + y)
        page.mouse.down()
        page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
        page.mouse.up()
        page.wait_for_timeout(300)
        after = svg_root(page)
        if mode == "heatmap":
            assert (
                page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
                != before_pan
            )
            assert (
                page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
                != domains[0]
            )
            assert (
                page.evaluate("api.getScaleResolutionByName('sim-y').getDomain()")
                != domains[1]
            )
            assert value_texts(after)
        else:
            coordinates = point_coordinates(page)[0]
            assert not np.array_equal(coordinates, before_pan)
            assert all(
                (
                    a > b
                    for a, b in zip(
                        point_spacing(coordinates), point_spacing(before), strict=True
                    )
                )
            )
        if mode != "shuffle":
            labels = [
                e
                for e in after.iter()
                if e.tag.endswith("text")
                and e.text in {"1", "2", "3"}
                and (position(e)[1] > bounds["y"] + bounds["height"])
            ]
            assert labels
            rules = [
                line
                for group in after.iter()
                if group.get("data-mark-type") == "rule"
                and group.get("stroke-dasharray")
                for line in group
            ]
            for label in labels:
                assert any(
                    (
                        abs(position(label)[0] - float(line.get("x1"))) <= 1
                        for line in rules
                    )
                )
        path = tmp_path / "simulation.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    def test_point_simulation_legend_is_below_the_realization_axis(self, page):
        from tests.integrations.scanpy.browser.interactions import position

        sim_render(page, gsc.pl.sim(make_sim(), show=False))
        root = svg_root(page)
        texts = [e for e in root.iter() if e.tag.endswith("text")]
        keys = [position(e)[1] for e in texts if e.text in {"A", "B"}]
        axis = [position(e)[1] for e in texts if e.text == "realizations"]
        assert len(keys) == 2 and len(axis) == 1
        assert min(keys) > max(axis) + 5


def presentation_plot_points(page):
    """Return exported plot circles, excluding legend symbols."""
    return [
        circle
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == "point" and group.get("clip-path")
        for circle in group
    ]


class TestPresentation:
    """Observe native controls and zoom sizing without changing stored analysis."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("missing", [None, "dispersions_norm", "means"])
    def test_hvg_slider_changes_both_panels_and_count_and_keeps_saved_flags(
        self, page, missing
    ):
        result = make_hvg_result()
        if missing is not None:
            result.loc[result.index[0], missing] = np.nan
        before = result.copy(deep=True)
        chart = gsc.pl.highly_variable_genes(
            result, threshold_slider=True, zoom=True, show=False
        )
        presentation_render(page, chart)
        slider = page.locator('input[type="range"]')
        assert slider.count() == 1
        for cutoff in [-1, 1.0, 2.5, 8.0]:
            slider.evaluate(
                "(el, value) => {el.value=value; el.dispatchEvent(new Event('input', {bubbles:true}));}",
                cutoff,
            )
            above = result.dispersions_norm >= cutoff
            expected = int(above.sum())
            page.wait_for_function(
                "async count => (await (await api.imageExport.svg()).blob.text()).includes(count + ' genes above cutoff (preview)')",
                arg=expected,
            )
            circles = presentation_plot_points(page)
            visible = result.means.notna()
            assert (
                len(circles)
                == visible.sum() + (visible & result.dispersions_norm.notna()).sum()
            )
            assert sum((c.get("fill") == "#2563a6" for c in circles)) == 2 * int(
                (visible & above).sum()
            )
        np.testing.assert_array_equal(result.highly_variable, before.highly_variable)

    @pytest.mark.smoke
    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    def test_profile_dropdown_dims_other_series_without_dropping_points(
        self, page, family
    ):
        chart = getattr(gsc.pl, family)(
            [[1, 3], [2, 4], [3, 5]],
            var_names=["A", "B"],
            series_select=True,
            ruler=True,
            zoom=True,
            show=False,
        )
        presentation_render(page, chart)
        before = point_coordinates(page)[0]
        page.locator("select").select_option(label="A")
        circles = presentation_plot_points(page)
        assert len(circles) == 6
        assert (
            sorted((float(c.get("fill-opacity", "1")) for c in circles))
            == [0.12] * 3 + [0.85] * 3
        )
        np.testing.assert_array_equal(point_coordinates(page)[0], before)
        page.locator("select").select_option(label="All")
        assert all(
            (
                float(c.get("fill-opacity", "1")) == 0.85
                for c in presentation_plot_points(page)
            )
        )
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        pointer(page, bounds)
        assert any(
            (group.get("stroke") == "#64748b" for group in svg_root(page).iter())
        )

    @pytest.mark.parametrize("as_heatmap", [False, True])
    def test_adjacency_points_grow_on_y_zoom_and_stay_bounded(self, page, as_heatmap):
        chart = gsc.pl.paga_adjacency(
            make_adjacency(),
            as_heatmap=as_heatmap,
            labels=["A", "B", "C"],
            zoom=True,
            width=360,
            height=300,
            show=False,
        )
        bounds = presentation_render(page, chart)
        before = [float(c.get("r")) for c in presentation_plot_points(page)]
        assert before
        point = presentation_plot_points(page)[0]
        pointer(
            page,
            bounds,
            (float(point.get("cx")) - bounds["x"]) / bounds["width"],
            (float(point.get("cy")) - bounds["y"]) / bounds["height"],
        )
        page.mouse.wheel(0, -500)
        page.wait_for_timeout(700)
        after = [float(c.get("r")) for c in presentation_plot_points(page)]
        assert after and min(after) > max(before)
        assert max(after) <= 2 * min(before) + 0.01

    @pytest.mark.parametrize("as_heatmap", [False, True])
    def test_path_uses_native_group_track_and_gene_focus(self, page, as_heatmap):
        chart = gsc.pl.paga_path(
            make_path(),
            ["beta", "alpha"],
            ["g1", "g2"],
            as_heatmap=as_heatmap,
            series_select=True,
            ruler=True,
            zoom="xy",
            show=False,
        )
        presentation_render(page, chart)
        page.locator("select").select_option(label="g1")
        root = svg_root(page)
        text = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert "beta" in text and "alpha" in text
        if not as_heatmap:
            assert "Value" in text

    def test_two_profile_controls_remain_independent_in_a_composition(self, page):
        left = gsc.pl.timeseries(
            [[1, 2], [3, 4]], var_names=["A", "B"], series_select=True, show=False
        )
        right = gsc.pl.timeseries(
            [[1, 2], [3, 4]], var_names=["A", "B"], series_select=True, show=False
        )
        presentation_render(
            page, gs.hconcat(left, right).resolve_scale(default="independent")
        )
        controls = page.locator("select")
        assert controls.count() == 2
        controls.nth(0).select_option(label="A")
        circles = presentation_plot_points(page)
        assert sum((float(c.get("fill-opacity", "1")) == 0.12 for c in circles)) == 2

    def test_compare_embedding_points_grow_but_graph_node_sizes_keep_their_meaning(
        self, page
    ):
        chart = gsc.pl.paga_compare(
            make_compare(),
            legend_fontweight="normal",
            zoom=True,
            add_pos=False,
            show=False,
        )
        bounds = presentation_render(page, chart)
        groups = [
            g
            for g in svg_root(page).iter()
            if g.get("data-mark-type") == "point" and g.get("clip-path")
        ]
        before = [[float(c.get("r")) for c in group] for group in groups]
        assert len(before) == 2 and before[0] and before[1]
        cell = list(groups[0])[0]
        pointer(
            page,
            bounds,
            (float(cell.get("cx")) - bounds["x"]) / bounds["width"],
            (float(cell.get("cy")) - bounds["y"]) / bounds["height"],
        )
        page.mouse.wheel(0, -200)
        page.wait_for_timeout(700)
        after = [
            [float(c.get("r")) for c in group]
            for group in svg_root(page).iter()
            if group.get("data-mark-type") == "point" and group.get("clip-path")
        ]
        assert after[0] and min(after[0]) > max(before[0])
        assert max(after[0]) <= 2 * max(before[0]) + 0.01
        assert all((radius in before[1] for radius in after[1]))

    def test_paga_edge_slider_filters_rules_without_changing_nodes(self, page):
        chart = gsc.pl.paga(
            make_paga(),
            pos=POSITIONS,
            edge_slider=True,
            show_node_labels=False,
            add_pos=False,
            show=False,
        )
        presentation_render(page, chart)
        before = point_coordinates(page)[0]
        root = svg_root(page)
        assert (
            sum(
                (
                    len(g)
                    for g in root.iter()
                    if g.get("data-mark-type") == "rule" and g.get("clip-path")
                )
            )
            > 0
        )
        assert {"A", "B", "C", "D"}.issubset(
            (e.text for e in root.iter() if e.tag.endswith("text"))
        )
        assert not any(
            (
                g.get("clip-path") and len(g)
                for g in root.iter()
                if g.get("data-mark-type") == "text"
            )
        )
        page.locator('input[type="range"]').evaluate(
            "el => {el.value=1; el.dispatchEvent(new Event('input', {bubbles:true}));}"
        )
        page.wait_for_function(
            "async () => {\n        const svg = new DOMParser().parseFromString(await (await api.imageExport.svg()).blob.text(), 'image/svg+xml');\n        return [...svg.querySelectorAll('[data-mark-type=\"rule\"][clip-path]')].every(g=>g.children.length === 0);\n    }"
        )
        root = svg_root(page)
        assert (
            sum(
                (
                    len(g)
                    for g in root.iter()
                    if g.get("data-mark-type") == "rule" and g.get("clip-path")
                )
            )
            == 0
        )
        np.testing.assert_array_equal(point_coordinates(page)[0], before)

    @pytest.mark.parametrize("as_heatmap", [False, True])
    def test_simulation_gene_and_run_dropdowns_emphasize_their_intersection(
        self, page, as_heatmap
    ):
        chart = gsc.pl.sim(
            make_sim(),
            as_heatmap=as_heatmap,
            series_select=True,
            run_select=True,
            ruler=True,
            show=False,
        )
        presentation_render(page, chart)
        controls = page.locator("select")
        assert controls.count() == 2
        controls.nth(0).select_option(label="A")
        controls.nth(1).select_option(label="2")
        marks = [
            child
            for group in svg_root(page).iter()
            if group.get("data-mark-type") == ("rect" if as_heatmap else "point")
            and group.get("clip-path")
            for child in group
        ]
        assert len(marks) == 14
        assert (
            sum((float(mark.get("fill-opacity", "1")) == 0.85 for mark in marks)) == 3
        )
        assert (
            sum((float(mark.get("fill-opacity", "1")) == 0.12 for mark in marks)) == 11
        )

    def test_simulation_lines_keep_missing_values_and_run_boundaries(self, page):
        simulation = make_sim()
        simulation.X[1, 0] = np.nan
        chart = gsc.pl.sim(simulation, connect=True, show=False)
        spec = chart.to_dict()
        points = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
        domain = points["encoding"]["x"]["scale"]["domain"]
        bounds = presentation_render(page, chart)
        segments = [
            line
            for group in svg_root(page).iter()
            if group.get("data-mark-type") == "rule"
            and group.get("clip-path")
            and (not group.get("stroke-dasharray"))
            for line in group
        ]
        assert len(segments) == 6
        for line in segments:
            times = [
                (float(line.get(k)) - bounds["x"]) / bounds["width"] * np.ptp(domain)
                + domain[0]
                for k in ("x1", "x2")
            ]
            np.testing.assert_allclose(times, np.round(times), atol=0.01)
            assert np.floor(round(times[0]) / 3) == np.floor(round(times[1]) / 3)
        assert len(presentation_plot_points(page)) == 13
