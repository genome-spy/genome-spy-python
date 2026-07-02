from __future__ import annotations

import json
import math
from datetime import datetime

import genome_spy as gs
import pytest

from genome_spy.chart import DEFAULT_EMBED_URL, DEFAULT_SCHEMA_URL
from genome_spy.schema import SCHEMA_VERSION, UnitSpec
from genome_spy.schema.channels import X as GeneratedX
from genome_spy.schemapi import SchemaValidationError


def test_package_exposes_version() -> None:
    assert gs.__version__ == "0.1.0"


def test_chart_directly_inherits_generated_unit_spec() -> None:
    original = gs.Chart([{"x": 1}], schema_url="https://example.test/schema.json")
    marked = original.mark_point().encode(x="x:Q")

    assert isinstance(original, UnitSpec)
    assert isinstance(marked, UnitSpec)
    assert "mark" not in original.to_dict(validate=False)
    assert marked.to_dict()["mark"] == "point"
    assert marked.to_dict()["$schema"] == "https://example.test/schema.json"


def test_public_channel_wrapper_is_generated_and_fluent() -> None:
    channel = gs.X("position:Q").scale(zero=False).title("Position")

    assert isinstance(channel, GeneratedX)
    assert channel.encoding_name == "x"
    assert channel.to_dict() == {
        "field": "position",
        "type": "quantitative",
        "scale": {"zero": False},
        "title": "Position",
    }


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
        "$schema": DEFAULT_SCHEMA_URL,
        "description": "Simple point plot",
        "width": 320,
        "height": 180,
        "data": {"values": [{"x": 1, "y": 2, "label": "A"}]},
        "mark": {"type": "point", "size": 64},
        "encoding": {
            "x": {"field": "x", "type": "quantitative"},
            "y": {
                "field": "y",
                "type": "quantitative",
                "scale": {"reverse": True},
            },
            "color": {"value": "steelblue"},
            "text": {"field": "label", "type": "nominal"},
        },
    }


def test_altair_style_penguins_snippet_serializes() -> None:
    class DataFrameLike:
        def to_dict(self, *, orient: str) -> list[dict[str, object]]:
            assert orient == "records"
            return [
                {
                    "Flipper Length (mm)": 181,
                    "Body Mass (g)": 3750,
                    "Beak Depth (mm)": 18.7,
                    "Species": "Adelie",
                }
            ]

    source = DataFrameLike()

    chart = (
        gs.Chart(source)
        .mark_circle()
        .encode(
            gs.X("Flipper Length (mm)").scale(zero=False),
            gs.Y("Body Mass (g)").scale(zero=False, padding=1),
            gs.Size("Beak Depth (mm)").scale(zero=False),
            color="Species",
        )
    )

    spec = chart.to_dict()

    assert spec["data"]["values"][0]["Species"] == "Adelie"
    assert spec["mark"] == "point"
    assert spec["encoding"]["x"] == {
        "field": "Flipper Length (mm)",
        "scale": {"zero": False},
        "type": "quantitative",
    }
    assert spec["encoding"]["y"] == {
        "field": "Body Mass (g)",
        "scale": {"reverse": True, "zero": False, "padding": 1},
        "type": "quantitative",
    }
    assert spec["encoding"]["size"] == {
        "field": "Beak Depth (mm)",
        "scale": {"zero": False},
        "type": "quantitative",
    }
    assert spec["encoding"]["color"] == {
        "field": "Species",
        "type": "nominal",
    }


def test_altair_style_tick_shorthand_serializes() -> None:
    chart = (
        gs.Chart(
            [
                {"Horsepower": 130, "Cylinders": 8},
                {"Horsepower": 95, "Cylinders": 6},
            ]
        )
        .mark_tick()
        .encode(x="Horsepower:Q", y="Cylinders:O")
    )

    spec = chart.to_dict()

    assert spec["mark"] == "tick"
    assert spec["encoding"]["x"] == {
        "field": "Horsepower",
        "type": "quantitative",
    }
    assert spec["encoding"]["y"] == {
        "field": "Cylinders",
        "type": "ordinal",
        "scale": {"reverse": True},
    }


def test_genomespy_style_stacked_bar_transforms_serialize() -> None:
    chart = (
        gs.Chart(
            [
                {"variety": "Manchuria", "site": "Waseca", "yield": 48.8},
                {"variety": "Manchuria", "site": "Morris", "yield": 27.4},
            ]
        )
        .transform_aggregate(
            groupby=["variety", "site"],
            fields=["yield"],
            ops=["sum"],
            as_=["yieldSum"],
        )
        .transform_stack(
            field="yieldSum",
            groupby=["variety"],
            sort={"field": "site", "order": "ascending"},
            as_=["yieldStart", "yieldEnd"],
        )
        .mark_rect()
        .encode(
            x=gs.X("yieldStart:Q").title("Sum of yield"),
            x2="yieldEnd",
            y=gs.Y("variety:N").scale(padding=0.1, reverse=False),
            color="site:N",
        )
    )

    spec = chart.to_dict()

    assert spec["transform"] == [
        {
            "type": "aggregate",
            "groupby": ["variety", "site"],
            "fields": ["yield"],
            "ops": ["sum"],
            "as": ["yieldSum"],
        },
        {
            "type": "stack",
            "field": "yieldSum",
            "groupby": ["variety"],
            "sort": {"field": "site", "order": "ascending"},
            "as": ["yieldStart", "yieldEnd"],
        },
    ]
    assert spec["mark"] == "rect"
    assert spec["encoding"]["x"] == {
        "field": "yieldStart",
        "title": "Sum of yield",
        "type": "quantitative",
    }
    assert spec["encoding"]["x2"] == {"field": "yieldEnd"}
    assert spec["encoding"]["y"]["field"] == "variety"
    assert spec["encoding"]["y"]["type"] == "nominal"
    assert spec["encoding"]["y"]["scale"] == {"padding": 0.1, "reverse": False}
    assert spec["encoding"]["color"] == {
        "field": "site",
        "type": "nominal",
    }


def test_y_scale_reverse_can_be_overridden() -> None:
    chart = (
        gs.Chart([{"x": 1, "y": 2}])
        .mark_point()
        .encode(x="x:Q", y=gs.Y("y:Q").scale(reverse=False))
    )

    assert chart.to_dict()["encoding"]["y"]["scale"] == {"reverse": False}


def test_plain_mapping_data_is_preserved() -> None:
    chart = gs.Chart(data={"url": "data.csv"}).mark_rect().encode(x="x:Q", y="y:Q")

    assert chart.to_dict()["data"] == {"url": "data.csv"}


def test_dataframe_like_nan_values_are_serialized_as_null() -> None:
    chart = gs.Chart([{"x": math.nan, "y": 2}]).mark_point().encode(x="x:Q", y="y:Q")

    assert chart.to_dict()["data"]["values"] == [{"x": None, "y": 2}]


def test_dataframe_like_datetime_values_are_json_safe() -> None:
    chart = (
        gs.Chart([{"x": 1, "when": datetime(1970, 1, 1)}]).mark_tick().encode(x="x:Q")
    )

    spec = chart.to_dict()

    assert spec["data"]["values"] == [{"x": 1, "when": "1970-01-01T00:00:00"}]
    json.dumps(spec)


def test_chart_spec_and_string_repr_expose_json_spec() -> None:
    chart = gs.Chart([{"x": 1}]).mark_point().encode(x="x:Q")

    assert chart.spec == chart.to_dict()
    assert json.loads(repr(chart.spec)) == chart.to_dict()
    assert '"encoding"' in repr(chart.spec)
    assert "'encoding'" not in repr(chart.spec)
    assert json.loads(str(chart)) == chart.to_dict()


def test_chart_spec_ipython_pretty_prints_json() -> None:
    class Printer:
        def __init__(self) -> None:
            self.output = ""

        def text(self, value: str) -> None:
            self.output += value

    chart = gs.Chart([{"x": 1}]).mark_point().encode(x="x:Q")
    printer = Printer()

    chart.spec._repr_pretty_(printer, cycle=False)

    assert json.loads(printer.output) == chart.to_dict()
    assert "\n  " in printer.output


def test_chart_spec_mimebundle_prefers_pretty_text() -> None:
    chart = gs.Chart([{"x": 1}]).mark_point().encode(x="x:Q")

    bundle = chart.spec._repr_mimebundle_()

    assert set(bundle) == {"text/plain"}
    assert json.loads(bundle["text/plain"]) == chart.to_dict()
    assert "\n  " in bundle["text/plain"]


def test_to_html_embeds_genomespy_runtime() -> None:
    html = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q").to_html()

    assert "await import(moduleUrl)" in html
    assert "module.embed ?? module.default?.embed ?? module.default" in html
    assert "dist/bundle/index.es.js" in html
    assert '"mark":"point"' in html
    assert json.dumps("x") in html


def test_runtime_urls_match_generated_schema_version() -> None:
    versioned_package = f"@genome-spy/core@{SCHEMA_VERSION}"

    assert versioned_package in DEFAULT_SCHEMA_URL
    assert versioned_package in DEFAULT_EMBED_URL


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


def test_chart_validates_complete_spec_by_default() -> None:
    chart = gs.Chart([{"x": 1}], mark="not-a-mark").encode(x="x:Q")

    with pytest.raises(SchemaValidationError, match="Invalid Root"):
        chart.to_dict()

    assert chart.to_dict(validate=False)["mark"] == "not-a-mark"
