"""Registered heatmap tiles, complete annotations, unequal trees and cell hover."""

from io import BytesIO
import json
from pathlib import Path
import warnings

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata, heatmap_cases

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "heatmap.json").read_text())


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", heatmap_cases())
def test_complete_registered_heatmaps(page, tmp_path, case):
    reference = REFERENCE["cases"][case]
    options = heatmap_cases()[case].copy()
    names = options.pop("var_names", ["g1", "g2", "g3"])
    groupby = options.pop("groupby", "group")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.heatmap(
            make_heatmap_adata(case),
            names,
            groupby,
            width=reference["plot_size"][0],
            height=reference["plot_size"][1],
            show=False,
            **options,
        )
    bounds = render(page, chart)
    canvas = page.locator("canvas").first.bounding_box()
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    for text in set(
        reference["x_labels"] + reference["y_labels"] + reference["group_labels"]
    ):
        if text:
            assert f">{text}<" in svg, (case, text)
    left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": left,
                    "y": top,
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    expected = Image.open(FIXTURES / f"heatmap-{case}-panel.png").convert("RGB")
    values = np.array(reference["values"], dtype=float)
    for row, column in np.ndindex(values.shape):
        # Sample inside each tile, clear of group borders and palette boundaries.
        x, y = (column + 0.25) / values.shape[1], (row + 0.25) / values.shape[0]
        np.testing.assert_allclose(
            np.asarray(actual)[int(y * actual.height), int(x * actual.width)].astype(
                int
            ),
            np.asarray(expected)[
                int(y * expected.height), int(x * expected.width)
            ].astype(int),
            atol=12,
            err_msg=case,
        )
    # Register upstream branch coordinates directly, without fitting the image.
    swapped = options.get("swap_axes", False)
    paths = reference["tree_paths"]
    maximum = (
        max((point[1 if swapped else 0] for path in paths for point in path), default=1)
        or 1
    )
    screenshot = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    for path in paths:
        for start, stop in zip(path[:-1], path[1:], strict=True):
            for fraction in (0.25, 0.5, 0.75):
                point = np.array(start) + (np.array(stop) - start) * fraction
                if swapped:
                    px = left + (point[0] + 0.5) / values.shape[1] * bounds["width"]
                    py = top - point[1] / maximum * 80
                else:
                    px = left + bounds["width"] + point[0] / maximum * 100
                    py = top + (point[1] + 0.5) / values.shape[0] * bounds["height"]
                px, py = round(px * 1.5), round(py * 1.5)
                region = screenshot[py - 3 : py + 4, px - 3 : px + 4].astype(int)
                assert region.size and np.any(np.abs(region - 85).max(axis=2) < 40), (
                    case,
                    point,
                )
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    (tmp_path / f"{case}.svg").write_text(svg)
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


@pytest.mark.parametrize("swapped", [False, True])
def test_cell_hover_after_tree_reordering_and_resize(page, tmp_path, swapped):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.heatmap(
            make_heatmap_adata(),
            ["g1", "g2"],
            "group",
            dendrogram=True,
            swap_axes=swapped,
            width=450,
            height=300,
            show=False,
        )
    spec = chart.to_dict()
    first = spec["datasets"][spec["layer"][0]["data"]["name"]][0]
    for width, height in ((450, 300), (600, 420)):
        bounds = render(page, chart.properties(width=width, height=height))
        canvas = page.locator("canvas").first.bounding_box()
        columns, rows = (9, 2) if swapped else (2, 9)
        px = canvas["x"] + bounds["x"] + bounds["width"] / columns / 2
        py = canvas["y"] + bounds["y"] + bounds["height"] / rows / 2
        page.mouse.move(px - 2, py - 2)
        page.wait_for_timeout(450)
        for dx in (0, 1, -1):
            page.mouse.move(px + dx, py)
            page.wait_for_timeout(80)
            if page.locator("table.attributes").is_visible():
                break
        page.locator("table.attributes").wait_for(state="visible")
        values = [
            row.locator("td").inner_text().strip()
            for row in page.locator("table.attributes tr").all()
        ]
        assert values[:4] == [
            first["_obs_id"],
            first["_obs_label"],
            first["_gene"],
            first["_group"],
        ]
        assert float(values[4]) == first["_value"]
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        page.mouse.wheel(0, -200)
        page.wait_for_timeout(80)
        assert (
            page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
            == svg
        )
    output = tmp_path / "heatmap.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
