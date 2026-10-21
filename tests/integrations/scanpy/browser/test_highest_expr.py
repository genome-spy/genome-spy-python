"""Observe native box geometry, whole charts, hover, zoom and offline delivery."""

from io import BytesIO
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.highest_expr_fixture import make_counts


@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_complete_boxes_match_scanpy_quartiles_whiskers_axes_and_pixels(
    page, tmp_path, log
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_counts()
    with (
        plt.rc_context(plt.rcParamsDefault),
        pytest.warns(UserWarning, match="zero counts"),
    ):
        ax = sc.pl.highest_expr_genes(a, n_top=5, log=log, show=False)
    ax.figure.canvas.draw()
    bounds = ax.get_window_extent()
    reference = tmp_path / "reference.png"
    ax.figure.savefig(
        reference,
        dpi=150,
        bbox_inches=bounds.transformed(ax.figure.dpi_scale_trans.inverted()),
        pad_inches=0,
    )
    vertices = [p.get_path().vertices for p in ax.patches]
    labels = [t.get_text() for t in ax.get_yticklabels()]
    with pytest.warns(UserWarning, match="zero counts"):
        chart = gsc.pl.highest_expr_genes(
            a, n_top=5, log=log, width=bounds.width, height=bounds.height, show=False
        )
    actual_bounds = render(page, chart)
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    root = ET.fromstring(svg)
    text = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert "% of total counts" in text and all(
        text.count(label) == 1 for label in labels
    )
    (tmp_path / "native.svg").write_text(svg)
    boxes = [
        e
        for group in root.iter()
        if group.get("data-mark-type") == "rect"
        for e in group
    ]
    # Every quartile rectangle must retain the reference width and row position.
    assert len(boxes) == 5
    assert [e.get("fill") for e in boxes] == [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
    ]
    for row, (element, expected) in enumerate(zip(boxes, vertices, strict=True)):
        x1, x2 = expected[:, 0].min(), expected[:, 0].max()
        lo, hi = ax.get_xlim()
        if log:
            x1, x2, lo, hi = np.log10([x1, x2, lo, hi])
        np.testing.assert_allclose(
            [float(element.get("x")), float(element.get("width"))],
            [
                actual_bounds["x"] + (x1 - lo) / (hi - lo) * actual_bounds["width"],
                max(0.5, (x2 - x1) / (hi - lo) * actual_bounds["width"]),
            ],
            atol=0.3,
        )
        np.testing.assert_allclose(
            [float(element.get("y")), float(element.get("height"))],
            [
                actual_bounds["y"] + (row + 0.1) * actual_bounds["height"] / 5,
                0.8 * actual_bounds["height"] / 5,
            ],
            atol=0.3,
        )
    canvas = page.locator("canvas").first.bounding_box()
    crop = page.screenshot(
        clip={
            "x": canvas["x"] + actual_bounds["x"],
            "y": canvas["y"] + actual_bounds["y"],
            "width": actual_bounds["width"],
            "height": actual_bounds["height"],
        }
    )
    actual = Image.open(BytesIO(crop)).convert("RGB")
    actual.save(tmp_path / "native.png")
    expected = Image.open(reference).convert("RGB").resize(actual.size)
    Image.blend(expected, actual, 0.5).save(tmp_path / "registered-overlay.png")
    page.screenshot(path=str(tmp_path / "complete-chart.png"))
    difference = np.abs(
        np.asarray(actual).astype(float) - np.asarray(expected).astype(float)
    )
    # Independent browser rasterization may differ along thin strokes, not box interiors.
    assert difference.mean() < 10
    assert (difference.max(axis=2) > 80).mean() < 0.06
    plt.close(ax.figure)


def test_box_and_outlier_hover_zoom_and_offline_html(page, tmp_path):
    with pytest.warns(UserWarning, match="zero counts"):
        chart = gsc.pl.highest_expr_genes(
            make_counts(), n_top=5, zoom=True, width=400, height=300, show=False
        )
    bounds = render(page, chart)
    domain = chart.to_dict()["layer"][0]["encoding"]["x"]["scale"]["domain"]
    move_to(page, bounds, 2, 4.5, domain, [5, 0], "gene-0")
    page.get_by_text("Median (%)", exact=True).wait_for(state="visible")
    assert [t.strip() for t in page.locator("table.attributes td").all_text_contents()][
        :2
    ] == ["gene-0", "gene-0"]
    move_to(page, bounds, 0, 0.5, domain, [5, 0], "0")
    page.get_by_text("Cell ID", exact=True).wait_for(state="visible")
    assert [
        t.strip() for t in page.locator("table.attributes td").all_text_contents()
    ] == ["gene-4", "0", "0", "0.000"]
    before = page.evaluate(
        "api.getScaleResolutionByName('highest-expression-x').getDomain()"
    )
    page.mouse.wheel(0, -180)
    page.wait_for_function(
        "before=>{const d=api.getScaleResolutionByName('highest-expression-x').getDomain();return d[1]-d[0]<before[1]-before[0];}",
        arg=before,
    )
    path = tmp_path / "highest.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
