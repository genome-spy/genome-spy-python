"""Observed native track registration, hover, legends and linked navigation."""

import warnings
import xml.etree.ElementTree as ET

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_heatmap import hover_at
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.helpers import tree_segments, units


@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("group_gap", [0, 5])
@pytest.mark.parametrize("page", [1, 1.5], indirect=True)
def test_tracks_tree_hover_and_linked_x_zoom(page, log, group_gap):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        a = make_heatmap_adata()
    chart = gsc.pl.tracksplot(
        a,
        {"First": ["g1", "g2"], "Last": ["g3"]},
        "group",
        dendrogram=True,
        log=log,
        zoom=True,
        group_gap=group_gap,
        spacing=7 if group_gap else 0,
        width=540,
        height=180,
        show=False,
    )
    spec = chart.to_dict()
    spec["scales"]["x"]["name"] = "cells"
    render(page, spec)
    boxes = [
        page.evaluate(f"api.views.getLayoutBounds({{scope:[],view:'panel-{i}'}})")
        for i in range(5)
    ]
    assert all(box["width"] == pytest.approx(540) for box in boxes), boxes
    assert len({round(box["x"], 2) for box in boxes}) == 1
    for previous, current in zip(boxes, boxes[1:]):
        assert current["y"] - previous["y"] - previous["height"] == pytest.approx(
            7 if group_gap else 0
        )
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    root = ET.fromstring(svg)
    labels = [element.text for element in root.iter() if element.tag.endswith("}text")]
    assert all(
        label in labels for label in ["g1", "g2", "g3", "group", "C", "A", "D", "B"]
    )
    assert tree_segments(root)
    # Native SVG rects expose actual cell footprints, not just a generated spec.
    rect_groups = [
        element for element in root.iter() if element.get("data-mark-type") == "rect"
    ]
    profiles = [group for group in rect_groups if len(list(group)) > 1][:3]
    assert len(profiles) == 3
    cells = spec["datasets"][spec["data"]["name"]]
    cuts = [3, 4, 7]
    step = (540 - len(cuts) * group_gap) / 9

    def cell_left(row):
        return row["_cell"] * step + group_gap * sum(
            cut <= row["_cell"] for cut in cuts
        )

    for slot, (group, bounds) in enumerate(zip(profiles, boxes[1:4], strict=True)):
        domain = units(spec)[slot + 1]["layer"][0]["encoding"]["y"]["scale"]["domain"]
        low, high = np.log(domain) if log else domain
        visible = [row for row in cells if not log or row[f"_value_{slot}"] > 0]
        rects = list(group)
        assert len(rects) == len(visible)
        for rect, row in zip(rects, visible, strict=True):
            value = row[f"_value_{slot}"]
            transformed = np.log(value) if log else value
            top = bounds["y"] + (high - transformed) / (high - low) * bounds["height"]
            baseline = (
                bounds["y"] + (1 if log else high / (high - low)) * bounds["height"]
            )
            # Native SVG rects include a subpixel overlap to avoid seams.
            assert float(rect.get("x")) == pytest.approx(
                bounds["x"] + cell_left(row), abs=0.25
            )
            assert float(rect.get("y")) == pytest.approx(top, abs=0.25)
            assert float(rect.get("width")) == pytest.approx(step, abs=0.31)
            assert float(rect.get("height")) == pytest.approx(baseline - top, abs=0.31)
    probe = max(cells, key=lambda row: row["_value_0"])
    bounds = boxes[1]
    hover_at(page, bounds["x"] + cell_left(probe) + step / 2, bounds["y"] + 30)
    tooltip = page.locator("table.attributes")
    assert probe["_obs_id"] in tooltip.inner_text()
    assert "g1 expression" in tooltip.inner_text()
    strip = boxes[-1]
    hover_at(page, strip["x"] + 30, strip["y"] + 7)
    assert page.locator("table.attributes").is_visible()
    assert "group" in page.locator("table.attributes").inner_text()
    canvas = page.locator("canvas").first.bounding_box()
    track = boxes[1]
    page.mouse.move(canvas["x"] + track["x"] + 270, canvas["y"] + track["y"] + 30)
    before = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
    page.mouse.wheel(0, -250)
    # Finish native wheel animation before measuring the pan.
    page.evaluate("""async () => {
        const scale = api.getScaleResolutionByName('cells');
        let previous = scale.getDomain().slice(), stable = 0;
        while (stable < 3) {
            await new Promise(requestAnimationFrame);
            const current = scale.getDomain();
            stable = current.every((value, i) => value === previous[i]) ? stable + 1 : 0;
            previous = current.slice();
        }
    }""")
    after = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
    assert np.ptp(after) < np.ptp(before)
    page.mouse.down()
    page.mouse.move(
        canvas["x"] + track["x"] + 320, canvas["y"] + track["y"] + 30, steps=5
    )
    page.mouse.up()
    page.wait_for_timeout(100)
    panned = page.evaluate("api.getScaleResolutionByName('cells').getDomain()")
    assert panned[0] < after[0] and panned[1] < after[1]
    assert np.ptp(panned) < np.ptp(before)
    # Fixed pixel gaps entering/leaving the viewport can change the data span.
    if not group_gap:
        assert np.ptp(panned) == pytest.approx(np.ptp(after))
    assert "NaN" not in page.evaluate(
        "async () => (await api.imageExport.svg()).blob.text()"
    )
