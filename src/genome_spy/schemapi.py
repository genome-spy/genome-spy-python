"""Runtime primitives for generated GenomeSpy schema wrappers.

Unlike Altair, this small GenomeSpy-specific runtime is maintained directly in
the installable package. Generation tooling imports it from generated classes
but does not maintain a duplicate source copy.
"""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any, ClassVar, Self

from jsonschema import ValidationError
from jsonschema.validators import validator_for


class SchemaValidationError(ValueError):
    """Report a generated-schema validation failure.

    The error retains the original ``jsonschema`` failure and adds the wrapper
    class and failing JSON path to the message.

    Args:
        schema_class: Wrapper class whose schema rejected the instance.
        error: Original JSON Schema validation error.

    Returns:
        A contextual validation exception.

    Raises:
        No exceptions are raised during initialization.

    Example:
        ``SchemaValidationError(UnitSpec, error)``
    """

    def __init__(self, schema_class: type[SchemaBase], error: ValidationError) -> None:
        self.schema_class = schema_class
        self.original = error
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        super().__init__(f"Invalid {schema_class.__name__} at {path}: {error.message}")


class UndefinedType:
    """Sentinel for properties omitted from a serialized spec."""

    def __repr__(self) -> str:
        return "Undefined"


Undefined = UndefinedType()


class SchemaBase:
    """Small base class for future generated GenomeSpy schema wrappers."""

    _schema: ClassVar[dict[str, Any]] = {}
    _rootschema: ClassVar[dict[str, Any]] = {}

    def __init__(self, **kwds: Any) -> None:
        self._kwds = kwds

    def copy(self, *, deep: bool = True, **kwds: Any) -> Self:
        """Return a copy with optional keyword updates."""
        values = deepcopy(self._kwds) if deep else dict(self._kwds)
        merged = {**values, **kwds}
        return self.__class__(**merged)

    def to_dict(self, *, validate: bool = True) -> dict[str, Any]:
        """Serialize this schema wrapper to a JSON-compatible dictionary."""
        result = {
            key: _todict(value)
            for key, value in self._kwds.items()
            if value is not Undefined
        }
        if validate:
            try:
                self.validate(result)
            except ValidationError as error:
                raise SchemaValidationError(type(self), error) from None
        return result

    def to_json(self, *, validate: bool = True) -> str:
        """Serialize this schema wrapper to formatted JSON."""
        return json.dumps(self.to_dict(validate=validate), indent=2)

    @classmethod
    def validate(cls, instance: dict[str, Any]) -> None:
        """Validate an instance against this wrapper's schema."""
        rootschema = cls._rootschema or cls._schema
        validator_class = validator_for(rootschema)
        validator_class.check_schema(rootschema)
        validator = validator_class(rootschema).evolve(schema=cls._schema)
        validator.validate(instance)


def _todict(value: Any) -> Any:
    if isinstance(value, SchemaBase):
        return value.to_dict()
    if isinstance(value, list | tuple):
        return [_todict(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _todict(item) for key, item in value.items() if item is not Undefined
        }
    return value


__all__ = ["SchemaBase", "SchemaValidationError", "Undefined", "UndefinedType"]
