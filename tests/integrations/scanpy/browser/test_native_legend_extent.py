"""Retain C11's upstream reproducer without changing the bundled renderer."""

import xml.etree.ElementTree as ET

import pytest
import genome_spy as gs
from genome_spy.schema import SCHEMA_VERSION
from tests.integrations.scanpy.browser.test_umap import render


@pytest.mark.xfail(
    SCHEMA_VERSION == "1.2.0",
    strict=True,
    raises=AssertionError,
    reason="C11: Core 1.2 vertical legend extent excludes subsequent columns",
)
def test_native_vertical_legend_keeps_every_column_visible(page, tmp_path):
    categories = [f"category-{i}" for i in range(12)]
    chart = (
        gs.Chart([{"x": i, "group": group} for i, group in enumerate(categories)])
        .mark_point()
        .encode(
            x="x:Q",
            y=gs.value(0.5),
            color=gs.Color("group:N").legend(values=categories, columns=2, title=None),
        )
        .properties(width=300, height=300)
        .configure_legend(
            symbolSize=64,
            labelFontSize=12,
            rowPadding=4,
            layout=gs.LegendLayout(anchor="middle", wrap=False),
        )
    )
    chart.save(tmp_path / "native-legend.html", inline=True, controls=False)
    render(page, chart)
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    (tmp_path / "native-legend.svg").write_text(svg)
    page.screenshot(path=str(tmp_path / "native-legend.png"), full_page=True)
    labels = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
    assert {label for label in labels if label in categories} == set(categories)
