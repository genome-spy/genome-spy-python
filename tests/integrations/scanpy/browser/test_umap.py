"""Observed Scanpy UMAP hover, navigation, offline delivery and render fidelity."""

from io import BytesIO
import json
from pathlib import Path
import warnings

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy._embed import bundled_module_url
from tests.integrations.scanpy.fixture_data import make_adata, reference_cases
from tests.integrations.scanpy.helpers import points, units

sc = pytest.importorskip("scanpy")
mpl = pytest.importorskip("matplotlib")
Image = pytest.importorskip("PIL.Image")
REFERENCE_DIR = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((REFERENCE_DIR / "umap.json").read_text())


def fixture():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_adata()


def render(page, chart, *, renderer="webgl"):
    spec = chart.to_dict()
    for i, panel in enumerate(units(spec)):
        panel["name"] = f"panel-{i}"
    page.set_content(
        '<style>body{margin:0;background:white}</style><div id="chart"></div>'
    )
    page.evaluate(
        """async ({url,spec,renderer}) => {
        const {embed} = await import(url);
        window.api = await Promise.race([
            embed(document.querySelector('#chart'),spec,{renderer}),
            new Promise((_,reject)=>setTimeout(()=>reject(Error('Embed timeout')),20000)),
        ]);
        await new Promise(requestAnimationFrame);
        await new Promise(requestAnimationFrame);
    }""",
        {"url": bundled_module_url("embed"), "spec": spec, "renderer": renderer},
    )
    page.locator("canvas").first.wait_for(state="visible")
    page.wait_for_function("""() => Math.abs(
        document.querySelector('canvas').getBoundingClientRect().width
        - api.getLogicalCanvasSize().width) < 0.1""")
    assert page.locator(".message-box").count() == 0, page.locator(
        ".message-box"
    ).all_text_contents()
    return page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")


def move_to(page, bounds, x, y, x_domain, y_domain, expected_id):
    canvas = page.locator("canvas").first.bounding_box()
    px = (
        canvas["x"]
        + bounds["x"]
        + bounds["width"] * (x - x_domain[0]) / (x_domain[1] - x_domain[0])
    )
    py = (
        canvas["y"]
        + bounds["y"]
        + bounds["height"] * (1 - (y - y_domain[0]) / (y_domain[1] - y_domain[0]))
    )
    page.mouse.move(px - 2, py - 2)
    # Native tooltips suppress flashes for 70 ms on entry and 400 ms after a
    # large jump. Model a pointer pause before the final short movement.
    page.wait_for_timeout(450)
    # Probe only the one-pixel picking neighborhood, as in the resource benchmark.
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        page.mouse.move(px + dx, py + dy)
        page.wait_for_timeout(80)
        if page.get_by_text(expected_id, exact=True).is_visible():
            break
    return px, py


@pytest.mark.parametrize("color", ["cell_type", "score"])
def test_hover_reports_known_zero_nonzero_and_missing_observations(page, color):
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


@pytest.mark.parametrize("case", ["categorical", "continuous", "grid"])
def test_complete_chart_has_original_guides_labels_and_unclipped_layout(
    page, tmp_path, case
):
    with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
        chart = gsc.pl.umap(
            fixture(), **reference_cases()[case], size=np.arange(8) * 7 + 25, show=False
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


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize(
    "marker,token,linewidth",
    [(".", "dot", 0), ("o", "circle", 0), (".", "dot-stroke", 2)],
)
def test_rendered_marker_footprint_matches_registered_scanpy_export(
    page, tmp_path, reference_images, marker, token, linewidth
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
    canvas = page.locator("canvas").first.bounding_box()
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": canvas["x"] + bounds["x"],
                    "y": canvas["y"] + bounds["y"],
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    reference = Image.open(reference_images("umap") / f"footprint-{token}.png").convert(
        "RGB"
    )

    def footprint(image):
        pixels = np.asarray(image)
        yy, xx = np.where(pixels.max(axis=2) < 128)
        assert len(xx) > 20
        return np.array([xx.max() - xx.min() + 1, yy.max() - yy.min() + 1])

    expected = REFERENCE[f"footprint_{token}"]["diameter_at_export"]
    np.testing.assert_allclose(footprint(actual), footprint(reference), atol=2)
    np.testing.assert_allclose(footprint(actual), [expected, expected], atol=2)
    # A fourfold size mistake doubles the diameter and cannot pass this oracle.
    assert np.all(np.abs(footprint(actual) * 2 - footprint(reference)) > 2)
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


def test_wheel_navigation_changes_coordinates_and_offline_html_needs_no_network(
    page, tmp_path
):
    with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
        chart = gsc.pl.umap(
            fixture(), color="score", size=100, zoom=True, frameon=False, show=False
        )
    bounds = render(page, chart)
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
        """before => ['umap-x-0', 'umap-y-1'].every((name, i) => {
            const domain = api.getScaleResolutionByName(name).getDomain();
            return domain[1] - domain[0] < before[i][1] - before[i][0];
        })""",
        arg=domains,
    )
    assert page.locator("canvas").first.screenshot() != before
    page.evaluate("api.getScaleResolutionByName('umap-x-0').resetZoom()")
    page.evaluate("api.getScaleResolutionByName('umap-y-1').resetZoom()")
    page.wait_for_function(
        "() => Math.abs(api.getScaleResolutionByName('umap-x-0').getDomain()[0] + 2.2) < 1e-6"
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


@pytest.mark.parametrize("color", ["cell_type", "score"])
def test_overlapping_points_hover_the_last_visible_observation(page, color):
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


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", ["categorical", "continuous", "grid"])
def test_registered_plot_areas_match_reference_positions_colors_and_footprints(
    page, tmp_path, reference_images, case
):
    from scipy.ndimage import distance_transform_edt

    page.set_viewport_size({"width": 2800, "height": 1800})
    width, height = REFERENCE["cases"][case]["panels"][0]["plot_size"]
    chart = gsc.pl.umap(
        fixture(),
        **reference_cases()[case],
        size=np.arange(8) * 7 + 25,
        width=width,
        height=height,
        show=False,
    )
    render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    for i, panel in enumerate(REFERENCE["cases"][case]["panels"]):
        bounds = page.evaluate(
            "i=>api.views.getLayoutBounds({scope:[],view:`panel-${i}`})", i
        )
        np.testing.assert_allclose(
            [bounds["width"], bounds["height"]],
            np.array(panel["plot_size"]),
            # Native layout rounds panel edges to backing pixels.
            atol=1,
        )
        actual = Image.open(
            BytesIO(
                page.screenshot(
                    clip={
                        "x": canvas["x"] + bounds["x"],
                        "y": canvas["y"] + bounds["y"],
                        "width": bounds["width"],
                        "height": bounds["height"],
                    }
                )
            )
        ).convert("RGB")
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

        native_ink, reference_ink = colored(native), colored(reference)
        assert native_ink.sum() > 30 and reference_ink.sum() > 30
        # Layout rounds logical edges before DPR conversion; include only the
        # measured rounding displacement, without fitting or shifting images.
        rounding = 1.5 * np.max(
            np.abs(np.array([bounds["width"], bounds["height"]]) - panel["plot_size"])
        )
        assert rounding <= 1.5
        assert (
            distance_transform_edt(~reference_ink)[native_ink].max() <= 2.5 + rounding
        )
        assert (
            distance_transform_edt(~native_ink)[reference_ink].max() <= 2.5 + rounding
        )
        # Compare actual interior paint at each non-overlapping observation.
        # Antialiased intersections can blend two valid colors differently in
        # Agg/WebGL, so they are covered by geometry and draw-order checks.
        for source_index, (x, y), paint in zip(
            panel["order"], panel["coordinates"], panel["colors"], strict=True
        ):
            if source_index in (0, 2):
                continue
            xd, yd = panel["x_domain"], panel["y_domain"]
            px = round((x - xd[0]) / (xd[1] - xd[0]) * bounds["width"] * 1.5)
            py = round((1 - (y - yd[0]) / (yd[1] - yd[0])) * bounds["height"] * 1.5)
            expected_color = np.array([int(paint[j : j + 2], 16) for j in (1, 3, 5)])
            region = native[max(0, py - 1) : py + 2, max(0, px - 1) : px + 2]
            assert np.abs(region - expected_color).max(axis=2).min() <= 12
        actual.save(tmp_path / f"{case}-native-panel-{i}.png")
        Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
            tmp_path / f"{case}-registered-overlay-{i}.png"
        )


def test_zero_size_points_leave_no_visible_footprint(page):
    a = fixture()[:1].copy()
    chart = gsc.pl.umap(
        a, size=0, frameon=False, na_color="black", hover=False, show=False
    )
    render(page, chart)
    pixels = np.asarray(
        Image.open(BytesIO(page.locator("canvas").first.screenshot())).convert("RGB")
    )
    assert pixels.min() == 255


@pytest.mark.parametrize(
    "colorbar,expected", [(None, [68, 1, 84]), ("right", [33, 145, 140])]
)
def test_constant_expression_preserves_scanpy_colorbar_normalization(
    page, colorbar, expected
):
    a = fixture()[:1].copy()
    a.obs["score"] = 5.0
    bounds = render(
        page,
        gsc.pl.umap(
            a, color="score", colorbar_loc=colorbar, size=144, frameon=False, show=False
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


def test_native_sized_panels_and_numeric_guide_fit_side_by_side(page, tmp_path):
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
    render(page, chart)
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
