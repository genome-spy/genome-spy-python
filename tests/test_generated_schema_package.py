from __future__ import annotations

from genome_spy.schema import Root, UnitSpec, load_schema


def test_generated_schema_package_loads_real_genomespy_schema() -> None:
    schema = load_schema()

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert len(schema["definitions"]) >= 200
    assert "UnitSpec" in schema["definitions"]


def test_generated_schema_wrappers_serialize_keyword_properties() -> None:
    assert Root(mark="point").to_dict() == {"mark": "point"}
    assert UnitSpec(mark="point", width=320).to_dict() == {
        "mark": "point",
        "width": 320,
    }
