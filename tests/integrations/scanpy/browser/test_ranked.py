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

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/ranked.json").read_text()
)["cases"]


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
