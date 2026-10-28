"""Observe native brackets, annotation spans, graph labels and path guides."""

from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import hover_at, svg_root
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.expression_fixtures import make_heatmap_adata
from tests.integrations.scanpy.paga_fixtures import POSITIONS, make_paga
from tests.integrations.scanpy.paga_fixtures import make_path


@pytest.mark.parametrize(
    "family,swapped",
    [
        ("dotplot", False),
        ("dotplot", True),
        ("matrixplot", False),
        ("matrixplot", True),
        ("heatmap", False),
    ],
)
def test_marker_brackets_clear_the_matrix_in_both_orientations(page, family, swapped):
    chart = getattr(gsc.pl, family)(
        make_heatmap_adata(),
        {"First": ["g1", "g2"], "Last": ["g3"]},
        "group",
        swap_axes=swapped,
        width=380,
        height=260,
        show=False,
    )
    bounds = render(page, chart)
    view = next(
        e for e in svg_root(page).iter() if e.get("data-name") == f"{family}-brackets"
    )
    lines = [e for e in view.iter() if e.tag.endswith("line")]
    assert len(lines) == 6
    for line in lines[:2]:
        if swapped:
            assert float(line.get("x1")) == pytest.approx(
                bounds["x"] + bounds["width"] + 10, abs=1
            )
        else:
            assert float(line.get("y1")) == pytest.approx(bounds["y"] - 10, abs=1)
    axis = "x" if swapped else "y"
    assert all(
        abs(float(e.get(f"{axis}2")) - float(e.get(f"{axis}1")))
        == pytest.approx(10, abs=0.1)
        for e in lines[2:]
    )
    assert {e.text for e in view.iter() if e.tag.endswith("text")} == {"First", "Last"}


@pytest.mark.parametrize("page", [1.5], indirect=True)
def test_dense_category_strips_have_no_outline_and_keep_hover(page):
    a = AnnData(
        np.zeros((700, 2)),
        obs=pd.DataFrame(
            {"group": pd.Categorical(["A"] * 350 + ["B"] * 350)},
            index=[f"cell-{i}" for i in range(700)],
        ),
    )
    a.uns["group_colors"] = ["red", "blue"]
    chart = gsc.pl.clustermap(
        a,
        obs_keys="group",
        row_cluster=False,
        col_cluster=False,
        xticklabels=False,
        yticklabels=False,
        width=240,
        height=350,
        zoom=True,
        show=False,
    )
    render(page, chart)
    bounds = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'clustermap-left-colors-0'})"
    )
    view = next(
        e
        for e in svg_root(page).iter()
        if e.get("data-name") == "clustermap-left-colors-0"
    )
    group = next(e for e in view.iter() if e.get("data-mark-type") == "rect")
    assert len(group) == 700 and group.get("stroke") == "none"
    assert float(group.get("stroke-width")) == 0
    pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
    x = round((bounds["x"] + bounds["width"] / 2) * 1.5)
    for low, high, color, label in (
        (0.05, 0.45, [255, 0, 0], "A"),
        (0.55, 0.95, [0, 0, 255], "B"),
    ):
        strip = pixels[
            round((bounds["y"] + bounds["height"] * low) * 1.5) : round(
                (bounds["y"] + bounds["height"] * high) * 1.5
            ),
            x,
        ]
        assert np.abs(strip.astype(int) - color).max() <= 3
        hover_at(
            page,
            bounds["x"] + bounds["width"] / 2,
            bounds["y"] + bounds["height"] * (low + high) / 2,
        )
        assert (
            page.locator("table.attributes").get_by_text(label, exact=True).is_visible()
        )


def test_paga_labels_clear_nodes_and_colorbar_has_normal_width(page):
    chart = gsc.pl.paga(
        make_paga("gene_raw"),
        color="g1",
        pos=POSITIONS,
        width=500,
        height=350,
        show=False,
    )
    render(page, chart)
    root = svg_root(page)
    panel = next(e for e in root.iter() if e.get("data-name") == "panel-0")
    rules = [e for e in panel.iter() if e.get("data-mark-type") == "rule"]
    assert rules and all(e.get("stroke") == "#999999" for e in rules)
    circles = list(next(e for e in panel.iter() if e.get("data-mark-type") == "point"))
    labels = list(next(e for e in panel.iter() if e.get("data-mark-type") == "text"))
    assert len(circles) == len(labels) == 4
    assert {label.text for label in labels} == {"A", "B", "C", "D"}
    boxes = page.evaluate("""async () => {
        const host = document.createElement('div');
        host.style.cssText = 'position:absolute;visibility:hidden';
        host.innerHTML = await (await api.imageExport.svg()).blob.text();
        document.body.append(host);
        const panel = host.querySelector('[data-name="panel-0"]');
        const bounds = selector => [...panel.querySelectorAll(selector)].map(e => {
            const {left, right, top, bottom} = e.getBoundingClientRect();
            return {left, right, top, bottom};
        });
        const result = {nodes: bounds('circle'), labels: bounds('text')};
        host.remove();
        return result;
    }""")
    assert len(boxes["nodes"]) == len(boxes["labels"]) == 4
    for label in boxes["labels"]:
        for node in boxes["nodes"]:
            assert (
                label["right"] <= node["left"]
                or label["left"] >= node["right"]
                or label["bottom"] <= node["top"]
                or label["top"] >= node["bottom"]
            )
    gradients = [
        e
        for e in root.iter()
        if e.tag.endswith("rect") and e.get("fill", "").startswith("url(")
    ]
    assert len(gradients) == 1
    assert float(gradients[0].get("width")) == pytest.approx(15, abs=0.1)


def test_path_labels_only_appear_when_their_visible_group_span_fits(page):
    a = make_path()
    names = {"beta": "Long category B", "alpha": "Long category A"}
    a.obs["cluster"] = a.obs["cluster"].cat.rename_categories(names)
    chart = gsc.pl.paga_path(
        a,
        list(names.values()),
        ["g1", "g2"],
        width=140,
        height=180,
        zoom="xy",
        show=False,
    )
    spec = chart.to_dict()
    spec["scales"]["x"]["name"] = "path-x"
    render(page, spec)

    def group_labels():
        """Read only visible band labels, excluding the native legend entries."""
        group = next(
            e for e in svg_root(page).iter() if e.get("data-name") == "paga-path-groups"
        )
        return [e.text for e in group.iter() if e.tag.endswith("text")]

    texts = {e.text for e in svg_root(page).iter() if e.tag.endswith("text")}
    assert {"cluster", "dpt_pseudotime", *names.values()} <= texts
    assert group_labels() == []
    page.evaluate(
        "async () => api.getScaleResolutionByName('path-x').zoomTo([-0.5, 0.5])"
    )
    page.wait_for_timeout(300)
    assert group_labels() == ["Long category B"]
    bounds = page.evaluate(
        "api.views.getLayoutBounds({scope:[],view:'paga-path-groups'})"
    )
    hover_at(
        page, bounds["x"] + bounds["width"] / 2, bounds["y"] + bounds["height"] / 2
    )
    assert (
        page.locator("table.attributes")
        .get_by_text("Long category B", exact=True)
        .is_visible()
    )
