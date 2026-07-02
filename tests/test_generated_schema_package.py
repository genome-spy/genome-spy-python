from __future__ import annotations

import pytest

from genome_spy.schema import MARK_TYPES, SCHEMA_VERSION, Root, UnitSpec, load_schema
from genome_spy.schema import channels as generated_channels
from genome_spy.schemapi import SchemaValidationError


def test_generated_schema_package_loads_real_genomespy_schema() -> None:
    schema = load_schema()

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert len(schema["definitions"]) >= 200
    assert "UnitSpec" in schema["definitions"]
    assert MARK_TYPES == ("rect", "point", "rule", "tick", "text", "link")
    assert SCHEMA_VERSION == "0.80.0"


def test_generated_schema_wrappers_serialize_keyword_properties() -> None:
    assert Root(mark="point").to_dict() == {"mark": "point"}
    assert UnitSpec(mark="point", width=320).to_dict() == {
        "mark": "point",
        "width": 320,
    }


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
    assert hasattr(generated_channels.X("field:Q"), "axis")
    assert hasattr(generated_channels.X("field:Q"), "scale")
    assert not hasattr(generated_channels.X("field:Q"), "legend")
    assert hasattr(generated_channels.Color("field:N"), "legend")
