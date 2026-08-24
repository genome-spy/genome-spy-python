from __future__ import annotations

import json
import math
import inspect
from datetime import datetime

import genome_spy as gs
import polars as pl
import pytest

from genome_spy.chart import DEFAULT_EMBED_URL, DEFAULT_SCHEMA_URL
from genome_spy import api as public_api
from genome_spy.schema import (
    CompareParams,
    ConcatSpec,
    DynamicOpacity,
    ExprRef,
    HandledTooltip,
    GenomeSpyConfig,
    GenomeAxis,
    HConcatSpec,
    ImportSpec,
    LayerSpec,
    Legend,
    MultiscaleSpec,
    SCHEMA_VERSION,
    Step,
    Title,
    Scale,
    UnitSpec,
    VConcatSpec,
    ViewBackground,
    ViewConfig,
)
from genome_spy.schema import ergonomics as generated_ergonomics
from genome_spy.schema.channels import X as GeneratedX
from genome_spy.channels import LocusChannel
from genome_spy.schemapi import SchemaValidationError


def test_package_exposes_version() -> None:
    assert gs.__version__ == "0.1.0"


def test_public_api_exports_are_unique() -> None:
    assert len(public_api.__all__) == len(set(public_api.__all__))
    assert len(gs.__all__) == len(set(gs.__all__))


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


def test_generated_channel_simple_setters_are_schema_driven() -> None:
    channel = gs.X("position:Q").field("position_bp").type("quantitative").band(0.5)

    assert channel.to_dict() == {
        "field": "position_bp",
        "type": "quantitative",
        "band": 0.5,
    }


def test_generated_channel_nested_setters_accept_schema_wrappers() -> None:
    channel = (
        gs.X("position:Q")
        .axis(GenomeAxis(title="Position axis"))
        .scale(Scale(zero=False), padding=12)
    )
    color = gs.Color("species:N").legend(Legend(title="Species legend"))

    assert channel.to_dict() == {
        "field": "position",
        "type": "quantitative",
        "axis": {"title": "Position axis"},
        "scale": {"zero": False, "padding": 12},
    }
    assert color.to_dict() == {
        "field": "species",
        "type": "nominal",
        "legend": {"title": "Species legend"},
    }


def test_channel_sort_supports_fluent_compare_configuration() -> None:
    channel = gs.Y("gene:N").sort(field="score", order="descending")

    assert channel.to_dict() == {
        "field": "gene",
        "type": "nominal",
        "sort": {"field": "score", "order": "descending"},
    }

    signature = inspect.signature(gs.Y("gene:N").sort)
    assert {"value", "field", "order"} == set(signature.parameters)
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )


def test_channel_sort_accepts_schema_wrapper_and_simple_values() -> None:
    wrapped = gs.Y("gene:N").sort(CompareParams(field="score", order="ascending"))
    simple = gs.Y("gene:N").sort(["TP53", "NPM1"])

    assert wrapped.to_dict()["sort"] == {"field": "score", "order": "ascending"}
    assert simple.to_dict()["sort"] == ["TP53", "NPM1"]


def test_public_api_exposes_additional_ergonomic_builders() -> None:
    assert gs.expr("datum.x * 2").to_dict() == {"expr": "datum.x * 2"}
    assert gs.title("Example", orient="left").to_dict() == {
        "text": "Example",
        "orient": "left",
    }
    assert gs.step(18).to_dict() == {"step": 18}
    assert gs.dynamic_opacity(
        unitsPerPixel=[100000, 40000], values=[0, 1]
    ).to_dict() == {
        "unitsPerPixel": [100000, 40000],
        "values": [0, 1],
    }
    assert gs.datum(0, type="quantitative").to_dict() == {
        "datum": 0,
        "type": "quantitative",
    }
    assert gs.data_format(type="bed").to_dict() == {"type": "bed"}
    assert gs.parse(chrom="string", start="integer").to_dict() == {
        "chrom": "string",
        "start": "integer",
    }
    assert gs.param("threshold", value=5).to_dict() == {"name": "threshold", "value": 5}
    assert gs.compare("site", order="ascending").to_dict() == {
        "field": "site",
        "order": "ascending",
    }
    assert gs.scales(x=Scale(domain=[0, 10])) == {"x": {"domain": [0, 10]}}
    assert gs.axes(x=GenomeAxis(orient="top")) == {"x": {"orient": "top"}}
    assert gs.Paddings(top=-5).to_dict() == {"top": -5}
    assert gs.SizeDef(grow=2).to_dict() == {"grow": 2}
    assert gs.condition("hover", 1, empty=False).to_dict() == {
        "empty": False,
        "param": "hover",
        "value": 1,
    }
    assert gs.condition("category", "selected").to_dict() == {
        "empty": True,
        "param": "category",
        "value": "selected",
    }
    assert gs.condition("hover", gs.expr("datum.size")).value(3).to_dict() == {
        "empty": True,
        "param": "hover",
        "value": 3,
    }
    assert gs.XOffset("displacement:Q").scale(None).to_dict() == {
        "field": "displacement",
        "type": "quantitative",
        "scale": None,
    }
    assert gs.YOffset(gs.value(2)).to_dict() == {"value": 2}
    assert gs.view(stroke="lightgray").to_dict() == {"stroke": "lightgray"}
    assert gs.view_config(stroke="lightgray").to_dict() == {"stroke": "lightgray"}
    assert gs.config(view=gs.view(stroke="lightgray")).to_dict() == {
        "view": {"stroke": "lightgray"}
    }

    assert isinstance(gs.expr("datum.x"), ExprRef)
    assert isinstance(gs.compare("site"), CompareParams)
    assert isinstance(gs.title("Example"), Title)
    assert isinstance(gs.step(10), Step)
    assert isinstance(gs.view(stroke="lightgray"), ViewBackground)
    assert isinstance(gs.view_config(stroke="lightgray"), ViewConfig)
    assert isinstance(gs.config(), GenomeSpyConfig)
    assert isinstance(gs.HandledTooltip(handler="demo"), HandledTooltip)
    assert isinstance(
        gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
        DynamicOpacity,
    )


def test_schema_object_helpers_have_generated_keyword_signatures() -> None:
    helper_parameters = {
        "title": {"text", "orient", "subtitle"},
        "dynamic_opacity": {"channel", "unitsPerPixel", "values"},
        "data_format": {"columns", "delimiter", "parse", "property", "type"},
        "param": {"name", "bind", "select", "transition", "value"},
        "view": {"fill", "stroke", "style"},
        "view_config": {"continuousWidth", "discreteHeight", "stroke"},
        "config": {"axis", "legend", "mark", "view"},
    }

    for helper_name, expected_parameters in helper_parameters.items():
        helper = getattr(gs, helper_name)
        signature = inspect.signature(helper)

        assert expected_parameters <= set(signature.parameters)
        assert all(
            parameter.kind is not inspect.Parameter.VAR_KEYWORD
            for parameter in signature.parameters.values()
        )
        assert helper is getattr(generated_ergonomics, helper_name)


def test_top_level_copy_methods_have_generated_keyword_signatures() -> None:
    chart = gs.Chart([{"x": 1}]).mark_point().copy(width=240, height=120)

    assert chart.to_dict()["width"] == 240
    assert chart.to_dict()["height"] == 120
    for chart_class in (
        gs.Chart,
        gs.LayerChart,
        gs.HConcatChart,
        gs.VConcatChart,
        gs.ConcatChart,
        gs.MultiscaleChart,
    ):
        signature = inspect.signature(chart_class.copy)

        assert {"deep", "config", "width"} <= set(signature.parameters)
        assert all(
            parameter.kind is not inspect.Parameter.VAR_KEYWORD
            for parameter in signature.parameters.values()
        )


def test_top_level_constructors_and_properties_are_root_variant_specific() -> None:
    structural_parameters = {
        "mark",
        "layer",
        "hconcat",
        "vconcat",
        "concat",
        "multiscale",
    }
    expected = {
        gs.Chart: "mark",
        gs.LayerChart: "layer",
        gs.HConcatChart: "hconcat",
        gs.VConcatChart: "vconcat",
        gs.ConcatChart: "concat",
        gs.MultiscaleChart: "multiscale",
    }

    for chart_class, structural_parameter in expected.items():
        for callable_ in (chart_class, chart_class.properties):
            signature = inspect.signature(callable_)
            assert structural_parameter in signature.parameters
            assert structural_parameters & set(signature.parameters) == {
                structural_parameter
            }
            assert all(
                parameter.kind is not inspect.Parameter.VAR_KEYWORD
                for parameter in signature.parameters.values()
            )

    assert "columns" in inspect.signature(gs.ConcatChart).parameters
    assert "columns" not in inspect.signature(gs.VConcatChart).parameters
    assert "stops" in inspect.signature(gs.MultiscaleChart).parameters
    assert "stops" not in inspect.signature(gs.Chart).parameters
    imported_signature = inspect.signature(gs.ImportedView)
    assert {"import_", "config", "name", "params", "visible", "zindex"} == set(
        imported_signature.parameters
    )
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in imported_signature.parameters.values()
    )


def test_expression_helper_works_in_channel_definitions() -> None:
    chart = (
        gs.Chart([{"x": 1, "label": "A", "strand": "+"}])
        .mark_point()
        .encode(
            x="x:Q",
            dx=gs.Dx(gs.expr("datum.x * 2"), type="quantitative").scale(None),
            shape=gs.Shape("strand:N")
            .scale(domain=["-", "+"], range=["triangle-left", "triangle-right"])
            .legend(None),
        )
    )

    assert chart.to_dict()["encoding"]["dx"] == {
        "expr": "datum.x * 2",
        "type": "quantitative",
        "scale": None,
    }
    assert chart.to_dict()["encoding"]["shape"] == {
        "field": "strand",
        "type": "nominal",
        "scale": {
            "domain": ["-", "+"],
            "range": ["triangle-left", "triangle-right"],
        },
        "legend": None,
    }


def test_generated_channel_constructor_accepts_schema_wrappers() -> None:
    channel = gs.Dx(gs.expr("datum.x * 2"), type="quantitative")

    assert channel.to_dict() == {
        "expr": "datum.x * 2",
        "type": "quantitative",
    }


def test_generated_channel_nested_setters_allow_null_override() -> None:
    channel = gs.X("position:Q").axis(None)

    assert channel.to_dict() == {
        "field": "position",
        "type": "quantitative",
        "axis": None,
    }


def test_locus_channel_supports_fluent_axis_and_scale_configuration() -> None:
    channel = (
        gs.Locus("chrom", "pos")
        .axis(title="Genomic position", grid=False)
        .scale(assembly="hg38")
    )

    assert channel.to_dict() == {
        "chrom": "chrom",
        "pos": "pos",
        "type": "locus",
        "axis": {"title": "Genomic position", "grid": False},
        "scale": {"assembly": "hg38"},
    }


def test_locus_helper_returns_dedicated_channel_type() -> None:
    channel = gs.Locus("chrom", "pos").chrom("chromosome").pos("position").band(0.5)

    assert isinstance(channel, LocusChannel)
    assert channel.to_dict() == {
        "chrom": "chromosome",
        "pos": "position",
        "type": "locus",
        "band": 0.5,
    }


def test_locus_and_compare_helpers_have_generated_keyword_signatures() -> None:
    locus_signature = inspect.signature(gs.Locus)
    compare_signature = inspect.signature(gs.compare)

    assert {"axis", "band", "offset", "scale", "title"} <= set(
        locus_signature.parameters
    )
    assert set(compare_signature.parameters) == {"field", "order"}
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for signature in (locus_signature, compare_signature)
        for parameter in signature.parameters.values()
    )


def test_datum_and_value_helpers_have_generated_keyword_signatures() -> None:
    datum_signature = inspect.signature(gs.datum)
    value_signature = inspect.signature(gs.value)

    assert {"axis", "condition", "scale", "type"} <= set(datum_signature.parameters)
    assert {"buildIndex", "condition", "description", "title", "value"} == set(
        value_signature.parameters
    )
    assert {"datum", "field", "axis", "scale", "type"}.isdisjoint(
        value_signature.parameters
    )
    assert {"field", "value"}.isdisjoint(datum_signature.parameters)
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for signature in (datum_signature, value_signature)
        for parameter in signature.parameters.values()
    )


def test_constant_channel_helpers_preserve_fluent_configuration() -> None:
    channel = gs.datum(0, type="quantitative").scale(zero=True).axis(title="Score")

    assert channel.to_dict() == {
        "datum": 0,
        "type": "quantitative",
        "scale": {"zero": True},
        "axis": {"title": "Score"},
    }
    assert channel.encoding_name is None
    assert not hasattr(gs.value("steelblue"), "scale")

    with pytest.raises(TypeError, match="Positional encodings must be channel objects"):
        gs.Chart().encode(gs.datum(0))


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
            "y": {"field": "y", "type": "quantitative"},
            "color": {"value": "steelblue"},
            "text": {"field": "label", "type": "nominal"},
        },
    }


# Adapted from Vega-Altair's multifeature scatter-plot example:
# https://github.com/vega/altair/blob/main/tests/examples_methods_syntax/multifeature_scatter_plot.py
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
        "scale": {"zero": False, "padding": 1},
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


def test_chart_properties_support_genomic_top_level_config() -> None:
    chart = (
        gs.Chart([{"chrom": "chr1", "start": 1, "end": 10, "value": 3}])
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "start"),
            x2=gs.Locus("chrom", "end"),
            y="value:Q",
        )
        .properties(
            assembly="hg38",
            config=gs.config(view=gs.view_config(stroke="lightgray")),
            viewportHeight="container",
            view=gs.view(stroke="lightgray"),
            params=[gs.param("threshold", value=5)],
        )
    )

    spec = chart.to_dict()

    assert spec["assembly"] == "hg38"
    assert spec["config"] == {"view": {"stroke": "lightgray"}}
    assert spec["viewportHeight"] == "container"
    assert spec["view"] == {"stroke": "lightgray"}
    assert spec["params"] == [{"name": "threshold", "value": 5}]


def test_generated_configure_methods_merge_top_level_config() -> None:
    chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q")
        .configure(view=gs.view_config(stroke="lightgray"))
        .configure_axis(title="Position", domain=False)
        .configure_mark(opacity=0.5)
    )

    spec = chart.to_dict()

    assert spec["config"] == {
        "view": {"stroke": "lightgray"},
        "axis": {"title": "Position", "domain": False},
        "mark": {"opacity": 0.5},
    }


def test_generated_configure_methods_match_helper_serialization() -> None:
    helper_chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q")
        .properties(config=gs.config(view=gs.view_config(stroke="lightgray")))
    )
    generated_chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q")
        .configure_view(stroke="lightgray")
    )

    assert helper_chart.to_dict()["config"] == generated_chart.to_dict()["config"]


def test_top_level_with_view_merges_nested_properties_and_preserves_chart_type() -> (
    None
):
    chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q")
        .with_view(stroke="lightgray")
        .with_view(fill="#f8f8f8")
    )

    assert isinstance(chart, gs.Chart)
    assert chart.to_dict()["view"] == {
        "stroke": "lightgray",
        "fill": "#f8f8f8",
    }


def test_top_level_with_config_and_with_scales_merge_across_calls() -> None:
    chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q")
        .with_config(view={"stroke": "lightgray"})
        .with_config(axis={"grid": False})
        .with_scales(x={"zoom": True})
        .with_scales(color={"scheme": "blues"})
    )

    assert chart.to_dict()["config"] == {
        "view": {"stroke": "lightgray"},
        "axis": {"grid": False},
    }
    assert chart.to_dict()["scales"] == {
        "x": {"zoom": True},
        "color": {"scheme": "blues"},
    }


def test_top_level_merge_methods_have_generated_keyword_signatures() -> None:
    for method, expected in (
        (gs.Chart.with_config, {"axis", "view"}),
        (gs.Chart.with_view, {"fill", "stroke"}),
        (gs.Chart.with_scales, {"color", "x"}),
    ):
        signature = inspect.signature(method)
        assert expected <= set(signature.parameters)
        assert all(
            parameter.kind is not inspect.Parameter.VAR_KEYWORD
            for parameter in signature.parameters.values()
        )

    assert "direction" in inspect.signature(gs.Chart.with_scales).parameters
    for method in (
        gs.VConcatChart.resolve_axis,
        gs.VConcatChart.resolve_legend,
        gs.VConcatChart.resolve_scale,
    ):
        assert {"direction", "tooltip"} <= set(inspect.signature(method).parameters)


def test_composition_properties_support_root_level_genomic_config() -> None:
    chart = (
        gs.vconcat(gs.Chart([{"x": 1}]).mark_point().encode(x="x:Q"), spacing=10)
        .properties(
            assembly="hg38",
            scales=gs.scales(
                x=Scale(
                    domain=[
                        {"chrom": "chr1", "pos": 1},
                        {"chrom": "chr1", "pos": 10},
                    ]
                )
            ),
        )
        .resolve_scale(y="independent")
        .resolve_axis(y="independent")
    )

    spec = chart.to_dict()

    assert spec["assembly"] == "hg38"
    assert spec["spacing"] == 10
    assert spec["scales"] == {
        "x": {
            "domain": [
                {"chrom": "chr1", "pos": 1},
                {"chrom": "chr1", "pos": 10},
            ]
        }
    }
    assert spec["resolve"] == {
        "scale": {"y": "independent"},
        "axis": {"y": "independent"},
    }


def test_public_composition_helpers_have_generated_keyword_signatures() -> None:
    signature = inspect.signature(gs.vconcat)

    assert "charts" in signature.parameters
    assert "spacing" in signature.parameters
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    assert "columns" in inspect.signature(gs.concat).parameters
    assert "stops" in inspect.signature(gs.multiscale).parameters
    import_signature = inspect.signature(gs.import_view)
    assert "params" in import_signature.parameters
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in import_signature.parameters.values()
    )


def test_generated_channels_have_explicit_constructor_and_nested_signatures() -> None:
    constructor_signature = inspect.signature(gs.X)
    scale_signature = inspect.signature(gs.X("value:Q").scale)

    assert "field" in constructor_signature.parameters
    assert "scale" in constructor_signature.parameters
    assert "domain" in scale_signature.parameters
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in constructor_signature.parameters.values()
    )
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in scale_signature.parameters.values()
    )


def test_generated_configure_methods_work_on_compositions() -> None:
    chart = (
        gs.vconcat(gs.Chart([{"x": 1}]).mark_point().encode(x="x:Q"))
        .configure_axis_x(labelAngle=0)
        .configure_title(anchor="start")
    )

    spec = chart.to_dict()

    assert spec["config"] == {
        "axisX": {"labelAngle": 0},
        "title": {"anchor": "start"},
    }


def test_layer_chart_supports_top_level_encode() -> None:
    layer_chart = (
        gs.layer(gs.Chart().mark_rule(), gs.Chart().mark_point())
        .encode(x=gs.Locus("chrom", "start"), y=gs.Y("_lane:O").axis(None))
        .properties(data=[{"chrom": "chr1", "start": 1, "_lane": 0}])
    )

    assert layer_chart.to_dict()["encoding"] == {
        "x": {"chrom": "chrom", "pos": "start", "type": "locus"},
        "y": {
            "field": "_lane",
            "type": "ordinal",
            "axis": None,
        },
    }


def test_encode_supports_null_secondary_channels() -> None:
    chart = gs.Chart([{"x": 1}]).mark_rule().encode(x="x:Q", x2=None)

    assert chart.to_dict()["encoding"]["x2"] is None


def test_encode_supports_multi_field_tooltips() -> None:
    chart = (
        gs.Chart([{"base": "A", "score": 1.0}])
        .mark_text()
        .encode(
            text="base:N",
            tooltip=[
                gs.Tooltip("base:N"),
                gs.Tooltip("score:Q"),
            ],
        )
    )

    assert chart.to_dict()["encoding"]["tooltip"] == [
        {"field": "base", "type": "nominal"},
        {"field": "score", "type": "quantitative"},
    ]


def test_templates_accept_chart_objects_without_nested_schema_urls() -> None:
    template = gs.Chart(mark="point")
    chart = gs.vconcat(gs.import_view(template="track")).properties(
        templates={"track": template}
    )

    spec = chart.to_dict()

    assert spec["templates"] == {"track": {"mark": "point"}}
    assert "$schema" not in spec["templates"]["track"]


def test_chart_accepts_schema_data_wrapper() -> None:
    chart = (
        gs.Chart(
            gs.Data(
                url="https://example.test/features.tsv",
                format={"type": "tsv"},
            )
        )
        .mark_rect()
        .encode(x="x:Q", y="y:Q")
    )

    spec = chart.to_dict()

    assert spec["data"] == {
        "url": "https://example.test/features.tsv",
        "format": {"type": "tsv"},
    }


def test_chart_accepts_lazy_data_helper() -> None:
    chart = (
        gs.Chart(gs.lazy.bigwig("https://example.test/signal.bw", pixelsPerBin=1))
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "start"),
            x2=gs.Locus("chrom", "end"),
            y="score:Q",
        )
    )

    spec = chart.to_dict()

    assert spec["data"] == {
        "lazy": {
            "type": "bigwig",
            "url": "https://example.test/signal.bw",
            "pixelsPerBin": 1,
        }
    }


def test_lazy_namespace_supports_generic_and_named_sources() -> None:
    gff3 = gs.lazy.gff3(
        "https://example.test/genes.gff3.gz",
        windowSize=2_000_000,
    )
    custom = gs.lazy.source("indexedFasta", "https://example.test/reference.fa.gz")

    assert gff3.to_dict(validate=False) == {
        "lazy": {
            "type": "gff3",
            "url": "https://example.test/genes.gff3.gz",
            "windowSize": 2_000_000,
        }
    }
    assert custom.to_dict(validate=False) == {
        "lazy": {
            "type": "indexedFasta",
            "url": "https://example.test/reference.fa.gz",
        }
    }


def test_lazy_data_helpers_have_generated_keyword_signatures() -> None:
    bigwig_signature = inspect.signature(gs.lazy.bigwig)
    gff3_signature = inspect.signature(gs.lazy.gff3)

    assert "pixelsPerBin" in bigwig_signature.parameters
    assert "addChrPrefix" in gff3_signature.parameters
    assert "windowSize" in gff3_signature.parameters
    assert hasattr(gs.lazy, "tabix")
    assert {
        "bam",
        "bigbed",
        "bigwig",
        "gff3",
        "indexed_fasta",
        "tabix",
        "vcf",
    } <= set(dir(gs.lazy))
    assert all(
        parameter.kind is not inspect.Parameter.VAR_KEYWORD
        for parameter in bigwig_signature.parameters.values()
    )


def test_generic_transform_appends_raw_mappings() -> None:
    chart = (
        gs.Chart([{"x": 1, "label": "A"}])
        .mark_point()
        .transform(
            {"type": "collect", "sort": {"field": ["x"]}},
            {"type": "project", "fields": ["x", "label"]},
        )
        .encode(x="x:Q")
    )

    spec = chart.to_dict()

    assert spec["transform"] == [
        {"type": "collect", "sort": {"field": ["x"]}},
        {"type": "project", "fields": ["x", "label"]},
    ]


def test_generic_transform_rejects_unsupported_values() -> None:
    with pytest.raises(TypeError, match="Unsupported transform value"):
        gs.Chart([{"x": 1}]).mark_point().transform(42)  # type: ignore[arg-type]


def test_generic_transform_chains_with_existing_helpers() -> None:
    chart = (
        gs.Chart([{"x": 1, "width": 2}])
        .mark_rect()
        .transform_formula(expr="datum.x + datum.width", as_="x2")
        .transform({"type": "filter", "expr": "datum.x2 > 0"})
        .encode(x="x:Q", x2="x2")
    )

    spec = chart.to_dict()

    assert spec["transform"] == [
        {"type": "formula", "expr": "datum.x + datum.width", "as": "x2"},
        {"type": "filter", "expr": "datum.x2 > 0"},
    ]


def test_genomic_transform_helpers_serialize() -> None:
    chart = (
        gs.Chart([{"chrom": "chr1", "start": 10, "end": 20, "label": "A"}])
        .mark_rect()
        .transform_linearize_genomic_coordinate(
            chrom="chrom",
            pos="start",
            as_="_start",
        )
        .transform_collect(sort=gs.compare(["_start"]))
        .transform_pileup(start="_start", end="end", as_="lane")
        .transform_measure_text(field="label", as_="labelWidth", fontSize=11)
        .transform_filter_scored_labels(
            lane="lane",
            score="end",
            width="labelWidth",
            pos="_start",
            padding=4,
        )
        .encode(x="start:Q")
    )

    spec = chart.to_dict()

    assert spec["transform"] == [
        {
            "type": "linearizeGenomicCoordinate",
            "chrom": "chrom",
            "pos": "start",
            "as": "_start",
        },
        {"type": "collect", "sort": {"field": ["_start"]}},
        {"type": "pileup", "start": "_start", "end": "end", "as": "lane"},
        {
            "type": "measureText",
            "field": "label",
            "as": "labelWidth",
            "fontSize": 11,
        },
        {
            "type": "filterScoredLabels",
            "lane": "lane",
            "score": "end",
            "width": "labelWidth",
            "pos": "_start",
            "padding": 4,
        },
    ]


def test_project_and_flatten_helpers_serialize() -> None:
    chart = (
        gs.Chart([{"values": [1, 2], "meta": "x"}])
        .mark_point()
        .transform_project(fields=["values", "meta"], as_=["items", "meta"])
        .transform_flatten(fields=["items"], as_=["item"], index="row")
        .transform_flatten_compressed_exons(start="_start")
        .encode(x="item:Q")
    )

    spec = chart.to_dict()

    assert spec["transform"] == [
        {"type": "project", "fields": ["values", "meta"], "as": ["items", "meta"]},
        {"type": "flatten", "fields": ["items"], "as": ["item"], "index": "row"},
        {"type": "flattenCompressedExons", "start": "_start"},
    ]


def test_additional_transform_helpers_cover_common_docs_patterns() -> None:
    chart = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .transform_coverage(start="start", end="end", as_="coverage", chrom="chrom")
        .transform_flatten()
        .transform_flatten_sequence(field="sequence", as_=["raw_pos", "base"])
        .transform_regex_extract(field="label", regex="^(A)", as_="prefix")
        .encode(x="x:Q")
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "coverage",
            "start": "start",
            "end": "end",
            "as": "coverage",
            "chrom": "chrom",
        },
        {"type": "flatten"},
        {"type": "flattenSequence", "field": "sequence", "as": ["raw_pos", "base"]},
        {"type": "regexExtract", "field": "label", "regex": "^(A)", "as": "prefix"},
    ]


# Adapted from Vega-Altair's tick-mark documentation:
# https://github.com/vega/altair/blob/main/doc/user_guide/marks/tick.rst
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
            sort=gs.compare("site", order="ascending"),
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


def test_locus_interval_chart_serializes_secondary_locus_channel() -> None:
    chart = (
        gs.Chart(
            [{"chrom": "chr1", "start": 100_000, "end": 180_000, "feature": "promoter"}]
        )
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "start").scale(assembly="hg38"),
            x2=gs.Locus("chrom", "end"),
            y=gs.Y("feature:N").scale(reverse=False),
            color="feature:N",
        )
    )

    spec = chart.to_dict()

    assert spec["encoding"]["x"] == {
        "chrom": "chrom",
        "pos": "start",
        "type": "locus",
        "scale": {"assembly": "hg38"},
    }
    assert spec["encoding"]["x2"] == {"chrom": "chrom", "pos": "end"}


def test_y_scale_reverse_is_only_serialized_when_explicit() -> None:
    default_chart = (
        gs.Chart([{"x": 1, "y": 2}])
        .mark_point()
        .encode(x="x:Q", y=gs.Y("y:Q").scale(zero=False))
    )
    chart = (
        gs.Chart([{"x": 1, "y": 2}])
        .mark_point()
        .encode(x="x:Q", y=gs.Y("y:Q").scale(reverse=True))
    )

    assert default_chart.to_dict()["encoding"]["y"]["scale"] == {"zero": False}
    assert chart.to_dict()["encoding"]["y"]["scale"] == {"reverse": True}


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


def test_prepare_render_uses_arrow_without_changing_json_serialization() -> None:
    frame = pl.DataFrame({"x": [1, 2], "label": ["A", "B"]})
    chart = gs.Chart(frame).mark_point().encode(x="x:Q")

    prepared = chart._prepare_render()

    identifier = next(iter(prepared.buffers))
    assert prepared.spec["data"] == {
        "url": f"arrow://{identifier}",
        "format": {"type": "arrow"},
    }
    assert prepared.buffers[identifier] == gs.to_arrow_ipc(frame)
    assert chart.to_dict()["data"] == {
        "values": [{"x": 1, "label": "A"}, {"x": 2, "label": "B"}]
    }


def test_prepare_render_encodes_a_shared_table_once_in_a_composition() -> None:
    frame = pl.DataFrame({"x": [1, 2], "y": [3, 4]})
    calls = 0

    class CountingFrame:
        __module__ = "polars"

        schema = frame.schema

        def write_ipc(self, *, file: object, compression: str) -> bytes:
            nonlocal calls
            calls += 1
            assert file is None
            assert compression == "uncompressed"
            return frame.write_ipc(file=None, compression=compression)

        def to_dicts(self) -> list[dict[str, object]]:
            raise AssertionError("render preparation must not materialize records")

    data = CountingFrame()
    chart = gs.Chart(data).mark_point().encode(x="x", y="y") + gs.Chart(
        data
    ).mark_text().encode(x="x", text="y")

    prepared = chart._prepare_render()

    assert calls == 1
    assert len(prepared.buffers) == 1
    assert prepared.spec["layer"][0]["data"] == prepared.spec["layer"][1]["data"]
    assert prepared.spec["layer"][0]["encoding"]["x"]["type"] == "quantitative"


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


def test_composition_charts_directly_inherit_generated_specs() -> None:
    one = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")
    two = gs.Chart(data=[{"x": 2}]).mark_point().encode(x="x:Q")

    layered = one + two
    horizontal = one | two
    vertical = one & two
    grid = gs.concat(one, two, columns=2)

    assert isinstance(layered, LayerSpec)
    assert isinstance(horizontal, HConcatSpec)
    assert isinstance(vertical, VConcatSpec)
    assert isinstance(grid, ConcatSpec)


def test_composition_charts_preserve_custom_schema_url_on_copy() -> None:
    one = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")
    two = gs.Chart(data=[{"x": 2}]).mark_point().encode(x="x:Q")

    chart = gs.LayerChart(layer=[one], schema_url="https://example.test/schema.json")
    layered = chart + two

    assert layered.to_dict()["$schema"] == "https://example.test/schema.json"


def test_composition_charts_expose_resolution_ergonomics() -> None:
    one = (
        gs.Chart(data=[{"x": 1, "species": "a"}])
        .mark_point()
        .encode(x="x:Q", color="species:N")
    )
    two = (
        gs.Chart(data=[{"x": 2, "species": "b"}])
        .mark_point()
        .encode(x="x:Q", color="species:N")
    )

    chart = (
        (one | two)
        .resolve_scale(x="independent", color="shared")
        .resolve_axis(x="shared")
        .resolve_legend(color="independent")
    )

    spec = chart.to_dict()

    assert spec["resolve"] == {
        "scale": {"x": "independent", "color": "shared"},
        "axis": {"x": "shared"},
        "legend": {"color": "independent"},
    }


def test_composition_resolution_merges_across_repeated_calls() -> None:
    one = gs.Chart(data=[{"x": 1}]).mark_point().encode(x="x:Q")
    two = gs.Chart(data=[{"x": 2}]).mark_point().encode(x="x:Q")

    chart = (one | two).resolve_scale(x="independent").resolve_scale(color="shared")

    assert chart.to_dict()["resolve"] == {
        "scale": {"x": "independent", "color": "shared"}
    }


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


def test_multiscale_helper_serializes_generated_root_variant() -> None:
    overview = gs.Chart(mark="rect")
    detail = gs.Chart(mark="text")

    chart = gs.multiscale(overview, detail, stops=[1])
    spec = chart.to_dict()

    assert isinstance(chart, MultiscaleSpec)
    assert spec["stops"] == [1]
    assert [child["mark"] for child in spec["multiscale"]] == ["rect", "text"]


def test_imported_views_participate_in_composition() -> None:
    reference = gs.import_view(template="allele-track", params={"allele": "ref"})
    alternate = gs.import_view(template="allele-track", params={"allele": "alt"})

    chart = gs.vconcat(
        reference,
        alternate,
        templates={"allele-track": {"mark": "point"}},
    )
    spec = chart.to_dict()

    assert isinstance(reference, ImportSpec)
    assert spec["vconcat"] == [
        {
            "import": {"template": "allele-track"},
            "params": {"allele": "ref"},
        },
        {
            "import": {"template": "allele-track"},
            "params": {"allele": "alt"},
        },
    ]


def test_imported_views_support_altair_style_composition_operators() -> None:
    left = gs.import_view(template="left")
    right = gs.import_view(template="right")

    assert (left + right).to_dict(validate=False)["layer"]
    assert (left & right).to_dict(validate=False)["vconcat"]
    assert (left | right).to_dict(validate=False)["hconcat"]


def test_import_view_requires_exactly_one_source() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        gs.import_view()
    with pytest.raises(ValueError, match="exactly one"):
        gs.import_view(url="track.json", template="track")

    assert gs.import_view(url="track.json").to_dict() == {
        "import": {"url": "track.json"}
    }


def test_from_dict_round_trips_nested_root_variants_without_mutating_input() -> None:
    schema_url = "https://example.test/genome-spy-schema.json"
    original = {
        "$schema": schema_url,
        "templates": {"track": {"mark": "point"}},
        "vconcat": [
            {"import": {"template": "track"}},
            {
                "stops": [1],
                "multiscale": [
                    {"mark": "rect"},
                    {"mark": "text"},
                ],
            },
        ],
    }
    expected = json.loads(json.dumps(original))

    chart = gs.TopLevelSpec.from_dict(original)
    spec = chart.to_dict()

    assert isinstance(chart, gs.VConcatChart)
    assert isinstance(chart._kwds["vconcat"][0], gs.ImportedView)
    assert isinstance(chart._kwds["vconcat"][1], gs.MultiscaleChart)
    assert spec == expected
    assert original == expected


def test_from_json_dispatches_unit_specs_and_rejects_non_objects() -> None:
    chart = gs.Chart.from_json('{"mark": "point"}')

    assert isinstance(chart, gs.Chart)
    assert chart.to_dict(include_schema=False) == {"mark": "point"}

    with pytest.raises(TypeError, match="decode to an object"):
        gs.Chart.from_json("[]")


@pytest.mark.parametrize(
    ("spec", "expected_type"),
    [
        ({"mark": "point"}, gs.Chart),
        ({"layer": [{"mark": "point"}]}, gs.LayerChart),
        ({"stops": [1], "multiscale": [{"mark": "point"}]}, gs.MultiscaleChart),
        ({"vconcat": [{"mark": "point"}]}, gs.VConcatChart),
        ({"hconcat": [{"mark": "point"}]}, gs.HConcatChart),
        ({"columns": 1, "concat": [{"mark": "point"}]}, gs.ConcatChart),
    ],
)
def test_from_dict_dispatches_every_root_variant(
    spec: dict[str, object], expected_type: type[gs.TopLevelSpec]
) -> None:
    chart = gs.TopLevelSpec.from_dict(spec)

    assert isinstance(chart, expected_type)
    assert chart.to_dict(include_schema=False) == spec


def test_from_dict_rejects_standalone_imports() -> None:
    with pytest.raises(ValueError, match="must be nested"):
        gs.TopLevelSpec.from_dict(
            {"import": {"template": "track"}},
            validate=False,
        )


def test_chart_validates_complete_spec_by_default() -> None:
    chart = gs.Chart([{"x": 1}], mark="not-a-mark").encode(x="x:Q")

    with pytest.raises(SchemaValidationError, match="Invalid Root"):
        chart.to_dict()

    assert chart.to_dict(validate=False)["mark"] == "not-a-mark"


def test_secondary_channels_never_carry_type() -> None:
    # x2/y2 only take field/value in GenomeSpy's schema; an inferred `type`
    # there is invalid, so it must be stripped (and the full spec must validate).
    chart = (
        gs.Chart([{"s": 10, "e": 20, "v": 3}])
        .mark_rect()
        .encode(
            x=gs.X("s:Q"),
            x2=gs.X2("e"),
            y=gs.Y("v:Q").scale(reverse=False, zero=True),
            y2=gs.Y2("v"),
        )
    )

    encoding = chart.to_dict()["encoding"]
    assert "type" not in encoding["x2"]
    assert "type" not in encoding["y2"]


def test_key_channel_never_carries_type() -> None:
    chart = (
        gs.Chart([{"id": "a", "value": 1}])
        .mark_point()
        .encode(x="value:Q", key=gs.Key("id"))
    )

    assert chart.to_dict()["encoding"]["key"] == {"field": "id"}
