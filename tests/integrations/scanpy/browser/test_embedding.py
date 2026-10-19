"""Observe shared embedding rendering, native navigation, hover and linked selection."""

from io import BytesIO
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.embedding_fixture import (
    embedding_cases,
    make_embedding_adata,
)
from tests.integrations.scanpy.helpers import points

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/embedding.json").read_text()
)["cases"]


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", embedding_cases())
def test_complete_embedding_matches_registered_points_guides_and_axis_labels(
    page, tmp_path, reference_images, case
):
    expected = REFERENCE[case]
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


def assert_complete_chart(page, tmp_path, chart, expected, reference_image, case):
    """Compare registered point footprints, paints and complete native labels to an oracle."""
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
    oracle = Image.open(reference_image).convert("RGB")
    assert (
        abs(actual.width - oracle.width) <= 2
        and abs(actual.height - oracle.height) <= 2
    )
    # Equal coordinate registration and export DPI keep point locations and footprints comparable.
    mask = np.min(np.asarray(actual), axis=2) < 245
    target = np.min(np.asarray(oracle), axis=2) < 245
    for x, y in expected["coordinates"]:
        x0, x1 = expected["x_domain"]
        y0, y1 = expected["y_domain"]
        px, py = (
            round((x - x0) / (x1 - x0) * actual.width),
            round((y1 - y) / (y1 - y0) * actual.height),
        )
        assert (
            mask[py - 3 : py + 4, px - 3 : px + 4].any()
            and target[py - 3 : py + 4, px - 3 : px + 4].any()
        )
        patch = np.asarray(actual)[py - 1 : py + 2, px - 1 : px + 2].astype(int)
        paint = np.asarray(oracle)[py, px].astype(int)
        assert np.abs(patch - paint).max(axis=2).min() <= 12

    # Most raster differences should be confined to antialiased point boundaries.
    extent = (0, 0, min(actual.width, oracle.width), min(actual.height, oracle.height))
    pixels = np.asarray(actual.crop(extent)).astype(int)
    reference = np.asarray(oracle.crop(extent)).astype(int)
    assert (np.abs(pixels - reference).max(axis=2) > 32).mean() < 0.025
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    labels = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
    for label in expected["labels"] + [expected["title"]] + (expected["legend"] or []):
        if label:
            assert label in labels
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    Image.blend(actual.crop(extent), oracle.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("basis", ["tsne", "diffmap", "pca", "draw_graph_fa"])
def test_shared_hover_zoom_and_offline_delivery(page, tmp_path, basis):
    a = make_embedding_adata()
    chart = gsc.pl.embedding(
        a,
        basis,
        color="score",
        obs_id="cell_id",
        size=100,
        zoom=True,
        frameon=True,
        show=False,
    )
    spec = chart.to_dict()
    mark = points(spec)
    bounds = render(page, chart)
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


def test_pca_brush_count_and_python_membership_agree(page):
    a = make_embedding_adata()
    brush = gs.selection_interval("cells", encodings=["x", "y"])
    chart = gsc.pl.pca(a, color=["cell_type", "score"], selection=brush, show=False)
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    x, y = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    page.mouse.move(x + bounds["width"] * 0.15, y + bounds["height"] * 0.2)
    page.mouse.down()
    page.mouse.move(x + bounds["width"] * 0.65, y + bounds["height"] * 0.7, steps=12)
    page.mouse.up()
    snapshot = page.evaluate("api.getParam('cells').getValue()")
    mask = gsc.selection_mask(a, snapshot, basis="pca")
    assert 0 < mask.sum() < a.n_obs
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert f"{mask.sum()} cells selected" in svg
