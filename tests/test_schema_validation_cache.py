"""Schema setup is reusable; every new value and changed schema is still checked."""

from copy import deepcopy
from typing import Any, ClassVar
from unittest.mock import patch

import pytest
from jsonschema import SchemaError
from jsonschema.validators import validator_for

from genome_spy.schemapi import SchemaBase, SchemaValidationError


@pytest.fixture
def wrappers(request):
    """Create two wrappers sharing one schema, independently of other tests' caches."""
    root = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": request.node.name,
        "definitions": {
            "word": {
                "type": "object",
                "properties": {"value": {"type": "string"}},
                "required": ["value"],
            },
            "nested": {
                "type": "object",
                "properties": {"child": {"$ref": "#/definitions/word"}},
                "required": ["child"],
            },
        },
    }

    class Word(SchemaBase):
        _rootschema = root
        _schema: ClassVar[dict[str, Any]] = {"$ref": "#/definitions/word"}

    class Nested(SchemaBase):
        _rootschema = root
        _schema: ClassVar[dict[str, Any]] = {"$ref": "#/definitions/nested"}

    return root, Word, Nested


def test_shared_schema_is_checked_once_but_every_instance_is_validated(wrappers):
    root, Word, Nested = wrappers
    validator = validator_for(root)
    with patch.object(validator, "check_schema", wraps=validator.check_schema) as check:
        assert Word(value="first").to_dict() == {"value": "first"}
        assert Nested(child=Word(value="second")).to_dict() == {
            "child": {"value": "second"}
        }
        with pytest.raises(SchemaValidationError, match="value"):
            Word(value=3).to_dict()
        with pytest.raises(SchemaValidationError, match="child.value"):
            Nested(child={"value": 3}).to_dict()
        assert check.call_count == 1


def test_changed_and_replaced_schemas_are_checked_again(wrappers):
    root, Word, _ = wrappers
    Word(value="before").to_dict()
    root["definitions"]["word"]["properties"]["value"]["type"] = "integer"
    assert Word(value=3).to_dict() == {"value": 3}
    with pytest.raises(SchemaValidationError):
        Word(value="after").to_dict()
    Word._rootschema = deepcopy(root)
    Word._rootschema["definitions"]["word"]["properties"]["value"]["type"] = "boolean"
    assert Word(value=True).to_dict() == {"value": True}
    with pytest.raises(SchemaValidationError):
        Word(value=3).to_dict()


def test_invalid_schema_cannot_reuse_an_earlier_success(wrappers):
    root, Word, _ = wrappers
    Word(value="before").to_dict()
    field = root["definitions"]["word"]["properties"]["value"]
    field["type"] = "not-a-json-schema-type"
    with pytest.raises(SchemaError):
        Word(value="after").to_dict()
    field["type"] = "string"
    assert Word(value="recovered").to_dict() == {"value": "recovered"}
