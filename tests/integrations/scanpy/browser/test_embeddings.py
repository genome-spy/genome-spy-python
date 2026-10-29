"""Embeddings behavior and regressions."""

import json
from io import BytesIO
from pathlib import Path

import numpy as np
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import move_to, wait_for_navigation
from tests.integrations.scanpy.browser.rendering import (
    assert_complete_chart,
    panel_image,
    render,
)
from tests.integrations.scanpy.embedding_fixtures import (
    embedding_cases,
    graph_adata,
    make_embedding_adata,
    make_scatter_adata,
    reference_cases,
    scatter_cases,
)
from tests.integrations.scanpy.embedding_fixtures import umap_data as fixture
from tests.integrations.scanpy.helpers import name_embedding_scales, points, units

sc = pytest.importorskip("scanpy")
mpl = pytest.importorskip("matplotlib")
Image = pytest.importorskip("PIL.Image")
UMAP_REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
UMAP_REFERENCE = json.loads((UMAP_REFERENCE_DIR / "umap.json").read_text())


class TestUmap:
    """Observed Scanpy UMAP hover, navigation, offline delivery and render fidelity."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("color", ["cell_type", "score"])
    def test_hover_reports_known_zero_nonzero_and_missing_observations(
        self, page, color
    ):
        a = fixture()
        # Give the missing observation an exposed point for the hover assertion.
        # Duplicate-coordinate preservation is tested independently in Python.
        a.obsm["X_umap"][2, :2] = [-0.5, 0.5]
        with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
            chart = gsc.pl.umap(
                a, color=color, size=144, frameon=False, show=False, obs_id="cell_id"
            )
        bounds = render(page, chart)
        spec = chart.to_dict()
        unit = points(spec)
        domains = [unit["encoding"][d]["scale"]["domain"] for d in ("x", "y")]
        for index in [1, 4, 6, 2]:
            x, y = a.obsm["X_umap"][index, :2]
            move_to(page, bounds, float(x), float(y), *domains, f"stable-{index}")
            page.get_by_text(f"stable-{index}", exact=True).wait_for(state="visible")
            assert page.get_by_text("Observation ID", exact=True).is_visible()

    @pytest.mark.parametrize("offset", [0.3, 0.65])
    def test_tiny_points_can_be_hovered_at_their_center(self, page, offset):
        a = fixture()[:1].copy()
        a.obsm["X_umap"] = np.array([[0.0, 0.0]])
        chart = gsc.pl.umap(
            a,
            size=2,
            frameon=False,
            width=100,
            height=100,
            show=False,
            obs_id="cell_id",
        )
        bounds = render(page, chart)
        page.locator("#chart").evaluate(
            "(element, offset) => element.style.marginLeft = `${offset}px`", offset
        )
        domain = points(chart.to_dict())["encoding"]["x"]["scale"]["domain"]
        x, y = move_to(page, bounds, 0, 0, domain, domain, "stable-0")
        page.mouse.move(x, y)
        page.wait_for_timeout(80)
        assert page.get_by_text("stable-0", exact=True).is_visible()

    def test_zero_size_observations_are_not_pickable(self, page):
        a = fixture()[:2].copy()
        chart = gsc.pl.umap(
            a,
            size=[2, 0],
            frameon=False,
            width=100,
            height=100,
            show=False,
            obs_id="cell_id",
        )
        bounds = render(page, chart)
        encoding = points(chart.to_dict())["encoding"]
        domains = [encoding[d]["scale"]["domain"] for d in ("x", "y")]
        move_to(
            page, bounds, *map(float, a.obsm["X_umap"][0, :2]), *domains, "stable-0"
        )
        assert page.get_by_text("stable-0", exact=True).is_visible()
        move_to(
            page, bounds, *map(float, a.obsm["X_umap"][1, :2]), *domains, "stable-1"
        )
        assert not page.get_by_text("stable-1", exact=True).is_visible()

    @pytest.mark.parametrize("case", ["categorical", "continuous", "grid"])
    def test_complete_chart_has_original_guides_labels_and_unclipped_layout(
        self, page, tmp_path, case
    ):
        with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
            chart = gsc.pl.umap(
                fixture(),
                **reference_cases()[case],
                size=np.arange(8) * 7 + 25,
                show=False,
            )
        render(page, chart, renderer="canvas")
        svg = page.evaluate(
            "async () => { const result=await api.imageExport.svg(); return await result.blob.text(); }"
        )
        assert "<svg" in svg
        if case == "categorical":
            for label in ["C", "B", "A", "unused", "NA", "UMAP1", "UMAP2", "cell_type"]:
                assert label in svg
        if case == "continuous":
            assert "score" in svg
            assert "UMAP1" not in svg and "UMAP2" not in svg
        if case == "grid":
            assert svg.count("g1") >= 2
            assert svg.count("score") >= 2
            assert "raw_only" in svg
        page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
        geometry = page.evaluate(
            "({logical:api.getLogicalCanvasSize(),rendered:api.getRenderedBounds()})"
        )
        assert geometry["rendered"]["width"] <= geometry["logical"]["width"] + 1
        assert geometry["rendered"]["height"] <= geometry["logical"]["height"] + 1

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize(
        "marker,token,linewidth",
        [
            (".", "dot", 0),
            ("o", "circle", 0),
            (".", "dot-stroke", 2),
            ("s", "square", 0),
            ("s", "square-stroke", 2),
            ("D", "diamond", 0),
            ("D", "diamond-stroke", 2),
        ],
    )
    def test_rendered_marker_footprint_matches_registered_scanpy_export(
        self, page, tmp_path, reference_images, marker, token, linewidth
    ):
        a = fixture()[:1].copy()
        a.obsm["X_umap"] = np.array([[0.0, 0.0]])
        # Reference exports at 150 DPI from a 100-DPI figure; browser DPR is 1.5.
        with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 150}):
            chart = gsc.pl.umap(
                a,
                size=144,
                marker=marker,
                na_color="black",
                frameon=False,
                show=False,
                edgecolors="black" if linewidth else "none",
                linewidths=linewidth,
            )
        bounds = render(page, chart)
        actual = panel_image(page, bounds)
        reference = Image.open(
            reference_images("umap") / f"footprint-{token}.png"
        ).convert("RGB")

        def footprint(image):
            pixels = np.asarray(image)
            yy, xx = np.where(pixels.max(axis=2) < 128)
            assert len(xx) > 20
            return np.array([xx.max() - xx.min() + 1, yy.max() - yy.min() + 1])

        expected = UMAP_REFERENCE[f"footprint_{token}"]["diameter_at_export"]
        np.testing.assert_allclose(footprint(actual), footprint(reference), atol=2)
        np.testing.assert_allclose(footprint(actual), [expected, expected], atol=2)
        # A fourfold size mistake doubles the diameter and cannot pass this oracle.
        assert np.all(np.abs(footprint(actual) * 2 - footprint(reference)) > 2)
        if marker in ("s", "D"):
            mask = np.asarray(actual).max(axis=2) < 128
            yy, xx = np.where(mask)
            coverage = mask[yy.min() : yy.max() + 1, xx.min() : xx.max() + 1].mean()
            # Equal bounds alone cannot distinguish circles, squares and diamonds.
            assert coverage > 0.95 if marker == "s" else 0.45 < coverage < 0.6
        actual.save(tmp_path / f"native-{token}.png")
        Image.blend(
            reference.crop(
                (
                    0,
                    0,
                    min(actual.width, reference.width),
                    min(actual.height, reference.height),
                )
            ),
            actual.crop(
                (
                    0,
                    0,
                    min(actual.width, reference.width),
                    min(actual.height, reference.height),
                )
            ),
            0.5,
        ).save(tmp_path / f"overlay-{token}.png")

    @pytest.mark.smoke
    def test_wheel_navigation_changes_coordinates_and_offline_html_needs_no_network(
        self, page, tmp_path
    ):
        calls = []

        def upper(values):
            calls.append(values.copy())
            return float(np.nanmax(values))

        with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
            chart = gsc.pl.umap(
                fixture(),
                color="score",
                vmax=upper,
                size=100,
                zoom=True,
                frameon=False,
                show=False,
            )
        bounds = render(page, name_embedding_scales(chart.to_dict(), "umap"))
        canvas = page.locator("canvas").first.bounding_box()
        before = page.locator("canvas").first.screenshot()
        domains = page.evaluate(
            "['umap-x-0', 'umap-y-1'].map(name => api.getScaleResolutionByName(name).getDomain())"
        )
        page.mouse.move(
            canvas["x"] + bounds["x"] + bounds["width"] / 2,
            canvas["y"] + bounds["y"] + bounds["height"] / 2,
        )
        page.mouse.wheel(0, -300)
        page.wait_for_function(
            "before => ['umap-x-0', 'umap-y-1'].every((name, i) => {\n            const domain = api.getScaleResolutionByName(name).getDomain();\n            return domain[1] - domain[0] < before[i][1] - before[i][0];\n        })",
            arg=domains,
        )
        # Finish the wheel gesture before issuing a separate reset action.
        wait_for_navigation(page, "umap", scale_names=["umap-x-0", "umap-y-1"])
        assert page.locator("canvas").first.screenshot() != before
        page.evaluate("api.getScaleResolutionByName('umap-x-0').resetZoom()")
        page.evaluate("api.getScaleResolutionByName('umap-y-1').resetZoom()")
        page.wait_for_function(
            """before => ['umap-x-0', 'umap-y-1'].every((name, i) =>
                api.getScaleResolutionByName(name).getDomain().every(
                    (value, j) => Math.abs(value - before[i][j]) < 1e-6))""",
            arg=domains,
        )
        output = tmp_path / "umap.html"
        chart.save(output, inline=True, controls=False)
        requests = []
        page.on(
            "request",
            lambda request: (
                requests.append(request.url)
                if request.url.startswith(("https:", "http:"))
                else None
            ),
        )
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not requests
        assert page.locator(".message-box").count() == 0
        assert len(calls) == 1
        np.testing.assert_array_equal(calls[0], [np.nan, -1, 0, 0, 1, 1, 2, 4])

    @pytest.mark.parametrize("color", ["cell_type", "score"])
    def test_overlapping_points_hover_the_last_visible_observation(self, page, color):
        a = fixture()
        chart = gsc.pl.umap(
            a, color=color, size=144, frameon=False, show=False, obs_id="cell_id"
        )
        bounds = render(page, chart)
        spec = points(chart.to_dict())
        domains = [spec["encoding"][d]["scale"]["domain"] for d in ("x", "y")]
        move_to(page, bounds, -2, -1, *domains, "stable-0")
        page.get_by_text("stable-0", exact=True).wait_for(state="visible")
        assert not page.get_by_text("stable-2", exact=True).is_visible()

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", ["categorical", "continuous", "grid"])
    def test_registered_plot_areas_match_reference_positions_colors_and_footprints(
        self, page, tmp_path, reference_images, case
    ):
        from scipy.ndimage import distance_transform_edt

        page.set_viewport_size({"width": 2800, "height": 1800})
        width, height = UMAP_REFERENCE["cases"][case]["panels"][0]["plot_size"]
        chart = gsc.pl.umap(
            fixture(),
            **reference_cases()[case],
            size=np.arange(8) * 7 + 25,
            width=width,
            height=height,
            show=False,
        )
        render(page, chart)
        for i, panel in enumerate(UMAP_REFERENCE["cases"][case]["panels"]):
            bounds = page.evaluate(
                "i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i
            )
            np.testing.assert_allclose(
                [bounds["width"], bounds["height"]],
                np.array(panel["plot_size"]),
                atol=1,
            )
            # Native layout rounds panel edges to backing pixels.
            actual = panel_image(page, bounds)
            expected = Image.open(
                reference_images("umap") / f"{case}-panel-{i}.png"
            ).convert("RGB")
            assert abs(actual.width - expected.width) <= 1
            assert abs(actual.height - expected.height) <= 1
            # Only the known one-pixel crop rounding is reconciled; no image fit,
            # rotation, fitted scale, or per-point alignment is permitted.
            extent = (
                0,
                0,
                min(actual.width, expected.width),
                min(actual.height, expected.height),
            )
            native = np.asarray(actual.crop(extent)).astype(int)
            reference = np.asarray(expected.crop(extent)).astype(int)

            def colored(pixels):
                return (pixels.max(axis=2) - pixels.min(axis=2) > 25) & (
                    pixels.min(axis=2) < 220
                )

            native_ink, reference_ink = (colored(native), colored(reference))
            assert native_ink.sum() > 30 and reference_ink.sum() > 30
            # Layout rounds logical edges before DPR conversion; include only the
            # measured rounding displacement, without fitting or shifting images.
            rounding = 1.5 * np.max(
                np.abs(
                    np.array([bounds["width"], bounds["height"]]) - panel["plot_size"]
                )
            )
            assert rounding <= 1.5
            assert (
                distance_transform_edt(~reference_ink)[native_ink].max()
                <= 2.5 + rounding
            )
            assert (
                distance_transform_edt(~native_ink)[reference_ink].max()
                <= 2.5 + rounding
            )
            # Compare actual interior paint at each non-overlapping observation.
            # Antialiased intersections can blend two valid colors differently in
            # Agg/WebGL, so they are covered by geometry and draw-order checks.
            for source_index, (x, y), paint in zip(
                panel["order"], panel["coordinates"], panel["colors"], strict=True
            ):
                if source_index in (0, 2):
                    continue
                xd, yd = (panel["x_domain"], panel["y_domain"])
                px = round((x - xd[0]) / (xd[1] - xd[0]) * bounds["width"] * 1.5)
                py = round((1 - (y - yd[0]) / (yd[1] - yd[0])) * bounds["height"] * 1.5)
                expected_color = np.array(
                    [int(paint[j : j + 2], 16) for j in (1, 3, 5)]
                )
                region = native[max(0, py - 1) : py + 2, max(0, px - 1) : px + 2]
                assert np.abs(region - expected_color).max(axis=2).min() <= 12
            actual.save(tmp_path / f"{case}-native-panel-{i}.png")
            Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
                tmp_path / f"{case}-registered-overlay-{i}.png"
            )

    def test_zero_size_points_leave_no_visible_footprint(self, page):
        a = fixture()[:1].copy()
        chart = gsc.pl.umap(
            a, size=0, frameon=False, na_color="black", hover=False, show=False
        )
        render(page, chart)
        pixels = np.asarray(
            Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
                "RGB"
            )
        )
        assert pixels.min() == 255

    @pytest.mark.parametrize(
        "colorbar,expected", [(None, [68, 1, 84]), ("right", [33, 145, 140])]
    )
    def test_constant_expression_preserves_scanpy_colorbar_normalization(
        self, page, colorbar, expected
    ):
        a = fixture()[:1].copy()
        a.obs["score"] = 5.0
        bounds = render(
            page,
            gsc.pl.umap(
                a,
                color="score",
                colorbar_loc=colorbar,
                size=144,
                frameon=False,
                show=False,
            ),
        )
        pixels = Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert(
            "RGB"
        )
        center = (
            round(bounds["x"] + bounds["width"] / 2),
            round(bounds["y"] + bounds["height"] / 2),
        )
        np.testing.assert_allclose(pixels.getpixel(center), expected, atol=3)

    def test_native_sized_panels_and_numeric_guide_fit_side_by_side(
        self, page, tmp_path
    ):
        page.set_viewport_size({"width": 1000, "height": 700})
        chart = gsc.pl.umap(
            fixture(),
            color=["cell_type", "score"],
            size=144,
            width=300,
            height=260,
            ncols=2,
            zoom=True,
            obs_id="cell_id",
            show=False,
        )
        render(page, name_embedding_scales(chart.to_dict(), "umap"))
        panels = page.evaluate(
            "[0,1].map(i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`}))"
        )
        for panel in panels:
            np.testing.assert_allclose(
                [panel["width"], panel["height"]], [300, 260], atol=1
            )
        assert panels[1]["x"] > panels[0]["x"] + panels[0]["width"]
        assert abs(panels[0]["y"] - panels[1]["y"]) < 1
        canvas = page.locator("canvas").first
        assert canvas.bounding_box()["width"] <= 1000
        png = canvas.screenshot(path=str(tmp_path / "native-sized-umap.png"))
        pixels = np.asarray(Image.open(BytesIO(png)).convert("RGB")).astype(int)
        # Only the continuous guide lies right of the second plot. Its chromatic
        # pixels must reach both ends of the requested panel, inside the canvas.
        guide = pixels[:, int(np.ceil(panels[1]["x"] + panels[1]["width"])) + 1 :]
        yy, _ = np.where(guide.max(axis=2) - guide.min(axis=2) > 70)
        assert len(yy) > 100
        assert abs(yy.min() - panels[1]["y"]) <= 2
        assert abs(yy.max() - (panels[1]["y"] + panels[1]["height"])) <= 2
        spec = chart.to_dict()
        domains = [
            points(units(spec)[0])["encoding"][d]["scale"]["domain"] for d in ("x", "y")
        ]
        move_to(page, panels[0], 1, 0, *domains, "stable-1")
        page.get_by_text("stable-1", exact=True).wait_for(state="visible")
        page.mouse.wheel(0, -300)
        page.wait_for_function(
            "low=>api.getScaleResolutionByName('umap-x-0').getDomain()[0]>low",
            arg=domains[0][0],
        )


EMBEDDING_REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/embedding.json").read_text()
)["cases"]


class TestEmbedding:
    """Observe shared embedding rendering, native navigation, hover and linked selection."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", embedding_cases())
    def test_complete_embedding_matches_registered_points_guides_and_axis_labels(
        self, page, tmp_path, reference_images, case
    ):
        expected = EMBEDDING_REFERENCE[case]
        family, options = embedding_cases()[case]
        chart = getattr(gsc.pl, family)(
            make_embedding_adata(),
            **options,
            size=np.arange(8) * 7 + 25,
            frameon=True,
            width=expected["plot_size"][0],
            height=expected["plot_size"][1],
            show=False,
        )
        assert_complete_chart(
            page,
            tmp_path,
            chart,
            expected,
            reference_images("embedding") / f"{case}-panel.png",
            case,
        )

    @pytest.mark.parametrize("basis", ["tsne", "diffmap", "pca", "draw_graph_fa"])
    @pytest.mark.parametrize("location", ["left", "top"])
    def test_shared_hover_zoom_and_offline_delivery(
        self, page, tmp_path, basis, location
    ):
        a = graph_adata()
        chart = gsc.pl.embedding(
            a,
            basis,
            color="score",
            edges=True,
            vcenter="p50",
            colorbar_loc=location,
            obs_id="cell_id",
            size=100,
            zoom=True,
            frameon=True,
            show=False,
        )
        spec = chart.to_dict()
        mark = points(spec)
        bounds = render(page, name_embedding_scales(chart.to_dict(), basis))
        coords = a.obsm[f"X_{basis}"][4, :2]
        move_to(
            page,
            bounds,
            *map(float, coords),
            mark["encoding"]["x"]["scale"]["domain"],
            mark["encoding"]["y"]["scale"]["domain"],
            "stable-4",
        )
        assert page.locator("table.attributes th").all_text_contents()[-2:] == [
            mark["encoding"][axis]["axis"]["title"] for axis in ("x", "y")
        ]
        expression = "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())"
        names = [f"{basis}-x-0", f"{basis}-y-1"]
        before = page.evaluate(expression, names)
        page.mouse.wheel(0, -220)
        page.wait_for_function(
            "({names,before})=>names.every((n,i)=>api.getScaleResolutionByName(n).getDomain()[1]-api.getScaleResolutionByName(n).getDomain()[0]<before[i][1]-before[i][0])",
            arg={"names": names, "before": before},
        )
        path = tmp_path / f"{basis}.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    def test_pca_brush_count_and_python_membership_agree(self, page):
        a = graph_adata()
        brush = gs.selection_interval("cells", encodings=["x", "y"])
        chart = gsc.pl.pca(
            a,
            color=["cell_type", "score"],
            edges=True,
            vcenter=[None, 0],
            colorbar_loc="bottom",
            selection=brush,
            show=False,
        )
        bounds = render(page, chart)
        canvas = page.locator("canvas").first.bounding_box()
        x, y = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        page.mouse.move(x + bounds["width"] * 0.15, y + bounds["height"] * 0.2)
        page.mouse.down()
        page.mouse.move(
            x + bounds["width"] * 0.65, y + bounds["height"] * 0.7, steps=12
        )
        page.mouse.up()
        snapshot = page.evaluate("api.getParam('cells').getValue()")
        mask = gsc.selection_mask(a, snapshot, basis="pca")
        assert 0 < mask.sum() < a.n_obs
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        assert f"{mask.sum()} cells selected" in svg


SCATTER_REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/scatter.json").read_text()
)["cases"]


class TestScatter:
    """Observe scatter's shared point renderer, native axes, hover and navigation."""

    @pytest.mark.reference
    @pytest.mark.parametrize("family", ["umap", "scatter"])
    @pytest.mark.parametrize(
        "marker,shape", [("o", "circle"), ("s", "rect"), ("D", "path")]
    )
    def test_category_legend_matches_panel_marker_and_expected_width(
        self, page, family, marker, shape
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc
        from matplotlib.markers import MarkerStyle

        data = make_scatter_adata()
        data.obs["two"] = ["A", "B"] * (data.n_obs // 2)
        args = (data, "x_value", "y_value") if family == "scatter" else (data,)
        options = dict(color="two", marker=marker, show=False)
        ax = getattr(sc.pl, family)(*args, **options)
        handle = ax.get_legend().legend_handles[0]
        reference_marker = MarkerStyle(marker)
        path = (
            reference_marker.get_path().transformed(reference_marker.get_transform())
            if family == "umap"
            else handle.get_paths()[0]
        )
        expected_width = (
            handle.get_sizes()[0] ** 0.5 * path.get_extents().width * 100 / 72
        )
        plt.close(ax.figure)
        bounds = render(page, getattr(gsc.pl, family)(*args, **options))
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        symbols = page.evaluate(
            "({svg,edge}) => {\n        const root = new DOMParser().parseFromString(svg,'image/svg+xml').documentElement;\n        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        document.body.append(root);\n        const symbols = [...root.querySelectorAll('circle,rect,path')].flatMap(n => {\n            const b=n.getBoundingClientRect();\n            return b.x > edge ? [{shape:n.tagName,width:b.width}] : [];\n        });\n        root.remove();\n        return symbols;\n        }",
            {"svg": svg, "edge": bounds["x"] + bounds["width"]},
        )
        assert len(symbols) == 2
        assert all((s["shape"] == shape for s in symbols))
        assert all(
            (s["width"] == pytest.approx(expected_width, abs=0.1) for s in symbols)
        )

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("case", scatter_cases())
    def test_complete_scatter_matches_registered_points_axes_labels_and_guides(
        self, page, tmp_path, reference_images, case
    ):
        expected = SCATTER_REFERENCE[case]
        chart = gsc.pl.scatter(
            make_scatter_adata(),
            **scatter_cases()[case],
            size=80,
            frameon=True,
            width=expected["plot_size"][0],
            height=expected["plot_size"][1],
            show=False,
        )
        assert_complete_chart(
            page,
            tmp_path,
            chart,
            expected,
            reference_images("scatter") / f"{case}-panel.png",
            case,
        )

    @pytest.mark.parametrize("axis", ["obs", "var"])
    def test_scatter_hover_zoom_and_offline_html_use_existing_embedding_interactions(
        self, page, tmp_path, axis
    ):
        options = (
            dict(x="x_value", y="y_value", color="cell_type")
            if axis == "obs"
            else dict(x="mean_value", y="dispersion", color="gene_group")
        )
        chart = gsc.pl.scatter(
            make_scatter_adata(), **options, size=200, zoom=True, show=False
        )
        spec = chart.to_dict()
        point = points(spec)
        bounds = render(page, name_embedding_scales(chart.to_dict(), "scatter"))
        row = next(iter(spec["datasets"].values()))[4 if axis == "obs" else 1]
        domains = [point["encoding"][a]["scale"]["domain"] for a in ("x", "y")]
        move_to(
            page, bounds, row["_coord_0"], row["_coord_1"], *domains, row["_obs_label"]
        )
        page.get_by_text(
            "Observation" if axis == "obs" else "Variable", exact=True
        ).wait_for(state="visible")
        assert [
            name for name in page.locator("table.attributes th").all_text_contents()
        ][-2:] == [options["x"], options["y"]]
        assert [
            value.strip()
            for value in page.locator("table.attributes td").all_text_contents()[:2]
        ] == [row["_obs_id"], row["_obs_label"]]
        names = ["scatter-x-0", "scatter-y-1"]
        expression = "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())"
        before = page.evaluate(expression, names)
        page.mouse.wheel(0, -220)
        page.wait_for_function(
            "({names,before})=>names.every((n,i)=>api.getScaleResolutionByName(n).getDomain()[1]-api.getScaleResolutionByName(n).getDomain()[0]<before[i][1]-before[i][0])",
            arg={"names": names, "before": before},
        )
        path = tmp_path / f"scatter-{axis}.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    @pytest.mark.parametrize("family,rows", [("scatter", 1), ("umap", 1), ("umap", 2)])
    def test_native_collected_legends_fit_below_all_panels_with_compact_symbols(
        self, page, tmp_path, family, rows
    ):
        import scanpy as sc

        a = sc.datasets.pbmc68k_reduced()
        options = (
            {"x": "n_counts", "y": "n_genes"} if family == "scatter" else {"ncols": 2}
        )
        colors = (
            ["louvain", "percent_mito"]
            if rows == 1
            else ["louvain", "n_counts", "phase", "percent_mito"]
        )
        chart = (
            getattr(gsc.pl, family)(
                a, color=colors, width=280, height=280, show=False, **options
            )
            .resolve_legend(default="collected")
            .configure_legend(
                orient="bottom",
                direction="horizontal",
                columns=6,
                symbolSize=64,
                gradientLength=140,
                gradientThickness=10,
                tickCount=3,
                layout={"anchor": "middle", "wrap": True},
            )
        )
        render(page, chart)
        bounds = [
            page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i)
            for i in range(len(colors))
        ]
        plot_bottom = max((b["y"] + b["height"] for b in bounds))
        svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
        guides = page.evaluate(
            "svg=>{\n        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;\n        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        document.body.append(root);\n        const box = node => { const r=node.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height}; };\n        const result = {\n            text: [...root.querySelectorAll('text')].map(n=>({label:n.textContent,...box(n)})),\n            shapes: [...root.querySelectorAll('path,circle,rect')].map(box),\n            gradients: [...root.querySelectorAll('rect')].filter(n=>(n.getAttribute('fill')||'').startsWith('url(')).map(box),\n        };\n        root.remove();\n        return result;\n    }",
            svg,
        )
        labels = [
            r
            for r in guides["text"]
            if r["label"] in [str(i) for i in range(11)] + ["G1", "S", "G2M"]
        ]
        assert len(labels) == 11 + (3 if rows == 2 else 0)
        assert all((label["y"] > plot_bottom for label in labels))
        symbols = [
            b
            for b in guides["shapes"]
            if b["y"] > plot_bottom
            and b["width"] > 4
            and (abs(b["width"] - b["height"]) < 0.1)
        ]
        assert len(symbols) == len(labels)
        assert all((symbol["width"] < 12 for symbol in symbols))
        assert len(guides["gradients"]) == (1 if rows == 1 else 2)
        assert all(
            (
                g["y"] > plot_bottom and abs(g["width"] - 140) < 1
                for g in guides["gradients"]
            )
        )
        for gradient in guides["gradients"]:
            ticks = sorted(
                (
                    label
                    for label in guides["text"]
                    if gradient["y"] + gradient["height"]
                    <= label["y"]
                    < gradient["y"] + gradient["height"] + 25
                    and gradient["x"] - 20
                    <= label["x"]
                    < gradient["x"] + gradient["width"] + 20
                ),
                key=lambda label: label["x"],
            )
            assert len(ticks) >= 2
            assert all(
                (
                    left["x"] + left["width"] <= right["x"]
                    for left, right in zip(ticks, ticks[1:])
                )
            )
        size = page.evaluate("api.getLogicalCanvasSize()")
        for item in labels + symbols + guides["gradients"]:
            assert 0 <= item["x"] and item["x"] + item["width"] <= size["width"] + 1
            assert item["y"] + item["height"] <= size["height"] + 1
        page.screenshot(
            path=str(tmp_path / f"{family}-{rows}-bottom-guides.png"), full_page=True
        )
