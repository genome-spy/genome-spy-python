from __future__ import annotations

import inspect
import json
import subprocess
import sys
from importlib.resources import files

import genome_spy as gs
import pytest

from genome_spy.schema import (
    AxesKwds,
    CompareParamsKwds,
    HandledTooltipKwds,
    MARK_TYPES,
    ColorSchemeConfig,
    ResolveKwds,
    SCHEMA_VERSION,
    ColorDef,
    GenomeAxis,
    ImportSpec,
    Legend,
    LookupParams,
    PositionDef,
    PointProps,
    Root,
    Scale,
    SchemeParamsKwds,
    UnitSpec,
    ViewOpacityDef,
    load_schema,
)
from genome_spy.schema import channels as generated_channels
from genome_spy.schema.mixins import TransformMethodMixin
from genome_spy.schemapi import SchemaValidationError


def test_package_declares_inline_typing_support() -> None:
    assert files("genome_spy").joinpath("py.typed").is_file()


def test_external_type_checker_sees_generated_public_signatures(tmp_path) -> None:
    consumer = tmp_path / "consumer.py"
    consumer.write_text(
        "\n".join(
            [
                "import genome_spy as gs",
                "chart = gs.Chart().mark_text(size=12).encode(x=gs.X('x:Q'))",
                "gs.vconcat(chart, spacing=2)",
                "gs.Chart().mark_text(size='large')",
                "gs.Chart().properties(layer=[])",
            ]
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", str(consumer)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert 'Argument "size"' in completed.stdout
    assert 'Unexpected keyword argument "layer"' in completed.stdout


def test_generated_schema_package_loads_real_genomespy_schema() -> None:
    schema = load_schema()

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert len(schema["definitions"]) >= 200
    assert "UnitSpec" in schema["definitions"]
    assert MARK_TYPES == ("rect", "point", "rule", "tick", "text", "link", "arrow")
    assert SCHEMA_VERSION == "0.85.0"


def test_generated_schema_wrappers_serialize_keyword_properties() -> None:
    assert Root(mark="point").to_dict() == {"mark": "point"}
    assert UnitSpec(mark="point", width=320).to_dict() == {
        "mark": "point",
        "width": 320,
    }


def test_generated_wrappers_resolve_constructor_properties_through_refs() -> None:
    color = ColorDef(field="species", type="nominal", legend={"title": "Species"})
    position = PositionDef(field="x", type="quantitative", axis={"title": "X axis"})

    assert color.to_dict(validate=False) == {
        "field": "species",
        "type": "nominal",
        "legend": {"title": "Species"},
    }
    assert position.to_dict(validate=False) == {
        "field": "x",
        "type": "quantitative",
        "axis": {"title": "X axis"},
    }

    color_signature = inspect.signature(ColorDef.__init__)
    position_signature = inspect.signature(PositionDef.__init__)

    assert "field" in color_signature.parameters
    assert "legend" in color_signature.parameters
    assert "axis" in position_signature.parameters
    assert "pos" in position_signature.parameters


def test_generated_wrappers_expose_fluent_property_methods() -> None:
    legend = Legend().title("Species legend").padding(8)
    scale = Scale().zero(False).scheme(ColorSchemeConfig(name="blues"))
    axis = GenomeAxis().title("Position axis").grid(True)

    assert legend.to_dict(validate=False) == {"title": "Species legend", "padding": 8}
    assert scale.to_dict(validate=False) == {
        "zero": False,
        "scheme": {"name": "blues"},
    }
    assert axis.to_dict(validate=False) == {
        "title": "Position axis",
        "grid": True,
    }


def test_generated_wrappers_expose_altair_style_property_setters() -> None:
    legend = Legend().title("Species legend").padding(8)
    scale = Scale().zero(False).scheme(name="blues")
    axis = GenomeAxis().title("Position axis").grid(True)

    assert legend.to_dict(validate=False) == {"title": "Species legend", "padding": 8}
    assert scale.to_dict(validate=False) == {
        "zero": False,
        "scheme": {"name": "blues"},
    }
    assert axis.to_dict(validate=False) == {
        "title": "Position axis",
        "grid": True,
    }


def test_generated_wrappers_preserve_python_keyword_properties() -> None:
    import_signature = inspect.signature(ImportSpec.__init__)
    lookup_signature = inspect.signature(LookupParams.__init__)

    imported = ImportSpec(import_={"template": "allele-track"})
    lookup = LookupParams(
        type="lookup",
        from_={"source": "input"},
        key="id",
        as_=["matched_id"],
    )

    assert "import_" in import_signature.parameters
    assert "from_" in lookup_signature.parameters
    assert "as_" in lookup_signature.parameters
    assert imported.to_dict() == {"import": {"template": "allele-track"}}
    assert lookup.to_dict() == {
        "type": "lookup",
        "from": {"source": "input"},
        "key": "id",
        "as": ["matched_id"],
    }


def test_generated_wrappers_nested_methods_merge_helper_kwargs() -> None:
    color = ColorDef(field="species", type="nominal").legend(title="Species")
    position = PositionDef(field="x", type="quantitative").scale(
        Scale(zero=False), padding=4
    )

    assert color.to_dict(validate=False) == {
        "field": "species",
        "type": "nominal",
        "legend": {"title": "Species"},
    }
    assert position.to_dict(validate=False) == {
        "field": "x",
        "type": "quantitative",
        "scale": {"zero": False, "padding": 4},
    }


def test_generated_wrappers_accept_composition_resolution_mappings() -> None:
    axes: AxesKwds = {"x": {"title": "Shared x"}}
    resolve: ResolveKwds = {"scale": {"color": "shared"}}
    spec = (
        UnitSpec(mark="point")
        .axes(axes)
        .legends({"color": {"title": "Species"}})
        .resolve(resolve)
        .scales({"color": {"scheme": "blues"}})
    )

    assert spec.to_dict(validate=False) == {
        "mark": "point",
        "axes": {"x": {"title": "Shared x"}},
        "legends": {"color": {"title": "Species"}},
        "resolve": {"scale": {"color": "shared"}},
        "scales": {"color": {"scheme": "blues"}},
    }


def test_generated_kwds_helpers_cover_repeated_helper_objects() -> None:
    sort: CompareParamsKwds = {"field": "value", "order": "descending"}
    scheme: SchemeParamsKwds = {"name": "blues"}
    tooltip: HandledTooltipKwds = {"handler": "toggleTooltip", "params": {"mode": "x"}}

    point = PointProps(type="point", tooltip=tooltip).to_dict(validate=False)
    opacity = ViewOpacityDef(
        type="viewOpacity",
        values=[0.2, 0.8],
        sort=sort,
    ).to_dict(validate=False)
    scale = Scale(scheme=scheme).to_dict(validate=False)

    assert point["tooltip"] == {
        "handler": "toggleTooltip",
        "params": {"mode": "x"},
    }
    assert opacity == {
        "type": "viewOpacity",
        "values": [0.2, 0.8],
        "sort": {"field": "value", "order": "descending"},
    }
    assert scale == {"scheme": {"name": "blues"}}


def test_generated_schema_wrappers_validate_by_default() -> None:
    with pytest.raises(SchemaValidationError, match="Invalid UnitSpec at mark"):
        UnitSpec(mark="not-a-mark").to_dict()

    assert UnitSpec(mark="not-a-mark").to_dict(validate=False) == {"mark": "not-a-mark"}


def test_generated_schema_copy_is_deep_by_default() -> None:
    original = UnitSpec(mark="point", transform=[{"type": "filter", "expr": "x > 0"}])
    copied = original.copy()

    copied._kwds["transform"][0]["expr"] = "x > 1"

    assert original._kwds["transform"][0]["expr"] == "x > 0"


def test_generated_channels_match_encoding_schema() -> None:
    encoding_names = load_schema()["definitions"]["Encoding"]["properties"]

    assert len(generated_channels.__all__) == len(encoding_names)
    assert {channel.lower() for channel in generated_channels.__all__} == {
        channel.lower() for channel in encoding_names
    }


def test_generated_channels_expose_schema_derived_nested_setters() -> None:
    assert "axis" in generated_channels.X.__dict__
    assert "scale" in generated_channels.X.__dict__
    assert "legend" not in generated_channels.X.__dict__
    assert hasattr(generated_channels.Color("field:N"), "legend")


def test_generated_transform_methods_cover_transform_union() -> None:
    schema = load_schema()
    capabilities = json.loads(
        files("genome_spy.schema")
        .joinpath("capabilities.json")
        .read_text(encoding="utf-8")
    )
    transform_refs = {
        variant["$ref"].rsplit("/", 1)[-1]
        for variant in schema["definitions"]["TransformParams"]["anyOf"]
    }
    generated_refs = {transform["schema"] for transform in capabilities["transforms"]}

    assert generated_refs == transform_refs
    assert all(
        transform["method"] in TransformMethodMixin.__dict__
        for transform in capabilities["transforms"]
    )
    assert all(
        hasattr(gs.Chart, transform["method"])
        for transform in capabilities["transforms"]
    )
    assert set(capabilities["root_spec_variants"]) == {
        "mark",
        "layer",
        "multiscale",
        "vconcat",
        "hconcat",
        "concat",
    }


def test_generated_transform_methods_normalize_python_keywords() -> None:
    signature = inspect.signature(gs.Chart.transform_lookup)
    chart = (
        gs.Chart()
        .mark_point()
        .transform_lookup(
            from_={"data": {"values": [{"id": 1}]}},
            key="id",
            fields=["id"],
        )
        .transform_window(ops=["lead"], fields=["id"], as_=["next_id"])
    )

    assert "from_" in signature.parameters
    assert "type" not in signature.parameters
    assert chart.to_dict(validate=False)["transform"] == [
        {
            "type": "lookup",
            "from": {"data": {"values": [{"id": 1}]}},
            "key": "id",
            "fields": ["id"],
        },
        {
            "type": "window",
            "ops": ["lead"],
            "fields": ["id"],
            "as": ["next_id"],
        },
    ]


def test_generated_filter_rejects_an_empty_predicate() -> None:
    with pytest.raises(TypeError, match="requires an expression or param"):
        gs.Chart().transform_filter()

    assert gs.Chart().transform_filter(param="selected").to_dict(validate=False)[
        "transform"
    ] == [{"type": "filter", "param": "selected"}]
