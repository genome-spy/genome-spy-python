"""Pointer gestures and exported state used by observed interaction checks."""

import re
import xml.etree.ElementTree as ET

import numpy as np

from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.helpers import leaf_marks, units


def render_summary(page, chart):
    """Render the summary and return the view names used by interaction checks."""
    spec = chart.to_dict()
    names = {view.get("name"): f"panel-{i}" for i, view in enumerate(units(spec))}
    for view in units(spec):
        for leaf in leaf_marks(view):
            if leaf.get("name"):
                names.setdefault(leaf["name"], leaf["name"])
    render(page, spec)
    return names


def rows(page, name):
    """Read a small view table through the public browser API."""
    return page.evaluate(
        "name => api.views.get({scope:[],view:name}).data.read({scope:'all',limit:100}).rows",
        name,
    )


def set_brush(page, intervals):
    """Set the shared cell brush and wait for the next frame."""
    page.evaluate(
        "intervals => api.params.get('cells').setValue({type:'interval', intervals})",
        intervals,
    )
    page.evaluate("() => new Promise(requestAnimationFrame)")


def point_spacing(coordinates):
    """Measure adjacent sample and paired-value spacing despite viewport culling."""
    xs = np.unique(coordinates[:, 0])
    paired = [np.ptp(coordinates[coordinates[:, 0] == x, 1]) for x in xs]
    return np.median(np.diff(xs)), np.median([d for d in paired if d > 0])


def point_coordinates(page):
    """Read exported circle centers to observe navigation without naming scales."""
    return [
        np.array([[float(p.get("cx")), float(p.get("cy"))] for p in group])
        for group in svg_root(page).iter()
        if group.get("data-mark-type") == "point" and group.get("clip-path")
    ]


def svg_root(page):
    """Read native exported geometry after the renderer finishes its frame."""
    return ET.fromstring(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )


def value_texts(root):
    """Find visible fitted values, excluding axis and legend text."""
    return [
        e
        for e in root.iter()
        if e.tag.endswith("text")
        and e.get("fill") in ("white", "black")
        and re.fullmatch(r"[−-]?\d+\.\d{2}", e.text or "")
    ]


def position(element):
    """Read the native SVG text position in logical canvas pixels."""
    return [
        float(v)
        for v in re.search(r"translate\(([^)]+)\)", element.get("transform"))
        .group(1)
        .split()
    ]


def ruler_lines(root):
    """Read the visible native crosshair lines from an exported chart."""
    return [
        line
        for group in root.iter()
        if group.get("stroke") == "#4682b4"
        for line in group
        if line.tag.endswith("line")
    ]


def pointer(page, bounds, x=0.5, y=0.5):
    """Move inside a plot using fractions of its logical extent."""
    canvas = page.locator("canvas").first.bounding_box()
    px, py = (
        canvas["x"] + bounds["x"] + x * bounds["width"],
        canvas["y"] + bounds["y"] + y * bounds["height"],
    )
    page.mouse.move(px, py)
    return px, py


def hover_at(page, x, y, *, probe=True, canvas_index=0, target=None):
    """Pause then move within the native tooltip's small picking neighborhood."""
    canvas = page.locator("canvas").nth(canvas_index).bounding_box()
    page.mouse.move(canvas["x"] + x - 2, canvas["y"] + y - 2)
    page.wait_for_timeout(450)
    offsets = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)) if probe else ((0, 0),)
    for dx, dy in offsets:
        page.mouse.move(canvas["x"] + x + dx, canvas["y"] + y + dy)
        page.wait_for_timeout(80)
        if target is not None and target.is_visible():
            break


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
        if (
            page.locator("table.attributes")
            .get_by_text(expected_id, exact=True)
            .first.is_visible()
        ):
            break
    return px, py


def wait_for_navigation(page, family, probe=2):
    """Wait for stable scale positions before measuring a completed zoom or pan."""
    page.evaluate(
        """async ({family,probe})=>{
        const sample=()=>['x','y'].flatMap(axis=>{
            const s=api.getScaleResolutionByName(`${family}-${axis}`).getScale();
            return [...s.domain(),s(0),s(probe)];
        });
        let previous=sample(), stable=0;
        const deadline=performance.now()+3000;
        while(performance.now()<deadline){
            await new Promise(requestAnimationFrame);
            const current=sample();
            stable=current.every((v,i)=>Math.abs(v-previous[i])<1e-7)?stable+1:0;
            if(stable>=3)return;
            previous=current;
        }
        throw Error('Navigation did not settle');
    }""",
        {"family": family, "probe": probe},
    )
