"""Small ergonomic helpers for common GenomeSpy schema objects.

These mirror Altair's pattern of exposing a small handwritten authoring layer
on top of generated schema wrappers, so docs and examples can avoid repetitive
raw dictionaries.

The module intentionally contains two kinds of helpers:

- tiny readability-first constructors such as ``expr(...)`` and ``title(...)``,
- thin compatibility wrappers around generated config or mapping surfaces such
  as ``config(...)`` and ``scales(...)``.
"""

from __future__ import annotations

from typing import Any, TypedDict, Unpack, cast

from genome_spy.schema._kwds import (
    DataFormatKwds,
    DynamicOpacityKwds,
    GenomeSpyConfigKwds,
    ScalesKwds,
    ViewBackgroundKwds,
    ViewConfigKwds,
)
from genome_spy.schema._typing import ParseValue_T
from genome_spy.schema.core import (
    BindCheckbox,
    BindInput,
    BindRadioSelect,
    BindRange,
    DataFormat,
    DynamicOpacity,
    ExprRef,
    GenomeSpyConfig,
    IntervalSelectionConfig,
    Parameter,
    Parse,
    PointSelectionConfig,
    RulerConfig,
    RulerInitMapping,
    Step,
    Title,
    ViewBackground,
    ViewConfig,
)
from genome_spy.schemapi import normalize_schema_value


class _ParameterHelperKwds(TypedDict, total=False):
    """Typed kwargs accepted by ``param`` beyond the positional name."""

    bind: BindCheckbox | BindRadioSelect | BindRange | BindInput | dict[str, Any]
    description: str
    expr: str
    persist: bool
    push: str
    ruler: RulerConfig | dict[str, Any]
    select: str | PointSelectionConfig | IntervalSelectionConfig | dict[str, Any]
    value: RulerInitMapping | dict[str, Any]


def _normalized_mapping_payload(**kwargs: Any) -> dict[str, Any]:
    """Return schema-normalized key/value pairs for mapping-style helpers."""
    return {
        key: normalize_schema_value(value, validate=False)
        for key, value in kwargs.items()
    }


def _normalized_config_value(key: str, value: Any) -> Any:
    """Return a normalized top-level config value for ``config(...)``."""
    if key == "view" and isinstance(value, ViewBackground):
        return ViewConfig(**value.to_dict(validate=False))
    return normalize_schema_value(value, validate=False)


__all__ = [
    "config",
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


def title(text: str, /, **kwargs: Any) -> Title:
    """Create a chart title object."""
    return Title(text=text, **kwargs)


def step(value: float, /) -> Step:
    """Create a step-sized dimension wrapper."""
    return Step(step=value)


def dynamic_opacity(**kwargs: Unpack[DynamicOpacityKwds]) -> DynamicOpacity:
    """Create a zoom-dependent opacity definition."""
    return DynamicOpacity(**kwargs)


def parse(**kwargs: ParseValue_T) -> Parse:
    """Create a parse mapping for a data format."""
    return Parse(**kwargs)


def data_format(**kwargs: Unpack[DataFormatKwds]) -> DataFormat:
    """Create a data-format wrapper."""
    return DataFormat(**kwargs)


def param(name: str, /, **kwargs: Unpack[_ParameterHelperKwds]) -> Parameter:
    """Create a parameter definition."""
    payload: dict[str, Any] = {"name": name, **kwargs}
    return Parameter(**payload)


# Compatibility wrappers around generated config or mapping-shaped surfaces.


def scales(**kwargs: Unpack[ScalesKwds]) -> ScalesKwds:
    """Create top-level shared scale configuration.

    This remains a small handwritten helper because the schema models shared
    scales as a typed mapping rather than a dedicated wrapper object.
    """
    return cast(ScalesKwds, _normalized_mapping_payload(**kwargs))


def view(**kwargs: Unpack[ViewBackgroundKwds]) -> ViewBackground:
    """Create a view background configuration.

    Prefer ``chart.configure_view(...)`` when the view settings are part of
    top-level chart config rather than the root spec's own ``view`` property.
    """
    return ViewBackground(**kwargs)


def view_config(**kwargs: Unpack[ViewConfigKwds]) -> ViewConfig:
    """Create a top-level view config object.

    Prefer ``chart.configure_view(...)`` when you are authoring chart config
    through the fluent chart API.
    """
    return ViewConfig(**kwargs)


def config(**kwargs: Unpack[GenomeSpyConfigKwds]) -> GenomeSpyConfig:
    """Create a top-level GenomeSpy config object.

    Prefer generated ``configure(...)`` and ``configure_* (...)`` chart methods
    for fluent authoring on chart objects.
    """
    payload = {
        key: _normalized_config_value(key, value) for key, value in kwargs.items()
    }
    return GenomeSpyConfig(**payload)
