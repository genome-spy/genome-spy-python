"""Dpt behavior and regressions."""

import warnings

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
from tests.integrations.scanpy.browser.rendering import (
    panel_image,
    style_profile_reference,
)
from tests.integrations.scanpy.browser.rendering import render_heatmap as render
from tests.integrations.scanpy.profile_fixtures import (
    dpt_cases,
    dpt_profile_cases,
    dpt_reference,
    make_dpt,
    make_dpt_profiles,
)


class TestDptGroups:
    """Registered DPT panels and native hover/navigation without trajectory inference."""

    @pytest.mark.parametrize("case", dpt_cases())
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_dpt_panels_match_scanpy_points_and_guides(
        self, page, tmp_path, case
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        adata, options = (make_dpt(case), dpt_cases()[case])
        with (
            mpl.rc_context({"figure.dpi": 100, "figure.figsize": (6.4, 4.8)}),
            warnings.catch_warnings(),
        ):
            warnings.simplefilter("ignore")
            fig = dpt_reference(adata, **options)
            for ax in fig.axes:
                style_profile_reference(ax)
            fig.canvas.draw()
            reference = tmp_path / "reference.png"
            fig.savefig(reference, dpi=150)
            full = Image.open(reference).convert("RGB")
            references = []
            for ax in fig.axes:
                bbox = ax.get_window_extent()
                crop = full.crop(
                    (
                        round(bbox.x0 * 1.5),
                        round(full.height - bbox.y1 * 1.5),
                        round(bbox.x1 * 1.5),
                        round(full.height - bbox.y0 * 1.5),
                    )
                )
                xy = np.ma.concatenate([c.get_offsets() for c in ax.collections])
                references.append(
                    (
                        bbox,
                        crop,
                        np.asarray(xy)[~np.ma.getmaskarray(xy).any(axis=1)],
                        ax.get_xlim(),
                        ax.get_ylim(),
                    )
                )
            plt.close(fig)
        chart = gsc.pl.dpt_groups_pseudotime(adata, show=False, **options)
        render(page, chart)
        root = svg_root(page)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert all(
            (label in texts for label in ["dpt groups", "pseudotime", "dpt order"])
        )
        gradients = [
            e
            for e in root.iter()
            if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
        ]
        assert bool(gradients) == (case != "integer_time")
        assert all((str(group) in texts for group in adata.obs["dpt_groups"].unique()))
        for i, (bbox, expected, xy, dx, dy) in enumerate(references):
            bounds = page.evaluate(
                "view=>api.views.getLayoutBounds({scope:[],view})", f"panel-{i}"
            )
            assert bounds["width"] == pytest.approx(bbox.width, abs=0.6)
            assert bounds["height"] == pytest.approx(bbox.height, abs=0.6)
            actual = panel_image(page, bounds)
            a, b = (np.asarray(actual).astype(int), np.asarray(expected).astype(int))
            checked = 0
            for x, y in xy:
                if any((x == h for h in adata.uns["dpt_changepoints"])):
                    continue
                fx, fy = ((x - dx[0]) / np.ptp(dx), 1 - (y - dy[0]) / np.ptp(dy))
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
                tmp_path / f"panel-{i}-overlay.png"
            )
        page.screenshot(path=str(tmp_path / "complete.png"), full_page=True)

    def test_hover_and_navigation_stay_independent_and_export_offline(
        self, page, tmp_path
    ):
        import pandas as pd
        from anndata import AnnData

        adata = AnnData(
            obs=pd.DataFrame(
                {
                    "dpt_groups": pd.Categorical(
                        ["beta", "alpha"] * 15, categories=["beta", "alpha"]
                    ),
                    "dpt_order": np.roll(np.arange(30), 5),
                    "dpt_pseudotime": np.linspace(0, 1, 30),
                },
                index=[f"cell-{i}" for i in range(30)],
            ),
            uns={"dpt_changepoints": [10, 20]},
        )
        chart = gsc.pl.dpt_groups_pseudotime(
            adata, marker="o", zoom=True, width=500, height=200, show=False
        )
        render(page, chart)
        before = point_coordinates(page)
        spec = chart.to_dict()
        targets = []
        for i in (0, 1):
            point = spec["vconcat"][i]["layer"][0]
            dx, dy = [point["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
            value = 0 if i == 0 else 10 / 29
            bounds = page.evaluate(
                "view=>api.views.getLayoutBounds({scope:[],view})", f"panel-{i}"
            )
            x = bounds["x"] + bounds["width"] * (5 - dx[0]) / np.ptp(dx)
            y = bounds["y"] + bounds["height"] * (1 - (value - dy[0]) / np.ptp(dy))
            targets.append((x, y))
            hover_at(page, x, y)
            page.locator("table.attributes").wait_for(state="visible")
            cells = [
                s.strip()
                for s in page.locator("table.attributes td").all_text_contents()
            ]
            assert cells[:3] == (
                ["beta", "10", "5.000"] if i == 0 else ["0", "10", "5.000"]
            )
            assert float(cells[3]) == pytest.approx(value, rel=0.001)
        hover_at(page, *targets[0])
        page.mouse.wheel(0, -250)
        page.wait_for_timeout(500)
        zoomed = point_coordinates(page)
        assert not np.array_equal(before[0], zoomed[0])
        np.testing.assert_allclose(before[1], zoomed[1])
        canvas = page.locator("canvas").first.bounding_box()
        x, y = targets[0]
        page.mouse.move(canvas["x"] + x, canvas["y"] + y)
        page.mouse.down()
        page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y - 15, steps=5)
        page.mouse.up()
        page.wait_for_timeout(400)
        panned = point_coordinates(page)
        assert not np.array_equal(panned[0], zoomed[0])
        np.testing.assert_allclose(before[1], panned[1])
        path = tmp_path / "dpt.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    def test_categorical_group_key_is_readable_and_matches_the_plotted_colors(
        self, page
    ):
        from tests.integrations.scanpy.browser.rendering import render

        chart = gsc.pl.dpt_groups_pseudotime(
            make_dpt(), width=480, height=180, show=False
        )
        bounds = render(page, chart)
        root = svg_root(page)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert "DPT group" in texts and "alpha" in texts and ("beta" in texts)
        assert "unused" not in texts
        plots = [
            g
            for g in root.iter()
            if g.get("data-mark-type") == "point" and g.get("clip-path")
        ]
        keys = [
            e
            for g in root.iter()
            if g.get("data-mark-type") == "point" and (not g.get("clip-path"))
            for e in g
        ]
        assert len(keys) == 2
        assert {e.get("fill") for e in keys} == {e.get("fill") for e in plots[0]}
        assert all((float(e.get("r")) == pytest.approx(3.5, abs=0.05) for e in keys))
        assert all((float(e.get("cx")) > bounds["x"] + bounds["width"] for e in keys))


class TestDptTimeseries:
    """Registered DPT expression charts and observed shared native interactions."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", dpt_profile_cases())
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_dpt_expression_matches_scanpy_paint_labels_and_boundaries(
        self, page, tmp_path, case
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc

        adata, options = (make_dpt_profiles(case), dpt_profile_cases()[case])
        with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sc.pl.dpt_timeseries(adata, show=False, **options)
            fig, ax = (plt.gcf(), plt.gcf().axes[0])
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
        actual = panel_image(page, bounds)
        a, b = (np.asarray(actual).astype(int), np.asarray(expected).astype(int))
        checked = 0
        if heatmap:
            for fx in np.linspace(0.07, 0.93, 17):
                x = limits[0][0] + fx * np.ptp(limits[0])
                if any((abs(x - h) < 0.1 for h in adata.uns["dpt_changepoints"])):
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
        self, page, tmp_path, heatmap
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
            point = next((m for m in spec["layer"] if m["mark"]["type"] == "point"))
            dy = point["encoding"]["y"]["scale"]["domain"]
            y = bounds["y"] + bounds["height"] * (1 - (10 - dy[0]) / np.ptp(dy))
        hover_at(page, x, y)
        page.locator("table.attributes").wait_for(state="visible")
        cells = [
            s.strip() for s in page.locator("table.attributes td").all_text_contents()
        ]
        assert cells == (
            ["A", "10", "10.00"] if heatmap else ["A", "10", "10.00", "10.00"]
        )
        before = (
            page.evaluate(
                "api.getScaleResolutionByName('dpt_timeseries-x').getDomain()"
            )
            if heatmap
            else point_coordinates(page)[0]
        )
        page.mouse.wheel(0, -500)
        page.wait_for_timeout(700)
        zoomed = (
            page.evaluate(
                "api.getScaleResolutionByName('dpt_timeseries-x').getDomain()"
            )
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
            page.evaluate(
                "api.getScaleResolutionByName('dpt_timeseries-x').getDomain()"
            )
            if heatmap
            else point_coordinates(page)[0]
        )
        assert not np.array_equal(after, zoomed)
        if heatmap:
            assert value_texts(svg_root(page))
        else:
            assert all(
                (
                    a > b
                    for a, b in zip(
                        point_spacing(after), point_spacing(before), strict=True
                    )
                )
            )
        path = tmp_path / "dpt.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()
