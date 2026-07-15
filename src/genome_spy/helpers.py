"""Small ergonomic helpers for common GenomeSpy schema objects.

These mirror Altair's pattern of exposing a small handwritten authoring layer
on top of generated schema wrappers, so docs and examples can avoid repetitive
raw dictionaries.
"""

from __future__ import annotations

from typing import Any, Sequence, cast

from genome_spy.schema._kwds import ScalesKwds
from genome_spy.schema.core import (
    DataFormat,
    DynamicOpacity,
    ExprRef,
    GenomeSpyConfig,
    Parameter,
    Parse,
    Step,
    Title,
    ViewBackground,
    ViewConfig,
)
from genome_spy.schemapi import normalize_schema_value


def expr(expression: str) -> ExprRef:
    """Create a GenomeSpy expression reference."""
    return ExprRef(expr=expression)


def title(text: str, /, **kwargs: Any) -> Title:
    """Create a chart title object."""
    return Title(text=text, **kwargs)


def step(value: float, /) -> Step:
    """Create a step-sized dimension wrapper."""
    return Step(step=value)


def dynamic_opacity(
    *,
    unitsPerPixel: Sequence[float | ExprRef | dict[str, Any]],
    values: Sequence[float],
    channel: str | None = None,
    **kwargs: Any,
) -> DynamicOpacity:
    """Create a zoom-dependent opacity definition."""
    payload: dict[str, Any] = {
        "unitsPerPixel": unitsPerPixel,
        "values": values,
        **kwargs,
    }
    if channel is not None:
        payload["channel"] = channel
    return DynamicOpacity(**payload)


def parse(**kwargs: Any) -> Parse:
    """Create a parse mapping for a data format."""
    return Parse(**kwargs)


def data_format(*, type: str | None = None, **kwargs: Any) -> DataFormat:
    """Create a data-format wrapper."""
    payload = dict(kwargs)
    if type is not None:
        payload["type"] = type
    return DataFormat(**payload)


def param(name: str, /, **kwargs: Any) -> Parameter:
    """Create a parameter definition."""
    return Parameter(name=name, **kwargs)


def scales(**kwargs: Any) -> ScalesKwds:
    """Create top-level shared scale configuration."""
    payload = {
        key: normalize_schema_value(value, validate=False)
        for key, value in kwargs.items()
    }
    return cast(ScalesKwds, payload)


def view(**kwargs: Any) -> ViewBackground:
    """Create a view background configuration."""
    return ViewBackground(**kwargs)


def view_config(**kwargs: Any) -> ViewConfig:
    """Create a top-level view config object.

    Prefer ``chart.configure_view(...)`` when you are authoring chart config
    through the fluent chart API.
    """
    return ViewConfig(**kwargs)


def config(**kwargs: Any) -> GenomeSpyConfig:
    """Create a top-level GenomeSpy config object.

    Prefer generated ``configure(...)`` and ``configure_* (...)`` chart methods
    for fluent authoring on chart objects.
    """
    payload: dict[str, Any] = {}
    for key, value in kwargs.items():
        if key == "view" and isinstance(value, ViewBackground):
            payload[key] = ViewConfig(**value.to_dict(validate=False))
        else:
            payload[key] = normalize_schema_value(value, validate=False)
    return GenomeSpyConfig(**payload)
