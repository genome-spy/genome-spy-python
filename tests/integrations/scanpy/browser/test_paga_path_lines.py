"""Observed native PAGA line geometry, guides, hover, navigation and HTML."""

import numpy as np
import pytest
from PIL import Image
from scipy.ndimage import distance_transform_edt

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import hover_at, pointer, svg_root
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.paga_fixtures import make_path


def line_groups(root, panel="panel-0"):
    """Read the plotted rules inside one panel, excluding guides and axes."""
    view = next(e for e in root.iter() if e.get("data-name") == panel)
    return [e for e in view.iter() if e.get("data-mark-type") == "rule"]


@pytest.mark.reference
@pytest.mark.parametrize(
    "options,case",
    [({}, "default"), ({"n_avg": 2, "xlim": (1, None)}, "default"), ({}, "missing")],
)
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_registered_lines_preserve_values_gaps_colors_and_native_legend(
    page, tmp_path, options, case
):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_path(case=case)
    with mpl.rc_context({"figure.dpi": 100}):
        fig, ax = plt.subplots(figsize=(8, 4))
        sc.pl.paga_path(
            a,
            ["beta", "alpha"],
            ["g1", "g2"],
            as_heatmap=False,
            show=False,
            ax=ax,
            **options,
        )
        fig.canvas.draw()
        box = ax.get_window_extent()
        expected = [line.get_xydata().copy() for line in ax.lines]
        colors = [mpl.colors.to_hex(line.get_color()) for line in ax.lines]
        domains = ax.get_xlim(), ax.get_ylim()
        reference = tmp_path / "scanpy.png"
        fig.savefig(reference, dpi=150)
        image = Image.open(reference).convert("RGB")
        target = image.crop(
            (
                round(box.x0 * 1.5),
                round(image.height - box.y1 * 1.5),
                round(box.x1 * 1.5),
                round(image.height - box.y0 * 1.5),
            )
        )
        plt.close(fig)
    chart = gsc.pl.paga_path(
        a,
        ["beta", "alpha"],
        ["g1", "g2"],
        as_heatmap=False,
        width=box.width,
        height=box.height,
        show=False,
        **options,
    )
    bounds = render(page, chart)
    assert bounds["width"] == pytest.approx(box.width, abs=0.5)
    assert bounds["height"] == pytest.approx(box.height, abs=0.5)
    root = svg_root(page)
    groups = line_groups(root)
    assert len(groups) == 1 and groups[0].get("stroke-linecap") == "round"
    lines = list(groups[0])
    expected_segments = []
    for color, points in zip(colors, expected, strict=True):
        for start, end in zip(points[:-1], points[1:], strict=True):
            if np.isfinite([start, end]).all():
                expected_segments.append((color, start, end))
    assert len(lines) == len(expected_segments)
    for line, (color, start, end) in zip(lines, expected_segments, strict=True):
        assert line.get("stroke") == color
        projected = []
        for point in (start, end):
            projected.extend(
                [
                    bounds["x"]
                    + bounds["width"] * (point[0] - domains[0][0]) / np.ptp(domains[0]),
                    bounds["y"]
                    + bounds["height"]
                    * (1 - (point[1] - domains[1][0]) / np.ptp(domains[1])),
                ]
            )
        np.testing.assert_allclose(
            [float(line.get(k)) for k in ("x1", "y1", "x2", "y2")], projected, atol=0.5
        )
    texts = {e.text for e in root.iter() if e.tag.endswith("text")}
    assert {"g1", "g2", "cluster"} <= texts
    legend = next(
        e for e in root.iter() if e.get("data-view-path", "").endswith("/legend_bottom")
    )
    assert any(e.get("data-mark-type") == "point" for e in legend.iter())
    actual = panel_image(page, bounds)
    actual = actual.resize(target.size)
    if case == "default" and not options:
        # The later orange profile must cover the blue profile at their crossing.
        crossing = (6 / 13, 68 / 13)
        px = round((crossing[0] - domains[0][0]) / np.ptp(domains[0]) * target.width)
        py = round(
            (1 - (crossing[1] - domains[1][0]) / np.ptp(domains[1])) * target.height
        )
        for image in (actual, target):
            red, green, blue = image.getpixel((px, py))
            assert red > 180 and 80 < green < 180 and blue < 90
    # Compare line footprints within two logical pixels, allowing native caps and rasterization.
    masks = [(np.asarray(v).min(axis=2) < 235)[5:-5, 5:-5] for v in (actual, target)]
    assert all(mask.any() for mask in masks)
    for own, other in (masks, masks[::-1]):
        distances = distance_transform_edt(~other)[own]
        assert np.quantile(distances, 0.999) <= 3
    actual.save(tmp_path / "native.png")


@pytest.mark.parametrize("zoom,hover", [(True, True), ("xy", False)])
def test_line_hover_navigation_independent_composition_and_offline_html(
    page, tmp_path, zoom, hover
):
    chart = gsc.pl.paga_path(
        make_path(),
        ["beta", "alpha"],
        ["g1", "g2"],
        as_heatmap=False,
        width=400,
        height=220,
        zoom=zoom,
        hover=hover,
        show=False,
    )
    spec = chart.to_dict()
    panel = spec["spec"]
    for axis in ("x", "y"):
        panel["encoding"][axis]["scale"]["name"] = f"line-{axis}"
    bounds = render(page, spec)
    xdomain = panel["encoding"]["x"]["scale"]["domain"]
    ydomain = panel["encoding"]["y"]["scale"]["domain"]
    x = bounds["x"] + bounds["width"] * (0.5 - xdomain[0]) / np.ptp(xdomain)
    y = bounds["y"] + bounds["height"] * (1 - (5 - ydomain[0]) / np.ptp(ydomain))
    hover_at(page, x, y)
    tooltip = page.locator("table.attributes")
    if hover:
        assert tooltip.get_by_text("g1", exact=True).is_visible()
        assert tooltip.get_by_text("Next value", exact=True).is_visible()
    else:
        assert not tooltip.is_visible()
    before = page.evaluate(
        "['x','y'].map(a=>api.getScaleResolutionByName('line-'+a).getDomain())"
    )
    pointer(page, bounds)
    page.mouse.wheel(0, -180)
    page.wait_for_timeout(500)
    after = page.evaluate(
        "['x','y'].map(a=>api.getScaleResolutionByName('line-'+a).getDomain())"
    )
    assert (before[0] != after[0]) is (zoom == "xy")
    assert before[1] != after[1]
    combined = (
        (chart | chart)
        .resolve_scale(default="independent")
        .resolve_legend(default="independent")
    )
    bounds = render(page, combined)

    def geometry():
        """Return both panels' rule endpoints to distinguish linked and independent navigation."""
        root = svg_root(page)
        return [
            [
                dict(line.attrib)
                for group in line_groups(root, f"panel-{i}")
                for line in group
            ]
            for i in range(2)
        ]

    before = geometry()
    px, py = pointer(page, bounds)
    page.mouse.wheel(0, -120)
    page.wait_for_timeout(500)
    after = geometry()
    assert before[0] != after[0] and before[1] == after[1]
    page.mouse.down()
    page.mouse.move(px + 12, py + 8, steps=5)
    page.mouse.up()
    page.wait_for_timeout(500)
    assert geometry()[0] != after[0] and geometry()[1] == after[1]
    output = tmp_path / "lines.html"
    combined.save(output, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(output.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("options", [{"keys": ["g1"]}, {"n_avg": 4}, {"xlim": (3, 1)}])
def test_single_key_single_sample_and_empty_crop_render_natively(page, options):
    options = options.copy()
    keys = options.pop("keys", ["g1", "g2"])
    chart = gsc.pl.paga_path(
        make_path(), ["beta", "alpha"], keys, as_heatmap=False, show=False, **options
    )
    render(page, chart)
    root = svg_root(page)
    texts = {e.text for e in root.iter() if e.tag.endswith("text")}
    if len(keys) == 1:
        assert "g1" in texts
    else:
        assert {"g1", "g2"} <= texts
