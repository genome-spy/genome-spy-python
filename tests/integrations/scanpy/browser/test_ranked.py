"""Observe complete ranking panels and reuse of native expression interactions."""

from io import BytesIO
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.browser.test_grid_interactions import pointer
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases
from tests.integrations.scanpy.helpers import points

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/ranked.json").read_text()
)["cases"]
STATISTICS = json.loads(
    (Path(__file__).parents[1] / "fixtures/ranked.json").read_text()
)["statistics"]


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", ranked_cases())
def test_complete_rank_panels_match_registered_labels_and_score_positions(
    page, tmp_path, reference_images, case
):
    family, args, options = ranked_cases()[case]
    reference = REFERENCE[case]["panels"]
    width, height = reference[0]["plot_size"]
    chart = getattr(gsc.pl, family)(
        make_ranked_adata(), *args, width=width, height=height, show=False, **options
    )
    render(page, chart)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    (tmp_path / f"ranked-{case}.svg").write_text(svg)
    root = ET.fromstring(svg)
    texts = [e for e in root.iter() if e.tag.endswith("text")]
    label_names = {label["text"] for panel in reference for label in panel["labels"]}
    labels = [e for e in texts if e.text in label_names]
    assert len(labels) == sum(len(panel["labels"]) for panel in reference)
    image = Image.open(BytesIO(page.screenshot(full_page=True))).convert("RGBA")
    canvas = page.locator("canvas").first.bounding_box()
    image.save(tmp_path / f"ranked-{case}.png")
    for i, panel in enumerate(reference):
        bounds = page.evaluate(
            "i => api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i
        )
        for label in panel["labels"]:
            x, y = label["position"]
            x0, x1 = panel["x_domain"]
            y0, y1 = panel["y_domain"]
            expected = [
                bounds["x"] + (x - x0) / (x1 - x0) * bounds["width"],
                bounds["y"] + (y1 - y) / (y1 - y0) * bounds["height"],
            ]
            positions = [
                list(
                    map(
                        float,
                        re.search(
                            r"translate\(([-\d.e]+)[ ,]+([-\d.e]+)",
                            e.get("transform", ""),
                        ).groups(),
                    )
                )
                for e in labels
                if e.text == label["text"]
            ]
            # Viewport origins and extents each snap to physical pixels.
            assert any(np.allclose(pos, expected, atol=2 / 1.5) for pos in positions), (
                label,
                positions,
                expected,
            )
        for text in (panel["title"], panel["xlabel"], panel["ylabel"]):
            if text:
                assert text in [e.text for e in texts]
        left, top = canvas["x"] + bounds["x"], canvas["y"] + bounds["y"]
        crop = image.crop(
            tuple(round(v * 1.5) for v in (left, top, left + width, top + height))
        )
        expected_image = Image.open(
            reference_images("ranked") / f"ranked-{case}-panel-{i}.png"
        ).convert("RGBA")
        assert (
            abs(crop.width - expected_image.width) <= 1
            and abs(crop.height - expected_image.height) <= 1
        )
        # Register the plot origins without fitting or resampling either image.
        size = (
            max(crop.width, expected_image.width),
            max(crop.height, expected_image.height),
        )
        layers = [Image.new("RGBA", size, "white") for _ in range(2)]
        layers[0].paste(crop, (0, 0))
        layers[1].paste(expected_image, (0, 0))
        Image.blend(*layers, 0.5).save(tmp_path / f"ranked-{case}-overlay-{i}.png")


def test_rank_label_native_hover_and_offline_html(page, tmp_path):
    chart = gsc.pl.rank_genes_groups(
        make_ranked_adata(), groups="C", n_genes=3, show=False
    )
    bounds = render(page, chart)
    px, py = pointer(page, bounds, x=(1 + 0.9) / 3.8, y=(4.9 - 2) / 3.9)
    page.mouse.move(px - 2, py - 4)
    page.wait_for_timeout(450)
    for dx, dy in [(0, -4), (0, -8), (2, -4)]:
        page.mouse.move(px + dx, py + dy)
        page.wait_for_timeout(100)
        if page.locator("table.attributes").is_visible():
            break
    assert [
        text.strip() for text in page.locator("table.attributes td").all_text_contents()
    ] == [
        "g1",
        "2.000",
        "1",
    ]
    path = tmp_path / "ranking.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("family", ["dotplot", "matrixplot", "heatmap"])
def test_ranked_expression_uses_existing_y_navigation_and_guides(page, family):
    options = {"highlight": True} if family == "dotplot" else {"show_values": True}
    chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
        make_ranked_adata(),
        n_genes=2,
        zoom=True,
        width=360,
        height=240,
        show=False,
        **options,
    )
    bounds = render(page, chart)
    before = page.evaluate(
        "['grid_x_step','grid_y_step'].map(n=>api.getParam(n).getValue())"
    )
    pointer(page, bounds)
    page.mouse.wheel(0, -260)
    page.wait_for_timeout(700)
    after = page.evaluate(
        "['grid_x_step','grid_y_step'].map(n=>api.getParam(n).getValue())"
    )
    assert after[0] == before[0] and after[1] > before[1]
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert all(text in svg for text in ("g1", "g2", "g3", "g4"))


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_statistic_colors_labels_and_complete_guides_match_scanpy(
    page, family, tmp_path, reference_images
):
    reference = STATISTICS[family]
    chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
        make_ranked_adata(),
        groups=["A", "C"],
        n_genes=2,
        values_to_plot=reference["metric"],
        cmap="viridis",
        dendrogram=False,
        width=reference["plot_size"][0],
        height=reference["plot_size"][1],
        show=False,
    )
    spec = chart.to_dict()
    mark = points(spec)
    np.testing.assert_allclose(
        mark["encoding"]["color"]["scale"]["domain"], reference["color_domain"]
    )
    assert mark["encoding"]["color"]["legend"]["title"] == reference["legend_title"]
    bounds = render(page, chart)
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
    expected = Image.open(
        reference_images("ranked") / f"ranked-statistic-{family}-panel.png"
    ).convert("RGB")
    assert (
        abs(actual.width - expected.width) <= 2
        and abs(actual.height - expected.height) <= 2
    )
    # Sample each mark center using the upstream plot domains at export DPI.
    for row in next(rows for rows in spec["datasets"].values() if "_mean" in rows[0]):
        x, y = row["_x"] + 0.5, row["_y"] + 0.5
        x0, x1 = reference["x_domain"]
        y1, y0 = reference["y_domain"]
        px, py = (
            round((x - x0) / (x1 - x0) * actual.width),
            round((y - y0) / (y1 - y0) * actual.height),
        )
        assert (
            np.abs(
                np.asarray(actual)[py, px].astype(int)
                - np.asarray(expected)[py, px].astype(int)
            ).max()
            <= 12
        ), row
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    texts = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
    for label in (
        reference["x_labels"] + reference["y_labels"] + [reference["legend_title"]]
    ):
        assert label in texts
    page.screenshot(
        path=str(tmp_path / f"statistic-{family}-complete.png"), full_page=True
    )
    extent = (
        0,
        0,
        min(actual.width, expected.width),
        min(actual.height, expected.height),
    )
    Image.blend(actual.crop(extent), expected.crop(extent), 0.5).save(
        tmp_path / f"statistic-{family}-overlay.png"
    )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_statistic_hover_zoom_and_offline_delivery(page, family, tmp_path):
    options = {"highlight": True} if family == "dotplot" else {"show_values": True}
    chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
        make_ranked_adata(),
        var_names=["g2"],
        values_to_plot="scores",
        dendrogram=False,
        zoom=True,
        width=300,
        height=320,
        show=False,
        **options,
    )
    bounds = render(page, chart)
    x = 0.5
    y = 1 / 5 if family == "dotplot" else 1 / 8
    px, py = pointer(page, bounds, x=x, y=y)
    page.mouse.move(px - 2, py - 2)
    page.wait_for_timeout(450)
    page.mouse.move(px, py)
    page.locator("table.attributes").wait_for(state="visible")
    values = [
        s.strip() for s in page.locator("table.attributes td").all_text_contents()
    ]
    assert values[:3] == (
        ["g2", "C", "4.000"] if family == "dotplot" else ["g2", "A", "6.000"]
    )
    if family == "dotplot":
        assert float(values[-1]) == 100
    before = page.evaluate(
        "['grid_x_step','grid_y_step'].map(n=>api.getParam(n).getValue())"
    )
    pointer(page, bounds)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(500)
    after = page.evaluate(
        "['grid_x_step','grid_y_step'].map(n=>api.getParam(n).getValue())"
    )
    assert after[0] == before[0] and after[1] > before[1]
    path = tmp_path / f"statistic-{family}.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
