"""Observed native time-series heatmaps, including cropped edges and highlights."""

from io import BytesIO
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_grid_interactions import (
    pointer,
    position,
    svg_root,
    value_texts,
)


@pytest.mark.parametrize("shape", [(5, 3), (1, 3), (5, 1), (1, 1)])
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_chart_matches_scanpy_crop_orientation_and_highlights(
    page, tmp_path, shape
):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    values = np.arange(np.prod(shape), dtype=float).reshape(shape)
    names = np.array([f"variable-{i}" for i in range(shape[1])])
    highlights = [0.25] if shape[0] > 1 else [0.025]
    with mpl.rc_context({"figure.dpi": 100, "font.size": 10}):
        sc.pl.timeseries_as_heatmap(values, var_names=names, highlights_x=highlights)
        fig, ax = plt.gcf(), plt.gcf().axes[0]
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        expected = Image.open(reference).convert("RGB")
        expected = expected.crop(
            (
                round(bbox.x0 * 1.5),
                round(expected.height - bbox.y1 * 1.5),
                round(bbox.x1 * 1.5),
                round(expected.height - bbox.y0 * 1.5),
            )
        )
        limits = [ax.get_xlim(), ax.get_ylim()]
        line = ax.lines[0]
        expected_x = ax.transData.transform((highlights[0], 0))[0] - bbox.x0
        plt.close(fig)
    chart = gsc.pl.timeseries_as_heatmap(
        values, var_names=names, highlights_x=highlights, show=False
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.6)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.6)
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
    # Register both exports on the actual plotting limits, away from glyph/edge antialiasing.
    for x in np.linspace(0.08, 0.92, 15):
        if abs(x - expected_x / bbox.width) < 0.015:
            continue
        for y in np.linspace(0.08, 0.92, 13):
            px, py = (
                limits[0][0] + x * np.ptp(limits[0]),
                limits[1][1] - y * np.ptp(limits[1]),
            )
            if any(abs(v - (round(v - 0.5) + 0.5)) < 0.04 for v in (px, py)):
                continue
            np.testing.assert_allclose(
                np.array(actual)[int(y * actual.height), int(x * actual.width)].astype(
                    int
                ),
                np.array(expected)[
                    int(y * expected.height), int(x * expected.width)
                ].astype(int),
                atol=12,
            )
    root = svg_root(page)
    ET.ElementTree(root).write(tmp_path / "native.svg", encoding="unicode")
    labels = {
        e.text: position(e)
        for e in root.iter()
        if e.tag.endswith("text") and (e.text or "").startswith("variable-")
    }
    assert set(labels) == set(names)
    sample_ticks = [
        e
        for e in root.iter()
        if e.tag.endswith("text")
        and e.get("transform")
        and position(e)[1] > bounds["y"] + bounds["height"]
        and bounds["x"] - 1 <= position(e)[0] <= bounds["x"] + bounds["width"] + 1
    ]
    assert len(sample_ticks) >= 2
    for i, name in enumerate(names):
        assert labels[name][1] == pytest.approx(
            bounds["y"]
            + bounds["height"] * (1 - (i - limits[1][0]) / np.ptp(limits[1])),
            abs=0.6,
        )
        assert 0 <= labels[name][0] < bounds["x"]
    rules = [
        e
        for e in root.iter()
        if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
    ]
    assert len(rules) == 1 and len(rules[0]) == 1
    assert float(rules[0][0].get("x1")) == pytest.approx(
        bounds["x"] + expected_x, abs=0.6
    )
    assert float(rules[0].get("stroke-width")) == pytest.approx(
        line.get_linewidth() * 100 / 72, abs=0.06
    )
    assert list(map(float, rules[0].get("stroke-dasharray").split())) == pytest.approx(
        [round(v * 100 / 72) for v in line._dash_pattern[1]]
    )
    gradients = [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
    ]
    assert len(gradients) == 1
    assert float(gradients[0].get("height")) == pytest.approx(
        bounds["height"] * 0.5, abs=2
    )
    assert float(gradients[0].get("x")) > bounds["x"] + bounds["width"]
    actual.save(tmp_path / "native-panel.png")
    expected.save(tmp_path / "reference-panel.png")
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "registered-overlay.png"
    )
    page.screenshot(path=str(tmp_path / "native-complete.png"), full_page=True)


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_hover_values_labels_and_highlights_follow_native_zoom(page, tmp_path, zoom):
    values = np.arange(2400).reshape(200, 12)
    names = [f"gene-{i}" for i in range(12)]
    chart = gsc.pl.timeseries_as_heatmap(
        values,
        var_names=names,
        highlights_x=[100.25],
        zoom=zoom,
        show_values=True,
        width=460,
        height=260,
        show=False,
    )
    spec = chart.to_dict()
    for axis in ("x", "y"):
        spec["scales"][axis]["name"] = f"timeseries_as_heatmap-{axis}"
    bounds = render(page, spec)
    initial = {
        axis: page.evaluate(
            "a=>api.getScaleResolutionByName(`timeseries_as_heatmap-${a}`).getDomain()",
            axis,
        )
        for axis in ("x", "y")
    }
    assert not value_texts(svg_root(page))
    px, py = pointer(page, bounds, 100 / 199, 1 - 5 / 11)
    for _ in range(4):
        page.mouse.wheel(0, -350)
        page.wait_for_timeout(250)
    page.wait_for_timeout(700)
    domains = {
        axis: page.evaluate(
            "a=>api.getScaleResolutionByName(`timeseries_as_heatmap-${a}`).getDomain()",
            axis,
        )
        for axis in ("x", "y")
    }
    assert (domains["x"] != initial["x"]) is (zoom == "xy")
    assert np.ptp(domains["y"]) < np.ptp(initial["y"])
    bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
    root = svg_root(page)
    rules = [
        e
        for e in root.iter()
        if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
    ]
    assert len(rules) == 1
    assert float(rules[0][0].get("x1")) == pytest.approx(
        bounds["x"]
        + bounds["width"] * (100.25 - domains["x"][0]) / np.ptp(domains["x"]),
        abs=0.6,
    )
    if zoom == "xy":
        labels = value_texts(root)
        assert labels
        interior = 0
        for label in labels:
            value = float(label.text)
            row, col = next(
                (r, c) for r, c in np.ndindex(values.T.shape) if values.T[r, c] == value
            )
            for i, (axis, slot, extent) in enumerate(
                (("x", col, "width"), ("y", row, "height"))
            ):
                edges = np.clip(
                    (np.array([slot - 0.5, slot + 0.5]) - domains[axis][0])
                    / np.ptp(domains[axis]),
                    0,
                    1,
                )
                if axis == "y":
                    edges = 1 - edges
                edges = bounds[axis] + edges * bounds[extent]
                # Full cells center their labels; partial cells use native text fitting.
                if domains[axis][0] <= slot - 0.5 and slot + 0.5 <= domains[axis][1]:
                    assert position(label)[i] == pytest.approx(
                        float(np.mean(edges)), abs=0.6
                    )
                    interior += 1
        assert interior > 2
    col = int(round(domains["x"][0] + 0.3 * np.ptp(domains["x"])))
    row = int(round(np.mean(domains["y"])))
    x = (col - domains["x"][0]) / np.ptp(domains["x"])
    y = 1 - (row - domains["y"][0]) / np.ptp(domains["y"])
    pointer(page, bounds, x - 0.002, y - 0.002)
    page.wait_for_timeout(450)
    pointer(page, bounds, x, y)
    page.locator("table.attributes").wait_for(state="visible")
    hover = [
        text.strip() for text in page.locator("table.attributes td").all_text_contents()
    ]
    assert hover[:2] == [f"gene-{row}", str(col)]
    assert float(hover[2]) == values[col, row]
    # Panning updates native positions rather than rebuilding the chart in Python.
    page.mouse.down()
    page.mouse.move(px + 18, py + 12, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    moved = page.evaluate(
        "api.getScaleResolutionByName('timeseries_as_heatmap-y').getDomain()"
    )
    assert moved != domains["y"]
    bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
    visible = [
        e
        for e in svg_root(page).iter()
        if e.tag.endswith("text") and (e.text or "").startswith("gene-")
    ]
    assert visible
    for label in visible:
        slot = int(label.text.removeprefix("gene-"))
        assert moved[0] <= slot <= moved[1]
        assert position(label)[1] == pytest.approx(
            bounds["y"] + bounds["height"] * (1 - (slot - moved[0]) / np.ptp(moved)),
            abs=0.6,
        )
    path = tmp_path / "timeseries.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
