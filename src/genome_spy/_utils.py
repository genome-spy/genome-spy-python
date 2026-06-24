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
