"""Qc behavior and regressions."""

import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import move_to
from tests.integrations.scanpy.browser.rendering import assert_complete_chart, render
from tests.integrations.scanpy.helpers import leaf_marks, units
from tests.integrations.scanpy.qc_fixtures import (
    make_counts,
    make_hvg_result,
    make_scrublet,
)


class TestHighestExpr:
    """Observe native box geometry, whole charts, hover, zoom and offline delivery."""

    @pytest.mark.reference
    @pytest.mark.parametrize("log", [False, True])
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_boxes_match_scanpy_quartiles_whiskers_axes_and_pixels(
        self, page, tmp_path, log
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        a = make_counts()
        with (
            plt.rc_context(plt.rcParamsDefault),
            pytest.warns(UserWarning, match="zero counts"),
        ):
            ax = sc.pl.highest_expr_genes(a, n_top=5, log=log, show=False)
        ax.figure.canvas.draw()
        bounds = ax.get_window_extent()
        reference = tmp_path / "reference.png"
        ax.figure.savefig(
            reference,
            dpi=150,
            bbox_inches=bounds.transformed(ax.figure.dpi_scale_trans.inverted()),
            pad_inches=0,
        )
        vertices = [p.get_path().vertices for p in ax.patches]
        labels = [t.get_text() for t in ax.get_yticklabels()]
        with pytest.warns(UserWarning, match="zero counts"):
            chart = gsc.pl.highest_expr_genes(
                a,
                n_top=5,
                log=log,
                width=bounds.width,
                height=bounds.height,
                show=False,
            )
        actual_bounds = render(page, chart)
        svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        text = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert "% of total counts" in text and all(
            (text.count(label) == 1 for label in labels)
        )
        (tmp_path / "native.svg").write_text(svg)
        boxes = [
            e
            for group in root.iter()
            if group.get("data-mark-type") == "rect"
            for e in group
        ]
        # Every quartile rectangle must retain the reference width and row position.
        assert len(boxes) == 5
        assert [e.get("fill") for e in boxes] == [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
        ]
        for row, (element, expected) in enumerate(zip(boxes, vertices, strict=True)):
            x1, x2 = (expected[:, 0].min(), expected[:, 0].max())
            lo, hi = ax.get_xlim()
            if log:
                x1, x2, lo, hi = np.log10([x1, x2, lo, hi])
            np.testing.assert_allclose(
                [float(element.get("x")), float(element.get("width"))],
                [
                    actual_bounds["x"] + (x1 - lo) / (hi - lo) * actual_bounds["width"],
                    max(0.5, (x2 - x1) / (hi - lo) * actual_bounds["width"]),
                ],
                atol=0.3,
            )
            np.testing.assert_allclose(
                [float(element.get("y")), float(element.get("height"))],
                [
                    actual_bounds["y"] + (row + 0.1) * actual_bounds["height"] / 5,
                    0.8 * actual_bounds["height"] / 5,
                ],
                atol=0.3,
            )
        canvas = page.locator("canvas").first.bounding_box()
        crop = page.screenshot(
            clip={
                "x": canvas["x"] + actual_bounds["x"],
                "y": canvas["y"] + actual_bounds["y"],
                "width": actual_bounds["width"],
                "height": actual_bounds["height"],
            }
        )
        actual = Image.open(BytesIO(crop)).convert("RGB")
        actual.save(tmp_path / "native.png")
        expected = Image.open(reference).convert("RGB").resize(actual.size)
        Image.blend(expected, actual, 0.5).save(tmp_path / "registered-overlay.png")
        page.screenshot(path=str(tmp_path / "complete-chart.png"))
        difference = np.abs(
            np.asarray(actual).astype(float) - np.asarray(expected).astype(float)
        )
        # Independent browser rasterization may differ along thin strokes, not box interiors.
        assert difference.mean() < 10
        assert (difference.max(axis=2) > 80).mean() < 0.06
        plt.close(ax.figure)

    def test_box_and_outlier_hover_zoom_and_offline_html(self, page, tmp_path):
        with pytest.warns(UserWarning, match="zero counts"):
            chart = gsc.pl.highest_expr_genes(
                make_counts(), n_top=5, zoom=True, width=400, height=300, show=False
            )
        bounds = render(page, chart)
        domain = chart.to_dict()["layer"][0]["encoding"]["x"]["scale"]["domain"]
        move_to(page, bounds, 2, 4.5, domain, [5, 0], "gene-0")
        page.get_by_text("Median (%)", exact=True).wait_for(state="visible")
        assert [
            t.strip() for t in page.locator("table.attributes td").all_text_contents()
        ][:2] == ["gene-0", "gene-0"]
        move_to(page, bounds, 0, 0.5, domain, [5, 0], "0")
        page.get_by_text("Cell ID", exact=True).wait_for(state="visible")
        assert [
            t.strip() for t in page.locator("table.attributes td").all_text_contents()
        ] == ["gene-4", "0", "0", "0.000"]
        before = page.evaluate(
            "api.getScaleResolutionByName('highest-expression-x').getDomain()"
        )
        page.mouse.wheel(0, -180)
        page.wait_for_function(
            "before=>{const d=api.getScaleResolutionByName('highest-expression-x').getDomain();return d[1]-d[0]<before[1]-before[0];}",
            arg=before,
        )
        path = tmp_path / "highest.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestHvg:
    """Observe complete QC panels, shared native legends, hover, navigation and HTML."""

    @pytest.mark.reference
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    @pytest.mark.parametrize("flavor", ["seurat", "seurat_v3"])
    @pytest.mark.parametrize("log", [False, True])
    def test_both_qc_panels_match_registered_scanpy_points_axes_and_legends(
        self, page, tmp_path, flavor, log
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        data = make_hvg_result(flavor=flavor)
        references = []
        with plt.rc_context({"figure.dpi": 100}):
            sc.pl.highly_variable_genes(data, log=log, show=False)
            figure = plt.gcf()
            # Register Scanpy's positions using the deliberately reviewed native paint.
            for index, ax in enumerate(figure.axes):
                for artist, color in zip(
                    ax.collections, ["#2563a6", "#cbd5e1"], strict=True
                ):
                    artist.set_facecolor(color)
                    artist.set_sizes([9 / (100 / 72) ** 2])
                    artist.set_linewidths([0])
                ax.set_xlabel("Mean expression")
                ax.set_ylabel(
                    ("Normalized " if index == 0 else "")
                    + ("variance" if flavor == "seurat_v3" else "dispersion")
                )
            legend = [
                text.get_text() for text in figure.axes[0].get_legend().get_texts()
            ]
            # Native guides are collected below the pair rather than over its points.
            figure.axes[0].get_legend().set_visible(False)
            figure.canvas.draw()
            for index, ax in enumerate(figure.axes):
                box = ax.get_window_extent()
                image = tmp_path / f"reference-{index}.png"
                figure.savefig(
                    image,
                    dpi=150,
                    bbox_inches=box.transformed(figure.dpi_scale_trans.inverted()),
                    pad_inches=0,
                )
                references.append(
                    (
                        image,
                        {
                            "coordinates": np.concatenate(
                                [c.get_offsets() for c in ax.collections]
                            ).tolist(),
                            "x_domain": ax.get_xlim(),
                            "y_domain": ax.get_ylim(),
                            "log": log,
                            "labels": [ax.get_xlabel(), ax.get_ylabel()],
                            "title": None,
                            "legend": legend,
                            "width": box.width,
                            "height": box.height,
                        },
                    )
                )
            plt.close(figure)
        chart = gsc.pl.highly_variable_genes(
            data,
            log=log,
            width=references[0][1]["width"],
            height=references[0][1]["height"],
            show=False,
        )
        for index, (image, expected) in enumerate(references):
            assert_complete_chart(
                page,
                tmp_path,
                chart,
                expected,
                image,
                f"hvg-{index}",
                panel_index=index,
            )
        svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        labels = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert all((labels.count(label) == 1 for label in legend))
        fills = page.evaluate(
            "svg => {\n        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;\n        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';\n        document.body.append(root);\n        const colors = [...root.querySelectorAll('circle')]\n            .filter(n => +n.getAttribute('r') > 2).map(n => getComputedStyle(n).fill);\n        root.remove();\n        return colors;\n    }",
            svg,
        )
        assert fills == ["rgb(37, 99, 166)", "rgb(203, 213, 225)"]
        assert len([e for e in root.iter() if e.tag.endswith("circle")]) == 2 * len(
            data
        ) + len(legend)

    @pytest.mark.parametrize("log", [False, True])
    def test_hover_zoom_and_offline_delivery(self, page, tmp_path, log):
        chart = gsc.pl.highly_variable_genes(
            make_hvg_result(), log=log, zoom=True, show=False
        )
        spec = chart.to_dict()
        encoding = units(spec)[0]["encoding"]
        for index, panel in enumerate(units(spec)):
            for axis in ("x", "y"):
                panel["encoding"][axis]["scale"]["name"] = f"hvg-{axis}-{index}"
        bounds = render(page, spec)
        domains = [encoding[axis]["scale"]["domain"] for axis in ("x", "y")]
        coordinates = [2, 1.3]
        if log:
            domains = [np.log10(d).tolist() for d in domains]
            coordinates = np.log10(coordinates).tolist()
        move_to(page, bounds, *coordinates, *domains, "gene-4")
        page.get_by_text("Selection", exact=True).wait_for(state="visible")
        assert [
            value.strip()
            for value in page.locator("table.attributes td").all_text_contents()
        ] == ["gene-4", "gene-4", "highly variable genes", "2.000", "1.300"]
        names = ["hvg-x-0", "hvg-y-0", "hvg-x-1", "hvg-y-1"]
        before = page.evaluate(
            "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())", names
        )
        page.mouse.wheel(0, -220)
        page.wait_for_function(
            "({names,before})=>names.slice(0,2).every((n,i)=>{const d=api.getScaleResolutionByName(n).getDomain();return d[1]-d[0]<before[i][1]-before[i][0];})",
            arg={"names": names, "before": before},
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('hvg-x-1').getDomain()")
            == before[2]
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('hvg-y-1').getDomain()")
            == before[3]
        )
        path = tmp_path / "hvg.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()


class TestScrublet:
    """Observe registered native histograms, thresholds, hover, zoom and HTML delivery."""

    @pytest.mark.reference
    @pytest.mark.parametrize("batched", [False, True])
    @pytest.mark.parametrize("scales", [("log", "linear"), ("linear", "log")])
    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_histograms_match_public_scanpy_bars_axes_and_thresholds(
        self, page, tmp_path, batched, scales
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        a = make_scrublet(batched)
        with plt.rc_context(plt.rcParamsDefault):
            axes = np.asarray(
                sc.pl.scrublet_score_distribution(
                    a, scale_hist_obs=scales[0], scale_hist_sim=scales[1], show=False
                )
            ).ravel()
        axes[0].figure.canvas.draw()
        bounds = axes[0].get_window_extent()
        chart = gsc.pl.scrublet_score_distribution(
            a,
            scale_hist_obs=scales[0],
            scale_hist_sim=scales[1],
            width=bounds.width,
            height=bounds.height,
            show=False,
        )
        render(page, chart)
        svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
        root = ET.fromstring(svg)
        texts = [e.text for e in root.iter() if e.tag.endswith("text")]
        assert texts.count("Doublet score") == len(axes) and texts.count(
            "Prob. density"
        ) == len(axes)
        assert all((ax.get_title() in texts for ax in axes))
        (tmp_path / "native.svg").write_text(svg)
        panels = units(chart.to_dict())
        groups = [g for g in root.iter() if g.get("data-mark-type") == "rect"]
        rectangles = [list(g) for g in groups]
        clips = {
            e.get("id"): list(e)[0].attrib
            for e in root.iter()
            if e.tag.endswith("clipPath")
        }
        assert len(rectangles) == len(axes)
        canvas = page.locator("canvas").first.bounding_box()
        for i, (ax, panel) in enumerate(zip(axes, panels, strict=True)):
            clip_id = groups[i].get("clip-path").removeprefix("url(#").removesuffix(")")
            native = {key: float(value) for key, value in clips[clip_id].items()}
            np.testing.assert_allclose(
                page.evaluate(
                    "i=>api.getScaleResolutionByName('scrublet-y-'+i).getDomain()", i
                ),
                ax.get_ylim(),
            )
            positive = [p for p in ax.patches if p.get_height() > 0]
            assert len(rectangles[i]) == len(positive)
            for rectangle, patch in zip(rectangles[i], positive, strict=True):
                low, high = ax.get_ylim()
                top = patch.get_height()
                if ax.get_yscale() == "log":
                    low, high, top = np.log10([low, high, top])
                x0, x1 = ax.get_xlim()
                expected_box = [
                    native["x"] + (patch.get_x() - x0) / (x1 - x0) * native["width"],
                    native["y"] + (high - top) / (high - low) * native["height"],
                    patch.get_width() / (x1 - x0) * native["width"],
                    (top - low) / (high - low) * native["height"],
                ]
                actual_box = [
                    float(rectangle.get(key)) for key in ("x", "y", "width", "height")
                ]
                assert np.isfinite(actual_box).all()
                np.testing.assert_allclose(actual_box, expected_box, atol=0.3)
            reference = tmp_path / f"reference-{i}.png"
            ax.figure.savefig(
                reference,
                dpi=150,
                bbox_inches=ax.get_window_extent().transformed(
                    ax.figure.dpi_scale_trans.inverted()
                ),
                pad_inches=0,
            )
            crop = page.screenshot(
                clip={
                    "x": canvas["x"] + native["x"],
                    "y": canvas["y"] + native["y"],
                    "width": native["width"],
                    "height": native["height"],
                }
            )
            actual = Image.open(BytesIO(crop)).convert("RGB")
            actual.save(tmp_path / f"native-{i}.png")
            expected = Image.open(reference).convert("RGB").resize(actual.size)
            Image.blend(expected, actual, 0.5).save(tmp_path / f"overlay-{i}.png")
            difference = np.abs(
                np.asarray(actual).astype(float) - np.asarray(expected).astype(float)
            )
            # Fractional bin edges change gray pixels; exact bar geometry is checked above.
            assert difference.mean() < 12
            assert (difference.max(axis=2) > 80).mean() < 0.045
            # Register the threshold against its score coordinate and the full panel height.
            if ax.lines:
                threshold = ax.lines[0].get_xdata()[0]
                low, high = leaf_marks(panel)[0]["encoding"]["x"]["scale"]["domain"]
                x = native["x"] + (threshold - low) / (high - low) * native["width"]
                assert any(
                    (
                        abs(float(e.get("x1", "-100")) - x) < 0.3
                        and abs(float(e.get("x2", "-100")) - x) < 0.3
                        and (
                            abs(
                                abs(float(e.get("y2", "0")) - float(e.get("y1", "0")))
                                - native["height"]
                            )
                            < 0.3
                        )
                        for e in root.iter()
                        if e.tag.endswith("line")
                    )
                )
        page.screenshot(path=str(tmp_path / "complete-chart.png"))
        plt.close(axes[0].figure)

    def test_native_bin_hover_independent_zoom_and_offline_html(self, page, tmp_path):
        chart = gsc.pl.scrublet_score_distribution(
            make_scrublet(), zoom=True, width=320, height=220, show=False
        )
        panel = units(chart.to_dict())[0]
        encoding = leaf_marks(panel)[0]["encoding"]
        xdomain = encoding["x"]["scale"]["domain"]
        ydomain = encoding["y"]["scale"]["domain"]
        bounds = render(page, chart)
        y = (ydomain[0] * 4.9) ** 0.5
        move_to(
            page,
            bounds,
            1 / 98,
            float(np.log10(y)),
            xdomain,
            np.log10(ydomain).tolist(),
            "Observed transcriptomes",
        )
        page.get_by_text("Probability density", exact=True).wait_for(state="visible")
        assert [
            t.strip() for t in page.locator("table.attributes td").all_text_contents()
        ] == ["All cells", "Observed transcriptomes", "0.000", "0.02041", "1", "4.900"]
        names = ["scrublet-x-0", "scrublet-x-1"]
        before = page.evaluate(
            "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())", names
        )
        page.mouse.wheel(0, -200)
        page.wait_for_function(
            "before=>{const d=api.getScaleResolutionByName('scrublet-x-0').getDomain();return d[1]-d[0]<before[0][1]-before[0][0]}",
            arg=before,
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('scrublet-x-1').getDomain()")
            == before[1]
        )
        path = tmp_path / "scrublet.html"
        chart.save(path, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(path.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert not page.locator(".message-box").count()

    @pytest.mark.smoke
    def test_threshold_slider_updates_pair_colors_and_rule_with_independent_batches(
        self, page, tmp_path
    ):
        from genome_spy.integrations.scanpy._qc.scrublet_data import prepare_scrublet
        from tests.integrations.scanpy.browser.interactions import svg_root

        a = make_scrublet(True)
        table, _ = prepare_scrublet(a)
        chart = gsc.pl.scrublet_score_distribution(a, threshold_slider=True, show=False)
        render(page, chart)
        sliders = page.locator('input[type="range"]')
        assert sliders.count() == 2
        before = svg_root(page)
        assert (
            sum((e.text == "Bins" for e in before.iter() if e.tag.endswith("text")))
            == 2
        )

        def rectangles(root):
            """Read histogram bins, excluding legend and frame rectangles."""
            return [
                list(g)
                for g in root.iter()
                if g.get("data-mark-type") == "rect" and g.get("clip-path")
            ]

        original = rectangles(before)
        for proposed in [0.15, 0.7]:
            sliders.nth(0).evaluate(
                "(el, value) => {el.value=value; el.dispatchEvent(new Event('input', {bubbles:true}));}",
                proposed,
            )
            cutoff = float(sliders.nth(0).input_value())
            page.wait_for_timeout(100)
            root = svg_root(page)
            bars = rectangles(root)
            assert len(bars) == 4
            assert [[r.attrib for r in b] for b in bars[2:]] == [
                [r.attrib for r in b] for b in original[2:]
            ]
            for index in [0, 1]:
                rows = table[(table.panel == index) & (table.density > 0)]
                expected = [
                    "#cbd5e1"
                    if r.end <= cutoff
                    else "#2563a6"
                    if r.start > cutoff
                    else "#94a3b8"
                    for r in rows.itertuples()
                ]
                assert [r.get("fill") for r in bars[index]] == expected
                for actual, saved in zip(bars[index], original[index], strict=True):
                    assert all(
                        (
                            actual.get(k) == saved.get(k)
                            for k in ["x", "y", "width", "height"]
                        )
                    )
                domain = leaf_marks(units(chart.to_dict())[index])[0]["encoding"]["x"][
                    "scale"
                ]["domain"]
                groups = [
                    g
                    for g in root.iter()
                    if g.get("data-mark-type") == "rect" and g.get("clip-path")
                ]
                clip_id = (
                    groups[index]
                    .get("clip-path")
                    .removeprefix("url(#")
                    .removesuffix(")")
                )
                bounds = {
                    k: float(v)
                    for e in root.iter()
                    if e.get("id") == clip_id
                    for k, v in e[0].attrib.items()
                }
                expected_x = (
                    bounds["x"]
                    + (cutoff - domain[0]) / np.ptp(domain) * bounds["width"]
                )
                rules = [
                    e
                    for g in root.iter()
                    if g.get("data-mark-type") == "rule" and g.get("clip-path")
                    for e in g
                ]
                assert any(
                    (abs(float(r.get("x1")) - expected_x) < 0.3 for r in rules)
                ), (cutoff, expected_x, [r.attrib for r in rules])
        assert a.uns["scrublet"]["batches"]["B"]["threshold"] == 0.27
        row = table[(table.panel == 0) & (table.start < 0.8) & (table.end > 0.8)].iloc[
            0
        ]
        encoding = leaf_marks(units(chart.to_dict())[0])[0]["encoding"]
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        ydomain = encoding["y"]["scale"]["domain"]
        move_to(
            page,
            bounds,
            float((row.start + row.end) / 2),
            float(np.log10((ydomain[0] * row.density) ** 0.5)),
            encoding["x"]["scale"]["domain"],
            np.log10(ydomain).tolist(),
            "Above cutoff",
        )
        page.get_by_text("Preview cutoff", exact=True).wait_for(state="visible")
        output = tmp_path / "scrublet-slider.html"
        chart.save(output, inline=True, controls=False)
        page.context.set_offline(True)
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert page.locator('input[type="range"]').count() == 2
