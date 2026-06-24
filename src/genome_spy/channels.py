"""Channel helpers for the first handwritten GenomeSpy API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from genome_spy._utils import is_mapping, parse_shorthand


@dataclass(frozen=True, slots=True)
class Channel:
    """A serializable GenomeSpy encoding channel definition."""

    definition: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the JSON-serializable channel definition."""
        return dict(self.definition)


def channel(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    """Create a channel definition from shorthand or a raw mapping."""
    if isinstance(value, Channel):
        definition = value.to_dict()
    elif isinstance(value, str):
        definition = parse_shorthand(value)
    elif is_mapping(value):
        definition = dict(value)
    else:
        raise TypeError(f"Unsupported channel value: {type(value)!r}")

    definition.update(kwargs)
    return Channel(definition)


def value(value: Any, /, **kwargs: Any) -> Channel:
    """Create a constant-value encoding channel."""
    return Channel({"value": value, **kwargs})


def X(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Y(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def X2(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Y2(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Color(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Size(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Text(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)


def Opacity(value: Channel | str | dict[str, Any], /, **kwargs: Any) -> Channel:
    return channel(value, **kwargs)
