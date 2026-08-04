"""Authoring-edge normalization helpers for the handwritten chart API."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, datetime
from typing import Any, cast

from genome_spy._utils import is_mapping
from genome_spy.channels import Channel, channel
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    normalize_mapping_value,
    normalize_schema_value,
)


def normalize_data(data: Any) -> Any:
    """Normalize Python-side data inputs into schema-compatible values."""
    if data is None:
        return None
    if isinstance(data, SchemaBase):
        return data.to_dict(validate=False)
    records = records_from_data(data)
    if records is not None:
        return records_data(records)
    if is_mapping(data):
        return cast(dict[str, Any], normalize_schema_value(data, validate=False))
    raise TypeError(f"Unsupported data value: {type(data)!r}")


def json_safe(value: Any) -> Any:
    """Convert authoring-edge values into JSON-safe primitives."""
    if value is None:
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, datetime | date):
        return value.isoformat()
    if not isinstance(value, str | bytes) and hasattr(value, "item"):
        try:
            item = value.item()
        except (AttributeError, TypeError, ValueError):
            item = value
        if item is not value:
            return json_safe(item)
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if is_mapping(value):
        return {key: json_safe(item) for key, item in value.items()}
    return value


def records_from_data(data: Any) -> list[dict[str, Any]] | None:
    """Extract record-like rows from common Python table inputs."""
    if isinstance(data, list):
        return data
    if hasattr(data, "to_dicts"):
        records = data.to_dicts()
        if isinstance(records, list):
            return records
        return None
    if is_mapping(data):
        values = data.get("values")
        if isinstance(values, list):
            return values
        return None
    if hasattr(data, "to_dict"):
        try:
            records = data.to_dict(orient="records")
        except TypeError:
            return None
        if isinstance(records, list):
            return records
    return None


def records_data(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Wrap record rows as inline schema data."""
    return {"values": json_safe(records)}


def infer_field_type(field: str, data: Any) -> str | None:
    """Infer a GenomeSpy encoding type from up to the first 100 records."""
    records = records_from_data(data)
    if not records:
        return None

    for row in records[:100]:
        if not is_mapping(row) or field not in row:
            continue
        inferred_type = infer_value_type(row[field])
        if inferred_type is not None:
            return inferred_type
    return None


def infer_value_type(value: Any) -> str | None:
    """Infer a GenomeSpy encoding type for one Python value."""
    if value is None:
        return None
    if isinstance(value, bool):
        return "nominal"
    if isinstance(value, int | float):
        return "quantitative"
    return "nominal"


def normalize_channel(
    name: str,
    value: Channel
    | SchemaBase
    | str
    | dict[str, Any]
    | Sequence[Channel | SchemaBase | str | dict[str, Any]]
    | None,
    *,
    data: Any = None,
) -> dict[str, Any] | list[dict[str, Any]] | None:
    """Normalize one chart encoding channel definition."""
    if value is None:
        return None
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return [channel(item, encoding_name=name).to_dict() for item in value]
    definition = channel(value).to_dict()
    return normalized_channel_definition(name, definition, data=data)


def normalized_channel_definition(
    name: str,
    definition: dict[str, Any],
    *,
    data: Any = None,
) -> dict[str, Any]:
    """Normalize one mapping-form channel definition."""
    normalized = dict(definition)
    if name in {"x2", "y2"}:
        normalized.pop("type", None)
    elif "type" not in normalized and isinstance(normalized.get("field"), str):
        inferred_type = infer_field_type(normalized["field"], data)
        if inferred_type is not None:
            normalized["type"] = inferred_type
    return normalized


def merge_encoding_definitions(
    current_encoding: Any,
    updates: dict[
        str,
        Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None,
    ],
    *,
    data: Any,
) -> dict[str, Any]:
    """Merge and normalize chart encoding updates."""
    merged = {} if current_encoding is Undefined else dict(current_encoding)
    for name, value in updates.items():
        merged[name] = normalize_channel(name, value, data=data)
    return merged


def normalize_transform(transform: SchemaBase | dict[str, Any]) -> dict[str, Any]:
    """Normalize one transform definition."""
    try:
        return normalize_mapping_value(transform, key="transform", validate=False)
    except TypeError as error:
        raise TypeError(f"Unsupported transform value: {type(transform)!r}") from error


def normalize_transform_kwarg(
    value: SchemaBase | dict[str, Any],
    *,
    key: str,
) -> dict[str, Any]:
    """Normalize one nested transform keyword value."""
    return normalize_mapping_value(value, key=key, validate=False)
