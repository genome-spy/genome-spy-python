"""Pca behavior and regressions."""

import re
import xml.etree.ElementTree as ET

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.interactions import move_to, pointer
from tests.integrations.scanpy.browser.rendering import render
from tests.integrations.scanpy.embedding_fixtures import make_pca_adata
from tests.integrations.scanpy.helpers import name_embedding_scales, points, units


def pca_overview_rank_texts(svg):
    """Return rotated rank-label geometry to detect accidental diagnostic zoom."""
    return [
        e.attrib
        for e in ET.fromstring(svg).iter()
        if e.tag.endswith("text")
        and e.text in ("g1", "g2", "g3", "g4", "PC4", "PC5")
        and ("rotate" in e.get("transform", ""))
    ]


class TestPcaOverview:
    """Observe parent chart fidelity, isolated PCA navigation and offline overview delivery."""

    @pytest.mark.parametrize("page", [1.5], indirect=True)
    def test_complete_overview_keeps_parent_axes_guides_and_registered_rank_labels(
        self, page, tmp_path
    ):
        chart = gsc.pl.pca_overview(
            make_pca_adata(), color=["group", "g1"], width=210, height=180, show=False
        )
        spec = chart.to_dict()
        render(page, chart)
        svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        texts = [e for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
        labels = [e.text for e in texts]
        assert all(
            (
                text in labels
                for text in [
                    "group",
                    "g1",
                    "PC1",
                    "PC2",
                    "PC3",
                    "variance ratio",
                    "ranking",
                    "C",
                    "A",
                    "D",
                    "B",
                ]
            )
        )
        bounds = [
            page.evaluate(
                "i => api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i
            )
            for i in range(6)
        ]
        size = page.evaluate("api.getLogicalCanvasSize()")
        assert size["width"] <= 736
        assert bounds[2]["y"] == pytest.approx(bounds[3]["y"], abs=1)
        assert bounds[4]["y"] > bounds[2]["y"] + bounds[2]["height"]
        assert all(
            (0 <= box["x"] < box["x"] + box["width"] <= size["width"] for box in bounds)
        )
        for i, box in enumerate(bounds):
            assert box["width"] == pytest.approx(
                210 if i < 2 else 280 if i < 5 else 300, abs=1
            )
            assert box["height"] == pytest.approx(180 if i < 2 else 300, abs=1)
        assert max((b["y"] + b["height"] for b in bounds[:2])) < min(
            (b["y"] for b in bounds[2:5])
        )
        assert max((b["y"] + b["height"] for b in bounds[2:4])) < bounds[4]["y"]
        assert bounds[4]["y"] == pytest.approx(bounds[5]["y"], abs=1)
        for panel, box in zip(units(spec)[2:], bounds[2:], strict=True):
            x0, x1 = panel["encoding"]["x"]["scale"]["domain"]
            y0, y1 = panel["encoding"]["y"]["scale"]["domain"]
            for record in spec["datasets"][panel["data"]["name"]]:
                expected = [
                    box["x"] + (record["_rank"] - x0) / (x1 - x0) * box["width"],
                    box["y"] + (y1 - record["_score"]) / (y1 - y0) * box["height"],
                ]
                positions = [
                    list(
                        map(
                            float,
                            re.search(
                                "translate\\(([-\\d.e]+)[ ,]+([-\\d.e]+)",
                                e.get("transform", ""),
                            ).groups(),
                        )
                    )
                    for e in texts
                    if e.text == record["_label"]
                ]
                assert any(
                    (
                        np.allclose(position, expected, atol=2 / 1.5)
                        for position in positions
                    )
                ), (record, positions, expected)
        page.screenshot(path=str(tmp_path / "overview-complete.png"), full_page=True)
        (tmp_path / "overview-complete.svg").write_text(svg)

    def test_overview_hover_navigation_and_offline_html_keep_diagnostics_fixed(
        self, page, tmp_path
    ):
        a = make_pca_adata()
        chart = gsc.pl.pca_overview(a, color=["group", "g1"], zoom=True, show=False)
        spec = chart.to_dict()
        bounds = render(page, name_embedding_scales(chart.to_dict(), "pca"))
        panel = points(units(spec)[0])
        domains = [panel["encoding"][axis]["scale"]["domain"] for axis in ("x", "y")]
        move_to(page, bounds, 2, 4, *domains, "cell2")
        assert page.get_by_text("cell2", exact=True).first.is_visible()
        before = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        names = ["pca-x-0", "pca-y-1"]
        domains = page.evaluate(
            "names => names.map(n => api.getScaleResolutionByName(n).getDomain())",
            names,
        )
        pointer(page, bounds)
        page.mouse.wheel(0, -220)
        page.wait_for_function(
            "({names,domains}) => names.every((n,i) => {const d=api.getScaleResolutionByName(n).getDomain(); return d[1]-d[0]<domains[i][1]-domains[i][0]})",
            arg={"names": names, "domains": domains},
        )
        # Let wheel navigation settle before testing hover in another row.
        page.wait_for_timeout(700)
        after = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
        assert before != after
        assert pca_overview_rank_texts(before) and pca_overview_rank_texts(
            after
        ) == pca_overview_rank_texts(before)
        rank = units(spec)[2]
        record = spec["datasets"][rank["data"]["name"]][1]
        box = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-2'})")
        x0, x1 = rank["encoding"]["x"]["scale"]["domain"]
        y0, y1 = rank["encoding"]["y"]["scale"]["domain"]
        px, py = pointer(
            page,
            box,
            x=(record["_rank"] - x0) / (x1 - x0),
            y=(y1 - record["_score"]) / (y1 - y0),
        )
        for dx, dy in [(0, -4), (0, -8), (2, -4)]:
            page.mouse.move(px + dx, py + dy)
            page.wait_for_timeout(450)
            page.mouse.move(px + dx + 0.2, py + dy + 0.2)
            page.wait_for_timeout(100)
            if (
                page.locator("table.attributes")
                .get_by_text(record["_label"], exact=True)
                .is_visible()
            ):
                break
        page.get_by_text(record["_label"], exact=True).wait_for(state="visible")
        assert page.get_by_text("Score", exact=True).is_visible()
        output = tmp_path / "overview.html"
        chart.save(output, inline=True)
        page.route("https://**/*", lambda route: route.abort())
        page.route("http://**/*", lambda route: route.abort())
        page.goto(output.as_uri())
        page.locator("canvas").first.wait_for(state="visible")
        assert page.locator(".message-box").count() == 0
