"""Small ergonomic helpers for common GenomeSpy schema objects.

These mirror Altair's pattern of exposing a small handwritten authoring layer
on top of generated schema wrappers, so docs and examples can avoid repetitive
raw dictionaries.

The module intentionally contains two kinds of helpers:

- tiny readability-first constructors such as ``expr(...)`` and ``step(...)``,
- generated schema-object constructors and the two mapping-shaped helpers
  whose keys are intentionally open-ended.
"""

from __future__ import annotations

from typing import Any, Unpack, cast, overload

from genome_spy.schema._kwds import AxesKwds, ScalesKwds
from genome_spy.schema._typing import ParseValue_T
from genome_spy.schema.core import (
    ConditionalParameterValueDefNumberExprRef,
    ConditionalParameterValueDefStringNullExprRef,
    ExprRef,
    Parse,
    Step,
)
from genome_spy.schema.ergonomics import (
    config,
    data_format,
    dynamic_opacity,
    param,
    title,
    view,
    view_config,
)
from genome_spy.schemapi import normalize_schema_value


def _normalized_mapping_payload(**kwargs: Any) -> dict[str, Any]:
    """Return schema-normalized key/value pairs for mapping-style helpers."""
    return {
        key: normalize_schema_value(value, validate=False)
        for key, value in kwargs.items()
    }


__all__ = [
    "axes",
    "config",
    "condition",
    "data_format",
    "dynamic_opacity",
    "expr",
    "param",
    "parse",
    "scales",
    "step",
    "title",
    "view",
    "view_config",
]


def expr(expression: str) -> ExprRef:
    """Create a GenomeSpy expression reference."""
    return ExprRef(expr=expression)


def axes(**kwargs: Unpack[AxesKwds]) -> AxesKwds:
    """Create top-level shared axis configuration.

    Args:
        **kwargs: Axis configuration keyed by channel name.

    Returns:
        A normalized typed axis mapping.

    Example:
        >>> axes(x=GenomeAxis(orient="top"))
        {'x': {'orient': 'top'}}
    """
    return cast(AxesKwds, _normalized_mapping_payload(**kwargs))


@overload
def condition(
    param: str, value: float | ExprRef, /, *, empty: bool = True
) -> ConditionalParameterValueDefNumberExprRef: ...


@overload
def condition(
    param: str, value: str | None, /, *, empty: bool = True
) -> ConditionalParameterValueDefStringNullExprRef: ...


def condition(
    param: str, value: float | str | None | ExprRef, /, *, empty: bool = True
) -> (
    ConditionalParameterValueDefNumberExprRef
    | ConditionalParameterValueDefStringNullExprRef
):
    """Create a parameter predicate for a conditional encoding value.

    Args:
        param: Name of the parameter to test.
        value: Visual value applied when the parameter predicate matches.
        empty: Whether an empty parameter selection matches.

    Returns:
        A schema-backed conditional value definition.

    Example:
        >>> condition("hover", 1, empty=False).to_dict()
        {'empty': False, 'param': 'hover', 'value': 1}
    """
    if isinstance(value, str) or value is None:
        return ConditionalParameterValueDefStringNullExprRef(
            param=param, empty=empty, value=value
        )
    return ConditionalParameterValueDefNumberExprRef(
        param=param, empty=empty, value=value
    )


def step(value: float, /) -> Step:
    """Create a step-sized dimension wrapper."""
    return Step(step=value)


def parse(**kwargs: ParseValue_T) -> Parse:
    """Create a parse mapping for a data format."""
    return Parse(**kwargs)


def scales(**kwargs: Unpack[ScalesKwds]) -> ScalesKwds:
    """Create top-level shared scale configuration.

    This remains a small handwritten helper because the schema models shared
    scales as a typed mapping rather than a dedicated wrapper object.
    """
    return cast(ScalesKwds, _normalized_mapping_payload(**kwargs))
