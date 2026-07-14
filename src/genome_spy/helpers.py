"""Small ergonomic helpers for common GenomeSpy schema objects.

These mirror Altair's pattern of exposing a small handwritten authoring layer
on top of generated schema wrappers, so docs and examples can avoid repetitive
raw dictionaries.
"""

from __future__ import annotations

from typing import Any, Sequence

from genome_spy.schema.core import (
    DataFormat,
    DynamicOpacity,
    ExprRef,
    Parameter,
    Parse,
    Step,
    Title,
)


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
