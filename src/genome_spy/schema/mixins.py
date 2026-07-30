"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from typing import Any, Self

from genome_spy.schemapi import Undefined, use_signature
from genome_spy.schema import core
from genome_spy.schema._kwds import (
    AxisConfigKwds,
    GenomeSpyConfigKwds,
    LegendConfigKwds,
    LinkConfigKwds,
    MarkConfigKwds,
    PointConfigKwds,
    RangeConfigKwds,
    RectConfigKwds,
    RuleConfigKwds,
    ScaleConfigKwds,
    TextConfigKwds,
    TitleConfigKwds,
    ViewConfigKwds,
)


class MarkMethodMixin:
    """Grammar-derived mark methods for the handwritten chart API."""

    @use_signature(core.RectProps)
    def mark_rect(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``rect``."""
        return self._with_mark("rect", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.PointProps)
    def mark_point(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``point``."""
        return self._with_mark("point", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.RuleProps)
    def mark_rule(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``rule``."""
        return self._with_mark("rule", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.TickProps)
    def mark_tick(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``tick``."""
        return self._with_mark("tick", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.TextProps)
    def mark_text(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``text``."""
        return self._with_mark("text", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.LinkProps)
    def mark_link(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``link``."""
        return self._with_mark("link", **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.ArrowProps)
    def mark_arrow(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``arrow``."""
        return self._with_mark("arrow", **kwargs)  # type: ignore[attr-defined, no-any-return]


class ConfigMethodMixin:
    """Schema-derived config methods for the handwritten chart API."""

    @use_signature(core.GenomeSpyConfig)
    def configure(
        self,
        value: core.GenomeSpyConfig | GenomeSpyConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with merged top-level config."""
        return self._configure(value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.ArrowConfig)
    def configure_arrow(
        self,
        value: core.ArrowConfig | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``arrow`` config updated."""
        return self._configure_nested("arrow", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axis`` config updated."""
        return self._configure_nested("axis", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_bottom(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisBottom`` config updated."""
        return self._configure_nested("axisBottom", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_index(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisIndex`` config updated."""
        return self._configure_nested("axisIndex", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_left(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisLeft`` config updated."""
        return self._configure_nested("axisLeft", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_locus(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisLocus`` config updated."""
        return self._configure_nested("axisLocus", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_nominal(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisNominal`` config updated."""
        return self._configure_nested("axisNominal", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_ordinal(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisOrdinal`` config updated."""
        return self._configure_nested("axisOrdinal", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_quantitative(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisQuantitative`` config updated."""
        return self._configure_nested("axisQuantitative", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_right(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisRight`` config updated."""
        return self._configure_nested("axisRight", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_top(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisTop`` config updated."""
        return self._configure_nested("axisTop", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_x(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisX`` config updated."""
        return self._configure_nested("axisX", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.AxisConfig)
    def configure_axis_y(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``axisY`` config updated."""
        return self._configure_nested("axisY", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.LegendConfig)
    def configure_legend(
        self,
        value: core.LegendConfig | LegendConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``legend`` config updated."""
        return self._configure_nested("legend", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.LegendConfig)
    def configure_legend_track(
        self,
        value: core.LegendConfig | LegendConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``legendTrack`` config updated."""
        return self._configure_nested("legendTrack", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.LinkConfig)
    def configure_link(
        self,
        value: core.LinkConfig | LinkConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``link`` config updated."""
        return self._configure_nested("link", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.MarkConfig)
    def configure_mark(
        self,
        value: core.MarkConfig | MarkConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``mark`` config updated."""
        return self._configure_nested("mark", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.PointConfig)
    def configure_point(
        self,
        value: core.PointConfig | PointConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``point`` config updated."""
        return self._configure_nested("point", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.RangeConfig)
    def configure_range(
        self,
        value: core.RangeConfig | RangeConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``range`` config updated."""
        return self._configure_nested("range", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.RectConfig)
    def configure_rect(
        self,
        value: core.RectConfig | RectConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``rect`` config updated."""
        return self._configure_nested("rect", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.RuleConfig)
    def configure_rule(
        self,
        value: core.RuleConfig | RuleConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``rule`` config updated."""
        return self._configure_nested("rule", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.ScaleConfig)
    def configure_scale(
        self,
        value: core.ScaleConfig | ScaleConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``scale`` config updated."""
        return self._configure_nested("scale", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    def configure_style(
        self,
        value: dict[str, Any],
    ) -> Self:
        """Return a chart with ``style`` config updated."""
        return self._configure_property("style", value)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.TextConfig)
    def configure_text(
        self,
        value: core.TextConfig | TextConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``text`` config updated."""
        return self._configure_nested("text", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.TickConfig)
    def configure_tick(
        self,
        value: core.TickConfig | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``tick`` config updated."""
        return self._configure_nested("tick", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.TitleConfig)
    def configure_title(
        self,
        value: core.TitleConfig | TitleConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``title`` config updated."""
        return self._configure_nested("title", value, **kwargs)  # type: ignore[attr-defined, no-any-return]

    @use_signature(core.ViewConfig)
    def configure_view(
        self,
        value: core.ViewConfig | ViewConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a chart with ``view`` config updated."""
        return self._configure_nested("view", value, **kwargs)  # type: ignore[attr-defined, no-any-return]


__all__ = ["ConfigMethodMixin", "MarkMethodMixin"]
