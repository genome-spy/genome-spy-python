from __future__ import annotations

import json

import genome_spy as gs


def test_package_exposes_version() -> None:
    assert gs.__version__ == "0.1.0"


def test_chart_serializes_core_spec() -> None:
    chart = (
        gs.Chart(data=[{"x": 1, "y": 2, "label": "A"}])
        .mark_point(size=64)
        .encode(
            x=gs.X("x:Q"),
            y=gs.Y("y:Q"),
            color=gs.value("steelblue"),
            text=gs.Text("label:N"),
        )
        .properties(width=320, height=180, description="Simple point plot")
    )

    assert chart.to_dict() == {
        "$schema": "https://cdn.jsdelivr.net/npm/@genome-spy/core/dist/schema.json",
        "description": "Simple point plot",
        "width": 320,
        "height": 180,
        "data": {"values": [{"x": 1, "y": 2, "label": "A"}]},
        "mark": {"type": "point", "size": 64},
        "encoding": {
            "x": {"field": "x", "type": "quantitative"},
            "y": {"field": "y", "type": "quantitative"},
            "color": {"value": "steelblue"},
            "text": {"field": "label", "type": "nominal"},
        },
    }


def test_plain_mapping_data_is_preserved() -> None:
    chart = gs.Chart(data={"url": "data.csv"}).mark_rect().encode(x="x:Q", y="y:Q")

    assert chart.to_dict()["data"] == {"url": "data.csv"}


def test_to_html_embeds_genomespy_runtime() -> None:
    html = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q").to_html()

    assert "await import(moduleUrl)" in html
    assert "module.embed ?? module.default?.embed ?? module.default" in html
    assert "dist/bundle/index.es.js" in html
    assert '"mark":"point"' in html
    assert json.dumps("x") in html


def test_default_repr_uses_widget_bundle_when_available() -> None:
    bundle = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")._repr_mimebundle_()

    assert isinstance(bundle, tuple)
    assert "application/vnd.jupyter.widget-view+json" in bundle[0]


def test_transform_formula_serializes() -> None:
    chart = (
        gs.Chart(data=[{"x": 1}])
        .transform_formula(expr="datum.x * 2", as_="double_x")
        .mark_point()
        .encode(x="double_x:Q")
    )

    assert chart.to_dict()["transform"] == [
        {"type": "formula", "expr": "datum.x * 2", "as": "double_x"}
    ]


def test_layer_operator_serializes_without_nested_schema() -> None:
    points = gs.Chart(data=[{"x": 1, "y": 2}]).mark_point().encode(x="x:Q", y="y:Q")
    labels = points.mark_text(dx=6).encode(text=gs.Text("y:Q"))

    layered = points + labels
    spec = layered.to_dict()

    assert "layer" in spec
    assert "$schema" not in spec["layer"][0]
    assert spec["layer"][0]["mark"] == "point"
    assert spec["layer"][1]["mark"] == {"type": "text", "dx": 6}


def test_concat_operators_match_genomespy_core_keys() -> None:
    left = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")
    right = gs.Chart(data=[{"x": 2}]).mark_point().encode(x="x:Q")

    assert "hconcat" in (left | right).to_dict()
    assert "vconcat" in (left & right).to_dict()


def test_grid_concat_helper_serializes_columns() -> None:
    one = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")
    two = gs.Chart(data=[{"x": 2}]).mark_point().encode(x="x:Q")

    spec = gs.concat(one, two, columns=2).to_dict()

    assert spec["columns"] == 2
    assert len(spec["concat"]) == 2
