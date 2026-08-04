"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Self, Literal

from genome_spy.schema._typing import (
    AggregateOp_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    PrimaryPositionalChannel_T,
    WindowOp_T,
)
from genome_spy.schemapi import Undefined, UndefinedType, use_signature
from genome_spy.schema import core
from genome_spy.schema._kwds import (
    AxisConfigKwds,
    CompareParamsKwds,
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


class TransformMethodMixin:
    """Schema-derived transform methods for top-level specifications."""

    def transform_alignment_mismatches(
        self,
        *,
        cigar: Field_T | UndefinedType = Undefined,
        copyFields: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        md: Field_T | UndefinedType = Undefined,
        quality: Field_T | UndefinedType = Undefined,
        sequence: Field_T | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``alignmentMismatches`` transform."""
        transform: dict[str, Any] = {"type": "alignmentMismatches"}
        if cigar is not Undefined:
            transform["cigar"] = cigar
        if copyFields is not Undefined:
            transform["copyFields"] = copyFields
        if description is not Undefined:
            transform["description"] = description
        if md is not Undefined:
            transform["md"] = md
        if quality is not Undefined:
            transform["quality"] = quality
        if sequence is not Undefined:
            transform["sequence"] = sequence
        if start is not Undefined:
            transform["start"] = start
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_aggregate(
        self,
        *,
        as_: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        ops: Sequence[AggregateOp_T] | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``aggregate`` transform."""
        transform: dict[str, Any] = {"type": "aggregate"}
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if fields is not Undefined:
            transform["fields"] = fields
        if groupby is not Undefined:
            transform["groupby"] = groupby
        if ops is not Undefined:
            transform["ops"] = ops
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_collect(
        self,
        *,
        description: str | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        sort: core.CompareParams | CompareParamsKwds | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``collect`` transform."""
        transform: dict[str, Any] = {"type": "collect"}
        if description is not Undefined:
            transform["description"] = description
        if groupby is not Undefined:
            transform["groupby"] = groupby
        if sort is not Undefined:
            transform["sort"] = sort
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_coverage(
        self,
        *,
        end: Field_T,
        start: Field_T,
        as_: str | UndefinedType = Undefined,
        asChrom: str | UndefinedType = Undefined,
        asEnd: str | UndefinedType = Undefined,
        asStart: str | UndefinedType = Undefined,
        chrom: Field_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        weight: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``coverage`` transform."""
        transform: dict[str, Any] = {"type": "coverage"}
        transform["end"] = end
        transform["start"] = start
        if as_ is not Undefined:
            transform["as"] = as_
        if asChrom is not Undefined:
            transform["asChrom"] = asChrom
        if asEnd is not Undefined:
            transform["asEnd"] = asEnd
        if asStart is not Undefined:
            transform["asStart"] = asStart
        if chrom is not Undefined:
            transform["chrom"] = chrom
        if description is not Undefined:
            transform["description"] = description
        if weight is not Undefined:
            transform["weight"] = weight
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_coordinate_lookup(
        self,
        *,
        from_: core.CoordinateLookupInput | dict[str, Any],
        key: Field_T | Sequence[Field_T],
        as_: Sequence[str] | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        default: Any | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Field_T | Sequence[Field_T] | None | UndefinedType = Undefined,
        values: Sequence[Field_T] | None | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``coordinateLookup`` transform."""
        transform: dict[str, Any] = {"type": "coordinateLookup"}
        transform["from"] = from_
        transform["key"] = key
        if as_ is not Undefined:
            transform["as"] = as_
        if channel is not Undefined:
            transform["channel"] = channel
        if default is not Undefined:
            transform["default"] = default
        if description is not Undefined:
            transform["description"] = description
        if fields is not Undefined:
            transform["fields"] = fields
        if values is not Undefined:
            transform["values"] = values
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten_delimited(
        self,
        *,
        field: Sequence[Field_T] | Field_T,
        separator: Sequence[str] | str,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flattenDelimited`` transform."""
        transform: dict[str, Any] = {"type": "flattenDelimited"}
        transform["field"] = field
        transform["separator"] = separator
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_formula(
        self,
        *,
        as_: str,
        expr: str,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``formula`` transform."""
        transform: dict[str, Any] = {"type": "formula"}
        transform["as"] = as_
        transform["expr"] = expr
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_lookup(
        self,
        *,
        from_: core.UrlData
        | dict[str, Any]
        | core.InlineData
        | core.NamedData
        | core.DynamicCallbackData
        | core.LazyData
        | core.LookupSelfInput,
        key: Field_T | Sequence[Field_T],
        as_: Sequence[str] | UndefinedType = Undefined,
        default: Any | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Field_T | Sequence[Field_T] | None | UndefinedType = Undefined,
        values: Sequence[Field_T] | None | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``lookup`` transform."""
        transform: dict[str, Any] = {"type": "lookup"}
        transform["from"] = from_
        transform["key"] = key
        if as_ is not Undefined:
            transform["as"] = as_
        if default is not Undefined:
            transform["default"] = default
        if description is not Undefined:
            transform["description"] = description
        if fields is not Undefined:
            transform["fields"] = fields
        if values is not Undefined:
            transform["values"] = values
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_filter(
        self,
        expression: str | UndefinedType = Undefined,
        *,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        fields: dict[str, Any] | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``filter`` transform."""
        transform: dict[str, Any] = {"type": "filter"}
        if expression is not Undefined:
            if expr is not Undefined or param is not Undefined:
                raise TypeError("expression cannot be combined with expr or param")
            expr = expression
        if expr is Undefined and param is Undefined:
            raise TypeError("filter requires an expression or param")
        if description is not Undefined:
            transform["description"] = description
        if empty is not Undefined:
            transform["empty"] = empty
        if expr is not Undefined:
            transform["expr"] = expr
        if fields is not Undefined:
            transform["fields"] = fields
        if param is not Undefined:
            transform["param"] = param
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_filter_scored_labels(
        self,
        *,
        pos: Field_T,
        score: Field_T,
        width: Field_T,
        asMidpoint: str | UndefinedType = Undefined,
        channel: Literal["x", "y"] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        lane: Field_T | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        pos2: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``filterScoredLabels`` transform."""
        transform: dict[str, Any] = {"type": "filterScoredLabels"}
        transform["pos"] = pos
        transform["score"] = score
        transform["width"] = width
        if asMidpoint is not Undefined:
            transform["asMidpoint"] = asMidpoint
        if channel is not Undefined:
            transform["channel"] = channel
        if description is not Undefined:
            transform["description"] = description
        if lane is not Undefined:
            transform["lane"] = lane
        if padding is not Undefined:
            transform["padding"] = padding
        if pos2 is not Undefined:
            transform["pos2"] = pos2
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten(
        self,
        *,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        index: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flatten`` transform."""
        transform: dict[str, Any] = {"type": "flatten"}
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if fields is not Undefined:
            transform["fields"] = fields
        if index is not Undefined:
            transform["index"] = index
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten_compressed_exons(
        self,
        *,
        as_: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        exons: Field_T | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flattenCompressedExons`` transform."""
        transform: dict[str, Any] = {"type": "flattenCompressedExons"}
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if exons is not Undefined:
            transform["exons"] = exons
        if start is not Undefined:
            transform["start"] = start
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten_cigar(
        self,
        *,
        cigar: Field_T | UndefinedType = Undefined,
        copyFields: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flattenCigar`` transform."""
        transform: dict[str, Any] = {"type": "flattenCigar"}
        if cigar is not Undefined:
            transform["cigar"] = cigar
        if copyFields is not Undefined:
            transform["copyFields"] = copyFields
        if description is not Undefined:
            transform["description"] = description
        if start is not Undefined:
            transform["start"] = start
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten_sequence(
        self,
        *,
        as_: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flattenSequence`` transform."""
        transform: dict[str, Any] = {"type": "flattenSequence"}
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if field is not Undefined:
            transform["field"] = field
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_identifier(
        self,
        *,
        as_: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``identifier`` transform."""
        transform: dict[str, Any] = {"type": "identifier"}
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_linearize_genomic_coordinate(
        self,
        *,
        as_: str | Sequence[str],
        chrom: Field_T,
        pos: Field_T | Sequence[Field_T],
        channel: Literal["x", "y"] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        offset: float | Sequence[float] | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``linearizeGenomicCoordinate`` transform."""
        transform: dict[str, Any] = {"type": "linearizeGenomicCoordinate"}
        transform["as"] = as_
        transform["chrom"] = chrom
        transform["pos"] = pos
        if channel is not Undefined:
            transform["channel"] = channel
        if description is not Undefined:
            transform["description"] = description
        if offset is not Undefined:
            transform["offset"] = offset
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_measure_text(
        self,
        *,
        as_: str,
        field: Field_T,
        fontSize: float | core.ExprRef | dict[str, Any],
        description: str | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``measureText`` transform."""
        transform: dict[str, Any] = {"type": "measureText"}
        transform["as"] = as_
        transform["field"] = field
        transform["fontSize"] = fontSize
        if description is not Undefined:
            transform["description"] = description
        if font is not Undefined:
            transform["font"] = font
        if fontStyle is not Undefined:
            transform["fontStyle"] = fontStyle
        if fontWeight is not Undefined:
            transform["fontWeight"] = fontWeight
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_truncate_text(
        self,
        *,
        field: Field_T,
        fontSize: float,
        as_: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        ellipsis: str | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        limit: float | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``truncateText`` transform."""
        transform: dict[str, Any] = {"type": "truncateText"}
        transform["field"] = field
        transform["fontSize"] = fontSize
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if ellipsis is not Undefined:
            transform["ellipsis"] = ellipsis
        if font is not Undefined:
            transform["font"] = font
        if fontStyle is not Undefined:
            transform["fontStyle"] = fontStyle
        if fontWeight is not Undefined:
            transform["fontWeight"] = fontWeight
        if limit is not Undefined:
            transform["limit"] = limit
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_pack_legend_labels(
        self,
        *,
        labelWidth: Field_T,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        direction: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        fontSize: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        rowPadding: float | UndefinedType = Undefined,
        symbolOffset: float | UndefinedType = Undefined,
        symbolSize: float | Field_T | UndefinedType = Undefined,
        symbolStrokeWidth: float | Field_T | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        yExtent: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``packLegendLabels`` transform."""
        transform: dict[str, Any] = {"type": "packLegendLabels"}
        transform["labelWidth"] = labelWidth
        if columnPadding is not Undefined:
            transform["columnPadding"] = columnPadding
        if columns is not Undefined:
            transform["columns"] = columns
        if description is not Undefined:
            transform["description"] = description
        if direction is not Undefined:
            transform["direction"] = direction
        if fontSize is not Undefined:
            transform["fontSize"] = fontSize
        if labelOffset is not Undefined:
            transform["labelOffset"] = labelOffset
        if rowPadding is not Undefined:
            transform["rowPadding"] = rowPadding
        if symbolOffset is not Undefined:
            transform["symbolOffset"] = symbolOffset
        if symbolSize is not Undefined:
            transform["symbolSize"] = symbolSize
        if symbolStrokeWidth is not Undefined:
            transform["symbolStrokeWidth"] = symbolStrokeWidth
        if xOffset is not Undefined:
            transform["xOffset"] = xOffset
        if yExtent is not Undefined:
            transform["yExtent"] = yExtent
        if yOffset is not Undefined:
            transform["yOffset"] = yOffset
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_merge_facets(
        self,
        *,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``mergeFacets`` transform."""
        transform: dict[str, Any] = {"type": "mergeFacets"}
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_pileup(
        self,
        *,
        end: Field_T,
        start: Field_T,
        as_: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        preference: Field_T | UndefinedType = Undefined,
        preferredOrder: Sequence[str]
        | Sequence[float]
        | Sequence[bool]
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``pileup`` transform."""
        transform: dict[str, Any] = {"type": "pileup"}
        transform["end"] = end
        transform["start"] = start
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if preference is not Undefined:
            transform["preference"] = preference
        if preferredOrder is not Undefined:
            transform["preferredOrder"] = preferredOrder
        if spacing is not Undefined:
            transform["spacing"] = spacing
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_project(
        self,
        *,
        fields: Sequence[Field_T],
        as_: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``project`` transform."""
        transform: dict[str, Any] = {"type": "project"}
        transform["fields"] = fields
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_regex_extract(
        self,
        *,
        as_: str | Sequence[str],
        field: Field_T,
        regex: str,
        description: str | UndefinedType = Undefined,
        skipInvalidInput: bool | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``regexExtract`` transform."""
        transform: dict[str, Any] = {"type": "regexExtract"}
        transform["as"] = as_
        transform["field"] = field
        transform["regex"] = regex
        if description is not Undefined:
            transform["description"] = description
        if skipInvalidInput is not Undefined:
            transform["skipInvalidInput"] = skipInvalidInput
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_regex_fold(
        self,
        *,
        asValue: Sequence[str] | str,
        columnRegex: Sequence[str] | str,
        asKey: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        skipRegex: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``regexFold`` transform."""
        transform: dict[str, Any] = {"type": "regexFold"}
        transform["asValue"] = asValue
        transform["columnRegex"] = columnRegex
        if asKey is not Undefined:
            transform["asKey"] = asKey
        if description is not Undefined:
            transform["description"] = description
        if skipRegex is not Undefined:
            transform["skipRegex"] = skipRegex
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_sample(
        self,
        *,
        description: str | UndefinedType = Undefined,
        size: float | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``sample`` transform."""
        transform: dict[str, Any] = {"type": "sample"}
        if description is not Undefined:
            transform["description"] = description
        if size is not Undefined:
            transform["size"] = size
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_stack(
        self,
        *,
        groupby: Sequence[Field_T],
        as_: Sequence[str] | UndefinedType = Undefined,
        baseField: Field_T | UndefinedType = Undefined,
        cardinality: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        offset: Literal["zero", "center", "normalize", "information"]
        | UndefinedType = Undefined,
        sort: core.CompareParams | CompareParamsKwds | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``stack`` transform."""
        transform: dict[str, Any] = {"type": "stack"}
        transform["groupby"] = groupby
        if as_ is not Undefined:
            transform["as"] = as_
        if baseField is not Undefined:
            transform["baseField"] = baseField
        if cardinality is not Undefined:
            transform["cardinality"] = cardinality
        if description is not Undefined:
            transform["description"] = description
        if field is not Undefined:
            transform["field"] = field
        if offset is not Undefined:
            transform["offset"] = offset
        if sort is not Undefined:
            transform["sort"] = sort
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_window(
        self,
        *,
        ops: Sequence[WindowOp_T],
        as_: Sequence[str | None] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T | None] | UndefinedType = Undefined,
        frame: Sequence[float | None] | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        ignorePeers: bool | UndefinedType = Undefined,
        params: Sequence[float | None] | UndefinedType = Undefined,
        sort: core.CompareParams | CompareParamsKwds | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``window`` transform."""
        transform: dict[str, Any] = {"type": "window"}
        transform["ops"] = ops
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if fields is not Undefined:
            transform["fields"] = fields
        if frame is not Undefined:
            transform["frame"] = frame
        if groupby is not Undefined:
            transform["groupby"] = groupby
        if ignorePeers is not Undefined:
            transform["ignorePeers"] = ignorePeers
        if params is not Undefined:
            transform["params"] = params
        if sort is not Undefined:
            transform["sort"] = sort
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]


__all__ = ["ConfigMethodMixin", "MarkMethodMixin", "TransformMethodMixin"]
