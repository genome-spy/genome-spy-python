"""Registered heatmap tiles, complete annotations, unequal trees and cell hover."""

from io import BytesIO
import json
from pathlib import Path
import re
import warnings
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata, heatmap_cases

FIXTURES = Path(__file__).parents[1] / "fixtures"
REFERENCE = json.loads((FIXTURES / "heatmap.json").read_text())


@pytest.mark.parametrize("swapped", [False, True])
def test_zoom_moves_cell_annotations_and_tree(page, swapped):
    chart = gsc.pl.heatmap(
        make_heatmap_adata(),
        {"First": ["g1", "g2"], "Last": ["g3"]},
        "group",
        dendrogram=True,
        swap_axes=swapped,
        zoom="xy",
        width=450,
        height=300,
        show=False,
    )
    bounds = render(page, chart)
    before = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + bounds["x"] + 225, canvas["y"] + bounds["y"] + 150)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(180)
    domains = page.evaluate(
        "['heatmap-x','heatmap-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
    )
    assert domains[0][1] - domains[0][0] < (8 if swapped else 2)
    assert domains[1][1] - domains[1][0] < (2 if swapped else 8)
    after = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert before != after
    root = ET.fromstring(after)
    texts = {
        element.text: [
            float(value)
            for value in re.search(r"translate\(([^)]+)\)", element.get("transform"))
            .group(1)
            .split()
        ]
        for element in root.iter()
        if element.tag.endswith("text")
        and element.text in {"A", "D", "g1", "g2", "g3", "First", "Last"}
    }
    # Gene labels outside the visible rows/columns must disappear after zooming.
    assert "g2" in texts and "g1" not in texts and "g3" not in texts
    assert "First" not in texts and "Last" not in texts
    tree = next(
        element for element in root.iter() if element.get("stroke") == "#555555"
    )
    edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
    leaves = [
        float(line.get("x" + endpoint if swapped else "y" + endpoint))
        for line in tree
        for endpoint in ("1", "2")
        if abs(float(line.get("y" + endpoint if swapped else "x" + endpoint)) - edge)
        < 1
    ]
    for group in ("A", "D"):
        assert any(
            abs(point - texts[group][0 if swapped else 1]) < 0.2 for point in leaves
        ), (group, texts, leaves, bounds)
    # The center tile keeps the same cell identity after zooming around the center.
    px = canvas["x"] + bounds["x"] + bounds["width"] / 2
    py = canvas["y"] + bounds["y"] + bounds["height"] / 2
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.locator("table.attributes").wait_for(state="visible")
    spec = chart.to_dict()
    cell = spec["datasets"][spec["layer"][0]["data"]["name"]][4 * 3 + 1]
    assert [
        row.locator("td").inner_text().strip()
        for row in page.locator("table.attributes tr").all()
    ][:4] == [cell["_obs_id"], cell["_obs_label"], cell["_gene"], cell["_group"]]
    # Panning changes the visible domain while the tree stays within the cell extent.
    page.mouse.move(canvas["x"] + bounds["x"] + 225, canvas["y"] + bounds["y"] + 150)
    page.mouse.down()
    page.mouse.move(
        canvas["x"] + bounds["x"] + 270, canvas["y"] + bounds["y"] + 180, steps=5
    )
    page.mouse.up()
    page.wait_for_timeout(150)
    assert (
        page.evaluate(
            "['heatmap-x','heatmap-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
        )
        != domains
    )
    panned = ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    tree = next(
        element for element in panned.iter() if element.get("stroke") == "#555555"
    )
    start, extent = (
        (bounds["x"], bounds["width"]) if swapped else (bounds["y"], bounds["height"])
    )
    for line in tree:
        for endpoint in ("1", "2"):
            assert (
                start - 1
                <= float(line.get(("x" if swapped else "y") + endpoint))
                <= start + extent + 1
            )


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", heatmap_cases())
def test_complete_registered_heatmaps(page, tmp_path, reference_images, case):
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
    expected = Image.open(
        reference_images("heatmap") / f"heatmap-{case}-panel.png"
    ).convert("RGB")
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
