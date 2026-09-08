"""Settings for preparing chart data during serialization."""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import AbstractContextManager
from hashlib import sha256
from typing import Any

from genome_spy.schema.core import _ROOT_SCHEMA
from genome_spy.schemapi import SchemaBase

__all__ = ["DataTransformerSettings", "data_transformers"]


class _RestoreSettings(AbstractContextManager["DataTransformerSettings"]):
    def __init__(self, settings: DataTransformerSettings, previous: bool) -> None:
        self.settings = settings
        self.previous = previous

    def __enter__(self) -> DataTransformerSettings:
        return self.settings

    def __exit__(self, *args: Any) -> None:
        self.settings.consolidate_datasets = self.previous


class DataTransformerSettings:
    """Control whether exported charts share repeated inline tables.

    Description:
        Consolidation is enabled by default. This settings object supports
        dataset consolidation only, not a registry of transformer plugins.

    Example:
        >>> with data_transformers.enable(consolidate_datasets=False):
        ...     spec = chart.to_dict()
    """

    def __init__(self) -> None:
        self._consolidate_datasets = True

    @property
    def consolidate_datasets(self) -> bool:
        """Whether eligible inline tables become shared named datasets."""
        return self._consolidate_datasets

    @consolidate_datasets.setter
    def consolidate_datasets(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("consolidate_datasets must be a boolean.")
        self._consolidate_datasets = value

    def enable(
        self, *, consolidate_datasets: bool = True
    ) -> AbstractContextManager[DataTransformerSettings]:
        """Apply a setting, optionally restoring it after a ``with`` block.

        Description:
            The change takes effect immediately. When used as a context manager,
            the previous value is restored even if the block raises an error.

        Args:
            consolidate_datasets: Whether to share eligible inline tables.

        Returns:
            A context manager that restores the previous setting.

        Raises:
            TypeError: If the setting is not a boolean.

        Example:
            >>> with data_transformers.enable(consolidate_datasets=False):
            ...     spec = chart.to_dict()
        """
        previous = self.consolidate_datasets
        self.consolidate_datasets = consolidate_datasets
        return _RestoreSettings(self, previous)


data_transformers = DataTransformerSettings()


def _schema_parts(
    schema: dict[str, Any], seen: set[int] | None = None
) -> Iterator[dict[str, Any]]:
    """Resolve schema alternatives without descending into instance fields."""
    if seen is None:
        seen = set()
    if id(schema) in seen:
        return
    seen.add(id(schema))
    yield schema
    ref = schema.get("$ref")
    if isinstance(ref, str):
        name = ref.removeprefix("#/definitions/")
        target = _ROOT_SCHEMA.get("definitions", {}).get(name, {})
        yield from _schema_parts(target, seen)
    for keyword in ("anyOf", "oneOf", "allOf"):
        for alternative in schema.get(keyword, []):
            yield from _schema_parts(alternative, seen)


def _data_slots(
    value: Any,
    schema: dict[str, Any] = _ROOT_SCHEMA,
    *,
    owner: str | None = None,
    scoped: bool = False,
    root: bool = True,
) -> Iterator[tuple[str, dict[str, Any], str | None, bool]]:
    """Visit only schema-declared data sources and dataset declarations.

    Open mappings (including rows, metadata, and parameter values) are opaque.
    Schema references also discover sources inside new transform definitions.
    """
    if isinstance(value, SchemaBase):
        value = value._kwds
    if not isinstance(value, (dict, list, tuple)):
        return
    parts = list(_schema_parts(schema))
    source_refs = {"#/definitions/InlineData", "#/definitions/NamedData"}
    if (
        isinstance(value, dict)
        and value.keys() & {"values", "name", "url", "lazy", "sequence"}
        and any(p.get("$ref") in source_refs for p in parts)
    ):
        yield "data", value, owner, scoped
        return
    if isinstance(value, (list, tuple)):
        items = [p["items"] for p in parts if isinstance(p.get("items"), dict)]
        if items:
            for item in value:
                yield from _data_slots(
                    item, {"anyOf": items}, owner=owner, scoped=scoped, root=False
                )
        return
    properties: dict[str, list[dict[str, Any]]] = {}
    for part in parts:
        for key, child_schema in part.get("properties", {}).items():
            properties.setdefault(key, []).append(child_schema)
    if not root and "datasets" in properties and "datasets" in value:
        name = value.get("name")
        owner = name if isinstance(name, str) and name else None
        scoped = True
    for key, child_schemas in properties.items():
        if key not in value:
            continue
        if key == "datasets":
            if isinstance(value[key], dict):
                yield "datasets", value[key], owner, scoped
        else:
            yield from _data_slots(
                value[key],
                {"anyOf": child_schemas},
                owner=owner,
                scoped=scoped,
                root=False,
            )


class _DatasetConsolidation:
    """Collect tables once per serialization, reserving authored names first."""

    def __init__(self, authored: Any) -> None:
        self.reserved: set[str] = set()
        for kind, value, _, _ in _data_slots(authored):
            if kind == "datasets":
                self.reserved.update(value)
            elif isinstance(value.get("name"), str):
                self.reserved.add(value["name"])
        self.names: dict[str, str] = {}
        self.datasets: dict[str, Any] = {}

    def source(self, source: Any) -> Any:
        if not isinstance(source, dict) or set(source) - {"values", "description"}:
            return source
        rows = source.get("values")
        # Non-array and format-bearing sources need their inline loader.
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            return source
        canonical = json.dumps(
            rows, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        name = self.names.get(canonical)
        if name is None:
            base = "data-" + sha256(canonical.encode()).hexdigest()[:32]
            name = base
            suffix = 1
            while name in self.reserved:
                name = f"{base}-{suffix}"
                suffix += 1
            self.reserved.add(name)
            self.names[canonical] = name
            self.datasets[name] = rows
        return {key: value for key, value in source.items() if key != "values"} | {
            "name": name
        }

    def finish(self, spec: dict[str, Any]) -> dict[str, Any]:
        # Also cover raw/generated nested specs and secondary transform inputs.
        for kind, source, _, _ in _data_slots(spec):
            if kind == "data":
                replacement = self.source(source)
                if replacement is not source:
                    source.clear()
                    source.update(replacement)
        if self.datasets:
            spec.setdefault("datasets", {}).update(self.datasets)
        return spec


def _consolidate(spec: dict[str, Any]) -> dict[str, Any]:
    """Consolidate an owned serialized spec without changing authored names."""
    return _DatasetConsolidation(spec).finish(spec)
