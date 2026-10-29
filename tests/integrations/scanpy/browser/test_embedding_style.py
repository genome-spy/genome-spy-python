"""Embedding style behavior and regressions."""

import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData
from PIL import Image
from scipy import sparse
from scipy.ndimage import distance_transform_cdt, maximum_filter, minimum_filter

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy.schema import SCHEMA_VERSION
from tests.integrations.scanpy.browser.interactions import move_to
from tests.integrations.scanpy.browser.rendering import (
    assert_complete_chart,
    guide_geometry,
    render,
)
from tests.integrations.scanpy.embedding_fixtures import (
    graph_adata,
    make_density,
    make_embedding_adata,
)
from tests.integrations.scanpy.helpers import name_embedding_scales, points, units


class TestColorBounds:
    """Centered colors retain native point paint, guides and registered Scanpy geometry."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize(
        "options,constant",
        [
            ({"vcenter": 0, "vmin": -2, "vmax": 4}, False),
            ({"vcenter": "p50"}, False),
            ({"vcenter": 10}, False),
            ({"vcenter": 2}, True),
            ({"vcenter": 2, "colorbar_loc": None}, True),
        ],
    )
    def test_centered_paint_and_guides_match_registered_scanpy(
        self, page, tmp_path, options, constant
    ):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import scanpy as sc

        data = make_embedding_adata()
        data.obs["score"] = 2.0 if constant else [-3, -2, -1, 0, 1, 2, 4, 6]
        options = dict(
            color="score",
            size=144,
            marker="o",
            cmap="viridis",
            frameon=True,
            title="Centered scores",
            show=False,
            **options,
        )
        reference = tmp_path / "scanpy-panel.png"
        with plt.rc_context({"figure.figsize": (4, 3), "figure.dpi": 100}):
            ax = sc.pl.umap(data, **options)
            ax.figure.canvas.draw()
            box = ax.get_window_extent()
            expected = dict(
                coordinates=data.obsm["X_umap"][:, :2].tolist(),
                x_domain=list(ax.get_xlim()),
                y_domain=list(ax.get_ylim()),
                labels=[ax.get_xlabel(), ax.get_ylabel()],
                title=ax.get_title(),
                legend=None,
            )
            ax.figure.savefig(
                reference,
                dpi=150,
                bbox_inches=box.transformed(ax.figure.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            plt.close(ax.figure)
        chart = gsc.pl.umap(data, width=box.width, height=box.height, **options)
        assert_complete_chart(page, tmp_path, chart, expected, reference, "centered")
        if options["vcenter"] == 0:
            guides = guide_geometry(page)
            assert len(guides["gradients"]) == 1
            gradient = guides["gradients"][0]
            zero = next(
                (label for label in guides["text"] if label["label"] in {"0", "0.0"})
            )
            assert (
                abs(
                    zero["y"]
                    + zero["height"] / 2
                    - gradient["y"]
                    - gradient["height"] / 2
                )
                < 2
            )
            canvas = page.locator("canvas").first.bounding_box()
            dpr = page.evaluate("devicePixelRatio")
            x = round((canvas["x"] + gradient["x"] + gradient["width"] / 2) * dpr)
            y = round((canvas["y"] + gradient["y"] + gradient["height"] / 2) * dpr)
            pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
            np.testing.assert_allclose(
                pixels[y, x],
                np.array(matplotlib.colormaps["viridis"](0.5)[:3]) * 255,
                atol=3,
            )


class TestColorbar:
    """Native continuous guides fit their panels and remain configurable after collection."""

    @pytest.mark.parametrize("location", [None, "right", "left", "top", "bottom"])
    @pytest.mark.parametrize("rows", [1, 2])
    def test_colorbars_fit_mixed_panel_grids_without_moving_category_legends(
        self, page, tmp_path, location, rows
    ):
        colors = (
            ["cell_type", "score"] if rows == 1 else ["cell_type", "score", "g1", "g2"]
        )
        chart = gsc.pl.umap(
            make_embedding_adata(),
            color=colors,
            ncols=2,
            colorbar_loc=location,
            width=320,
            height=180,
            frameon=True,
            show=False,
        )
        render(page, chart)
        bounds = [
            page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i)
            for i in range(len(colors))
        ]
        guides = guide_geometry(page)
        assert len(guides["gradients"]) == (0 if location is None else len(colors) - 1)
        for gradient, panel in zip(
            guides["gradients"], bounds[1:], strict=location is not None
        ):
            if location in ("top", "bottom"):
                assert abs(gradient["width"] - panel["width"]) <= 2
                assert gradient["height"] < 15
                if location == "top":
                    assert gradient["y"] + gradient["height"] <= panel["y"]
                else:
                    assert gradient["y"] >= panel["y"] + panel["height"]
            else:
                assert abs(gradient["height"] - panel["height"]) <= 2
                assert gradient["width"] < 15
                if location == "left":
                    assert gradient["x"] + gradient["width"] <= panel["x"]
                else:
                    assert gradient["x"] >= panel["x"] + panel["width"]
        categories = [
            item
            for item in guides["text"]
            if item["label"] in {"C", "B", "A", "unused", "NA"}
        ]
        assert len(categories) == 5
        assert all(
            (item["x"] >= bounds[0]["x"] + bounds[0]["width"] for item in categories)
        )
        size = page.evaluate("api.getLogicalCanvasSize()")
        for item in guides["text"] + guides["gradients"]:
            assert item["x"] >= -1 and item["y"] >= -1
            assert item["x"] + item["width"] <= size["width"] + 1
            assert item["y"] + item["height"] <= size["height"] + 1
        page.screenshot(path=str(tmp_path / f"{rows}-{location}.png"), full_page=True)

    def test_collected_numeric_colorbars_accept_native_orientation_and_size_overrides(
        self, page
    ):
        chart = (
            gsc.pl.umap(
                make_embedding_adata(),
                color=["score", "g1", "g2", "raw_only"],
                colorbar_loc="top",
                ncols=2,
                width=320,
                height=180,
                show=False,
            )
            .resolve_legend(default="collected")
            .configure_legend(
                orient="left",
                direction="vertical",
                gradientLength=140,
                gradientThickness=8,
            )
        )
        render(page, chart)
        guides = guide_geometry(page)
        assert len(guides["gradients"]) == 4
        plot_left = min(
            (
                page.evaluate(
                    "i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i}).x", i
                )
                for i in range(4)
            )
        )
        assert all(
            (
                bar["x"] + bar["width"] < plot_left
                and abs(bar["height"] - 140) <= 2
                and (abs(bar["width"] - 8) < 1)
                for bar in guides["gradients"]
            )
        )
        size = page.evaluate("api.getLogicalCanvasSize()")
        for item in guides["text"] + guides["gradients"]:
            assert item["x"] >= -1 and item["y"] >= -1
            assert item["x"] + item["width"] <= size["width"] + 1
            assert item["y"] + item["height"] <= size["height"] + 1

    @pytest.mark.reference
    @pytest.mark.xfail(
        SCHEMA_VERSION == "1.2.0",
        strict=True,
        raises=AssertionError,
        reason="C11: Core 1.2 vertical legend extent excludes subsequent columns",
    )
    def test_native_vertical_legend_keeps_every_column_visible(self, page, tmp_path):
        categories = [f"category-{i}" for i in range(12)]
        chart = (
            gs.Chart([{"x": i, "group": group} for i, group in enumerate(categories)])
            .mark_point()
            .encode(
                x="x:Q",
                y=gs.value(0.5),
                color=gs.Color("group:N").legend(
                    values=categories, columns=2, title=None
                ),
            )
            .properties(width=300, height=300)
            .configure_legend(
                symbolSize=64,
                labelFontSize=12,
                rowPadding=4,
                layout=gs.LegendLayout(anchor="middle", wrap=False),
            )
        )
        chart.save(tmp_path / "native-legend.html", inline=True, controls=False)
        render(page, chart)
        svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
        (tmp_path / "native-legend.svg").write_text(svg)
        page.screenshot(path=str(tmp_path / "native-legend.png"), full_page=True)
        labels = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
        assert {label for label in labels if label in categories} == set(categories)


def embedding_outlines__pixel_error(pixels, target, radius):
    """Compare painted colors within a small browser rasterization neighborhood."""
    height, width = pixels.shape[:2]
    padded = np.pad(
        target, ((radius, radius), (radius, radius), (0, 0)), constant_values=255
    )
    error = np.full((height, width), 255)
    for y in range(2 * radius + 1):
        for x in range(2 * radius + 1):
            error = np.minimum(
                error,
                np.abs(pixels - padded[y : y + height, x : x + width]).max(axis=2),
            )
    return error


class TestEmbeddingOutlines:
    """Registered outline footprints and draw order in native WebGL rendering."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("marker", [".", "o", "s", "D"])
    @pytest.mark.parametrize("overlap", [False, True])
    @pytest.mark.parametrize("preset", ["default", "custom", "edge"])
    def test_outlined_points_match_registered_scanpy_paint(
        self, page, tmp_path, marker, overlap, preset
    ):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import scanpy as sc

        distance = 0.1 if overlap else 0.4
        data = AnnData(
            obs=pd.DataFrame(
                {"group": pd.Categorical(["A", "A", "A", "B"])},
                index=["lo", "hi", "a", "b"],
            ),
            obsm={
                "X_umap": np.array([[-1, -1], [1, 1], [-distance, 0], [distance, 0]])
            },
        )
        options = dict(
            color="group",
            size=[0, 0, 2304, 5184],
            marker=marker,
            palette=["#4477aa", "#cc6677"],
            add_outline=True,
            legend_loc="none",
            title="",
            frameon=False,
            show=False,
        )
        if preset == "custom":
            options.update(
                outline_width=(0.2, 0.1),
                outline_color=("navy", "ivory"),
                alpha=0.4,
                linewidths=0,
            )
        elif preset == "edge":
            options.update(edgecolor="red", linewidth=2)
        with plt.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
            ax = sc.pl.umap(data, **options)
            ax.figure.canvas.draw()
            box = ax.get_window_extent()
            output = BytesIO()
            ax.figure.savefig(
                output,
                dpi=150,
                bbox_inches=box.transformed(ax.figure.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            reference = Image.open(output).convert("RGB")
            plt.close(ax.figure)
        bounds = render(
            page, gsc.pl.umap(data, width=box.width, height=box.height, **options)
        )
        # Let the embed's opening animation settle before registering painted pixels.
        page.wait_for_timeout(500)
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        canvas = page.locator("canvas").bounding_box()
        # Crop physical pixels so fractional CSS offsets cannot shift the registration.
        dpr = page.evaluate("devicePixelRatio")
        left, top = (canvas["x"] + bounds["x"], canvas["y"] + bounds["y"])
        actual = (
            Image.open(BytesIO(page.screenshot()))
            .convert("RGB")
            .crop(
                (
                    round(left * dpr),
                    round(top * dpr),
                    round((left + bounds["width"]) * dpr),
                    round((top + bounds["height"]) * dpr),
                )
            )
        )
        width, height = (
            min(actual.width, reference.width),
            min(actual.height, reference.height),
        )
        actual, reference = (
            actual.crop((0, 0, width, height)),
            reference.crop((0, 0, width, height)),
        )
        pixels, target = (
            np.asarray(actual).astype(int),
            np.asarray(reference).astype(int),
        )
        actual.save(tmp_path / "native.png")
        reference.save(tmp_path / "scanpy.png")
        Image.blend(actual, reference, 0.5).save(tmp_path / "registered-overlay.png")
        masks = [image.min(axis=2) < 240 for image in (pixels, target)]
        extents = []
        for mask in masks:
            yy, xx = np.where(mask)
            assert len(xx) > 200
            extents.append([xx.min(), yy.min(), xx.max(), yy.max()])
        np.testing.assert_allclose(
            extents[0],
            extents[1],
            atol=3,
            err_msg=str((bounds, box.bounds, actual.size, reference.size)),
        )
        painted = masks[0] | masks[1]
        # Compare flat paint separately from each renderer's antialiasing transitions.
        radius = int(np.ceil(dpr))
        for first, second in ((pixels, target), (target, pixels)):
            neighborhood = (2 * radius + 1, 2 * radius + 1, 1)
            variation = maximum_filter(first, size=neighborhood) - minimum_filter(
                first, size=neighborhood
            )
            interior = painted & (variation.max(axis=2) == 0)
            assert interior.sum() > 200
            assert (
                embedding_outlines__pixel_error(first, second, radius)[interior] > 32
            ).mean() < 0.05

    @pytest.mark.parametrize("marker", ["o", "s", "D"])
    def test_outline_hover_linked_brush_navigation_and_offline_delivery(
        self, page, tmp_path, marker
    ):
        import genome_spy as gs
        from tests.integrations.scanpy.browser.interactions import move_to

        data = AnnData(
            obs=pd.DataFrame(
                {"group": pd.Categorical(["A", "A", "A", "B"])},
                index=["lo", "hi", "a", "b"],
            ),
            obsm={"X_umap": np.array([[-1, -1], [1, 1], [-0.4, 0], [0.4, 0]])},
        )
        brush = gs.selection_interval("cells", encodings=["x", "y"])
        chart = gsc.pl.umap(
            data,
            color="group",
            palette=["#4477aa", "#cc6677"],
            size=[0, 0, 144, 144],
            marker=marker,
            add_outline=True,
            selection=brush,
            zoom=True,
            width=300,
            height=300,
            show=False,
        )
        bounds = render(page, name_embedding_scales(chart.to_dict(), "umap"))
        canvas = page.locator("canvas").bounding_box()
        domains = [
            page.evaluate(
                f"api.getScaleResolutionByName('umap-{axis}-{i}').getDomain()"
            )
            for i, axis in enumerate(("x", "y"))
        ]
        move_to(page, bounds, -0.4, 0, *domains, "a")
        page.get_by_text("Observation ID", exact=True).wait_for(state="visible")

        def location(x, y):
            return (
                canvas["x"]
                + bounds["x"]
                + (x - domains[0][0]) / np.ptp(domains[0]) * bounds["width"],
                canvas["y"]
                + bounds["y"]
                + (1 - (y - domains[1][0]) / np.ptp(domains[1])) * bounds["height"],
            )

        page.keyboard.down("Shift")
        page.mouse.move(*location(-0.6, -0.3))
        page.mouse.down()
        page.mouse.move(*location(-0.2, 0.3), steps=10)
        page.mouse.up()
        page.keyboard.up("Shift")
        page.wait_for_timeout(150)
        selected = page.evaluate("api.getParam('cells').getValue()")
        assert gsc.selection_mask(data, selected).tolist() == [
            False,
            False,
            True,
            False,
        ]
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        assert ">1 cells selected<" in svg
        root = ET.fromstring(svg)
        assert {"A", "B"} <= {e.text for e in root.iter() if e.tag.endswith("text")}
        if marker in ("s", "D"):
            assert not any((e.tag.endswith("circle") for e in root.iter()))
        page.mouse.move(1, 1)
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        for x in (-0.4, 0.4):
            px, py = location(x, 0)
            # Sample the outer black halo, clear of the white gap and foreground.
            # The native brush overlay can lightly tint the selected halo.
            np.testing.assert_allclose(
                pixels[
                    round(py), round(px + 11 * (np.sqrt(2) if marker == "D" else 1))
                ],
                [0] * 3,
                atol=15 if x < 0 else 5,
            )
        foreground = np.array([204, 102, 119])
        expected = np.full(3, 255.0)
        for color, alpha in ((np.zeros(3), 1), (np.full(3, 255), 1), (foreground, 0.7)):
            expected = alpha * color + (1 - alpha) * expected
        px, py = location(0.4, 0)
        np.testing.assert_allclose(pixels[round(py), round(px)], expected, atol=5)
        page.mouse.move(
            canvas["x"] + bounds["x"] + 150, canvas["y"] + bounds["y"] + 150
        )
        page.mouse.wheel(0, -250)
        page.wait_for_timeout(300)
        assert (
            page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()")
            != domains[0]
        )
        output = tmp_path / "outlined-embedding.html"
        chart.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestEmbeddingEdges:
    """Stored edges stay beneath points and follow native coordinate scales."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("outlined", [False, True])
    @pytest.mark.parametrize("width,color", [(0, "navy"), (0.1, "grey"), (1.2, "navy")])
    def test_registered_edges_and_point_order_match_scanpy(
        self, page, tmp_path, outlined, width, color
    ):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import scanpy as sc
        from matplotlib.collections import LineCollection

        data = graph_adata()
        data.obsm["X_umap"] = np.array(
            [
                [-1, -1],
                [1, -1],
                [1, 1],
                [-1, 1],
                [0, 0],
                [0.2, -0.8],
                [0.8, 0.4],
                [-0.8, 0.3],
            ]
        )
        data.obs["score"] = np.arange(8, dtype=float)
        options = dict(
            color="score",
            edges=True,
            edges_width=width,
            edges_color=color,
            add_outline=outlined,
            alpha=0.6,
            size=144,
            marker="o",
            frameon=True,
            title="Stored graph",
            show=False,
        )
        reference = tmp_path / "scanpy.png"
        with plt.rc_context({"figure.figsize": (4, 3), "figure.dpi": 100}):
            ax = sc.pl.umap(data.copy(), **options)
            ax.figure.canvas.draw()
            box = ax.get_window_extent()
            segments = next(
                (c for c in ax.collections if isinstance(c, LineCollection))
            ).get_segments()
            xdomain, ydomain = (ax.get_xlim(), ax.get_ylim())
            ax.figure.savefig(
                reference,
                dpi=150,
                bbox_inches=box.transformed(ax.figure.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            plt.close(ax.figure)
        chart = gsc.pl.umap(data, width=box.width, height=box.height, **options)
        bounds = render(page, chart)
        canvas = page.locator("canvas").bounding_box()
        dpr = page.evaluate("devicePixelRatio")
        full = Image.open(BytesIO(page.screenshot())).convert("RGB")
        left, top = (canvas[axis] + bounds[axis] for axis in ("x", "y"))
        actual = full.crop(
            (
                round(left * dpr),
                round(top * dpr),
                round((left + bounds["width"]) * dpr),
                round((top + bounds["height"]) * dpr),
            )
        )
        oracle = Image.open(reference).convert("RGB")
        assert (
            abs(actual.width - oracle.width) <= 2
            and abs(actual.height - oracle.height) <= 2
        )
        extent = (
            0,
            0,
            min(actual.width, oracle.width),
            min(actual.height, oracle.height),
        )
        actual, oracle = (actual.crop(extent), oracle.crop(extent))
        pixels, target = (
            np.asarray(actual).astype(int),
            np.asarray(oracle).astype(int),
        )
        radius = int(np.ceil(dpr))
        interior = [image[radius:-radius, radius:-radius] for image in (pixels, target)]
        masks = [image.min(axis=2) < 240 for image in interior]
        # Agg and WebGL distribute stroke coverage differently; compare position and total ink.
        for first, second in [(masks[0], masks[1]), (masks[1], masks[0])]:
            distance = distance_transform_cdt(~second, metric="chessboard")
            assert (distance[first] > radius).mean() < 0.01
        ink = [(255 - image).sum() for image in interior]
        assert abs(ink[0] / ink[1] - 1) < 0.1
        for x, y in data.obsm["X_umap"]:
            px = round((x - xdomain[0]) / np.ptp(xdomain) * actual.width)
            py = round((ydomain[1] - y) / np.ptp(ydomain) * actual.height)
            assert (
                np.abs(pixels[py - 1 : py + 2, px - 1 : px + 2] - target[py, px])
                .max(axis=2)
                .min()
                <= 12
            )
        rgb = np.asarray(matplotlib.colors.to_rgb(color)) * 255
        edge_hue = (255 - rgb) / (255 - rgb).max()
        for segment in segments:
            x, y = segment[0] * 0.7 + segment[1] * 0.3
            px = round((x - xdomain[0]) / np.ptp(xdomain) * actual.width)
            py = round((ydomain[1] - y) / np.ptp(ydomain) * actual.height)
            patch = pixels[py - 2 : py + 3, px - 2 : px + 3].reshape(-1, 3)
            # Every interior segment must paint; point-only charts cannot pass this check.
            painted = patch.min() < 250
            assert painted == (width > 0)
            if width:
                darkest = patch[patch.sum(axis=1).argmin()]
                hue = (255 - darkest) / (255 - darkest).max()
                np.testing.assert_allclose(hue, edge_hue, atol=0.03)
        guides = guide_geometry(page)
        assert {"Stored graph", "UMAP1", "UMAP2"} <= {
            item["label"] for item in guides["text"]
        }
        assert len(guides["gradients"]) == 1
        assert abs(guides["gradients"][0]["height"] - bounds["height"]) <= 2
        actual.save(tmp_path / "native-panel.png")
        Image.blend(actual, oracle, 0.5).save(tmp_path / "registered-overlay.png")
        page.screenshot(path=str(tmp_path / "complete.png"))

    def test_empty_graph_renders_only_the_existing_points(self, page):
        data = graph_adata()
        data.obsp["connectivities"] = sparse.csr_matrix((8, 8))
        render(page, gsc.pl.umap(data, color="score", edges=True, show=False))


class TestEmbeddingDensity:
    """Registered density point colors, footprints, guides and observed navigation."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("mode", ["groups", "global", "bounds", "center", "unused"])
    def test_density_panels_match_public_scanpy_background_foreground_and_guides(
        self, page, tmp_path, mode
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        a = make_density(grouped=mode != "global")
        options = {"color_map": "viridis"}
        if mode == "groups":
            options["group"] = ["A", "B"]
        if mode == "unused":
            a.obs["condition"] = a.obs["condition"].cat.add_categories(["unused"])
            options["group"] = ["unused"]
        if mode == "bounds":
            options.update(vmin=0.2, vmax=0.7)
        if mode == "center":
            options.update(vcenter=0.3)
        with plt.rc_context(plt.rcParamsDefault):
            result = sc.pl.embedding_density(
                a.copy(), key="scores", show=False, **options
            )
        axes = result if isinstance(result, list) else [result]
        axes[0].figure.canvas.draw()
        references = []
        for i, ax in enumerate(axes):
            bounds = ax.get_window_extent()
            path = tmp_path / f"reference-{i}.png"
            ax.figure.savefig(
                path,
                dpi=150,
                bbox_inches=bounds.transformed(ax.figure.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            references.append(
                (
                    path,
                    {
                        "coordinates": ax.collections[0].get_offsets().tolist(),
                        "x_domain": ax.get_xlim(),
                        "y_domain": ax.get_ylim(),
                        "labels": [ax.get_xlabel(), ax.get_ylabel()],
                        "title": ax.get_title(),
                        "legend": None,
                    },
                )
            )
        chart = gsc.pl.embedding_density(
            a,
            key="scores",
            width=bounds.width,
            height=bounds.height,
            show=False,
            **options,
        )
        for i, (path, expected) in enumerate(references):
            assert_complete_chart(
                page,
                tmp_path,
                chart,
                expected,
                path,
                f"density-{mode}-{i}",
                panel_index=i,
            )
        plt.close(axes[0].figure)

    def test_default_palette_and_under_over_colors_use_native_point_encodings(
        self, page
    ):
        a = make_density(False)
        chart = gsc.pl.embedding_density(a, vmin=0.2, vmax=0.8, show=False)
        render(page, chart)
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        circles = [e for e in root.iter() if e.tag.endswith("circle")]
        # Vega's yelloworangered endpoints intentionally differ from Matplotlib YlOrRd.
        assert len(circles) == a.n_obs
        assert {"rgb(254, 224, 135)", "rgb(175, 2, 37)"} <= {
            e.get("fill") for e in circles
        }
        for paint in ("lightgray", "black"):
            layer = next((e for e in root.iter() if e.get("fill") == paint))
            assert sum((e.tag.endswith("circle") for e in layer.iter())) == 2

    @pytest.mark.parametrize("group", [["A", "B"], "A"])
    def test_hover_reports_stored_density_and_shared_zoom_including_background_cells(
        self, page, tmp_path, group
    ):
        a = make_density()
        chart = gsc.pl.embedding_density(
            a,
            key="scores",
            group=group,
            obs_id="cell_id",
            zoom=True,
            width=280,
            height=260,
            show=False,
        )
        spec = chart.to_dict()
        bounds = render(page, name_embedding_scales(chart.to_dict(), "umap"))
        encoding = points(units(spec)[0])["encoding"]
        domains = [encoding[axis]["scale"]["domain"] for axis in ("x", "y")]
        for index in (0, 1):
            x, y = a.obsm["X_umap"][index, :2]
            move_to(page, bounds, x, y, *domains, f"id-{index}")
            page.get_by_text("scores (obs['scores'])", exact=True).wait_for(
                state="visible"
            )
            values = [
                s.strip()
                for s in page.locator("table.attributes td").all_text_contents()
            ]
            assert values[:2] == [f"id-{index}", f"cell-{index}"]
            assert float(values[2]) == pytest.approx(a.obs["scores"].iloc[index])
        before = page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()")
        page.mouse.wheel(0, -180)
        page.wait_for_function(
            "b=>{const d=api.getScaleResolutionByName('umap-x-0').getDomain();return d[1]-d[0]<b[1]-b[0]}",
            arg=before,
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()")
            != before
        )
        path = tmp_path / "density.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()
