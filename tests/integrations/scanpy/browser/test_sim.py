"""Complete simulation guides, registered marks and observed native navigation."""

from io import BytesIO
import warnings

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_heatmap import hover_at, render
from tests.integrations.scanpy.browser.test_grid_interactions import (
    svg_root,
    position,
    value_texts,
)
from tests.integrations.scanpy.browser.test_timeseries import point_coordinates
from tests.integrations.scanpy.sim_fixture import make_sim, sim_cases
from tests.integrations.scanpy.helpers import leaf_marks


def point_spacing(coordinates):
    """Measure adjacent sample and paired-value spacing despite viewport culling."""
    xs = np.unique(coordinates[:, 0])
    paired = [np.ptp(coordinates[coordinates[:, 0] == x, 1]) for x in xs]
    return np.median(np.diff(xs)), np.median([d for d in paired if d > 0])


@pytest.mark.parametrize("case", sim_cases())
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_simulation_matches_scanpy_ticks_boundaries_and_paint(
    page, tmp_path, case
):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    adata, options = make_sim(), sim_cases()[case]
    state = np.random.get_state()
    try:
        with mpl.rc_context({"figure.dpi": 100}), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sc.pl.sim(adata, show=False, **options)
            fig, ax = plt.gcf(), plt.gcf().axes[0]
            fig.canvas.draw()
            bbox = ax.get_window_extent()
            limits = [ax.get_xlim(), ax.get_ylim()]
            ticks = list(
                zip(ax.get_xticks(), [t.get_text() for t in ax.get_xticklabels()])
            )
            heatmap = bool(ax.images)
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
            plt.close(fig)
    finally:
        np.random.set_state(state)
    chart = gsc.pl.sim(
        adata, width=bbox.width, height=bbox.height, show=False, **options
    )
    bounds = render(page, chart)
    root = svg_root(page)
    (tmp_path / "native.svg").write_text(
        page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    )
    for axis, extent in (("width", bbox.width), ("height", bbox.height)):
        assert bounds[axis] == pytest.approx(extent, abs=0.6)
    texts = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert "A" in texts and "B" in texts
    boundaries = np.arange(
        options.get("tmax_realization", 3), 7, options.get("tmax_realization", 3)
    )
    rules = [
        e
        for e in root.iter()
        if e.get("data-mark-type") == "rule" and e.get("stroke-dasharray")
    ]
    lines = list(rules[0]) if rules else []
    assert len(lines) == len(boundaries)
    for line, boundary in zip(lines, boundaries, strict=True):
        assert float(line.get("x1")) == pytest.approx(
            bounds["x"]
            + (boundary - limits[0][0]) / np.ptp(limits[0]) * bounds["width"],
            abs=1,
        )
    if not heatmap:
        assert (
            "index (arbitrary order)" if options.get("shuffle") else "realizations"
        ) in texts
    if not options.get("shuffle"):
        labels = [
            e
            for e in root.iter()
            if e.tag.endswith("text")
            and e.text in {label for _, label in ticks}
            and position(e)[1] > bounds["y"] + bounds["height"]
        ]
        assert len(labels) == len(ticks), [
            (e.text, position(e)) for e in root.iter() if e.tag.endswith("text")
        ]
        for x, label in ticks:
            element = next(e for e in labels if e.text == label)
            assert position(element)[0] == pytest.approx(
                bounds["x"] + (x - limits[0][0]) / np.ptp(limits[0]) * bounds["width"],
                abs=1,
            )
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
    a, b = np.asarray(actual).astype(int), np.asarray(expected).astype(int)
    if heatmap:
        for fx in np.linspace(0.07, 0.93, 12):
            for fy in (0.2, 0.8):
                # Stay away from realization rules and tile borders.
                x = limits[0][0] + fx * np.ptp(limits[0])
                if (
                    min(
                        abs(x - h)
                        for h in [
                            0.5,
                            1.5,
                            2.5,
                            3.5,
                            4.5,
                            5.5,
                            *np.arange(
                                options.get("tmax_realization", 3),
                                7,
                                options.get("tmax_realization", 3),
                            ),
                        ]
                    )
                    < 0.08
                ):
                    continue
                np.testing.assert_allclose(
                    a[int(fy * actual.height), int(fx * actual.width)],
                    b[int(fy * expected.height), int(fx * expected.width)],
                    atol=12,
                )
    else:
        spec = chart.to_dict()
        point = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
        for row in spec["datasets"][point["data"]["name"]]:
            # Whole-pixel native dashes can cover a different part of a tiny dot.
            if any(row["_time"] == boundary for boundary in boundaries):
                continue
            fx = (row["_time"] - limits[0][0]) / np.ptp(limits[0])
            fy = 1 - (row["_value"] - limits[1][0]) / np.ptp(limits[1])
            if not (0.02 < fx < 0.98 and 0.02 < fy < 0.98):
                continue
            ap = a[
                int(fy * actual.height) - 5 : int(fy * actual.height) + 6,
                int(fx * actual.width) - 5 : int(fx * actual.width) + 6,
            ]
            bp = b[
                int(fy * expected.height) - 5 : int(fy * expected.height) + 6,
                int(fx * expected.width) - 5 : int(fx * expected.width) + 6,
            ]
            assert (
                abs(
                    np.count_nonzero(np.min(ap, axis=2) < 220)
                    - np.count_nonzero(np.min(bp, axis=2) < 220)
                )
                <= 15
            )
            assert np.min(np.linalg.norm(ap.reshape(-1, 3) - bp[5, 5], axis=1)) < 35
    actual.save(tmp_path / "native-panel.png")
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / "registered-overlay.png"
    )
    page.screenshot(path=str(tmp_path / "complete.png"), full_page=True)


@pytest.mark.parametrize("mode", ["points", "heatmap", "shuffle"])
def test_hover_navigation_realization_labels_and_offline_delivery(page, tmp_path, mode):
    adata = make_sim()
    adata = type(adata)(
        np.arange(60, dtype=float).reshape(30, 2),
        var=adata.var.copy(),
        uns={"tmax_write": 10},
    )
    chart = gsc.pl.sim(
        adata,
        as_heatmap=mode == "heatmap",
        shuffle=mode == "shuffle",
        marker="o",
        zoom="xy",
        show_values=mode == "heatmap",
        width=500,
        height=300,
        show=False,
    )
    spec = chart.to_dict()
    if mode == "heatmap":
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"sim-{axis}"
    bounds = render(page, spec)
    mark = next(
        m
        for m in leaf_marks(spec)
        if m["mark"]["type"] == ("rect" if mode == "heatmap" else "point")
    )
    if mode == "heatmap":
        domains = [spec["scales"][axis]["domain"] for axis in ("x", "y")]
        tx, ty = 10, 0.2
        expected = ["A", "10", "20.00"]
    else:
        domains = [mark["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
        rows = spec["datasets"][mark["data"]["name"]]
        sample = next(r for r in rows if r["_sample"] == 10 and r["_series"] == "A")
        tx, ty = sample["_time"], sample["_value"]
        expected = ["A", "10", "10.00", f"{ty:.2f}"]
    x = bounds["x"] + (tx - domains[0][0]) / np.ptp(domains[0]) * bounds["width"]
    y = bounds["y"] + (1 - (ty - domains[1][0]) / np.ptp(domains[1])) * bounds["height"]
    hover_at(page, x, y)
    page.locator("table.attributes").wait_for(state="visible")
    assert [
        s.strip() for s in page.locator("table.attributes td").all_text_contents()
    ] == expected
    before = point_coordinates(page)[0] if mode != "heatmap" else None
    page.mouse.wheel(0, -500)
    page.wait_for_timeout(700)
    before_pan = (
        page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
        if mode == "heatmap"
        else point_coordinates(page)[0]
    )
    canvas = page.locator("canvas").first.bounding_box()
    page.mouse.move(canvas["x"] + x, canvas["y"] + y)
    page.mouse.down()
    page.mouse.move(canvas["x"] + x + 20, canvas["y"] + y + 15, steps=5)
    page.mouse.up()
    page.wait_for_timeout(300)
    after = svg_root(page)
    if mode == "heatmap":
        assert (
            page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
            != before_pan
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('sim-x').getDomain()")
            != domains[0]
        )
        assert (
            page.evaluate("api.getScaleResolutionByName('sim-y').getDomain()")
            != domains[1]
        )
        assert value_texts(after)
    else:
        coordinates = point_coordinates(page)[0]
        assert not np.array_equal(coordinates, before_pan)
        assert all(
            a > b
            for a, b in zip(
                point_spacing(coordinates), point_spacing(before), strict=True
            )
        )
    if mode != "shuffle":
        labels = [
            e
            for e in after.iter()
            if e.tag.endswith("text")
            and e.text in {"1", "2", "3"}
            and position(e)[1] > bounds["y"] + bounds["height"]
        ]
        assert labels
        rules = [
            line
            for group in after.iter()
            if group.get("data-mark-type") == "rule" and group.get("stroke-dasharray")
            for line in group
        ]
        for label in labels:
            assert any(
                abs(position(label)[0] - float(line.get("x1"))) <= 1 for line in rules
            )
    path = tmp_path / "simulation.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
