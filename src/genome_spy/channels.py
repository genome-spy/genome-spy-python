"""Channel helpers for the first handwritten GenomeSpy API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, cast

from genome_spy._utils import is_mapping, parse_shorthand
from genome_spy.schema._kwds import CompareParamsKwds
from genome_spy.schema.core import CompareParams
from genome_spy.schema.ergonomics import (
    DatumChannelMethodMixin,
    Locus,
    LocusChannelMethodMixin,
    ValueChannelMethodMixin,
    compare,
    datum,
    locus,
    value,
)
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    merge_mapping_value,
    normalize_schema_value,
)

_MISSING = Undefined

__all__ = [
    "Channel",
    "LocusChannel",
    "Locus",
    "channel",
    "compare",
    "datum",
    "locus",
    "value",
]


@dataclass(frozen=True, slots=True)
class Channel:
    """A serializable GenomeSpy encoding channel definition.

    This class is mostly a small runtime backend for generated channel wrappers
    and the handwritten locus helper, not the main authoring surface users
    should build on directly.
    """

    definition: dict[str, Any] = field(default_factory=dict)
    encoding_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the JSON-serializable channel definition."""
        return dict(self.definition)

    def _with_sort(
        self,
        value: CompareParams | CompareParamsKwds | str | list[str] | None | object,
        /,
        properties: dict[str, Any],
    ) -> Self:
        """Return a channel with a normalized ``sort`` configuration."""
        definition = self.to_dict()
        definition["sort"] = _merge_sort_value(
            definition.get("sort", Undefined),
            value,
            **properties,
        )
        return self._replace_definition(definition)

    def _with_nested(
        self,
        key: str,
        value: SchemaBase | dict[str, Any] | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Self:
        definition = self.to_dict()
        definition[key] = merge_mapping_value(
            definition.get(key, Undefined),
            key,
            value,
            **kwargs,
        )
        return self._replace_definition(definition)

    def _with_property(self, key: str, value: Any) -> Self:
        definition = self.to_dict()
        definition[key] = normalize_schema_value(value, validate=False)
        return self._replace_definition(definition)

    def _replace_definition(self, definition: dict[str, Any]) -> Self:
        if type(self) is Channel:
            return cast(Self, Channel(definition, self.encoding_name))
        return self.__class__(definition)


@dataclass(frozen=True, slots=True)
class LocusChannel(LocusChannelMethodMixin, Channel):
    """A handwritten locus channel with generated-style fluent setters.

    GenomeSpy's genomic locus channels are intentionally kept as a small
    handwritten ergonomic layer rather than forced into the ordinary generated
    channel shape.
    """

    def title(self, value: str | None) -> Self:
        """Return a locus channel with ``title`` updated."""
        return self._with_property("title", value)

    def chrom(self, value: str) -> Self:
        """Return a locus channel with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def pos(self, value: str | None) -> Self:
        """Return a locus channel with ``pos`` updated."""
        return self._with_property("pos", value)

    def offset(self, value: float) -> Self:
        """Return a locus channel with ``offset`` updated."""
        return self._with_property("offset", value)

    def band(self, value: float) -> Self:
        """Return a locus channel with ``band`` updated."""
        return self._with_property("band", value)


@dataclass(frozen=True, slots=True)
class DatumChannel(DatumChannelMethodMixin, Channel):
    """A constant-datum channel with schema-derived fluent methods."""


@dataclass(frozen=True, slots=True)
class ValueChannel(ValueChannelMethodMixin, Channel):
    """A constant-value channel with schema-derived fluent methods."""


def channel(
    value: Channel | SchemaBase | str | dict[str, Any],
    /,
    *,
    encoding_name: str | None = None,
    **kwargs: Any,
) -> Channel:
    """Create a generic channel definition from shorthand or a raw mapping."""
    if isinstance(value, Channel):
        definition = value.to_dict()
        encoding_name = encoding_name or value.encoding_name
    elif isinstance(value, SchemaBase):
        definition = cast(dict[str, Any], normalize_schema_value(value, validate=False))
    elif isinstance(value, str):
        definition = parse_shorthand(value)
    elif is_mapping(value):
        definition = cast(dict[str, Any], normalize_schema_value(value, validate=False))
    else:
        raise TypeError(f"Unsupported channel value: {type(value)!r}")

    definition.update(kwargs)
    return Channel(definition, encoding_name=encoding_name)


def _merge_sort_value(
    current: Any,
    value: CompareParams
    | CompareParamsKwds
    | str
    | list[str]
    | None
    | object = _MISSING,
    /,
    **kwargs: Any,
) -> Any:
    if value is _MISSING or value is None or isinstance(value, CompareParams | dict):
        try:
            return merge_mapping_value(current, "sort", value, **kwargs)
        except TypeError as error:
            message = str(error)
            if "null 'sort'" in message or "non-mapping value" in message:
                raise
            raise TypeError(
                f"Unsupported nested 'sort' value: {type(value)!r}"
            ) from error

    if isinstance(value, str | list):
        if kwargs:
            raise TypeError(
                "Cannot merge keyword properties into simple 'sort' values."
            )
        return normalize_schema_value(value, validate=False)

    raise TypeError(f"Unsupported nested 'sort' value: {type(value)!r}")
