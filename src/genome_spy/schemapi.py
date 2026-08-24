"""Runtime primitives for generated GenomeSpy schema wrappers.

Unlike Altair, this small GenomeSpy-specific runtime is maintained directly in
the installable package. Generation tooling imports it from generated classes
but does not maintain a duplicate source copy.

Portions are adapted from Vega-Altair's schema runtime:
https://github.com/vega/altair/blob/main/altair/utils/schemapi.py
Copyright (c) 2015-2025, Vega-Altair Developers. BSD-3-Clause license; see
``LICENSES/ALTAIR-BSD-3-Clause.txt``.
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

    def __deepcopy__(self, memo: dict[int, Any]) -> UndefinedType:
        """Preserve sentinel identity when schema state is deeply copied."""
        del memo
        return self


Undefined = UndefinedType()


class SchemaBase:
    """Small base class for future generated GenomeSpy schema wrappers."""

    _schema: ClassVar[dict[str, Any]] = {}
    _rootschema: ClassVar[dict[str, Any]] = {}

    def __init__(self, **kwds: Any) -> None:
        self._kwds = kwds

    def __getattr__(self, name: str) -> Any:
        """Expose stored schema properties as attributes."""
        if name == "_kwds":
            raise AttributeError(name)
        try:
            return self._kwds[name]
        except KeyError:
            raise AttributeError(name) from None

    def copy(self, *, deep: bool = True, **kwds: Any) -> Self:
        """Return a copy with optional keyword updates."""
        values = deepcopy(self._kwds) if deep else dict(self._kwds)
        merged = {**values, **kwds}
        return self.__class__(**merged)

    def _with_property(
        self, name: str, value: Any = Undefined, /, **kwargs: Any
    ) -> Self:
        """Return a shallow copy with one schema property updated."""
        if kwargs:
            if value is Undefined:
                merged_value: Any = dict(kwargs)
            elif value is None:
                raise TypeError(f"Cannot merge keyword properties into null {name!r}.")
            elif isinstance(value, SchemaBase):
                merged_value = value.to_dict(validate=False)
                merged_value.update(kwargs)
            elif isinstance(value, dict):
                merged_value = dict(value)
                merged_value.update(kwargs)
            else:
                raise TypeError(f"Unsupported nested {name!r} value: {type(value)!r}")
            return self.copy(deep=False, **{name: merged_value})
        return self.copy(deep=False, **{name: value})

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

    @classmethod
    def resolve_references(cls) -> dict[str, Any]:
        """Return this class schema with referenced properties merged in."""
        rootschema = cls._rootschema or cls._schema
        return _resolve_schema_references(cls._schema, rootschema)


def _todict(value: Any) -> Any:
    return normalize_schema_value(value, validate=True)


def normalize_schema_value(value: Any, *, validate: bool = False) -> Any:
    """Recursively convert schema wrappers into plain Python values."""
    if isinstance(value, SchemaBase):
        return value.to_dict(validate=validate)
    if isinstance(value, list | tuple):
        return [normalize_schema_value(item, validate=validate) for item in value]
    if isinstance(value, dict):
        return {
            key: normalize_schema_value(item, validate=validate)
            for key, item in value.items()
            if item is not Undefined
        }
    return value


def normalize_mapping_value(
    value: SchemaBase | dict[str, Any],
    *,
    key: str,
    validate: bool = False,
) -> dict[str, Any]:
    """Convert a schema wrapper or mapping into a plain mapping."""
    normalized = normalize_schema_value(value, validate=validate)
    if not isinstance(normalized, dict):
        raise TypeError(f"Unsupported nested {key!r} value: {type(value)!r}")
    return normalized


def merge_mapping_value(
    current: Any,
    key: str,
    value: Any = Undefined,
    /,
    **kwargs: Any,
) -> Any:
    """Merge a nested schema object using builder-style semantics."""
    if value is Undefined:
        if current is Undefined or current is None:
            return dict(kwargs)
        if isinstance(current, SchemaBase | dict):
            merged = normalize_mapping_value(current, key=key, validate=False)
            merged.update(kwargs)
            return merged
        raise TypeError(f"Cannot merge {key!r} into non-mapping value.")

    if value is None:
        if kwargs:
            raise TypeError(f"Cannot merge keyword properties into null {key!r}.")
        return None

    merged = normalize_mapping_value(value, key=key, validate=False)
    if kwargs:
        merged.update(kwargs)
    return merged


def _ref_name(schema: dict[str, Any]) -> str | None:
    ref = schema.get("$ref")
    if not isinstance(ref, str):
        return None
    return ref.split("/")[-1]


def _resolve_schema_references(
    schema: dict[str, Any],
    rootschema: dict[str, Any],
    *,
    seen: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    ref_name = _ref_name(schema)
    if ref_name is not None:
        definitions = rootschema.get("definitions", {})
        if not isinstance(definitions, dict) or ref_name in seen:
            return {}
        target = definitions.get(ref_name)
        if not isinstance(target, dict):
            return {}
        return _resolve_schema_references(
            target,
            rootschema,
            seen=seen | {ref_name},
        )

    resolved = dict(schema)
    properties: dict[str, Any] = {}
    own_properties = schema.get("properties", {})
    if isinstance(own_properties, dict):
        properties.update(own_properties)
    for key in ("anyOf", "oneOf", "allOf"):
        variants = schema.get(key, [])
        if not isinstance(variants, list):
            continue
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            variant_properties = _resolve_schema_references(
                variant,
                rootschema,
                seen=seen,
            ).get("properties", {})
            if isinstance(variant_properties, dict):
                properties.update(variant_properties)
    if properties:
        resolved["properties"] = properties
    return resolved


__all__ = [
    "merge_mapping_value",
    "normalize_mapping_value",
    "normalize_schema_value",
    "SchemaBase",
    "SchemaValidationError",
    "Undefined",
    "UndefinedType",
]
