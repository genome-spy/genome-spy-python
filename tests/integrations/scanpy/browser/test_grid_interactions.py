"""Observe shared grid navigation, fitted values and dot row/column highlighting."""

import re
import warnings
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.clustermap_fixture import make_cluster_adata


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


@pytest.mark.parametrize(
    "family", ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]
)
def test_default_zoom_and_pan_change_only_y(page, family):
    common = dict(zoom=True, width=180, height=90, show=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        if family == "matrix":
            chart = gsc.pl.matrix(
                np.arange(12).reshape(4, 3), show_values=True, **common
            )
        elif family == "clustermap":
            chart = gsc.pl.clustermap(make_cluster_adata(), show_values=True, **common)
        else:
            chart = getattr(gsc.pl, family)(
                make_heatmap_adata(),
                ["g1", "g2", "g3"],
                "group",
                **(
                    {"highlight": True}
                    if family == "dotplot"
                    else {"show_values": True}
                ),
                **common,
            )
    bounds = render(page, chart)
    domains = f"['{family}-x','{family}-y'].map(n=>api.getScaleResolutionByName(n).getDomain())"
    before = page.evaluate(domains)
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -800)
    page.wait_for_timeout(180)
    zoomed = page.evaluate(domains)
    assert zoomed[0] == before[0]
    assert zoomed[1][1] - zoomed[1][0] < before[1][1] - before[1][0]
    if family == "heatmap":
        assert value_texts(svg_root(page))
    page.mouse.down()
    page.mouse.move(px + 25, py + 15, steps=5)
    page.mouse.up()
    page.wait_for_timeout(150)
    panned = page.evaluate(domains)
    assert panned[0] == before[0]
    assert panned[1] != zoomed[1]


@pytest.mark.parametrize(
    "family,swapped",
    [
        (family, swapped)
        for family in ("dotplot", "matrixplot")
        for swapped in (False, True)
    ]
    + [("clustermap", False)],
)
def test_enabling_navigation_keeps_initial_pixels(page, family, swapped):
    images, circles, rectangles = [], [], []
    for zoom in (False, True):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            common = dict(zoom=zoom, width=360, height=260, show=False)
            if family == "clustermap":
                chart = gsc.pl.clustermap(
                    make_cluster_adata(), obs_keys="group", **common
                )
            else:
                chart = getattr(gsc.pl, family)(
                    make_heatmap_adata(),
                    ["g1", "g2", "g3"],
                    "group",
                    swap_axes=swapped,
                    **common,
                    **({"highlight": zoom} if family == "dotplot" else {}),
                )
        target = page.context.new_page()
        try:
            bounds = render(target, chart)
            canvas = target.locator("canvas").first.bounding_box()
            pixels = target.screenshot(
                clip={
                    "x": canvas["x"] + bounds["x"],
                    "y": canvas["y"] + bounds["y"],
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
            images.append(np.asarray(Image.open(BytesIO(pixels))).astype(int))
            circles.append(
                sorted(
                    tuple(e.get(k) for k in ("cx", "cy", "r", "fill"))
                    for e in svg_root(target).iter()
                    if e.tag.endswith("circle")
                )
            )
            rectangles.append(
                sorted(
                    tuple(rect.get(k) for k in ("x", "y", "width", "height", "fill"))
                    for group in svg_root(target).iter()
                    if group.get("data-mark-type") == "rect"
                    for rect in group
                    if rect.tag.endswith("rect")
                )
            )
        finally:
            target.close()
    assert images[0].shape == images[1].shape
    assert circles[0] == circles[1]
    assert rectangles[0] == rectangles[1]
    difference = np.abs(images[0][2:-2, 2:-2] - images[1][2:-2, 2:-2]).max(axis=2)
    # Native clipped marks can rasterize differently along their antialiased edges.
    edges = np.zeros(difference.shape, dtype=bool)
    yy, xx = np.indices(difference.shape)
    for cx, cy, radius, _ in circles[0]:
        edges |= (
            np.abs(
                np.hypot(
                    xx + 2 + bounds["x"] - float(cx), yy + 2 + bounds["y"] - float(cy)
                )
                - float(radius)
            )
            < 2
        )
    for left, top, width, height, _ in rectangles[0]:
        left, top, width, height = map(float, (left, top, width, height))
        px, py = xx + 2 + bounds["x"], yy + 2 + bounds["y"]
        edges |= (
            (px >= left - 2)
            & (px <= left + width + 2)
            & (py >= top - 2)
            & (py <= top + height + 2)
            & (
                (np.abs(px - left) < 2)
                | (np.abs(px - left - width) < 2)
                | (np.abs(py - top) < 2)
                | (np.abs(py - top - height) < 2)
            )
        )
    assert difference[~edges].max() <= 2


@pytest.mark.parametrize("family", ["matrix", "matrixplot", "heatmap", "clustermap"])
def test_dense_values_appear_after_zoom_and_do_not_block_hover(page, family, tmp_path):
    from anndata import AnnData

    values = np.random.default_rng(41).uniform(0, 4, size=(30, 30))
    common = dict(width=180, height=180, zoom="xy", show_values=True, show=False)
    if family == "matrix":
        chart = gsc.pl.matrix(values, **common)
    else:
        a = AnnData(
            values,
            obs=pd.DataFrame(
                {"group": pd.Categorical([f"c{i}" for i in range(30)])},
                index=[f"cell{i}" for i in range(30)],
            ),
            var=pd.DataFrame(index=[f"g{i}" for i in range(30)]),
        )
        if family == "clustermap":
            chart = gsc.pl.clustermap(a, standard_scale=1, **common)
        else:
            chart = getattr(gsc.pl, family)(
                a, list(a.var_names), "group", standard_scale="var", **common
            )
    bounds = render(page, chart)
    assert not value_texts(svg_root(page))
    pointer(page, bounds)
    page.mouse.wheel(0, -800)
    page.wait_for_timeout(180)
    labels = value_texts(svg_root(page))
    assert labels
    label = min(
        labels,
        key=lambda e: sum(
            (v - c) ** 2
            for v, c in zip(
                position(e), (bounds["x"] + 90, bounds["y"] + 90), strict=True
            )
        ),
    )
    canvas = page.locator("canvas").first.bounding_box()
    px, py = position(label)
    page.mouse.move(canvas["x"] + px - 2, canvas["y"] + py - 2)
    page.wait_for_timeout(450)
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        page.mouse.move(canvas["x"] + px + dx, canvas["y"] + py + dy)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    page.locator("table.attributes").wait_for(state="visible")
    plotted = float(
        page.locator("table.attributes tr")
        .last.locator("td")
        .inner_text()
        .replace("−", "-")
    )
    assert plotted == pytest.approx(float(label.text.replace("−", "-")), abs=0.0051)
    if family != "matrix":
        assert 0 <= plotted <= 1
        if family != "clustermap":
            assert "scaled" in page.locator("table.attributes").inner_text()
    page.screenshot(path=str(tmp_path / f"{family}-zoomed-values.png"), full_page=True)
    # The same declarative interactions must survive standalone HTML delivery.
    if family == "matrix":
        output = tmp_path / "matrix-values.html"
        chart.save(output, inline=True, controls=False)
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        assert page.locator(".message-box").count() == 0


@pytest.mark.parametrize(
    "scheme,alpha,expected",
    [
        ("viridis", 1, ["white", "black"]),
        ("blues", 1, ["black", "white"]),
        ("redblue", 1, ["white", "white"]),
        ("viridis", 0.1, ["black", "black"]),
    ],
)
def test_text_contrast_follows_native_palette_bounds_and_opacity(
    page, scheme, alpha, expected
):
    a = make_heatmap_adata()
    a.X[:, :2] = [0, 1]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.heatmap(
            a,
            ["g1", "g2"],
            "group",
            cmap=scheme,
            alpha=alpha,
            vmin=0.2,
            vmax=0.8,
            show_values=True,
            width=200,
            height=270,
            show=False,
        )
    render(page, chart)
    labels = value_texts(svg_root(page))
    assert len(labels) == 18
    for text, color in zip(("0.00", "1.00"), expected, strict=True):
        assert {e.get("fill") for e in labels if e.text == text} == {color}


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_summary_zoom_and_pan_keep_tree_leaves_and_labels_aligned(
    page, family, swapped
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = getattr(gsc.pl, family)(
            make_heatmap_adata(),
            ["g1", "g2", "g3"],
            "group",
            dendrogram=True,
            swap_axes=swapped,
            zoom="xy",
            width=360,
            height=260,
            show=False,
            **({"highlight": True} if family == "dotplot" else {"show_values": True}),
        )
    bounds = render(page, chart)
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -220)
    page.wait_for_timeout(160)
    before = page.evaluate(f"api.getScaleResolutionByName('{family}-x').getDomain()")
    for pan in (False, True):
        if pan:
            page.mouse.down()
            page.mouse.move(px + 18, py + 15, steps=5)
            page.mouse.up()
            page.wait_for_timeout(150)
        root = svg_root(page)
        labels = {
            e.text: position(e)
            for e in root.iter()
            if e.tag.endswith("text") and e.text in {"A", "B", "C", "D"}
        }
        assert labels
        tree = next(e for e in root.iter() if e.get("stroke") == "#555555")
        edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
        leaves = [
            float(line.get(("x" if swapped else "y") + endpoint))
            for line in tree
            for endpoint in ("1", "2")
            if abs(float(line.get(("y" if swapped else "x") + endpoint)) - edge) < 1
        ]
        assert all(
            any(abs(leaf - xy[0 if swapped else 1]) < 0.2 for leaf in leaves)
            for xy in labels.values()
        )
    assert (
        page.evaluate(f"api.getScaleResolutionByName('{family}-x').getDomain()")
        != before
    )


@pytest.mark.parametrize("swapped", [False, True])
@pytest.mark.parametrize("hover", [False, True])
def test_dot_highlight_follows_slots_clears_and_preserves_size_guides(
    page, swapped, hover, tmp_path
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = gsc.pl.dotplot(
            make_heatmap_adata(),
            ["g2", "g2", "g1"],
            "group",
            swap_axes=swapped,
            highlight=True,
            zoom="xy",
            hover=hover,
            width=360,
            height=260,
            show=False,
        )
    bounds = render(page, chart)
    coordinates = (
        "['x','y'].map(axis => api.getParam('grid_cursor').getValue().values[axis])"
    )
    assert page.evaluate(coordinates) == [None, None]
    # The two g2 slots have the same label but must select different columns/rows.
    for slot in (0, 1):
        column, row = (0, slot) if swapped else (slot, 0)
        columns, rows = (4, 3) if swapped else (3, 4)
        pointer(page, bounds, (column + 0.8) / (columns + 0.6), (row + 1) / (rows + 1))
        page.wait_for_timeout(100)
        assert page.evaluate(coordinates) == [column, row]
        root = svg_root(page)
        guides = ruler_lines(root)
        assert len(guides) == 2
        vertical, horizontal = guides
        x = bounds["x"] + (column + 0.8) / (columns + 0.6) * bounds["width"]
        y = bounds["y"] + (row + 1) / (rows + 1) * bounds["height"]
        assert [float(vertical.get(k)) for k in ("x1", "x2")] == pytest.approx(
            [x, x], abs=1
        )
        assert sorted(float(vertical.get(k)) for k in ("y1", "y2")) == pytest.approx(
            [bounds["y"], bounds["y"] + bounds["height"]], abs=1
        )
        assert [float(horizontal.get(k)) for k in ("y1", "y2")] == pytest.approx(
            [y, y], abs=1
        )
        assert sorted(float(horizontal.get(k)) for k in ("x1", "x2")) == pytest.approx(
            [bounds["x"], bounds["x"] + bounds["width"]], abs=1
        )
        # Rulers track the whole slot, even away from any hoverable dot.
        pointer(
            page, bounds, (column + 0.4) / (columns + 0.6), (row + 0.6) / (rows + 1)
        )
        page.wait_for_timeout(100)
        assert page.evaluate(coordinates) == [column, row]
        assert not page.locator("table.attributes").is_visible()
    px, py = pointer(
        page, bounds, (column + 0.8) / (columns + 0.6), (row + 1) / (rows + 1)
    )
    page.wait_for_timeout(450)
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(80)
        if page.locator("table.attributes").is_visible():
            break
    if hover:
        page.get_by_text("Expressing cells (%)", exact=True).wait_for(state="visible")
    else:
        assert page.locator("table.attributes").count() == 0
    radii = sorted(
        float(e.get("r")) for e in svg_root(page).iter() if e.tag.endswith("circle")
    )
    pointer(page, bounds)
    page.mouse.wheel(0, -200)
    page.wait_for_timeout(150)
    after = sorted(
        float(e.get("r")) for e in svg_root(page).iter() if e.tag.endswith("circle")
    )
    assert after == radii
    origins = page.evaluate(
        "['grid_x_origin','grid_y_origin','grid_x_step','grid_y_step'].map(n=>api.getParam(n).getValue())"
    )
    px, py = pointer(
        page,
        bounds,
        origins[0] + (column + 0.5) * origins[2],
        origins[1] + (row + 0.5) * origins[3],
    )
    for dx in (0, 1, -1):
        page.mouse.move(px + dx, py)
        page.wait_for_timeout(100)
        selected = page.evaluate(coordinates)
        if selected == [column, row]:
            break
    assert selected == [column, row]
    canvas = page.locator("canvas").first.bounding_box()
    vertical, horizontal = ruler_lines(svg_root(page))
    assert float(vertical.get("x1")) == pytest.approx(px - canvas["x"], abs=1)
    assert float(horizontal.get("y1")) == pytest.approx(py - canvas["y"], abs=1)
    page.mouse.move(1, 1)
    page.wait_for_timeout(100)
    assert page.evaluate(coordinates) == [None, None]
    assert not ruler_lines(svg_root(page))
    if not hover:
        output = tmp_path / "dotplot-rulers.html"
        chart.save(output, inline=True, controls=False)
        page.goto(output.as_uri())
        page.locator("canvas").wait_for(state="visible")
        before = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
        pointer(page, bounds, 0.5, 0.5)
        page.wait_for_timeout(100)
        after = np.asarray(Image.open(BytesIO(page.screenshot()))).astype(int)
        assert (np.abs(after - before).max(axis=2) > 10).sum() > 200
        assert page.locator(".message-box").count() == 0
