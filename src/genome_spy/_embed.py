"""Shared rendering configuration for GenomeSpy browser embeds."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, TypeAlias

from genome_spy.schema import SCHEMA_VERSION
from genome_spy.schemapi import Undefined, UndefinedType

ControlName: TypeAlias = Literal["svg", "png", "inspector", "full-window"]
Controls: TypeAlias = bool | ControlName | Sequence[ControlName]

_CONTROL_DEFINITIONS: dict[ControlName, tuple[str, str]] = {
    "svg": ("core", "svgButton"),
    "png": ("core", "pngButton"),
    "inspector": ("inspector", "inspectorButton"),
    "full-window": ("core", "fullWindowButton"),
}
DEFAULT_CONTROLS: tuple[ControlName, ...] = ("svg", "png", "inspector")
SUPPORTED_CONTROLS: tuple[ControlName, ...] = tuple(_CONTROL_DEFINITIONS)

_CORE_PACKAGE_URL = (
    f"https://cdn.jsdelivr.net/npm/@genome-spy/core@{SCHEMA_VERSION}/dist"
)
DEFAULT_EMBED_URL = f"{_CORE_PACKAGE_URL}/bundle/index.es.js"
DEFAULT_CONTROLS_MODULE_URL = f"{_CORE_PACKAGE_URL}/src/controls.js"
DEFAULT_INSPECTOR_MODULE_URL = (
    "https://cdn.jsdelivr.net/npm/"
    f"@genome-spy/inspector@{SCHEMA_VERSION}/dist/index.es.js"
)


def normalize_controls(
    controls: Controls | UndefinedType = Undefined,
) -> tuple[ControlName, ...]:
    """Return validated control names in display order."""
    if controls is Undefined or controls is True:
        return DEFAULT_CONTROLS
    if controls is False:
        return ()

    values: Sequence[str]
    if isinstance(controls, str):
        values = (controls,)
    elif isinstance(controls, Sequence):
        values = controls
    else:
        raise TypeError(
            "controls must be a boolean, a control name, or a sequence of "
            "control names."
        )

    normalized: list[ControlName] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            raise TypeError("Every control name must be a string.")
        if value not in SUPPORTED_CONTROLS:
            expected = ", ".join(repr(name) for name in SUPPORTED_CONTROLS)
            raise ValueError(
                f"Unknown GenomeSpy control {value!r}. Expected one of: {expected}."
            )
        if value in seen:
            raise ValueError(f"GenomeSpy control {value!r} was specified twice.")
        seen.add(value)
        normalized.append(value)
    return tuple(normalized)


def control_definitions() -> dict[str, dict[str, str]]:
    """Return browser module and export metadata for supported controls."""
    return {
        name: {"module": module, "export": export}
        for name, (module, export) in _CONTROL_DEFINITIONS.items()
    }


__all__ = [
    "ControlName",
    "Controls",
    "DEFAULT_CONTROLS",
    "DEFAULT_CONTROLS_MODULE_URL",
    "DEFAULT_EMBED_URL",
    "DEFAULT_INSPECTOR_MODULE_URL",
    "SUPPORTED_CONTROLS",
]
