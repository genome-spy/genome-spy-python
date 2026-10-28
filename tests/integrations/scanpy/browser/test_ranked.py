"""Observe complete ranking panels and reuse of native expression interactions."""

import json
import re
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import pointer
from tests.integrations.scanpy.browser.rendering import panel_image, render
from tests.integrations.scanpy.helpers import index_position, points, scanpy_rank_labels
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/ranked.json").read_text()
)["cases"]
STATISTICS = json.loads(
    (Path(__file__).parents[1] / "fixtures/ranked.json").read_text()
)["statistics"]


@pytest.mark.reference
@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", ranked_cases())
def test_complete_rank_panels_match_registered_labels_and_score_positions(
    page, tmp_path, reference_images, case
):
    family, args, options = ranked_cases()[case]
    # Compare ties with local Scanpy; NumPy's tie order varies across processors.
    upstream = scanpy_rank_labels(family, make_ranked_adata(), *args, **options)
    reference = [
        {
            **panel,
            "labels": [
                {**label, "text": text, "position": [rank, score]}
                for label, (rank, text, score) in zip(
                    panel["labels"], labels, strict=True
                )
            ],
        }
        for panel, labels in zip(REFERENCE[case]["panels"], upstream, strict=True)
    ]
    width, height = reference[0]["plot_size"]
    chart = getattr(gsc.pl, family)(
        make_ranked_adata(), *args, width=width, height=height, show=False, **options
    )
    render(page, chart)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    (tmp_path / f"ranked-{case}.svg").write_text(svg)
    root = ET.fromstring(svg)
    texts = [e for e in root.iter() if e.tag.endswith("text")]
    label_names = {
        label["text"].replace("⋮", "...")
        for panel in reference
        for label in panel["labels"]
    }
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
            if family in ("pca_loadings", "pca_variance_ratio"):
                y1 += 0.3 * (y1 - y0)
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
                if e.text == label["text"].replace("⋮", "...")
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


@pytest.mark.reference
@pytest.mark.parametrize(
    "family,options,expected",
    [
        ("rank_genes_groups", {"groups": "C", "n_genes": 3}, ["g1", "2.000", "1"]),
        (
            "pca_loadings",
            {"components": "1", "n_points": 2, "include_lowest": False},
            ["g4", "6.000", "1"],
        ),
        ("pca_variance_ratio", {"n_pcs": 2}, ["PC4", "0.2000", "1"]),
        ("pca_variance_ratio", {"n_pcs": 3, "log": True}, ["PC4", "−1.609", "1"]),
    ],
)
def test_rank_label_native_hover_and_offline_html(
    page, tmp_path, family, options, expected
):
    if family == "pca_variance_ratio":
        labels = scanpy_rank_labels(family, make_ranked_adata(), **options)[0]
        expected = [labels[1][1], *expected[1:]]
    chart = getattr(gsc.pl, family)(make_ranked_adata(), show=False, **options)
    spec = chart.to_dict()
    x0, x1 = spec["encoding"]["x"]["scale"]["domain"]
    y0, y1 = spec["encoding"]["y"]["scale"]["domain"]
    record = spec["datasets"][spec["data"]["name"]][1]
    bounds = render(page, chart)
    px, py = pointer(
        page,
        bounds,
        x=(record["_rank"] - x0) / (x1 - x0),
        y=(y1 - record["_score"]) / (y1 - y0),
    )
    page.mouse.move(px - 2, py - 4)
    page.wait_for_timeout(450)
    for dx, dy in [(0, -4), (0, -8), (2, -4)]:
        page.mouse.move(px + dx, py + dy)
        page.wait_for_timeout(100)
        if page.locator("table.attributes").is_visible():
            break
    assert [
        text.strip() for text in page.locator("table.attributes td").all_text_contents()
    ] == expected
    path = tmp_path / "ranking.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize(
    "family,options,y",
    [
        (
            "pca_loadings",
            {"components": "1", "include_lowest": False, "n_points": 2},
            2.4 / 4.6,
        ),
        ("pca_variance_ratio", {"n_pcs": 2}, 0.22 / 0.23),
    ],
)
def test_pca_hover_can_be_disabled(page, family, options, y):
    chart = getattr(gsc.pl, family)(
        make_ranked_adata(), hover=False, show=False, **options
    )
    bounds = render(page, chart)
    px, py = pointer(page, bounds, x=1.9 / 3.8, y=y)
    page.mouse.move(px, py - 4)
    page.wait_for_timeout(450)
    assert not page.locator("table.attributes").is_visible()


@pytest.mark.parametrize(
    "family,options,panel_count",
    [
        ("pca_loadings", {"components": "1,2", "n_points": 20}, 2),
        ("pca_variance_ratio", {"n_pcs": 19}, 1),
        ("pca_variance_ratio", {"n_pcs": 19, "log": True}, 1),
    ],
)
def test_packaged_pca_labels_fit_inside_their_plot_axes(
    page, family, options, panel_count
):
    import scanpy as sc

    a = sc.datasets.pbmc68k_reduced()
    chart = getattr(gsc.pl, family)(
        a[:, a.var["highly_variable"]], show=False, **options
    )
    spec = chart.to_dict()
    names = {
        r["_label"]
        for table in spec["datasets"].values()
        for r in table
        if r["_label"] != "⋮"
    }
    render(page, chart)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    boxes = page.evaluate(
        """({svg,names}) => {
        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;
        root.style.cssText='position:absolute;left:0;top:0;visibility:hidden';
        document.body.append(root);
        const boxes=[...root.querySelectorAll('text')].filter(n=>names.includes(n.textContent)).map(n=>{
            const r=n.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};
        });
        root.remove(); return boxes;
    }""",
        {"svg": svg, "names": list(names)},
    )
    size = page.evaluate("api.getLogicalCanvasSize()")
    assert len(boxes) == 20 * panel_count
    assert all(
        0 <= b["y"] and b["y"] + b["height"] <= size["height"] + 1 for b in boxes
    )
    assert all(0 <= b["x"] and b["x"] + b["width"] <= size["width"] + 1 for b in boxes)
    panels = [
        page.evaluate("i => api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i)
        for i in range(panel_count)
    ]
    for box in boxes:
        panel = next(p for p in panels if p["x"] - 1 <= box["x"] <= p["x"] + p["width"])
        assert box["y"] >= panel["y"] - 1
        assert box["y"] + box["height"] <= panel["y"] + panel["height"] + 1
    assert "?" not in [
        e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")
    ]


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
    bounds = render(page, chart, scale_prefix=family)
    domains = f"['x','y'].map(axis=>api.getScaleResolutionByName('{family}-'+axis).getDomain())"
    before = page.evaluate(domains)
    pointer(page, bounds)
    page.mouse.wheel(0, -260)
    page.wait_for_timeout(700)
    after = page.evaluate(domains)
    assert after[0] == before[0]
    assert after[1][1] - after[1][0] < before[1][1] - before[1][0]
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    assert all(text in svg for text in ("g1", "g2", "g3", "g4"))


@pytest.mark.reference
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
    actual = panel_image(page, bounds)
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
        original = (px, py)
        xscale, yscale = spec["scales"]["x"], spec["scales"]["y"]
        px = round(
            index_position(
                x,
                xscale["domain"][1] + 1,
                xscale["paddingOuter"],
                bounds["width"],
                xscale["gapPositions"],
            )
            * 1.5
        )
        py = round(
            index_position(
                y,
                yscale["domain"][1] + 1,
                yscale["paddingOuter"],
                bounds["height"],
                yscale["gapPositions"],
            )
            * 1.5
        )
        assert (
            np.abs(
                np.asarray(actual)[py, px].astype(int)
                - np.asarray(expected)[original[1], original[0]].astype(int)
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
    bounds = render(page, chart, scale_prefix=family)
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
    domains = f"['x','y'].map(axis=>api.getScaleResolutionByName('{family}-'+axis).getDomain())"
    before = page.evaluate(domains)
    pointer(page, bounds)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(500)
    after = page.evaluate(domains)
    assert after[0] == before[0]
    assert after[1][1] - after[1][0] < before[1][1] - before[1][0]
    path = tmp_path / f"statistic-{family}.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
