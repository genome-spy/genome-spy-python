"""Complete native path heatmaps and observed aligned-track navigation."""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import hover_at, pointer, svg_root
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.paga_path_fixture import make_path


def bounds_for(page, name):
    """Read the named native view's bounds, including side tracks."""
    return page.evaluate("name=>api.views.getLayoutBounds({scope:[],view:name})", name)


@pytest.mark.reference
@pytest.mark.parametrize(
    "options",
    [
        {},
        {"n_avg": 3},
        {"n_avg": 2, "normalize_to_zero_one": True},
        {"show_node_names": False, "show_yticks": False, "show_colorbar": False},
        {"annotations": ()},
    ],
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_registered_complete_heatmap_and_tracks(page, tmp_path, options):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_path()
    plt.close("all")
    with mpl.rc_context({"figure.dpi": 100}):
        fig = plt.figure(figsize=(8, 8))
        fig.subplots_adjust(bottom=0.5, top=0.9)
        ax = sc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], show=False, **options)
        fig.canvas.draw()
        axes = [ax] + [v for v in fig.axes if v is not ax and v.images]
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        image = Image.open(reference).convert("RGB")
        boxes = [v.get_window_extent() for v in axes]
        expected = [
            image.crop(
                (
                    round(b.x0 * 1.5),
                    round(image.height - b.y1 * 1.5),
                    round(b.x1 * 1.5),
                    round(image.height - b.y0 * 1.5),
                )
            )
            for b in boxes
        ]
        arrays = [np.asarray(v.images[0].get_array()) for v in axes]
        plt.close(fig)
    chart = gsc.pl.paga_path(
        a,
        ["beta", "alpha"],
        ["g1", "g2"],
        width=boxes[0].width,
        height=boxes[0].height,
        show=False,
        **options,
    )
    spec = chart.to_dict()
    annotation_colors = None
    if options.get("annotations") != ():
        spec["surround"]["bottom"]["views"][1]["encoding"]["color"]["scale"]["name"] = (
            "annotation-greys"
        )
    main = render(page, spec)
    if options.get("annotations") != ():
        # Native Greys fidelity is an accepted limit; retain Scanpy's values and domains.
        values = arrays[-1].ravel()
        native = page.evaluate(
            """values => {
                const scale = api.getScaleResolutionByName('annotation-greys').getScale();
                const rgb = value => scale(value).match(/[\\d.]+/g).map(Number);
                return {domain: scale.domain(), colors: values.map(rgb),
                    endpoints: scale.domain().map(rgb)};
            }""",
            values.tolist(),
        )
        np.testing.assert_allclose(native["domain"], [values.min(), values.max()])
        np.testing.assert_equal(native["endpoints"], [[226] * 3, [30] * 3])
        annotation_colors = np.asarray(native["colors"]).reshape(*arrays[-1].shape, 3)
    bounds = [main, bounds_for(page, "paga-path-groups")]
    if options.get("annotations") != ():
        bounds.append(bounds_for(page, "paga-path-annotation-0"))
    canvas = page.locator("canvas").first.bounding_box()
    for index, (bound, box, target, values) in enumerate(
        zip(bounds, boxes, expected, arrays, strict=True)
    ):
        assert bound["width"] == pytest.approx(box.width, abs=0.5)
        assert bound["height"] == pytest.approx(box.height, abs=0.5)
        if index:
            assert bound["x"] == pytest.approx(main["x"], abs=0.1)
            assert bound["y"] == pytest.approx(
                bounds[index - 1]["y"] + bounds[index - 1]["height"], abs=0.1
            )
        actual = Image.open(
            BytesIO(
                page.screenshot(
                    clip={
                        "x": canvas["x"] + bound["x"],
                        "y": canvas["y"] + bound["y"],
                        "width": bound["width"],
                        "height": bound["height"],
                    }
                )
            )
        ).convert("RGB")
        pixels, reference_pixels = (
            np.asarray(actual).astype(int),
            np.asarray(target).astype(int),
        )
        rows, columns = values.shape
        # Sample away from centered text while checking every tile and original group band.
        for row, column in np.ndindex(rows, columns):
            x, y = (column + 0.25) / columns, (row + 0.25) / rows
            observed = pixels[int(y * actual.height), int(x * actual.width)]
            reference_color = reference_pixels[
                int(y * target.height), int(x * target.width)
            ]
            if index == 2:
                np.testing.assert_allclose(
                    observed, annotation_colors[row, column], atol=3
                )
                if values[row, column] == values.min():
                    np.testing.assert_equal(reference_color, [255] * 3)
                if values[row, column] == values.max():
                    np.testing.assert_equal(reference_color, [0] * 3)
            else:
                np.testing.assert_allclose(observed, reference_color, atol=12)
        Image.blend(actual.resize(target.size), target, 0.5).save(
            tmp_path / f"overlay-{index}.png"
        )
    root = svg_root(page)
    text = {e.text for e in root.iter() if e.tag.endswith("text")}
    if options.get("show_yticks", True):
        assert {"g1", "g2", "cluster"} <= text
    if options.get("show_node_names", True):
        assert {"beta", "alpha"} <= text
    gradients = [e for e in root.iter() if e.tag.endswith("linearGradient")]
    assert len(gradients) == int(options.get("show_colorbar", True)) + int(
        options.get("annotations") != ()
    )
    page.screenshot(path=str(tmp_path / "complete.png"), full_page=True)


@pytest.mark.parametrize("zoom", [True, "xy"])
@pytest.mark.parametrize("hover", [True, False])
def test_native_hover_zoom_values_composition_and_offline_html(
    page, tmp_path, zoom, hover
):
    chart = gsc.pl.paga_path(
        make_path(),
        ["beta", "alpha"],
        ["g1", "g2"],
        hover=hover,
        zoom=zoom,
        show_values=True,
        width=400,
        height=160,
        show=False,
    )
    spec = chart.to_dict()
    for axis in ("x", "y"):
        spec["scales"][axis]["name"] = f"path-{axis}"
    main = render(page, spec)
    before = page.evaluate(
        "['x','y'].map(a=>api.getScaleResolutionByName('path-'+a).getDomain())"
    )
    hover_at(page, main["x"] + main["width"] / 8, main["y"] + main["height"] / 4)
    table = page.locator("table.attributes")
    if hover:
        assert table.is_visible()
        assert table.get_by_text("g1", exact=True).is_visible()
        assert float(table.locator("td").last.inner_text()) == pytest.approx(8)
    else:
        assert not table.is_visible()
    group = bounds_for(page, "paga-path-groups")
    hover_at(page, group["x"] + group["width"] / 8, group["y"] + group["height"] / 4)
    if hover:
        assert table.get_by_text("beta", exact=True).is_visible()
    else:
        assert not table.is_visible()
    pointer(page, main)
    page.mouse.wheel(0, -180)
    page.wait_for_timeout(700)
    zoomed = page.evaluate(
        "['x','y'].map(a=>api.getScaleResolutionByName('path-'+a).getDomain())"
    )
    assert (zoomed[0] != before[0]) is (zoom == "xy")
    assert zoomed[1] != before[1]
    root = svg_root(page)
    assert any(e.tag.endswith("text") and e.text == "8.00" for e in root.iter())
    combined = (
        (chart | chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    composed = render(page, combined)

    def rectangles():
        """Read each native mark's geometry so unchanged panels cannot mimic linked navigation."""
        return [
            [
                (
                    element.get("x"),
                    element.get("y"),
                    element.get("width"),
                    element.get("height"),
                )
                for element in group
            ]
            for group in svg_root(page).iter()
            if group.get("data-mark-type") == "rect" and group.get("clip-path")
        ]

    before_rects = rectangles()
    assert len(before_rects) == 6
    px, py = pointer(page, composed)
    page.mouse.wheel(0, -150)
    page.wait_for_timeout(700)
    zoom_rects = rectangles()
    assert zoom_rects[0] != before_rects[0]
    assert zoom_rects[3:] == before_rects[3:]
    assert (zoom_rects[1] != before_rects[1]) is (zoom == "xy")
    page.mouse.down()
    page.mouse.move(px + 8, py + 8, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    pan_rects = rectangles()
    assert pan_rects[0] != zoom_rects[0]
    assert pan_rects[3:] == before_rects[3:]
    output = tmp_path / "path.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.reference
@pytest.mark.parametrize("guide", [True, False])
def test_constant_values_keep_public_palette_position_with_or_without_guide(
    page, guide
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_path()
    a.raw.X[:] = 7
    try:
        ax = sc.pl.paga_path(
            a,
            ["beta", "alpha"],
            ["g1", "g2"],
            annotations=(),
            show_colorbar=guide,
            show=False,
        )
        expected = np.asarray(ax.images[0].cmap(ax.images[0].norm(7)))[:3] * 255
        chart = gsc.pl.paga_path(
            a,
            ["beta", "alpha"],
            ["g1", "g2"],
            annotations=(),
            show_colorbar=guide,
            show=False,
        )
        main = render(page, chart)
        canvas = page.locator("canvas").first.bounding_box()
        image = Image.open(BytesIO(page.screenshot())).convert("RGB")
        actual = image.getpixel(
            (
                round(canvas["x"] + main["x"] + main["width"] / 4),
                round(canvas["y"] + main["y"] + main["height"] / 4),
            )
        )
        np.testing.assert_allclose(actual, expected, atol=6)
        assert main["width"] == pytest.approx(ax.get_window_extent().width, abs=0.5)
        assert main["height"] == pytest.approx(ax.get_window_extent().height, abs=0.5)
    finally:
        plt.close("all")
