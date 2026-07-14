"""Channel helpers for the first handwritten GenomeSpy API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, cast

from genome_spy._utils import is_mapping, parse_shorthand
from genome_spy.schemapi import SchemaBase

_MISSING = object()


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
        if value is _MISSING:
            previous = definition.get(key)
            if previous is None:
                definition[key] = dict(kwargs)
            elif is_mapping(previous):
                definition[key] = {**previous, **kwargs}
            else:
                raise TypeError(f"Cannot merge {key!r} into non-mapping value.")
            return self._replace_definition(definition)

        if value is None:
            if kwargs:
                raise TypeError(f"Cannot merge keyword properties into null {key!r}.")
            definition[key] = None
            return self._replace_definition(definition)

        if isinstance(value, SchemaBase):
            nested = value.to_dict()
        elif is_mapping(value):
            nested = dict(cast(dict[str, Any], value))
        else:
            raise TypeError(f"Unsupported nested {key!r} value: {type(value)!r}")

        if kwargs:
            nested.update(kwargs)
        definition[key] = nested
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
        definition = value.to_dict(validate=False)
    elif isinstance(value, str):
        definition = parse_shorthand(value)
    elif is_mapping(value):
        definition = dict(value)
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


def Locus(chrom: str, pos: str | None = None, /, **kwargs: Any) -> Channel:
    return locus(chrom, pos, **kwargs)
