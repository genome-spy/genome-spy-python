"""Internal helpers for the first GenomeSpy Python API slice."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

TYPE_ALIASES: dict[str, str] = {
    "q": "quantitative",
    "quantitative": "quantitative",
    "n": "nominal",
    "nominal": "nominal",
    "o": "ordinal",
    "ordinal": "ordinal",
    "i": "index",
    "index": "index",
    "g": "locus",
    "l": "locus",
    "locus": "locus",
}


def compact_json(data: Any) -> str:
    """Serialize JSON using stable, notebook-friendly formatting."""
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def pretty_json(data: Any) -> str:
    """Serialize JSON for user-facing export."""
    return json.dumps(data, indent=2)


class JsonSpec(dict[str, Any]):
    """Dict-like object whose display representation is valid JSON."""

    def __repr__(self) -> str:
        return pretty_json(self)

    def __str__(self) -> str:
        return pretty_json(self)

    def _repr_pretty_(self, printer: Any, cycle: bool) -> None:
        """Pretty-print JSON in IPython/Jupyter text output."""
        if cycle:
            printer.text("JsonSpec(...)")
            return
        printer.text(pretty_json(self))

    def _repr_mimebundle_(
        self,
        include: object | None = None,
        exclude: object | None = None,
    ) -> dict[str, str]:
        """Display as indented JSON text in notebook frontends."""
        del include, exclude
        return {"text/plain": pretty_json(self)}


def is_mapping(value: Any) -> bool:
    """Return whether ``value`` behaves like a mapping."""
    return isinstance(value, Mapping)


def parse_shorthand(shorthand: str) -> dict[str, Any]:
    """Parse a compact ``field:type`` channel shorthand."""
    field, separator, channel_type = shorthand.rpartition(":")
    if not separator:
        return {"field": shorthand}

    normalized_type = TYPE_ALIASES.get(channel_type.lower())
    if normalized_type is None:
        return {"field": shorthand}

    return {"field": field, "type": normalized_type}
