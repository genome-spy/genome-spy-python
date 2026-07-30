"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import TypeAlias, Literal

AggregateOp_T: TypeAlias = Literal[
    "count", "valid", "sum", "min", "max", "mean", "q1", "median", "q3", "variance"
]
Align_T: TypeAlias = Literal["left", "center", "right"]
ArrowDirection_T: TypeAlias = Literal["forward", "reverse"]
AxisOrient_T: TypeAlias = Literal["top", "bottom", "left", "right"]
AxisPlacement_T: TypeAlias = Literal["outside", "inside"]
Baseline_T: TypeAlias = Literal["top", "middle", "bottom", "alphabetic", "baseline"]
BuiltInThemeName_T: TypeAlias = Literal[
    "genomespy", "vegalite", "quartz", "dark", "fivethirtyeight", "urbaninstitute"
]
FieldName_T: TypeAlias = str
Field_T: TypeAlias = str
FontStyle_T: TypeAlias = Literal["normal", "italic"]
FontWeight_T: TypeAlias = (
    float
    | Literal["thin"]
    | Literal["light"]
    | Literal["regular"]
    | Literal["normal"]
    | Literal["medium"]
    | Literal["bold"]
    | Literal["black"]
)
InteractionEventType_T: TypeAlias = Literal[
    "click",
    "dblclick",
    "mouseenter",
    "mouseleave",
    "mouseover",
    "mousemove",
    "mousedown",
    "wheel",
]
DomEventType_T: TypeAlias = InteractionEventType_T | Literal["pointerover"]
LegendDirection_T: TypeAlias = Literal["vertical", "horizontal"]
LegendOrient_T: TypeAlias = Literal[
    "left",
    "right",
    "top",
    "bottom",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
]
LegendTitleOrient_T: TypeAlias = Literal["top", "bottom", "left", "right"]
MarkType_T: TypeAlias = Literal[
    "rect", "point", "rule", "tick", "text", "link", "arrow"
]
NumericDomain_T: TypeAlias = Sequence[float]
ParseValue_T: TypeAlias = str | None
PrimaryPositionalChannel_T: TypeAlias = Literal["x", "y"]
ResolutionBehavior_T: TypeAlias = Literal["independent", "shared", "excluded", "forced"]
RulerClear_T: TypeAlias = Literal["mouseleave", "mouseup", False]
RulerDisplay_T: TypeAlias = Literal["line", "center", "band", "none"]
RulerEventType_T: TypeAlias = Literal["mousemove", "mousedown"]
RulerExtent_T: TypeAlias = Literal["auto", "view", "container"]
RulerSnap_T: TypeAlias = Literal["auto", "integer", False]
RulerSource_T: TypeAlias = Literal["pointer", "viewport"]
ScalarDomain_T: TypeAlias = NumericDomain_T | Sequence[str] | Sequence[bool]
Scalar_T: TypeAlias = str | float | bool
ScaleInterpolate_T: TypeAlias = Literal[
    "rgb", "lab", "hcl", "hsl", "hsl-long", "hcl-long", "cubehelix", "cubehelix-long"
]
ScaleType_T: TypeAlias = Literal[
    "null",
    "linear",
    "log",
    "pow",
    "sqrt",
    "symlog",
    "identity",
    "sequential",
    "quantize",
    "threshold",
    "ordinal",
    "point",
    "band",
    "index",
    "locus",
]
SecondaryPositionalChannel_T: TypeAlias = Literal["x2", "y2"]
PositionalChannel_T: TypeAlias = (
    PrimaryPositionalChannel_T | SecondaryPositionalChannel_T
)
ChannelWithScale_T: TypeAlias = (
    PositionalChannel_T
    | Literal["color"]
    | Literal["fill"]
    | Literal["stroke"]
    | Literal["opacity"]
    | Literal["fillOpacity"]
    | Literal["strokeOpacity"]
    | Literal["strokeWidth"]
    | Literal["size"]
    | Literal["shape"]
    | Literal["direction"]
    | Literal["angle"]
    | Literal["dx"]
    | Literal["dy"]
)
SelectionExtent_T: TypeAlias = Literal["auto", "view", "container"]
SelectionType_T: TypeAlias = Literal["point", "interval"]
SortOrder_T: TypeAlias = Literal["ascending", "descending"]
TitleAnchor_T: TypeAlias = Literal[None, "start", "middle", "end"]
TitleFrame_T: TypeAlias = Literal["bounds", "group"]
TitleOrient_T: TypeAlias = Literal["none", "left", "right", "top", "bottom"]
TypeForShape_T: TypeAlias = Literal["ordinal", "nominal"]
Type_T: TypeAlias = Literal["quantitative", "ordinal", "nominal", "index", "locus"]
WindowOnlyOp_T: TypeAlias = Literal[
    "row_number",
    "rank",
    "dense_rank",
    "percent_rank",
    "cume_dist",
    "ntile",
    "lag",
    "lead",
    "first_value",
    "last_value",
    "nth_value",
    "prev_value",
    "next_value",
]
WindowOp_T: TypeAlias = WindowOnlyOp_T | AggregateOp_T

__all__ = [
    "AggregateOp_T",
    "Align_T",
    "ArrowDirection_T",
    "AxisOrient_T",
    "AxisPlacement_T",
    "Baseline_T",
    "BuiltInThemeName_T",
    "FieldName_T",
    "Field_T",
    "FontStyle_T",
    "FontWeight_T",
    "InteractionEventType_T",
    "DomEventType_T",
    "LegendDirection_T",
    "LegendOrient_T",
    "LegendTitleOrient_T",
    "MarkType_T",
    "NumericDomain_T",
    "ParseValue_T",
    "PrimaryPositionalChannel_T",
    "ResolutionBehavior_T",
    "RulerClear_T",
    "RulerDisplay_T",
    "RulerEventType_T",
    "RulerExtent_T",
    "RulerSnap_T",
    "RulerSource_T",
    "ScalarDomain_T",
    "Scalar_T",
    "ScaleInterpolate_T",
    "ScaleType_T",
    "SecondaryPositionalChannel_T",
    "PositionalChannel_T",
    "ChannelWithScale_T",
    "SelectionExtent_T",
    "SelectionType_T",
    "SortOrder_T",
    "TitleAnchor_T",
    "TitleFrame_T",
    "TitleOrient_T",
    "TypeForShape_T",
    "Type_T",
    "WindowOnlyOp_T",
    "WindowOp_T",
]
