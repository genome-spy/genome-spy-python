"""Observe shared embedding rendering, native navigation, hover and linked selection."""

import json
from pathlib import Path

import numpy as np
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import move_to
from tests.integrations.scanpy.browser.rendering import assert_complete_chart, render
from tests.integrations.scanpy.embedding_fixture import (
    embedding_cases,
    make_embedding_adata,
)
from tests.integrations.scanpy.fixture_support import graph_adata
from tests.integrations.scanpy.helpers import name_embedding_scales, points

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/embedding.json").read_text()
)["cases"]


@pytest.mark.reference
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


@pytest.mark.parametrize("basis", ["tsne", "diffmap", "pca", "draw_graph_fa"])
@pytest.mark.parametrize("location", ["left", "top"])
def test_shared_hover_zoom_and_offline_delivery(page, tmp_path, basis, location):
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


def test_pca_brush_count_and_python_membership_agree(page):
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
