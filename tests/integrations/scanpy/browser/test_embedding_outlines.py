"""Registered outline footprints and draw order in native WebGL rendering."""

from io import BytesIO
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import pytest
from PIL import Image
from anndata import AnnData
from scipy.ndimage import maximum_filter, minimum_filter

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import name_embedding_scales
from tests.integrations.scanpy.browser.test_umap import render


def _pixel_error(pixels, target, radius):
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


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("marker", [".", "o", "s", "D"])
@pytest.mark.parametrize("overlap", [False, True])
@pytest.mark.parametrize("preset", ["default", "custom", "edge"])
def test_outlined_points_match_registered_scanpy_paint(
    page, tmp_path, marker, overlap, preset
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
        obsm={"X_umap": np.array([[-1, -1], [1, 1], [-distance, 0], [distance, 0]])},
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
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
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
    pixels, target = np.asarray(actual).astype(int), np.asarray(reference).astype(int)
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
        assert (_pixel_error(first, second, radius)[interior] > 32).mean() < 0.05


@pytest.mark.parametrize("marker", ["o", "s", "D"])
def test_outline_hover_linked_brush_navigation_and_offline_delivery(
    page, tmp_path, marker
):
    import genome_spy as gs
    from tests.integrations.scanpy.browser.test_umap import move_to

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
        page.evaluate(f"api.getScaleResolutionByName('umap-{axis}-{i}').getDomain()")
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
    assert gsc.selection_mask(data, selected).tolist() == [False, False, True, False]
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert ">1 cells selected<" in svg
    root = ET.fromstring(svg)
    assert {"A", "B"} <= {e.text for e in root.iter() if e.tag.endswith("text")}
    if marker in ("s", "D"):
        assert not any(e.tag.endswith("circle") for e in root.iter())
    page.mouse.move(1, 1)
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    for x in (-0.4, 0.4):
        px, py = location(x, 0)
        # Sample the outer black halo, clear of the white gap and foreground.
        # The native brush overlay can lightly tint the selected halo.
        np.testing.assert_allclose(
            pixels[round(py), round(px + 11 * (np.sqrt(2) if marker == "D" else 1))],
            [0] * 3,
            atol=15 if x < 0 else 5,
        )
    foreground = np.array([204, 102, 119])
    expected = np.full(3, 255.0)
    for color, alpha in (
        (np.zeros(3), 1),
        (np.full(3, 255), 1),
        (foreground, 0.7),
    ):
        expected = alpha * color + (1 - alpha) * expected
    px, py = location(0.4, 0)
    np.testing.assert_allclose(pixels[round(py), round(px)], expected, atol=5)
    page.mouse.move(canvas["x"] + bounds["x"] + 150, canvas["y"] + bounds["y"] + 150)
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
