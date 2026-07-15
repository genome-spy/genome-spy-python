"""Channel helpers for the first handwritten GenomeSpy API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, cast

from genome_spy._utils import is_mapping, parse_shorthand
from genome_spy.schema._kwds import CompareParamsKwds
from genome_spy.schema._typing import SortOrder_T
from genome_spy.schema.core import CompareParams
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    merge_mapping_value,
    normalize_schema_value,
)

_MISSING = Undefined


@dataclass(frozen=True, slots=True)
class Channel:
    """A serializable GenomeSpy encoding channel definition."""

    definition: dict[str, Any] = field(default_factory=dict)
    encoding_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the JSON-serializable channel definition."""
        return dict(self.definition)

    def title(self, value: str | None) -> Self:
        """Return a channel with a title."""
        definition = self.to_dict()
        definition["title"] = value
        return self._replace_definition(definition)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a channel with a ``sort`` configuration."""
        definition = self.to_dict()
        definition["sort"] = _merge_sort_value(
            definition.get("sort", Undefined),
            value,
            **kwargs,
        )
        return self._replace_definition(definition)

    def axis(
        self,
        value: SchemaBase | dict[str, Any] | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a channel with an ``axis`` configuration."""
        return self._with_nested("axis", value, **kwargs)

    def scale(
        self,
        value: SchemaBase | dict[str, Any] | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a channel with a ``scale`` configuration."""
        return self._with_nested("scale", value, **kwargs)

    def legend(
        self,
        value: SchemaBase | dict[str, Any] | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a channel with a ``legend`` configuration."""
        return self._with_nested("legend", value, **kwargs)

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

    def _replace_definition(self, definition: dict[str, Any]) -> Self:
        if type(self) is Channel:
            return cast(Self, Channel(definition, self.encoding_name))
        return self.__class__(definition)


def channel(
    value: Channel | SchemaBase | str | dict[str, Any],
    /,
    *,
    encoding_name: str | None = None,
    **kwargs: Any,
) -> Channel:
    """Create a channel definition from shorthand or a raw mapping."""
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


def locus(chrom: str, pos: str | None = None, /, **kwargs: Any) -> Channel:
    """Create a GenomeSpy chromosomal locus channel definition."""
    definition: dict[str, Any] = {"chrom": chrom, "type": "locus", **kwargs}
    if pos is not None:
        definition["pos"] = pos
    return Channel(definition)


def value(value: Any, /, **kwargs: Any) -> Channel:
    """Create a constant-value encoding channel."""
    return Channel({"value": value, **kwargs})


def compare(
    field: str | list[str] | None = None,
    /,
    *,
    order: SortOrder_T | list[SortOrder_T] | None = None,
    **kwargs: Any,
) -> CompareParams:
    """Create a sort/compare definition."""
    payload = dict(kwargs)
    if field is not None:
        payload["field"] = field
    if order is not None:
        payload["order"] = order
    return CompareParams(**payload)


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


def Locus(chrom: str, pos: str | None = None, /, **kwargs: Any) -> Channel:
    return locus(chrom, pos, **kwargs)
