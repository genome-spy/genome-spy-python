"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import TYPE_CHECKING, TypedDict, Any, Literal

from genome_spy.schema._typing import (
    Align_T,
    AxisOrient_T,
    AxisPlacement_T,
    Baseline_T,
    DomEventType_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    LegendDirection_T,
    LegendOrient_T,
    LegendTitleOrient_T,
    PrimaryPositionalChannel_T,
    ResolutionBehavior_T,
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
    SelectionType_T,
    SortOrder_T,
    TitleAnchor_T,
    TitleFrame_T,
    TitleOrient_T,
)

if TYPE_CHECKING:
    from genome_spy.schema.core import (
        ArrowConfig,
        AxisConfig,
        BindCheckbox,
        BindInput,
        BindRadioSelect,
        BindRange,
        ChromPosDef,
        ChromosomalLocus,
        DirectionDef,
        ExprDef,
        ExprRef,
        FieldDefWithoutScale,
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull,
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber,
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull,
        FieldOrDatumDefWithConditionScaleDatumDefNumber,
        FieldOrDatumDefWithConditionScaleDatumDefStringNull,
        GenomeAxis,
        HandledTooltip,
        InlineGenomeDefinition,
        IntervalSelectionConfig,
        Legend,
        LegendConfig,
        LerpTransition,
        LinkConfig,
        MarkConfig,
        MarkPropExprDef,
        Parse,
        PointConfig,
        PointSelectionConfig,
        Position2Def,
        PositionDatumDef,
        PositionExprDef,
        PositionFieldDef,
        RangeConfig,
        RectConfig,
        RuleConfig,
        RulerConfig,
        RulerEventConfig,
        RulerInitMapping,
        RulerMarkConfig,
        Scale,
        ScaleConfig,
        ScaleInterpolateParams,
        SchemeParams,
        SelectionDomainRef,
        Step,
        StringDatumDef,
        StringFieldDef,
        TextConfig,
        TickConfig,
        TitleConfig,
        UrlGenomeDefinition,
        ValueDefNumber,
        ValueDefString,
        ValueDefWithConditionNumberType,
        ValueDefWithConditionStringNullType,
        ValueDefWithConditionStringNullTypeForShape,
        ViewConfig,
        ZoomParams,
    )


class AxisKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Axis`` mappings."""

    domain: bool
    domainCap: Literal["butt", "round", "square"]
    domainColor: str
    domainDash: Sequence[float]
    domainDashOffset: float
    domainWidth: float
    format: str
    grid: bool
    gridCap: Literal["butt", "round", "square"]
    gridColor: str
    gridDash: Sequence[float]
    gridDashOffset: float
    gridOpacity: float
    gridWidth: float
    labelAlign: Align_T
    labelAngle: float
    labelBaseline: Baseline_T
    labelColor: str
    labelFont: str
    labelFontSize: float
    labelFontStyle: FontStyle_T
    labelFontWeight: FontWeight_T
    labelLimit: float
    labelPadding: float
    labels: bool
    maxExtent: float
    minExtent: float
    offset: float
    orient: AxisOrient_T
    placement: AxisPlacement_T
    style: str | Sequence[str] | None
    tickCap: Literal["butt", "round", "square"]
    tickColor: str
    tickCount: float | ExprRef | dict[str, Any]
    tickDash: Sequence[float]
    tickDashOffset: float
    tickMinStep: float
    tickSize: float
    tickWidth: float
    ticks: bool
    title: str | None
    titleColor: str
    titleFit: Literal["point", "range"]
    titleFont: str
    titleFontSize: float
    titleFontStyle: FontStyle_T
    titleFontWeight: FontWeight_T
    titleOpacity: float
    titlePadding: float
    values: Sequence[Any]
    zindex: float


class AxisConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``AxisConfig`` mappings."""

    chromGrid: bool
    chromGridCap: Literal["butt", "round", "square"]
    chromGridColor: str
    chromGridDash: Sequence[float]
    chromGridDashOffset: float
    chromGridFillEven: str
    chromGridFillOdd: str
    chromGridOpacity: float
    chromGridWidth: float
    chromLabelAlign: Align_T
    chromLabelColor: str
    chromLabelFont: str
    chromLabelFontSize: float
    chromLabelFontStyle: FontStyle_T
    chromLabelFontWeight: FontWeight_T
    chromLabelPadding: float
    chromLabels: bool
    chromTickColor: str
    chromTickDash: Sequence[float]
    chromTickDashOffset: float
    chromTickSize: float
    chromTickWidth: float
    chromTicks: bool
    domain: bool
    domainCap: Literal["butt", "round", "square"]
    domainColor: str
    domainDash: Sequence[float]
    domainDashOffset: float
    domainWidth: float
    format: str
    grid: bool
    gridCap: Literal["butt", "round", "square"]
    gridColor: str
    gridDash: Sequence[float]
    gridDashOffset: float
    gridOpacity: float
    gridWidth: float
    labelAlign: Align_T
    labelAngle: float
    labelBaseline: Baseline_T
    labelColor: str
    labelFont: str
    labelFontSize: float
    labelFontStyle: FontStyle_T
    labelFontWeight: FontWeight_T
    labelLimit: float
    labelPadding: float
    labels: bool
    maxExtent: float
    minExtent: float
    offset: float
    orient: AxisOrient_T
    placement: AxisPlacement_T
    style: str | Sequence[str] | None
    tickCap: Literal["butt", "round", "square"]
    tickColor: str
    tickCount: float | ExprRef | dict[str, Any]
    tickDash: Sequence[float]
    tickDashOffset: float
    tickMinStep: float
    tickSize: float
    tickWidth: float
    ticks: bool
    title: str | None
    titleColor: str
    titleFit: Literal["point", "range"]
    titleFont: str
    titleFontSize: float
    titleFontStyle: FontStyle_T
    titleFontWeight: FontWeight_T
    titleOpacity: float
    titlePadding: float
    values: Sequence[Any]
    zindex: float


class BindCheckboxKwds(TypedDict, total=False):
    """TypedDict helper for raw ``BindCheckbox`` mappings."""

    debounce: float
    description: str
    input: Literal["checkbox"]
    name: str


class BindInputKwds(TypedDict, total=False):
    """TypedDict helper for raw ``BindInput`` mappings."""

    autocomplete: str
    debounce: float
    description: str
    input: Literal["text", "number", "color"]
    name: str
    placeholder: str


class BindRadioSelectKwds(TypedDict, total=False):
    """TypedDict helper for raw ``BindRadioSelect`` mappings."""

    debounce: float
    description: str
    input: Literal["radio", "select"]
    labels: Sequence[str]
    name: str
    options: Sequence[Any]


class BindRangeKwds(TypedDict, total=False):
    """TypedDict helper for raw ``BindRange`` mappings."""

    debounce: float
    description: str
    input: Literal["range"]
    max: float
    min: float
    name: str
    step: float


class CompareParamsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``CompareParams`` mappings."""

    field: Sequence[Field_T] | Field_T
    order: Sequence[SortOrder_T] | SortOrder_T


class DataFormatKwds(TypedDict, total=False):
    """TypedDict helper for raw ``DataFormat`` mappings."""

    columns: Sequence[str]
    delimiter: str
    parse: Parse | ParseKwds | None
    property: str
    type: str


class DynamicOpacityKwds(TypedDict, total=False):
    """TypedDict helper for raw ``DynamicOpacity`` mappings."""

    channel: PrimaryPositionalChannel_T | Literal["auto"]
    unitsPerPixel: Sequence[float | ExprRef | dict[str, Any]]
    values: Sequence[float]


class EncodingKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Encoding`` mappings."""

    angle: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    color: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
    )
    direction: DirectionDef | dict[str, Any]
    dx: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef
    )
    dy: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
        | MarkPropExprDef
    )
    facetIndex: FieldDefWithoutScale | dict[str, Any]
    fill: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
    )
    fillOpacity: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    key: (
        FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]]
    )
    opacity: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    sample: FieldDefWithoutScale | dict[str, Any]
    search: (
        FieldDefWithoutScale
        | dict[str, Any]
        | Sequence[FieldDefWithoutScale | dict[str, Any]]
    )
    semanticScore: dict[str, Any]
    shape: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullTypeForShape
    )
    size: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    stroke: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefStringNull
        | ValueDefWithConditionStringNullType
    )
    strokeOpacity: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    strokeWidth: (
        FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber
        | dict[str, Any]
        | FieldOrDatumDefWithConditionScaleDatumDefNumber
        | ValueDefWithConditionNumberType
    )
    text: StringFieldDef | dict[str, Any] | StringDatumDef | ExprDef | ValueDefString
    tooltip: (
        StringFieldDef
        | dict[str, Any]
        | StringDatumDef
        | ExprDef
        | ValueDefString
        | Sequence[
            StringFieldDef | dict[str, Any] | StringDatumDef | ExprDef | ValueDefString
        ]
        | None
    )
    uniqueId: FieldDefWithoutScale | dict[str, Any]
    x: dict[str, Any]
    x2: Position2Def | dict[str, Any] | None
    y: (
        PositionFieldDef
        | dict[str, Any]
        | ChromPosDef
        | PositionDatumDef
        | PositionExprDef
        | ValueDefNumber
    )
    y2: Position2Def | dict[str, Any] | None


class EventConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``EventConfig`` mappings."""

    filter: str
    type: DomEventType_T


class GenomeAxisKwds(TypedDict, total=False):
    """TypedDict helper for raw ``GenomeAxis`` mappings."""

    chromGrid: bool
    chromGridCap: Literal["butt", "round", "square"]
    chromGridColor: str
    chromGridDash: Sequence[float]
    chromGridDashOffset: float
    chromGridFillEven: str
    chromGridFillOdd: str
    chromGridOpacity: float
    chromGridWidth: float
    chromLabelAlign: Align_T
    chromLabelColor: str
    chromLabelFont: str
    chromLabelFontSize: float
    chromLabelFontStyle: FontStyle_T
    chromLabelFontWeight: FontWeight_T
    chromLabelPadding: float
    chromLabels: bool
    chromTickColor: str
    chromTickDash: Sequence[float]
    chromTickDashOffset: float
    chromTickSize: float
    chromTickWidth: float
    chromTicks: bool
    domain: bool
    domainCap: Literal["butt", "round", "square"]
    domainColor: str
    domainDash: Sequence[float]
    domainDashOffset: float
    domainWidth: float
    format: str
    grid: bool
    gridCap: Literal["butt", "round", "square"]
    gridColor: str
    gridDash: Sequence[float]
    gridDashOffset: float
    gridOpacity: float
    gridWidth: float
    labelAlign: Align_T
    labelAngle: float
    labelBaseline: Baseline_T
    labelColor: str
    labelFont: str
    labelFontSize: float
    labelFontStyle: FontStyle_T
    labelFontWeight: FontWeight_T
    labelLimit: float
    labelPadding: float
    labels: bool
    maxExtent: float
    minExtent: float
    offset: float
    orient: AxisOrient_T
    placement: AxisPlacement_T
    style: str | Sequence[str] | None
    tickCap: Literal["butt", "round", "square"]
    tickColor: str
    tickCount: float | ExprRef | dict[str, Any]
    tickDash: Sequence[float]
    tickDashOffset: float
    tickMinStep: float
    tickSize: float
    tickWidth: float
    ticks: bool
    title: str | None
    titleColor: str
    titleFit: Literal["point", "range"]
    titleFont: str
    titleFontSize: float
    titleFontStyle: FontStyle_T
    titleFontWeight: FontWeight_T
    titleOpacity: float
    titlePadding: float
    values: Sequence[Any]
    zindex: float


class GenomeSpyConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``GenomeSpyConfig`` mappings."""

    arrow: ArrowConfig | dict[str, Any]
    axis: AxisConfig | AxisConfigKwds
    axisBottom: AxisConfig | AxisConfigKwds
    axisIndex: AxisConfig | AxisConfigKwds
    axisLeft: AxisConfig | AxisConfigKwds
    axisLocus: AxisConfig | AxisConfigKwds
    axisNominal: AxisConfig | AxisConfigKwds
    axisOrdinal: AxisConfig | AxisConfigKwds
    axisQuantitative: AxisConfig | AxisConfigKwds
    axisRight: AxisConfig | AxisConfigKwds
    axisTop: AxisConfig | AxisConfigKwds
    axisX: AxisConfig | AxisConfigKwds
    axisY: AxisConfig | AxisConfigKwds
    legend: LegendConfig | LegendConfigKwds
    legendTrack: LegendConfig | LegendConfigKwds
    link: LinkConfig | LinkConfigKwds
    mark: MarkConfig | MarkConfigKwds
    point: PointConfig | PointConfigKwds
    range: RangeConfig | RangeConfigKwds
    rect: RectConfig | RectConfigKwds
    rule: RuleConfig | RuleConfigKwds
    scale: ScaleConfig | ScaleConfigKwds
    style: dict[str, Any]
    text: TextConfig | TextConfigKwds
    tick: TickConfig | dict[str, Any]
    title: TitleConfig | TitleConfigKwds
    view: ViewConfig | ViewConfigKwds


class HandledTooltipKwds(TypedDict, total=False):
    """TypedDict helper for raw ``HandledTooltip`` mappings."""

    handler: str
    params: dict[str, Any]


class LegendKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Legend`` mappings."""

    backgroundFill: str
    backgroundFillOpacity: float
    backgroundStroke: str
    backgroundStrokeOpacity: float
    backgroundStrokeWidth: float
    columns: float
    direction: LegendDirection_T
    labelLimit: float
    offset: float
    orient: LegendOrient_T | ExprRef | dict[str, Any]
    padding: float
    style: str | Sequence[str] | None
    symbolSize: float
    symbolType: str
    title: str | None
    titleOrient: LegendTitleOrient_T
    values: Sequence[str | float | bool]


class LegendConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``LegendConfig`` mappings."""

    backgroundFill: str
    backgroundFillOpacity: float
    backgroundStroke: str
    backgroundStrokeOpacity: float
    backgroundStrokeWidth: float
    columnPadding: float
    columns: float
    direction: LegendDirection_T
    disable: bool | ExprRef | dict[str, Any]
    labelAlign: Align_T
    labelBaseline: Baseline_T
    labelColor: str
    labelFont: str
    labelFontSize: float
    labelFontStyle: FontStyle_T
    labelFontWeight: FontWeight_T
    labelLimit: float
    labelOffset: float
    offset: float
    orient: LegendOrient_T | ExprRef | dict[str, Any]
    padding: float
    rowPadding: float
    spacing: float
    style: str | Sequence[str] | None
    symbolBaseFillColor: str
    symbolBaseStrokeColor: str
    symbolOffset: float
    symbolSize: float
    symbolStrokeWidth: float
    symbolType: str
    title: str | None
    titleColor: str
    titleFont: str
    titleFontSize: float
    titleFontStyle: FontStyle_T
    titleFontWeight: FontWeight_T
    titleLimit: float
    titleOrient: LegendTitleOrient_T
    titlePadding: float
    values: Sequence[str | float | bool]


class LinkConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``LinkConfig`` mappings."""

    arcFadingDistance: Sequence[float] | Literal[False] | ExprRef | dict[str, Any]
    arcHeightFactor: float | ExprRef | dict[str, Any]
    buildIndex: bool
    clampApex: bool | ExprRef | dict[str, Any]
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    linkShape: (
        Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | ExprRef
        | dict[str, Any]
    )
    maxChordLength: float | ExprRef | dict[str, Any]
    minArcHeight: float | ExprRef | dict[str, Any]
    minBufferSize: float
    minPickingSize: float | ExprRef | dict[str, Any]
    noFadingOnPointSelection: bool | ExprRef | dict[str, Any]
    opacity: float | ExprRef | dict[str, Any]
    orient: Literal["vertical"] | Literal["horizontal"] | ExprRef | dict[str, Any]
    segments: float | ExprRef | dict[str, Any]
    size: float | ExprRef | dict[str, Any]
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    x: float | ExprRef | dict[str, Any]
    x2: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    y2: float | ExprRef | dict[str, Any]
    yOffset: float


class MarkConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``MarkConfig`` mappings."""

    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    minBufferSize: float
    opacity: float | ExprRef | dict[str, Any]
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    x: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    yOffset: float


class PaddingsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Paddings`` mappings."""

    bottom: float
    left: float
    right: float
    top: float


class ParameterKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Parameter`` mappings."""

    bind: (
        BindCheckbox
        | BindCheckboxKwds
        | BindRadioSelect
        | BindRadioSelectKwds
        | BindRange
        | BindRangeKwds
        | BindInput
        | BindInputKwds
    )
    description: str
    expr: str
    name: str
    persist: bool
    push: Literal["outer"]
    ruler: RulerConfig | RulerConfigKwds
    select: (
        SelectionType_T
        | PointSelectionConfig
        | dict[str, Any]
        | IntervalSelectionConfig
    )
    transition: LerpTransition | dict[str, Any]
    value: RulerInitMapping | dict[str, Any]


class ParseKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Parse`` mappings."""

    pass


class PointConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``PointConfig`` mappings."""

    angle: float | ExprRef | dict[str, Any]
    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    dx: float | ExprRef | dict[str, Any]
    dy: float | ExprRef | dict[str, Any]
    fill: str | ExprRef | dict[str, Any]
    fillGradientStrength: float | ExprRef | dict[str, Any]
    fillOpacity: float | ExprRef | dict[str, Any]
    filled: bool
    geometricZoomBound: float
    inwardStroke: bool | ExprRef | dict[str, Any]
    minBufferSize: float
    minPickingSize: float | ExprRef | dict[str, Any]
    opacity: float | ExprRef | dict[str, Any]
    sampleFacetPadding: float
    semanticScore: float | ExprRef | dict[str, Any]
    semanticZoomFraction: float | ExprRef | dict[str, Any]
    shape: str | ExprRef | dict[str, Any]
    size: float | ExprRef | dict[str, Any]
    stroke: str | ExprRef | dict[str, Any]
    strokeOpacity: float | ExprRef | dict[str, Any]
    strokeWidth: float | ExprRef | dict[str, Any]
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    x: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    yOffset: float


class RangeConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RangeConfig`` mappings."""

    angle: Sequence[float]
    diverging: str | SchemeParams | SchemeParamsKwds
    heatmap: str | SchemeParams | SchemeParamsKwds
    ramp: str | SchemeParams | SchemeParamsKwds
    shape: Sequence[str]
    size: Sequence[float]


class RectConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RectConfig`` mappings."""

    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cornerRadius: float | ExprRef | dict[str, Any]
    cornerRadiusBottomLeft: float | ExprRef | dict[str, Any]
    cornerRadiusBottomRight: float | ExprRef | dict[str, Any]
    cornerRadiusTopLeft: float | ExprRef | dict[str, Any]
    cornerRadiusTopRight: float | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    fill: str | ExprRef | dict[str, Any]
    fillOpacity: float | ExprRef | dict[str, Any]
    filled: bool
    hatch: (
        Literal["none"]
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
    )
    minBufferSize: float
    minHeight: float | ExprRef | dict[str, Any]
    minOpacity: float | ExprRef | dict[str, Any]
    minWidth: float | ExprRef | dict[str, Any]
    opacity: float | ExprRef | dict[str, Any]
    shadowBlur: float | ExprRef | dict[str, Any]
    shadowColor: str | ExprRef | dict[str, Any]
    shadowOffsetX: float | ExprRef | dict[str, Any]
    shadowOffsetY: float | ExprRef | dict[str, Any]
    shadowOpacity: float | ExprRef | dict[str, Any]
    stroke: str | ExprRef | dict[str, Any]
    strokeOpacity: float | ExprRef | dict[str, Any]
    strokeWidth: float | ExprRef | dict[str, Any]
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    x: float | ExprRef | dict[str, Any]
    x2: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    y2: float | ExprRef | dict[str, Any]
    yOffset: float


class RuleConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RuleConfig`` mappings."""

    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    minBufferSize: float
    minLength: float | ExprRef | dict[str, Any]
    opacity: float | ExprRef | dict[str, Any]
    size: float | ExprRef | dict[str, Any]
    strokeCap: (
        Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
    )
    strokeDash: Sequence[float]
    strokeDashOffset: float
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    x: float | ExprRef | dict[str, Any]
    x2: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    y2: float | ExprRef | dict[str, Any]
    yOffset: float


class RulerConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RulerConfig`` mappings."""

    clear: RulerClear_T
    display: RulerDisplay_T
    encodings: Sequence[PrimaryPositionalChannel_T]
    extent: RulerExtent_T
    mark: RulerMarkConfig | RulerMarkConfigKwds
    on: RulerEventType_T | RulerEventConfig | RulerEventConfigKwds | str
    snap: RulerSnap_T
    source: RulerSource_T


class RulerEventConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RulerEventConfig`` mappings."""

    filter: str
    type: RulerEventType_T


class RulerMarkConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``RulerMarkConfig`` mappings."""

    fill: str
    fillOpacity: float
    opacity: float
    shadowBlur: float | ExprRef | dict[str, Any]
    shadowColor: str | ExprRef | dict[str, Any]
    shadowOffsetX: float | ExprRef | dict[str, Any]
    shadowOffsetY: float | ExprRef | dict[str, Any]
    shadowOpacity: float | ExprRef | dict[str, Any]
    stroke: str
    strokeDash: Sequence[float]
    strokeWidth: float
    zindex: float


class ScaleKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Scale`` mappings."""

    align: float
    assembly: str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition
    base: float
    bins: Sequence[float]
    clamp: bool
    constant: float
    domain: (
        ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]]
    )
    domainMax: float
    domainMid: float
    domainMin: float
    domainTransition: bool | dict[str, Any]
    exponent: float
    interpolate: (
        ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds
    )
    name: str
    nice: bool | float | dict[str, Any]
    numberingOffset: float
    padding: float
    paddingInner: float
    paddingOuter: float
    range: Sequence[float | str | ExprRef | dict[str, Any]] | str
    reverse: bool
    round: bool
    scheme: str | SchemeParams | SchemeParamsKwds
    type: ScaleType_T
    zero: bool
    zoom: bool | ZoomParams | ZoomParamsKwds


class ScaleConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``ScaleConfig`` mappings."""

    align: float
    assembly: str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition
    base: float
    bins: Sequence[float]
    clamp: bool
    constant: float
    domain: (
        ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | SelectionDomainRef
        | dict[str, Any]
        | ExprRef
        | Sequence[float | str | bool | ExprRef | dict[str, Any]]
    )
    domainMax: float
    domainMid: float
    domainMin: float
    domainTransition: bool | dict[str, Any]
    exponent: float
    index: dict[str, Any]
    interpolate: (
        ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds
    )
    locus: dict[str, Any]
    name: str
    nice: bool | float | dict[str, Any]
    nominal: dict[str, Any]
    nominalColorScheme: str | SchemeParams | SchemeParamsKwds
    numberingOffset: float
    ordinal: dict[str, Any]
    ordinalColorScheme: str | SchemeParams | SchemeParamsKwds
    padding: float
    paddingInner: float
    paddingOuter: float
    quantitative: dict[str, Any]
    quantitativeColorScheme: str | SchemeParams | SchemeParamsKwds
    range: Sequence[float | str | ExprRef | dict[str, Any]] | str
    reverse: bool
    round: bool
    scheme: str | SchemeParams | SchemeParamsKwds
    type: ScaleType_T
    zero: bool
    zoom: bool | ZoomParams | ZoomParamsKwds


class ScaleInterpolateParamsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``ScaleInterpolateParams`` mappings."""

    gamma: float
    type: Literal["rgb", "cubehelix", "cubehelix-long"]


class SchemeParamsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``SchemeParams`` mappings."""

    count: float
    extent: Sequence[float]
    name: str


class SeparatorPropsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``SeparatorProps`` mappings."""

    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    includePlotMargin: bool
    minBufferSize: float
    minLength: float | ExprRef | dict[str, Any]
    opacity: float | ExprRef | dict[str, Any]
    size: float | ExprRef | dict[str, Any]
    strokeCap: (
        Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | ExprRef
        | dict[str, Any]
    )
    strokeDash: Sequence[float]
    strokeDashOffset: float
    style: str | Sequence[str]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    type: Literal["rule"]
    x: float | ExprRef | dict[str, Any]
    x2: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    y2: float | ExprRef | dict[str, Any]
    yOffset: float
    zindex: float


class SizeDefKwds(TypedDict, total=False):
    """TypedDict helper for raw ``SizeDef`` mappings."""

    grow: float
    maxPx: float
    minPx: float
    px: float


class StepKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Step`` mappings."""

    step: float | ExprRef | dict[str, Any]


class TextConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``TextConfig`` mappings."""

    align: Align_T
    angle: float | ExprRef | dict[str, Any]
    baseline: Baseline_T
    buildIndex: bool
    clip: bool | Literal["x"] | Literal["y"] | Literal["never"]
    color: str | ExprRef | dict[str, Any]
    cullByVisibleRange: bool | Literal["x"] | Literal["y"]
    cursor: str | ExprRef | dict[str, Any]
    dx: float
    dy: float
    fitToBand: bool | ExprRef | dict[str, Any]
    flushX: bool | ExprRef | dict[str, Any]
    flushY: bool | ExprRef | dict[str, Any]
    font: str
    fontStyle: FontStyle_T
    fontWeight: FontWeight_T
    logoLetters: bool | ExprRef | dict[str, Any]
    minBufferSize: float
    opacity: float | ExprRef | dict[str, Any]
    paddingX: float | ExprRef | dict[str, Any]
    paddingY: float | ExprRef | dict[str, Any]
    size: float | ExprRef | dict[str, Any]
    squeeze: bool | ExprRef | dict[str, Any]
    style: str | Sequence[str]
    text: Scalar_T | ExprRef | dict[str, Any]
    tooltip: HandledTooltip | HandledTooltipKwds | None | Literal[False]
    viewportEdgeFadeDistanceBottom: float
    viewportEdgeFadeDistanceLeft: float
    viewportEdgeFadeDistanceRight: float
    viewportEdgeFadeDistanceTop: float
    viewportEdgeFadeWidthBottom: float
    viewportEdgeFadeWidthLeft: float
    viewportEdgeFadeWidthRight: float
    viewportEdgeFadeWidthTop: float
    x: float | ExprRef | dict[str, Any]
    x2: float | ExprRef | dict[str, Any]
    xOffset: float
    y: float | ExprRef | dict[str, Any]
    y2: float | ExprRef | dict[str, Any]
    yOffset: float


class TitleKwds(TypedDict, total=False):
    """TypedDict helper for raw ``Title`` mappings."""

    align: Align_T
    anchor: TitleAnchor_T
    angle: float | ExprRef | dict[str, Any]
    baseline: Baseline_T
    color: str | ExprRef | dict[str, Any]
    dx: float
    dy: float
    font: str
    fontSize: float | ExprRef | dict[str, Any]
    fontStyle: FontStyle_T
    fontWeight: FontWeight_T
    frame: TitleFrame_T
    offset: float
    orient: TitleOrient_T
    reserve: bool
    style: str | Sequence[str]
    subtitle: str | ExprRef | dict[str, Any]
    subtitleColor: str | ExprRef | dict[str, Any]
    subtitleFont: str
    subtitleFontSize: float | ExprRef | dict[str, Any]
    subtitleFontStyle: FontStyle_T
    subtitleFontWeight: FontWeight_T
    subtitlePadding: float
    text: str | ExprRef | dict[str, Any]
    zindex: float


class TitleConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``TitleConfig`` mappings."""

    align: Align_T
    anchor: TitleAnchor_T
    angle: float | ExprRef | dict[str, Any]
    baseline: Baseline_T
    color: str | ExprRef | dict[str, Any]
    dx: float
    dy: float
    font: str
    fontSize: float | ExprRef | dict[str, Any]
    fontStyle: FontStyle_T
    fontWeight: FontWeight_T
    frame: TitleFrame_T
    offset: float
    orient: TitleOrient_T
    reserve: bool
    style: str | Sequence[str]
    subtitle: str | ExprRef | dict[str, Any]
    subtitleColor: str | ExprRef | dict[str, Any]
    subtitleFont: str
    subtitleFontSize: float | ExprRef | dict[str, Any]
    subtitleFontStyle: FontStyle_T
    subtitleFontWeight: FontWeight_T
    subtitlePadding: float
    zindex: float


class ViewBackgroundKwds(TypedDict, total=False):
    """TypedDict helper for raw ``ViewBackground`` mappings."""

    fill: str
    fillOpacity: float
    shadowBlur: float | ExprRef | dict[str, Any]
    shadowColor: str | ExprRef | dict[str, Any]
    shadowOffsetX: float | ExprRef | dict[str, Any]
    shadowOffsetY: float | ExprRef | dict[str, Any]
    shadowOpacity: float | ExprRef | dict[str, Any]
    stroke: str
    strokeOpacity: float
    strokeWidth: float
    strokeZindex: float
    style: str | Sequence[str]
    zindex: float


class ViewConfigKwds(TypedDict, total=False):
    """TypedDict helper for raw ``ViewConfig`` mappings."""

    continuousHeight: float
    continuousWidth: float
    discreteHeight: float | Step | StepKwds
    discreteWidth: float | Step | StepKwds
    fill: str
    fillOpacity: float
    shadowBlur: float | ExprRef | dict[str, Any]
    shadowColor: str | ExprRef | dict[str, Any]
    shadowOffsetX: float | ExprRef | dict[str, Any]
    shadowOffsetY: float | ExprRef | dict[str, Any]
    shadowOpacity: float | ExprRef | dict[str, Any]
    step: float | ExprRef | dict[str, Any]
    stroke: str
    strokeOpacity: float
    strokeWidth: float
    strokeZindex: float
    zindex: float


class ZoomParamsKwds(TypedDict, total=False):
    """TypedDict helper for raw ``ZoomParams`` mappings."""

    extent: (
        ScalarDomain_T
        | Sequence[ChromosomalLocus | dict[str, Any]]
        | Literal["data"]
        | Literal["unbounded"]
    )


class AxesKwds(TypedDict, total=False):
    """TypedDict helper for composed-view axis resolution mappings."""

    x: GenomeAxis | GenomeAxisKwds
    y: GenomeAxis | GenomeAxisKwds


class LegendsKwds(TypedDict, total=False):
    """TypedDict helper for composed-view legend resolution mappings."""

    angle: Legend | LegendKwds
    color: Legend | LegendKwds
    dx: Legend | LegendKwds
    dy: Legend | LegendKwds
    fill: Legend | LegendKwds
    fillOpacity: Legend | LegendKwds
    opacity: Legend | LegendKwds
    shape: Legend | LegendKwds
    size: Legend | LegendKwds
    stroke: Legend | LegendKwds
    strokeOpacity: Legend | LegendKwds
    strokeWidth: Legend | LegendKwds


class ScalesKwds(TypedDict, total=False):
    """TypedDict helper for composed-view scale resolution mappings."""

    angle: Scale | ScaleKwds
    color: Scale | ScaleKwds
    dx: Scale | ScaleKwds
    dy: Scale | ScaleKwds
    fill: Scale | ScaleKwds
    fillOpacity: Scale | ScaleKwds
    opacity: Scale | ScaleKwds
    shape: Scale | ScaleKwds
    size: Scale | ScaleKwds
    stroke: Scale | ScaleKwds
    strokeOpacity: Scale | ScaleKwds
    strokeWidth: Scale | ScaleKwds
    x: Scale | ScaleKwds
    x2: Scale | ScaleKwds
    y: Scale | ScaleKwds
    y2: Scale | ScaleKwds


class AxisResolveKwds(TypedDict, total=False):
    """TypedDict helper for axis resolution behavior mappings."""

    angle: ResolutionBehavior_T
    color: ResolutionBehavior_T
    default: ResolutionBehavior_T
    dx: ResolutionBehavior_T
    dy: ResolutionBehavior_T
    facetIndex: ResolutionBehavior_T
    fill: ResolutionBehavior_T
    fillOpacity: ResolutionBehavior_T
    key: ResolutionBehavior_T
    opacity: ResolutionBehavior_T
    sample: ResolutionBehavior_T
    search: ResolutionBehavior_T
    semanticScore: ResolutionBehavior_T
    shape: ResolutionBehavior_T
    size: ResolutionBehavior_T
    stroke: ResolutionBehavior_T
    strokeOpacity: ResolutionBehavior_T
    strokeWidth: ResolutionBehavior_T
    text: ResolutionBehavior_T
    uniqueId: ResolutionBehavior_T
    x: ResolutionBehavior_T
    x2: ResolutionBehavior_T
    y: ResolutionBehavior_T
    y2: ResolutionBehavior_T


class LegendResolveKwds(TypedDict, total=False):
    """TypedDict helper for legend resolution behavior mappings."""

    angle: ResolutionBehavior_T
    color: ResolutionBehavior_T
    default: ResolutionBehavior_T
    dx: ResolutionBehavior_T
    dy: ResolutionBehavior_T
    facetIndex: ResolutionBehavior_T
    fill: ResolutionBehavior_T
    fillOpacity: ResolutionBehavior_T
    key: ResolutionBehavior_T
    opacity: ResolutionBehavior_T
    sample: ResolutionBehavior_T
    search: ResolutionBehavior_T
    semanticScore: ResolutionBehavior_T
    shape: ResolutionBehavior_T
    size: ResolutionBehavior_T
    stroke: ResolutionBehavior_T
    strokeOpacity: ResolutionBehavior_T
    strokeWidth: ResolutionBehavior_T
    text: ResolutionBehavior_T
    uniqueId: ResolutionBehavior_T
    x: ResolutionBehavior_T
    x2: ResolutionBehavior_T
    y: ResolutionBehavior_T
    y2: ResolutionBehavior_T


class ScaleResolveKwds(TypedDict, total=False):
    """TypedDict helper for scale resolution behavior mappings."""

    angle: ResolutionBehavior_T
    color: ResolutionBehavior_T
    default: ResolutionBehavior_T
    dx: ResolutionBehavior_T
    dy: ResolutionBehavior_T
    facetIndex: ResolutionBehavior_T
    fill: ResolutionBehavior_T
    fillOpacity: ResolutionBehavior_T
    key: ResolutionBehavior_T
    opacity: ResolutionBehavior_T
    sample: ResolutionBehavior_T
    search: ResolutionBehavior_T
    semanticScore: ResolutionBehavior_T
    shape: ResolutionBehavior_T
    size: ResolutionBehavior_T
    stroke: ResolutionBehavior_T
    strokeOpacity: ResolutionBehavior_T
    strokeWidth: ResolutionBehavior_T
    text: ResolutionBehavior_T
    uniqueId: ResolutionBehavior_T
    x: ResolutionBehavior_T
    x2: ResolutionBehavior_T
    y: ResolutionBehavior_T
    y2: ResolutionBehavior_T


class ResolveKwds(TypedDict, total=False):
    """TypedDict helper for composed-view resolution mappings."""

    axis: AxisResolveKwds
    legend: LegendResolveKwds
    scale: ScaleResolveKwds


__all__ = [
    "AxisKwds",
    "AxisConfigKwds",
    "BindCheckboxKwds",
    "BindInputKwds",
    "BindRadioSelectKwds",
    "BindRangeKwds",
    "CompareParamsKwds",
    "DataFormatKwds",
    "DynamicOpacityKwds",
    "EncodingKwds",
    "EventConfigKwds",
    "GenomeAxisKwds",
    "GenomeSpyConfigKwds",
    "HandledTooltipKwds",
    "LegendKwds",
    "LegendConfigKwds",
    "LinkConfigKwds",
    "MarkConfigKwds",
    "PaddingsKwds",
    "ParameterKwds",
    "ParseKwds",
    "PointConfigKwds",
    "RangeConfigKwds",
    "RectConfigKwds",
    "RuleConfigKwds",
    "RulerConfigKwds",
    "RulerEventConfigKwds",
    "RulerMarkConfigKwds",
    "ScaleKwds",
    "ScaleConfigKwds",
    "ScaleInterpolateParamsKwds",
    "SchemeParamsKwds",
    "SeparatorPropsKwds",
    "SizeDefKwds",
    "StepKwds",
    "TextConfigKwds",
    "TitleKwds",
    "TitleConfigKwds",
    "ViewBackgroundKwds",
    "ViewConfigKwds",
    "ZoomParamsKwds",
    "AxesKwds",
    "LegendsKwds",
    "ScalesKwds",
    "AxisResolveKwds",
    "LegendResolveKwds",
    "ScaleResolveKwds",
    "ResolveKwds",
]
