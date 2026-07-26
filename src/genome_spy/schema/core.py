"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
import json
from collections.abc import Sequence
from importlib.resources import files
from typing import Any, cast, Literal

from genome_spy.schema._typing import (
    AggregateOp_T,
    Align_T,
    AxisOrient_T,
    AxisPlacement_T,
    Baseline_T,
    BuiltInThemeName_T,
    ChannelWithScale_T,
    DomEventType_T,
    FieldName_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    LegendDirection_T,
    LegendOrient_T,
    LegendTitleOrient_T,
    MarkType_T,
    PrimaryPositionalChannel_T,
    RulerClear_T,
    RulerDisplay_T,
    RulerEventType_T,
    RulerExtent_T,
    RulerSnap_T,
    RulerSource_T,
    ScalarDomain_T,
    Scalar_T,
    ScaleInterpolate_T,
    ScaleType_T,
    SelectionExtent_T,
    SelectionType_T,
    SortOrder_T,
    TitleAnchor_T,
    TitleFrame_T,
    TitleOrient_T,
    TypeForShape_T,
    Type_T,
)
from genome_spy.schema._kwds import (
    AxesKwds,
    AxisConfigKwds,
    AxisKwds,
    BindCheckboxKwds,
    BindInputKwds,
    BindRadioSelectKwds,
    BindRangeKwds,
    CompareParamsKwds,
    DynamicOpacityKwds,
    EncodingKwds,
    EventConfigKwds,
    GenomeAxisKwds,
    GenomeSpyConfigKwds,
    HandledTooltipKwds,
    LegendConfigKwds,
    LegendKwds,
    LegendsKwds,
    LinkConfigKwds,
    MarkConfigKwds,
    PaddingsKwds,
    ParseKwds,
    PointConfigKwds,
    RangeConfigKwds,
    RectConfigKwds,
    ResolveKwds,
    RuleConfigKwds,
    RulerConfigKwds,
    RulerEventConfigKwds,
    RulerMarkConfigKwds,
    ScaleConfigKwds,
    ScaleInterpolateParamsKwds,
    ScaleKwds,
    ScalesKwds,
    SchemeParamsKwds,
    SeparatorPropsKwds,
    SizeDefKwds,
    StepKwds,
    TextConfigKwds,
    TitleConfigKwds,
    TitleKwds,
    ViewBackgroundKwds,
    ViewConfigKwds,
    ZoomParamsKwds,
)
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    UndefinedType,
    with_property_setters,
)


def load_schema() -> dict[str, Any]:
    """Load the packaged GenomeSpy JSON Schema."""
    schema_path = files(__package__).joinpath("genome-spy-schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise TypeError("Packaged GenomeSpy schema must be a JSON object.")
    return cast(dict[str, Any], schema)


_ROOT_SCHEMA = load_schema()
MARK_TYPES = ("rect", "point", "rule", "tick", "text", "link")


class GenomeSpySchema(SchemaBase):
    """Base class for generated GenomeSpy schema wrappers."""

    _rootschema = _ROOT_SCHEMA


class Root(GenomeSpySchema):
    """Generated wrapper for the root GenomeSpy specification."""

    _schema = _ROOT_SCHEMA

    def __init__(self, **kwds: Any) -> None:
        super().__init__(**kwds)


@with_property_setters
class AggregateOp(GenomeSpySchema):
    """Generated wrapper for ``AggregateOp``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AggregateOp", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class AggregateParams(GenomeSpySchema):
    """Generated wrapper for ``AggregateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AggregateParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        ops: Sequence[AggregateOp_T] | UndefinedType = Undefined,
        type: Literal["aggregate"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, fields=fields, groupby=groupby, ops=ops, type=type
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> AggregateParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(self, value: Sequence[Field_T]) -> AggregateParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_groupby(self, value: Sequence[Field_T]) -> AggregateParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_ops(self, value: Sequence[AggregateOp_T]) -> AggregateParams:
        """Return a copy with ``ops`` updated."""
        return self._with_property("ops", value)

    def with_type(self, value: Literal["aggregate"]) -> AggregateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Align(GenomeSpySchema):
    """Generated wrapper for ``Align``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Align", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class Axis(GenomeSpySchema):
    """Generated wrapper for ``Axis``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Axis", {})

    def __init__(
        self,
        domain: bool | UndefinedType = Undefined,
        domainCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        domainColor: str | UndefinedType = Undefined,
        domainDash: Sequence[float] | UndefinedType = Undefined,
        domainDashOffset: float | UndefinedType = Undefined,
        domainWidth: float | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        grid: bool | UndefinedType = Undefined,
        gridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        gridColor: str | UndefinedType = Undefined,
        gridDash: Sequence[float] | UndefinedType = Undefined,
        gridDashOffset: float | UndefinedType = Undefined,
        gridOpacity: float | UndefinedType = Undefined,
        gridWidth: float | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelAngle: float | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tickDash: Sequence[float] | UndefinedType = Undefined,
        tickDashOffset: float | UndefinedType = Undefined,
        tickMinStep: float | UndefinedType = Undefined,
        tickSize: float | UndefinedType = Undefined,
        tickWidth: float | UndefinedType = Undefined,
        ticks: bool | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleColor: str | UndefinedType = Undefined,
        titleFit: Literal["point", "range"] | UndefinedType = Undefined,
        titleFont: str | UndefinedType = Undefined,
        titleFontSize: float | UndefinedType = Undefined,
        titleFontStyle: FontStyle_T | UndefinedType = Undefined,
        titleFontWeight: FontWeight_T | UndefinedType = Undefined,
        titleOpacity: float | UndefinedType = Undefined,
        titlePadding: float | UndefinedType = Undefined,
        values: Sequence[Any] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            domain=domain,
            domainCap=domainCap,
            domainColor=domainColor,
            domainDash=domainDash,
            domainDashOffset=domainDashOffset,
            domainWidth=domainWidth,
            format=format,
            grid=grid,
            gridCap=gridCap,
            gridColor=gridColor,
            gridDash=gridDash,
            gridDashOffset=gridDashOffset,
            gridOpacity=gridOpacity,
            gridWidth=gridWidth,
            labelAlign=labelAlign,
            labelAngle=labelAngle,
            labelBaseline=labelBaseline,
            labelColor=labelColor,
            labelFont=labelFont,
            labelFontSize=labelFontSize,
            labelFontStyle=labelFontStyle,
            labelFontWeight=labelFontWeight,
            labelLimit=labelLimit,
            labelPadding=labelPadding,
            labels=labels,
            maxExtent=maxExtent,
            minExtent=minExtent,
            offset=offset,
            orient=orient,
            placement=placement,
            style=style,
            tickCap=tickCap,
            tickColor=tickColor,
            tickCount=tickCount,
            tickDash=tickDash,
            tickDashOffset=tickDashOffset,
            tickMinStep=tickMinStep,
            tickSize=tickSize,
            tickWidth=tickWidth,
            ticks=ticks,
            title=title,
            titleColor=titleColor,
            titleFit=titleFit,
            titleFont=titleFont,
            titleFontSize=titleFontSize,
            titleFontStyle=titleFontStyle,
            titleFontWeight=titleFontWeight,
            titleOpacity=titleOpacity,
            titlePadding=titlePadding,
            values=values,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_domain(self, value: bool) -> Axis:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Literal["butt", "round", "square"]) -> Axis:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: str) -> Axis:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Sequence[float]) -> Axis:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: float) -> Axis:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: float) -> Axis:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: str) -> Axis:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: bool) -> Axis:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Literal["butt", "round", "square"]) -> Axis:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: str) -> Axis:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Sequence[float]) -> Axis:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: float) -> Axis:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: float) -> Axis:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: float) -> Axis:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(self, value: Align_T) -> Axis:
        """Return a copy with ``labelAlign`` updated."""
        return self._with_property("labelAlign", value)

    def with_labelAngle(self, value: float) -> Axis:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(self, value: Baseline_T) -> Axis:
        """Return a copy with ``labelBaseline`` updated."""
        return self._with_property("labelBaseline", value)

    def with_labelColor(self, value: str) -> Axis:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: str) -> Axis:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: float) -> Axis:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(self, value: FontStyle_T) -> Axis:
        """Return a copy with ``labelFontStyle`` updated."""
        return self._with_property("labelFontStyle", value)

    def with_labelFontWeight(self, value: FontWeight_T) -> Axis:
        """Return a copy with ``labelFontWeight`` updated."""
        return self._with_property("labelFontWeight", value)

    def with_labelLimit(self, value: float) -> Axis:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: float) -> Axis:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: bool) -> Axis:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: float) -> Axis:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: float) -> Axis:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: float) -> Axis:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: AxisOrient_T) -> Axis:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_placement(self, value: AxisPlacement_T) -> Axis:
        """Return a copy with ``placement`` updated."""
        return self._with_property("placement", value)

    def with_style(self, value: str | Sequence[str] | None) -> Axis:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Literal["butt", "round", "square"]) -> Axis:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: str) -> Axis:
        """Return a copy with ``tickColor`` updated."""
        return self._with_property("tickColor", value)

    def with_tickCount(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``ExprRef`` tickCount."""
        return self._with_property("tickCount", value, **kwargs)

    def with_tickDash(self, value: Sequence[float]) -> Axis:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: float) -> Axis:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: float) -> Axis:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: float) -> Axis:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: float) -> Axis:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: bool) -> Axis:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: str | None) -> Axis:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: str) -> Axis:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Literal["point", "range"]) -> Axis:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: str) -> Axis:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: float) -> Axis:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(self, value: FontStyle_T) -> Axis:
        """Return a copy with ``titleFontStyle`` updated."""
        return self._with_property("titleFontStyle", value)

    def with_titleFontWeight(self, value: FontWeight_T) -> Axis:
        """Return a copy with ``titleFontWeight`` updated."""
        return self._with_property("titleFontWeight", value)

    def with_titleOpacity(self, value: float) -> Axis:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: float) -> Axis:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Sequence[Any]) -> Axis:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: float) -> Axis:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class AxisConfig(GenomeSpySchema):
    """Generated wrapper for ``AxisConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisConfig", {})

    def __init__(
        self,
        chromGrid: bool | UndefinedType = Undefined,
        chromGridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        chromGridColor: str | UndefinedType = Undefined,
        chromGridDash: Sequence[float] | UndefinedType = Undefined,
        chromGridDashOffset: float | UndefinedType = Undefined,
        chromGridFillEven: str | UndefinedType = Undefined,
        chromGridFillOdd: str | UndefinedType = Undefined,
        chromGridOpacity: float | UndefinedType = Undefined,
        chromGridWidth: float | UndefinedType = Undefined,
        chromLabelAlign: Align_T | UndefinedType = Undefined,
        chromLabelColor: str | UndefinedType = Undefined,
        chromLabelFont: str | UndefinedType = Undefined,
        chromLabelFontSize: float | UndefinedType = Undefined,
        chromLabelFontStyle: FontStyle_T | UndefinedType = Undefined,
        chromLabelFontWeight: FontWeight_T | UndefinedType = Undefined,
        chromLabelPadding: float | UndefinedType = Undefined,
        chromLabels: bool | UndefinedType = Undefined,
        chromTickColor: str | UndefinedType = Undefined,
        chromTickDash: Sequence[float] | UndefinedType = Undefined,
        chromTickDashOffset: float | UndefinedType = Undefined,
        chromTickSize: float | UndefinedType = Undefined,
        chromTickWidth: float | UndefinedType = Undefined,
        chromTicks: bool | UndefinedType = Undefined,
        domain: bool | UndefinedType = Undefined,
        domainCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        domainColor: str | UndefinedType = Undefined,
        domainDash: Sequence[float] | UndefinedType = Undefined,
        domainDashOffset: float | UndefinedType = Undefined,
        domainWidth: float | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        grid: bool | UndefinedType = Undefined,
        gridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        gridColor: str | UndefinedType = Undefined,
        gridDash: Sequence[float] | UndefinedType = Undefined,
        gridDashOffset: float | UndefinedType = Undefined,
        gridOpacity: float | UndefinedType = Undefined,
        gridWidth: float | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelAngle: float | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tickDash: Sequence[float] | UndefinedType = Undefined,
        tickDashOffset: float | UndefinedType = Undefined,
        tickMinStep: float | UndefinedType = Undefined,
        tickSize: float | UndefinedType = Undefined,
        tickWidth: float | UndefinedType = Undefined,
        ticks: bool | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleColor: str | UndefinedType = Undefined,
        titleFit: Literal["point", "range"] | UndefinedType = Undefined,
        titleFont: str | UndefinedType = Undefined,
        titleFontSize: float | UndefinedType = Undefined,
        titleFontStyle: FontStyle_T | UndefinedType = Undefined,
        titleFontWeight: FontWeight_T | UndefinedType = Undefined,
        titleOpacity: float | UndefinedType = Undefined,
        titlePadding: float | UndefinedType = Undefined,
        values: Sequence[Any] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            chromGrid=chromGrid,
            chromGridCap=chromGridCap,
            chromGridColor=chromGridColor,
            chromGridDash=chromGridDash,
            chromGridDashOffset=chromGridDashOffset,
            chromGridFillEven=chromGridFillEven,
            chromGridFillOdd=chromGridFillOdd,
            chromGridOpacity=chromGridOpacity,
            chromGridWidth=chromGridWidth,
            chromLabelAlign=chromLabelAlign,
            chromLabelColor=chromLabelColor,
            chromLabelFont=chromLabelFont,
            chromLabelFontSize=chromLabelFontSize,
            chromLabelFontStyle=chromLabelFontStyle,
            chromLabelFontWeight=chromLabelFontWeight,
            chromLabelPadding=chromLabelPadding,
            chromLabels=chromLabels,
            chromTickColor=chromTickColor,
            chromTickDash=chromTickDash,
            chromTickDashOffset=chromTickDashOffset,
            chromTickSize=chromTickSize,
            chromTickWidth=chromTickWidth,
            chromTicks=chromTicks,
            domain=domain,
            domainCap=domainCap,
            domainColor=domainColor,
            domainDash=domainDash,
            domainDashOffset=domainDashOffset,
            domainWidth=domainWidth,
            format=format,
            grid=grid,
            gridCap=gridCap,
            gridColor=gridColor,
            gridDash=gridDash,
            gridDashOffset=gridDashOffset,
            gridOpacity=gridOpacity,
            gridWidth=gridWidth,
            labelAlign=labelAlign,
            labelAngle=labelAngle,
            labelBaseline=labelBaseline,
            labelColor=labelColor,
            labelFont=labelFont,
            labelFontSize=labelFontSize,
            labelFontStyle=labelFontStyle,
            labelFontWeight=labelFontWeight,
            labelLimit=labelLimit,
            labelPadding=labelPadding,
            labels=labels,
            maxExtent=maxExtent,
            minExtent=minExtent,
            offset=offset,
            orient=orient,
            placement=placement,
            style=style,
            tickCap=tickCap,
            tickColor=tickColor,
            tickCount=tickCount,
            tickDash=tickDash,
            tickDashOffset=tickDashOffset,
            tickMinStep=tickMinStep,
            tickSize=tickSize,
            tickWidth=tickWidth,
            ticks=ticks,
            title=title,
            titleColor=titleColor,
            titleFit=titleFit,
            titleFont=titleFont,
            titleFontSize=titleFontSize,
            titleFontStyle=titleFontStyle,
            titleFontWeight=titleFontWeight,
            titleOpacity=titleOpacity,
            titlePadding=titlePadding,
            values=values,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_chromGrid(self, value: bool) -> AxisConfig:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(
        self, value: Literal["butt", "round", "square"]
    ) -> AxisConfig:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: str) -> AxisConfig:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Sequence[float]) -> AxisConfig:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: float) -> AxisConfig:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: str) -> AxisConfig:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: str) -> AxisConfig:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: float) -> AxisConfig:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: float) -> AxisConfig:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(self, value: Align_T) -> AxisConfig:
        """Return a copy with ``chromLabelAlign`` updated."""
        return self._with_property("chromLabelAlign", value)

    def with_chromLabelColor(self, value: str) -> AxisConfig:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: str) -> AxisConfig:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: float) -> AxisConfig:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(self, value: FontStyle_T) -> AxisConfig:
        """Return a copy with ``chromLabelFontStyle`` updated."""
        return self._with_property("chromLabelFontStyle", value)

    def with_chromLabelFontWeight(self, value: FontWeight_T) -> AxisConfig:
        """Return a copy with ``chromLabelFontWeight`` updated."""
        return self._with_property("chromLabelFontWeight", value)

    def with_chromLabelPadding(self, value: float) -> AxisConfig:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: bool) -> AxisConfig:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: str) -> AxisConfig:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Sequence[float]) -> AxisConfig:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: float) -> AxisConfig:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: float) -> AxisConfig:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: float) -> AxisConfig:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: bool) -> AxisConfig:
        """Return a copy with ``chromTicks`` updated."""
        return self._with_property("chromTicks", value)

    def with_domain(self, value: bool) -> AxisConfig:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Literal["butt", "round", "square"]) -> AxisConfig:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: str) -> AxisConfig:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Sequence[float]) -> AxisConfig:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: float) -> AxisConfig:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: float) -> AxisConfig:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: str) -> AxisConfig:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: bool) -> AxisConfig:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Literal["butt", "round", "square"]) -> AxisConfig:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: str) -> AxisConfig:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Sequence[float]) -> AxisConfig:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: float) -> AxisConfig:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: float) -> AxisConfig:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: float) -> AxisConfig:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(self, value: Align_T) -> AxisConfig:
        """Return a copy with ``labelAlign`` updated."""
        return self._with_property("labelAlign", value)

    def with_labelAngle(self, value: float) -> AxisConfig:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(self, value: Baseline_T) -> AxisConfig:
        """Return a copy with ``labelBaseline`` updated."""
        return self._with_property("labelBaseline", value)

    def with_labelColor(self, value: str) -> AxisConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: str) -> AxisConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: float) -> AxisConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(self, value: FontStyle_T) -> AxisConfig:
        """Return a copy with ``labelFontStyle`` updated."""
        return self._with_property("labelFontStyle", value)

    def with_labelFontWeight(self, value: FontWeight_T) -> AxisConfig:
        """Return a copy with ``labelFontWeight`` updated."""
        return self._with_property("labelFontWeight", value)

    def with_labelLimit(self, value: float) -> AxisConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: float) -> AxisConfig:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: bool) -> AxisConfig:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: float) -> AxisConfig:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: float) -> AxisConfig:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: float) -> AxisConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: AxisOrient_T) -> AxisConfig:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_placement(self, value: AxisPlacement_T) -> AxisConfig:
        """Return a copy with ``placement`` updated."""
        return self._with_property("placement", value)

    def with_style(self, value: str | Sequence[str] | None) -> AxisConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Literal["butt", "round", "square"]) -> AxisConfig:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: str) -> AxisConfig:
        """Return a copy with ``tickColor`` updated."""
        return self._with_property("tickColor", value)

    def with_tickCount(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``ExprRef`` tickCount."""
        return self._with_property("tickCount", value, **kwargs)

    def with_tickDash(self, value: Sequence[float]) -> AxisConfig:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: float) -> AxisConfig:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: float) -> AxisConfig:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: float) -> AxisConfig:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: float) -> AxisConfig:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: bool) -> AxisConfig:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: str | None) -> AxisConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: str) -> AxisConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Literal["point", "range"]) -> AxisConfig:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: str) -> AxisConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: float) -> AxisConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(self, value: FontStyle_T) -> AxisConfig:
        """Return a copy with ``titleFontStyle`` updated."""
        return self._with_property("titleFontStyle", value)

    def with_titleFontWeight(self, value: FontWeight_T) -> AxisConfig:
        """Return a copy with ``titleFontWeight`` updated."""
        return self._with_property("titleFontWeight", value)

    def with_titleOpacity(self, value: float) -> AxisConfig:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: float) -> AxisConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Sequence[Any]) -> AxisConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: float) -> AxisConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class AxisGenomeData(GenomeSpySchema):
    """Generated wrapper for ``AxisGenomeData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisGenomeData", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        type: Literal["axisGenome"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> AxisGenomeData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_type(self, value: Literal["axisGenome"]) -> AxisGenomeData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class AxisOrient(GenomeSpySchema):
    """Generated wrapper for ``AxisOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class AxisPlacement(GenomeSpySchema):
    """Generated wrapper for ``AxisPlacement``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisPlacement", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class AxisTicksData(GenomeSpySchema):
    """Generated wrapper for ``AxisTicksData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisTicksData", {})

    def __init__(
        self,
        axis: Axis | AxisKwds | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        type: Literal["axisTicks"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(axis=axis, channel=channel, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: Axis | AxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisTicksData:
        """Return a copy with a ``Axis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> AxisTicksData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_type(self, value: Literal["axisTicks"]) -> AxisTicksData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class BamData(GenomeSpySchema):
    """Generated wrapper for ``BamData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BamData", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        type: Literal["bam"] | UndefinedType = Undefined,
        url: str | ExprRef | dict[str, Any] | UrlTemplate | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            indexUrl=indexUrl,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> BamData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BamData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BamData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> BamData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> BamData:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_type(self, value: Literal["bam"]) -> BamData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(self, value: str | ExprRef | dict[str, Any] | UrlTemplate) -> BamData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(self, value: float) -> BamData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class Baseline(GenomeSpySchema):
    """Generated wrapper for ``Baseline``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Baseline", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class BedDataFormat(GenomeSpySchema):
    """Generated wrapper for ``BedDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BedDataFormat", {})

    def __init__(
        self,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: Literal["bed"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BedDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Literal["bed"]) -> BedDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class BedpeDataFormat(GenomeSpySchema):
    """Generated wrapper for ``BedpeDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BedpeDataFormat", {})

    def __init__(
        self,
        columns: Sequence[str] | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: Literal["bedpe"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_columns(self, value: Sequence[str]) -> BedpeDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BedpeDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Literal["bedpe"]) -> BedpeDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class BigBedData(GenomeSpySchema):
    """Generated wrapper for ``BigBedData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BigBedData", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        type: Literal["bigbed"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> BigBedData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> BigBedData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_type(self, value: Literal["bigbed"]) -> BigBedData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> BigBedData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``ExprRef`` windowSize."""
        return self._with_property("windowSize", value, **kwargs)


@with_property_setters
class BigWigData(GenomeSpySchema):
    """Generated wrapper for ``BigWigData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BigWigData", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        pixelsPerBin: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        type: Literal["bigwig"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            pixelsPerBin=pixelsPerBin,
            type=type,
            url=url,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> BigWigData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigWigData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigWigData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> BigWigData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_pixelsPerBin(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigWigData:
        """Return a copy with a ``ExprRef`` pixelsPerBin."""
        return self._with_property("pixelsPerBin", value, **kwargs)

    def with_type(self, value: Literal["bigwig"]) -> BigWigData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> BigWigData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class BindCheckbox(GenomeSpySchema):
    """Generated wrapper for ``BindCheckbox``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindCheckbox", {})

    def __init__(
        self,
        debounce: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        input: Literal["checkbox"] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            debounce=debounce, description=description, input=input, name=name
        )
        if kwds:
            self._kwds.update(kwds)

    def with_debounce(self, value: float) -> BindCheckbox:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: str) -> BindCheckbox:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Literal["checkbox"]) -> BindCheckbox:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_name(self, value: str) -> BindCheckbox:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class BindInput(GenomeSpySchema):
    """Generated wrapper for ``BindInput``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindInput", {})

    def __init__(
        self,
        autocomplete: str | UndefinedType = Undefined,
        debounce: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        input: Literal["text", "number", "color"] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        placeholder: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            autocomplete=autocomplete,
            debounce=debounce,
            description=description,
            input=input,
            name=name,
            placeholder=placeholder,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_autocomplete(self, value: str) -> BindInput:
        """Return a copy with ``autocomplete`` updated."""
        return self._with_property("autocomplete", value)

    def with_debounce(self, value: float) -> BindInput:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: str) -> BindInput:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Literal["text", "number", "color"]) -> BindInput:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_name(self, value: str) -> BindInput:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_placeholder(self, value: str) -> BindInput:
        """Return a copy with ``placeholder`` updated."""
        return self._with_property("placeholder", value)


@with_property_setters
class BindRadioSelect(GenomeSpySchema):
    """Generated wrapper for ``BindRadioSelect``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindRadioSelect", {})

    def __init__(
        self,
        debounce: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        input: Literal["radio", "select"] | UndefinedType = Undefined,
        labels: Sequence[str] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        options: Sequence[Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            debounce=debounce,
            description=description,
            input=input,
            labels=labels,
            name=name,
            options=options,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_debounce(self, value: float) -> BindRadioSelect:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: str) -> BindRadioSelect:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Literal["radio", "select"]) -> BindRadioSelect:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_labels(self, value: Sequence[str]) -> BindRadioSelect:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_name(self, value: str) -> BindRadioSelect:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_options(self, value: Sequence[Any]) -> BindRadioSelect:
        """Return a copy with ``options`` updated."""
        return self._with_property("options", value)


@with_property_setters
class BindRange(GenomeSpySchema):
    """Generated wrapper for ``BindRange``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindRange", {})

    def __init__(
        self,
        debounce: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        input: Literal["range"] | UndefinedType = Undefined,
        max: float | UndefinedType = Undefined,
        min: float | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        step: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            debounce=debounce,
            description=description,
            input=input,
            max=max,
            min=min,
            name=name,
            step=step,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_debounce(self, value: float) -> BindRange:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: str) -> BindRange:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Literal["range"]) -> BindRange:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_max(self, value: float) -> BindRange:
        """Return a copy with ``max`` updated."""
        return self._with_property("max", value)

    def with_min(self, value: float) -> BindRange:
        """Return a copy with ``min`` updated."""
        return self._with_property("min", value)

    def with_name(self, value: str) -> BindRange:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_step(self, value: float) -> BindRange:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


@with_property_setters
class Binding(GenomeSpySchema):
    """Generated wrapper for ``Binding``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Binding", {})

    def __init__(
        self,
        autocomplete: str | UndefinedType = Undefined,
        debounce: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        input: Literal["text", "number", "color"] | UndefinedType = Undefined,
        labels: Sequence[str] | UndefinedType = Undefined,
        max: float | UndefinedType = Undefined,
        min: float | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        options: Sequence[Any] | UndefinedType = Undefined,
        placeholder: str | UndefinedType = Undefined,
        step: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            autocomplete=autocomplete,
            debounce=debounce,
            description=description,
            input=input,
            labels=labels,
            max=max,
            min=min,
            name=name,
            options=options,
            placeholder=placeholder,
            step=step,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_autocomplete(self, value: str) -> Binding:
        """Return a copy with ``autocomplete`` updated."""
        return self._with_property("autocomplete", value)

    def with_debounce(self, value: float) -> Binding:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: str) -> Binding:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Literal["text", "number", "color"]) -> Binding:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_labels(self, value: Sequence[str]) -> Binding:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_max(self, value: float) -> Binding:
        """Return a copy with ``max`` updated."""
        return self._with_property("max", value)

    def with_min(self, value: float) -> Binding:
        """Return a copy with ``min`` updated."""
        return self._with_property("min", value)

    def with_name(self, value: str) -> Binding:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_options(self, value: Sequence[Any]) -> Binding:
        """Return a copy with ``options`` updated."""
        return self._with_property("options", value)

    def with_placeholder(self, value: str) -> Binding:
        """Return a copy with ``placeholder`` updated."""
        return self._with_property("placeholder", value)

    def with_step(self, value: float) -> Binding:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


@with_property_setters
class BrushConfig(GenomeSpySchema):
    """Generated wrapper for ``BrushConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BrushConfig", {})

    def __init__(
        self,
        clip: bool | Literal["never"] | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        measure: Literal["none", "inside", "outside"] | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeOpacity: float | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            clip=clip,
            cursor=cursor,
            fill=fill,
            fillOpacity=fillOpacity,
            measure=measure,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_clip(self, value: bool | Literal["never"]) -> BrushConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_fill(self, value: str) -> BrushConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: float) -> BrushConfig:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_measure(self, value: Literal["none", "inside", "outside"]) -> BrushConfig:
        """Return a copy with ``measure`` updated."""
        return self._with_property("measure", value)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BrushConfig:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_stroke(self, value: str) -> BrushConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: float) -> BrushConfig:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: float) -> BrushConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_zindex(self, value: float) -> BrushConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class BuiltInThemeName(GenomeSpySchema):
    """Generated wrapper for ``BuiltInThemeName``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BuiltInThemeName", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ChannelWithScale(GenomeSpySchema):
    """Generated wrapper for ``ChannelWithScale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChannelWithScale", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ChromPosDef(GenomeSpySchema):
    """Generated wrapper for ``ChromPosDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChromPosDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        chrom: FieldName_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        pos: FieldName_T | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Literal["locus"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            chrom=chrom,
            description=description,
            domainInert=domainInert,
            offset=offset,
            pos=pos,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> ChromPosDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(self, value: FieldName_T) -> ChromPosDef:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_description(self, value: str) -> ChromPosDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ChromPosDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_offset(self, value: float) -> ChromPosDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(self, value: FieldName_T) -> ChromPosDef:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> ChromPosDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ChromPosDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Literal["locus"]) -> ChromPosDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ChromosomalLocus(GenomeSpySchema):
    """Generated wrapper for ``ChromosomalLocus``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChromosomalLocus", {})

    def __init__(
        self,
        chrom: str | UndefinedType = Undefined,
        pos: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)

    def with_chrom(self, value: str) -> ChromosomalLocus:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_pos(self, value: float) -> ChromosomalLocus:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)


@with_property_setters
class CollectParams(GenomeSpySchema):
    """Generated wrapper for ``CollectParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CollectParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        sort: CompareParams | CompareParamsKwds | UndefinedType = Undefined,
        type: Literal["collect"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, groupby=groupby, sort=sort, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> CollectParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_groupby(self, value: Sequence[Field_T]) -> CollectParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_sort(
        self,
        value: CompareParams | CompareParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CollectParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_type(self, value: Literal["collect"]) -> CollectParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ColorDef(GenomeSpySchema):
    """Generated wrapper for ``ColorDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ColorDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ColorDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> ColorDef:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> ColorDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> ColorDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ColorDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> ColorDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> ColorDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> ColorDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ColorDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ColorDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ColorSchemeConfig(GenomeSpySchema):
    """Generated wrapper for ``ColorSchemeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ColorSchemeConfig", {})

    def __init__(
        self,
        count: float | UndefinedType = Undefined,
        extent: Sequence[float] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(count=count, extent=extent, name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_count(self, value: float) -> ColorSchemeConfig:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_extent(self, value: Sequence[float]) -> ColorSchemeConfig:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_name(self, value: str) -> ColorSchemeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class CompareParams(GenomeSpySchema):
    """Generated wrapper for ``CompareParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CompareParams", {})

    def __init__(
        self,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(field=field, order=order)
        if kwds:
            self._kwds.update(kwds)

    def with_field(self, value: Sequence[Field_T] | Field_T) -> CompareParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_order(self, value: Sequence[SortOrder_T] | SortOrder_T) -> CompareParams:
        """Return a copy with ``order`` updated."""
        return self._with_property("order", value)


@with_property_setters
class ComplexDomain(GenomeSpySchema):
    """Generated wrapper for ``ComplexDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ComplexDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``ConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ConcatSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        concat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            columns=columns,
            concat=concat,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            height=height,
            legends=legends,
            name=name,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            separator=separator,
            spacing=spacing,
            templates=templates,
            title=title,
            transform=transform,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> ConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> ConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: float) -> ConcatSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> ConcatSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> ConcatSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> ConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: LegendsKwds) -> ConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: str) -> ConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> ConcatSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> ConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> ConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> ConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | SeparatorPropsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: float) -> ConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: dict[str, Any]) -> ConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> ConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> ConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class ConditionalMarkPropExprDefType(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropExprDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropExprDef<Type>>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            description=description,
            domainInert=domainInert,
            empty=empty,
            expr=expr,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: str) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: str) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalMarkPropExprDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropExprDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropExprDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            description=description,
            domainInert=domainInert,
            empty=empty,
            expr=expr,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: str) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: str) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalMarkPropFieldDefType(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropFieldDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropFieldDef<Type>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            domainInert=domainInert,
            empty=empty,
            field=field,
            format=format,
            legend=legend,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: str) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: str) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalMarkPropFieldDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropFieldDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropFieldDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: TypeForShape_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            domainInert=domainInert,
            empty=empty,
            field=field,
            format=format,
            legend=legend,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: str) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: str) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: TypeForShape_T
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalScaleDatumDef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ScaleDatumDef>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Conditional<ScaleDatumDef>", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            datum=datum,
            description=description,
            domainInert=domainInert,
            empty=empty,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ConditionalScaleDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> ConditionalScaleDatumDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> ConditionalScaleDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalScaleDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalScaleDatumDef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalScaleDatumDef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalScaleDatumDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalScaleDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalScaleDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalScaleDatumDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalValueDefNumberExprRef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ValueDef<(number|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<ValueDef<(number|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: str | None) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalValueDefNumberExprRef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ConditionalValueDefStringNullExprRef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ValueDef<(string|null|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<ValueDef<(string|null|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: str | None) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ConditionalParameterMarkPropExprDefType(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropExprDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropExprDef<Type>>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            description=description,
            domainInert=domainInert,
            empty=empty,
            expr=expr,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: str) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: str) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalParameterMarkPropExprDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropExprDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropExprDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            description=description,
            domainInert=domainInert,
            empty=empty,
            expr=expr,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(
        self, value: float
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(
        self, value: str
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(
        self, value: bool
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: str) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: str) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: Type_T
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalParameterMarkPropFieldDefType(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropFieldDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropFieldDef<Type>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            domainInert=domainInert,
            empty=empty,
            field=field,
            format=format,
            legend=legend,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: str) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: str) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalParameterMarkPropFieldDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropFieldDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropFieldDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: TypeForShape_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            domainInert=domainInert,
            empty=empty,
            field=field,
            format=format,
            legend=legend,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(
        self, value: str
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(
        self, value: bool
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(
        self, value: str
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: str
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(
        self, value: str
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: TypeForShape_T
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalParameterScaleDatumDef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ScaleDatumDef>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ScaleDatumDef>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            datum=datum,
            description=description,
            domainInert=domainInert,
            empty=empty,
            param=param,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: bool) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ConditionalParameterValueDefNumberExprRef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ValueDef<(number|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ValueDef<(number|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(
        self, value: str | None
    ) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ConditionalParameterValueDefStringNullExprRef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ValueDef<(string|null|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ValueDef<(string|null|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(
        self, value: str
    ) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: str) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(
        self, value: str | None
    ) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class Contig(GenomeSpySchema):
    """Generated wrapper for ``Contig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Contig", {})

    def __init__(
        self,
        name: str | UndefinedType = Undefined,
        size: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(name=name, size=size)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: str) -> Contig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_size(self, value: float) -> Contig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)


@with_property_setters
class CoreRootSpec(GenomeSpySchema):
    """Generated wrapper for ``CoreRootSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CoreRootSpec", {})

    def __init__(
        self,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        concat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: UrlGenomeConfig
        | dict[str, Any]
        | InlineGenomeConfig
        | GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        hconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        layer: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        mark: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps
        | UndefinedType = Undefined,
        multiscale: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | DynamicOpacity
        | DynamicOpacityKwds
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        stops: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any]
        | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        vconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        view: ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            assembly=assembly,
            axes=axes,
            background=background,
            baseUrl=baseUrl,
            columns=columns,
            concat=concat,
            config=config,
            cursor=cursor,
            data=data,
            datasets=datasets,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            genome=genome,
            genomes=genomes,
            hconcat=hconcat,
            height=height,
            layer=layer,
            legends=legends,
            mark=mark,
            multiscale=multiscale,
            name=name,
            opacity=opacity,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            separator=separator,
            spacing=spacing,
            stops=stops,
            templates=templates,
            theme=theme,
            title=title,
            transform=transform,
            vconcat=vconcat,
            view=view,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_assembly(self, value: str) -> CoreRootSpec:
        """Return a copy with ``assembly`` updated."""
        return self._with_property("assembly", value)

    def with_axes(self, value: AxesKwds) -> CoreRootSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_background(self, value: str) -> CoreRootSpec:
        """Return a copy with ``background`` updated."""
        return self._with_property("background", value)

    def with_baseUrl(self, value: str) -> CoreRootSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: float) -> CoreRootSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> CoreRootSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_datasets(self, value: dict[str, Any]) -> CoreRootSpec:
        """Return a copy with ``datasets`` updated."""
        return self._with_property("datasets", value)

    def with_description(self, value: str | Sequence[str]) -> CoreRootSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> CoreRootSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_genome(
        self,
        value: UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase,
    ) -> CoreRootSpec:
        """Return a copy with ``genome`` updated."""
        return self._with_property("genome", value)

    def with_genomes(self, value: dict[str, Any]) -> CoreRootSpec:
        """Return a copy with ``genomes`` updated."""
        return self._with_property("genomes", value)

    def with_hconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: LegendsKwds) -> CoreRootSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps,
    ) -> CoreRootSpec:
        """Return a copy with ``mark`` updated."""
        return self._with_property("mark", value)

    def with_multiscale(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: str) -> CoreRootSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any],
    ) -> CoreRootSpec:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> CoreRootSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> CoreRootSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> CoreRootSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | SeparatorPropsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: float) -> CoreRootSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_stops(
        self,
        value: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any],
    ) -> CoreRootSpec:
        """Return a copy with ``stops`` updated."""
        return self._with_property("stops", value)

    def with_templates(self, value: dict[str, Any]) -> CoreRootSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_theme(
        self, value: BuiltInThemeName_T | Sequence[BuiltInThemeName_T]
    ) -> CoreRootSpec:
        """Return a copy with ``theme`` updated."""
        return self._with_property("theme", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> CoreRootSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> CoreRootSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class CoverageParams(GenomeSpySchema):
    """Generated wrapper for ``CoverageParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CoverageParams", {})

    def __init__(
        self,
        asChrom: str | UndefinedType = Undefined,
        asEnd: str | UndefinedType = Undefined,
        asStart: str | UndefinedType = Undefined,
        chrom: Field_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        end: Field_T | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
        type: Literal["coverage"] | UndefinedType = Undefined,
        weight: Field_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            asChrom=asChrom,
            asEnd=asEnd,
            asStart=asStart,
            chrom=chrom,
            description=description,
            end=end,
            start=start,
            type=type,
            weight=weight,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_asChrom(self, value: str) -> CoverageParams:
        """Return a copy with ``asChrom`` updated."""
        return self._with_property("asChrom", value)

    def with_asEnd(self, value: str) -> CoverageParams:
        """Return a copy with ``asEnd`` updated."""
        return self._with_property("asEnd", value)

    def with_asStart(self, value: str) -> CoverageParams:
        """Return a copy with ``asStart`` updated."""
        return self._with_property("asStart", value)

    def with_chrom(self, value: Field_T) -> CoverageParams:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_description(self, value: str) -> CoverageParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_end(self, value: Field_T) -> CoverageParams:
        """Return a copy with ``end`` updated."""
        return self._with_property("end", value)

    def with_start(self, value: Field_T) -> CoverageParams:
        """Return a copy with ``start`` updated."""
        return self._with_property("start", value)

    def with_type(self, value: Literal["coverage"]) -> CoverageParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_weight(self, value: Field_T) -> CoverageParams:
        """Return a copy with ``weight`` updated."""
        return self._with_property("weight", value)


@with_property_setters
class CsvDataFormat(GenomeSpySchema):
    """Generated wrapper for ``CsvDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CsvDataFormat", {})

    def __init__(
        self,
        columns: Sequence[str] | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: Literal["csv", "tsv"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_columns(self, value: Sequence[str]) -> CsvDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CsvDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Literal["csv", "tsv"]) -> CsvDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Data(GenomeSpySchema):
    """Generated wrapper for ``Data``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Data", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        dynamicCallbackSource: bool | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        lazy: LazyDataParams | dict[str, Any] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        sequence: SequenceParams | dict[str, Any] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlList
        | UrlTemplate
        | UndefinedType = Undefined,
        values: InlineDataset | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            dynamicCallbackSource=dynamicCallbackSource,
            format=format,
            lazy=lazy,
            name=name,
            sequence=sequence,
            url=url,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> Data:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: bool) -> Data:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> Data:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_lazy(
        self,
        value: LazyDataParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``LazyDataParams`` lazy."""
        return self._with_property("lazy", value, **kwargs)

    def with_name(self, value: str) -> Data:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_sequence(
        self,
        value: SequenceParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``SequenceParams`` sequence."""
        return self._with_property("sequence", value, **kwargs)

    def with_url(
        self,
        value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlList | UrlTemplate,
    ) -> Data:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_values(
        self,
        value: InlineDataset | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``InlineDataset`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class DataFormat(GenomeSpySchema):
    """Generated wrapper for ``DataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DataFormat", {})

    def __init__(
        self,
        columns: Sequence[str] | UndefinedType = Undefined,
        delimiter: str | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        property: str | UndefinedType = Undefined,
        type: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            columns=columns,
            delimiter=delimiter,
            parse=parse,
            property=property,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_columns(self, value: Sequence[str]) -> DataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_delimiter(self, value: str) -> DataFormat:
        """Return a copy with ``delimiter`` updated."""
        return self._with_property("delimiter", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_property(self, value: str) -> DataFormat:
        """Return a copy with ``property`` updated."""
        return self._with_property("property", value)

    def with_type(self, value: str) -> DataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class DataSource(GenomeSpySchema):
    """Generated wrapper for ``DataSource``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DataSource", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        dynamicCallbackSource: bool | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        lazy: LazyDataParams | dict[str, Any] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlList
        | UrlTemplate
        | UndefinedType = Undefined,
        values: InlineDataset | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            dynamicCallbackSource=dynamicCallbackSource,
            format=format,
            lazy=lazy,
            name=name,
            url=url,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> DataSource:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: bool) -> DataSource:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> DataSource:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_lazy(
        self,
        value: LazyDataParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``LazyDataParams`` lazy."""
        return self._with_property("lazy", value, **kwargs)

    def with_name(self, value: str) -> DataSource:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(
        self,
        value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlList | UrlTemplate,
    ) -> DataSource:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_values(
        self,
        value: InlineDataset | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``InlineDataset`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class DomEventType(GenomeSpySchema):
    """Generated wrapper for ``DomEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class DomainValue(GenomeSpySchema):
    """Generated wrapper for ``DomainValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomainValue", {})

    def __init__(self, expr: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: str) -> DomainValue:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


@with_property_setters
class DomainValueArray(GenomeSpySchema):
    """Generated wrapper for ``DomainValueArray``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomainValueArray", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class DsvDataFormat(GenomeSpySchema):
    """Generated wrapper for ``DsvDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DsvDataFormat", {})

    def __init__(
        self,
        columns: Sequence[str] | UndefinedType = Undefined,
        delimiter: str | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: Literal["dsv"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, delimiter=delimiter, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_columns(self, value: Sequence[str]) -> DsvDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_delimiter(self, value: str) -> DsvDataFormat:
        """Return a copy with ``delimiter`` updated."""
        return self._with_property("delimiter", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DsvDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Literal["dsv"]) -> DsvDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class DynamicCallbackData(GenomeSpySchema):
    """Generated wrapper for ``DynamicCallbackData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DynamicCallbackData", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        dynamicCallbackSource: bool | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            dynamicCallbackSource=dynamicCallbackSource,
            format=format,
            name=name,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> DynamicCallbackData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: bool) -> DynamicCallbackData:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> DynamicCallbackData:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_name(self, value: str) -> DynamicCallbackData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class DynamicOpacity(GenomeSpySchema):
    """Generated wrapper for ``DynamicOpacity``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DynamicOpacity", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T
        | Literal["auto"]
        | UndefinedType = Undefined,
        unitsPerPixel: Sequence[float | ExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        values: Sequence[float] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, unitsPerPixel=unitsPerPixel, values=values)
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self, value: PrimaryPositionalChannel_T | Literal["auto"]
    ) -> DynamicOpacity:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_unitsPerPixel(
        self, value: Sequence[float | ExprRef | dict[str, Any]]
    ) -> DynamicOpacity:
        """Return a copy with ``unitsPerPixel`` updated."""
        return self._with_property("unitsPerPixel", value)

    def with_values(self, value: Sequence[float]) -> DynamicOpacity:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class Encoding(GenomeSpySchema):
    """Generated wrapper for ``Encoding``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Encoding", {})

    def __init__(
        self,
        angle: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        color: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
        | UndefinedType = Undefined,
        dx: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef
        | UndefinedType = Undefined,
        dy: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef
        | UndefinedType = Undefined,
        facetIndex: FieldDefWithoutScale | dict[str, Any] | UndefinedType = Undefined,
        fill: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
        | UndefinedType = Undefined,
        fillOpacity: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        key: FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]]
        | UndefinedType = Undefined,
        opacity: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        sample: FieldDefWithoutScale | dict[str, Any] | UndefinedType = Undefined,
        search: FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]]
        | UndefinedType = Undefined,
        semanticScore: dict[str, Any] | UndefinedType = Undefined,
        shape: FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullTypeForShape
        | UndefinedType = Undefined,
        size: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        stroke: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
        | UndefinedType = Undefined,
        strokeOpacity: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        strokeWidth: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | UndefinedType = Undefined,
        text: StringFieldDef
        | dict[str, Any]
        | StringDatumDef
        | ExprDef
        | ValueDefString
        | UndefinedType = Undefined,
        uniqueId: FieldDefWithoutScale | dict[str, Any] | UndefinedType = Undefined,
        x: dict[str, Any] | UndefinedType = Undefined,
        x2: Position2Def | dict[str, Any] | None | UndefinedType = Undefined,
        y: PositionFieldDef
        | dict[str, Any]
        | ChromPosDef
        | PositionDatumDef
        | PositionExprDef
        | ValueDefNumber
        | UndefinedType = Undefined,
        y2: Position2Def | dict[str, Any] | None | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            angle=angle,
            color=color,
            dx=dx,
            dy=dy,
            facetIndex=facetIndex,
            fill=fill,
            fillOpacity=fillOpacity,
            key=key,
            opacity=opacity,
            sample=sample,
            search=search,
            semanticScore=semanticScore,
            shape=shape,
            size=size,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            text=text,
            uniqueId=uniqueId,
            x=x,
            x2=x2,
            y=y,
            y2=y2,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_angle(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``angle`` updated."""
        return self._with_property("angle", value)

    def with_color(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType,
    ) -> Encoding:
        """Return a copy with ``color`` updated."""
        return self._with_property("color", value)

    def with_dx(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef,
    ) -> Encoding:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef,
    ) -> Encoding:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_facetIndex(
        self,
        value: FieldDefWithoutScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``FieldDefWithoutScale`` facetIndex."""
        return self._with_property("facetIndex", value, **kwargs)

    def with_fill(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType,
    ) -> Encoding:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_key(
        self,
        value: FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]],
    ) -> Encoding:
        """Return a copy with ``key`` updated."""
        return self._with_property("key", value)

    def with_opacity(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_sample(
        self,
        value: FieldDefWithoutScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``FieldDefWithoutScale`` sample."""
        return self._with_property("sample", value, **kwargs)

    def with_search(
        self,
        value: FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]],
    ) -> Encoding:
        """Return a copy with ``search`` updated."""
        return self._with_property("search", value)

    def with_semanticScore(self, value: dict[str, Any]) -> Encoding:
        """Return a copy with ``semanticScore`` updated."""
        return self._with_property("semanticScore", value)

    def with_shape(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullTypeForShape,
    ) -> Encoding:
        """Return a copy with ``shape`` updated."""
        return self._with_property("shape", value)

    def with_size(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_stroke(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType,
    ) -> Encoding:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(
        self,
        value: FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType,
    ) -> Encoding:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_text(
        self,
        value: StringFieldDef
        | dict[str, Any]
        | StringDatumDef
        | ExprDef
        | ValueDefString,
    ) -> Encoding:
        """Return a copy with ``text`` updated."""
        return self._with_property("text", value)

    def with_uniqueId(
        self,
        value: FieldDefWithoutScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``FieldDefWithoutScale`` uniqueId."""
        return self._with_property("uniqueId", value, **kwargs)

    def with_x(self, value: dict[str, Any]) -> Encoding:
        """Return a copy with ``x`` updated."""
        return self._with_property("x", value)

    def with_x2(
        self,
        value: Position2Def | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``Position2Def`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_y(
        self,
        value: PositionFieldDef
        | dict[str, Any]
        | ChromPosDef
        | PositionDatumDef
        | PositionExprDef
        | ValueDefNumber,
    ) -> Encoding:
        """Return a copy with ``y`` updated."""
        return self._with_property("y", value)

    def with_y2(
        self,
        value: Position2Def | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``Position2Def`` y2."""
        return self._with_property("y2", value, **kwargs)


@with_property_setters
class EventConfig(GenomeSpySchema):
    """Generated wrapper for ``EventConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("EventConfig", {})

    def __init__(
        self,
        filter: str | UndefinedType = Undefined,
        type: DomEventType_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(filter=filter, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_filter(self, value: str) -> EventConfig:
        """Return a copy with ``filter`` updated."""
        return self._with_property("filter", value)

    def with_type(self, value: DomEventType_T) -> EventConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ExprDef(GenomeSpySchema):
    """Generated wrapper for ``ExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band, description=description, expr=expr, title=title, type=type
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> ExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: str) -> ExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_title(self, value: str | None) -> ExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ExprDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ExprFilterParams(GenomeSpySchema):
    """Generated wrapper for ``ExprFilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprFilterParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        type: Literal["filter"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, expr=expr, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ExprFilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: str) -> ExprFilterParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_type(self, value: Literal["filter"]) -> ExprFilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ExprRef(GenomeSpySchema):
    """Generated wrapper for ``ExprRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprRef", {})

    def __init__(self, expr: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: str) -> ExprRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


@with_property_setters
class Field(GenomeSpySchema):
    """Generated wrapper for ``Field``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Field", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class FieldDefWithoutScale(GenomeSpySchema):
    """Generated wrapper for ``FieldDefWithoutScale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FieldDefWithoutScale", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FieldDefWithoutScale:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: str) -> FieldDefWithoutScale:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: str | None) -> FieldDefWithoutScale:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


@with_property_setters
class FieldName(GenomeSpySchema):
    """Generated wrapper for ``FieldName``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FieldName", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,(string|null)>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: Type_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,number>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterValueDefNumberExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterValueDefNumberExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: Type_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull(
    GenomeSpySchema
):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<TypeForShape>,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<TypeForShape>,(string|null)>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: TypeForShape_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: str
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: TypeForShape_T
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FieldOrDatumDefWithConditionScaleDatumDefStringNull(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<ScaleDatumDef,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<ScaleDatumDef,(string|null)>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(
        self, value: float
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterValueDefStringNullExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(
        self, value: str
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: Type_T
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FieldOrDatumDefWithConditionScaleDatumDefNumber(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<ScaleDatumDef,number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<ScaleDatumDef,number>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterValueDefNumberExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(
        self, value: float
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterValueDefNumberExprRef
        | dict[str, Any]
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(
        self, value: str
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: bool
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: str | None
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self, value: Type_T
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FilterParams(GenomeSpySchema):
    """Generated wrapper for ``FilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FilterParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        fields: dict[str, Any] | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        type: Literal["filter"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            empty=empty,
            expr=expr,
            fields=fields,
            param=param,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> FilterParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: str) -> FilterParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_fields(self, value: dict[str, Any]) -> FilterParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_param(self, value: str) -> FilterParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_type(self, value: Literal["filter"]) -> FilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FilterScoredLabelsParams(GenomeSpySchema):
    """Generated wrapper for ``FilterScoredLabelsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FilterScoredLabelsParams", {})

    def __init__(
        self,
        asMidpoint: str | UndefinedType = Undefined,
        channel: Literal["x", "y"] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        lane: Field_T | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        pos: Field_T | UndefinedType = Undefined,
        pos2: Field_T | UndefinedType = Undefined,
        score: Field_T | UndefinedType = Undefined,
        type: Literal["filterScoredLabels"] | UndefinedType = Undefined,
        width: Field_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            asMidpoint=asMidpoint,
            channel=channel,
            description=description,
            lane=lane,
            padding=padding,
            pos=pos,
            pos2=pos2,
            score=score,
            type=type,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_asMidpoint(self, value: str) -> FilterScoredLabelsParams:
        """Return a copy with ``asMidpoint`` updated."""
        return self._with_property("asMidpoint", value)

    def with_channel(self, value: Literal["x", "y"]) -> FilterScoredLabelsParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_description(self, value: str) -> FilterScoredLabelsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_lane(self, value: Field_T) -> FilterScoredLabelsParams:
        """Return a copy with ``lane`` updated."""
        return self._with_property("lane", value)

    def with_padding(self, value: float) -> FilterScoredLabelsParams:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_pos(self, value: Field_T) -> FilterScoredLabelsParams:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_pos2(self, value: Field_T) -> FilterScoredLabelsParams:
        """Return a copy with ``pos2`` updated."""
        return self._with_property("pos2", value)

    def with_score(self, value: Field_T) -> FilterScoredLabelsParams:
        """Return a copy with ``score`` updated."""
        return self._with_property("score", value)

    def with_type(
        self, value: Literal["filterScoredLabels"]
    ) -> FilterScoredLabelsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_width(self, value: Field_T) -> FilterScoredLabelsParams:
        """Return a copy with ``width`` updated."""
        return self._with_property("width", value)


@with_property_setters
class FlattenCompressedExonsParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenCompressedExonsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FlattenCompressedExonsParams", {}
    )

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        exons: Field_T | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
        type: Literal["flattenCompressedExons"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, exons=exons, start=start, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FlattenCompressedExonsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_exons(self, value: Field_T) -> FlattenCompressedExonsParams:
        """Return a copy with ``exons`` updated."""
        return self._with_property("exons", value)

    def with_start(self, value: Field_T) -> FlattenCompressedExonsParams:
        """Return a copy with ``start`` updated."""
        return self._with_property("start", value)

    def with_type(
        self, value: Literal["flattenCompressedExons"]
    ) -> FlattenCompressedExonsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FlattenDelimitedParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenDelimitedParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenDelimitedParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        separator: Sequence[str] | str | UndefinedType = Undefined,
        type: Literal["flattenDelimited"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, field=field, separator=separator, type=type
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FlattenDelimitedParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Sequence[Field_T] | Field_T) -> FlattenDelimitedParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_separator(self, value: Sequence[str] | str) -> FlattenDelimitedParams:
        """Return a copy with ``separator`` updated."""
        return self._with_property("separator", value)

    def with_type(self, value: Literal["flattenDelimited"]) -> FlattenDelimitedParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FlattenParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        index: str | UndefinedType = Undefined,
        type: Literal["flatten"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, fields=fields, index=index, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FlattenParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(self, value: Sequence[Field_T] | Field_T) -> FlattenParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_index(self, value: str) -> FlattenParams:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_type(self, value: Literal["flatten"]) -> FlattenParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FlattenSequenceParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenSequenceParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenSequenceParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        type: Literal["flattenSequence"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FlattenSequenceParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Field_T) -> FlattenSequenceParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_type(self, value: Literal["flattenSequence"]) -> FlattenSequenceParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class FontStyle(GenomeSpySchema):
    """Generated wrapper for ``FontStyle``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FontStyle", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class FontWeight(GenomeSpySchema):
    """Generated wrapper for ``FontWeight``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FontWeight", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class FormulaParams(GenomeSpySchema):
    """Generated wrapper for ``FormulaParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FormulaParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        type: Literal["formula"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, expr=expr, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> FormulaParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: str) -> FormulaParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_type(self, value: Literal["formula"]) -> FormulaParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Generator(GenomeSpySchema):
    """Generated wrapper for ``Generator``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Generator", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        sequence: SequenceParams | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, name=name, sequence=sequence)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> Generator:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: str) -> Generator:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_sequence(
        self,
        value: SequenceParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Generator:
        """Return a copy with a ``SequenceParams`` sequence."""
        return self._with_property("sequence", value, **kwargs)


@with_property_setters
class GenomeAxis(GenomeSpySchema):
    """Generated wrapper for ``GenomeAxis``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeAxis", {})

    def __init__(
        self,
        chromGrid: bool | UndefinedType = Undefined,
        chromGridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        chromGridColor: str | UndefinedType = Undefined,
        chromGridDash: Sequence[float] | UndefinedType = Undefined,
        chromGridDashOffset: float | UndefinedType = Undefined,
        chromGridFillEven: str | UndefinedType = Undefined,
        chromGridFillOdd: str | UndefinedType = Undefined,
        chromGridOpacity: float | UndefinedType = Undefined,
        chromGridWidth: float | UndefinedType = Undefined,
        chromLabelAlign: Align_T | UndefinedType = Undefined,
        chromLabelColor: str | UndefinedType = Undefined,
        chromLabelFont: str | UndefinedType = Undefined,
        chromLabelFontSize: float | UndefinedType = Undefined,
        chromLabelFontStyle: FontStyle_T | UndefinedType = Undefined,
        chromLabelFontWeight: FontWeight_T | UndefinedType = Undefined,
        chromLabelPadding: float | UndefinedType = Undefined,
        chromLabels: bool | UndefinedType = Undefined,
        chromTickColor: str | UndefinedType = Undefined,
        chromTickDash: Sequence[float] | UndefinedType = Undefined,
        chromTickDashOffset: float | UndefinedType = Undefined,
        chromTickSize: float | UndefinedType = Undefined,
        chromTickWidth: float | UndefinedType = Undefined,
        chromTicks: bool | UndefinedType = Undefined,
        domain: bool | UndefinedType = Undefined,
        domainCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        domainColor: str | UndefinedType = Undefined,
        domainDash: Sequence[float] | UndefinedType = Undefined,
        domainDashOffset: float | UndefinedType = Undefined,
        domainWidth: float | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        grid: bool | UndefinedType = Undefined,
        gridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        gridColor: str | UndefinedType = Undefined,
        gridDash: Sequence[float] | UndefinedType = Undefined,
        gridDashOffset: float | UndefinedType = Undefined,
        gridOpacity: float | UndefinedType = Undefined,
        gridWidth: float | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelAngle: float | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tickDash: Sequence[float] | UndefinedType = Undefined,
        tickDashOffset: float | UndefinedType = Undefined,
        tickMinStep: float | UndefinedType = Undefined,
        tickSize: float | UndefinedType = Undefined,
        tickWidth: float | UndefinedType = Undefined,
        ticks: bool | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleColor: str | UndefinedType = Undefined,
        titleFit: Literal["point", "range"] | UndefinedType = Undefined,
        titleFont: str | UndefinedType = Undefined,
        titleFontSize: float | UndefinedType = Undefined,
        titleFontStyle: FontStyle_T | UndefinedType = Undefined,
        titleFontWeight: FontWeight_T | UndefinedType = Undefined,
        titleOpacity: float | UndefinedType = Undefined,
        titlePadding: float | UndefinedType = Undefined,
        values: Sequence[Any] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            chromGrid=chromGrid,
            chromGridCap=chromGridCap,
            chromGridColor=chromGridColor,
            chromGridDash=chromGridDash,
            chromGridDashOffset=chromGridDashOffset,
            chromGridFillEven=chromGridFillEven,
            chromGridFillOdd=chromGridFillOdd,
            chromGridOpacity=chromGridOpacity,
            chromGridWidth=chromGridWidth,
            chromLabelAlign=chromLabelAlign,
            chromLabelColor=chromLabelColor,
            chromLabelFont=chromLabelFont,
            chromLabelFontSize=chromLabelFontSize,
            chromLabelFontStyle=chromLabelFontStyle,
            chromLabelFontWeight=chromLabelFontWeight,
            chromLabelPadding=chromLabelPadding,
            chromLabels=chromLabels,
            chromTickColor=chromTickColor,
            chromTickDash=chromTickDash,
            chromTickDashOffset=chromTickDashOffset,
            chromTickSize=chromTickSize,
            chromTickWidth=chromTickWidth,
            chromTicks=chromTicks,
            domain=domain,
            domainCap=domainCap,
            domainColor=domainColor,
            domainDash=domainDash,
            domainDashOffset=domainDashOffset,
            domainWidth=domainWidth,
            format=format,
            grid=grid,
            gridCap=gridCap,
            gridColor=gridColor,
            gridDash=gridDash,
            gridDashOffset=gridDashOffset,
            gridOpacity=gridOpacity,
            gridWidth=gridWidth,
            labelAlign=labelAlign,
            labelAngle=labelAngle,
            labelBaseline=labelBaseline,
            labelColor=labelColor,
            labelFont=labelFont,
            labelFontSize=labelFontSize,
            labelFontStyle=labelFontStyle,
            labelFontWeight=labelFontWeight,
            labelLimit=labelLimit,
            labelPadding=labelPadding,
            labels=labels,
            maxExtent=maxExtent,
            minExtent=minExtent,
            offset=offset,
            orient=orient,
            placement=placement,
            style=style,
            tickCap=tickCap,
            tickColor=tickColor,
            tickCount=tickCount,
            tickDash=tickDash,
            tickDashOffset=tickDashOffset,
            tickMinStep=tickMinStep,
            tickSize=tickSize,
            tickWidth=tickWidth,
            ticks=ticks,
            title=title,
            titleColor=titleColor,
            titleFit=titleFit,
            titleFont=titleFont,
            titleFontSize=titleFontSize,
            titleFontStyle=titleFontStyle,
            titleFontWeight=titleFontWeight,
            titleOpacity=titleOpacity,
            titlePadding=titlePadding,
            values=values,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_chromGrid(self, value: bool) -> GenomeAxis:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(
        self, value: Literal["butt", "round", "square"]
    ) -> GenomeAxis:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Sequence[float]) -> GenomeAxis:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(self, value: Align_T) -> GenomeAxis:
        """Return a copy with ``chromLabelAlign`` updated."""
        return self._with_property("chromLabelAlign", value)

    def with_chromLabelColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(self, value: FontStyle_T) -> GenomeAxis:
        """Return a copy with ``chromLabelFontStyle`` updated."""
        return self._with_property("chromLabelFontStyle", value)

    def with_chromLabelFontWeight(self, value: FontWeight_T) -> GenomeAxis:
        """Return a copy with ``chromLabelFontWeight`` updated."""
        return self._with_property("chromLabelFontWeight", value)

    def with_chromLabelPadding(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: bool) -> GenomeAxis:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Sequence[float]) -> GenomeAxis:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: float) -> GenomeAxis:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: bool) -> GenomeAxis:
        """Return a copy with ``chromTicks`` updated."""
        return self._with_property("chromTicks", value)

    def with_domain(self, value: bool) -> GenomeAxis:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Literal["butt", "round", "square"]) -> GenomeAxis:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Sequence[float]) -> GenomeAxis:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: float) -> GenomeAxis:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: float) -> GenomeAxis:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: str) -> GenomeAxis:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: bool) -> GenomeAxis:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Literal["butt", "round", "square"]) -> GenomeAxis:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Sequence[float]) -> GenomeAxis:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: float) -> GenomeAxis:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: float) -> GenomeAxis:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: float) -> GenomeAxis:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(self, value: Align_T) -> GenomeAxis:
        """Return a copy with ``labelAlign`` updated."""
        return self._with_property("labelAlign", value)

    def with_labelAngle(self, value: float) -> GenomeAxis:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(self, value: Baseline_T) -> GenomeAxis:
        """Return a copy with ``labelBaseline`` updated."""
        return self._with_property("labelBaseline", value)

    def with_labelColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: str) -> GenomeAxis:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: float) -> GenomeAxis:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(self, value: FontStyle_T) -> GenomeAxis:
        """Return a copy with ``labelFontStyle`` updated."""
        return self._with_property("labelFontStyle", value)

    def with_labelFontWeight(self, value: FontWeight_T) -> GenomeAxis:
        """Return a copy with ``labelFontWeight`` updated."""
        return self._with_property("labelFontWeight", value)

    def with_labelLimit(self, value: float) -> GenomeAxis:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: float) -> GenomeAxis:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: bool) -> GenomeAxis:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: float) -> GenomeAxis:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: float) -> GenomeAxis:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: float) -> GenomeAxis:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: AxisOrient_T) -> GenomeAxis:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_placement(self, value: AxisPlacement_T) -> GenomeAxis:
        """Return a copy with ``placement`` updated."""
        return self._with_property("placement", value)

    def with_style(self, value: str | Sequence[str] | None) -> GenomeAxis:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Literal["butt", "round", "square"]) -> GenomeAxis:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``tickColor`` updated."""
        return self._with_property("tickColor", value)

    def with_tickCount(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``ExprRef`` tickCount."""
        return self._with_property("tickCount", value, **kwargs)

    def with_tickDash(self, value: Sequence[float]) -> GenomeAxis:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: float) -> GenomeAxis:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: float) -> GenomeAxis:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: float) -> GenomeAxis:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: float) -> GenomeAxis:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: bool) -> GenomeAxis:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: str | None) -> GenomeAxis:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: str) -> GenomeAxis:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Literal["point", "range"]) -> GenomeAxis:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: str) -> GenomeAxis:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: float) -> GenomeAxis:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(self, value: FontStyle_T) -> GenomeAxis:
        """Return a copy with ``titleFontStyle`` updated."""
        return self._with_property("titleFontStyle", value)

    def with_titleFontWeight(self, value: FontWeight_T) -> GenomeAxis:
        """Return a copy with ``titleFontWeight`` updated."""
        return self._with_property("titleFontWeight", value)

    def with_titleOpacity(self, value: float) -> GenomeAxis:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: float) -> GenomeAxis:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Sequence[Any]) -> GenomeAxis:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: float) -> GenomeAxis:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class GenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``GenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeConfig", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        url: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, name=name, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(self, value: Sequence[Contig | dict[str, Any]]) -> GenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_name(self, value: str) -> GenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(self, value: str) -> GenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class GenomeConfigBase(GenomeSpySchema):
    """Generated wrapper for ``GenomeConfigBase``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeConfigBase", {})

    def __init__(self, name: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: str) -> GenomeConfigBase:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class GenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``GenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeDefinition", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        url: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(
        self, value: Sequence[Contig | dict[str, Any]]
    ) -> GenomeDefinition:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: str) -> GenomeDefinition:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class GenomeSpyConfig(GenomeSpySchema):
    """Generated wrapper for ``GenomeSpyConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeSpyConfig", {})

    def __init__(
        self,
        axis: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisBottom: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisIndex: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLeft: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLocus: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisNominal: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisOrdinal: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisQuantitative: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisRight: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisTop: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisX: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisY: AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        legend: LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        legendTrack: LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        link: LinkConfig | LinkConfigKwds | UndefinedType = Undefined,
        mark: MarkConfig | MarkConfigKwds | UndefinedType = Undefined,
        point: PointConfig | PointConfigKwds | UndefinedType = Undefined,
        range: RangeConfig | RangeConfigKwds | UndefinedType = Undefined,
        rect: RectConfig | RectConfigKwds | UndefinedType = Undefined,
        rule: RuleConfig | RuleConfigKwds | UndefinedType = Undefined,
        scale: ScaleConfig | ScaleConfigKwds | UndefinedType = Undefined,
        style: dict[str, Any] | UndefinedType = Undefined,
        text: TextConfig | TextConfigKwds | UndefinedType = Undefined,
        tick: TickConfig | dict[str, Any] | UndefinedType = Undefined,
        title: TitleConfig | TitleConfigKwds | UndefinedType = Undefined,
        view: ViewConfig | ViewConfigKwds | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            axisBottom=axisBottom,
            axisIndex=axisIndex,
            axisLeft=axisLeft,
            axisLocus=axisLocus,
            axisNominal=axisNominal,
            axisOrdinal=axisOrdinal,
            axisQuantitative=axisQuantitative,
            axisRight=axisRight,
            axisTop=axisTop,
            axisX=axisX,
            axisY=axisY,
            legend=legend,
            legendTrack=legendTrack,
            link=link,
            mark=mark,
            point=point,
            range=range,
            rect=rect,
            rule=rule,
            scale=scale,
            style=style,
            text=text,
            tick=tick,
            title=title,
            view=view,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_axisBottom(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisBottom."""
        return self._with_property("axisBottom", value, **kwargs)

    def with_axisIndex(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisIndex."""
        return self._with_property("axisIndex", value, **kwargs)

    def with_axisLeft(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisLeft."""
        return self._with_property("axisLeft", value, **kwargs)

    def with_axisLocus(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisLocus."""
        return self._with_property("axisLocus", value, **kwargs)

    def with_axisNominal(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisNominal."""
        return self._with_property("axisNominal", value, **kwargs)

    def with_axisOrdinal(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisOrdinal."""
        return self._with_property("axisOrdinal", value, **kwargs)

    def with_axisQuantitative(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisQuantitative."""
        return self._with_property("axisQuantitative", value, **kwargs)

    def with_axisRight(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisRight."""
        return self._with_property("axisRight", value, **kwargs)

    def with_axisTop(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisTop."""
        return self._with_property("axisTop", value, **kwargs)

    def with_axisX(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisX."""
        return self._with_property("axisX", value, **kwargs)

    def with_axisY(
        self,
        value: AxisConfig | AxisConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisY."""
        return self._with_property("axisY", value, **kwargs)

    def with_legend(
        self,
        value: LegendConfig | LegendConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LegendConfig`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_legendTrack(
        self,
        value: LegendConfig | LegendConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LegendConfig`` legendTrack."""
        return self._with_property("legendTrack", value, **kwargs)

    def with_link(
        self,
        value: LinkConfig | LinkConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LinkConfig`` link."""
        return self._with_property("link", value, **kwargs)

    def with_mark(
        self,
        value: MarkConfig | MarkConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``MarkConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_point(
        self,
        value: PointConfig | PointConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``PointConfig`` point."""
        return self._with_property("point", value, **kwargs)

    def with_range(
        self,
        value: RangeConfig | RangeConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RangeConfig`` range."""
        return self._with_property("range", value, **kwargs)

    def with_rect(
        self,
        value: RectConfig | RectConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RectConfig`` rect."""
        return self._with_property("rect", value, **kwargs)

    def with_rule(
        self,
        value: RuleConfig | RuleConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RuleConfig`` rule."""
        return self._with_property("rule", value, **kwargs)

    def with_scale(
        self,
        value: ScaleConfig | ScaleConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``ScaleConfig`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_style(self, value: dict[str, Any]) -> GenomeSpyConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(
        self,
        value: TextConfig | TextConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``TextConfig`` text."""
        return self._with_property("text", value, **kwargs)

    def with_tick(
        self,
        value: TickConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``TickConfig`` tick."""
        return self._with_property("tick", value, **kwargs)

    def with_title(
        self,
        value: TitleConfig | TitleConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``TitleConfig`` title."""
        return self._with_property("title", value, **kwargs)

    def with_view(
        self,
        value: ViewConfig | ViewConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``ViewConfig`` view."""
        return self._with_property("view", value, **kwargs)


@with_property_setters
class Gff3Data(GenomeSpySchema):
    """Generated wrapper for ``Gff3Data``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Gff3Data", {})

    def __init__(
        self,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        type: Literal["gff3"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            addChrPrefix=addChrPrefix,
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            indexUrl=indexUrl,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_addChrPrefix(self, value: bool | str) -> Gff3Data:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> Gff3Data:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Gff3Data:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Gff3Data:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> Gff3Data:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> Gff3Data:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_type(self, value: Literal["gff3"]) -> Gff3Data:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> Gff3Data:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(self, value: float) -> Gff3Data:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class HConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``HConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("HConcatSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        hconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            hconcat=hconcat,
            height=height,
            legends=legends,
            name=name,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            separator=separator,
            spacing=spacing,
            templates=templates,
            title=title,
            transform=transform,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> HConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> HConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> HConcatSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> HConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> HConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_hconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> HConcatSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: LegendsKwds) -> HConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: str) -> HConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> HConcatSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> HConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> HConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> HConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | SeparatorPropsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: float) -> HConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: dict[str, Any]) -> HConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> HConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> HConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class HandledTooltip(GenomeSpySchema):
    """Generated wrapper for ``HandledTooltip``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("HandledTooltip", {})

    def __init__(
        self,
        handler: str | UndefinedType = Undefined,
        params: dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(handler=handler, params=params)
        if kwds:
            self._kwds.update(kwds)

    def with_handler(self, value: str) -> HandledTooltip:
        """Return a copy with ``handler`` updated."""
        return self._with_property("handler", value)

    def with_params(self, value: dict[str, Any]) -> HandledTooltip:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)


@with_property_setters
class IdentifierParams(GenomeSpySchema):
    """Generated wrapper for ``IdentifierParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IdentifierParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        type: Literal["identifier"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> IdentifierParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_type(self, value: Literal["identifier"]) -> IdentifierParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ImportSpec(GenomeSpySchema):
    """Generated wrapper for ``ImportSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ImportSpec", {})

    def __init__(
        self,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | dict[str, Any]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(config=config, name=name, params=params, visible=visible)
        if kwds:
            self._kwds.update(kwds)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ImportSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_name(self, value: str) -> ImportSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | dict[str, Any],
    ) -> ImportSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_visible(self, value: bool) -> ImportSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)


@with_property_setters
class IndexUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlSourceRef", {})

    def __init__(
        self,
        expr: str | UndefinedType = Undefined,
        template: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(expr=expr, template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: str) -> IndexUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_template(self, value: str) -> IndexUrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


@with_property_setters
class IndexUrlTemplate(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlTemplate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlTemplate", {})

    def __init__(self, template: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_template(self, value: str) -> IndexUrlTemplate:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


@with_property_setters
class IndexedFastaData(GenomeSpySchema):
    """Generated wrapper for ``IndexedFastaData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexedFastaData", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        type: Literal["indexedFasta"] | UndefinedType = Undefined,
        url: str | ExprRef | dict[str, Any] | UrlTemplate | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            indexUrl=indexUrl,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> IndexedFastaData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IndexedFastaData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IndexedFastaData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> IndexedFastaData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> IndexedFastaData:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_type(self, value: Literal["indexedFasta"]) -> IndexedFastaData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | ExprRef | dict[str, Any] | UrlTemplate
    ) -> IndexedFastaData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(self, value: float) -> IndexedFastaData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class InlineData(GenomeSpySchema):
    """Generated wrapper for ``InlineData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineData", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        values: InlineDataset | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, format=format, name=name, values=values
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> InlineData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> InlineData:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_name(self, value: str) -> InlineData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_values(
        self,
        value: InlineDataset | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> InlineData:
        """Return a copy with a ``InlineDataset`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class InlineDataset(GenomeSpySchema):
    """Generated wrapper for ``InlineDataset``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineDataset", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class InlineGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``InlineGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineGenomeConfig", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(
        self, value: Sequence[Contig | dict[str, Any]]
    ) -> InlineGenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_name(self, value: str) -> InlineGenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class InlineGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``InlineGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineGenomeDefinition", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(
        self, value: Sequence[Contig | dict[str, Any]]
    ) -> InlineGenomeDefinition:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)


@with_property_setters
class InlineLocusAssembly(GenomeSpySchema):
    """Generated wrapper for ``InlineLocusAssembly``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineLocusAssembly", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        url: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(
        self, value: Sequence[Contig | dict[str, Any]]
    ) -> InlineLocusAssembly:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: str) -> InlineLocusAssembly:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class InteractionEventType(GenomeSpySchema):
    """Generated wrapper for ``InteractionEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InteractionEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class IntervalSelectionConfig(GenomeSpySchema):
    """Generated wrapper for ``IntervalSelectionConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IntervalSelectionConfig", {})

    def __init__(
        self,
        clear: DomEventType_T
        | EventConfig
        | EventConfigKwds
        | str
        | bool
        | UndefinedType = Undefined,
        encodings: Sequence[PrimaryPositionalChannel_T] | UndefinedType = Undefined,
        extent: SelectionExtent_T | UndefinedType = Undefined,
        mark: BrushConfig | dict[str, Any] | UndefinedType = Undefined,
        on: DomEventType_T
        | EventConfig
        | EventConfigKwds
        | str
        | UndefinedType = Undefined,
        type: Literal["interval"] | UndefinedType = Undefined,
        zoom: DomEventType_T
        | EventConfig
        | EventConfigKwds
        | str
        | bool
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            clear=clear,
            encodings=encodings,
            extent=extent,
            mark=mark,
            on=on,
            type=type,
            zoom=zoom,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_clear(
        self, value: DomEventType_T | EventConfig | EventConfigKwds | str | bool
    ) -> IntervalSelectionConfig:
        """Return a copy with ``clear`` updated."""
        return self._with_property("clear", value)

    def with_encodings(
        self, value: Sequence[PrimaryPositionalChannel_T]
    ) -> IntervalSelectionConfig:
        """Return a copy with ``encodings`` updated."""
        return self._with_property("encodings", value)

    def with_extent(self, value: SelectionExtent_T) -> IntervalSelectionConfig:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_mark(
        self,
        value: BrushConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``BrushConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_on(
        self, value: DomEventType_T | EventConfig | EventConfigKwds | str
    ) -> IntervalSelectionConfig:
        """Return a copy with ``on`` updated."""
        return self._with_property("on", value)

    def with_type(self, value: Literal["interval"]) -> IntervalSelectionConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_zoom(
        self, value: DomEventType_T | EventConfig | EventConfigKwds | str | bool
    ) -> IntervalSelectionConfig:
        """Return a copy with ``zoom`` updated."""
        return self._with_property("zoom", value)


@with_property_setters
class JsonDataFormat(GenomeSpySchema):
    """Generated wrapper for ``JsonDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("JsonDataFormat", {})

    def __init__(
        self,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        property: str | UndefinedType = Undefined,
        type: Literal["json"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(parse=parse, property=property, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> JsonDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_property(self, value: str) -> JsonDataFormat:
        """Return a copy with ``property`` updated."""
        return self._with_property("property", value)

    def with_type(self, value: Literal["json"]) -> JsonDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class KeyDef(GenomeSpySchema):
    """Generated wrapper for ``KeyDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("KeyDef", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> KeyDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: str) -> KeyDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: str | None) -> KeyDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


@with_property_setters
class LayerSpec(GenomeSpySchema):
    """Generated wrapper for ``LayerSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LayerSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        layer: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | DynamicOpacity
        | DynamicOpacityKwds
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        view: ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            height=height,
            layer=layer,
            legends=legends,
            name=name,
            opacity=opacity,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            templates=templates,
            title=title,
            transform=transform,
            view=view,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> LayerSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> LayerSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> LayerSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> LayerSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> LayerSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> LayerSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: LegendsKwds) -> LayerSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: str) -> LayerSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any],
    ) -> LayerSpec:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> LayerSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> LayerSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> LayerSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> LayerSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_templates(self, value: dict[str, Any]) -> LayerSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> LayerSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> LayerSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class LazyData(GenomeSpySchema):
    """Generated wrapper for ``LazyData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LazyData", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        lazy: LazyDataParams | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, lazy=lazy)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> LazyData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_lazy(
        self,
        value: LazyDataParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyData:
        """Return a copy with a ``LazyDataParams`` lazy."""
        return self._with_property("lazy", value, **kwargs)


@with_property_setters
class LazyDataParams(GenomeSpySchema):
    """Generated wrapper for ``LazyDataParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LazyDataParams", {})

    def __init__(
        self,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        axis: Axis | AxisKwds | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        columns: Sequence[str] | UndefinedType = Undefined,
        count: float | UndefinedType = Undefined,
        dataType: Type_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        pixelsPerBin: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sizeMode: Literal["area", "strokeWidth"] | UndefinedType = Undefined,
        type: Literal["vcf"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        values: Sequence[Scalar_T] | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            addChrPrefix=addChrPrefix,
            axis=axis,
            channel=channel,
            columns=columns,
            count=count,
            dataType=dataType,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            format=format,
            indexUrl=indexUrl,
            parse=parse,
            pixelsPerBin=pixelsPerBin,
            sizeMode=sizeMode,
            type=type,
            url=url,
            values=values,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_addChrPrefix(self, value: bool | str) -> LazyDataParams:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_axis(
        self,
        value: Axis | AxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``Axis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> LazyDataParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_columns(self, value: Sequence[str]) -> LazyDataParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_count(self, value: float) -> LazyDataParams:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_dataType(self, value: Type_T) -> LazyDataParams:
        """Return a copy with ``dataType`` updated."""
        return self._with_property("dataType", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> LazyDataParams:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_format(self, value: str) -> LazyDataParams:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> LazyDataParams:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_pixelsPerBin(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``ExprRef`` pixelsPerBin."""
        return self._with_property("pixelsPerBin", value, **kwargs)

    def with_sizeMode(self, value: Literal["area", "strokeWidth"]) -> LazyDataParams:
        """Return a copy with ``sizeMode`` updated."""
        return self._with_property("sizeMode", value)

    def with_type(self, value: Literal["vcf"]) -> LazyDataParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> LazyDataParams:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_values(self, value: Sequence[Scalar_T]) -> LazyDataParams:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_windowSize(self, value: float) -> LazyDataParams:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class Legend(GenomeSpySchema):
    """Generated wrapper for ``Legend``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Legend", {})

    def __init__(
        self,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            backgroundFill=backgroundFill,
            backgroundFillOpacity=backgroundFillOpacity,
            backgroundStroke=backgroundStroke,
            backgroundStrokeOpacity=backgroundStrokeOpacity,
            backgroundStrokeWidth=backgroundStrokeWidth,
            columns=columns,
            direction=direction,
            labelLimit=labelLimit,
            offset=offset,
            orient=orient,
            padding=padding,
            style=style,
            symbolSize=symbolSize,
            symbolType=symbolType,
            title=title,
            titleOrient=titleOrient,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_backgroundFill(self, value: str) -> Legend:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: float) -> Legend:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: str) -> Legend:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: float) -> Legend:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: float) -> Legend:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_columns(self, value: float) -> Legend:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_direction(self, value: LegendDirection_T) -> Legend:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_labelLimit(self, value: float) -> Legend:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_offset(self, value: float) -> Legend:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: LegendOrient_T | ExprRef | dict[str, Any]) -> Legend:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_padding(self, value: float) -> Legend:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_style(self, value: str | Sequence[str] | None) -> Legend:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_symbolSize(self, value: float) -> Legend:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolType(self, value: str) -> Legend:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_title(self, value: str | None) -> Legend:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleOrient(self, value: LegendTitleOrient_T) -> Legend:
        """Return a copy with ``titleOrient`` updated."""
        return self._with_property("titleOrient", value)

    def with_values(self, value: Sequence[str | float | bool]) -> Legend:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class LegendConfig(GenomeSpySchema):
    """Generated wrapper for ``LegendConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendConfig", {})

    def __init__(
        self,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        disable: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        rowPadding: float | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolBaseFillColor: str | UndefinedType = Undefined,
        symbolBaseStrokeColor: str | UndefinedType = Undefined,
        symbolOffset: float | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolStrokeWidth: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleColor: str | UndefinedType = Undefined,
        titleFont: str | UndefinedType = Undefined,
        titleFontSize: float | UndefinedType = Undefined,
        titleFontStyle: FontStyle_T | UndefinedType = Undefined,
        titleFontWeight: FontWeight_T | UndefinedType = Undefined,
        titleLimit: float | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        titlePadding: float | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            backgroundFill=backgroundFill,
            backgroundFillOpacity=backgroundFillOpacity,
            backgroundStroke=backgroundStroke,
            backgroundStrokeOpacity=backgroundStrokeOpacity,
            backgroundStrokeWidth=backgroundStrokeWidth,
            columnPadding=columnPadding,
            columns=columns,
            direction=direction,
            disable=disable,
            labelAlign=labelAlign,
            labelBaseline=labelBaseline,
            labelColor=labelColor,
            labelFont=labelFont,
            labelFontSize=labelFontSize,
            labelFontStyle=labelFontStyle,
            labelFontWeight=labelFontWeight,
            labelLimit=labelLimit,
            labelOffset=labelOffset,
            offset=offset,
            orient=orient,
            padding=padding,
            rowPadding=rowPadding,
            spacing=spacing,
            style=style,
            symbolBaseFillColor=symbolBaseFillColor,
            symbolBaseStrokeColor=symbolBaseStrokeColor,
            symbolOffset=symbolOffset,
            symbolSize=symbolSize,
            symbolStrokeWidth=symbolStrokeWidth,
            symbolType=symbolType,
            title=title,
            titleColor=titleColor,
            titleFont=titleFont,
            titleFontSize=titleFontSize,
            titleFontStyle=titleFontStyle,
            titleFontWeight=titleFontWeight,
            titleLimit=titleLimit,
            titleOrient=titleOrient,
            titlePadding=titlePadding,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_backgroundFill(self, value: str) -> LegendConfig:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: float) -> LegendConfig:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: str) -> LegendConfig:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: float) -> LegendConfig:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: float) -> LegendConfig:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_columnPadding(self, value: float) -> LegendConfig:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: float) -> LegendConfig:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_direction(self, value: LegendDirection_T) -> LegendConfig:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_disable(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``ExprRef`` disable."""
        return self._with_property("disable", value, **kwargs)

    def with_labelAlign(self, value: Align_T) -> LegendConfig:
        """Return a copy with ``labelAlign`` updated."""
        return self._with_property("labelAlign", value)

    def with_labelBaseline(self, value: Baseline_T) -> LegendConfig:
        """Return a copy with ``labelBaseline`` updated."""
        return self._with_property("labelBaseline", value)

    def with_labelColor(self, value: str) -> LegendConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: str) -> LegendConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: float) -> LegendConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(self, value: FontStyle_T) -> LegendConfig:
        """Return a copy with ``labelFontStyle`` updated."""
        return self._with_property("labelFontStyle", value)

    def with_labelFontWeight(self, value: FontWeight_T) -> LegendConfig:
        """Return a copy with ``labelFontWeight`` updated."""
        return self._with_property("labelFontWeight", value)

    def with_labelLimit(self, value: float) -> LegendConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelOffset(self, value: float) -> LegendConfig:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_offset(self, value: float) -> LegendConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self, value: LegendOrient_T | ExprRef | dict[str, Any]
    ) -> LegendConfig:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_padding(self, value: float) -> LegendConfig:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_rowPadding(self, value: float) -> LegendConfig:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_spacing(self, value: float) -> LegendConfig:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_style(self, value: str | Sequence[str] | None) -> LegendConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_symbolBaseFillColor(self, value: str) -> LegendConfig:
        """Return a copy with ``symbolBaseFillColor`` updated."""
        return self._with_property("symbolBaseFillColor", value)

    def with_symbolBaseStrokeColor(self, value: str) -> LegendConfig:
        """Return a copy with ``symbolBaseStrokeColor`` updated."""
        return self._with_property("symbolBaseStrokeColor", value)

    def with_symbolOffset(self, value: float) -> LegendConfig:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: float) -> LegendConfig:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: float) -> LegendConfig:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_symbolType(self, value: str) -> LegendConfig:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_title(self, value: str | None) -> LegendConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: str) -> LegendConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFont(self, value: str) -> LegendConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: float) -> LegendConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(self, value: FontStyle_T) -> LegendConfig:
        """Return a copy with ``titleFontStyle`` updated."""
        return self._with_property("titleFontStyle", value)

    def with_titleFontWeight(self, value: FontWeight_T) -> LegendConfig:
        """Return a copy with ``titleFontWeight`` updated."""
        return self._with_property("titleFontWeight", value)

    def with_titleLimit(self, value: float) -> LegendConfig:
        """Return a copy with ``titleLimit`` updated."""
        return self._with_property("titleLimit", value)

    def with_titleOrient(self, value: LegendTitleOrient_T) -> LegendConfig:
        """Return a copy with ``titleOrient`` updated."""
        return self._with_property("titleOrient", value)

    def with_titlePadding(self, value: float) -> LegendConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Sequence[str | float | bool]) -> LegendConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class LegendDirection(GenomeSpySchema):
    """Generated wrapper for ``LegendDirection``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendDirection", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class LegendOrient(GenomeSpySchema):
    """Generated wrapper for ``LegendOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class LegendTitleOrient(GenomeSpySchema):
    """Generated wrapper for ``LegendTitleOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendTitleOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class LinearizeGenomicCoordinateParams(GenomeSpySchema):
    """Generated wrapper for ``LinearizeGenomicCoordinateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "LinearizeGenomicCoordinateParams", {}
    )

    def __init__(
        self,
        channel: Literal["x", "y"] | UndefinedType = Undefined,
        chrom: Field_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        offset: float | Sequence[float] | UndefinedType = Undefined,
        pos: Field_T | Sequence[Field_T] | UndefinedType = Undefined,
        type: Literal["linearizeGenomicCoordinate"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel,
            chrom=chrom,
            description=description,
            offset=offset,
            pos=pos,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self, value: Literal["x", "y"]
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_chrom(self, value: Field_T) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_description(self, value: str) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_offset(
        self, value: float | Sequence[float]
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self, value: Field_T | Sequence[Field_T]
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_type(
        self, value: Literal["linearizeGenomicCoordinate"]
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class LinkConfig(GenomeSpySchema):
    """Generated wrapper for ``LinkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LinkConfig", {})

    def __init__(
        self,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clampApex: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        maxChordLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minArcHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical"]
        | Literal["horizontal"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        segments: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            arcFadingDistance=arcFadingDistance,
            arcHeightFactor=arcHeightFactor,
            buildIndex=buildIndex,
            clampApex=clampApex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            linkShape=linkShape,
            maxChordLength=maxChordLength,
            minArcHeight=minArcHeight,
            minBufferSize=minBufferSize,
            minPickingSize=minPickingSize,
            noFadingOnPointSelection=noFadingOnPointSelection,
            opacity=opacity,
            orient=orient,
            segments=segments,
            size=size,
            style=style,
            tooltip=tooltip,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_arcFadingDistance(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` arcFadingDistance."""
        return self._with_property("arcFadingDistance", value, **kwargs)

    def with_arcHeightFactor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` arcHeightFactor."""
        return self._with_property("arcHeightFactor", value, **kwargs)

    def with_buildIndex(self, value: bool) -> LinkConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clampApex(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` clampApex."""
        return self._with_property("clampApex", value, **kwargs)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> LinkConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> LinkConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_linkShape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` linkShape."""
        return self._with_property("linkShape", value, **kwargs)

    def with_maxChordLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` maxChordLength."""
        return self._with_property("maxChordLength", value, **kwargs)

    def with_minArcHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` minArcHeight."""
        return self._with_property("minArcHeight", value, **kwargs)

    def with_minBufferSize(self, value: float) -> LinkConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_noFadingOnPointSelection(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` noFadingOnPointSelection."""
        return self._with_property("noFadingOnPointSelection", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_segments(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` segments."""
        return self._with_property("segments", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> LinkConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> LinkConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> LinkConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> LinkConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class LinkProps(GenomeSpySchema):
    """Generated wrapper for ``LinkProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LinkProps", {})

    def __init__(
        self,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clampApex: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        maxChordLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minArcHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical"]
        | Literal["horizontal"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        segments: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["link"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            arcFadingDistance=arcFadingDistance,
            arcHeightFactor=arcHeightFactor,
            buildIndex=buildIndex,
            clampApex=clampApex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            linkShape=linkShape,
            maxChordLength=maxChordLength,
            minArcHeight=minArcHeight,
            minBufferSize=minBufferSize,
            minPickingSize=minPickingSize,
            noFadingOnPointSelection=noFadingOnPointSelection,
            opacity=opacity,
            orient=orient,
            segments=segments,
            size=size,
            style=style,
            tooltip=tooltip,
            type=type,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_arcFadingDistance(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` arcFadingDistance."""
        return self._with_property("arcFadingDistance", value, **kwargs)

    def with_arcHeightFactor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` arcHeightFactor."""
        return self._with_property("arcHeightFactor", value, **kwargs)

    def with_buildIndex(self, value: bool) -> LinkProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clampApex(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` clampApex."""
        return self._with_property("clampApex", value, **kwargs)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> LinkProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> LinkProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_linkShape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` linkShape."""
        return self._with_property("linkShape", value, **kwargs)

    def with_maxChordLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` maxChordLength."""
        return self._with_property("maxChordLength", value, **kwargs)

    def with_minArcHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` minArcHeight."""
        return self._with_property("minArcHeight", value, **kwargs)

    def with_minBufferSize(self, value: float) -> LinkProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_noFadingOnPointSelection(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` noFadingOnPointSelection."""
        return self._with_property("noFadingOnPointSelection", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_segments(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` segments."""
        return self._with_property("segments", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> LinkProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> LinkProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["link"]) -> LinkProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> LinkProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> LinkProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class MarkConfig(GenomeSpySchema):
    """Generated wrapper for ``MarkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkConfig", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            minBufferSize=minBufferSize,
            opacity=opacity,
            style=style,
            tooltip=tooltip,
            x=x,
            xOffset=xOffset,
            y=y,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> MarkConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> MarkConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> MarkConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_minBufferSize(self, value: float) -> MarkConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> MarkConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> MarkConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: float) -> MarkConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_yOffset(self, value: float) -> MarkConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class MarkPropDefStringNullTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<(string|null),TypeForShape>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "MarkPropDef<(string|null),TypeForShape>", {}
    )

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class MarkPropDefStringNull(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropDef<(string|null)>", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> MarkPropDefStringNull:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> MarkPropDefStringNull:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> MarkPropDefStringNull:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> MarkPropDefStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> MarkPropDefStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> MarkPropDefStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> MarkPropDefStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self, value: ChannelWithScale_T
    ) -> MarkPropDefStringNull:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> MarkPropDefStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> MarkPropDefStringNull:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class MarkPropDefNumber(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropDef<number>", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> MarkPropDefNumber:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> MarkPropDefNumber:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> MarkPropDefNumber:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> MarkPropDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> MarkPropDefNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> MarkPropDefNumber:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> MarkPropDefNumber:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> MarkPropDefNumber:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> MarkPropDefNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> MarkPropDefNumber:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class MarkPropExprDef(GenomeSpySchema):
    """Generated wrapper for ``MarkPropExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropExprDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            description=description,
            domainInert=domainInert,
            expr=expr,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> MarkPropExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> MarkPropExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> MarkPropExprDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: str) -> MarkPropExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> MarkPropExprDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropExprDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> MarkPropExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> MarkPropExprDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class MarkProps(GenomeSpySchema):
    """Generated wrapper for ``MarkProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkProps", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clampApex: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadius: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        fitToBand: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        hatch: Literal["none"]
        | Literal["diagonal"]
        | Literal["antiDiagonal"]
        | Literal["cross"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | Literal["grid"]
        | Literal["dots"]
        | Literal["rings"]
        | Literal["ringsLarge"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        inwardStroke: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        logoLetters: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        maxChordLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minArcHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical"]
        | Literal["horizontal"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        paddingX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        segments: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticScore: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticZoomFraction: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shape: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        squeeze: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        text: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["point"] | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            angle=angle,
            arcFadingDistance=arcFadingDistance,
            arcHeightFactor=arcHeightFactor,
            baseline=baseline,
            buildIndex=buildIndex,
            clampApex=clampApex,
            clip=clip,
            color=color,
            cornerRadius=cornerRadius,
            cornerRadiusBottomLeft=cornerRadiusBottomLeft,
            cornerRadiusBottomRight=cornerRadiusBottomRight,
            cornerRadiusTopLeft=cornerRadiusTopLeft,
            cornerRadiusTopRight=cornerRadiusTopRight,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            dx=dx,
            dy=dy,
            fill=fill,
            fillGradientStrength=fillGradientStrength,
            fillOpacity=fillOpacity,
            filled=filled,
            fitToBand=fitToBand,
            flushX=flushX,
            flushY=flushY,
            font=font,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            geometricZoomBound=geometricZoomBound,
            hatch=hatch,
            inwardStroke=inwardStroke,
            linkShape=linkShape,
            logoLetters=logoLetters,
            maxChordLength=maxChordLength,
            minArcHeight=minArcHeight,
            minBufferSize=minBufferSize,
            minHeight=minHeight,
            minLength=minLength,
            minOpacity=minOpacity,
            minPickingSize=minPickingSize,
            minWidth=minWidth,
            noFadingOnPointSelection=noFadingOnPointSelection,
            opacity=opacity,
            orient=orient,
            paddingX=paddingX,
            paddingY=paddingY,
            sampleFacetPadding=sampleFacetPadding,
            segments=segments,
            semanticScore=semanticScore,
            semanticZoomFraction=semanticZoomFraction,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            shape=shape,
            size=size,
            squeeze=squeeze,
            stroke=stroke,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            text=text,
            thickness=thickness,
            tooltip=tooltip,
            type=type,
            viewportEdgeFadeDistanceBottom=viewportEdgeFadeDistanceBottom,
            viewportEdgeFadeDistanceLeft=viewportEdgeFadeDistanceLeft,
            viewportEdgeFadeDistanceRight=viewportEdgeFadeDistanceRight,
            viewportEdgeFadeDistanceTop=viewportEdgeFadeDistanceTop,
            viewportEdgeFadeWidthBottom=viewportEdgeFadeWidthBottom,
            viewportEdgeFadeWidthLeft=viewportEdgeFadeWidthLeft,
            viewportEdgeFadeWidthRight=viewportEdgeFadeWidthRight,
            viewportEdgeFadeWidthTop=viewportEdgeFadeWidthTop,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> MarkProps:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_arcFadingDistance(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` arcFadingDistance."""
        return self._with_property("arcFadingDistance", value, **kwargs)

    def with_arcHeightFactor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` arcHeightFactor."""
        return self._with_property("arcHeightFactor", value, **kwargs)

    def with_baseline(self, value: Baseline_T) -> MarkProps:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_buildIndex(self, value: bool) -> MarkProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clampApex(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` clampApex."""
        return self._with_property("clampApex", value, **kwargs)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> MarkProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cornerRadius(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cornerRadius."""
        return self._with_property("cornerRadius", value, **kwargs)

    def with_cornerRadiusBottomLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomLeft."""
        return self._with_property("cornerRadiusBottomLeft", value, **kwargs)

    def with_cornerRadiusBottomRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomRight."""
        return self._with_property("cornerRadiusBottomRight", value, **kwargs)

    def with_cornerRadiusTopLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cornerRadiusTopLeft."""
        return self._with_property("cornerRadiusTopLeft", value, **kwargs)

    def with_cornerRadiusTopRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cornerRadiusTopRight."""
        return self._with_property("cornerRadiusTopRight", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> MarkProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_dx(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` dx."""
        return self._with_property("dx", value, **kwargs)

    def with_dy(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` dy."""
        return self._with_property("dy", value, **kwargs)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillGradientStrength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` fillGradientStrength."""
        return self._with_property("fillGradientStrength", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> MarkProps:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_fitToBand(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` fitToBand."""
        return self._with_property("fitToBand", value, **kwargs)

    def with_flushX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` flushX."""
        return self._with_property("flushX", value, **kwargs)

    def with_flushY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` flushY."""
        return self._with_property("flushY", value, **kwargs)

    def with_font(self, value: str) -> MarkProps:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(self, value: FontStyle_T) -> MarkProps:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> MarkProps:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_geometricZoomBound(self, value: float) -> MarkProps:
        """Return a copy with ``geometricZoomBound`` updated."""
        return self._with_property("geometricZoomBound", value)

    def with_hatch(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` hatch."""
        return self._with_property("hatch", value, **kwargs)

    def with_inwardStroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` inwardStroke."""
        return self._with_property("inwardStroke", value, **kwargs)

    def with_linkShape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` linkShape."""
        return self._with_property("linkShape", value, **kwargs)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_maxChordLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` maxChordLength."""
        return self._with_property("maxChordLength", value, **kwargs)

    def with_minArcHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minArcHeight."""
        return self._with_property("minArcHeight", value, **kwargs)

    def with_minBufferSize(self, value: float) -> MarkProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minHeight."""
        return self._with_property("minHeight", value, **kwargs)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_minOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minOpacity."""
        return self._with_property("minOpacity", value, **kwargs)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_minWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` minWidth."""
        return self._with_property("minWidth", value, **kwargs)

    def with_noFadingOnPointSelection(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` noFadingOnPointSelection."""
        return self._with_property("noFadingOnPointSelection", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_paddingX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` paddingX."""
        return self._with_property("paddingX", value, **kwargs)

    def with_paddingY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` paddingY."""
        return self._with_property("paddingY", value, **kwargs)

    def with_sampleFacetPadding(self, value: float) -> MarkProps:
        """Return a copy with ``sampleFacetPadding`` updated."""
        return self._with_property("sampleFacetPadding", value)

    def with_segments(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` segments."""
        return self._with_property("segments", value, **kwargs)

    def with_semanticScore(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` semanticScore."""
        return self._with_property("semanticScore", value, **kwargs)

    def with_semanticZoomFraction(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` semanticZoomFraction."""
        return self._with_property("semanticZoomFraction", value, **kwargs)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_shape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` shape."""
        return self._with_property("shape", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_squeeze(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` squeeze."""
        return self._with_property("squeeze", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> MarkProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> MarkProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> MarkProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(self, value: Scalar_T | ExprRef | dict[str, Any]) -> MarkProps:
        """Return a copy with ``text`` updated."""
        return self._with_property("text", value)

    def with_thickness(self, value: float) -> MarkProps:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> MarkProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["point"]) -> MarkProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: float) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthTop`` updated."""
        return self._with_property("viewportEdgeFadeWidthTop", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> MarkProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> MarkProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class MarkType(GenomeSpySchema):
    """Generated wrapper for ``MarkType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class MeasureTextParams(GenomeSpySchema):
    """Generated wrapper for ``MeasureTextParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MeasureTextParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        type: Literal["measureText"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            field=field,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> MeasureTextParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Field_T) -> MeasureTextParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_font(self, value: str) -> MeasureTextParams:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MeasureTextParams:
        """Return a copy with a ``ExprRef`` fontSize."""
        return self._with_property("fontSize", value, **kwargs)

    def with_fontStyle(self, value: FontStyle_T) -> MeasureTextParams:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> MeasureTextParams:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_type(self, value: Literal["measureText"]) -> MeasureTextParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class MergeFacetsParams(GenomeSpySchema):
    """Generated wrapper for ``MergeFacetsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MergeFacetsParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        type: Literal["mergeFacets"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> MergeFacetsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_type(self, value: Literal["mergeFacets"]) -> MergeFacetsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class MultiUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``MultiUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiUrlSourceRef", {})

    def __init__(
        self,
        attach: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: FieldName_T | UndefinedType = Undefined,
        maxValues: float | UndefinedType = Undefined,
        onLoadError: Literal["error", "skip"] | UndefinedType = Undefined,
        template: str | UndefinedType = Undefined,
        values: Sequence[Scalar_T]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            attach=attach,
            expr=expr,
            field=field,
            maxValues=maxValues,
            onLoadError=onLoadError,
            template=template,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_attach(self, value: bool) -> MultiUrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: str) -> MultiUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: FieldName_T) -> MultiUrlSourceRef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_maxValues(self, value: float) -> MultiUrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Literal["error", "skip"]) -> MultiUrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: str) -> MultiUrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)

    def with_values(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiUrlSourceRef:
        """Return a copy with a ``ExprRef`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class MultiscaleSpec(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        multiscale: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | DynamicOpacity
        | DynamicOpacityKwds
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        stops: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any]
        | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        view: ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            height=height,
            legends=legends,
            multiscale=multiscale,
            name=name,
            opacity=opacity,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            stops=stops,
            templates=templates,
            title=title,
            transform=transform,
            view=view,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> MultiscaleSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> MultiscaleSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> MultiscaleSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> MultiscaleSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> MultiscaleSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: LegendsKwds) -> MultiscaleSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_multiscale(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> MultiscaleSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: str) -> MultiscaleSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any],
    ) -> MultiscaleSpec:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> MultiscaleSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> MultiscaleSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> MultiscaleSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> MultiscaleSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_stops(
        self,
        value: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any],
    ) -> MultiscaleSpec:
        """Return a copy with ``stops`` updated."""
        return self._with_property("stops", value)

    def with_templates(self, value: dict[str, Any]) -> MultiscaleSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> MultiscaleSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> MultiscaleSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class MultiscaleStops(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleStops``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleStops", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T
        | Literal["auto"]
        | UndefinedType = Undefined,
        fade: float | UndefinedType = Undefined,
        metric: Literal["unitsPerPixel"] | UndefinedType = Undefined,
        values: Sequence[float | ExprRef | dict[str, Any]] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, fade=fade, metric=metric, values=values)
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self, value: PrimaryPositionalChannel_T | Literal["auto"]
    ) -> MultiscaleStops:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_fade(self, value: float) -> MultiscaleStops:
        """Return a copy with ``fade`` updated."""
        return self._with_property("fade", value)

    def with_metric(self, value: Literal["unitsPerPixel"]) -> MultiscaleStops:
        """Return a copy with ``metric`` updated."""
        return self._with_property("metric", value)

    def with_values(
        self, value: Sequence[float | ExprRef | dict[str, Any]]
    ) -> MultiscaleStops:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class MultiscaleStopsDef(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleStopsDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleStopsDef", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T
        | Literal["auto"]
        | UndefinedType = Undefined,
        fade: float | UndefinedType = Undefined,
        metric: Literal["unitsPerPixel"] | UndefinedType = Undefined,
        values: Sequence[float | ExprRef | dict[str, Any]] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, fade=fade, metric=metric, values=values)
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self, value: PrimaryPositionalChannel_T | Literal["auto"]
    ) -> MultiscaleStopsDef:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_fade(self, value: float) -> MultiscaleStopsDef:
        """Return a copy with ``fade`` updated."""
        return self._with_property("fade", value)

    def with_metric(self, value: Literal["unitsPerPixel"]) -> MultiscaleStopsDef:
        """Return a copy with ``metric`` updated."""
        return self._with_property("metric", value)

    def with_values(
        self, value: Sequence[float | ExprRef | dict[str, Any]]
    ) -> MultiscaleStopsDef:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class NamedData(GenomeSpySchema):
    """Generated wrapper for ``NamedData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NamedData", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, format=format, name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> NamedData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> NamedData:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_name(self, value: str) -> NamedData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class NamedGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``NamedGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NamedGenomeConfig", {})

    def __init__(
        self,
        contigs: Sequence[Contig | dict[str, Any]] | UndefinedType = Undefined,
        url: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(
        self, value: Sequence[Contig | dict[str, Any]]
    ) -> NamedGenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: str) -> NamedGenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class NumericDomain(GenomeSpySchema):
    """Generated wrapper for ``NumericDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class NumericMarkPropDef(GenomeSpySchema):
    """Generated wrapper for ``NumericMarkPropDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericMarkPropDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> NumericMarkPropDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> NumericMarkPropDef:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> NumericMarkPropDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> NumericMarkPropDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> NumericMarkPropDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> NumericMarkPropDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> NumericMarkPropDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> NumericMarkPropDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> NumericMarkPropDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> NumericMarkPropDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class NumericStopDef(GenomeSpySchema):
    """Generated wrapper for ``NumericStopDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericStopDef", {})

    def __init__(self, expr: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: str) -> NumericStopDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


@with_property_setters
class NumericValueDef(GenomeSpySchema):
    """Generated wrapper for ``NumericValueDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericValueDef", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> NumericValueDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> NumericValueDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericValueDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class OtherDataFormat(GenomeSpySchema):
    """Generated wrapper for ``OtherDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("OtherDataFormat", {})

    def __init__(
        self,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> OtherDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: str) -> OtherDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class PackLegendLabelsParams(GenomeSpySchema):
    """Generated wrapper for ``PackLegendLabelsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PackLegendLabelsParams", {})

    def __init__(
        self,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        direction: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        fontSize: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        labelWidth: Field_T | UndefinedType = Undefined,
        rowPadding: float | UndefinedType = Undefined,
        symbolOffset: float | UndefinedType = Undefined,
        symbolSize: float | Field_T | UndefinedType = Undefined,
        symbolStrokeWidth: float | Field_T | UndefinedType = Undefined,
        type: Literal["packLegendLabels"] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        yExtent: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            columnPadding=columnPadding,
            columns=columns,
            description=description,
            direction=direction,
            fontSize=fontSize,
            labelOffset=labelOffset,
            labelWidth=labelWidth,
            rowPadding=rowPadding,
            symbolOffset=symbolOffset,
            symbolSize=symbolSize,
            symbolStrokeWidth=symbolStrokeWidth,
            type=type,
            xOffset=xOffset,
            yExtent=yExtent,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_columnPadding(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_description(self, value: str) -> PackLegendLabelsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_direction(
        self, value: Literal["vertical", "horizontal"]
    ) -> PackLegendLabelsParams:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_fontSize(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_labelOffset(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelWidth(self, value: Field_T) -> PackLegendLabelsParams:
        """Return a copy with ``labelWidth`` updated."""
        return self._with_property("labelWidth", value)

    def with_rowPadding(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_symbolOffset(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: float | Field_T) -> PackLegendLabelsParams:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: float | Field_T) -> PackLegendLabelsParams:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_type(self, value: Literal["packLegendLabels"]) -> PackLegendLabelsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_xOffset(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_yExtent(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PackLegendLabelsParams:
        """Return a copy with a ``ExprRef`` yExtent."""
        return self._with_property("yExtent", value, **kwargs)

    def with_yOffset(self, value: float) -> PackLegendLabelsParams:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class PaddingConfig(GenomeSpySchema):
    """Generated wrapper for ``PaddingConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PaddingConfig", {})

    def __init__(
        self,
        bottom: float | UndefinedType = Undefined,
        left: float | UndefinedType = Undefined,
        right: float | UndefinedType = Undefined,
        top: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(bottom=bottom, left=left, right=right, top=top)
        if kwds:
            self._kwds.update(kwds)

    def with_bottom(self, value: float) -> PaddingConfig:
        """Return a copy with ``bottom`` updated."""
        return self._with_property("bottom", value)

    def with_left(self, value: float) -> PaddingConfig:
        """Return a copy with ``left`` updated."""
        return self._with_property("left", value)

    def with_right(self, value: float) -> PaddingConfig:
        """Return a copy with ``right`` updated."""
        return self._with_property("right", value)

    def with_top(self, value: float) -> PaddingConfig:
        """Return a copy with ``top`` updated."""
        return self._with_property("top", value)


@with_property_setters
class Paddings(GenomeSpySchema):
    """Generated wrapper for ``Paddings``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Paddings", {})

    def __init__(
        self,
        bottom: float | UndefinedType = Undefined,
        left: float | UndefinedType = Undefined,
        right: float | UndefinedType = Undefined,
        top: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(bottom=bottom, left=left, right=right, top=top)
        if kwds:
            self._kwds.update(kwds)

    def with_bottom(self, value: float) -> Paddings:
        """Return a copy with ``bottom`` updated."""
        return self._with_property("bottom", value)

    def with_left(self, value: float) -> Paddings:
        """Return a copy with ``left`` updated."""
        return self._with_property("left", value)

    def with_right(self, value: float) -> Paddings:
        """Return a copy with ``right`` updated."""
        return self._with_property("right", value)

    def with_top(self, value: float) -> Paddings:
        """Return a copy with ``top`` updated."""
        return self._with_property("top", value)


@with_property_setters
class Parameter(GenomeSpySchema):
    """Generated wrapper for ``Parameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Parameter", {})

    def __init__(
        self,
        bind: BindCheckbox
        | BindCheckboxKwds
        | BindRadioSelect
        | BindRadioSelectKwds
        | BindRange
        | BindRangeKwds
        | BindInput
        | BindInputKwds
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        persist: bool | UndefinedType = Undefined,
        push: Literal["outer"] | UndefinedType = Undefined,
        ruler: RulerConfig | RulerConfigKwds | UndefinedType = Undefined,
        select: SelectionType_T
        | PointSelectionConfig
        | dict[str, Any]
        | IntervalSelectionConfig
        | UndefinedType = Undefined,
        value: RulerInitMapping | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            bind=bind,
            description=description,
            expr=expr,
            name=name,
            persist=persist,
            push=push,
            ruler=ruler,
            select=select,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_bind(
        self,
        value: BindCheckbox
        | BindCheckboxKwds
        | BindRadioSelect
        | BindRadioSelectKwds
        | BindRange
        | BindRangeKwds
        | BindInput
        | BindInputKwds,
    ) -> Parameter:
        """Return a copy with ``bind`` updated."""
        return self._with_property("bind", value)

    def with_description(self, value: str) -> Parameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: str) -> Parameter:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_name(self, value: str) -> Parameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: bool) -> Parameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Literal["outer"]) -> Parameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_ruler(
        self,
        value: RulerConfig | RulerConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``RulerConfig`` ruler."""
        return self._with_property("ruler", value, **kwargs)

    def with_select(
        self,
        value: SelectionType_T
        | PointSelectionConfig
        | dict[str, Any]
        | IntervalSelectionConfig,
    ) -> Parameter:
        """Return a copy with ``select`` updated."""
        return self._with_property("select", value)

    def with_value(
        self,
        value: RulerInitMapping | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``RulerInitMapping`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class Parse(GenomeSpySchema):
    """Generated wrapper for ``Parse``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Parse", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ParseValue(GenomeSpySchema):
    """Generated wrapper for ``ParseValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ParseValue", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class PileupParams(GenomeSpySchema):
    """Generated wrapper for ``PileupParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PileupParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        end: Field_T | UndefinedType = Undefined,
        preference: Field_T | UndefinedType = Undefined,
        preferredOrder: Sequence[str]
        | Sequence[float]
        | Sequence[bool]
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
        type: Literal["pileup"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            end=end,
            preference=preference,
            preferredOrder=preferredOrder,
            spacing=spacing,
            start=start,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> PileupParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_end(self, value: Field_T) -> PileupParams:
        """Return a copy with ``end`` updated."""
        return self._with_property("end", value)

    def with_preference(self, value: Field_T) -> PileupParams:
        """Return a copy with ``preference`` updated."""
        return self._with_property("preference", value)

    def with_preferredOrder(
        self, value: Sequence[str] | Sequence[float] | Sequence[bool]
    ) -> PileupParams:
        """Return a copy with ``preferredOrder`` updated."""
        return self._with_property("preferredOrder", value)

    def with_spacing(self, value: float) -> PileupParams:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_start(self, value: Field_T) -> PileupParams:
        """Return a copy with ``start`` updated."""
        return self._with_property("start", value)

    def with_type(self, value: Literal["pileup"]) -> PileupParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class PointConfig(GenomeSpySchema):
    """Generated wrapper for ``PointConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointConfig", {})

    def __init__(
        self,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        inwardStroke: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        semanticScore: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticZoomFraction: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shape: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            angle=angle,
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            dx=dx,
            dy=dy,
            fill=fill,
            fillGradientStrength=fillGradientStrength,
            fillOpacity=fillOpacity,
            filled=filled,
            geometricZoomBound=geometricZoomBound,
            inwardStroke=inwardStroke,
            minBufferSize=minBufferSize,
            minPickingSize=minPickingSize,
            opacity=opacity,
            sampleFacetPadding=sampleFacetPadding,
            semanticScore=semanticScore,
            semanticZoomFraction=semanticZoomFraction,
            shape=shape,
            size=size,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            tooltip=tooltip,
            x=x,
            xOffset=xOffset,
            y=y,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_buildIndex(self, value: bool) -> PointConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> PointConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> PointConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_dx(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` dx."""
        return self._with_property("dx", value, **kwargs)

    def with_dy(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` dy."""
        return self._with_property("dy", value, **kwargs)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillGradientStrength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` fillGradientStrength."""
        return self._with_property("fillGradientStrength", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> PointConfig:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_geometricZoomBound(self, value: float) -> PointConfig:
        """Return a copy with ``geometricZoomBound`` updated."""
        return self._with_property("geometricZoomBound", value)

    def with_inwardStroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` inwardStroke."""
        return self._with_property("inwardStroke", value, **kwargs)

    def with_minBufferSize(self, value: float) -> PointConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_sampleFacetPadding(self, value: float) -> PointConfig:
        """Return a copy with ``sampleFacetPadding`` updated."""
        return self._with_property("sampleFacetPadding", value)

    def with_semanticScore(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` semanticScore."""
        return self._with_property("semanticScore", value, **kwargs)

    def with_semanticZoomFraction(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` semanticZoomFraction."""
        return self._with_property("semanticZoomFraction", value, **kwargs)

    def with_shape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` shape."""
        return self._with_property("shape", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> PointConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> PointConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: float) -> PointConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_yOffset(self, value: float) -> PointConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class PointProps(GenomeSpySchema):
    """Generated wrapper for ``PointProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointProps", {})

    def __init__(
        self,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        inwardStroke: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        semanticScore: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticZoomFraction: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shape: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["point"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            angle=angle,
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            dx=dx,
            dy=dy,
            fill=fill,
            fillGradientStrength=fillGradientStrength,
            fillOpacity=fillOpacity,
            filled=filled,
            geometricZoomBound=geometricZoomBound,
            inwardStroke=inwardStroke,
            minBufferSize=minBufferSize,
            minPickingSize=minPickingSize,
            opacity=opacity,
            sampleFacetPadding=sampleFacetPadding,
            semanticScore=semanticScore,
            semanticZoomFraction=semanticZoomFraction,
            shape=shape,
            size=size,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            tooltip=tooltip,
            type=type,
            x=x,
            xOffset=xOffset,
            y=y,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_buildIndex(self, value: bool) -> PointProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> PointProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> PointProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_dx(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` dx."""
        return self._with_property("dx", value, **kwargs)

    def with_dy(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` dy."""
        return self._with_property("dy", value, **kwargs)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillGradientStrength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` fillGradientStrength."""
        return self._with_property("fillGradientStrength", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> PointProps:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_geometricZoomBound(self, value: float) -> PointProps:
        """Return a copy with ``geometricZoomBound`` updated."""
        return self._with_property("geometricZoomBound", value)

    def with_inwardStroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` inwardStroke."""
        return self._with_property("inwardStroke", value, **kwargs)

    def with_minBufferSize(self, value: float) -> PointProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_sampleFacetPadding(self, value: float) -> PointProps:
        """Return a copy with ``sampleFacetPadding`` updated."""
        return self._with_property("sampleFacetPadding", value)

    def with_semanticScore(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` semanticScore."""
        return self._with_property("semanticScore", value, **kwargs)

    def with_semanticZoomFraction(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` semanticZoomFraction."""
        return self._with_property("semanticZoomFraction", value, **kwargs)

    def with_shape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` shape."""
        return self._with_property("shape", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> PointProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> PointProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["point"]) -> PointProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: float) -> PointProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_yOffset(self, value: float) -> PointProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class PointSelectionConfig(GenomeSpySchema):
    """Generated wrapper for ``PointSelectionConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointSelectionConfig", {})

    def __init__(
        self,
        clear: DomEventType_T
        | EventConfig
        | EventConfigKwds
        | str
        | bool
        | UndefinedType = Undefined,
        on: DomEventType_T
        | EventConfig
        | EventConfigKwds
        | str
        | UndefinedType = Undefined,
        toggle: bool | UndefinedType = Undefined,
        type: Literal["point"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(clear=clear, on=on, toggle=toggle, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_clear(
        self, value: DomEventType_T | EventConfig | EventConfigKwds | str | bool
    ) -> PointSelectionConfig:
        """Return a copy with ``clear`` updated."""
        return self._with_property("clear", value)

    def with_on(
        self, value: DomEventType_T | EventConfig | EventConfigKwds | str
    ) -> PointSelectionConfig:
        """Return a copy with ``on`` updated."""
        return self._with_property("on", value)

    def with_toggle(self, value: bool) -> PointSelectionConfig:
        """Return a copy with ``toggle`` updated."""
        return self._with_property("toggle", value)

    def with_type(self, value: Literal["point"]) -> PointSelectionConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Position2Def(GenomeSpySchema):
    """Generated wrapper for ``Position2Def``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Position2Def", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        chrom: FieldName_T | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        pos: FieldName_T | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            chrom=chrom,
            datum=datum,
            description=description,
            domainInert=domainInert,
            expr=expr,
            field=field,
            offset=offset,
            pos=pos,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> Position2Def:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(self, value: FieldName_T) -> Position2Def:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> Position2Def:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> Position2Def:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> Position2Def:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: str) -> Position2Def:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: str) -> Position2Def:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_offset(self, value: float) -> Position2Def:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(self, value: FieldName_T) -> Position2Def:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> Position2Def:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> Position2Def:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> Position2Def:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class PositionDatumDef(GenomeSpySchema):
    """Generated wrapper for ``PositionDatumDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionDatumDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            datum=datum,
            description=description,
            domainInert=domainInert,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> PositionDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self, value: Scalar_T | ExprRef | dict[str, Any]
    ) -> PositionDatumDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> PositionDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> PositionDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> PositionDatumDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> PositionDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> PositionDatumDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class PositionDef(GenomeSpySchema):
    """Generated wrapper for ``PositionDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        chrom: FieldName_T | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        pos: FieldName_T | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            chrom=chrom,
            datum=datum,
            description=description,
            domainInert=domainInert,
            expr=expr,
            field=field,
            offset=offset,
            pos=pos,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> PositionDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(self, value: FieldName_T) -> PositionDef:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> PositionDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> PositionDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> PositionDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: str) -> PositionDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: str) -> PositionDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_offset(self, value: float) -> PositionDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(self, value: FieldName_T) -> PositionDef:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> PositionDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> PositionDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> PositionDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class PositionExprDef(GenomeSpySchema):
    """Generated wrapper for ``PositionExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionExprDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            description=description,
            domainInert=domainInert,
            expr=expr,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionExprDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> PositionExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> PositionExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> PositionExprDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: str) -> PositionExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_title(self, value: str | None) -> PositionExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> PositionExprDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class PositionFieldDef(GenomeSpySchema):
    """Generated wrapper for ``PositionFieldDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionFieldDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            description=description,
            domainInert=domainInert,
            field=field,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> PositionFieldDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: str) -> PositionFieldDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> PositionFieldDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> PositionFieldDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> PositionFieldDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> PositionFieldDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> PositionFieldDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class PositionValueDef(GenomeSpySchema):
    """Generated wrapper for ``PositionValueDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionValueDef", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> PositionValueDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> PositionValueDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionValueDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class PositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``PositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class PrimaryPositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``PrimaryPositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PrimaryPositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ProjectParams(GenomeSpySchema):
    """Generated wrapper for ``ProjectParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ProjectParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | UndefinedType = Undefined,
        type: Literal["project"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, fields=fields, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ProjectParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(self, value: Sequence[Field_T]) -> ProjectParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_type(self, value: Literal["project"]) -> ProjectParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class RangeConfig(GenomeSpySchema):
    """Generated wrapper for ``RangeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RangeConfig", {})

    def __init__(
        self,
        angle: Sequence[float] | UndefinedType = Undefined,
        diverging: str | SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        heatmap: str | SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        ramp: str | SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        shape: Sequence[str] | UndefinedType = Undefined,
        size: Sequence[float] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            angle=angle,
            diverging=diverging,
            heatmap=heatmap,
            ramp=ramp,
            shape=shape,
            size=size,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_angle(self, value: Sequence[float]) -> RangeConfig:
        """Return a copy with ``angle`` updated."""
        return self._with_property("angle", value)

    def with_diverging(
        self, value: str | SchemeParams | SchemeParamsKwds
    ) -> RangeConfig:
        """Return a copy with ``diverging`` updated."""
        return self._with_property("diverging", value)

    def with_heatmap(self, value: str | SchemeParams | SchemeParamsKwds) -> RangeConfig:
        """Return a copy with ``heatmap`` updated."""
        return self._with_property("heatmap", value)

    def with_ramp(self, value: str | SchemeParams | SchemeParamsKwds) -> RangeConfig:
        """Return a copy with ``ramp`` updated."""
        return self._with_property("ramp", value)

    def with_shape(self, value: Sequence[str]) -> RangeConfig:
        """Return a copy with ``shape`` updated."""
        return self._with_property("shape", value)

    def with_size(self, value: Sequence[float]) -> RangeConfig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)


@with_property_setters
class RectConfig(GenomeSpySchema):
    """Generated wrapper for ``RectConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RectConfig", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadius: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        hatch: Literal["none"]
        | Literal["diagonal"]
        | Literal["antiDiagonal"]
        | Literal["cross"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | Literal["grid"]
        | Literal["dots"]
        | Literal["rings"]
        | Literal["ringsLarge"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cornerRadius=cornerRadius,
            cornerRadiusBottomLeft=cornerRadiusBottomLeft,
            cornerRadiusBottomRight=cornerRadiusBottomRight,
            cornerRadiusTopLeft=cornerRadiusTopLeft,
            cornerRadiusTopRight=cornerRadiusTopRight,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            fill=fill,
            fillOpacity=fillOpacity,
            filled=filled,
            hatch=hatch,
            minBufferSize=minBufferSize,
            minHeight=minHeight,
            minOpacity=minOpacity,
            minWidth=minWidth,
            opacity=opacity,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            tooltip=tooltip,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> RectConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> RectConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cornerRadius(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cornerRadius."""
        return self._with_property("cornerRadius", value, **kwargs)

    def with_cornerRadiusBottomLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomLeft."""
        return self._with_property("cornerRadiusBottomLeft", value, **kwargs)

    def with_cornerRadiusBottomRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomRight."""
        return self._with_property("cornerRadiusBottomRight", value, **kwargs)

    def with_cornerRadiusTopLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusTopLeft."""
        return self._with_property("cornerRadiusTopLeft", value, **kwargs)

    def with_cornerRadiusTopRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusTopRight."""
        return self._with_property("cornerRadiusTopRight", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> RectConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> RectConfig:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_hatch(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` hatch."""
        return self._with_property("hatch", value, **kwargs)

    def with_minBufferSize(self, value: float) -> RectConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` minHeight."""
        return self._with_property("minHeight", value, **kwargs)

    def with_minOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` minOpacity."""
        return self._with_property("minOpacity", value, **kwargs)

    def with_minWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` minWidth."""
        return self._with_property("minWidth", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> RectConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> RectConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> RectConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> RectConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class RectProps(GenomeSpySchema):
    """Generated wrapper for ``RectProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RectProps", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadius: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        hatch: Literal["none"]
        | Literal["diagonal"]
        | Literal["antiDiagonal"]
        | Literal["cross"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | Literal["grid"]
        | Literal["dots"]
        | Literal["rings"]
        | Literal["ringsLarge"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["rect"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cornerRadius=cornerRadius,
            cornerRadiusBottomLeft=cornerRadiusBottomLeft,
            cornerRadiusBottomRight=cornerRadiusBottomRight,
            cornerRadiusTopLeft=cornerRadiusTopLeft,
            cornerRadiusTopRight=cornerRadiusTopRight,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            fill=fill,
            fillOpacity=fillOpacity,
            filled=filled,
            hatch=hatch,
            minBufferSize=minBufferSize,
            minHeight=minHeight,
            minOpacity=minOpacity,
            minWidth=minWidth,
            opacity=opacity,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            tooltip=tooltip,
            type=type,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> RectProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> RectProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cornerRadius(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cornerRadius."""
        return self._with_property("cornerRadius", value, **kwargs)

    def with_cornerRadiusBottomLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomLeft."""
        return self._with_property("cornerRadiusBottomLeft", value, **kwargs)

    def with_cornerRadiusBottomRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomRight."""
        return self._with_property("cornerRadiusBottomRight", value, **kwargs)

    def with_cornerRadiusTopLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cornerRadiusTopLeft."""
        return self._with_property("cornerRadiusTopLeft", value, **kwargs)

    def with_cornerRadiusTopRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cornerRadiusTopRight."""
        return self._with_property("cornerRadiusTopRight", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> RectProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> RectProps:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_hatch(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` hatch."""
        return self._with_property("hatch", value, **kwargs)

    def with_minBufferSize(self, value: float) -> RectProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` minHeight."""
        return self._with_property("minHeight", value, **kwargs)

    def with_minOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` minOpacity."""
        return self._with_property("minOpacity", value, **kwargs)

    def with_minWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` minWidth."""
        return self._with_property("minWidth", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> RectProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> RectProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["rect"]) -> RectProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> RectProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> RectProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class RegexExtractParams(GenomeSpySchema):
    """Generated wrapper for ``RegexExtractParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RegexExtractParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        regex: str | UndefinedType = Undefined,
        skipInvalidInput: bool | UndefinedType = Undefined,
        type: Literal["regexExtract"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            field=field,
            regex=regex,
            skipInvalidInput=skipInvalidInput,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> RegexExtractParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Field_T) -> RegexExtractParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_regex(self, value: str) -> RegexExtractParams:
        """Return a copy with ``regex`` updated."""
        return self._with_property("regex", value)

    def with_skipInvalidInput(self, value: bool) -> RegexExtractParams:
        """Return a copy with ``skipInvalidInput`` updated."""
        return self._with_property("skipInvalidInput", value)

    def with_type(self, value: Literal["regexExtract"]) -> RegexExtractParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class RegexFoldParams(GenomeSpySchema):
    """Generated wrapper for ``RegexFoldParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RegexFoldParams", {})

    def __init__(
        self,
        asKey: str | UndefinedType = Undefined,
        asValue: Sequence[str] | str | UndefinedType = Undefined,
        columnRegex: Sequence[str] | str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        skipRegex: str | UndefinedType = Undefined,
        type: Literal["regexFold"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            asKey=asKey,
            asValue=asValue,
            columnRegex=columnRegex,
            description=description,
            skipRegex=skipRegex,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_asKey(self, value: str) -> RegexFoldParams:
        """Return a copy with ``asKey`` updated."""
        return self._with_property("asKey", value)

    def with_asValue(self, value: Sequence[str] | str) -> RegexFoldParams:
        """Return a copy with ``asValue`` updated."""
        return self._with_property("asValue", value)

    def with_columnRegex(self, value: Sequence[str] | str) -> RegexFoldParams:
        """Return a copy with ``columnRegex`` updated."""
        return self._with_property("columnRegex", value)

    def with_description(self, value: str) -> RegexFoldParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_skipRegex(self, value: str) -> RegexFoldParams:
        """Return a copy with ``skipRegex`` updated."""
        return self._with_property("skipRegex", value)

    def with_type(self, value: Literal["regexFold"]) -> RegexFoldParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ResolutionBehavior(GenomeSpySchema):
    """Generated wrapper for ``ResolutionBehavior``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ResolutionBehavior", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RuleConfig(GenomeSpySchema):
    """Generated wrapper for ``RuleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RuleConfig", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            minBufferSize=minBufferSize,
            minLength=minLength,
            opacity=opacity,
            size=size,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            style=style,
            tooltip=tooltip,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> RuleConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> RuleConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> RuleConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_minBufferSize(self, value: float) -> RuleConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> RuleConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> RuleConfig:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: str | Sequence[str]) -> RuleConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> RuleConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> RuleConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> RuleConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class RuleProps(GenomeSpySchema):
    """Generated wrapper for ``RuleProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RuleProps", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["rule"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            minBufferSize=minBufferSize,
            minLength=minLength,
            opacity=opacity,
            size=size,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            style=style,
            tooltip=tooltip,
            type=type,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> RuleProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> RuleProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> RuleProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_minBufferSize(self, value: float) -> RuleProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> RuleProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> RuleProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: str | Sequence[str]) -> RuleProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> RuleProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["rule"]) -> RuleProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> RuleProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> RuleProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class RulerChannelValue(GenomeSpySchema):
    """Generated wrapper for ``RulerChannelValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerChannelValue", {})

    def __init__(
        self,
        chrom: str | UndefinedType = Undefined,
        pos: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)

    def with_chrom(self, value: str) -> RulerChannelValue:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_pos(self, value: float) -> RulerChannelValue:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)


@with_property_setters
class RulerClear(GenomeSpySchema):
    """Generated wrapper for ``RulerClear``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerClear", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RulerConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerConfig", {})

    def __init__(
        self,
        clear: RulerClear_T | UndefinedType = Undefined,
        display: RulerDisplay_T | UndefinedType = Undefined,
        encodings: Sequence[PrimaryPositionalChannel_T] | UndefinedType = Undefined,
        extent: RulerExtent_T | UndefinedType = Undefined,
        mark: RulerMarkConfig | RulerMarkConfigKwds | UndefinedType = Undefined,
        on: RulerEventType_T
        | RulerEventConfig
        | RulerEventConfigKwds
        | str
        | UndefinedType = Undefined,
        snap: RulerSnap_T | UndefinedType = Undefined,
        source: RulerSource_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            clear=clear,
            display=display,
            encodings=encodings,
            extent=extent,
            mark=mark,
            on=on,
            snap=snap,
            source=source,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_clear(self, value: RulerClear_T) -> RulerConfig:
        """Return a copy with ``clear`` updated."""
        return self._with_property("clear", value)

    def with_display(self, value: RulerDisplay_T) -> RulerConfig:
        """Return a copy with ``display`` updated."""
        return self._with_property("display", value)

    def with_encodings(
        self, value: Sequence[PrimaryPositionalChannel_T]
    ) -> RulerConfig:
        """Return a copy with ``encodings`` updated."""
        return self._with_property("encodings", value)

    def with_extent(self, value: RulerExtent_T) -> RulerConfig:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_mark(
        self,
        value: RulerMarkConfig | RulerMarkConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerMarkConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_on(
        self, value: RulerEventType_T | RulerEventConfig | RulerEventConfigKwds | str
    ) -> RulerConfig:
        """Return a copy with ``on`` updated."""
        return self._with_property("on", value)

    def with_snap(self, value: RulerSnap_T) -> RulerConfig:
        """Return a copy with ``snap`` updated."""
        return self._with_property("snap", value)

    def with_source(self, value: RulerSource_T) -> RulerConfig:
        """Return a copy with ``source`` updated."""
        return self._with_property("source", value)


@with_property_setters
class RulerDisplay(GenomeSpySchema):
    """Generated wrapper for ``RulerDisplay``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerDisplay", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RulerEventConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerEventConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerEventConfig", {})

    def __init__(
        self,
        filter: str | UndefinedType = Undefined,
        type: RulerEventType_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(filter=filter, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_filter(self, value: str) -> RulerEventConfig:
        """Return a copy with ``filter`` updated."""
        return self._with_property("filter", value)

    def with_type(self, value: RulerEventType_T) -> RulerEventConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class RulerEventType(GenomeSpySchema):
    """Generated wrapper for ``RulerEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RulerExtent(GenomeSpySchema):
    """Generated wrapper for ``RulerExtent``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerExtent", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RulerInitMapping(GenomeSpySchema):
    """Generated wrapper for ``RulerInitMapping``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerInitMapping", {})

    def __init__(
        self,
        x: Scalar_T
        | ChromosomalLocus
        | dict[str, Any]
        | None
        | UndefinedType = Undefined,
        y: Scalar_T
        | ChromosomalLocus
        | dict[str, Any]
        | None
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(x=x, y=y)
        if kwds:
            self._kwds.update(kwds)

    def with_x(
        self, value: Scalar_T | ChromosomalLocus | dict[str, Any] | None
    ) -> RulerInitMapping:
        """Return a copy with ``x`` updated."""
        return self._with_property("x", value)

    def with_y(
        self, value: Scalar_T | ChromosomalLocus | dict[str, Any] | None
    ) -> RulerInitMapping:
        """Return a copy with ``y`` updated."""
        return self._with_property("y", value)


@with_property_setters
class RulerMarkConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerMarkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerMarkConfig", {})

    def __init__(
        self,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        opacity: float | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            fill=fill,
            fillOpacity=fillOpacity,
            opacity=opacity,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            stroke=stroke,
            strokeDash=strokeDash,
            strokeWidth=strokeWidth,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_fill(self, value: str) -> RulerMarkConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: float) -> RulerMarkConfig:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_opacity(self, value: float) -> RulerMarkConfig:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerMarkConfig:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerMarkConfig:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerMarkConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerMarkConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerMarkConfig:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_stroke(self, value: str) -> RulerMarkConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeDash(self, value: Sequence[float]) -> RulerMarkConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeWidth(self, value: float) -> RulerMarkConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_zindex(self, value: float) -> RulerMarkConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class RulerParameter(GenomeSpySchema):
    """Generated wrapper for ``RulerParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerParameter", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        persist: bool | UndefinedType = Undefined,
        push: Literal["outer"] | UndefinedType = Undefined,
        ruler: RulerConfig | RulerConfigKwds | UndefinedType = Undefined,
        value: RulerInitMapping | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            name=name,
            persist=persist,
            push=push,
            ruler=ruler,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> RulerParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: str) -> RulerParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: bool) -> RulerParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Literal["outer"]) -> RulerParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_ruler(
        self,
        value: RulerConfig | RulerConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerParameter:
        """Return a copy with a ``RulerConfig`` ruler."""
        return self._with_property("ruler", value, **kwargs)

    def with_value(
        self,
        value: RulerInitMapping | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerParameter:
        """Return a copy with a ``RulerInitMapping`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class RulerSnap(GenomeSpySchema):
    """Generated wrapper for ``RulerSnap``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerSnap", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class RulerSource(GenomeSpySchema):
    """Generated wrapper for ``RulerSource``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerSource", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class SampleParams(GenomeSpySchema):
    """Generated wrapper for ``SampleParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SampleParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        size: float | UndefinedType = Undefined,
        type: Literal["sample"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, size=size, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> SampleParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_size(self, value: float) -> SampleParams:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_type(self, value: Literal["sample"]) -> SampleParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Scalar(GenomeSpySchema):
    """Generated wrapper for ``Scalar``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Scalar", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ScalarDomain(GenomeSpySchema):
    """Generated wrapper for ``ScalarDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScalarDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class Scale(GenomeSpySchema):
    """Generated wrapper for ``Scale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Scale", {})

    def __init__(
        self,
        align: float | UndefinedType = Undefined,
        assembly: str
        | UrlGenomeDefinition
        | dict[str, Any]
        | InlineGenomeDefinition
        | UndefinedType = Undefined,
        base: float | UndefinedType = Undefined,
        bins: Sequence[float] | UndefinedType = Undefined,
        clamp: bool | UndefinedType = Undefined,
        constant: float | UndefinedType = Undefined,
        domain: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        domainMax: float | UndefinedType = Undefined,
        domainMid: float | UndefinedType = Undefined,
        domainMin: float | UndefinedType = Undefined,
        domainTransition: bool | dict[str, Any] | UndefinedType = Undefined,
        exponent: float | UndefinedType = Undefined,
        interpolate: ScaleInterpolate_T
        | ScaleInterpolateParams
        | ScaleInterpolateParamsKwds
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        nice: bool | float | dict[str, Any] | UndefinedType = Undefined,
        numberingOffset: float | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingInner: float | UndefinedType = Undefined,
        paddingOuter: float | UndefinedType = Undefined,
        range: Sequence[float | str | ExprRef | dict[str, Any]]
        | str
        | UndefinedType = Undefined,
        reverse: bool | UndefinedType = Undefined,
        round: bool | UndefinedType = Undefined,
        scheme: str | SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        type: ScaleType_T | UndefinedType = Undefined,
        zero: bool | UndefinedType = Undefined,
        zoom: bool | ZoomParams | ZoomParamsKwds | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            assembly=assembly,
            base=base,
            bins=bins,
            clamp=clamp,
            constant=constant,
            domain=domain,
            domainMax=domainMax,
            domainMid=domainMid,
            domainMin=domainMin,
            domainTransition=domainTransition,
            exponent=exponent,
            interpolate=interpolate,
            name=name,
            nice=nice,
            numberingOffset=numberingOffset,
            padding=padding,
            paddingInner=paddingInner,
            paddingOuter=paddingOuter,
            range=range,
            reverse=reverse,
            round=round,
            scheme=scheme,
            type=type,
            zero=zero,
            zoom=zoom,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: float) -> Scale:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_assembly(
        self, value: str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition
    ) -> Scale:
        """Return a copy with ``assembly`` updated."""
        return self._with_property("assembly", value)

    def with_base(self, value: float) -> Scale:
        """Return a copy with ``base`` updated."""
        return self._with_property("base", value)

    def with_bins(self, value: Sequence[float]) -> Scale:
        """Return a copy with ``bins`` updated."""
        return self._with_property("bins", value)

    def with_clamp(self, value: bool) -> Scale:
        """Return a copy with ``clamp`` updated."""
        return self._with_property("clamp", value)

    def with_constant(self, value: float) -> Scale:
        """Return a copy with ``constant`` updated."""
        return self._with_property("constant", value)

    def with_domain(
        self,
        value: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]],
    ) -> Scale:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainMax(self, value: float) -> Scale:
        """Return a copy with ``domainMax`` updated."""
        return self._with_property("domainMax", value)

    def with_domainMid(self, value: float) -> Scale:
        """Return a copy with ``domainMid`` updated."""
        return self._with_property("domainMid", value)

    def with_domainMin(self, value: float) -> Scale:
        """Return a copy with ``domainMin`` updated."""
        return self._with_property("domainMin", value)

    def with_domainTransition(self, value: bool | dict[str, Any]) -> Scale:
        """Return a copy with ``domainTransition`` updated."""
        return self._with_property("domainTransition", value)

    def with_exponent(self, value: float) -> Scale:
        """Return a copy with ``exponent`` updated."""
        return self._with_property("exponent", value)

    def with_interpolate(
        self,
        value: ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds,
    ) -> Scale:
        """Return a copy with ``interpolate`` updated."""
        return self._with_property("interpolate", value)

    def with_name(self, value: str) -> Scale:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_nice(self, value: bool | float | dict[str, Any]) -> Scale:
        """Return a copy with ``nice`` updated."""
        return self._with_property("nice", value)

    def with_numberingOffset(self, value: float) -> Scale:
        """Return a copy with ``numberingOffset`` updated."""
        return self._with_property("numberingOffset", value)

    def with_padding(self, value: float) -> Scale:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_paddingInner(self, value: float) -> Scale:
        """Return a copy with ``paddingInner`` updated."""
        return self._with_property("paddingInner", value)

    def with_paddingOuter(self, value: float) -> Scale:
        """Return a copy with ``paddingOuter`` updated."""
        return self._with_property("paddingOuter", value)

    def with_range(
        self, value: Sequence[float | str | ExprRef | dict[str, Any]] | str
    ) -> Scale:
        """Return a copy with ``range`` updated."""
        return self._with_property("range", value)

    def with_reverse(self, value: bool) -> Scale:
        """Return a copy with ``reverse`` updated."""
        return self._with_property("reverse", value)

    def with_round(self, value: bool) -> Scale:
        """Return a copy with ``round`` updated."""
        return self._with_property("round", value)

    def with_scheme(
        self,
        value: SchemeParams | SchemeParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``SchemeParams`` scheme."""
        return self._with_property("scheme", value, **kwargs)

    def with_type(self, value: ScaleType_T) -> Scale:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_zero(self, value: bool) -> Scale:
        """Return a copy with ``zero`` updated."""
        return self._with_property("zero", value)

    def with_zoom(
        self,
        value: ZoomParams | ZoomParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``ZoomParams`` zoom."""
        return self._with_property("zoom", value, **kwargs)


@with_property_setters
class ScaleConfig(GenomeSpySchema):
    """Generated wrapper for ``ScaleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleConfig", {})

    def __init__(
        self,
        align: float | UndefinedType = Undefined,
        assembly: str
        | UrlGenomeDefinition
        | dict[str, Any]
        | InlineGenomeDefinition
        | UndefinedType = Undefined,
        base: float | UndefinedType = Undefined,
        bins: Sequence[float] | UndefinedType = Undefined,
        clamp: bool | UndefinedType = Undefined,
        constant: float | UndefinedType = Undefined,
        domain: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        domainMax: float | UndefinedType = Undefined,
        domainMid: float | UndefinedType = Undefined,
        domainMin: float | UndefinedType = Undefined,
        domainTransition: bool | dict[str, Any] | UndefinedType = Undefined,
        exponent: float | UndefinedType = Undefined,
        index: dict[str, Any] | UndefinedType = Undefined,
        interpolate: ScaleInterpolate_T
        | ScaleInterpolateParams
        | ScaleInterpolateParamsKwds
        | UndefinedType = Undefined,
        locus: dict[str, Any] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        nice: bool | float | dict[str, Any] | UndefinedType = Undefined,
        nominal: dict[str, Any] | UndefinedType = Undefined,
        nominalColorScheme: str
        | SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        numberingOffset: float | UndefinedType = Undefined,
        ordinal: dict[str, Any] | UndefinedType = Undefined,
        ordinalColorScheme: str
        | SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingInner: float | UndefinedType = Undefined,
        paddingOuter: float | UndefinedType = Undefined,
        quantitative: dict[str, Any] | UndefinedType = Undefined,
        quantitativeColorScheme: str
        | SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        range: Sequence[float | str | ExprRef | dict[str, Any]]
        | str
        | UndefinedType = Undefined,
        reverse: bool | UndefinedType = Undefined,
        round: bool | UndefinedType = Undefined,
        scheme: str | SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        type: ScaleType_T | UndefinedType = Undefined,
        zero: bool | UndefinedType = Undefined,
        zoom: bool | ZoomParams | ZoomParamsKwds | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            assembly=assembly,
            base=base,
            bins=bins,
            clamp=clamp,
            constant=constant,
            domain=domain,
            domainMax=domainMax,
            domainMid=domainMid,
            domainMin=domainMin,
            domainTransition=domainTransition,
            exponent=exponent,
            index=index,
            interpolate=interpolate,
            locus=locus,
            name=name,
            nice=nice,
            nominal=nominal,
            nominalColorScheme=nominalColorScheme,
            numberingOffset=numberingOffset,
            ordinal=ordinal,
            ordinalColorScheme=ordinalColorScheme,
            padding=padding,
            paddingInner=paddingInner,
            paddingOuter=paddingOuter,
            quantitative=quantitative,
            quantitativeColorScheme=quantitativeColorScheme,
            range=range,
            reverse=reverse,
            round=round,
            scheme=scheme,
            type=type,
            zero=zero,
            zoom=zoom,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: float) -> ScaleConfig:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_assembly(
        self, value: str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition
    ) -> ScaleConfig:
        """Return a copy with ``assembly`` updated."""
        return self._with_property("assembly", value)

    def with_base(self, value: float) -> ScaleConfig:
        """Return a copy with ``base`` updated."""
        return self._with_property("base", value)

    def with_bins(self, value: Sequence[float]) -> ScaleConfig:
        """Return a copy with ``bins`` updated."""
        return self._with_property("bins", value)

    def with_clamp(self, value: bool) -> ScaleConfig:
        """Return a copy with ``clamp`` updated."""
        return self._with_property("clamp", value)

    def with_constant(self, value: float) -> ScaleConfig:
        """Return a copy with ``constant`` updated."""
        return self._with_property("constant", value)

    def with_domain(
        self,
        value: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]],
    ) -> ScaleConfig:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainMax(self, value: float) -> ScaleConfig:
        """Return a copy with ``domainMax`` updated."""
        return self._with_property("domainMax", value)

    def with_domainMid(self, value: float) -> ScaleConfig:
        """Return a copy with ``domainMid`` updated."""
        return self._with_property("domainMid", value)

    def with_domainMin(self, value: float) -> ScaleConfig:
        """Return a copy with ``domainMin`` updated."""
        return self._with_property("domainMin", value)

    def with_domainTransition(self, value: bool | dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``domainTransition`` updated."""
        return self._with_property("domainTransition", value)

    def with_exponent(self, value: float) -> ScaleConfig:
        """Return a copy with ``exponent`` updated."""
        return self._with_property("exponent", value)

    def with_index(self, value: dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_interpolate(
        self,
        value: ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds,
    ) -> ScaleConfig:
        """Return a copy with ``interpolate`` updated."""
        return self._with_property("interpolate", value)

    def with_locus(self, value: dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``locus`` updated."""
        return self._with_property("locus", value)

    def with_name(self, value: str) -> ScaleConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_nice(self, value: bool | float | dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``nice`` updated."""
        return self._with_property("nice", value)

    def with_nominal(self, value: dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``nominal`` updated."""
        return self._with_property("nominal", value)

    def with_nominalColorScheme(
        self, value: str | SchemeParams | SchemeParamsKwds
    ) -> ScaleConfig:
        """Return a copy with ``nominalColorScheme`` updated."""
        return self._with_property("nominalColorScheme", value)

    def with_numberingOffset(self, value: float) -> ScaleConfig:
        """Return a copy with ``numberingOffset`` updated."""
        return self._with_property("numberingOffset", value)

    def with_ordinal(self, value: dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``ordinal`` updated."""
        return self._with_property("ordinal", value)

    def with_ordinalColorScheme(
        self, value: str | SchemeParams | SchemeParamsKwds
    ) -> ScaleConfig:
        """Return a copy with ``ordinalColorScheme`` updated."""
        return self._with_property("ordinalColorScheme", value)

    def with_padding(self, value: float) -> ScaleConfig:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_paddingInner(self, value: float) -> ScaleConfig:
        """Return a copy with ``paddingInner`` updated."""
        return self._with_property("paddingInner", value)

    def with_paddingOuter(self, value: float) -> ScaleConfig:
        """Return a copy with ``paddingOuter`` updated."""
        return self._with_property("paddingOuter", value)

    def with_quantitative(self, value: dict[str, Any]) -> ScaleConfig:
        """Return a copy with ``quantitative`` updated."""
        return self._with_property("quantitative", value)

    def with_quantitativeColorScheme(
        self, value: str | SchemeParams | SchemeParamsKwds
    ) -> ScaleConfig:
        """Return a copy with ``quantitativeColorScheme`` updated."""
        return self._with_property("quantitativeColorScheme", value)

    def with_range(
        self, value: Sequence[float | str | ExprRef | dict[str, Any]] | str
    ) -> ScaleConfig:
        """Return a copy with ``range`` updated."""
        return self._with_property("range", value)

    def with_reverse(self, value: bool) -> ScaleConfig:
        """Return a copy with ``reverse`` updated."""
        return self._with_property("reverse", value)

    def with_round(self, value: bool) -> ScaleConfig:
        """Return a copy with ``round`` updated."""
        return self._with_property("round", value)

    def with_scheme(
        self,
        value: SchemeParams | SchemeParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``SchemeParams`` scheme."""
        return self._with_property("scheme", value, **kwargs)

    def with_type(self, value: ScaleType_T) -> ScaleConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_zero(self, value: bool) -> ScaleConfig:
        """Return a copy with ``zero`` updated."""
        return self._with_property("zero", value)

    def with_zoom(
        self,
        value: ZoomParams | ZoomParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ZoomParams`` zoom."""
        return self._with_property("zoom", value, **kwargs)


@with_property_setters
class ScaleInterpolate(GenomeSpySchema):
    """Generated wrapper for ``ScaleInterpolate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleInterpolate", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class ScaleInterpolateParams(GenomeSpySchema):
    """Generated wrapper for ``ScaleInterpolateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleInterpolateParams", {})

    def __init__(
        self,
        gamma: float | UndefinedType = Undefined,
        type: Literal["rgb", "cubehelix", "cubehelix-long"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(gamma=gamma, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_gamma(self, value: float) -> ScaleInterpolateParams:
        """Return a copy with ``gamma`` updated."""
        return self._with_property("gamma", value)

    def with_type(
        self, value: Literal["rgb", "cubehelix", "cubehelix-long"]
    ) -> ScaleInterpolateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class ScaleType(GenomeSpySchema):
    """Generated wrapper for ``ScaleType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class SchemeParams(GenomeSpySchema):
    """Generated wrapper for ``SchemeParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SchemeParams", {})

    def __init__(
        self,
        count: float | UndefinedType = Undefined,
        extent: Sequence[float] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(count=count, extent=extent, name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_count(self, value: float) -> SchemeParams:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_extent(self, value: Sequence[float]) -> SchemeParams:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_name(self, value: str) -> SchemeParams:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


@with_property_setters
class SearchDef(GenomeSpySchema):
    """Generated wrapper for ``SearchDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SearchDef", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> SearchDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: str) -> SearchDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: str | None) -> SearchDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


@with_property_setters
class SecondaryChromPosDef(GenomeSpySchema):
    """Generated wrapper for ``SecondaryChromPosDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SecondaryChromPosDef", {})

    def __init__(
        self,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        chrom: FieldName_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        pos: FieldName_T | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axis=axis,
            band=band,
            chrom=chrom,
            description=description,
            domainInert=domainInert,
            offset=offset,
            pos=pos,
            title=title,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SecondaryChromPosDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: float) -> SecondaryChromPosDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(self, value: FieldName_T) -> SecondaryChromPosDef:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_description(self, value: str) -> SecondaryChromPosDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> SecondaryChromPosDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_offset(self, value: float) -> SecondaryChromPosDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(self, value: FieldName_T) -> SecondaryChromPosDef:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_title(self, value: str | None) -> SecondaryChromPosDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


@with_property_setters
class SecondaryPositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``SecondaryPositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SecondaryPositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class SelectionDomainRef(GenomeSpySchema):
    """Generated wrapper for ``SelectionDomainRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionDomainRef", {})

    def __init__(
        self,
        encoding: Literal["x", "y"] | UndefinedType = Undefined,
        initial: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(encoding=encoding, initial=initial, param=param)
        if kwds:
            self._kwds.update(kwds)

    def with_encoding(self, value: Literal["x", "y"]) -> SelectionDomainRef:
        """Return a copy with ``encoding`` updated."""
        return self._with_property("encoding", value)

    def with_initial(
        self, value: ScalarDomain_T | Sequence[ChromosomalLocus | dict[str, Any]]
    ) -> SelectionDomainRef:
        """Return a copy with ``initial`` updated."""
        return self._with_property("initial", value)

    def with_param(self, value: str) -> SelectionDomainRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)


@with_property_setters
class SelectionExtent(GenomeSpySchema):
    """Generated wrapper for ``SelectionExtent``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionExtent", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class SelectionFilterParams(GenomeSpySchema):
    """Generated wrapper for ``SelectionFilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionFilterParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        fields: dict[str, Any] | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        type: Literal["filter"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, fields=fields, param=param, type=type
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> SelectionFilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: bool) -> SelectionFilterParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_fields(self, value: dict[str, Any]) -> SelectionFilterParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_param(self, value: str) -> SelectionFilterParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_type(self, value: Literal["filter"]) -> SelectionFilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class SelectionInitIntervalMapping(GenomeSpySchema):
    """Generated wrapper for ``SelectionInitIntervalMapping``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "SelectionInitIntervalMapping", {}
    )

    def __init__(
        self,
        x: Sequence[float] | UndefinedType = Undefined,
        y: Sequence[float] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(x=x, y=y)
        if kwds:
            self._kwds.update(kwds)

    def with_x(self, value: Sequence[float]) -> SelectionInitIntervalMapping:
        """Return a copy with ``x`` updated."""
        return self._with_property("x", value)

    def with_y(self, value: Sequence[float]) -> SelectionInitIntervalMapping:
        """Return a copy with ``y`` updated."""
        return self._with_property("y", value)


@with_property_setters
class SelectionParameter(GenomeSpySchema):
    """Generated wrapper for ``SelectionParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionParameter", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        persist: bool | UndefinedType = Undefined,
        push: Literal["outer"] | UndefinedType = Undefined,
        select: SelectionType_T
        | PointSelectionConfig
        | dict[str, Any]
        | IntervalSelectionConfig
        | UndefinedType = Undefined,
        value: SelectionInitIntervalMapping
        | dict[str, Any]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            name=name,
            persist=persist,
            push=push,
            select=select,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> SelectionParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: str) -> SelectionParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: bool) -> SelectionParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Literal["outer"]) -> SelectionParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_select(
        self,
        value: SelectionType_T
        | PointSelectionConfig
        | dict[str, Any]
        | IntervalSelectionConfig,
    ) -> SelectionParameter:
        """Return a copy with ``select`` updated."""
        return self._with_property("select", value)

    def with_value(
        self,
        value: SelectionInitIntervalMapping | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SelectionParameter:
        """Return a copy with a ``SelectionInitIntervalMapping`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class SelectionType(GenomeSpySchema):
    """Generated wrapper for ``SelectionType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class SeparatorProps(GenomeSpySchema):
    """Generated wrapper for ``SeparatorProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SeparatorProps", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        includePlotMargin: bool | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["rule"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            includePlotMargin=includePlotMargin,
            minBufferSize=minBufferSize,
            minLength=minLength,
            opacity=opacity,
            size=size,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            style=style,
            tooltip=tooltip,
            type=type,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> SeparatorProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> SeparatorProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> SeparatorProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_includePlotMargin(self, value: bool) -> SeparatorProps:
        """Return a copy with ``includePlotMargin`` updated."""
        return self._with_property("includePlotMargin", value)

    def with_minBufferSize(self, value: float) -> SeparatorProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> SeparatorProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> SeparatorProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: str | Sequence[str]) -> SeparatorProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> SeparatorProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["rule"]) -> SeparatorProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> SeparatorProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> SeparatorProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)

    def with_zindex(self, value: float) -> SeparatorProps:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class SequenceGenerator(GenomeSpySchema):
    """Generated wrapper for ``SequenceGenerator``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SequenceGenerator", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        sequence: SequenceParams | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, name=name, sequence=sequence)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> SequenceGenerator:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: str) -> SequenceGenerator:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_sequence(
        self,
        value: SequenceParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SequenceGenerator:
        """Return a copy with a ``SequenceParams`` sequence."""
        return self._with_property("sequence", value, **kwargs)


@with_property_setters
class SequenceParams(GenomeSpySchema):
    """Generated wrapper for ``SequenceParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SequenceParams", {})

    def __init__(
        self,
        start: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        step: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stop: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(start=start, step=step, stop=stop)
        if kwds:
            self._kwds.update(kwds)

    def with_start(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SequenceParams:
        """Return a copy with a ``ExprRef`` start."""
        return self._with_property("start", value, **kwargs)

    def with_step(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SequenceParams:
        """Return a copy with a ``ExprRef`` step."""
        return self._with_property("step", value, **kwargs)

    def with_stop(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SequenceParams:
        """Return a copy with a ``ExprRef`` stop."""
        return self._with_property("stop", value, **kwargs)


@with_property_setters
class ShapeDef(GenomeSpySchema):
    """Generated wrapper for ``ShapeDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ShapeDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        condition: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        legend: Legend | LegendKwds | None | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            condition=condition,
            datum=datum,
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            legend=legend,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> ShapeDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> ShapeDef:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> ShapeDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> ShapeDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ShapeDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> ShapeDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> ShapeDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | LegendKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> ShapeDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> ShapeDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> ShapeDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class SingleUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``SingleUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SingleUrlSourceRef", {})

    def __init__(
        self,
        attach: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: FieldName_T | UndefinedType = Undefined,
        maxValues: float | UndefinedType = Undefined,
        onLoadError: Literal["error", "skip"] | UndefinedType = Undefined,
        template: str | UndefinedType = Undefined,
        values: Sequence[Scalar_T]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            attach=attach,
            expr=expr,
            field=field,
            maxValues=maxValues,
            onLoadError=onLoadError,
            template=template,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_attach(self, value: bool) -> SingleUrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: str) -> SingleUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: FieldName_T) -> SingleUrlSourceRef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_maxValues(self, value: float) -> SingleUrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Literal["error", "skip"]) -> SingleUrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: str) -> SingleUrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)

    def with_values(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SingleUrlSourceRef:
        """Return a copy with a ``ExprRef`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class SizeDef(GenomeSpySchema):
    """Generated wrapper for ``SizeDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SizeDef", {})

    def __init__(
        self,
        grow: float | UndefinedType = Undefined,
        maxPx: float | UndefinedType = Undefined,
        minPx: float | UndefinedType = Undefined,
        px: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(grow=grow, maxPx=maxPx, minPx=minPx, px=px)
        if kwds:
            self._kwds.update(kwds)

    def with_grow(self, value: float) -> SizeDef:
        """Return a copy with ``grow`` updated."""
        return self._with_property("grow", value)

    def with_maxPx(self, value: float) -> SizeDef:
        """Return a copy with ``maxPx`` updated."""
        return self._with_property("maxPx", value)

    def with_minPx(self, value: float) -> SizeDef:
        """Return a copy with ``minPx`` updated."""
        return self._with_property("minPx", value)

    def with_px(self, value: float) -> SizeDef:
        """Return a copy with ``px`` updated."""
        return self._with_property("px", value)


@with_property_setters
class SortOrder(GenomeSpySchema):
    """Generated wrapper for ``SortOrder``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SortOrder", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class StackParams(GenomeSpySchema):
    """Generated wrapper for ``StackParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StackParams", {})

    def __init__(
        self,
        baseField: Field_T | UndefinedType = Undefined,
        cardinality: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        offset: Literal["zero", "center", "normalize", "information"]
        | UndefinedType = Undefined,
        sort: CompareParams | CompareParamsKwds | UndefinedType = Undefined,
        type: Literal["stack"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            baseField=baseField,
            cardinality=cardinality,
            description=description,
            field=field,
            groupby=groupby,
            offset=offset,
            sort=sort,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_baseField(self, value: Field_T) -> StackParams:
        """Return a copy with ``baseField`` updated."""
        return self._with_property("baseField", value)

    def with_cardinality(self, value: float) -> StackParams:
        """Return a copy with ``cardinality`` updated."""
        return self._with_property("cardinality", value)

    def with_description(self, value: str) -> StackParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Field_T) -> StackParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_groupby(self, value: Sequence[Field_T]) -> StackParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_offset(
        self, value: Literal["zero", "center", "normalize", "information"]
    ) -> StackParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_sort(
        self,
        value: CompareParams | CompareParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StackParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_type(self, value: Literal["stack"]) -> StackParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Step(GenomeSpySchema):
    """Generated wrapper for ``Step``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Step", {})

    def __init__(self, step: float | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(step=step)
        if kwds:
            self._kwds.update(kwds)

    def with_step(self, value: float) -> Step:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


@with_property_setters
class StringDatumDef(GenomeSpySchema):
    """Generated wrapper for ``StringDatumDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StringDatumDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            datum=datum,
            description=description,
            format=format,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> StringDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> StringDatumDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> StringDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(self, value: str) -> StringDatumDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> StringDatumDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> StringDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> StringDatumDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class StringFieldDef(GenomeSpySchema):
    """Generated wrapper for ``StringFieldDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StringFieldDef", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            domainInert=domainInert,
            field=field,
            format=format,
            title=title,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> StringFieldDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> StringFieldDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: str) -> StringFieldDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> StringFieldDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_title(self, value: str | None) -> StringFieldDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> StringFieldDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class StyleConfig(GenomeSpySchema):
    """Generated wrapper for ``StyleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StyleConfig", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        anchor: TitleAnchor_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        chromGrid: bool | UndefinedType = Undefined,
        chromGridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        chromGridColor: str | UndefinedType = Undefined,
        chromGridDash: Sequence[float] | UndefinedType = Undefined,
        chromGridDashOffset: float | UndefinedType = Undefined,
        chromGridFillEven: str | UndefinedType = Undefined,
        chromGridFillOdd: str | UndefinedType = Undefined,
        chromGridOpacity: float | UndefinedType = Undefined,
        chromGridWidth: float | UndefinedType = Undefined,
        chromLabelAlign: Align_T | UndefinedType = Undefined,
        chromLabelColor: str | UndefinedType = Undefined,
        chromLabelFont: str | UndefinedType = Undefined,
        chromLabelFontSize: float | UndefinedType = Undefined,
        chromLabelFontStyle: FontStyle_T | UndefinedType = Undefined,
        chromLabelFontWeight: FontWeight_T | UndefinedType = Undefined,
        chromLabelPadding: float | UndefinedType = Undefined,
        chromLabels: bool | UndefinedType = Undefined,
        chromTickColor: str | UndefinedType = Undefined,
        chromTickDash: Sequence[float] | UndefinedType = Undefined,
        chromTickDashOffset: float | UndefinedType = Undefined,
        chromTickSize: float | UndefinedType = Undefined,
        chromTickWidth: float | UndefinedType = Undefined,
        chromTicks: bool | UndefinedType = Undefined,
        clampApex: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        cornerRadius: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        disable: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        domain: bool | UndefinedType = Undefined,
        domainCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        domainColor: str | UndefinedType = Undefined,
        domainDash: Sequence[float] | UndefinedType = Undefined,
        domainDashOffset: float | UndefinedType = Undefined,
        domainWidth: float | UndefinedType = Undefined,
        dx: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        fitToBand: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        frame: TitleFrame_T | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        grid: bool | UndefinedType = Undefined,
        gridCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        gridColor: str | UndefinedType = Undefined,
        gridDash: Sequence[float] | UndefinedType = Undefined,
        gridDashOffset: float | UndefinedType = Undefined,
        gridOpacity: float | UndefinedType = Undefined,
        gridWidth: float | UndefinedType = Undefined,
        hatch: Literal["none"]
        | Literal["diagonal"]
        | Literal["antiDiagonal"]
        | Literal["cross"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | Literal["grid"]
        | Literal["dots"]
        | Literal["rings"]
        | Literal["ringsLarge"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        inwardStroke: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelAngle: float | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        logoLetters: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        maxChordLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minArcHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        minHeight: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minPickingSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical", "horizontal"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | ExprRef
        | dict[str, Any]
        | AxisOrient_T
        | TitleOrient_T
        | LegendOrient_T
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        reserve: bool | UndefinedType = Undefined,
        rowPadding: float | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        segments: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticScore: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        semanticZoomFraction: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shape: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        squeeze: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        strokeOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeWidth: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        subtitle: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFont: str | UndefinedType = Undefined,
        subtitleFontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFontStyle: FontStyle_T | UndefinedType = Undefined,
        subtitleFontWeight: FontWeight_T | UndefinedType = Undefined,
        subtitlePadding: float | UndefinedType = Undefined,
        symbolBaseFillColor: str | UndefinedType = Undefined,
        symbolBaseStrokeColor: str | UndefinedType = Undefined,
        symbolOffset: float | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolStrokeWidth: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        text: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tickDash: Sequence[float] | UndefinedType = Undefined,
        tickDashOffset: float | UndefinedType = Undefined,
        tickMinStep: float | UndefinedType = Undefined,
        tickSize: float | UndefinedType = Undefined,
        tickWidth: float | UndefinedType = Undefined,
        ticks: bool | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleColor: str | UndefinedType = Undefined,
        titleFit: Literal["point", "range"] | UndefinedType = Undefined,
        titleFont: str | UndefinedType = Undefined,
        titleFontSize: float | UndefinedType = Undefined,
        titleFontStyle: FontStyle_T | UndefinedType = Undefined,
        titleFontWeight: FontWeight_T | UndefinedType = Undefined,
        titleLimit: float | UndefinedType = Undefined,
        titleOpacity: float | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        titlePadding: float | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        values: Sequence[Any]
        | Sequence[str | float | bool]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            anchor=anchor,
            angle=angle,
            arcFadingDistance=arcFadingDistance,
            arcHeightFactor=arcHeightFactor,
            backgroundFill=backgroundFill,
            backgroundFillOpacity=backgroundFillOpacity,
            backgroundStroke=backgroundStroke,
            backgroundStrokeOpacity=backgroundStrokeOpacity,
            backgroundStrokeWidth=backgroundStrokeWidth,
            baseline=baseline,
            buildIndex=buildIndex,
            chromGrid=chromGrid,
            chromGridCap=chromGridCap,
            chromGridColor=chromGridColor,
            chromGridDash=chromGridDash,
            chromGridDashOffset=chromGridDashOffset,
            chromGridFillEven=chromGridFillEven,
            chromGridFillOdd=chromGridFillOdd,
            chromGridOpacity=chromGridOpacity,
            chromGridWidth=chromGridWidth,
            chromLabelAlign=chromLabelAlign,
            chromLabelColor=chromLabelColor,
            chromLabelFont=chromLabelFont,
            chromLabelFontSize=chromLabelFontSize,
            chromLabelFontStyle=chromLabelFontStyle,
            chromLabelFontWeight=chromLabelFontWeight,
            chromLabelPadding=chromLabelPadding,
            chromLabels=chromLabels,
            chromTickColor=chromTickColor,
            chromTickDash=chromTickDash,
            chromTickDashOffset=chromTickDashOffset,
            chromTickSize=chromTickSize,
            chromTickWidth=chromTickWidth,
            chromTicks=chromTicks,
            clampApex=clampApex,
            clip=clip,
            color=color,
            columnPadding=columnPadding,
            columns=columns,
            cornerRadius=cornerRadius,
            cornerRadiusBottomLeft=cornerRadiusBottomLeft,
            cornerRadiusBottomRight=cornerRadiusBottomRight,
            cornerRadiusTopLeft=cornerRadiusTopLeft,
            cornerRadiusTopRight=cornerRadiusTopRight,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            direction=direction,
            disable=disable,
            domain=domain,
            domainCap=domainCap,
            domainColor=domainColor,
            domainDash=domainDash,
            domainDashOffset=domainDashOffset,
            domainWidth=domainWidth,
            dx=dx,
            dy=dy,
            fill=fill,
            fillGradientStrength=fillGradientStrength,
            fillOpacity=fillOpacity,
            filled=filled,
            fitToBand=fitToBand,
            flushX=flushX,
            flushY=flushY,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            format=format,
            frame=frame,
            geometricZoomBound=geometricZoomBound,
            grid=grid,
            gridCap=gridCap,
            gridColor=gridColor,
            gridDash=gridDash,
            gridDashOffset=gridDashOffset,
            gridOpacity=gridOpacity,
            gridWidth=gridWidth,
            hatch=hatch,
            inwardStroke=inwardStroke,
            labelAlign=labelAlign,
            labelAngle=labelAngle,
            labelBaseline=labelBaseline,
            labelColor=labelColor,
            labelFont=labelFont,
            labelFontSize=labelFontSize,
            labelFontStyle=labelFontStyle,
            labelFontWeight=labelFontWeight,
            labelLimit=labelLimit,
            labelOffset=labelOffset,
            labelPadding=labelPadding,
            labels=labels,
            linkShape=linkShape,
            logoLetters=logoLetters,
            maxChordLength=maxChordLength,
            maxExtent=maxExtent,
            minArcHeight=minArcHeight,
            minBufferSize=minBufferSize,
            minExtent=minExtent,
            minHeight=minHeight,
            minLength=minLength,
            minOpacity=minOpacity,
            minPickingSize=minPickingSize,
            minWidth=minWidth,
            noFadingOnPointSelection=noFadingOnPointSelection,
            offset=offset,
            opacity=opacity,
            orient=orient,
            padding=padding,
            paddingX=paddingX,
            paddingY=paddingY,
            placement=placement,
            reserve=reserve,
            rowPadding=rowPadding,
            sampleFacetPadding=sampleFacetPadding,
            segments=segments,
            semanticScore=semanticScore,
            semanticZoomFraction=semanticZoomFraction,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            shape=shape,
            size=size,
            spacing=spacing,
            squeeze=squeeze,
            stroke=stroke,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            style=style,
            subtitle=subtitle,
            subtitleColor=subtitleColor,
            subtitleFont=subtitleFont,
            subtitleFontSize=subtitleFontSize,
            subtitleFontStyle=subtitleFontStyle,
            subtitleFontWeight=subtitleFontWeight,
            subtitlePadding=subtitlePadding,
            symbolBaseFillColor=symbolBaseFillColor,
            symbolBaseStrokeColor=symbolBaseStrokeColor,
            symbolOffset=symbolOffset,
            symbolSize=symbolSize,
            symbolStrokeWidth=symbolStrokeWidth,
            symbolType=symbolType,
            text=text,
            thickness=thickness,
            tickCap=tickCap,
            tickColor=tickColor,
            tickCount=tickCount,
            tickDash=tickDash,
            tickDashOffset=tickDashOffset,
            tickMinStep=tickMinStep,
            tickSize=tickSize,
            tickWidth=tickWidth,
            ticks=ticks,
            title=title,
            titleColor=titleColor,
            titleFit=titleFit,
            titleFont=titleFont,
            titleFontSize=titleFontSize,
            titleFontStyle=titleFontStyle,
            titleFontWeight=titleFontWeight,
            titleLimit=titleLimit,
            titleOpacity=titleOpacity,
            titleOrient=titleOrient,
            titlePadding=titlePadding,
            tooltip=tooltip,
            values=values,
            viewportEdgeFadeDistanceBottom=viewportEdgeFadeDistanceBottom,
            viewportEdgeFadeDistanceLeft=viewportEdgeFadeDistanceLeft,
            viewportEdgeFadeDistanceRight=viewportEdgeFadeDistanceRight,
            viewportEdgeFadeDistanceTop=viewportEdgeFadeDistanceTop,
            viewportEdgeFadeWidthBottom=viewportEdgeFadeWidthBottom,
            viewportEdgeFadeWidthLeft=viewportEdgeFadeWidthLeft,
            viewportEdgeFadeWidthRight=viewportEdgeFadeWidthRight,
            viewportEdgeFadeWidthTop=viewportEdgeFadeWidthTop,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> StyleConfig:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_anchor(self, value: TitleAnchor_T) -> StyleConfig:
        """Return a copy with ``anchor`` updated."""
        return self._with_property("anchor", value)

    def with_angle(self, value: float | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``angle`` updated."""
        return self._with_property("angle", value)

    def with_arcFadingDistance(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` arcFadingDistance."""
        return self._with_property("arcFadingDistance", value, **kwargs)

    def with_arcHeightFactor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` arcHeightFactor."""
        return self._with_property("arcHeightFactor", value, **kwargs)

    def with_backgroundFill(self, value: str) -> StyleConfig:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: float) -> StyleConfig:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: str) -> StyleConfig:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: float) -> StyleConfig:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_baseline(self, value: Baseline_T) -> StyleConfig:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_buildIndex(self, value: bool) -> StyleConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_chromGrid(self, value: bool) -> StyleConfig:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(
        self, value: Literal["butt", "round", "square"]
    ) -> StyleConfig:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: str) -> StyleConfig:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: str) -> StyleConfig:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: str) -> StyleConfig:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: float) -> StyleConfig:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(self, value: Align_T) -> StyleConfig:
        """Return a copy with ``chromLabelAlign`` updated."""
        return self._with_property("chromLabelAlign", value)

    def with_chromLabelColor(self, value: str) -> StyleConfig:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: str) -> StyleConfig:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: float) -> StyleConfig:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(self, value: FontStyle_T) -> StyleConfig:
        """Return a copy with ``chromLabelFontStyle`` updated."""
        return self._with_property("chromLabelFontStyle", value)

    def with_chromLabelFontWeight(self, value: FontWeight_T) -> StyleConfig:
        """Return a copy with ``chromLabelFontWeight`` updated."""
        return self._with_property("chromLabelFontWeight", value)

    def with_chromLabelPadding(self, value: float) -> StyleConfig:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: bool) -> StyleConfig:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: str) -> StyleConfig:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: float) -> StyleConfig:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: bool) -> StyleConfig:
        """Return a copy with ``chromTicks`` updated."""
        return self._with_property("chromTicks", value)

    def with_clampApex(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` clampApex."""
        return self._with_property("clampApex", value, **kwargs)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> StyleConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(self, value: str | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``color`` updated."""
        return self._with_property("color", value)

    def with_columnPadding(self, value: float) -> StyleConfig:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: float) -> StyleConfig:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_cornerRadius(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cornerRadius."""
        return self._with_property("cornerRadius", value, **kwargs)

    def with_cornerRadiusBottomLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomLeft."""
        return self._with_property("cornerRadiusBottomLeft", value, **kwargs)

    def with_cornerRadiusBottomRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusBottomRight."""
        return self._with_property("cornerRadiusBottomRight", value, **kwargs)

    def with_cornerRadiusTopLeft(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusTopLeft."""
        return self._with_property("cornerRadiusTopLeft", value, **kwargs)

    def with_cornerRadiusTopRight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cornerRadiusTopRight."""
        return self._with_property("cornerRadiusTopRight", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> StyleConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_direction(self, value: LegendDirection_T) -> StyleConfig:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_disable(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` disable."""
        return self._with_property("disable", value, **kwargs)

    def with_domain(self, value: bool) -> StyleConfig:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Literal["butt", "round", "square"]) -> StyleConfig:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: str) -> StyleConfig:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_dx(self, value: float | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: float | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_fill(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillGradientStrength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` fillGradientStrength."""
        return self._with_property("fillGradientStrength", value, **kwargs)

    def with_fillOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_filled(self, value: bool) -> StyleConfig:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_fitToBand(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` fitToBand."""
        return self._with_property("fitToBand", value, **kwargs)

    def with_flushX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` flushX."""
        return self._with_property("flushX", value, **kwargs)

    def with_flushY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` flushY."""
        return self._with_property("flushY", value, **kwargs)

    def with_font(self, value: str) -> StyleConfig:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` fontSize."""
        return self._with_property("fontSize", value, **kwargs)

    def with_fontStyle(self, value: FontStyle_T) -> StyleConfig:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> StyleConfig:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_format(self, value: str) -> StyleConfig:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_frame(self, value: TitleFrame_T) -> StyleConfig:
        """Return a copy with ``frame`` updated."""
        return self._with_property("frame", value)

    def with_geometricZoomBound(self, value: float) -> StyleConfig:
        """Return a copy with ``geometricZoomBound`` updated."""
        return self._with_property("geometricZoomBound", value)

    def with_grid(self, value: bool) -> StyleConfig:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Literal["butt", "round", "square"]) -> StyleConfig:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: str) -> StyleConfig:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: float) -> StyleConfig:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_hatch(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` hatch."""
        return self._with_property("hatch", value, **kwargs)

    def with_inwardStroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` inwardStroke."""
        return self._with_property("inwardStroke", value, **kwargs)

    def with_labelAlign(self, value: Align_T) -> StyleConfig:
        """Return a copy with ``labelAlign`` updated."""
        return self._with_property("labelAlign", value)

    def with_labelAngle(self, value: float) -> StyleConfig:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(self, value: Baseline_T) -> StyleConfig:
        """Return a copy with ``labelBaseline`` updated."""
        return self._with_property("labelBaseline", value)

    def with_labelColor(self, value: str) -> StyleConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: str) -> StyleConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: float) -> StyleConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(self, value: FontStyle_T) -> StyleConfig:
        """Return a copy with ``labelFontStyle`` updated."""
        return self._with_property("labelFontStyle", value)

    def with_labelFontWeight(self, value: FontWeight_T) -> StyleConfig:
        """Return a copy with ``labelFontWeight`` updated."""
        return self._with_property("labelFontWeight", value)

    def with_labelLimit(self, value: float) -> StyleConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelPadding(self, value: float) -> StyleConfig:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: bool) -> StyleConfig:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_linkShape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` linkShape."""
        return self._with_property("linkShape", value, **kwargs)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_maxChordLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` maxChordLength."""
        return self._with_property("maxChordLength", value, **kwargs)

    def with_maxExtent(self, value: float) -> StyleConfig:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minArcHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minArcHeight."""
        return self._with_property("minArcHeight", value, **kwargs)

    def with_minBufferSize(self, value: float) -> StyleConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minExtent(self, value: float) -> StyleConfig:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_minHeight(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minHeight."""
        return self._with_property("minHeight", value, **kwargs)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_minOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minOpacity."""
        return self._with_property("minOpacity", value, **kwargs)

    def with_minPickingSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minPickingSize."""
        return self._with_property("minPickingSize", value, **kwargs)

    def with_minWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` minWidth."""
        return self._with_property("minWidth", value, **kwargs)

    def with_noFadingOnPointSelection(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` noFadingOnPointSelection."""
        return self._with_property("noFadingOnPointSelection", value, **kwargs)

    def with_offset(self, value: float) -> StyleConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(
        self,
        value: Literal["vertical", "horizontal"]
        | Literal["vertical"]
        | Literal["horizontal"]
        | ExprRef
        | dict[str, Any]
        | AxisOrient_T
        | TitleOrient_T
        | LegendOrient_T,
    ) -> StyleConfig:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_padding(self, value: float) -> StyleConfig:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_paddingX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` paddingX."""
        return self._with_property("paddingX", value, **kwargs)

    def with_paddingY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` paddingY."""
        return self._with_property("paddingY", value, **kwargs)

    def with_placement(self, value: AxisPlacement_T) -> StyleConfig:
        """Return a copy with ``placement`` updated."""
        return self._with_property("placement", value)

    def with_reserve(self, value: bool) -> StyleConfig:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_rowPadding(self, value: float) -> StyleConfig:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_sampleFacetPadding(self, value: float) -> StyleConfig:
        """Return a copy with ``sampleFacetPadding`` updated."""
        return self._with_property("sampleFacetPadding", value)

    def with_segments(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` segments."""
        return self._with_property("segments", value, **kwargs)

    def with_semanticScore(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` semanticScore."""
        return self._with_property("semanticScore", value, **kwargs)

    def with_semanticZoomFraction(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` semanticZoomFraction."""
        return self._with_property("semanticZoomFraction", value, **kwargs)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_shape(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` shape."""
        return self._with_property("shape", value, **kwargs)

    def with_size(self, value: float | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_spacing(self, value: float) -> StyleConfig:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_squeeze(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` squeeze."""
        return self._with_property("squeeze", value, **kwargs)

    def with_stroke(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_strokeOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_style(self, value: str | Sequence[str] | None) -> StyleConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_subtitle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` subtitle."""
        return self._with_property("subtitle", value, **kwargs)

    def with_subtitleColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` subtitleColor."""
        return self._with_property("subtitleColor", value, **kwargs)

    def with_subtitleFont(self, value: str) -> StyleConfig:
        """Return a copy with ``subtitleFont`` updated."""
        return self._with_property("subtitleFont", value)

    def with_subtitleFontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` subtitleFontSize."""
        return self._with_property("subtitleFontSize", value, **kwargs)

    def with_subtitleFontStyle(self, value: FontStyle_T) -> StyleConfig:
        """Return a copy with ``subtitleFontStyle`` updated."""
        return self._with_property("subtitleFontStyle", value)

    def with_subtitleFontWeight(self, value: FontWeight_T) -> StyleConfig:
        """Return a copy with ``subtitleFontWeight`` updated."""
        return self._with_property("subtitleFontWeight", value)

    def with_subtitlePadding(self, value: float) -> StyleConfig:
        """Return a copy with ``subtitlePadding`` updated."""
        return self._with_property("subtitlePadding", value)

    def with_symbolBaseFillColor(self, value: str) -> StyleConfig:
        """Return a copy with ``symbolBaseFillColor`` updated."""
        return self._with_property("symbolBaseFillColor", value)

    def with_symbolBaseStrokeColor(self, value: str) -> StyleConfig:
        """Return a copy with ``symbolBaseStrokeColor`` updated."""
        return self._with_property("symbolBaseStrokeColor", value)

    def with_symbolOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: float) -> StyleConfig:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_symbolType(self, value: str) -> StyleConfig:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_text(self, value: Scalar_T | ExprRef | dict[str, Any]) -> StyleConfig:
        """Return a copy with ``text`` updated."""
        return self._with_property("text", value)

    def with_thickness(self, value: float) -> StyleConfig:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tickCap(self, value: Literal["butt", "round", "square"]) -> StyleConfig:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: str) -> StyleConfig:
        """Return a copy with ``tickColor`` updated."""
        return self._with_property("tickColor", value)

    def with_tickCount(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` tickCount."""
        return self._with_property("tickCount", value, **kwargs)

    def with_tickDash(self, value: Sequence[float]) -> StyleConfig:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: float) -> StyleConfig:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: float) -> StyleConfig:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: float) -> StyleConfig:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: bool) -> StyleConfig:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: str | None) -> StyleConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: str) -> StyleConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Literal["point", "range"]) -> StyleConfig:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: str) -> StyleConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: float) -> StyleConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(self, value: FontStyle_T) -> StyleConfig:
        """Return a copy with ``titleFontStyle`` updated."""
        return self._with_property("titleFontStyle", value)

    def with_titleFontWeight(self, value: FontWeight_T) -> StyleConfig:
        """Return a copy with ``titleFontWeight`` updated."""
        return self._with_property("titleFontWeight", value)

    def with_titleLimit(self, value: float) -> StyleConfig:
        """Return a copy with ``titleLimit`` updated."""
        return self._with_property("titleLimit", value)

    def with_titleOpacity(self, value: float) -> StyleConfig:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titleOrient(self, value: LegendTitleOrient_T) -> StyleConfig:
        """Return a copy with ``titleOrient`` updated."""
        return self._with_property("titleOrient", value)

    def with_titlePadding(self, value: float) -> StyleConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> StyleConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_values(
        self, value: Sequence[Any] | Sequence[str | float | bool]
    ) -> StyleConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: float) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthTop`` updated."""
        return self._with_property("viewportEdgeFadeWidthTop", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> StyleConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)

    def with_zindex(self, value: float) -> StyleConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class TabixTsvData(GenomeSpySchema):
    """Generated wrapper for ``TabixTsvData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TabixTsvData", {})

    def __init__(
        self,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        columns: Sequence[str] | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        parse: Parse | ParseKwds | None | UndefinedType = Undefined,
        type: Literal["tabix"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            addChrPrefix=addChrPrefix,
            channel=channel,
            columns=columns,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            indexUrl=indexUrl,
            parse=parse,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_addChrPrefix(self, value: bool | str) -> TabixTsvData:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> TabixTsvData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_columns(self, value: Sequence[str]) -> TabixTsvData:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> TabixTsvData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> TabixTsvData:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_parse(
        self,
        value: Parse | ParseKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Literal["tabix"]) -> TabixTsvData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> TabixTsvData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(self, value: float) -> TabixTsvData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class TemplateImport(GenomeSpySchema):
    """Generated wrapper for ``TemplateImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TemplateImport", {})

    def __init__(self, template: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_template(self, value: str) -> TemplateImport:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


@with_property_setters
class TextConfig(GenomeSpySchema):
    """Generated wrapper for ``TextConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextConfig", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        fitToBand: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        logoLetters: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        squeeze: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        text: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            angle=angle,
            baseline=baseline,
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            dx=dx,
            dy=dy,
            fitToBand=fitToBand,
            flushX=flushX,
            flushY=flushY,
            font=font,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            logoLetters=logoLetters,
            minBufferSize=minBufferSize,
            opacity=opacity,
            paddingX=paddingX,
            paddingY=paddingY,
            size=size,
            squeeze=squeeze,
            style=style,
            text=text,
            tooltip=tooltip,
            viewportEdgeFadeDistanceBottom=viewportEdgeFadeDistanceBottom,
            viewportEdgeFadeDistanceLeft=viewportEdgeFadeDistanceLeft,
            viewportEdgeFadeDistanceRight=viewportEdgeFadeDistanceRight,
            viewportEdgeFadeDistanceTop=viewportEdgeFadeDistanceTop,
            viewportEdgeFadeWidthBottom=viewportEdgeFadeWidthBottom,
            viewportEdgeFadeWidthLeft=viewportEdgeFadeWidthLeft,
            viewportEdgeFadeWidthRight=viewportEdgeFadeWidthRight,
            viewportEdgeFadeWidthTop=viewportEdgeFadeWidthTop,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> TextConfig:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(self, value: Baseline_T) -> TextConfig:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_buildIndex(self, value: bool) -> TextConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> TextConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> TextConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_dx(self, value: float) -> TextConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: float) -> TextConfig:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_fitToBand(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` fitToBand."""
        return self._with_property("fitToBand", value, **kwargs)

    def with_flushX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` flushX."""
        return self._with_property("flushX", value, **kwargs)

    def with_flushY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` flushY."""
        return self._with_property("flushY", value, **kwargs)

    def with_font(self, value: str) -> TextConfig:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(self, value: FontStyle_T) -> TextConfig:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> TextConfig:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_minBufferSize(self, value: float) -> TextConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_paddingX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` paddingX."""
        return self._with_property("paddingX", value, **kwargs)

    def with_paddingY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` paddingY."""
        return self._with_property("paddingY", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_squeeze(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` squeeze."""
        return self._with_property("squeeze", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> TextConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(self, value: Scalar_T | ExprRef | dict[str, Any]) -> TextConfig:
        """Return a copy with ``text`` updated."""
        return self._with_property("text", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> TextConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: float) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthTop`` updated."""
        return self._with_property("viewportEdgeFadeWidthTop", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> TextConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> TextConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class TextDef(GenomeSpySchema):
    """Generated wrapper for ``TextDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextDef", {})

    def __init__(
        self,
        band: float | UndefinedType = Undefined,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: str | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
        value: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band,
            datum=datum,
            description=description,
            domainInert=domainInert,
            expr=expr,
            field=field,
            format=format,
            resolutionChannel=resolutionChannel,
            scale=scale,
            title=title,
            type=type,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_band(self, value: float) -> TextDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(self, value: Scalar_T | ExprRef | dict[str, Any]) -> TextDef:
        """Return a copy with ``datum`` updated."""
        return self._with_property("datum", value)

    def with_description(self, value: str) -> TextDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> TextDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: str) -> TextDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: str) -> TextDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: str) -> TextDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_resolutionChannel(self, value: ChannelWithScale_T) -> TextDef:
        """Return a copy with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def with_scale(
        self,
        value: Scale | ScaleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: str | None) -> TextDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Type_T) -> TextDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class TextProps(GenomeSpySchema):
    """Generated wrapper for ``TextProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextProps", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        fitToBand: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        logoLetters: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        squeeze: bool | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        text: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["text"] | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            angle=angle,
            baseline=baseline,
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            dx=dx,
            dy=dy,
            fitToBand=fitToBand,
            flushX=flushX,
            flushY=flushY,
            font=font,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            logoLetters=logoLetters,
            minBufferSize=minBufferSize,
            opacity=opacity,
            paddingX=paddingX,
            paddingY=paddingY,
            size=size,
            squeeze=squeeze,
            style=style,
            text=text,
            tooltip=tooltip,
            type=type,
            viewportEdgeFadeDistanceBottom=viewportEdgeFadeDistanceBottom,
            viewportEdgeFadeDistanceLeft=viewportEdgeFadeDistanceLeft,
            viewportEdgeFadeDistanceRight=viewportEdgeFadeDistanceRight,
            viewportEdgeFadeDistanceTop=viewportEdgeFadeDistanceTop,
            viewportEdgeFadeWidthBottom=viewportEdgeFadeWidthBottom,
            viewportEdgeFadeWidthLeft=viewportEdgeFadeWidthLeft,
            viewportEdgeFadeWidthRight=viewportEdgeFadeWidthRight,
            viewportEdgeFadeWidthTop=viewportEdgeFadeWidthTop,
            x=x,
            x2=x2,
            xOffset=xOffset,
            y=y,
            y2=y2,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> TextProps:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(self, value: Baseline_T) -> TextProps:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_buildIndex(self, value: bool) -> TextProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> TextProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> TextProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_dx(self, value: float) -> TextProps:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: float) -> TextProps:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_fitToBand(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` fitToBand."""
        return self._with_property("fitToBand", value, **kwargs)

    def with_flushX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` flushX."""
        return self._with_property("flushX", value, **kwargs)

    def with_flushY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` flushY."""
        return self._with_property("flushY", value, **kwargs)

    def with_font(self, value: str) -> TextProps:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(self, value: FontStyle_T) -> TextProps:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> TextProps:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_minBufferSize(self, value: float) -> TextProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_paddingX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` paddingX."""
        return self._with_property("paddingX", value, **kwargs)

    def with_paddingY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` paddingY."""
        return self._with_property("paddingY", value, **kwargs)

    def with_size(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_squeeze(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` squeeze."""
        return self._with_property("squeeze", value, **kwargs)

    def with_style(self, value: str | Sequence[str]) -> TextProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(self, value: Scalar_T | ExprRef | dict[str, Any]) -> TextProps:
        """Return a copy with ``text`` updated."""
        return self._with_property("text", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> TextProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["text"]) -> TextProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: float) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthTop`` updated."""
        return self._with_property("viewportEdgeFadeWidthTop", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_x2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` x2."""
        return self._with_property("x2", value, **kwargs)

    def with_xOffset(self, value: float) -> TextProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` y2."""
        return self._with_property("y2", value, **kwargs)

    def with_yOffset(self, value: float) -> TextProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class TickConfig(GenomeSpySchema):
    """Generated wrapper for ``TickConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TickConfig", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            minBufferSize=minBufferSize,
            minLength=minLength,
            opacity=opacity,
            orient=orient,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            style=style,
            thickness=thickness,
            tooltip=tooltip,
            x=x,
            xOffset=xOffset,
            y=y,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> TickConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> TickConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> TickConfig:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_minBufferSize(self, value: float) -> TickConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(self, value: Literal["vertical", "horizontal"]) -> TickConfig:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> TickConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> TickConfig:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: str | Sequence[str]) -> TickConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_thickness(self, value: float) -> TickConfig:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> TickConfig:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: float) -> TickConfig:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_yOffset(self, value: float) -> TickConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class TickProps(GenomeSpySchema):
    """Generated wrapper for ``TickProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TickProps", {})

    def __init__(
        self,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tooltip: HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        type: Literal["tick"] | UndefinedType = Undefined,
        x: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        y: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            buildIndex=buildIndex,
            clip=clip,
            color=color,
            cullByVisibleRange=cullByVisibleRange,
            cursor=cursor,
            minBufferSize=minBufferSize,
            minLength=minLength,
            opacity=opacity,
            orient=orient,
            strokeCap=strokeCap,
            strokeDash=strokeDash,
            strokeDashOffset=strokeDashOffset,
            style=style,
            thickness=thickness,
            tooltip=tooltip,
            type=type,
            x=x,
            xOffset=xOffset,
            y=y,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_buildIndex(self, value: bool) -> TickProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(
        self, value: bool | Literal["x"] | Literal["y"] | Literal["never"]
    ) -> TickProps:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_cullByVisibleRange(
        self, value: bool | Literal["x"] | Literal["y"]
    ) -> TickProps:
        """Return a copy with ``cullByVisibleRange`` updated."""
        return self._with_property("cullByVisibleRange", value)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_minBufferSize(self, value: float) -> TickProps:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minLength(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` minLength."""
        return self._with_property("minLength", value, **kwargs)

    def with_opacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_orient(self, value: Literal["vertical", "horizontal"]) -> TickProps:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_strokeCap(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` strokeCap."""
        return self._with_property("strokeCap", value, **kwargs)

    def with_strokeDash(self, value: Sequence[float]) -> TickProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: float) -> TickProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: str | Sequence[str]) -> TickProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_thickness(self, value: float) -> TickProps:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self, value: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    ) -> TickProps:
        """Return a copy with ``tooltip`` updated."""
        return self._with_property("tooltip", value)

    def with_type(self, value: Literal["tick"]) -> TickProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: float) -> TickProps:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_y(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``ExprRef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_yOffset(self, value: float) -> TickProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class Title(GenomeSpySchema):
    """Generated wrapper for ``Title``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Title", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        anchor: TitleAnchor_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        frame: TitleFrame_T | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: TitleOrient_T | UndefinedType = Undefined,
        reserve: bool | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        subtitle: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFont: str | UndefinedType = Undefined,
        subtitleFontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFontStyle: FontStyle_T | UndefinedType = Undefined,
        subtitleFontWeight: FontWeight_T | UndefinedType = Undefined,
        subtitlePadding: float | UndefinedType = Undefined,
        text: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            anchor=anchor,
            angle=angle,
            baseline=baseline,
            color=color,
            dx=dx,
            dy=dy,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            frame=frame,
            offset=offset,
            orient=orient,
            reserve=reserve,
            style=style,
            subtitle=subtitle,
            subtitleColor=subtitleColor,
            subtitleFont=subtitleFont,
            subtitleFontSize=subtitleFontSize,
            subtitleFontStyle=subtitleFontStyle,
            subtitleFontWeight=subtitleFontWeight,
            subtitlePadding=subtitlePadding,
            text=text,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> Title:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_anchor(self, value: TitleAnchor_T) -> Title:
        """Return a copy with ``anchor`` updated."""
        return self._with_property("anchor", value)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(self, value: Baseline_T) -> Title:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_dx(self, value: float) -> Title:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: float) -> Title:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_font(self, value: str) -> Title:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` fontSize."""
        return self._with_property("fontSize", value, **kwargs)

    def with_fontStyle(self, value: FontStyle_T) -> Title:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> Title:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_frame(self, value: TitleFrame_T) -> Title:
        """Return a copy with ``frame`` updated."""
        return self._with_property("frame", value)

    def with_offset(self, value: float) -> Title:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: TitleOrient_T) -> Title:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_reserve(self, value: bool) -> Title:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_style(self, value: str | Sequence[str]) -> Title:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_subtitle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` subtitle."""
        return self._with_property("subtitle", value, **kwargs)

    def with_subtitleColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` subtitleColor."""
        return self._with_property("subtitleColor", value, **kwargs)

    def with_subtitleFont(self, value: str) -> Title:
        """Return a copy with ``subtitleFont`` updated."""
        return self._with_property("subtitleFont", value)

    def with_subtitleFontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` subtitleFontSize."""
        return self._with_property("subtitleFontSize", value, **kwargs)

    def with_subtitleFontStyle(self, value: FontStyle_T) -> Title:
        """Return a copy with ``subtitleFontStyle`` updated."""
        return self._with_property("subtitleFontStyle", value)

    def with_subtitleFontWeight(self, value: FontWeight_T) -> Title:
        """Return a copy with ``subtitleFontWeight`` updated."""
        return self._with_property("subtitleFontWeight", value)

    def with_subtitlePadding(self, value: float) -> Title:
        """Return a copy with ``subtitlePadding`` updated."""
        return self._with_property("subtitlePadding", value)

    def with_text(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` text."""
        return self._with_property("text", value, **kwargs)

    def with_zindex(self, value: float) -> Title:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class TitleAnchor(GenomeSpySchema):
    """Generated wrapper for ``TitleAnchor``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleAnchor", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class TitleConfig(GenomeSpySchema):
    """Generated wrapper for ``TitleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleConfig", {})

    def __init__(
        self,
        align: Align_T | UndefinedType = Undefined,
        anchor: TitleAnchor_T | UndefinedType = Undefined,
        angle: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        color: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        frame: TitleFrame_T | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: TitleOrient_T | UndefinedType = Undefined,
        reserve: bool | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        subtitle: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFont: str | UndefinedType = Undefined,
        subtitleFontSize: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFontStyle: FontStyle_T | UndefinedType = Undefined,
        subtitleFontWeight: FontWeight_T | UndefinedType = Undefined,
        subtitlePadding: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            align=align,
            anchor=anchor,
            angle=angle,
            baseline=baseline,
            color=color,
            dx=dx,
            dy=dy,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            frame=frame,
            offset=offset,
            orient=orient,
            reserve=reserve,
            style=style,
            subtitle=subtitle,
            subtitleColor=subtitleColor,
            subtitleFont=subtitleFont,
            subtitleFontSize=subtitleFontSize,
            subtitleFontStyle=subtitleFontStyle,
            subtitleFontWeight=subtitleFontWeight,
            subtitlePadding=subtitlePadding,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_align(self, value: Align_T) -> TitleConfig:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_anchor(self, value: TitleAnchor_T) -> TitleConfig:
        """Return a copy with ``anchor`` updated."""
        return self._with_property("anchor", value)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(self, value: Baseline_T) -> TitleConfig:
        """Return a copy with ``baseline`` updated."""
        return self._with_property("baseline", value)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_dx(self, value: float) -> TitleConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: float) -> TitleConfig:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_font(self, value: str) -> TitleConfig:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` fontSize."""
        return self._with_property("fontSize", value, **kwargs)

    def with_fontStyle(self, value: FontStyle_T) -> TitleConfig:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> TitleConfig:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_frame(self, value: TitleFrame_T) -> TitleConfig:
        """Return a copy with ``frame`` updated."""
        return self._with_property("frame", value)

    def with_offset(self, value: float) -> TitleConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(self, value: TitleOrient_T) -> TitleConfig:
        """Return a copy with ``orient`` updated."""
        return self._with_property("orient", value)

    def with_reserve(self, value: bool) -> TitleConfig:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_style(self, value: str | Sequence[str]) -> TitleConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_subtitle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` subtitle."""
        return self._with_property("subtitle", value, **kwargs)

    def with_subtitleColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` subtitleColor."""
        return self._with_property("subtitleColor", value, **kwargs)

    def with_subtitleFont(self, value: str) -> TitleConfig:
        """Return a copy with ``subtitleFont`` updated."""
        return self._with_property("subtitleFont", value)

    def with_subtitleFontSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` subtitleFontSize."""
        return self._with_property("subtitleFontSize", value, **kwargs)

    def with_subtitleFontStyle(self, value: FontStyle_T) -> TitleConfig:
        """Return a copy with ``subtitleFontStyle`` updated."""
        return self._with_property("subtitleFontStyle", value)

    def with_subtitleFontWeight(self, value: FontWeight_T) -> TitleConfig:
        """Return a copy with ``subtitleFontWeight`` updated."""
        return self._with_property("subtitleFontWeight", value)

    def with_subtitlePadding(self, value: float) -> TitleConfig:
        """Return a copy with ``subtitlePadding`` updated."""
        return self._with_property("subtitlePadding", value)

    def with_zindex(self, value: float) -> TitleConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class TitleFrame(GenomeSpySchema):
    """Generated wrapper for ``TitleFrame``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleFrame", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class TitleOrient(GenomeSpySchema):
    """Generated wrapper for ``TitleOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class Tooltip(GenomeSpySchema):
    """Generated wrapper for ``Tooltip``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Tooltip", {})

    def __init__(
        self,
        handler: str | UndefinedType = Undefined,
        params: dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(handler=handler, params=params)
        if kwds:
            self._kwds.update(kwds)

    def with_handler(self, value: str) -> Tooltip:
        """Return a copy with ``handler`` updated."""
        return self._with_property("handler", value)

    def with_params(self, value: dict[str, Any]) -> Tooltip:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)


@with_property_setters
class TransformParams(GenomeSpySchema):
    """Generated wrapper for ``TransformParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TransformParams", {})

    def __init__(
        self,
        asChrom: str | UndefinedType = Undefined,
        asEnd: str | UndefinedType = Undefined,
        asKey: str | UndefinedType = Undefined,
        asMidpoint: str | UndefinedType = Undefined,
        asStart: str | UndefinedType = Undefined,
        asValue: Sequence[str] | str | UndefinedType = Undefined,
        baseField: Field_T | UndefinedType = Undefined,
        cardinality: float | UndefinedType = Undefined,
        channel: Literal["x", "y"] | UndefinedType = Undefined,
        chrom: Field_T | UndefinedType = Undefined,
        columnPadding: float | UndefinedType = Undefined,
        columnRegex: Sequence[str] | str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        direction: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        ellipsis: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        end: Field_T | UndefinedType = Undefined,
        exons: Field_T | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        fields: Sequence[Field_T] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        index: str | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        labelWidth: Field_T | UndefinedType = Undefined,
        lane: Field_T | UndefinedType = Undefined,
        limit: float | UndefinedType = Undefined,
        offset: Literal["zero", "center", "normalize", "information"]
        | UndefinedType = Undefined,
        ops: Sequence[AggregateOp_T] | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        pos: Field_T | Sequence[Field_T] | UndefinedType = Undefined,
        pos2: Field_T | UndefinedType = Undefined,
        preference: Field_T | UndefinedType = Undefined,
        preferredOrder: Sequence[str]
        | Sequence[float]
        | Sequence[bool]
        | UndefinedType = Undefined,
        regex: str | UndefinedType = Undefined,
        rowPadding: float | UndefinedType = Undefined,
        score: Field_T | UndefinedType = Undefined,
        separator: Sequence[str] | str | UndefinedType = Undefined,
        size: float | UndefinedType = Undefined,
        skipInvalidInput: bool | UndefinedType = Undefined,
        skipRegex: str | UndefinedType = Undefined,
        sort: CompareParams | CompareParamsKwds | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        start: Field_T | UndefinedType = Undefined,
        symbolOffset: float | UndefinedType = Undefined,
        symbolSize: float | Field_T | UndefinedType = Undefined,
        symbolStrokeWidth: float | Field_T | UndefinedType = Undefined,
        type: Literal["stack"] | UndefinedType = Undefined,
        weight: Field_T | UndefinedType = Undefined,
        width: Field_T | UndefinedType = Undefined,
        xOffset: float | UndefinedType = Undefined,
        yExtent: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            asChrom=asChrom,
            asEnd=asEnd,
            asKey=asKey,
            asMidpoint=asMidpoint,
            asStart=asStart,
            asValue=asValue,
            baseField=baseField,
            cardinality=cardinality,
            channel=channel,
            chrom=chrom,
            columnPadding=columnPadding,
            columnRegex=columnRegex,
            columns=columns,
            description=description,
            direction=direction,
            ellipsis=ellipsis,
            empty=empty,
            end=end,
            exons=exons,
            expr=expr,
            field=field,
            fields=fields,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            groupby=groupby,
            index=index,
            labelOffset=labelOffset,
            labelWidth=labelWidth,
            lane=lane,
            limit=limit,
            offset=offset,
            ops=ops,
            padding=padding,
            param=param,
            pos=pos,
            pos2=pos2,
            preference=preference,
            preferredOrder=preferredOrder,
            regex=regex,
            rowPadding=rowPadding,
            score=score,
            separator=separator,
            size=size,
            skipInvalidInput=skipInvalidInput,
            skipRegex=skipRegex,
            sort=sort,
            spacing=spacing,
            start=start,
            symbolOffset=symbolOffset,
            symbolSize=symbolSize,
            symbolStrokeWidth=symbolStrokeWidth,
            type=type,
            weight=weight,
            width=width,
            xOffset=xOffset,
            yExtent=yExtent,
            yOffset=yOffset,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_asChrom(self, value: str) -> TransformParams:
        """Return a copy with ``asChrom`` updated."""
        return self._with_property("asChrom", value)

    def with_asEnd(self, value: str) -> TransformParams:
        """Return a copy with ``asEnd`` updated."""
        return self._with_property("asEnd", value)

    def with_asKey(self, value: str) -> TransformParams:
        """Return a copy with ``asKey`` updated."""
        return self._with_property("asKey", value)

    def with_asMidpoint(self, value: str) -> TransformParams:
        """Return a copy with ``asMidpoint`` updated."""
        return self._with_property("asMidpoint", value)

    def with_asStart(self, value: str) -> TransformParams:
        """Return a copy with ``asStart`` updated."""
        return self._with_property("asStart", value)

    def with_asValue(self, value: Sequence[str] | str) -> TransformParams:
        """Return a copy with ``asValue`` updated."""
        return self._with_property("asValue", value)

    def with_baseField(self, value: Field_T) -> TransformParams:
        """Return a copy with ``baseField`` updated."""
        return self._with_property("baseField", value)

    def with_cardinality(self, value: float) -> TransformParams:
        """Return a copy with ``cardinality`` updated."""
        return self._with_property("cardinality", value)

    def with_channel(self, value: Literal["x", "y"]) -> TransformParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_chrom(self, value: Field_T) -> TransformParams:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_columnPadding(self, value: float) -> TransformParams:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columnRegex(self, value: Sequence[str] | str) -> TransformParams:
        """Return a copy with ``columnRegex`` updated."""
        return self._with_property("columnRegex", value)

    def with_columns(self, value: float) -> TransformParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_description(self, value: str) -> TransformParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_direction(
        self, value: Literal["vertical", "horizontal"]
    ) -> TransformParams:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_ellipsis(self, value: str) -> TransformParams:
        """Return a copy with ``ellipsis`` updated."""
        return self._with_property("ellipsis", value)

    def with_empty(self, value: bool) -> TransformParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_end(self, value: Field_T) -> TransformParams:
        """Return a copy with ``end`` updated."""
        return self._with_property("end", value)

    def with_exons(self, value: Field_T) -> TransformParams:
        """Return a copy with ``exons`` updated."""
        return self._with_property("exons", value)

    def with_expr(self, value: str) -> TransformParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: Field_T) -> TransformParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_fields(self, value: Sequence[Field_T]) -> TransformParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_font(self, value: str) -> TransformParams:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(self, value: float) -> TransformParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_fontStyle(self, value: FontStyle_T) -> TransformParams:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> TransformParams:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_groupby(self, value: Sequence[Field_T]) -> TransformParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_index(self, value: str) -> TransformParams:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_labelOffset(self, value: float) -> TransformParams:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelWidth(self, value: Field_T) -> TransformParams:
        """Return a copy with ``labelWidth`` updated."""
        return self._with_property("labelWidth", value)

    def with_lane(self, value: Field_T) -> TransformParams:
        """Return a copy with ``lane`` updated."""
        return self._with_property("lane", value)

    def with_limit(self, value: float) -> TransformParams:
        """Return a copy with ``limit`` updated."""
        return self._with_property("limit", value)

    def with_offset(
        self, value: Literal["zero", "center", "normalize", "information"]
    ) -> TransformParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_ops(self, value: Sequence[AggregateOp_T]) -> TransformParams:
        """Return a copy with ``ops`` updated."""
        return self._with_property("ops", value)

    def with_padding(self, value: float) -> TransformParams:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_param(self, value: str) -> TransformParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_pos(self, value: Field_T | Sequence[Field_T]) -> TransformParams:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)

    def with_pos2(self, value: Field_T) -> TransformParams:
        """Return a copy with ``pos2`` updated."""
        return self._with_property("pos2", value)

    def with_preference(self, value: Field_T) -> TransformParams:
        """Return a copy with ``preference`` updated."""
        return self._with_property("preference", value)

    def with_preferredOrder(
        self, value: Sequence[str] | Sequence[float] | Sequence[bool]
    ) -> TransformParams:
        """Return a copy with ``preferredOrder`` updated."""
        return self._with_property("preferredOrder", value)

    def with_regex(self, value: str) -> TransformParams:
        """Return a copy with ``regex`` updated."""
        return self._with_property("regex", value)

    def with_rowPadding(self, value: float) -> TransformParams:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_score(self, value: Field_T) -> TransformParams:
        """Return a copy with ``score`` updated."""
        return self._with_property("score", value)

    def with_separator(self, value: Sequence[str] | str) -> TransformParams:
        """Return a copy with ``separator`` updated."""
        return self._with_property("separator", value)

    def with_size(self, value: float) -> TransformParams:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_skipInvalidInput(self, value: bool) -> TransformParams:
        """Return a copy with ``skipInvalidInput`` updated."""
        return self._with_property("skipInvalidInput", value)

    def with_skipRegex(self, value: str) -> TransformParams:
        """Return a copy with ``skipRegex`` updated."""
        return self._with_property("skipRegex", value)

    def with_sort(
        self,
        value: CompareParams | CompareParamsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_spacing(self, value: float) -> TransformParams:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_start(self, value: Field_T) -> TransformParams:
        """Return a copy with ``start`` updated."""
        return self._with_property("start", value)

    def with_symbolOffset(self, value: float) -> TransformParams:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: float | Field_T) -> TransformParams:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: float | Field_T) -> TransformParams:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_type(self, value: Literal["stack"]) -> TransformParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_weight(self, value: Field_T) -> TransformParams:
        """Return a copy with ``weight`` updated."""
        return self._with_property("weight", value)

    def with_width(self, value: Field_T) -> TransformParams:
        """Return a copy with ``width`` updated."""
        return self._with_property("width", value)

    def with_xOffset(self, value: float) -> TransformParams:
        """Return a copy with ``xOffset`` updated."""
        return self._with_property("xOffset", value)

    def with_yExtent(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``ExprRef`` yExtent."""
        return self._with_property("yExtent", value, **kwargs)

    def with_yOffset(self, value: float) -> TransformParams:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


@with_property_setters
class TruncateTextParams(GenomeSpySchema):
    """Generated wrapper for ``TruncateTextParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TruncateTextParams", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        ellipsis: str | UndefinedType = Undefined,
        field: Field_T | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        limit: float | UndefinedType = Undefined,
        type: Literal["truncateText"] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description,
            ellipsis=ellipsis,
            field=field,
            font=font,
            fontSize=fontSize,
            fontStyle=fontStyle,
            fontWeight=fontWeight,
            limit=limit,
            type=type,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> TruncateTextParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_ellipsis(self, value: str) -> TruncateTextParams:
        """Return a copy with ``ellipsis`` updated."""
        return self._with_property("ellipsis", value)

    def with_field(self, value: Field_T) -> TruncateTextParams:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_font(self, value: str) -> TruncateTextParams:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(self, value: float) -> TruncateTextParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_fontStyle(self, value: FontStyle_T) -> TruncateTextParams:
        """Return a copy with ``fontStyle`` updated."""
        return self._with_property("fontStyle", value)

    def with_fontWeight(self, value: FontWeight_T) -> TruncateTextParams:
        """Return a copy with ``fontWeight`` updated."""
        return self._with_property("fontWeight", value)

    def with_limit(self, value: float) -> TruncateTextParams:
        """Return a copy with ``limit`` updated."""
        return self._with_property("limit", value)

    def with_type(self, value: Literal["truncateText"]) -> TruncateTextParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


@with_property_setters
class Type(GenomeSpySchema):
    """Generated wrapper for ``Type``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Type", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class TypeForShape(GenomeSpySchema):
    """Generated wrapper for ``TypeForShape``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TypeForShape", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


@with_property_setters
class UnitSpec(GenomeSpySchema):
    """Generated wrapper for ``UnitSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UnitSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        mark: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | DynamicOpacity
        | DynamicOpacityKwds
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        view: ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            height=height,
            legends=legends,
            mark=mark,
            name=name,
            opacity=opacity,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            templates=templates,
            title=title,
            transform=transform,
            view=view,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> UnitSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> UnitSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> UnitSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> UnitSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> UnitSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: LegendsKwds) -> UnitSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps,
    ) -> UnitSpec:
        """Return a copy with ``mark`` updated."""
        return self._with_property("mark", value)

    def with_name(self, value: str) -> UnitSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any],
    ) -> UnitSpec:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> UnitSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> UnitSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> UnitSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> UnitSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_templates(self, value: dict[str, Any]) -> UnitSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> UnitSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> UnitSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class UrlData(GenomeSpySchema):
    """Generated wrapper for ``UrlData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlData", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        format: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlList
        | UrlTemplate
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, format=format, name=name, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> UrlData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: CsvDataFormat
        | dict[str, Any]
        | DsvDataFormat
        | JsonDataFormat
        | BedDataFormat
        | BedpeDataFormat
        | OtherDataFormat,
    ) -> UrlData:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_name(self, value: str) -> UrlData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(
        self,
        value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlList | UrlTemplate,
    ) -> UrlData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class UrlGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeConfig", {})

    def __init__(
        self,
        name: str | UndefinedType = Undefined,
        url: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(name=name, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: str) -> UrlGenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(self, value: str) -> UrlGenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class UrlGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeDefinition", {})

    def __init__(self, url: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_url(self, value: str) -> UrlGenomeDefinition:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class UrlImport(GenomeSpySchema):
    """Generated wrapper for ``UrlImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlImport", {})

    def __init__(self, url: str | UndefinedType = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_url(self, value: str) -> UrlImport:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


@with_property_setters
class UrlList(GenomeSpySchema):
    """Generated wrapper for ``UrlList``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlList", {})

    def __init__(
        self,
        type: Literal["json", "csv", "tsv"] | UndefinedType = Undefined,
        urlsFromFile: str | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(type=type, urlsFromFile=urlsFromFile)
        if kwds:
            self._kwds.update(kwds)

    def with_type(self, value: Literal["json", "csv", "tsv"]) -> UrlList:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_urlsFromFile(self, value: str) -> UrlList:
        """Return a copy with ``urlsFromFile`` updated."""
        return self._with_property("urlsFromFile", value)


@with_property_setters
class UrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``UrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlSourceRef", {})

    def __init__(
        self,
        attach: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        field: FieldName_T | UndefinedType = Undefined,
        maxValues: float | UndefinedType = Undefined,
        onLoadError: Literal["error", "skip"] | UndefinedType = Undefined,
        template: str | UndefinedType = Undefined,
        type: Literal["json", "csv", "tsv"] | UndefinedType = Undefined,
        urlsFromFile: str | UndefinedType = Undefined,
        values: Sequence[Scalar_T]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            attach=attach,
            expr=expr,
            field=field,
            maxValues=maxValues,
            onLoadError=onLoadError,
            template=template,
            type=type,
            urlsFromFile=urlsFromFile,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_attach(self, value: bool) -> UrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: str) -> UrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: FieldName_T) -> UrlSourceRef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_maxValues(self, value: float) -> UrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Literal["error", "skip"]) -> UrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: str) -> UrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)

    def with_type(self, value: Literal["json", "csv", "tsv"]) -> UrlSourceRef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_urlsFromFile(self, value: str) -> UrlSourceRef:
        """Return a copy with ``urlsFromFile`` updated."""
        return self._with_property("urlsFromFile", value)

    def with_values(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlSourceRef:
        """Return a copy with a ``ExprRef`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class UrlTemplate(GenomeSpySchema):
    """Generated wrapper for ``UrlTemplate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlTemplate", {})

    def __init__(
        self,
        attach: bool | UndefinedType = Undefined,
        field: FieldName_T | UndefinedType = Undefined,
        maxValues: float | UndefinedType = Undefined,
        onLoadError: Literal["error", "skip"] | UndefinedType = Undefined,
        template: str | UndefinedType = Undefined,
        values: Sequence[Scalar_T]
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            attach=attach,
            field=field,
            maxValues=maxValues,
            onLoadError=onLoadError,
            template=template,
            values=values,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_attach(self, value: bool) -> UrlTemplate:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_field(self, value: FieldName_T) -> UrlTemplate:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_maxValues(self, value: float) -> UrlTemplate:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Literal["error", "skip"]) -> UrlTemplate:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: str) -> UrlTemplate:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)

    def with_values(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlTemplate:
        """Return a copy with a ``ExprRef`` values."""
        return self._with_property("values", value, **kwargs)


@with_property_setters
class VConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``VConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VConcatSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        vconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            height=height,
            legends=legends,
            name=name,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            separator=separator,
            spacing=spacing,
            templates=templates,
            title=title,
            transform=transform,
            vconcat=vconcat,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> VConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> VConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> VConcatSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> VConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> VConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: LegendsKwds) -> VConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: str) -> VConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> VConcatSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> VConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> VConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> VConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | SeparatorPropsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: float) -> VConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: dict[str, Any]) -> VConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> VConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> VConcatSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> VConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class ValueDefNumber(GenomeSpySchema):
    """Generated wrapper for ``ValueDef<number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ValueDef<number>", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ValueDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> ValueDefNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefNumber:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ValueDefString(GenomeSpySchema):
    """Generated wrapper for ``ValueDef<string>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ValueDef<string>", {})

    def __init__(
        self,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: str) -> ValueDefString:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> ValueDefString:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefString:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ValueDefWithConditionStringNullType(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<(string|null),Type>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<(string|null),Type>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> ValueDefWithConditionStringNullType:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(self, value: str) -> ValueDefWithConditionStringNullType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> ValueDefWithConditionStringNullType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionStringNullType:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ValueDefWithConditionStringNullTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<(string|null),TypeForShape>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<(string|null),TypeForShape>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: str | None | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(
        self, value: str
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(
        self, value: str | None
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class ValueDefWithConditionNumberType(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<number,Type>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<number,Type>", {}
    )

    def __init__(
        self,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        value: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)

    def with_condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> ValueDefWithConditionNumberType:
        """Return a copy with ``condition`` updated."""
        return self._with_property("condition", value)

    def with_description(self, value: str) -> ValueDefWithConditionNumberType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: str | None) -> ValueDefWithConditionNumberType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionNumberType:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


@with_property_setters
class VariableParameter(GenomeSpySchema):
    """Generated wrapper for ``VariableParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VariableParameter", {})

    def __init__(
        self,
        bind: BindCheckbox
        | BindCheckboxKwds
        | BindRadioSelect
        | BindRadioSelectKwds
        | BindRange
        | BindRangeKwds
        | BindInput
        | BindInputKwds
        | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        persist: bool | UndefinedType = Undefined,
        push: Literal["outer"] | UndefinedType = Undefined,
        value: Any | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            bind=bind,
            description=description,
            expr=expr,
            name=name,
            persist=persist,
            push=push,
            value=value,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_bind(
        self,
        value: BindCheckbox
        | BindCheckboxKwds
        | BindRadioSelect
        | BindRadioSelectKwds
        | BindRange
        | BindRangeKwds
        | BindInput
        | BindInputKwds,
    ) -> VariableParameter:
        """Return a copy with ``bind`` updated."""
        return self._with_property("bind", value)

    def with_description(self, value: str) -> VariableParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: str) -> VariableParameter:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_name(self, value: str) -> VariableParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: bool) -> VariableParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Literal["outer"]) -> VariableParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_value(self, value: Any) -> VariableParameter:
        """Return a copy with ``value`` updated."""
        return self._with_property("value", value)


@with_property_setters
class VcfData(GenomeSpySchema):
    """Generated wrapper for ``VcfData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VcfData", {})

    def __init__(
        self,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | ExprRef
        | dict[str, Any]
        | IndexUrlTemplate
        | UndefinedType = Undefined,
        type: Literal["vcf"] | UndefinedType = Undefined,
        url: str
        | Sequence[str]
        | ExprRef
        | dict[str, Any]
        | UrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            addChrPrefix=addChrPrefix,
            channel=channel,
            debounce=debounce,
            debounceDomainChange=debounceDomainChange,
            debounceMode=debounceMode,
            indexUrl=indexUrl,
            type=type,
            url=url,
            windowSize=windowSize,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_addChrPrefix(self, value: bool | str) -> VcfData:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(self, value: PrimaryPositionalChannel_T) -> VcfData:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_debounce(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VcfData:
        """Return a copy with a ``ExprRef`` debounce."""
        return self._with_property("debounce", value, **kwargs)

    def with_debounceDomainChange(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VcfData:
        """Return a copy with a ``ExprRef`` debounceDomainChange."""
        return self._with_property("debounceDomainChange", value, **kwargs)

    def with_debounceMode(self, value: Literal["domain", "window"]) -> VcfData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self, value: str | ExprRef | dict[str, Any] | IndexUrlTemplate
    ) -> VcfData:
        """Return a copy with ``indexUrl`` updated."""
        return self._with_property("indexUrl", value)

    def with_type(self, value: Literal["vcf"]) -> VcfData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self, value: str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate
    ) -> VcfData:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)

    def with_windowSize(self, value: float) -> VcfData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


@with_property_setters
class ViewBackground(GenomeSpySchema):
    """Generated wrapper for ``ViewBackground``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewBackground", {})

    def __init__(
        self,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeOpacity: float | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        strokeZindex: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            fill=fill,
            fillOpacity=fillOpacity,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            strokeZindex=strokeZindex,
            style=style,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_fill(self, value: str) -> ViewBackground:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: float) -> ViewBackground:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewBackground:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewBackground:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewBackground:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewBackground:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewBackground:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_stroke(self, value: str) -> ViewBackground:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: float) -> ViewBackground:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: float) -> ViewBackground:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_strokeZindex(self, value: float) -> ViewBackground:
        """Return a copy with ``strokeZindex`` updated."""
        return self._with_property("strokeZindex", value)

    def with_style(self, value: str | Sequence[str]) -> ViewBackground:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_zindex(self, value: float) -> ViewBackground:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class ViewConfig(GenomeSpySchema):
    """Generated wrapper for ``ViewConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewConfig", {})

    def __init__(
        self,
        continuousHeight: float | UndefinedType = Undefined,
        continuousWidth: float | UndefinedType = Undefined,
        discreteHeight: float | Step | StepKwds | UndefinedType = Undefined,
        discreteWidth: float | Step | StepKwds | UndefinedType = Undefined,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        shadowBlur: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetY: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOpacity: float | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        step: float | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeOpacity: float | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        strokeZindex: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            continuousHeight=continuousHeight,
            continuousWidth=continuousWidth,
            discreteHeight=discreteHeight,
            discreteWidth=discreteWidth,
            fill=fill,
            fillOpacity=fillOpacity,
            shadowBlur=shadowBlur,
            shadowColor=shadowColor,
            shadowOffsetX=shadowOffsetX,
            shadowOffsetY=shadowOffsetY,
            shadowOpacity=shadowOpacity,
            step=step,
            stroke=stroke,
            strokeOpacity=strokeOpacity,
            strokeWidth=strokeWidth,
            strokeZindex=strokeZindex,
            zindex=zindex,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_continuousHeight(self, value: float) -> ViewConfig:
        """Return a copy with ``continuousHeight`` updated."""
        return self._with_property("continuousHeight", value)

    def with_continuousWidth(self, value: float) -> ViewConfig:
        """Return a copy with ``continuousWidth`` updated."""
        return self._with_property("continuousWidth", value)

    def with_discreteHeight(
        self,
        value: Step | StepKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``Step`` discreteHeight."""
        return self._with_property("discreteHeight", value, **kwargs)

    def with_discreteWidth(
        self,
        value: Step | StepKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``Step`` discreteWidth."""
        return self._with_property("discreteWidth", value, **kwargs)

    def with_fill(self, value: str) -> ViewConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: float) -> ViewConfig:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_shadowBlur(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``ExprRef`` shadowBlur."""
        return self._with_property("shadowBlur", value, **kwargs)

    def with_shadowColor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``ExprRef`` shadowColor."""
        return self._with_property("shadowColor", value, **kwargs)

    def with_shadowOffsetX(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetX."""
        return self._with_property("shadowOffsetX", value, **kwargs)

    def with_shadowOffsetY(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``ExprRef`` shadowOffsetY."""
        return self._with_property("shadowOffsetY", value, **kwargs)

    def with_shadowOpacity(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``ExprRef`` shadowOpacity."""
        return self._with_property("shadowOpacity", value, **kwargs)

    def with_step(self, value: float) -> ViewConfig:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)

    def with_stroke(self, value: str) -> ViewConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: float) -> ViewConfig:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: float) -> ViewConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_strokeZindex(self, value: float) -> ViewConfig:
        """Return a copy with ``strokeZindex`` updated."""
        return self._with_property("strokeZindex", value)

    def with_zindex(self, value: float) -> ViewConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


@with_property_setters
class ViewOpacityDef(GenomeSpySchema):
    """Generated wrapper for ``ViewOpacityDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewOpacityDef", {})

    def __init__(
        self,
        channel: PrimaryPositionalChannel_T
        | Literal["auto"]
        | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        unitsPerPixel: Sequence[float | ExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        values: Sequence[float] | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel, expr=expr, unitsPerPixel=unitsPerPixel, values=values
        )
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self, value: PrimaryPositionalChannel_T | Literal["auto"]
    ) -> ViewOpacityDef:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_expr(self, value: str) -> ViewOpacityDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_unitsPerPixel(
        self, value: Sequence[float | ExprRef | dict[str, Any]]
    ) -> ViewOpacityDef:
        """Return a copy with ``unitsPerPixel`` updated."""
        return self._with_property("unitsPerPixel", value)

    def with_values(self, value: Sequence[float]) -> ViewOpacityDef:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


@with_property_setters
class ViewSpec(GenomeSpySchema):
    """Generated wrapper for ``ViewSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewSpec", {})

    def __init__(
        self,
        axes: AxesKwds | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        concat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        config: GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator
        | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: Encoding | EncodingKwds | UndefinedType = Undefined,
        hconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        height: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        layer: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        mark: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps
        | UndefinedType = Undefined,
        multiscale: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ]
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | DynamicOpacity
        | DynamicOpacityKwds
        | ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        stops: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any]
        | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        title: str | Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ]
        | UndefinedType = Undefined,
        vconcat: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ]
        | UndefinedType = Undefined,
        view: ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: SizeDef
        | SizeDefKwds
        | float
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: SizeDef
        | SizeDefKwds
        | float
        | Step
        | StepKwds
        | Literal["container"]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            axes=axes,
            baseUrl=baseUrl,
            columns=columns,
            concat=concat,
            config=config,
            cursor=cursor,
            data=data,
            description=description,
            domainInert=domainInert,
            encoding=encoding,
            hconcat=hconcat,
            height=height,
            layer=layer,
            legends=legends,
            mark=mark,
            multiscale=multiscale,
            name=name,
            opacity=opacity,
            padding=padding,
            params=params,
            resolve=resolve,
            scales=scales,
            separator=separator,
            spacing=spacing,
            stops=stops,
            templates=templates,
            title=title,
            transform=transform,
            vconcat=vconcat,
            view=view,
            viewportHeight=viewportHeight,
            viewportWidth=viewportWidth,
            visible=visible,
            width=width,
        )
        if kwds:
            self._kwds.update(kwds)

    def with_axes(self, value: AxesKwds) -> ViewSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: str) -> ViewSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: float) -> ViewSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> ViewSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_cursor(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``ExprRef`` cursor."""
        return self._with_property("cursor", value, **kwargs)

    def with_data(
        self,
        value: UrlData
        | dict[str, Any]
        | InlineData
        | NamedData
        | DynamicCallbackData
        | LazyData
        | SequenceGenerator,
    ) -> ViewSpec:
        """Return a copy with ``data`` updated."""
        return self._with_property("data", value)

    def with_description(self, value: str | Sequence[str]) -> ViewSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: bool) -> ViewSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | EncodingKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_hconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> ViewSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> ViewSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: LegendsKwds) -> ViewSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType_T
        | RectProps
        | dict[str, Any]
        | TextProps
        | RuleProps
        | TickProps
        | LinkProps
        | PointProps,
    ) -> ViewSpec:
        """Return a copy with ``mark`` updated."""
        return self._with_property("mark", value)

    def with_multiscale(
        self,
        value: Sequence[
            LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec
        ],
    ) -> ViewSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: str) -> ViewSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any],
    ) -> ViewSpec:
        """Return a copy with ``opacity`` updated."""
        return self._with_property("opacity", value)

    def with_padding(self, value: Paddings | PaddingsKwds | float) -> ViewSpec:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_params(
        self,
        value: Sequence[
            VariableParameter | dict[str, Any] | SelectionParameter | RulerParameter
        ],
    ) -> ViewSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: ResolveKwds) -> ViewSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: ScalesKwds) -> ViewSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | SeparatorPropsKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: float) -> ViewSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_stops(
        self,
        value: Sequence[float | ExprRef | dict[str, Any]]
        | MultiscaleStops
        | dict[str, Any],
    ) -> ViewSpec:
        """Return a copy with ``stops`` updated."""
        return self._with_property("stops", value)

    def with_templates(self, value: dict[str, Any]) -> ViewSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | TitleKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(
        self,
        value: Sequence[
            AggregateParams
            | dict[str, Any]
            | CollectParams
            | CoverageParams
            | FlattenDelimitedParams
            | FormulaParams
            | ExprFilterParams
            | SelectionFilterParams
            | FilterScoredLabelsParams
            | FlattenParams
            | FlattenCompressedExonsParams
            | FlattenSequenceParams
            | IdentifierParams
            | LinearizeGenomicCoordinateParams
            | MeasureTextParams
            | TruncateTextParams
            | PackLegendLabelsParams
            | MergeFacetsParams
            | PileupParams
            | ProjectParams
            | RegexExtractParams
            | RegexFoldParams
            | SampleParams
            | StackParams
        ],
    ) -> ViewSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(
        self,
        value: Sequence[
            UnitSpec
            | dict[str, Any]
            | LayerSpec
            | MultiscaleSpec
            | VConcatSpec
            | HConcatSpec
            | ConcatSpec
            | ImportSpec
        ],
    ) -> ViewSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: bool) -> ViewSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | SizeDefKwds | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


@with_property_setters
class ZoomParams(GenomeSpySchema):
    """Generated wrapper for ``ZoomParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ZoomParams", {})

    def __init__(
        self,
        extent: ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | UndefinedType = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(extent=extent)
        if kwds:
            self._kwds.update(kwds)

    def with_extent(
        self, value: ScalarDomain_T | Sequence[ChromosomalLocus | dict[str, Any]]
    ) -> ZoomParams:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)


__all__ = [
    "GenomeSpySchema",
    "MARK_TYPES",
    "Root",
    "load_schema",
    "AggregateOp",
    "AggregateParams",
    "Align",
    "Axis",
    "AxisConfig",
    "AxisGenomeData",
    "AxisOrient",
    "AxisPlacement",
    "AxisTicksData",
    "BamData",
    "Baseline",
    "BedDataFormat",
    "BedpeDataFormat",
    "BigBedData",
    "BigWigData",
    "BindCheckbox",
    "BindInput",
    "BindRadioSelect",
    "BindRange",
    "Binding",
    "BrushConfig",
    "BuiltInThemeName",
    "ChannelWithScale",
    "ChromPosDef",
    "ChromosomalLocus",
    "CollectParams",
    "ColorDef",
    "ColorSchemeConfig",
    "CompareParams",
    "ComplexDomain",
    "ConcatSpec",
    "ConditionalMarkPropExprDefType",
    "ConditionalMarkPropExprDefTypeForShape",
    "ConditionalMarkPropFieldDefType",
    "ConditionalMarkPropFieldDefTypeForShape",
    "ConditionalScaleDatumDef",
    "ConditionalValueDefNumberExprRef",
    "ConditionalValueDefStringNullExprRef",
    "ConditionalParameterMarkPropExprDefType",
    "ConditionalParameterMarkPropExprDefTypeForShape",
    "ConditionalParameterMarkPropFieldDefType",
    "ConditionalParameterMarkPropFieldDefTypeForShape",
    "ConditionalParameterScaleDatumDef",
    "ConditionalParameterValueDefNumberExprRef",
    "ConditionalParameterValueDefStringNullExprRef",
    "Contig",
    "CoreRootSpec",
    "CoverageParams",
    "CsvDataFormat",
    "Data",
    "DataFormat",
    "DataSource",
    "DomEventType",
    "DomainValue",
    "DomainValueArray",
    "DsvDataFormat",
    "DynamicCallbackData",
    "DynamicOpacity",
    "Encoding",
    "EventConfig",
    "ExprDef",
    "ExprFilterParams",
    "ExprRef",
    "Field",
    "FieldDefWithoutScale",
    "FieldName",
    "FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull",
    "FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber",
    "FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull",
    "FieldOrDatumDefWithConditionScaleDatumDefStringNull",
    "FieldOrDatumDefWithConditionScaleDatumDefNumber",
    "FilterParams",
    "FilterScoredLabelsParams",
    "FlattenCompressedExonsParams",
    "FlattenDelimitedParams",
    "FlattenParams",
    "FlattenSequenceParams",
    "FontStyle",
    "FontWeight",
    "FormulaParams",
    "Generator",
    "GenomeAxis",
    "GenomeConfig",
    "GenomeConfigBase",
    "GenomeDefinition",
    "GenomeSpyConfig",
    "Gff3Data",
    "HConcatSpec",
    "HandledTooltip",
    "IdentifierParams",
    "ImportSpec",
    "IndexUrlSourceRef",
    "IndexUrlTemplate",
    "IndexedFastaData",
    "InlineData",
    "InlineDataset",
    "InlineGenomeConfig",
    "InlineGenomeDefinition",
    "InlineLocusAssembly",
    "InteractionEventType",
    "IntervalSelectionConfig",
    "JsonDataFormat",
    "KeyDef",
    "LayerSpec",
    "LazyData",
    "LazyDataParams",
    "Legend",
    "LegendConfig",
    "LegendDirection",
    "LegendOrient",
    "LegendTitleOrient",
    "LinearizeGenomicCoordinateParams",
    "LinkConfig",
    "LinkProps",
    "MarkConfig",
    "MarkPropDefStringNullTypeForShape",
    "MarkPropDefStringNull",
    "MarkPropDefNumber",
    "MarkPropExprDef",
    "MarkProps",
    "MarkType",
    "MeasureTextParams",
    "MergeFacetsParams",
    "MultiUrlSourceRef",
    "MultiscaleSpec",
    "MultiscaleStops",
    "MultiscaleStopsDef",
    "NamedData",
    "NamedGenomeConfig",
    "NumericDomain",
    "NumericMarkPropDef",
    "NumericStopDef",
    "NumericValueDef",
    "OtherDataFormat",
    "PackLegendLabelsParams",
    "PaddingConfig",
    "Paddings",
    "Parameter",
    "Parse",
    "ParseValue",
    "PileupParams",
    "PointConfig",
    "PointProps",
    "PointSelectionConfig",
    "Position2Def",
    "PositionDatumDef",
    "PositionDef",
    "PositionExprDef",
    "PositionFieldDef",
    "PositionValueDef",
    "PositionalChannel",
    "PrimaryPositionalChannel",
    "ProjectParams",
    "RangeConfig",
    "RectConfig",
    "RectProps",
    "RegexExtractParams",
    "RegexFoldParams",
    "ResolutionBehavior",
    "RuleConfig",
    "RuleProps",
    "RulerChannelValue",
    "RulerClear",
    "RulerConfig",
    "RulerDisplay",
    "RulerEventConfig",
    "RulerEventType",
    "RulerExtent",
    "RulerInitMapping",
    "RulerMarkConfig",
    "RulerParameter",
    "RulerSnap",
    "RulerSource",
    "SampleParams",
    "Scalar",
    "ScalarDomain",
    "Scale",
    "ScaleConfig",
    "ScaleInterpolate",
    "ScaleInterpolateParams",
    "ScaleType",
    "SchemeParams",
    "SearchDef",
    "SecondaryChromPosDef",
    "SecondaryPositionalChannel",
    "SelectionDomainRef",
    "SelectionExtent",
    "SelectionFilterParams",
    "SelectionInitIntervalMapping",
    "SelectionParameter",
    "SelectionType",
    "SeparatorProps",
    "SequenceGenerator",
    "SequenceParams",
    "ShapeDef",
    "SingleUrlSourceRef",
    "SizeDef",
    "SortOrder",
    "StackParams",
    "Step",
    "StringDatumDef",
    "StringFieldDef",
    "StyleConfig",
    "TabixTsvData",
    "TemplateImport",
    "TextConfig",
    "TextDef",
    "TextProps",
    "TickConfig",
    "TickProps",
    "Title",
    "TitleAnchor",
    "TitleConfig",
    "TitleFrame",
    "TitleOrient",
    "Tooltip",
    "TransformParams",
    "TruncateTextParams",
    "Type",
    "TypeForShape",
    "UnitSpec",
    "UrlData",
    "UrlGenomeConfig",
    "UrlGenomeDefinition",
    "UrlImport",
    "UrlList",
    "UrlSourceRef",
    "UrlTemplate",
    "VConcatSpec",
    "ValueDefNumber",
    "ValueDefString",
    "ValueDefWithConditionStringNullType",
    "ValueDefWithConditionStringNullTypeForShape",
    "ValueDefWithConditionNumberType",
    "VariableParameter",
    "VcfData",
    "ViewBackground",
    "ViewConfig",
    "ViewOpacityDef",
    "ViewSpec",
    "ZoomParams",
]
