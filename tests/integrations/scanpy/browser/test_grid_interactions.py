"""Observe shared grid navigation, fitted values and dot row/column highlighting."""

import warnings
from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    pointer,
    position,
    ruler_lines,
    svg_root,
    value_texts,
)
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.clustermap_fixture import make_cluster_adata
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.helpers import tree_segments


@pytest.mark.parametrize("hover", [False, True])
def test_clustermap_strip_hover_before_and_after_navigation(page, hover):
    data = make_cluster_adata()
    chart = gsc.pl.clustermap(
        data,
        obs_keys="group",
        width=360,
        height=240,
        zoom="xy",
        hover=hover,
        show=False,
    )
    spec = chart.to_dict()
    records = spec["datasets"][spec["spec"]["layer"][0]["data"]["name"]]
    groups = [
        data.obs.loc[name, "group"]
        for name in dict.fromkeys(row["_row"] for row in records)
    ]
    bounds = render(page, chart)
    for navigated in (False, True):
        if navigated:
            px, py = pointer(page, bounds)
            page.mouse.wheel(0, -260)
            page.wait_for_timeout(700)
            page.mouse.down()
            page.mouse.move(px + 12, py + 10, steps=5)
            page.mouse.up()
            page.wait_for_timeout(700)
        centers = page.evaluate("""() => {
            const s=api.getScaleResolutionByName('clustermap-y').getScale();
            return Array.from({length:6},(_,i)=>1-s(i)+s.bandwidth()/2);
        }""")
        slot = min(range(len(groups)), key=lambda i: abs(centers[i] - 0.5))
        fraction = centers[slot]
        assert 0 < fraction < 1
        canvas = page.locator("canvas").first.bounding_box()
        px = canvas["x"] + bounds["x"] - 360 * 0.03 / 0.77 / 2
        py = canvas["y"] + bounds["y"] + fraction * bounds["height"]
        hover_at(page, px - canvas["x"], py - canvas["y"])
        if hover:
            page.locator("table.attributes").wait_for(state="visible", timeout=2000)
            assert [
                t.strip()
                for t in page.locator("table.attributes th").all_text_contents()
            ] == ["group"]
            assert [
                t.strip()
                for t in page.locator("table.attributes td").all_text_contents()
            ] == [groups[slot]]
        else:
            assert not page.locator("table.attributes").is_visible()


@pytest.mark.smoke
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
    spec = chart.to_dict()
    if family == "matrix":
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"matrix-{axis}"
    bounds = render(page, spec, scale_prefix=family)
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
    frame = chart.to_dict().get("spec", {}).get("view", {}).get("strokeWidth", 0)
    margin = max(2, int(np.ceil(frame / 2)) + 1)
    difference = np.abs(
        images[0][margin:-margin, margin:-margin]
        - images[1][margin:-margin, margin:-margin]
    ).max(axis=2)
    # Native clipped marks can rasterize differently along their antialiased edges.
    edges = np.zeros(difference.shape, dtype=bool)
    yy, xx = np.indices(difference.shape)
    for cx, cy, radius, _ in circles[0]:
        edges |= (
            np.abs(
                np.hypot(
                    xx + margin + bounds["x"] - float(cx),
                    yy + margin + bounds["y"] - float(cy),
                )
                - float(radius)
            )
            < 2
        )
    for left, top, width, height, _ in rectangles[0]:
        left, top, width, height = map(float, (left, top, width, height))
        px, py = xx + margin + bounds["x"], yy + margin + bounds["y"]
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


@pytest.mark.smoke
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
    if family == "heatmap":
        # Fixed group gaps leave less room for the thirty single-cell rows.
        for _ in range(5):
            if value_texts(svg_root(page)):
                break
            page.mouse.wheel(0, -800)
            page.wait_for_timeout(700)
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


@pytest.mark.smoke
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
    bounds = render(page, chart, scale_prefix=family)
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
        edge = bounds["y"] if swapped else bounds["x"] + bounds["width"]
        endpoints = np.array(tree_segments(root)).reshape(-1, 2)
        leaves = endpoints[
            np.abs(endpoints[:, 1 if swapped else 0] - edge) < 1, 0 if swapped else 1
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
    bounds = render(page, chart, scale_prefix="dotplot")
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
    fractions = page.evaluate(
        """([column,row])=>['x','y'].map((axis,i)=>{
        const s=api.getScaleResolutionByName(`dotplot-${axis}`).getScale();
        return axis==='x' ? s(column)+s.bandwidth()/2 : 1-s(row)+s.bandwidth()/2;
    })""",
        [column, row],
    )
    px, py = pointer(page, bounds, *fractions)
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


@pytest.mark.parametrize("page", [1, 1.5], indirect=True)
@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_summary_feature_spacing_survives_navigation(page, family, swapped):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = getattr(gsc.pl, family)(
            make_heatmap_adata(),
            {"First": ["g2", "g1"], "Again": ["g2"]},
            "group",
            dendrogram=True,
            swap_axes=swapped,
            zoom="xy",
            width=450,
            height=300,
            show=False,
            **(
                {"highlight": True, "group_gap": 4}
                if family == "dotplot"
                else {"show_values": True}
            ),
        )
    bounds = render(page, chart, scale_prefix=family)
    axis = "y" if swapped else "x"
    extent = "height" if swapped else "width"
    for navigated in (False, True):
        if navigated:
            px, py = pointer(page, bounds)
            page.mouse.wheel(0, -180)
            page.wait_for_timeout(200)
            page.mouse.down()
            page.mouse.move(px + 8, py + 8, steps=5)
            page.mouse.up()
        # Wait for the live scale transition before targeting a narrow gap.
        page.evaluate(
            """async family=>{
            const sample=()=>['x','y'].flatMap(axis=>{
                const s=api.getScaleResolutionByName(`${family}-${axis}`).getScale();
                return [...s.domain(),s(0),s(2)];
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
            family,
        )
        live = page.evaluate(
            """({family,axis,extent})=>{
            const s=api.getScaleResolutionByName(`${family}-${axis}`).getScale();
            const sign=axis==='x'?1:-1;
            const edge=s(1)+sign*s.bandwidth();
            return {gap:Math.abs(s(2)-edge)*extent,
                center:axis==='x'?(edge+s(2))/2:1-(edge+s(2))/2};
        }""",
            {"family": family, "axis": axis, "extent": bounds[extent]},
        )
        assert live["gap"] == pytest.approx(4 if family == "dotplot" else 0, abs=0.05)
        # The tree remains inside its native side and touches the matrix edge.
        tree = page.evaluate(
            "name=>api.views.getLayoutBounds({scope:[],view:name})", f"{family}-tree"
        )
        assert (tree["y"] + tree["height"] if swapped else tree["x"]) == pytest.approx(
            bounds["y"] if swapped else bounds["x"] + bounds["width"], abs=0.5
        )
        if family == "matrixplot":
            continue
        fractions = (0.5, live["center"]) if swapped else (live["center"], 0.5)
        pointer(page, bounds, *fractions)
        page.wait_for_timeout(450)
        pointer(page, bounds, *fractions)
        page.wait_for_timeout(100)
        assert not page.locator("table.attributes").is_visible()
        page.mouse.move(1, 1)
        page.wait_for_timeout(100)
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        canvas = page.locator("canvas").first.bounding_box()
        px, py = (
            round(
                canvas[coordinate] + bounds[coordinate] + fraction * bounds[dimension]
            )
            for coordinate, dimension, fraction in zip(
                ("x", "y"), ("width", "height"), fractions, strict=True
            )
        )
        assert (
            pixels[
                round(py * page.evaluate("devicePixelRatio")),
                round(px * page.evaluate("devicePixelRatio")),
            ].min()
            > 245
        )
