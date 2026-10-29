"""Paga behavior and regressions."""

import warnings

import numpy as np
import pytest
from PIL import Image

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    move_to,
    point_coordinates,
    svg_root,
)
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.helpers import leaf_marks, points
from tests.integrations.scanpy.paga_fixtures import (
    POSITIONS,
    make_compare,
    make_paga,
    paga_cases,
    paga_reference,
)


class TestPaga:
    """Registered native PAGA graph paint, labels, hover, navigation and HTML delivery."""

    @pytest.mark.reference
    @pytest.mark.parametrize(
        "case",
        [
            "default",
            "supplied",
            "dashed",
            "sizing",
            "aliases",
            "empty",
            "asymmetric_csc",
            "obs_score",
            "gene_raw",
            "gene_x",
            "degree_solid",
            "degree_dashed",
            "constant",
            "constant_no_guide",
            "gene_missing",
            "no_guide",
            "component",
            "component_tie",
            "component_empty",
            "component_score",
            "component_gene",
            "component_degree",
        ],
    )
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_native_graph_matches_scanpy_paint_and_labels(
        self, page, tmp_path, case
    ):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc
        from matplotlib.collections import LineCollection, PathCollection

        adata, reference_options = paga_reference(case)
        options = paga_cases()[case]
        with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ax = sc.pl.paga(adata, show=False, **reference_options)
            fig = ax.figure
            fig.canvas.draw()
            bbox = ax.get_window_extent()
            point = next((c for c in ax.collections if isinstance(c, PathCollection)))
            xy, areas, colors = (
                point.get_offsets(),
                point.get_sizes(),
                point.get_facecolors(),
            )
            visible = ~np.ma.getmaskarray(xy).any(axis=1)
            xy, areas, colors = (
                np.asarray(xy)[visible],
                areas[visible],
                colors[visible],
            )
            colorbar = len(fig.axes) > 1
            expected_lines = [
                c for c in ax.collections if isinstance(c, LineCollection)
            ]
            domains = [ax.get_xlim(), ax.get_ylim()]
            labels = [t.get_text() for t in ax.texts]
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
        chart = gsc.pl.paga(
            make_paga(case), width=bbox.width, height=bbox.height, show=False, **options
        )
        bounds = render(page, chart)
        assert bounds["width"] == pytest.approx(bbox.width, abs=0.5)
        assert bounds["height"] == pytest.approx(bbox.height, abs=0.5)
        root = svg_root(page)
        (tmp_path / "native.svg").write_text(
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        )
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert set(labels) <= set(texts)
        expected_guide = colorbar or options.get("color") in {
            "degree_solid",
            "degree_dashed",
        }
        assert (
            any((e.tag.endswith("linearGradient") for e in root.iter()))
            == expected_guide
        )
        if "title" in options:
            assert options["title"] in texts
        centers = point_coordinates(page)[0]
        # SVG uses rounded viewport bounds when color guides need fractional space.
        clip = next((e for e in root.iter() if e.tag.endswith("clipPath")))[0]
        viewport = {key: float(clip.get(key)) for key in ("x", "y", "width", "height")}
        for key, value in viewport.items():
            assert value == pytest.approx(bounds[key], abs=0.5)
        expected_centers = np.column_stack(
            [
                viewport["x"]
                + (xy[:, 0] - domains[0][0]) / np.ptp(domains[0]) * viewport["width"],
                viewport["y"]
                + (1 - (xy[:, 1] - domains[1][0]) / np.ptp(domains[1]))
                * viewport["height"],
            ]
        )
        np.testing.assert_allclose(centers, expected_centers, atol=0.06)
        rules = [
            e
            for e in root.iter()
            if e.get("data-mark-type") == "rule" and e.get("clip-path")
        ]
        assert len(rules) == len(expected_lines)
        for group, reference_line in zip(rules, expected_lines, strict=True):
            assert len(group) == len(reference_line.get_segments())
            for line, width in zip(group, reference_line.get_linewidths(), strict=True):
                assert float(
                    line.get("stroke-width", group.get("stroke-width", "1"))
                ) == pytest.approx(width * 100 / 72, abs=0.051)
        actual = panel_image(page, bounds)
        pixels, target = (
            np.asarray(actual).astype(float),
            np.asarray(expected).astype(float),
        )
        for center, area, color in zip(centers, areas, colors, strict=True):
            x, y = (center - [bounds["x"], bounds["y"]]) * 1.5
            radius = int((np.sqrt(area) / 2 + 2) * 100 / 72 * 1.5) + 2
            a = pixels[
                round(y) - radius : round(y) + radius + 1,
                round(x) - radius : round(x) + radius + 1,
            ]
            b = target[
                round(y) - radius : round(y) + radius + 1,
                round(x) - radius : round(x) + radius + 1,
            ]
            # Count colored paint separately from the black labels and graph edges.
            paint_a = np.argwhere(np.linalg.norm(a - color[:3] * 255, axis=2) < 40)
            paint_b = np.argwhere(np.linalg.norm(b - color[:3] * 255, axis=2) < 40)
            assert len(paint_a) > 20 and len(paint_b) > 20
            # Fonts cover different parts of small nodes; measure the surviving outer radius.
            radius_a = np.linalg.norm(paint_a - radius, axis=1).max()
            radius_b = np.linalg.norm(paint_b - radius, axis=1).max()
            assert radius_a == pytest.approx(radius_b, abs=2)
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

    @pytest.mark.smoke
    @pytest.mark.parametrize("color", [None, "score", "g1", "degree_solid"])
    @pytest.mark.parametrize("component", [False, True])
    def test_group_and_edge_hover_navigation_and_offline_html(
        self, page, tmp_path, color, component
    ):
        chart = gsc.pl.paga(
            make_paga("obs_score") if color else make_paga(),
            color=color,
            single_component=component,
            threshold=0.2 if component else None,
            pos=POSITIONS,
            zoom=True,
            width=500,
            height=350,
            show=False,
        )
        bounds = render(page, chart)
        centers = point_coordinates(page)[0]
        point = next(
            (m for m in leaf_marks(chart.to_dict()) if m["mark"]["type"] == "point")
        )
        dx, dy = [point["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
        # Native viewport culling may sort exported circles; project known group coordinates instead.
        projected = np.column_stack(
            [
                bounds["x"] + (POSITIONS[:, 0] - dx[0]) / np.ptp(dx) * bounds["width"],
                bounds["y"]
                + (1 - (POSITIONS[:, 1] - dy[0]) / np.ptp(dy)) * bounds["height"],
            ]
        )
        hover_at(page, *projected[1 if component else 0])
        page.locator("table.attributes").wait_for(state="visible")
        values = [
            t.strip() for t in page.locator("table.attributes td").all_text_contents()
        ]
        assert values[:3] == (["B", "B", "4"] if component else ["A", "A", "9"])
        if color:
            expected = (
                {"score": 5.5, "g1": 31.5, "degree_solid": 1}
                if component
                else {"score": -1, "g1": 12, "degree_solid": 0}
            )
            assert float(values[3].replace("−", "-")) == expected[color]
        else:
            assert len(values) == 3
        # B--C is a visible, isolated stored edge whose midpoint is outside either node.
        hover_at(page, *(projected[1] + projected[2]) / 2)
        page.locator("table.attributes").get_by_text(
            "Connectivity", exact=True
        ).wait_for(state="visible")
        assert float(page.locator("table.attributes td").last.inner_text()) == 0.5
        canvas = page.locator("canvas").first.bounding_box()
        page.mouse.move(
            canvas["x"] + bounds["x"] + 250, canvas["y"] + bounds["y"] + 175
        )
        page.mouse.wheel(0, -10)
        page.wait_for_timeout(700)
        zoomed = point_coordinates(page)[0]
        assert all((np.ptp(zoomed[:, i]) > np.ptp(centers[:, i]) for i in (0, 1)))
        canvas = page.locator("canvas").first.bounding_box()
        x, y = (canvas["x"] + bounds["x"] + 250, canvas["y"] + bounds["y"] + 175)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + 20, y + 15, steps=5)
        page.mouse.up()
        page.wait_for_timeout(500)
        assert not np.array_equal(point_coordinates(page)[0], zoomed)
        # Ordinary composition must not create duplicate global scale names.
        combined = gs.hconcat(chart, chart).resolve_scale(default="independent")
        render(page, combined)
        assert len(point_coordinates(page)) == 2
        path = tmp_path / "paga.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    def test_zero_node_size_keeps_labels_without_point_paint(self, page):
        chart = gsc.pl.paga(make_paga(), pos=POSITIONS, node_size_scale=0, show=False)
        render(page, chart)
        assert not point_coordinates(page)
        texts = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
        assert set("ABCD") <= set(texts)

    def test_disabled_hover_does_not_show_node_tooltips(self, page):
        render(page, gsc.pl.paga(make_paga(), pos=POSITIONS, hover=False, show=False))
        hover_at(page, *point_coordinates(page)[0][0])
        assert not page.locator("table.attributes").count()

    @pytest.mark.parametrize("color", [None, "score", "degree_solid"])
    def test_native_node_guide_names_and_colors_are_visible_without_node_labels(
        self, page, color
    ):
        from tests.integrations.scanpy.browser.interactions import svg_root

        a = make_paga("obs_score")
        chart = gsc.pl.paga(
            a, pos=POSITIONS, color=color, show_node_labels=False, show=False
        )
        render(page, chart)
        root = svg_root(page)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        gradients = [e for e in root.iter() if e.tag.endswith("linearGradient")]
        if color is None:
            assert "cluster" in texts and all(
                (name in texts for name in ["A", "B", "C", "D"])
            )
            assert not gradients
            guide_points = [
                g
                for g in root.iter()
                if g.get("data-mark-type") == "point" and (not g.get("clip-path"))
            ]
            assert sum((len(g) for g in guide_points)) == 4
        else:
            assert color in texts and len(gradients) == 1

    @pytest.mark.parametrize("color", ["score", "g1", "degree_solid"])
    @pytest.mark.parametrize("height", [120, 360])
    def test_numeric_colorbar_fits_plot_height_with_title_beside_it(
        self, page, color, height
    ):
        from tests.integrations.scanpy.browser.interactions import position, svg_root

        chart = gsc.pl.paga(
            make_paga("obs_score"),
            pos=POSITIONS,
            color=color,
            width=400,
            height=height,
            show_node_labels=False,
            show=False,
        )
        bounds = render(page, chart)
        root = svg_root(page)
        bars = [
            e
            for e in root.iter()
            if e.tag.endswith("rect")
            and e.get("fill", "").startswith("url(#legend-gradient-")
        ]
        assert len(bars) == 1
        bar = bars[0]
        top, length = (float(bar.get("y")), float(bar.get("height")))
        assert top == pytest.approx(bounds["y"], abs=1.1)
        assert top + length == pytest.approx(bounds["y"] + bounds["height"], abs=1.1)
        title = next(
            (e for e in root.iter() if e.tag.endswith("text") and e.text == color)
        )
        x, y = position(title)
        assert x > float(bar.get("x")) + float(bar.get("width"))
        assert y == pytest.approx(bounds["y"] + bounds["height"] / 2, abs=1.1)

    def test_displaced_label_avoids_its_actual_node_size_and_works_offline(
        self, page, tmp_path
    ):
        from tests.integrations.scanpy.browser.interactions import position

        chart = gsc.pl.paga(
            make_paga("component_empty"),
            pos=POSITIONS,
            single_component=True,
            node_size_scale=100,
            labels=["I"] * 4,
            fontsize=3,
            width=400,
            height=400,
            show=False,
        )
        render(page, chart)
        page.wait_for_timeout(1200)
        root = svg_root(page)
        circle = next(
            (
                e
                for g in root.iter()
                if g.get("data-mark-type") == "point" and g.get("clip-path")
                for e in g
            )
        )
        label = next(
            (
                e
                for g in root.iter()
                if g.get("data-mark-type") == "text" and g.get("clip-path")
                for e in g
            )
        )
        offset = np.array(position(label)) - [
            float(circle.get("cx")),
            float(circle.get("cy")),
        ]
        assert max(abs(offset)) > float(circle.get("r"))
        output = tmp_path / "paga-labels.html"
        chart.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


def paga_compare_point_coordinates(page, names=("panel-0", "panel-1")):
    """Read plot circles inside named panels, excluding their sibling legend views."""
    root = svg_root(page)
    result = []
    for name in names:
        panel = next((group for group in root.iter() if group.get("data-name") == name))
        group = next(
            (group for group in panel.iter() if group.get("data-mark-type") == "point")
        )
        result.append(
            np.array([[float(p.get("cx")), float(p.get("cy"))] for p in group])
        )
    return result


class TestPagaCompare:
    """Observe aligned PAGA comparison panels, default labels and linked navigation."""

    @pytest.mark.parametrize("palette", [["red", "blue", "green", "orange"], "set1"])
    @pytest.mark.parametrize("component", [False, True])
    def test_category_colors_match_between_cells_and_nodes_including_filtered_graphs(
        self, page, palette, component
    ):
        a = make_compare()
        chart = gsc.pl.paga_compare(
            a,
            palette=palette,
            single_component=component,
            threshold=0.2,
            legend_fontweight="normal",
            size=36,
            width=380,
            height=300,
            show=False,
        )
        spec = chart.to_dict()
        render(page, chart)
        root = svg_root(page)
        panels = [
            next((g for g in root.iter() if g.get("data-name") == f"panel-{i}"))
            for i in (0, 1)
        ]
        dots = [
            next((g for g in panel.iter() if g.get("data-mark-type") == "point"))
            for panel in panels
        ]
        boxes = [
            page.evaluate(
                "i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i
            )
            for i in (0, 1)
        ]
        domains = [
            points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
            for axis in ("x", "y")
        ]
        coordinates = paga_compare_point_coordinates(page)
        nodes = next(
            (rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0])
        )
        colors = []
        for node in nodes:
            row = np.flatnonzero(a.obs["cluster"] == node["_group"])[0]
            positions = [a.obsm["X_umap"][row, :2], [node["_x"], node["_y"]]]
            fills = []
            for i, (x, y) in enumerate(positions):
                box = boxes[i]
                target = [
                    box["x"] + (x - domains[0][0]) / np.ptp(domains[0]) * box["width"],
                    box["y"] + (domains[1][1] - y) / np.ptp(domains[1]) * box["height"],
                ]
                index = np.argmin(np.linalg.norm(coordinates[i] - target, axis=1))
                assert np.linalg.norm(coordinates[i][index] - target) < 1
                fills.append(dots[i][index].get("fill", dots[i].get("fill")))
            assert fills[0] == fills[1] and fills[0] is not None
            colors.append(fills[0])
        assert len(set(colors)) == len(nodes)

    @pytest.mark.parametrize("color", [None, "score"])
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_comparison_has_matched_domains_labels_and_native_guides(
        self, page, tmp_path, color
    ):
        a = make_compare()
        # Stored non-group layouts can extend beyond the embedding without expanding its limits.
        options = (
            {"color": color, "pos": [[1, 0.1], [2, 0.2], [3, 0.3], [40, 40]]}
            if color
            else {}
        )
        chart = gsc.pl.paga_compare(
            a,
            legend_fontweight="normal",
            show_node_labels=True,
            width=380,
            height=300,
            show=False,
            **options,
        )
        spec = chart.to_dict()
        first = render(page, chart)
        second = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
        assert first["width"] == second["width"] == 380
        assert first["height"] == second["height"] == 300
        assert first["y"] == second["y"]
        assert first["x"] + first["width"] < second["x"]
        domain = [
            points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
            for axis in ("x", "y")
        ]
        root = svg_root(page)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert ("score" if color else "cluster") in texts
        assert all((group in texts for group in ("A", "B", "C")))
        circles = paga_compare_point_coordinates(page)
        assert len(circles) == 2
        expected = a.uns["paga"]["pos"]
        expected = expected[
            (expected[:, 0] >= domain[0][0])
            & (expected[:, 0] <= domain[0][1])
            & (expected[:, 1] >= domain[1][0])
            & (expected[:, 1] <= domain[1][1])
        ]
        centers = np.column_stack(
            [
                second["x"]
                + (expected[:, 0] - domain[0][0]) / np.ptp(domain[0]) * second["width"],
                second["y"]
                + (domain[1][1] - expected[:, 1])
                / np.ptp(domain[1])
                * second["height"],
            ]
        )
        assert len(circles[1]) == len(centers)
        for center in centers:
            assert np.min(np.linalg.norm(circles[1] - center, axis=1)) < 1
        gradients = [e for e in root.iter() if e.tag.endswith("linearGradient")]
        assert bool(gradients) == bool(color)
        page.screenshot(path=str(tmp_path / "comparison.png"), full_page=True)

    def test_observation_and_group_hover_shared_zoom_pan_and_offline_html(
        self, page, tmp_path
    ):
        a = make_compare()
        chart = gsc.pl.paga_compare(
            a,
            legend_fontweight="normal",
            zoom=True,
            legend_loc="right margin",
            size=144,
            width=380,
            height=300,
            show=False,
        )
        spec = chart.to_dict()
        first = render(page, chart)
        second = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-1'})")
        domains = [
            points(spec["hconcat"][0])["encoding"][axis]["scale"]["domain"]
            for axis in ("x", "y")
        ]
        xy = a.obsm["X_umap"][3]
        move_to(page, first, *xy[:2], *domains, "cell-3")
        assert page.get_by_text("cell-3", exact=True).first.is_visible()
        node = a.uns["paga"]["pos"][1]
        projected = [
            second["x"]
            + (node[0] - domains[0][0]) / np.ptp(domains[0]) * second["width"],
            second["y"]
            + (domains[1][1] - node[1]) / np.ptp(domains[1]) * second["height"],
        ]
        hover_at(page, *projected)
        page.locator("table.attributes").get_by_text("Cells", exact=True).wait_for(
            state="visible"
        )
        assert [
            value.strip()
            for value in page.locator("table.attributes td").all_text_contents()[:3]
        ] == ["B", "B", "4"]
        before = paga_compare_point_coordinates(page)
        canvas = page.locator("canvas").first.bounding_box()
        x, y = (canvas["x"] + second["x"] + 190, canvas["y"] + second["y"] + 150)
        page.mouse.move(x, y)
        page.mouse.wheel(0, -20)
        page.wait_for_timeout(500)
        zoomed = paga_compare_point_coordinates(page)
        assert all(
            (
                np.ptp(after[:, 0]) > np.ptp(prior[:, 0])
                for prior, after in zip(before, zoomed, strict=True)
            )
        ), (before, zoomed)
        page.mouse.down()
        page.mouse.move(x + 12, y + 10, steps=5)
        page.mouse.up()
        page.wait_for_timeout(300)
        panned = paga_compare_point_coordinates(page)
        assert all(
            (
                not np.array_equal(left, right)
                for left, right in zip(zoomed, panned, strict=True)
            )
        )
        output = tmp_path / "compare.html"
        chart.save(output, inline=True, controls=False)
        page.route("https://**", lambda route: route.abort())
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        assert page.locator(".message-box").count() == 0

    def test_composed_comparisons_keep_navigation_inside_their_own_pair(
        self, page, tmp_path
    ):
        chart = gsc.pl.paga_compare(
            make_compare(),
            legend_fontweight="normal",
            zoom=True,
            width=280,
            height=220,
            show=False,
        )
        combined = (
            gs.vconcat(chart, chart)
            .resolve_scale(default="independent")
            .resolve_legend(default="independent")
        )
        bounds = render(page, combined)
        names = tuple((f"panel-{i}" for i in range(4)))

        def positions():
            locations = paga_compare_point_coordinates(page, names)
            boxes = [
                page.evaluate(
                    "name=>api.views.getLayoutBounds({scope:[],view:name})", name
                )
                for name in names
            ]
            return [
                rows - [box["x"], box["y"]]
                for rows, box in zip(locations, boxes, strict=True)
            ]

        before = positions()
        canvas = page.locator("canvas").first.bounding_box()
        x, y = (canvas["x"] + bounds["x"] + 140, canvas["y"] + bounds["y"] + 110)
        page.mouse.move(x, y)
        page.mouse.wheel(0, -20)
        page.wait_for_timeout(350)
        zoomed = positions()
        for i in (0, 1):
            assert np.ptp(zoomed[i][:, 0]) > np.ptp(before[i][:, 0])
        for i in (2, 3):
            np.testing.assert_allclose(zoomed[i], before[i], atol=0.2)
        page.mouse.down()
        page.mouse.move(x + 10, y + 8, steps=5)
        page.mouse.up()
        page.wait_for_timeout(250)
        panned = positions()
        assert all((not np.array_equal(panned[i], zoomed[i]) for i in (0, 1)))
        for i in (2, 3):
            np.testing.assert_allclose(panned[i], before[i], atol=0.2)
        output = tmp_path / "independent-comparisons.html"
        combined.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        assert not page.locator(".message-box").count()

    @pytest.mark.parametrize("node_labels", [False, True])
    def test_on_data_labels_displace_and_reflow_on_zoom(self, page, node_labels):
        from tests.integrations.scanpy.browser.interactions import pointer, position
        from tests.integrations.scanpy.helpers import name_embedding_scales

        a = make_compare()
        names = ["Alpha cells", "Beta cells", "Gamma cells", "Delta cells"]
        a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
        xy = np.column_stack(
            [a.obs["cluster"].cat.codes.to_numpy() * 0.1, np.zeros(a.n_obs)]
        )
        xy[:2, 0] = [-10, 10]
        a.obsm["X_umap"] = xy
        chart = gsc.pl.paga_compare(
            a,
            legend_fontweight="normal",
            legend_fontsize=12,
            legend_loc="none" if node_labels else "on data",
            show_node_labels=node_labels,
            width=400,
            height=300,
            zoom=True,
            show=False,
        )
        bounds = render(page, name_embedding_scales(chart.to_dict(), "labels"))
        page.wait_for_timeout(1200)

        def label_offsets():
            """Read native label offsets from their median anchors in the current viewport."""
            root = svg_root(page)
            group = next(
                (
                    g
                    for g in root.iter()
                    if g.get("data-mark-type") == "text"
                    and g.get("clip-path")
                    and ({e.text for e in g} == set(names))
                )
            )
            clip_id = group.get("clip-path").removeprefix("url(#").removesuffix(")")
            box = next((e[0] for e in root.iter() if e.get("id") == clip_id))
            domains = page.evaluate(
                "['x-0', 'y-1'].map(n=>api.getScaleResolutionByName('labels-'+n).getDomain())"
            )
            offsets = {}
            for element in group:
                i = names.index(element.text)
                anchor = np.array(
                    [
                        float(box.get("x"))
                        + (i * 0.1 - domains[0][0])
                        / np.ptp(domains[0])
                        * float(box.get("width")),
                        float(box.get("y"))
                        + domains[1][1] / np.ptp(domains[1]) * float(box.get("height")),
                    ]
                )
                offsets[element.text] = np.array(position(element)) - anchor
            return offsets

        before = label_offsets()
        assert set(before) == set(names)
        assert max((np.linalg.norm(value) for value in before.values())) > 10
        pointer(page, bounds)
        page.mouse.wheel(0, -600)
        page.wait_for_timeout(1200)
        after = label_offsets()
        assert set(after) == set(before)
        assert any((np.linalg.norm(after[key] - before[key]) > 1 for key in names))

    def test_long_group_key_fits_below_a_notebook_sized_comparison(self, page):
        from tests.integrations.scanpy.browser.interactions import position

        a = make_compare()
        names = [
            "CD4+/CD45RA+/CD25- Naive T",
            "CD4+/CD45RO+ Memory",
            "CD8+ Cytotoxic T",
            "CD14+ Monocyte",
        ]
        a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
        chart = gsc.pl.paga_compare(
            a, legend_fontweight="normal", width=300, height=300, show=False
        )
        render(page, chart)
        assert page.evaluate("api.getLogicalCanvasSize().width") <= 786
        root = svg_root(page)
        key = [
            e
            for g in root.iter()
            if g.get("data-mark-type") == "text" and (not g.get("clip-path"))
            for e in g
            if e.text in names
        ]
        assert {e.text for e in key} == set(names)
        bottom = max(
            (
                float(e[0].get("y")) + float(e[0].get("height"))
                for e in root.iter()
                if e.tag.endswith("clipPath")
            )
        )
        assert all((position(e)[1] > bottom for e in key))
