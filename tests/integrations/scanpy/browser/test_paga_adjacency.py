"""Registered adjacency tiles/tree points and observed native matrix interactions."""

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import (
    hover_at,
    point_coordinates,
    pointer,
    svg_root,
)
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.paga_fixtures import make_adjacency


@pytest.mark.reference
@pytest.mark.parametrize(
    "case", ["default", "empty_tree", "missing", "constant", "singleton"]
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_registered_complete_chart_matches_scanpy(page, tmp_path, case):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_adjacency(case=case)
    plt.close("all")
    with mpl.rc_context({"figure.dpi": 100}):
        sc.pl.paga_adjacency(a, color_map="viridis", show=False)
        fig = plt.gcf()
        ax = fig.axes[0]
        # Register the larger reviewed tree dots while retaining upstream positions.
        for artist in ax.collections:
            artist.set_sizes([16 / (100 / 72) ** 2])
            artist.set_linewidths([0])
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        points = np.concatenate([c.get_offsets() for c in ax.collections])
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        full = Image.open(reference).convert("RGB")
        expected = full.crop(
            (
                round(bbox.x0 * 1.5),
                round(full.height - bbox.y1 * 1.5),
                round(bbox.x1 * 1.5),
                round(full.height - bbox.y0 * 1.5),
            )
        )
        plt.close(fig)
    chart = gsc.pl.paga_adjacency(a, width=bbox.width, height=bbox.height, show=False)
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.5)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.5)
    actual = panel_image(page, bounds)
    assert abs(actual.width - expected.width) <= 2
    assert abs(actual.height - expected.height) <= 2
    pixels, target = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    count = a.uns["connectivities"].shape[0]
    for row, col in np.ndindex(count, count):
        for fraction in (0.25, 0.75):
            x, y = (col + fraction) / count, (row + fraction) / count
            np.testing.assert_allclose(
                pixels[int(y * actual.height), int(x * actual.width)],
                target[int(y * expected.height), int(x * expected.width)],
                atol=12,
            )
    point_groups = point_coordinates(page)
    assert len(point_groups) == bool(len(points))
    centers = point_groups[0] if len(points) else []
    expected_centers = [
        (
            bounds["x"] + (x + 0.5) / count * bounds["width"],
            bounds["y"] + (y + 0.5) / count * bounds["height"],
        )
        for x, y in points
    ]
    np.testing.assert_allclose(
        np.asarray(centers).reshape(-1, 2),
        np.asarray(expected_centers).reshape(-1, 2),
        atol=0.6,
    )
    for x, y in points:
        sizes = []
        for image in (actual, expected):
            cx, cy = (
                int((x + 0.5) / count * image.width),
                int((y + 0.5) / count * image.height),
            )
            patch = np.asarray(image)[cy - 5 : cy + 6, cx - 5 : cx + 6]
            sizes.append(np.count_nonzero((patch < 40).all(axis=2)))
        assert sizes[0] > 0 and sizes[1] > 0
        assert abs(sizes[0] - sizes[1]) <= 8
    root = svg_root(page)
    gradients = [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
    ]
    assert len(gradients) == 1
    assert float(gradients[0].get("height")) == pytest.approx(
        bounds["height"] * 0.5, abs=2
    )
    labels = {e.text for e in root.iter() if e.tag.endswith("text")}
    assert {str(i) for i in range(count)} <= labels
    page.screenshot(path=str(tmp_path / "native-complete.png"), full_page=True)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "registered-overlay.png"
    )


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_tree_points_follow_matrix_zoom_pan_with_hover_and_values(page, tmp_path, zoom):
    chart = gsc.pl.paga_adjacency(
        make_adjacency(), zoom=zoom, show_values=True, width=360, height=360, show=False
    )
    spec = chart.to_dict()
    for axis in ("x", "y"):
        spec["scales"][axis]["name"] = f"paga_adjacency-{axis}"
    bounds = render(page, spec)
    xname, yname = "paga_adjacency-x", "paga_adjacency-y"
    xbefore = page.evaluate(
        "name=>api.getScaleResolutionByName(name).getDomain()", xname
    )
    ybefore = page.evaluate(
        "name=>api.getScaleResolutionByName(name).getDomain()", yname
    )
    canvas = page.locator("canvas").first.bounding_box()
    # A tree point at (x=0,y=2) is deliberately transposed from matrix row zero.
    hover_at(
        page,
        canvas["x"] + bounds["x"] + bounds["width"] / 6,
        canvas["y"] + bounds["y"] + bounds["height"] * 5 / 6,
    )
    table = page.locator("table.attributes")
    assert table.get_by_text("Source group", exact=True).is_visible()
    assert [
        r.locator("td").inner_text().strip() for r in table.locator("tr").all()
    ] == ["0", "2"]
    hover_at(
        page,
        canvas["x"] + bounds["x"] + bounds["width"] * 5 / 6,
        canvas["y"] + bounds["y"] + bounds["height"] / 6,
    )
    values = [r.locator("td").inner_text().strip() for r in table.locator("tr").all()]
    assert values[:2] == ["0", "2"]
    assert float(values[2]) == pytest.approx(0.6)
    before_points = point_coordinates(page)[0]
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -180)
    page.wait_for_timeout(250)
    page.mouse.down()
    page.mouse.move(px + 12, py + 12, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    assert (
        page.evaluate("name=>api.getScaleResolutionByName(name).getDomain()", xname)
        != xbefore
    ) is (zoom == "xy")
    assert (
        page.evaluate("name=>api.getScaleResolutionByName(name).getDomain()", yname)
        != ybefore
    )
    after_points = point_coordinates(page)[0]
    assert not np.array_equal(after_points, before_points)
    projected = page.evaluate(
        """()=>{const x=api.getScaleResolutionByName('paga_adjacency-x').getScale();
        const y=api.getScaleResolutionByName('paga_adjacency-y').getScale();
        return [[0,2],[1,0]].map(([a,b])=>[
            x(a)+x.bandwidth()/2, 1-y(b)+y.bandwidth()/2]);}"""
    )
    projected = np.asarray(projected)
    # Native culling omits point centers outside the zoomed viewport.
    visible = ((projected >= 0) & (projected <= 1)).all(axis=1)
    expected = projected[visible] * [bounds["width"], bounds["height"]]
    expected += [bounds["x"], bounds["y"]]
    np.testing.assert_allclose(after_points, expected, atol=0.6)
    root = svg_root(page)
    assert any(e.tag.endswith("text") and e.text == "0.20" for e in root.iter())
    output = tmp_path / "paga-adjacency.html"
    chart.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_named_strips_keep_index_labels_aligned_and_legend_below_axis(page, zoom):
    from tests.integrations.scanpy.browser.interactions import position

    labels = ["Repeated long group", "Middle group", "Repeated long group"]
    chart = gsc.pl.paga_adjacency(
        make_adjacency(),
        as_heatmap=False,
        labels=labels,
        zoom=zoom,
        width=400,
        height=240,
        show=False,
    )
    bounds = render(page, chart)
    for navigated in [False, True]:
        if navigated:
            pointer(page, bounds)
            page.mouse.wheel(0, -150)
            page.wait_for_timeout(250)
        root = svg_root(page)
        text = [e for e in root.iter() if e.tag.endswith("text")]
        ticks = [e for e in text if e.text in labels]
        assert len(ticks) == 3
        names = [e for e in text if e.text in ["Adjacency", "Tree"]]
        assert len(names) == 2
        title = next(e for e in text if e.text == "Source group")
        # Native text bounds include rotation and the full long label, not just its anchor.
        box = page.evaluate("""() => {
            const views=api.debug.getViewRoot().getDescendants();
            const labelView=views.find(v=>v.spec.mark?.type==='text' && v.spec.encoding?.x?.field==='slot');
            const scale=labelView.getScaleResolution('x').getScale();
            return {bottom:labelView.coords.y+labelView.coords.height,
                    centers:[0,1,2].map(i=>labelView.coords.x+(scale(i)+scale.bandwidth()/2)*labelView.coords.width)};
        }""")
        assert all(position(e)[1] > bounds["y"] + bounds["height"] for e in ticks)
        assert position(title)[1] >= box["bottom"]
        assert min(position(e)[1] for e in names) > position(title)[1]
        np.testing.assert_allclose(
            [position(e)[0] for e in ticks], box["centers"], atol=0.6
        )
    combined = (
        (chart | chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    bounds = render(page, combined)
    before = point_coordinates(page)
    assert len(before) == 2
    pointer(page, bounds)
    page.mouse.wheel(0, -150)
    page.wait_for_timeout(250)
    after = point_coordinates(page)
    assert not np.array_equal(after[0], before[0])
    np.testing.assert_allclose(after[1], before[1], atol=0.1)
    text = [e.text for e in svg_root(page).iter() if e.tag.endswith("text")]
    assert text.count("Adjacency") == text.count("Tree") == 2


def test_hover_false_disables_matrix_and_tree_tooltips(page):
    bounds = render(
        page, gsc.pl.paga_adjacency(make_adjacency(), hover=False, show=False)
    )
    canvas = page.locator("canvas").first.bounding_box()
    for x, y in [(1 / 6, 5 / 6), (0.5, 1 / 6)]:
        hover_at(
            page,
            canvas["x"] + bounds["x"] + x * bounds["width"],
            canvas["y"] + bounds["y"] + y * bounds["height"],
        )
        assert not page.locator("table.attributes").is_visible()


@pytest.mark.reference
@pytest.mark.parametrize(
    "case",
    ["default", "constant", "missing", "diagonal", "negative", "singleton_empty"],
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_stripplot_matches_public_scanpy(page, tmp_path, case):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    plt.close("all")
    with mpl.rc_context({"figure.dpi": 100}):
        sc.pl.paga_adjacency(make_adjacency(case=case), as_heatmap=False, show=False)
        fig, ax = plt.gcf(), plt.gcf().axes[0]
        # Keep upstream positions and edge types, with the reviewed native paint.
        for artist in ax.collections:
            black = np.allclose(artist.get_facecolors()[0][:3], 0)
            artist.set_facecolor("#2563a6" if black else "#cbd5e1")
            artist.set_sizes([16 / (100 / 72) ** 2])
            artist.set_linewidths([0])
        fig.canvas.draw()
        bbox = ax.get_window_extent()
        positions = np.ma.concatenate([c.get_offsets() for c in ax.collections])
        colors = np.concatenate(
            [
                np.repeat(c.get_facecolors(), len(c.get_offsets()), axis=0)
                for c in ax.collections
            ]
        )
        visible = ~np.ma.getmaskarray(positions).any(axis=1)
        positions, colors = np.asarray(positions)[visible], colors[visible]
        domains = [ax.get_xlim(), ax.get_ylim()]
        reference = tmp_path / "reference.png"
        fig.savefig(reference, dpi=150)
        full = Image.open(reference).convert("RGB")
        expected = full.crop(
            (
                round(bbox.x0 * 1.5),
                round(full.height - bbox.y1 * 1.5),
                round(bbox.x1 * 1.5),
                round(full.height - bbox.y0 * 1.5),
            )
        )
        plt.close(fig)
    chart = gsc.pl.paga_adjacency(
        make_adjacency(case=case),
        as_heatmap=False,
        width=bbox.width,
        height=bbox.height,
        show=False,
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(bbox.width, abs=0.5)
    assert bounds["height"] == pytest.approx(bbox.height, abs=0.5)
    groups = point_coordinates(page)
    assert len(groups) == bool(len(positions))
    centers = groups[0] if len(positions) else np.empty((0, 2))
    normalized = (positions - np.array(domains)[:, 0]) / np.ptp(domains, axis=1)
    expected_centers = np.column_stack(
        [
            bounds["x"] + normalized[:, 0] * bounds["width"],
            bounds["y"] + (1 - normalized[:, 1]) * bounds["height"],
        ]
    )
    # SVG layout rounds fractional view edges to logical pixels.
    np.testing.assert_allclose(centers, expected_centers, atol=1)
    actual = panel_image(page, bounds)
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    last_colors = {
        tuple(xy): color for xy, color in zip(normalized, colors, strict=True)
    }
    for (x, y), color in last_colors.items():
        footprints = []
        for image in (actual, expected):
            cx, cy = int(x * image.width), int((1 - y) * image.height)
            patch = np.asarray(image)[cy - 5 : cy + 6, cx - 5 : cx + 6].astype(int)
            matches = np.max(np.abs(patch - color[:3] * 255), axis=2) < 20
            footprints.append(np.count_nonzero(matches))
        assert min(footprints) > 0 and abs(footprints[0] - footprints[1]) <= 8
    root = svg_root(page)
    assert not any(e.tag.endswith("linearGradient") for e in root.iter())
    assert any(e.tag.endswith("text") for e in root.iter())
    page.screenshot(path=str(tmp_path / "complete-stripplot.png"), full_page=True)
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "stripplot-overlay.png"
    )


@pytest.mark.parametrize("zoom", [True, "xy"])
@pytest.mark.parametrize("hover", [True, False])
def test_stripplot_hover_navigation_composition_and_html(page, tmp_path, zoom, hover):
    chart = gsc.pl.paga_adjacency(
        make_adjacency(),
        as_heatmap=False,
        hover=hover,
        zoom=zoom,
        width=360,
        height=280,
        show=False,
    )
    spec = chart.to_dict()
    for axis in ("x", "y"):
        spec["encoding"][axis]["scale"]["name"] = f"strip-{axis}"
    bounds = render(page, spec)
    domains = "['x','y'].map(a=>api.getScaleResolutionByName('strip-'+a).getDomain())"
    before = page.evaluate(domains)
    for value, target, kind in [(0.2, "1", "Adjacency"), (0.6, "2", "Tree")]:
        x = bounds["x"] + (0 - before[0][0]) / np.ptp(before[0]) * bounds["width"]
        y = (
            bounds["y"]
            + (1 - (value - before[1][0]) / np.ptp(before[1])) * bounds["height"]
        )
        hover_at(page, x, y)
        table = page.locator("table.attributes")
        if hover:
            table.wait_for(state="visible")
            values = [s.strip() for s in table.locator("td").all_text_contents()]
            assert values[:2] == ["0", target] and values[3] == kind
            assert float(values[2]) == pytest.approx(value)
        else:
            assert not table.is_visible()
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -150)
    page.wait_for_timeout(700)
    zoomed = page.evaluate(domains)
    assert (zoomed[0] != before[0]) is (zoom == "xy")
    assert np.ptp(zoomed[1]) < np.ptp(before[1])
    page.mouse.down()
    page.mouse.move(px + 10, py + 10, steps=5)
    page.mouse.up()
    page.wait_for_timeout(700)
    assert page.evaluate(domains)[1] != zoomed[1]
    combined = (
        (chart | chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    bounds = render(page, combined)
    before_points = point_coordinates(page)
    assert len(before_points) == 2
    pointer(page, bounds)
    page.mouse.wheel(0, -150)
    page.wait_for_timeout(700)
    after_points = point_coordinates(page)
    assert not np.array_equal(after_points[0], before_points[0])
    np.testing.assert_allclose(after_points[1], before_points[1], atol=0.1)
    output = tmp_path / "stripplot.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
