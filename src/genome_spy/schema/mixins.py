"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Self, Literal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genome_spy.channels import Channel

from genome_spy.schema._typing import (
    AggregateOp_T,
    Align_T,
    AxisOrient_T,
    AxisPlacement_T,
    Baseline_T,
    BuiltInThemeName_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    LegendDirection_T,
    LegendOrient_T,
    LegendResolutionBehavior_T,
    LegendTitleOrient_T,
    MarkType_T,
    PrimaryPositionalChannel_T,
    ResolutionBehavior_T,
    ScalarDomain_T,
    Scalar_T,
    ScaleInterpolate_T,
    ScaleType_T,
    TitleAnchor_T,
    TitleFrame_T,
    TitleOrient_T,
    WindowOp_T,
)
from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType
from genome_spy.schema import core
from genome_spy.schema._kwds import (
    AxesKwds,
    AxisConfigKwds,
    CompareParamsKwds,
    DynamicOpacityKwds,
    EncodingKwds,
    GenomeSpyConfigKwds,
    HandledTooltipKwds,
    LegendConfigKwds,
    LegendsKwds,
    LinkConfigKwds,
    MarkConfigKwds,
    PaddingsKwds,
    PointConfigKwds,
    RangeConfigKwds,
    RectConfigKwds,
    ResolveKwds,
    RuleConfigKwds,
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


class MarkMethodMixin:
    """Grammar-derived mark methods for the handwritten chart API."""

    def mark_rect(
        self,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadius: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minHeight: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOffsetY: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``rect``.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cornerRadius (float | ExprRef | dict[str, Any]): Radius of the rounded corners. **Default value:** ``0``
            cornerRadiusBottomLeft (float | ExprRef | dict[str, Any]): Radius of the bottom left rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusBottomRight (float | ExprRef | dict[str, Any]): Radius of the bottom right rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusTopLeft (float | ExprRef | dict[str, Any]): Radius of the top left rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusTopRight (float | ExprRef | dict[str, Any]): Radius of the top right rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            hatch (Literal['none'] | Literal['diagonal'] | Literal['antiDiagonal'] | Literal['cross'] | Literal['vertical'] | Literal['horizontal'] | Literal['grid'] | Literal['dots'] | Literal['rings'] | Literal['ringsLarge'] | ExprRef | dict[str, Any]): A hatch pattern drawn inside the mark using the stroke width, color, and opacity. The pattern is aligned in screen space and scaled by the stroke width. **Default value:** ``"none"``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minHeight (float | ExprRef | dict[str, Any]): The minimum height of a rectangle in pixels. The property clamps rectangles' heights. **Default value:** ``0``
            minOpacity (float | ExprRef | dict[str, Any]): Clamps the minimum size-dependent opacity. The property does not affect the ``opacity`` channel. Valid values are between ``0`` and ``1``. When a rectangle would be smaller than what is specified in ``minHeight`` and ``minWidth``, it is faded out proportionally. Example: a rectangle would be rendered as one pixel wide, but ``minWidth`` clamps it to five pixels. The rectangle is actually rendered as five pixels wide, but its opacity is multiplied by 0.2. With this setting, you can limit the factor to, for example, 0.5 to keep the rectangles more clearly visible. **Default value:** ``0``
            minWidth (float | ExprRef | dict[str, Any]): The minimum width of a rectangle in pixels. The property clamps rectangles' widths when the viewport is zoomed out. This property also reduces flickering of very narrow rectangles when zooming. The value should generally be at least one. **Default value:** ``1``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            shadowBlur (float | ExprRef | dict[str, Any]): The blur radius of the drop shadow in pixels. Higher values produce a more diffuse shadow. **Default value:** ``0``
            shadowColor (str | ExprRef | dict[str, Any]): The color of the drop shadow. Any valid CSS color string is allowed. **Default value:** ``"black"``
            shadowOffsetX (float | ExprRef | dict[str, Any]): The horizontal offset of the drop shadow in pixels. Positive values move the shadow to the right. **Default value:** ``0``
            shadowOffsetY (float | ExprRef | dict[str, Any]): The vertical offset of the drop shadow in pixels. Positive values move the shadow downward. **Default value:** ``0``
            shadowOpacity (float | ExprRef | dict[str, Any]): The opacity of the drop shadow. Value between ``0`` (fully transparent) and ``1`` (fully opaque). **Default value:** ``0`` (disabled)
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cornerRadius": cornerRadius,
            "cornerRadiusBottomLeft": cornerRadiusBottomLeft,
            "cornerRadiusBottomRight": cornerRadiusBottomRight,
            "cornerRadiusTopLeft": cornerRadiusTopLeft,
            "cornerRadiusTopRight": cornerRadiusTopRight,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "hatch": hatch,
            "minBufferSize": minBufferSize,
            "minHeight": minHeight,
            "minOpacity": minOpacity,
            "minWidth": minWidth,
            "opacity": opacity,
            "shadowBlur": shadowBlur,
            "shadowColor": shadowColor,
            "shadowOffsetX": shadowOffsetX,
            "shadowOffsetY": shadowOffsetY,
            "shadowOpacity": shadowOpacity,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("rect", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_point(
        self,
        *,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        inwardStroke: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        semanticScore: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        semanticZoomFraction: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shape: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``point``.

        Args:
            angle (float | ExprRef | dict[str, Any]): The rotation angle in degrees. **Default value:** ``0``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            dx (float | ExprRef | dict[str, Any]): Horizontal offset in pixels. **Default value:** ``0``
            dy (float | ExprRef | dict[str, Any]): Vertical offset in pixels. **Default value:** ``0``
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillGradientStrength (float | ExprRef | dict[str, Any]): Gradient strength controls the amount of the gradient eye-candy effect in the fill color. Valid values are between ``0`` and ``1``. **Default value:** ``0``
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            geometricZoomBound (float): Enables geometric zooming. The value is the base two logarithmic zoom level where the maximum point size is reached. **Default value:** ``0``
            inwardStroke (bool | ExprRef | dict[str, Any]): Should the stroke only grow inwards, e.g, the diameter/outline is not affected by the stroke width. Thus, a point that has a zero size has no visible stroke. This allows strokes to be used with geometric zoom, etc. **Default value:** ``false``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minPickingSize (float | ExprRef | dict[str, Any]): The minimum picking size invisibly increases the stroke width or point diameter of marks when pointing them with the mouse cursor, making it easier to select them. The valus is the minimum size in pixels. **Default value:** ``3.0`` for ``"link"`` and ``2.0`` for ``"point"``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            sampleFacetPadding (float): Additional padding used by sample facets. **Default value:** ``0.1``
            semanticScore (float | ExprRef | dict[str, Any]): The semantic score used by semantic zooming in the point mark. This is primarily intended for internal use. **Default value:** ``0``
            semanticZoomFraction (float | ExprRef | dict[str, Any]): TODO **Default value:** ``0.02``
            shape (str | ExprRef | dict[str, Any]): One of ``"circle"``, ``"square"``, ``"cross"``, ``"x"``, ``"+"``, ``"diamond"``, ``"triangle-up"``, ``"triangle-down"``, ``"triangle-right"``, ``"triangle-left"``, ``"tick-up"``, ``"tick-down"``, ``"tick-right"``, or ``"tick-left"``. The ``"x"`` and ``"+"`` shapes are stroke-only and use ``strokeWidth`` for their line thickness. **Default value:** ``"circle"``
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "angle": angle,
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "dx": dx,
            "dy": dy,
            "fill": fill,
            "fillGradientStrength": fillGradientStrength,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "geometricZoomBound": geometricZoomBound,
            "inwardStroke": inwardStroke,
            "minBufferSize": minBufferSize,
            "minPickingSize": minPickingSize,
            "opacity": opacity,
            "sampleFacetPadding": sampleFacetPadding,
            "semanticScore": semanticScore,
            "semanticZoomFraction": semanticZoomFraction,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("point", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_rule(
        self,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``rule``.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minLength (float | ExprRef | dict[str, Any]): The minimum stroke length in pixels. Use this property to ensure that very short strokes remain visible even when the user zooms out. **Default value:** ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            strokeCap (Literal['butt'] | Literal['square'] | Literal['round'] | ExprRef | dict[str, Any]): The style of stroke ends. Available choices: ``"butt"``, ``"round``", and ``"square"``. **Default value:** ``"butt"``
            strokeDash (Sequence[float]): An array of of alternating stroke and gap lengths or ``null`` for solid strokes. **Default value:** ``null``
            strokeDashOffset (float): An offset for the stroke dash pattern. **Default value:** ``0``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "minBufferSize": minBufferSize,
            "minLength": minLength,
            "opacity": opacity,
            "size": size,
            "strokeCap": strokeCap,
            "strokeDash": strokeDash,
            "strokeDashOffset": strokeDashOffset,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("rule", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_tick(
        self,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``tick``.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minLength (float | ExprRef | dict[str, Any]): The minimum stroke length in pixels. Use this property to ensure that very short strokes remain visible even when the user zooms out. **Default value:** ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            orient (Literal['vertical', 'horizontal']): The orientation of the tick mark. If omitted, GenomeSpy infers the orientation when one positional channel uses a band-like scale and the other does not, or when the orthogonal channel is omitted. Specify ``orient`` explicitly when both ``x`` and ``y`` use band-like scales. **Default value:** inferred
            strokeCap (Literal['butt'] | Literal['square'] | Literal['round'] | ExprRef | dict[str, Any]): The style of stroke ends. Available choices: ``"butt"``, ``"round``", and ``"square"``. **Default value:** ``"butt"``
            strokeDash (Sequence[float]): An array of of alternating stroke and gap lengths or ``null`` for solid strokes. **Default value:** ``null``
            strokeDashOffset (float): An offset for the stroke dash pattern. **Default value:** ``0``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            thickness (float): The thickness of the tick mark in pixels. Equivalent to the ``size`` of the underlying rule mark. **Default value:** ``1``
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "minBufferSize": minBufferSize,
            "minLength": minLength,
            "opacity": opacity,
            "orient": orient,
            "strokeCap": strokeCap,
            "strokeDash": strokeDash,
            "strokeDashOffset": strokeDashOffset,
            "style": style,
            "thickness": thickness,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("tick", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_text(
        self,
        *,
        align: Align_T | UndefinedType = Undefined,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        fitToBand: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        logoLetters: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingX: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        squeeze: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        text: Scalar_T | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``text``.

        Args:
            align (Align_T): The horizontal alignment of the text. One of ``"left"``, ``"center"``, or ``"right"``. **Default value:** ``"left"``
            angle (float | ExprRef | dict[str, Any]): The rotation angle in degrees. **Default value:** ``0``
            baseline (Baseline_T): The vertical alignment of the text. One of ``"top"``, ``"middle"``, ``"bottom"``. **Default value:** ``"bottom"``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            dx (float): The horizontal offset between the text and its anchor point, in pixels. Applied after the rotation by ``angle``.
            dy (float): The vertical offset between the text and its anchor point, in pixels. Applied after the rotation by ``angle``.
            fitToBand (bool | ExprRef | dict[str, Any]): If true, sets the secondary positional channel that allows the text to be squeezed (see the ``squeeze`` property). Can be used when: 1) ``"band"``, ``"index"``, or ``"locus"`` scale is being used and 2) only the primary positional channel is specified. **Default value:** ``false``
            flushX (bool | ExprRef | dict[str, Any]): If true, the text is kept inside the viewport when the range of ``x`` and ``x2`` intersect the viewport.
            flushY (bool | ExprRef | dict[str, Any]): If true, the text is kept inside the viewport when the range of ``y`` and ``y2`` intersect the viewport.
            font (str): The font typeface. GenomeSpy uses SDF versions of Google Fonts. Check their availability at the A-Frame Fonts repository. System fonts are **not** supported. **Default value:** ``"Lato"``
            fontStyle (FontStyle_T): The font style. Valid values: ``"normal"`` and ``"italic"``. **Default value:** ``"normal"``
            fontWeight (FontWeight_T): The font weight. The following strings and numbers are valid values: ``"thin"`` (``100``), ``"light"`` (``300``), ``"regular"`` (``400``), ``"normal"`` (``400``), ``"medium"`` (``500``), ``"bold"`` (``700``), ``"black"`` (``900``) **Default value:** ``"regular"``
            logoLetters (bool | ExprRef | dict[str, Any]): Stretch letters so that they can be used with sequence logos, etc...
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            paddingX (float | ExprRef | dict[str, Any]): The horizontal padding, in pixels, when the ``x2`` channel is used for ranged text. **Default value:** ``0``
            paddingY (float | ExprRef | dict[str, Any]): The vertical padding, in pixels, when the ``y2`` channel is used for ranged text. **Default value:** ``0``
            size (float | ExprRef | dict[str, Any]): The font size in pixels. **Default value:** ``11``
            squeeze (bool | ExprRef | dict[str, Any]): If the ``squeeze`` property is true and secondary positional channels (``x2`` and/or ``y2``) are used, the text is scaled to fit mark's width and/or height. **Default value:** ``true``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            text (Scalar_T | ExprRef | dict[str, Any]): The text to display. The format of numeric data can be customized by setting a format specifier to channel definition's ``format`` property. **Default value:** ``""``
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            viewportEdgeFadeDistanceBottom (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceBottom`` property.
            viewportEdgeFadeDistanceLeft (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceLeft`` property.
            viewportEdgeFadeDistanceRight (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceRight`` property.
            viewportEdgeFadeDistanceTop (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceTop`` property.
            viewportEdgeFadeWidthBottom (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthBottom`` property.
            viewportEdgeFadeWidthLeft (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthLeft`` property.
            viewportEdgeFadeWidthRight (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthRight`` property.
            viewportEdgeFadeWidthTop (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthTop`` property.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "align": align,
            "angle": angle,
            "baseline": baseline,
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "dx": dx,
            "dy": dy,
            "fitToBand": fitToBand,
            "flushX": flushX,
            "flushY": flushY,
            "font": font,
            "fontStyle": fontStyle,
            "fontWeight": fontWeight,
            "logoLetters": logoLetters,
            "minBufferSize": minBufferSize,
            "opacity": opacity,
            "paddingX": paddingX,
            "paddingY": paddingY,
            "size": size,
            "squeeze": squeeze,
            "style": style,
            "text": text,
            "tooltip": tooltip,
            "viewportEdgeFadeDistanceBottom": viewportEdgeFadeDistanceBottom,
            "viewportEdgeFadeDistanceLeft": viewportEdgeFadeDistanceLeft,
            "viewportEdgeFadeDistanceRight": viewportEdgeFadeDistanceRight,
            "viewportEdgeFadeDistanceTop": viewportEdgeFadeDistanceTop,
            "viewportEdgeFadeWidthBottom": viewportEdgeFadeWidthBottom,
            "viewportEdgeFadeWidthLeft": viewportEdgeFadeWidthLeft,
            "viewportEdgeFadeWidthRight": viewportEdgeFadeWidthRight,
            "viewportEdgeFadeWidthTop": viewportEdgeFadeWidthTop,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("text", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_link(
        self,
        *,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clampApex: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        maxChordLength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minArcHeight: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical"]
        | Literal["horizontal"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        segments: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``link``.

        Args:
            arcFadingDistance (Sequence[float] | Literal[False] | ExprRef | dict[str, Any]): The range of the ``"arc"`` shape's fading distance in pixels. This property allows for making the arc's opacity fade out as it extends away from the chord. The fading distance is interpolated from one to zero between the interval defined by this property. Both ``false`` and ``[0, 0]`` disable fading. **Default value:** ``false``
            arcHeightFactor (float | ExprRef | dict[str, Any]): Scaling factor for the ``"arc``" shape's height. The default value ``1.0`` produces roughly circular arcs. **Default value:** ``1.0``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clampApex (bool | ExprRef | dict[str, Any]): Whether the apex of the ``"dome"`` shape is clamped to the viewport edge. When over a half of the dome is located outside the viewport, clamping allows for more accurate reading of the value encoded by the apex' position. **Default value:** ``false``
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            linkShape (Literal['arc'] | Literal['diagonal'] | Literal['line'] | Literal['dome'] | ExprRef | dict[str, Any]): The shape of the link path. The ``"arc"`` shape draws a circular arc between the two points. The apex of the arc resides on the left side of the line that connects the two points. The ``"dome"`` shape draws a vertical or horizontal arc with a specific height. The primary positional channel determines the apex of the arc and the secondary determines the endpoint placement. The ``"diagonal"`` shape draws an "S"-shaped curve between the two points. The ``"line"`` shape draws a straight line between the two points. See an example of the different shapes below. **Default value:** ``"arc"``
            maxChordLength (float | ExprRef | dict[str, Any]): The maximum length of ``"arc"`` shape's chord in pixels. The chord is the line segment between the two points that define the arc. Limiting the chord length serves two purposes when zooming in close enough: 1) it prevents the arc from becoming a straight line and 2) it mitigates the limited precision of floating point numbers in arc rendering. **Default value:** ``50000``
            minArcHeight (float | ExprRef | dict[str, Any]): The minimum height of an ``"arc"`` shape. Makes very short links more clearly visible. **Default value:** ``1.5``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minPickingSize (float | ExprRef | dict[str, Any]): The minimum picking size invisibly increases the stroke width or point diameter of marks when pointing them with the mouse cursor, making it easier to select them. The valus is the minimum size in pixels. **Default value:** ``3.0`` for ``"link"`` and ``2.0`` for ``"point"``
            noFadingOnPointSelection (bool | ExprRef | dict[str, Any]): Disables fading of the link when an mark instance is subject to any point selection. As the fading distance is unavailable as a visual channel, this property allows for enhancing the visibility of the selected links. **Default value:** ``true``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            orient (Literal['vertical'] | Literal['horizontal'] | ExprRef | dict[str, Any]): The orientation of the link path. Either ``"vertical"`` or ``"horizontal"``. Only applies to diagonal links. **Default value:** ``"vertical"``
            segments (float | ExprRef | dict[str, Any]): The number of segments in the bézier curve. Affects the rendering quality and performance. Use a higher value for a smoother curve. **Default value:** ``101``
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "arcFadingDistance": arcFadingDistance,
            "arcHeightFactor": arcHeightFactor,
            "buildIndex": buildIndex,
            "clampApex": clampApex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "linkShape": linkShape,
            "maxChordLength": maxChordLength,
            "minArcHeight": minArcHeight,
            "minBufferSize": minBufferSize,
            "minPickingSize": minPickingSize,
            "noFadingOnPointSelection": noFadingOnPointSelection,
            "opacity": opacity,
            "orient": orient,
            "segments": segments,
            "size": size,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("link", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_arrow(
        self,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        direction: Literal["forward"]
        | Literal["reverse"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        headAngle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        headNotchAngle: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headPlacement: Literal["inside"]
        | Literal["outside"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headShape: Literal["triangle"]
        | Literal["open"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headSpacing: float
        | None
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minStemLength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float
        | core.ArrowRelativeSize
        | dict[str, Any]
        | core.ExprRef
        | UndefinedType = Undefined,
        startNotch: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stem: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``arrow``.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            direction (Literal['forward'] | Literal['reverse'] | ExprRef | dict[str, Any]): Direction of the arrowhead. ``"forward"`` places the arrowhead at the secondary endpoint (``x2``, ``y2``). ``"reverse"`` places it at the primary endpoint (``x``, ``y``). For data-driven direction, use the ``direction`` encoding channel. __Default value:__ ``"forward"``
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            headAngle (float | ExprRef | dict[str, Any]): Angle in degrees between the arrow axis and an outer edge of the arrowhead. Smaller values produce longer, narrower heads. Larger values produce shorter, blunter heads. Values are clamped to ``[1, 90]``. __Default value:__ ``45``
            headNotchAngle (float | ExprRef | dict[str, Any]): Angle in degrees between the arrow axis and the arrowhead notch edge. ``90`` places the notch point at the tip, producing a triangular head when ``headAngle`` is less than ``90``. Applies to ``"triangle"`` heads. ``"open"`` heads use ``headAngle`` for the notch edge as well. Values are clamped to ``[1, 90]``. __Default value:__ ``90``
            headPlacement (Literal['inside'] | Literal['outside'] | ExprRef | dict[str, Any]): Placement of the arrowhead relative to the encoded segment. ``"inside"`` keeps the whole arrowhead within the encoded segment. ``"outside"`` places the arrowhead beyond the encoded segment so that the head starts at the segment endpoint. __Default value:__ ``"inside"``
            headShape (Literal['triangle'] | Literal['open'] | ExprRef | dict[str, Any]): Shape of the arrowhead. ``"triangle"`` draws a filled head. ``"open"`` draws an open head whose thickness matches the resolved ``size``, even when ``stem`` is ``false``. __Default value:__ ``"triangle"``
            headSpacing (float | None | ExprRef | dict[str, Any]): Spacing between repeated arrowheads as a multiplier of resolved ``size``. The effective spacing is at least the rendered arrowhead footprint, including stroke. If ``null``, arrowheads are not repeated. __Default value:__ ``null``
            headWidth (float | ExprRef | dict[str, Any]): Width of the arrowhead as a multiplier of resolved ``size``. Values above ``1`` make the arrowhead wider than the stem. __Default value:__ ``3``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minSize (float | ExprRef | dict[str, Any]): Minimum resolved arrow stem thickness in pixels. Applies to numeric, band-relative, and encoded ``size`` values. __Default value:__ ``1``
            minStemLength (float | ExprRef | dict[str, Any]): Minimum visible length of the arrow stem in pixels. When a non-repeated arrow is too short for the configured shape and minimum stem length, the affected notch or head angle is made blunter toward 90 degrees. For ``"inside"`` placement, this applies to ``"triangle"`` heads and is measured from the start of the stem to where the stem meets the head notch edge. For ``"outside"`` placement, this applies when ``startNotch`` is ``true`` and is measured from the start notch to the head start. Has no effect when ``stem`` is ``false``. __Default value:__ ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            size (float | ArrowRelativeSize | dict[str, Any] | ExprRef): Arrow stem thickness in pixels, or as a fraction of the perpendicular band or view span for axis-aligned arrows. Numeric values are pixels. ``{ "band": 0.8 }`` resolves to 80% of the perpendicular band width, or 80% of the perpendicular view span when no band scale is available. Use ``channel`` to explicitly select the reference channel. Band-relative size is not supported for diagonal arrows. __Default value:__ ``8``
            startNotch (bool | ExprRef | dict[str, Any]): Whether to draw a notch at the start of the arrow. The start notch uses the same slope as the arrowhead edge. __Default value:__ ``false``
            stem (bool | ExprRef | dict[str, Any]): Whether to draw the arrow stem. When ``false``, the resolved ``size`` still controls open-head thickness. ``minStemLength`` has no effect when the stem is hidden. __Default value:__ ``true``
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "direction": direction,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "headAngle": headAngle,
            "headNotchAngle": headNotchAngle,
            "headPlacement": headPlacement,
            "headShape": headShape,
            "headSpacing": headSpacing,
            "headWidth": headWidth,
            "minBufferSize": minBufferSize,
            "minSize": minSize,
            "minStemLength": minStemLength,
            "opacity": opacity,
            "size": size,
            "startNotch": startNotch,
            "stem": stem,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("arrow", **defined)  # type: ignore[attr-defined, no-any-return]

    def mark_circle(
        self,
        *,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        inwardStroke: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        semanticScore: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        semanticZoomFraction: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shape: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Set the chart mark to ``point``.

        Args:
            angle (float | ExprRef | dict[str, Any]): The rotation angle in degrees. **Default value:** ``0``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            dx (float | ExprRef | dict[str, Any]): Horizontal offset in pixels. **Default value:** ``0``
            dy (float | ExprRef | dict[str, Any]): Vertical offset in pixels. **Default value:** ``0``
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillGradientStrength (float | ExprRef | dict[str, Any]): Gradient strength controls the amount of the gradient eye-candy effect in the fill color. Valid values are between ``0`` and ``1``. **Default value:** ``0``
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            geometricZoomBound (float): Enables geometric zooming. The value is the base two logarithmic zoom level where the maximum point size is reached. **Default value:** ``0``
            inwardStroke (bool | ExprRef | dict[str, Any]): Should the stroke only grow inwards, e.g, the diameter/outline is not affected by the stroke width. Thus, a point that has a zero size has no visible stroke. This allows strokes to be used with geometric zoom, etc. **Default value:** ``false``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minPickingSize (float | ExprRef | dict[str, Any]): The minimum picking size invisibly increases the stroke width or point diameter of marks when pointing them with the mouse cursor, making it easier to select them. The valus is the minimum size in pixels. **Default value:** ``3.0`` for ``"link"`` and ``2.0`` for ``"point"``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            sampleFacetPadding (float): Additional padding used by sample facets. **Default value:** ``0.1``
            semanticScore (float | ExprRef | dict[str, Any]): The semantic score used by semantic zooming in the point mark. This is primarily intended for internal use. **Default value:** ``0``
            semanticZoomFraction (float | ExprRef | dict[str, Any]): TODO **Default value:** ``0.02``
            shape (str | ExprRef | dict[str, Any]): One of ``"circle"``, ``"square"``, ``"cross"``, ``"x"``, ``"+"``, ``"diamond"``, ``"triangle-up"``, ``"triangle-down"``, ``"triangle-right"``, ``"triangle-left"``, ``"tick-up"``, ``"tick-down"``, ``"tick-right"``, or ``"tick-left"``. The ``"x"`` and ``"+"`` shapes are stroke-only and use ``strokeWidth`` for their line thickness. **Default value:** ``"circle"``
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        properties = {
            "angle": angle,
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "dx": dx,
            "dy": dy,
            "fill": fill,
            "fillGradientStrength": fillGradientStrength,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "geometricZoomBound": geometricZoomBound,
            "inwardStroke": inwardStroke,
            "minBufferSize": minBufferSize,
            "minPickingSize": minPickingSize,
            "opacity": opacity,
            "sampleFacetPadding": sampleFacetPadding,
            "semanticScore": semanticScore,
            "semanticZoomFraction": semanticZoomFraction,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_mark("point", **defined)  # type: ignore[attr-defined, no-any-return]


class EncodingMethodMixin:
    """Schema-derived encoding methods for renderable specifications."""

    def encode(
        self,
        *args: Channel,
        angle: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        color: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        direction: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        dx: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        dy: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        facetIndex: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        fill: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        fillOpacity: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        key: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        opacity: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        sample: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        search: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        semanticScore: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        shape: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        size: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        stroke: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        strokeOpacity: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        strokeWidth: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        text: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        tooltip: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        uniqueId: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        x: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        x2: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        xOffset: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        y: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        y2: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
        yOffset: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None
        | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with merged channel encodings.

        Args:
            angle (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Rotation angle of point and text marks.
            color (FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefStringNull | MarkPropExprDefType | ValueDefWithConditionStringNullType): Color of the marks – either fill or stroke color based on the ``filled`` property of mark definition. Note: 1) For fine-grained control over both fill and stroke colors of the marks, please use the ``fill`` and ``stroke`` channels. The ``fill`` or ``stroke`` encodings have higher precedence than ``color``, thus may override the ``color`` encoding if conflicting encodings are specified. 2) See the GenomeSpy scale documentation for more information about customizing color schemes.
            direction (DirectionDef | dict[str, Any]): Direction of arrow marks. Encoded values are mapped with a discrete scale whose range values must be ``"forward"`` or ``"reverse"``. This channel is supported by arrow marks only and does not create a legend.
            dx (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType | MarkPropExprDef): Legacy horizontal pixel offset for point marks.
            dy (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType | MarkPropExprDef): Legacy vertical pixel offset for point marks. Positive values move in the opposite direction from ``yOffset``.
            facetIndex (FieldDefWithoutScale | dict[str, Any]): For internal use
            fill (FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefStringNull | MarkPropExprDefType | ValueDefWithConditionStringNullType): Fill color of the marks. Note: The ``fill`` encoding has higher precedence than ``color``, thus may override the ``color`` encoding if conflicting encodings are specified.
            fillOpacity (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Fill opacity of the marks.
            key (FieldDefWithoutScale | dict[str, Any] | Sequence[FieldDefWithoutScale | dict[str, Any]]): One or more data fields that uniquely identify data objects for stable point selections and bookmarking across sessions. Unlike ``uniqueId`` (an implicit surrogate key), key fields must be stable in the source data. Use a single field definition for simple keys, or an array of field definitions for composite keys. For composite keys, field order is significant.
            opacity (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Opacity of the marks.
            sample (FieldDefWithoutScale | dict[str, Any]): Facet identifier for interactive filtering, sorting, and grouping in the App.
            search (FieldDefWithoutScale | dict[str, Any] | Sequence[FieldDefWithoutScale | dict[str, Any]]): One or more fields used by the App's location/search input to match data objects in this view. Use a single field definition for simple search, or an array for matching against multiple fields. A datum matches when any configured search field matches the entered term.
            semanticScore (dict[str, Any]): Schema-defined ``semanticScore`` property.
            shape (FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefStringNull | MarkPropExprDefTypeForShape | ValueDefWithConditionStringNullTypeForShape): Shape of the mark. For ``point`` marks the supported values include: - plotting shapes: ``"circle"``, ``"square"``, ``"cross"``, ``"diamond"``, ``"triangle-up"``, ``"triangle-down"``, ``"triangle-right"``, or ``"triangle-left"``. - stroke-only ``"x"`` and ``"+"`` shapes, whose line thickness is controlled by ``strokeWidth`` - centered directional shape ``"triangle"``
            size (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Size of the mark. - For ``"point"`` – the symbol size, or pixel area of the mark. - For ``"text"`` – the text's font size. - For ``"arrow"`` – the stem thickness in pixels.
            stroke (FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefStringNull | MarkPropExprDefType | ValueDefWithConditionStringNullType): Stroke color of the marks. Note: The ``stroke`` encoding has higher precedence than ``color``, thus may override the ``color`` encoding if conflicting encodings are specified.
            strokeOpacity (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Stroke opacity of the marks.
            strokeWidth (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType): Stroke width of the marks.
            text (StringFieldDef | dict[str, Any] | StringDatumDef | ExprDef | ValueDefString): Text of the ``text`` mark.
            tooltip (StringFieldDef | dict[str, Any] | StringDatumDef | ExprDef | ValueDefString | Sequence[StringFieldDef | dict[str, Any] | StringDatumDef | ExprDef | ValueDefString] | None): Fields, expressions, or values shown by the default tooltip handler. If omitted, the default tooltip handler shows the hovered datum's properties. If ``null``, the default tooltip handler shows no raw datum rows for this mark. Use an array to show multiple rows in a specific order.
            uniqueId (FieldDefWithoutScale | dict[str, Any]): For internal use
            x (dict[str, Any] | None): X coordinates of the marks. The ``value`` of this channel can be a number between zero and one.
            x2 (Position2Def | dict[str, Any] | None): X2 coordinates of the marks. The ``value`` of this channel can be a number between zero and one.
            xOffset (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType | MarkPropExprDef | None): Horizontal offset from the encoded x position, in logical pixels.
            y (PositionFieldDef | dict[str, Any] | ChromPosDef | PositionDatumDef | PositionExprDef | ValueDefNumber | None): Y coordinates of the marks. The ``value`` of this channel can be a number between zero and one.
            y2 (Position2Def | dict[str, Any] | None): Y2 coordinates of the marks. The ``value`` of this channel can be a number between zero and one.
            yOffset (FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber | dict[str, Any] | FieldOrDatumDefWithConditionScaleDatumDefNumber | MarkPropExprDefType | ValueDefWithConditionNumberType | MarkPropExprDef | None): Vertical offset from the encoded y position, in logical pixels.
        """
        properties = {
            "angle": angle,
            "color": color,
            "direction": direction,
            "dx": dx,
            "dy": dy,
            "facetIndex": facetIndex,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "key": key,
            "opacity": opacity,
            "sample": sample,
            "search": search,
            "semanticScore": semanticScore,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "text": text,
            "tooltip": tooltip,
            "uniqueId": uniqueId,
            "x": x,
            "x2": x2,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._encode(args, defined)  # type: ignore[attr-defined, no-any-return]


class ResolutionMethodMixin:
    """Schema-derived composition resolution methods."""

    def resolve_axis(
        self,
        *,
        angle: ResolutionBehavior_T | UndefinedType = Undefined,
        color: ResolutionBehavior_T | UndefinedType = Undefined,
        default: ResolutionBehavior_T | UndefinedType = Undefined,
        direction: ResolutionBehavior_T | UndefinedType = Undefined,
        dx: ResolutionBehavior_T | UndefinedType = Undefined,
        dy: ResolutionBehavior_T | UndefinedType = Undefined,
        facetIndex: ResolutionBehavior_T | UndefinedType = Undefined,
        fill: ResolutionBehavior_T | UndefinedType = Undefined,
        fillOpacity: ResolutionBehavior_T | UndefinedType = Undefined,
        key: ResolutionBehavior_T | UndefinedType = Undefined,
        opacity: ResolutionBehavior_T | UndefinedType = Undefined,
        sample: ResolutionBehavior_T | UndefinedType = Undefined,
        search: ResolutionBehavior_T | UndefinedType = Undefined,
        semanticScore: ResolutionBehavior_T | UndefinedType = Undefined,
        shape: ResolutionBehavior_T | UndefinedType = Undefined,
        size: ResolutionBehavior_T | UndefinedType = Undefined,
        stroke: ResolutionBehavior_T | UndefinedType = Undefined,
        strokeOpacity: ResolutionBehavior_T | UndefinedType = Undefined,
        strokeWidth: ResolutionBehavior_T | UndefinedType = Undefined,
        text: ResolutionBehavior_T | UndefinedType = Undefined,
        tooltip: ResolutionBehavior_T | UndefinedType = Undefined,
        uniqueId: ResolutionBehavior_T | UndefinedType = Undefined,
        x: ResolutionBehavior_T | UndefinedType = Undefined,
        x2: ResolutionBehavior_T | UndefinedType = Undefined,
        xOffset: ResolutionBehavior_T | UndefinedType = Undefined,
        y: ResolutionBehavior_T | UndefinedType = Undefined,
        y2: ResolutionBehavior_T | UndefinedType = Undefined,
        yOffset: ResolutionBehavior_T | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged axis resolutions."""
        properties = {
            "angle": angle,
            "color": color,
            "default": default,
            "direction": direction,
            "dx": dx,
            "dy": dy,
            "facetIndex": facetIndex,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "key": key,
            "opacity": opacity,
            "sample": sample,
            "search": search,
            "semanticScore": semanticScore,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "text": text,
            "tooltip": tooltip,
            "uniqueId": uniqueId,
            "x": x,
            "x2": x2,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_resolution("axis", defined)  # type: ignore[attr-defined, no-any-return]

    def resolve_legend(
        self,
        *,
        angle: LegendResolutionBehavior_T | UndefinedType = Undefined,
        color: LegendResolutionBehavior_T | UndefinedType = Undefined,
        default: LegendResolutionBehavior_T | UndefinedType = Undefined,
        direction: LegendResolutionBehavior_T | UndefinedType = Undefined,
        dx: LegendResolutionBehavior_T | UndefinedType = Undefined,
        dy: LegendResolutionBehavior_T | UndefinedType = Undefined,
        facetIndex: LegendResolutionBehavior_T | UndefinedType = Undefined,
        fill: LegendResolutionBehavior_T | UndefinedType = Undefined,
        fillOpacity: LegendResolutionBehavior_T | UndefinedType = Undefined,
        key: LegendResolutionBehavior_T | UndefinedType = Undefined,
        opacity: LegendResolutionBehavior_T | UndefinedType = Undefined,
        sample: LegendResolutionBehavior_T | UndefinedType = Undefined,
        search: LegendResolutionBehavior_T | UndefinedType = Undefined,
        semanticScore: LegendResolutionBehavior_T | UndefinedType = Undefined,
        shape: LegendResolutionBehavior_T | UndefinedType = Undefined,
        size: LegendResolutionBehavior_T | UndefinedType = Undefined,
        stroke: LegendResolutionBehavior_T | UndefinedType = Undefined,
        strokeOpacity: LegendResolutionBehavior_T | UndefinedType = Undefined,
        strokeWidth: LegendResolutionBehavior_T | UndefinedType = Undefined,
        text: LegendResolutionBehavior_T | UndefinedType = Undefined,
        tooltip: LegendResolutionBehavior_T | UndefinedType = Undefined,
        uniqueId: LegendResolutionBehavior_T | UndefinedType = Undefined,
        x: LegendResolutionBehavior_T | UndefinedType = Undefined,
        x2: LegendResolutionBehavior_T | UndefinedType = Undefined,
        xOffset: LegendResolutionBehavior_T | UndefinedType = Undefined,
        y: LegendResolutionBehavior_T | UndefinedType = Undefined,
        y2: LegendResolutionBehavior_T | UndefinedType = Undefined,
        yOffset: LegendResolutionBehavior_T | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged legend resolutions."""
        properties = {
            "angle": angle,
            "color": color,
            "default": default,
            "direction": direction,
            "dx": dx,
            "dy": dy,
            "facetIndex": facetIndex,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "key": key,
            "opacity": opacity,
            "sample": sample,
            "search": search,
            "semanticScore": semanticScore,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "text": text,
            "tooltip": tooltip,
            "uniqueId": uniqueId,
            "x": x,
            "x2": x2,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_resolution("legend", defined)  # type: ignore[attr-defined, no-any-return]

    def resolve_scale(
        self,
        *,
        angle: ResolutionBehavior_T | UndefinedType = Undefined,
        color: ResolutionBehavior_T | UndefinedType = Undefined,
        default: ResolutionBehavior_T | UndefinedType = Undefined,
        direction: ResolutionBehavior_T | UndefinedType = Undefined,
        dx: ResolutionBehavior_T | UndefinedType = Undefined,
        dy: ResolutionBehavior_T | UndefinedType = Undefined,
        facetIndex: ResolutionBehavior_T | UndefinedType = Undefined,
        fill: ResolutionBehavior_T | UndefinedType = Undefined,
        fillOpacity: ResolutionBehavior_T | UndefinedType = Undefined,
        key: ResolutionBehavior_T | UndefinedType = Undefined,
        opacity: ResolutionBehavior_T | UndefinedType = Undefined,
        sample: ResolutionBehavior_T | UndefinedType = Undefined,
        search: ResolutionBehavior_T | UndefinedType = Undefined,
        semanticScore: ResolutionBehavior_T | UndefinedType = Undefined,
        shape: ResolutionBehavior_T | UndefinedType = Undefined,
        size: ResolutionBehavior_T | UndefinedType = Undefined,
        stroke: ResolutionBehavior_T | UndefinedType = Undefined,
        strokeOpacity: ResolutionBehavior_T | UndefinedType = Undefined,
        strokeWidth: ResolutionBehavior_T | UndefinedType = Undefined,
        text: ResolutionBehavior_T | UndefinedType = Undefined,
        tooltip: ResolutionBehavior_T | UndefinedType = Undefined,
        uniqueId: ResolutionBehavior_T | UndefinedType = Undefined,
        x: ResolutionBehavior_T | UndefinedType = Undefined,
        x2: ResolutionBehavior_T | UndefinedType = Undefined,
        xOffset: ResolutionBehavior_T | UndefinedType = Undefined,
        y: ResolutionBehavior_T | UndefinedType = Undefined,
        y2: ResolutionBehavior_T | UndefinedType = Undefined,
        yOffset: ResolutionBehavior_T | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged scale resolutions."""
        properties = {
            "angle": angle,
            "color": color,
            "default": default,
            "direction": direction,
            "dx": dx,
            "dy": dy,
            "facetIndex": facetIndex,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "key": key,
            "opacity": opacity,
            "sample": sample,
            "search": search,
            "semanticScore": semanticScore,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "text": text,
            "tooltip": tooltip,
            "uniqueId": uniqueId,
            "x": x,
            "x2": x2,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "yOffset": yOffset,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_resolution("scale", defined)  # type: ignore[attr-defined, no-any-return]


class TopLevelMergeMixin:
    """Schema-derived top-level property merge methods."""

    def with_config(
        self,
        value: core.GenomeSpyConfig | GenomeSpyConfigKwds | None | object = Undefined,
        /,
        *,
        arrow: core.ArrowConfig | dict[str, Any] | UndefinedType = Undefined,
        axis: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisBottom: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisIndex: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLeft: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLocus: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisNominal: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisOrdinal: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisQuantitative: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisRight: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisTop: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisX: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisY: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        legend: core.LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        legendTrack: core.LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        link: core.LinkConfig | LinkConfigKwds | UndefinedType = Undefined,
        mark: core.MarkConfig | MarkConfigKwds | UndefinedType = Undefined,
        point: core.PointConfig | PointConfigKwds | UndefinedType = Undefined,
        range: core.RangeConfig | RangeConfigKwds | UndefinedType = Undefined,
        rect: core.RectConfig | RectConfigKwds | UndefinedType = Undefined,
        rule: core.RuleConfig | RuleConfigKwds | UndefinedType = Undefined,
        scale: core.ScaleConfig | ScaleConfigKwds | UndefinedType = Undefined,
        style: dict[str, Any] | UndefinedType = Undefined,
        text: core.TextConfig | TextConfigKwds | UndefinedType = Undefined,
        tick: core.TickConfig | dict[str, Any] | UndefinedType = Undefined,
        title: core.TitleConfig | TitleConfigKwds | UndefinedType = Undefined,
        view: core.ViewConfig | ViewConfigKwds | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged top-level ``config``.

        Args:
            arrow (ArrowConfig | dict[str, Any]): Defaults for arrow marks.
            axis (AxisConfig | AxisConfigKwds): Defaults shared by all axes.
            axisBottom (AxisConfig | AxisConfigKwds): Defaults for bottom-oriented axes.
            axisIndex (AxisConfig | AxisConfigKwds): Defaults for axes that visualize GenomeSpy ``index`` scales.
            axisLeft (AxisConfig | AxisConfigKwds): Defaults for left-oriented axes.
            axisLocus (AxisConfig | AxisConfigKwds): Defaults for axes that visualize GenomeSpy ``locus`` scales.
            axisNominal (AxisConfig | AxisConfigKwds): Defaults for axes that visualize nominal data.
            axisOrdinal (AxisConfig | AxisConfigKwds): Defaults for axes that visualize ordinal data.
            axisQuantitative (AxisConfig | AxisConfigKwds): Defaults for axes that visualize quantitative data.
            axisRight (AxisConfig | AxisConfigKwds): Defaults for right-oriented axes.
            axisTop (AxisConfig | AxisConfigKwds): Defaults for top-oriented axes.
            axisX (AxisConfig | AxisConfigKwds): Defaults for x axes.
            axisY (AxisConfig | AxisConfigKwds): Defaults for y axes.
            legend (LegendConfig | LegendConfigKwds): Defaults shared by all legends. Set ``disable`` to ``true`` to suppress automatic legend creation by default.
            legendTrack (LegendConfig | LegendConfigKwds): Defaults for legends of track-like views that use ``index`` or ``locus`` scales on the x channel. __Default value:__ ``{ "style": "track-bottom-legend" }``
            link (LinkConfig | LinkConfigKwds): Defaults for link marks.
            mark (MarkConfig | MarkConfigKwds): Defaults shared by all mark types.
            point (PointConfig | PointConfigKwds): Defaults for point marks.
            range (RangeConfig | RangeConfigKwds): Named reusable ranges for channels such as ``shape``, ``size``, and color.
            rect (RectConfig | RectConfigKwds): Defaults for rect marks.
            rule (RuleConfig | RuleConfigKwds): Defaults for rule marks.
            scale (ScaleConfig | ScaleConfigKwds): Defaults for scale behavior and scale-type-specific buckets.
            style (dict[str, Any]): Named reusable style buckets that marks, axes, legends, titles, and views can reference through their ``style`` properties.
            text (TextConfig | TextConfigKwds): Defaults for text marks.
            tick (TickConfig | dict[str, Any]): Defaults for tick marks.
            title (TitleConfig | TitleConfigKwds): Defaults for view titles.
            view (ViewConfig | ViewConfigKwds): Defaults for view background styling, including fill, stroke, shadow, and z-order properties.
        """
        defined = {
            "arrow": arrow,
            "axis": axis,
            "axisBottom": axisBottom,
            "axisIndex": axisIndex,
            "axisLeft": axisLeft,
            "axisLocus": axisLocus,
            "axisNominal": axisNominal,
            "axisOrdinal": axisOrdinal,
            "axisQuantitative": axisQuantitative,
            "axisRight": axisRight,
            "axisTop": axisTop,
            "axisX": axisX,
            "axisY": axisY,
            "legend": legend,
            "legendTrack": legendTrack,
            "link": link,
            "mark": mark,
            "point": point,
            "range": range,
            "rect": rect,
            "rule": rule,
            "scale": scale,
            "style": style,
            "text": text,
            "tick": tick,
            "title": title,
            "view": view,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._merge_top_level("config", value, defined)  # type: ignore[attr-defined, no-any-return]

    def with_view(
        self,
        value: core.ViewBackground | ViewBackgroundKwds | None | object = Undefined,
        /,
        *,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOffsetY: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeOpacity: float | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        strokeZindex: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged top-level ``view``.

        Args:
            fill (str): Fill color of the view background.
            fillOpacity (float): Opacity of the view background fill.
            shadowBlur (float | ExprRef | dict[str, Any]): The blur radius of the drop shadow in pixels. Higher values produce a more diffuse shadow. **Default value:** ``0``
            shadowColor (str | ExprRef | dict[str, Any]): The color of the drop shadow. Any valid CSS color string is allowed. **Default value:** ``"black"``
            shadowOffsetX (float | ExprRef | dict[str, Any]): The horizontal offset of the drop shadow in pixels. Positive values move the shadow to the right. **Default value:** ``0``
            shadowOffsetY (float | ExprRef | dict[str, Any]): The vertical offset of the drop shadow in pixels. Positive values move the shadow downward. **Default value:** ``0``
            shadowOpacity (float | ExprRef | dict[str, Any]): The opacity of the drop shadow. Value between ``0`` (fully transparent) and ``1`` (fully opaque). **Default value:** ``0`` (disabled)
            stroke (str): Stroke color of the view background.
            strokeOpacity (float): Opacity of the view background stroke.
            strokeWidth (float): Stroke width of the view background border.
            strokeZindex (float): Z-order of the background stroke relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. __Default value:__ ``"cell"``
            zindex (float): Z-order of the background fill relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``
        """
        defined = {
            "fill": fill,
            "fillOpacity": fillOpacity,
            "shadowBlur": shadowBlur,
            "shadowColor": shadowColor,
            "shadowOffsetX": shadowOffsetX,
            "shadowOffsetY": shadowOffsetY,
            "shadowOpacity": shadowOpacity,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "strokeZindex": strokeZindex,
            "style": style,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._merge_top_level("view", value, defined)  # type: ignore[attr-defined, no-any-return]

    def with_scales(
        self,
        value: ScalesKwds | None | object = Undefined,
        /,
        *,
        angle: core.Scale | ScaleKwds | UndefinedType = Undefined,
        color: core.Scale | ScaleKwds | UndefinedType = Undefined,
        direction: core.Scale | ScaleKwds | UndefinedType = Undefined,
        dx: core.Scale | ScaleKwds | UndefinedType = Undefined,
        dy: core.Scale | ScaleKwds | UndefinedType = Undefined,
        fill: core.Scale | ScaleKwds | UndefinedType = Undefined,
        fillOpacity: core.Scale | ScaleKwds | UndefinedType = Undefined,
        opacity: core.Scale | ScaleKwds | UndefinedType = Undefined,
        shape: core.Scale | ScaleKwds | UndefinedType = Undefined,
        size: core.Scale | ScaleKwds | UndefinedType = Undefined,
        stroke: core.Scale | ScaleKwds | UndefinedType = Undefined,
        strokeOpacity: core.Scale | ScaleKwds | UndefinedType = Undefined,
        strokeWidth: core.Scale | ScaleKwds | UndefinedType = Undefined,
        x: core.Scale | ScaleKwds | UndefinedType = Undefined,
        x2: core.Scale | ScaleKwds | UndefinedType = Undefined,
        xOffset: core.Scale | ScaleKwds | UndefinedType = Undefined,
        y: core.Scale | ScaleKwds | UndefinedType = Undefined,
        y2: core.Scale | ScaleKwds | UndefinedType = Undefined,
        yOffset: core.Scale | ScaleKwds | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with merged top-level ``scales``.

        Args:
            angle (Scale | ScaleKwds): Schema-defined ``angle`` property.
            color (Scale | ScaleKwds): Schema-defined ``color`` property.
            direction (Scale | ScaleKwds): Schema-defined ``direction`` property.
            dx (Scale | ScaleKwds): Schema-defined ``dx`` property.
            dy (Scale | ScaleKwds): Schema-defined ``dy`` property.
            fill (Scale | ScaleKwds): Schema-defined ``fill`` property.
            fillOpacity (Scale | ScaleKwds): Schema-defined ``fillOpacity`` property.
            opacity (Scale | ScaleKwds): Schema-defined ``opacity`` property.
            shape (Scale | ScaleKwds): Schema-defined ``shape`` property.
            size (Scale | ScaleKwds): Schema-defined ``size`` property.
            stroke (Scale | ScaleKwds): Schema-defined ``stroke`` property.
            strokeOpacity (Scale | ScaleKwds): Schema-defined ``strokeOpacity`` property.
            strokeWidth (Scale | ScaleKwds): Schema-defined ``strokeWidth`` property.
            x (Scale | ScaleKwds): Schema-defined ``x`` property.
            x2 (Scale | ScaleKwds): Schema-defined ``x2`` property.
            xOffset (Scale | ScaleKwds): Schema-defined ``xOffset`` property.
            y (Scale | ScaleKwds): Schema-defined ``y`` property.
            y2 (Scale | ScaleKwds): Schema-defined ``y2`` property.
            yOffset (Scale | ScaleKwds): Schema-defined ``yOffset`` property.
        """
        defined = {
            "angle": angle,
            "color": color,
            "direction": direction,
            "dx": dx,
            "dy": dy,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "opacity": opacity,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "x": x,
            "x2": x2,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._merge_top_level("scales", value, defined)  # type: ignore[attr-defined, no-any-return]


class ImportedViewConstructorMixin:
    """Schema-derived constructor for imported child views."""

    def __init__(
        self,
        import_: core.UrlImport
        | dict[str, Any]
        | core.TemplateImport
        | UndefinedType = Undefined,
        *,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | dict[str, Any]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> None:
        """Initialize an imported child view.

        Args:
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for the imported subtree at the import site. This config is merged before the imported spec's own root-level ``config``, so imported specs can remain self-contained and override import-site defaults where needed.
            import\\_ (UrlImport | dict[str, Any] | TemplateImport): The method to import a specification.
            name (str): The name given to the imported view. This property overrides the name specified in the imported specification and defines an import scope that is used for bookmarkable view visibility and parameter addressing.
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter] | dict[str, Any]): Dynamic variables that parameterize a visualization. Parameters defined here override the parameters defined in the imported specification.
            visible (bool): Overrides the visibility of the imported view. If not specified, the imported specification's ``visible`` property is used.
            zindex (float): Overrides the imported view's z-order among sibling views. Higher values render later. This does not affect layout order. __Default value:__ the imported view's ``zindex``, or ``0``
        """
        properties = {
            "config": config,
            "import": import_,
            "name": name,
            "params": params,
            "visible": visible,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_import(properties=defined)  # type: ignore[attr-defined]


class UnitPropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        data: Any | UndefinedType = Undefined,
        mark: MarkType_T
        | core.RectProps
        | dict[str, Any]
        | core.ArrowProps
        | core.TextProps
        | core.RuleProps
        | core.TickProps
        | core.LinkProps
        | core.PointProps
        | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            mark (MarkType_T | RectProps | dict[str, Any] | ArrowProps | TextProps | RuleProps | TickProps | LinkProps | PointProps): The graphical mark presenting the data objects.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): The background of the view, including fill, stroke, and stroke width.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "mark": mark,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        mark: MarkType_T
        | core.RectProps
        | dict[str, Any]
        | core.ArrowProps
        | core.TextProps
        | core.RuleProps
        | core.TickProps
        | core.LinkProps
        | core.PointProps
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            mark (MarkType_T | RectProps | dict[str, Any] | ArrowProps | TextProps | RuleProps | TickProps | LinkProps | PointProps): The graphical mark presenting the data objects.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): The background of the view, including fill, stroke, and stroke width.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "mark": mark,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        mark: MarkType_T
        | core.RectProps
        | dict[str, Any]
        | core.ArrowProps
        | core.TextProps
        | core.RuleProps
        | core.TickProps
        | core.LinkProps
        | core.PointProps
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            mark (MarkType_T | RectProps | dict[str, Any] | ArrowProps | TextProps | RuleProps | TickProps | LinkProps | PointProps): The graphical mark presenting the data objects.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): The background of the view, including fill, stroke, and stroke width.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "mark": mark,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class LayerPropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        layer: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            layer (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``layer`` property.
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "layer": layer,
            "legends": legends,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        layer: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            layer (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``layer`` property.
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "layer": layer,
            "legends": legends,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        layer: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            layer (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``layer`` property.
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "layer": layer,
            "legends": legends,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class HConcatPropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        hconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            hconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``hconcat`` property.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "hconcat": hconcat,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        hconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            hconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``hconcat`` property.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "hconcat": hconcat,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        hconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            hconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``hconcat`` property.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "hconcat": hconcat,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class VConcatPropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        vconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            vconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``vconcat`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "vconcat": vconcat,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        vconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            vconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``vconcat`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "vconcat": vconcat,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        vconcat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            vconcat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``vconcat`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "vconcat": vconcat,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class ConcatPropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        concat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            columns (float): The number of columns in the grid.
            concat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``concat`` property.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "columns": columns,
            "concat": concat,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        concat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            columns (float): The number of columns in the grid.
            concat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``concat`` property.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "columns": columns,
            "concat": concat,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        concat: Sequence[
            core.UnitSpec
            | dict[str, Any]
            | core.LayerSpec
            | core.MultiscaleSpec
            | core.VConcatSpec
            | core.HConcatSpec
            | core.ConcatSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        separator: bool
        | core.SeparatorProps
        | SeparatorPropsKwds
        | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            columns (float): The number of columns in the grid.
            concat (Sequence[UnitSpec | dict[str, Any] | LayerSpec | MultiscaleSpec | VConcatSpec | HConcatSpec | ConcatSpec | ImportSpec]): Schema-defined ``concat`` property.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
            spacing (float): The gap between the views, in pixels.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "columns": columns,
            "concat": concat,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "name": name,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "separator": separator,
            "spacing": spacing,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class MultiscalePropertiesMixin:
    """Schema-derived top-level property builder."""

    def __init__(
        self,
        multiscale: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        stops: Sequence[float | core.ExprRef | dict[str, Any]]
        | core.FadedMultiscaleStops
        | dict[str, Any]
        | core.TransitionedMultiscaleStops
        | UndefinedType = Undefined,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
        schema_url: str | None = None,
    ) -> None:
        """Initialize a schema-derived top-level specification.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            multiscale (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``multiscale`` property.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            stops (Sequence[float | ExprRef | dict[str, Any]] | FadedMultiscaleStops | dict[str, Any] | TransitionedMultiscaleStops): Stop definition that controls transitions between the multiscale levels. - ``number[]`` is shorthand for ``{ metric: "unitsPerPixel", values: ... }`` - ``(number | ExprRef)[]`` supports mixed constants and expressions - Object form allows configuring metric, channel, and fade.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
            schema_url (str | None): Root JSON Schema URL. Uses the packaged default when omitted.
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "multiscale": multiscale,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "stops": stops,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]

    def properties(
        self,
        *,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        multiscale: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        stops: Sequence[float | core.ExprRef | dict[str, Any]]
        | core.FadedMultiscaleStops
        | dict[str, Any]
        | core.TransitionedMultiscaleStops
        | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a new specification with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            multiscale (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``multiscale`` property.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            stops (Sequence[float | ExprRef | dict[str, Any]] | FadedMultiscaleStops | dict[str, Any] | TransitionedMultiscaleStops): Stop definition that controls transitions between the multiscale levels. - ``number[]`` is shorthand for ``{ metric: "unitsPerPixel", values: ... }`` - ``(number | ExprRef)[]`` supports mixed constants and expressions - Object form allows configuring metric, channel, and fade.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "multiscale": multiscale,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "stops": stops,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]

    def copy(
        self,
        *,
        deep: bool = True,
        assembly: str | UndefinedType = Undefined,
        axes: AxesKwds | UndefinedType = Undefined,
        background: str | UndefinedType = Undefined,
        baseUrl: str | UndefinedType = Undefined,
        config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        data: Any | UndefinedType = Undefined,
        datasets: dict[str, Any] | UndefinedType = Undefined,
        description: str | Sequence[str] | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
        genome: core.UrlGenomeConfig
        | dict[str, Any]
        | core.InlineGenomeConfig
        | core.GenomeConfigBase
        | UndefinedType = Undefined,
        genomes: dict[str, Any] | UndefinedType = Undefined,
        height: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        legends: LegendsKwds | UndefinedType = Undefined,
        multiscale: Sequence[
            core.LayerSpec
            | dict[str, Any]
            | core.UnitSpec
            | core.MultiscaleSpec
            | core.ImportSpec
        ]
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        opacity: float
        | core.DynamicOpacity
        | DynamicOpacityKwds
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
        padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
        params: Sequence[
            core.PlainValueParameter
            | dict[str, Any]
            | core.TransitionedValueParameter
            | core.ExprParameter
            | core.SelectionParameter
            | core.RulerParameter
        ]
        | UndefinedType = Undefined,
        resolve: ResolveKwds | UndefinedType = Undefined,
        scales: ScalesKwds | UndefinedType = Undefined,
        stops: Sequence[float | core.ExprRef | dict[str, Any]]
        | core.FadedMultiscaleStops
        | dict[str, Any]
        | core.TransitionedMultiscaleStops
        | UndefinedType = Undefined,
        templates: dict[str, Any] | UndefinedType = Undefined,
        theme: BuiltInThemeName_T
        | Sequence[BuiltInThemeName_T]
        | UndefinedType = Undefined,
        title: str | core.Title | TitleKwds | UndefinedType = Undefined,
        transform: Sequence[
            core.AlignmentMismatchesParams
            | dict[str, Any]
            | core.AggregateParams
            | core.CollectParams
            | core.CoverageParams
            | core.CoordinateLookupParams
            | core.CrossParams
            | core.Displace1DParams
            | core.FlattenDelimitedParams
            | core.FormulaParams
            | core.LookupParams
            | core.ExprFilterParams
            | core.SelectionFilterParams
            | core.AxisLabelLayoutParams
            | core.FilterScoredLabelsParams
            | core.FlattenParams
            | core.FlattenCompressedExonsParams
            | core.FlattenCigarParams
            | core.FlattenSequenceParams
            | core.IdentifierParams
            | core.LinearizeGenomicCoordinateParams
            | core.MeasureTextParams
            | core.TruncateTextParams
            | core.PackLegendLabelsParams
            | core.MergeFacetsParams
            | core.PileupParams
            | core.ProjectParams
            | core.RegexExtractParams
            | core.RegexFoldParams
            | core.SampleParams
            | core.SetIntersectionParams
            | core.StackParams
            | core.WindowParams
        ]
        | UndefinedType = Undefined,
        view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
        viewportHeight: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        viewportWidth: core.SizeDef
        | SizeDefKwds
        | float
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        visible: bool | UndefinedType = Undefined,
        width: core.SizeDef
        | SizeDefKwds
        | float
        | core.Step
        | StepKwds
        | core.ExprRef
        | dict[str, Any]
        | Literal["container"]
        | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a copy with updated top-level properties.

        Args:
            assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
            axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            background (str): Background color of the canvas.
            baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
            config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
            data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
            datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
            description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
            domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
            encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
            genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
            genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
            height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
            legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            multiscale (Sequence[LayerSpec | dict[str, Any] | UnitSpec | MultiscaleSpec | ImportSpec]): Schema-defined ``multiscale`` property.
            name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
            opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
            overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
            padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
            params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
            resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
            scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
            stops (Sequence[float | ExprRef | dict[str, Any]] | FadedMultiscaleStops | dict[str, Any] | TransitionedMultiscaleStops): Stop definition that controls transitions between the multiscale levels. - ``number[]`` is shorthand for ``{ metric: "unitsPerPixel", values: ... }`` - ``(number | ExprRef)[]`` supports mixed constants and expressions - Object form allows configuring metric, channel, and fade.
            templates (dict[str, Any]): Schema-defined ``templates`` property.
            theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
            title (str | Title | TitleKwds): View title.
            transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | Displace1DParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | AxisLabelLayoutParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
            view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
            viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
            viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
            visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
            width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
            zindex (float): Z-order among sibling views in a composition. Higher values render later. Views with equal values render in declaration order. This does not affect layout order. __Default value:__ ``0``
        """
        properties = {
            "assembly": assembly,
            "axes": axes,
            "background": background,
            "baseUrl": baseUrl,
            "config": config,
            "cursor": cursor,
            "data": data,
            "datasets": datasets,
            "description": description,
            "domainInert": domainInert,
            "encoding": encoding,
            "genome": genome,
            "genomes": genomes,
            "height": height,
            "legends": legends,
            "multiscale": multiscale,
            "name": name,
            "opacity": opacity,
            "overhang": overhang,
            "padding": padding,
            "params": params,
            "resolve": resolve,
            "scales": scales,
            "stops": stops,
            "templates": templates,
            "theme": theme,
            "title": title,
            "transform": transform,
            "view": view,
            "viewportHeight": viewportHeight,
            "viewportWidth": viewportWidth,
            "visible": visible,
            "width": width,
            "zindex": zindex,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]


class ConfigMethodMixin:
    """Schema-derived config methods for the handwritten chart API."""

    def configure(
        self,
        value: core.GenomeSpyConfig | GenomeSpyConfigKwds | None | object = Undefined,
        /,
        *,
        arrow: core.ArrowConfig | dict[str, Any] | UndefinedType = Undefined,
        axis: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisBottom: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisIndex: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLeft: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisLocus: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisNominal: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisOrdinal: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisQuantitative: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisRight: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisTop: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisX: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        axisY: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined,
        legend: core.LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        legendTrack: core.LegendConfig | LegendConfigKwds | UndefinedType = Undefined,
        link: core.LinkConfig | LinkConfigKwds | UndefinedType = Undefined,
        mark: core.MarkConfig | MarkConfigKwds | UndefinedType = Undefined,
        point: core.PointConfig | PointConfigKwds | UndefinedType = Undefined,
        range: core.RangeConfig | RangeConfigKwds | UndefinedType = Undefined,
        rect: core.RectConfig | RectConfigKwds | UndefinedType = Undefined,
        rule: core.RuleConfig | RuleConfigKwds | UndefinedType = Undefined,
        scale: core.ScaleConfig | ScaleConfigKwds | UndefinedType = Undefined,
        style: dict[str, Any] | UndefinedType = Undefined,
        text: core.TextConfig | TextConfigKwds | UndefinedType = Undefined,
        tick: core.TickConfig | dict[str, Any] | UndefinedType = Undefined,
        title: core.TitleConfig | TitleConfigKwds | UndefinedType = Undefined,
        view: core.ViewConfig | ViewConfigKwds | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with merged top-level config.

        Args:
            arrow (ArrowConfig | dict[str, Any]): Defaults for arrow marks.
            axis (AxisConfig | AxisConfigKwds): Defaults shared by all axes.
            axisBottom (AxisConfig | AxisConfigKwds): Defaults for bottom-oriented axes.
            axisIndex (AxisConfig | AxisConfigKwds): Defaults for axes that visualize GenomeSpy ``index`` scales.
            axisLeft (AxisConfig | AxisConfigKwds): Defaults for left-oriented axes.
            axisLocus (AxisConfig | AxisConfigKwds): Defaults for axes that visualize GenomeSpy ``locus`` scales.
            axisNominal (AxisConfig | AxisConfigKwds): Defaults for axes that visualize nominal data.
            axisOrdinal (AxisConfig | AxisConfigKwds): Defaults for axes that visualize ordinal data.
            axisQuantitative (AxisConfig | AxisConfigKwds): Defaults for axes that visualize quantitative data.
            axisRight (AxisConfig | AxisConfigKwds): Defaults for right-oriented axes.
            axisTop (AxisConfig | AxisConfigKwds): Defaults for top-oriented axes.
            axisX (AxisConfig | AxisConfigKwds): Defaults for x axes.
            axisY (AxisConfig | AxisConfigKwds): Defaults for y axes.
            legend (LegendConfig | LegendConfigKwds): Defaults shared by all legends. Set ``disable`` to ``true`` to suppress automatic legend creation by default.
            legendTrack (LegendConfig | LegendConfigKwds): Defaults for legends of track-like views that use ``index`` or ``locus`` scales on the x channel. __Default value:__ ``{ "style": "track-bottom-legend" }``
            link (LinkConfig | LinkConfigKwds): Defaults for link marks.
            mark (MarkConfig | MarkConfigKwds): Defaults shared by all mark types.
            point (PointConfig | PointConfigKwds): Defaults for point marks.
            range (RangeConfig | RangeConfigKwds): Named reusable ranges for channels such as ``shape``, ``size``, and color.
            rect (RectConfig | RectConfigKwds): Defaults for rect marks.
            rule (RuleConfig | RuleConfigKwds): Defaults for rule marks.
            scale (ScaleConfig | ScaleConfigKwds): Defaults for scale behavior and scale-type-specific buckets.
            style (dict[str, Any]): Named reusable style buckets that marks, axes, legends, titles, and views can reference through their ``style`` properties.
            text (TextConfig | TextConfigKwds): Defaults for text marks.
            tick (TickConfig | dict[str, Any]): Defaults for tick marks.
            title (TitleConfig | TitleConfigKwds): Defaults for view titles.
            view (ViewConfig | ViewConfigKwds): Defaults for view background styling, including fill, stroke, shadow, and z-order properties.
        """
        defined = {
            "arrow": arrow,
            "axis": axis,
            "axisBottom": axisBottom,
            "axisIndex": axisIndex,
            "axisLeft": axisLeft,
            "axisLocus": axisLocus,
            "axisNominal": axisNominal,
            "axisOrdinal": axisOrdinal,
            "axisQuantitative": axisQuantitative,
            "axisRight": axisRight,
            "axisTop": axisTop,
            "axisX": axisX,
            "axisY": axisY,
            "legend": legend,
            "legendTrack": legendTrack,
            "link": link,
            "mark": mark,
            "point": point,
            "range": range,
            "rect": rect,
            "rule": rule,
            "scale": scale,
            "style": style,
            "text": text,
            "tick": tick,
            "title": title,
            "view": view,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure(value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_arrow(
        self,
        value: core.ArrowConfig | dict[str, Any] | None | object = Undefined,
        /,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        direction: Literal["forward"]
        | Literal["reverse"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        headAngle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        headNotchAngle: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headPlacement: Literal["inside"]
        | Literal["outside"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headShape: Literal["triangle"]
        | Literal["open"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headSpacing: float
        | None
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        headWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minStemLength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float
        | core.ArrowRelativeSize
        | dict[str, Any]
        | core.ExprRef
        | UndefinedType = Undefined,
        startNotch: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stem: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``arrow`` config updated.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            direction (Literal['forward'] | Literal['reverse'] | ExprRef | dict[str, Any]): Direction of the arrowhead. ``"forward"`` places the arrowhead at the secondary endpoint (``x2``, ``y2``). ``"reverse"`` places it at the primary endpoint (``x``, ``y``). For data-driven direction, use the ``direction`` encoding channel. __Default value:__ ``"forward"``
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            headAngle (float | ExprRef | dict[str, Any]): Angle in degrees between the arrow axis and an outer edge of the arrowhead. Smaller values produce longer, narrower heads. Larger values produce shorter, blunter heads. Values are clamped to ``[1, 90]``. __Default value:__ ``45``
            headNotchAngle (float | ExprRef | dict[str, Any]): Angle in degrees between the arrow axis and the arrowhead notch edge. ``90`` places the notch point at the tip, producing a triangular head when ``headAngle`` is less than ``90``. Applies to ``"triangle"`` heads. ``"open"`` heads use ``headAngle`` for the notch edge as well. Values are clamped to ``[1, 90]``. __Default value:__ ``90``
            headPlacement (Literal['inside'] | Literal['outside'] | ExprRef | dict[str, Any]): Placement of the arrowhead relative to the encoded segment. ``"inside"`` keeps the whole arrowhead within the encoded segment. ``"outside"`` places the arrowhead beyond the encoded segment so that the head starts at the segment endpoint. __Default value:__ ``"inside"``
            headShape (Literal['triangle'] | Literal['open'] | ExprRef | dict[str, Any]): Shape of the arrowhead. ``"triangle"`` draws a filled head. ``"open"`` draws an open head whose thickness matches the resolved ``size``, even when ``stem`` is ``false``. __Default value:__ ``"triangle"``
            headSpacing (float | None | ExprRef | dict[str, Any]): Spacing between repeated arrowheads as a multiplier of resolved ``size``. The effective spacing is at least the rendered arrowhead footprint, including stroke. If ``null``, arrowheads are not repeated. __Default value:__ ``null``
            headWidth (float | ExprRef | dict[str, Any]): Width of the arrowhead as a multiplier of resolved ``size``. Values above ``1`` make the arrowhead wider than the stem. __Default value:__ ``3``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minSize (float | ExprRef | dict[str, Any]): Minimum resolved arrow stem thickness in pixels. Applies to numeric, band-relative, and encoded ``size`` values. __Default value:__ ``1``
            minStemLength (float | ExprRef | dict[str, Any]): Minimum visible length of the arrow stem in pixels. When a non-repeated arrow is too short for the configured shape and minimum stem length, the affected notch or head angle is made blunter toward 90 degrees. For ``"inside"`` placement, this applies to ``"triangle"`` heads and is measured from the start of the stem to where the stem meets the head notch edge. For ``"outside"`` placement, this applies when ``startNotch`` is ``true`` and is measured from the start notch to the head start. Has no effect when ``stem`` is ``false``. __Default value:__ ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            size (float | ArrowRelativeSize | dict[str, Any] | ExprRef): Arrow stem thickness in pixels, or as a fraction of the perpendicular band or view span for axis-aligned arrows. Numeric values are pixels. ``{ "band": 0.8 }`` resolves to 80% of the perpendicular band width, or 80% of the perpendicular view span when no band scale is available. Use ``channel`` to explicitly select the reference channel. Band-relative size is not supported for diagonal arrows. __Default value:__ ``8``
            startNotch (bool | ExprRef | dict[str, Any]): Whether to draw a notch at the start of the arrow. The start notch uses the same slope as the arrowhead edge. __Default value:__ ``false``
            stem (bool | ExprRef | dict[str, Any]): Whether to draw the arrow stem. When ``false``, the resolved ``size`` still controls open-head thickness. ``minStemLength`` has no effect when the stem is hidden. __Default value:__ ``true``
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "direction": direction,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "headAngle": headAngle,
            "headNotchAngle": headNotchAngle,
            "headPlacement": headPlacement,
            "headShape": headShape,
            "headSpacing": headSpacing,
            "headWidth": headWidth,
            "minBufferSize": minBufferSize,
            "minSize": minSize,
            "minStemLength": minStemLength,
            "opacity": opacity,
            "size": size,
            "startNotch": startNotch,
            "stem": stem,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("arrow", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axis`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axis", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_bottom(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisBottom`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisBottom", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_index(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisIndex`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisIndex", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_left(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisLeft`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisLeft", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_locus(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisLocus`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisLocus", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_nominal(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisNominal`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisNominal", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_ordinal(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisOrdinal`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisOrdinal", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_quantitative(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisQuantitative`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisQuantitative", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_right(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisRight`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisRight", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_top(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisTop`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisTop", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_x(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisX`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisX", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_axis_y(
        self,
        value: core.AxisConfig | AxisConfigKwds | None | object = Undefined,
        /,
        *,
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
        extraValues: Sequence[float] | UndefinedType = Undefined,
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
        labelFlush: bool | float | UndefinedType = Undefined,
        labelFlushOffset: float | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOverlap: bool
        | Literal["parity"]
        | Literal["greedy"]
        | UndefinedType = Undefined,
        labelPadding: float | UndefinedType = Undefined,
        labelSeparation: float | UndefinedType = Undefined,
        labels: bool | UndefinedType = Undefined,
        maxExtent: float | UndefinedType = Undefined,
        minExtent: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: AxisOrient_T | UndefinedType = Undefined,
        placement: AxisPlacement_T | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        tickCap: Literal["butt", "round", "square"] | UndefinedType = Undefined,
        tickColor: str | UndefinedType = Undefined,
        tickCount: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``axisY`` config updated.

        Args:
            chromGrid (bool): A boolean flag indicating if chromosome grid lines should be included as part of the axis. __Default value:__ ``false``
            chromGridCap (Literal['butt', 'round', 'square']): The stroke cap for the chromosome grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            chromGridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            chromGridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome grid mark lines.
            chromGridDashOffset (float): The pixel offset at which to start drawing with the chromosome grid mark dash array.
            chromGridFillEven (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridFillOdd (str): Fill color of odd chromosomes. __Default value:__ (none)
            chromGridOpacity (float): The opacity of the chromosome grid lines. __Default value:__ ``1``
            chromGridWidth (float): Width of the chromosome grid lines. __Default value:__ ``1``
            chromLabelAlign (Align_T): Horizontal text alignment of chromosome name labels. __Default value:__ ``"left"``
            chromLabelColor (str): Text color of chromosome name labels. __Default value:__ ``"black"``
            chromLabelFont (str): The font of chromosome name labels.
            chromLabelFontSize (float): Font size of chromosome name labels, in pixels. __Default value:__ ``13``
            chromLabelFontStyle (FontStyle_T): Font style of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelFontWeight (FontWeight_T): Font weight of chromosome name labels. __Default value:__ ``"normal"``
            chromLabelPadding (float): The padding, in pixels, between chromosome boundary ticks and chromosome name labels. __Default value:__ ``7``
            chromLabels (bool): A boolean flag indicating if chromosome name labels should be included as part of the genome axis. __Default value:__ ``true``
            chromTickColor (str): The color of chromosome boundary ticks. __Default value:__ ``"#989898"``
            chromTickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed chromosome boundary ticks. __Default value:__ ``[4, 2]``
            chromTickDashOffset (float): The pixel offset at which to start drawing with the chromosome tick dash array. __Default value:__ ``1``
            chromTickSize (float): The size in pixels of chromosome boundary ticks. __Default value:__ ``18``
            chromTickWidth (float): The width, in pixels, of chromosome boundary ticks. __Default value:__ ``1``
            chromTicks (bool): A boolean flag indicating if chromosome boundary ticks should be included as part of the genome axis. __Default value:__ ``true``
            domain (bool): A boolean flag indicating if the domain (the axis baseline) should be included as part of the axis. __Default value:__ ``true``
            domainCap (Literal['butt', 'round', 'square']): The stroke cap for the domain line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            domainColor (str): Color of axis domain line. __Default value:__ ``"gray"``.
            domainDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed domain lines.
            domainDashOffset (float): The pixel offset at which to start drawing with the domain dash array.
            domainWidth (float): Stroke width of axis domain line __Default value:__ ``1``
            extraValues (Sequence[float]): Additional tick and label values to include alongside automatically generated ticks on continuous scales. Values outside the visible scale range are omitted and duplicates are removed. During automatic overlap removal, these labels are reduced against other explicitly specified labels but take precedence over automatically generated labels. This property is ignored on discrete scales and when ``values`` is set.
            format (str): The format specifier pattern for axis labels. Must be a legal d3-format specifier.
            grid (bool): A boolean flag indicating if grid lines should be included as part of the axis. __Default value:__ ``false``
            gridCap (Literal['butt', 'round', 'square']): The stroke cap for the grid line's ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            gridColor (str): Color of grid lines. __Default value:__ ``lightgray``
            gridDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed grid mark lines.
            gridDashOffset (float): The pixel offset at which to start drawing with the grid mark dash array.
            gridOpacity (float): The opacity of the grid lines. __Default value:__ ``1``
            gridWidth (float): Width of the grid lines. __Default value:__ ``1``
            labelAlign (Align_T): Horizontal text alignment of axis tick labels, overriding the default setting for the current axis orientation.
            labelAngle (float): The rotation angle of the axis labels. __Default value:__ ``-90`` for nominal and ordinal fields; ``0`` otherwise.
            labelBaseline (Baseline_T): Vertical text baseline of axis tick labels, overriding the default setting for the current axis orientation. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, ``"bottom"``.
            labelColor (str): The color of the tick label, can be in hex color code or regular color name.
            labelFlush (bool | float): Indicates whether labels near the beginning or end of the axis should be aligned flush with the scale range. A number specifies the endpoint distance threshold in pixels. ``true`` uses a threshold of one pixel. Flushing is supported for quantitative, index, and locus axes. By default, it is enabled for non-zoomable x axes of these types. On a zoomable x axis with a configured bounded zoom extent, ticks matching the extent boundaries are flushed while they remain visible. Other zoomable ticks and y-axis ticks are not flushed by default. Flushing supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelFlushOffset (float): The number of pixels by which to move flush-adjusted labels outward from the axis range. __Default value:__ ``0``
            labelFont (str): The font of the tick label.
            labelFontSize (float): The font size of the label, in pixels.
            labelFontStyle (FontStyle_T): Font style of the title.
            labelFontWeight (FontWeight_T): Font weight of axis tick labels.
            labelLimit (float): Maximum allowed pixel width of axis tick labels. __Default value:__ ``180``
            labelOverlap (bool | Literal['parity'] | Literal['greedy']): The strategy for removing overlapping axis labels. ``true`` uses the ``"parity"`` strategy. ``"parity"`` removes every other label until the remaining labels no longer overlap. ``"greedy"`` keeps each label that does not overlap the previously retained label. ``false`` disables overlap removal. By default, overlap removal uses ``"parity"`` for linear-like continuous scales and ``"greedy"`` for logarithmic and symlog scales. It is disabled for discrete scales. Overlap removal supports label angles that are multiples of 90 degrees. The automatic behavior is disabled at other angles.
            labelPadding (float): The padding, in pixels, between axis and text labels. __Default value:__ ``2``
            labelSeparation (float): The minimum separation, in pixels, between retained axis labels. __Default value:__ ``2``
            labels (bool): A boolean flag indicating if labels should be included as part of the axis. __Default value:__ ``true``.
            maxExtent (float): The maximum extent in pixels that axis ticks and labels should use. This determines a maximum offset value for axis titles. __Default value:__ ``undefined``.
            minExtent (float): The minimum extent in pixels that axis ticks and labels should use. This determines a minimum offset value for axis titles. __Default value:__ ``30`` for y-axis; ``undefined`` for x-axis.
            offset (float): The orthogonal offset in pixels by which to displace the axis from its position along the edge of the chart.
            orient (AxisOrient_T): The orientation of the axis. One of ``"top"``, ``"bottom"``, ``"left"`` or ``"right"``. The orientation can be used to further specialize the axis type (e.g., a y axis oriented for the right edge of the chart). __Default value:__ ``"bottom"`` for x-axes and ``"left"`` for y-axes.
            placement (AxisPlacement_T): Placement of the axis relative to the plotting area. Outside axes reserve layout space outside the plot. Inside axes are mirrored into the plot and do not reserve external layout space. __Default value:__ ``"outside"``.
            style (str | Sequence[str] | None): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited axis styles.
            tickCap (Literal['butt', 'round', 'square']): The stroke cap for the tick lines' ending style. One of ``"butt"``, ``"round"`` or ``"square"``. __Default value:__ ``"butt"``
            tickColor (str): The color of the axis's tick. __Default value:__ ``"gray"``
            tickCount (float | ExprRef | dict[str, Any]): A desired number of ticks, for axes visualizing quantitative scales. The resulting number may be different so that values are "nice" (multiples of ``2``, ``5``, ``10``) and lie within the underlying scale's range. An expression reference can use ``axisLength`` for the current length of the axis in pixels. For example, ``{ "expr": "ceil(axisLength / 40)" }`` requests one tick per 40 pixels. __Default value:__ an expression based on ``axisLength``
            tickDash (Sequence[float]): An array of alternating [stroke, space] lengths for dashed tick mark lines.
            tickDashOffset (float): The pixel offset at which to start drawing with the tick mark dash array.
            tickMinStep (float): The minimum desired step between axis ticks, in terms of scale domain values. For example, a value of ``1`` indicates that ticks should not be less than 1 unit apart. If ``tickMinStep`` is specified, the ``tickCount`` value will be adjusted, if necessary, to enforce the minimum step value.
            tickSize (float): The size in pixels of axis ticks. __Default value:__ ``5``
            tickWidth (float): The width, in pixels, of ticks. __Default value:__ ``1``
            ticks (bool): Boolean value that determines whether the axis should include ticks. __Default value:__ ``true``
            title (str | None): A title for the axis. By default, the title is derived from the encoding title, field, or expression. Set to ``null`` to remove it.
            titleColor (str): Color of the title, can be in hex color code or regular color name.
            titleFit (Literal['point', 'range']): Fitting mode for the axis title. ``"point"`` anchors the title at the center of the axis without constraining its length. ``"range"`` constrains the title to the axis span using ranged text, allowing it to be squeezed to fit and kept visible inside scrollable viewports. __Default value:__ ``"point"``
            titleFont (str): Font of the title. (e.g., ``"Helvetica Neue"``).
            titleFontSize (float): Font size of the title.
            titleFontStyle (FontStyle_T): Font style of the title.
            titleFontWeight (FontWeight_T): Font weight of the title. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            titleOpacity (float): Opacity of the axis title.
            titlePadding (float): The padding, in pixels, between title and axis.
            values (Sequence[Any]): Explicitly set the visible axis tick and label values. During automatic overlap removal, these labels are reduced against each other but take precedence over automatically generated labels.
            zindex (float): Z-order of the axis relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``0``, or ``10`` when the view content is clipped or scrollable.
        """
        defined = {
            "chromGrid": chromGrid,
            "chromGridCap": chromGridCap,
            "chromGridColor": chromGridColor,
            "chromGridDash": chromGridDash,
            "chromGridDashOffset": chromGridDashOffset,
            "chromGridFillEven": chromGridFillEven,
            "chromGridFillOdd": chromGridFillOdd,
            "chromGridOpacity": chromGridOpacity,
            "chromGridWidth": chromGridWidth,
            "chromLabelAlign": chromLabelAlign,
            "chromLabelColor": chromLabelColor,
            "chromLabelFont": chromLabelFont,
            "chromLabelFontSize": chromLabelFontSize,
            "chromLabelFontStyle": chromLabelFontStyle,
            "chromLabelFontWeight": chromLabelFontWeight,
            "chromLabelPadding": chromLabelPadding,
            "chromLabels": chromLabels,
            "chromTickColor": chromTickColor,
            "chromTickDash": chromTickDash,
            "chromTickDashOffset": chromTickDashOffset,
            "chromTickSize": chromTickSize,
            "chromTickWidth": chromTickWidth,
            "chromTicks": chromTicks,
            "domain": domain,
            "domainCap": domainCap,
            "domainColor": domainColor,
            "domainDash": domainDash,
            "domainDashOffset": domainDashOffset,
            "domainWidth": domainWidth,
            "extraValues": extraValues,
            "format": format,
            "grid": grid,
            "gridCap": gridCap,
            "gridColor": gridColor,
            "gridDash": gridDash,
            "gridDashOffset": gridDashOffset,
            "gridOpacity": gridOpacity,
            "gridWidth": gridWidth,
            "labelAlign": labelAlign,
            "labelAngle": labelAngle,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFlush": labelFlush,
            "labelFlushOffset": labelFlushOffset,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOverlap": labelOverlap,
            "labelPadding": labelPadding,
            "labelSeparation": labelSeparation,
            "labels": labels,
            "maxExtent": maxExtent,
            "minExtent": minExtent,
            "offset": offset,
            "orient": orient,
            "placement": placement,
            "style": style,
            "tickCap": tickCap,
            "tickColor": tickColor,
            "tickCount": tickCount,
            "tickDash": tickDash,
            "tickDashOffset": tickDashOffset,
            "tickMinStep": tickMinStep,
            "tickSize": tickSize,
            "tickWidth": tickWidth,
            "ticks": ticks,
            "title": title,
            "titleColor": titleColor,
            "titleFit": titleFit,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleOpacity": titleOpacity,
            "titlePadding": titlePadding,
            "values": values,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("axisY", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_legend(
        self,
        value: core.LegendConfig | LegendConfigKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        disable: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        layout: core.LegendLayout | dict[str, Any] | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
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
        tickCount: float | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``legend`` config updated.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columnPadding (float): Padding between legend columns in pixels.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            disable (bool | ExprRef | dict[str, Any]): Disable automatic legend creation. Use ``legend: null`` on an encoding channel to remove that channel's legend. __Default value:__ ``false``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelAlign (Align_T): Horizontal alignment of legend labels.
            labelBaseline (Baseline_T): Baseline alignment of legend labels.
            labelColor (str): Legend label color.
            labelFont (str): Legend label font.
            labelFontSize (float): Legend label font size in pixels.
            labelFontStyle (FontStyle_T): Legend label font style.
            labelFontWeight (FontWeight_T): Legend label font weight.
            labelLimit (float): Maximum label text width in pixels.
            labelOffset (float): Offset between legend symbols and labels in pixels.
            layout (LegendLayout | dict[str, Any]): Layout of complete legends within each orientation region. A general direction or anchor applies to every region unless the orientation has its own override.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            rowPadding (float): Padding between legend rows in pixels.
            spacing (float): Spacing in pixels between legends collected into the same legend region.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolBaseFillColor (str): Base fill color for legend symbols when the legend does not encode fill.
            symbolBaseStrokeColor (str): Base stroke color for legend symbols when the legend does not encode stroke.
            symbolOffset (float): Offset applied to legend symbols in pixels.
            symbolSize (float): Symbol size in pixels squared.
            symbolStrokeWidth (float): Legend symbol stroke width in pixels.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleColor (str): Legend title color.
            titleFont (str): Legend title font.
            titleFontSize (float): Legend title font size in pixels.
            titleFontStyle (FontStyle_T): Legend title font style.
            titleFontWeight (FontWeight_T): Legend title font weight.
            titleLimit (float): Maximum title text width in pixels.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            titlePadding (float): Padding in pixels between the legend title and the legend body.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columnPadding": columnPadding,
            "columns": columns,
            "direction": direction,
            "disable": disable,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelAlign": labelAlign,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOffset": labelOffset,
            "layout": layout,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "rowPadding": rowPadding,
            "spacing": spacing,
            "style": style,
            "symbolBaseFillColor": symbolBaseFillColor,
            "symbolBaseStrokeColor": symbolBaseStrokeColor,
            "symbolOffset": symbolOffset,
            "symbolSize": symbolSize,
            "symbolStrokeWidth": symbolStrokeWidth,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleColor": titleColor,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleLimit": titleLimit,
            "titleOrient": titleOrient,
            "titlePadding": titlePadding,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("legend", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_legend_track(
        self,
        value: core.LegendConfig | LegendConfigKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columnPadding: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        disable: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelAlign: Align_T | UndefinedType = Undefined,
        labelBaseline: Baseline_T | UndefinedType = Undefined,
        labelColor: str | UndefinedType = Undefined,
        labelFont: str | UndefinedType = Undefined,
        labelFontSize: float | UndefinedType = Undefined,
        labelFontStyle: FontStyle_T | UndefinedType = Undefined,
        labelFontWeight: FontWeight_T | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        labelOffset: float | UndefinedType = Undefined,
        layout: core.LegendLayout | dict[str, Any] | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
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
        tickCount: float | UndefinedType = Undefined,
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
    ) -> Self:
        """Return a chart with ``legendTrack`` config updated.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columnPadding (float): Padding between legend columns in pixels.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            disable (bool | ExprRef | dict[str, Any]): Disable automatic legend creation. Use ``legend: null`` on an encoding channel to remove that channel's legend. __Default value:__ ``false``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelAlign (Align_T): Horizontal alignment of legend labels.
            labelBaseline (Baseline_T): Baseline alignment of legend labels.
            labelColor (str): Legend label color.
            labelFont (str): Legend label font.
            labelFontSize (float): Legend label font size in pixels.
            labelFontStyle (FontStyle_T): Legend label font style.
            labelFontWeight (FontWeight_T): Legend label font weight.
            labelLimit (float): Maximum label text width in pixels.
            labelOffset (float): Offset between legend symbols and labels in pixels.
            layout (LegendLayout | dict[str, Any]): Layout of complete legends within each orientation region. A general direction or anchor applies to every region unless the orientation has its own override.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            rowPadding (float): Padding between legend rows in pixels.
            spacing (float): Spacing in pixels between legends collected into the same legend region.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolBaseFillColor (str): Base fill color for legend symbols when the legend does not encode fill.
            symbolBaseStrokeColor (str): Base stroke color for legend symbols when the legend does not encode stroke.
            symbolOffset (float): Offset applied to legend symbols in pixels.
            symbolSize (float): Symbol size in pixels squared.
            symbolStrokeWidth (float): Legend symbol stroke width in pixels.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleColor (str): Legend title color.
            titleFont (str): Legend title font.
            titleFontSize (float): Legend title font size in pixels.
            titleFontStyle (FontStyle_T): Legend title font style.
            titleFontWeight (FontWeight_T): Legend title font weight.
            titleLimit (float): Maximum title text width in pixels.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            titlePadding (float): Padding in pixels between the legend title and the legend body.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columnPadding": columnPadding,
            "columns": columns,
            "direction": direction,
            "disable": disable,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelAlign": labelAlign,
            "labelBaseline": labelBaseline,
            "labelColor": labelColor,
            "labelFont": labelFont,
            "labelFontSize": labelFontSize,
            "labelFontStyle": labelFontStyle,
            "labelFontWeight": labelFontWeight,
            "labelLimit": labelLimit,
            "labelOffset": labelOffset,
            "layout": layout,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "rowPadding": rowPadding,
            "spacing": spacing,
            "style": style,
            "symbolBaseFillColor": symbolBaseFillColor,
            "symbolBaseStrokeColor": symbolBaseStrokeColor,
            "symbolOffset": symbolOffset,
            "symbolSize": symbolSize,
            "symbolStrokeWidth": symbolStrokeWidth,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleColor": titleColor,
            "titleFont": titleFont,
            "titleFontSize": titleFontSize,
            "titleFontStyle": titleFontStyle,
            "titleFontWeight": titleFontWeight,
            "titleLimit": titleLimit,
            "titleOrient": titleOrient,
            "titlePadding": titlePadding,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("legendTrack", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_link(
        self,
        value: core.LinkConfig | LinkConfigKwds | None | object = Undefined,
        /,
        *,
        arcFadingDistance: Sequence[float]
        | Literal[False]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        arcHeightFactor: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clampApex: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        linkShape: Literal["arc"]
        | Literal["diagonal"]
        | Literal["line"]
        | Literal["dome"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        maxChordLength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minArcHeight: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        noFadingOnPointSelection: bool
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical"]
        | Literal["horizontal"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        segments: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``link`` config updated.

        Args:
            arcFadingDistance (Sequence[float] | Literal[False] | ExprRef | dict[str, Any]): The range of the ``"arc"`` shape's fading distance in pixels. This property allows for making the arc's opacity fade out as it extends away from the chord. The fading distance is interpolated from one to zero between the interval defined by this property. Both ``false`` and ``[0, 0]`` disable fading. **Default value:** ``false``
            arcHeightFactor (float | ExprRef | dict[str, Any]): Scaling factor for the ``"arc``" shape's height. The default value ``1.0`` produces roughly circular arcs. **Default value:** ``1.0``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clampApex (bool | ExprRef | dict[str, Any]): Whether the apex of the ``"dome"`` shape is clamped to the viewport edge. When over a half of the dome is located outside the viewport, clamping allows for more accurate reading of the value encoded by the apex' position. **Default value:** ``false``
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            linkShape (Literal['arc'] | Literal['diagonal'] | Literal['line'] | Literal['dome'] | ExprRef | dict[str, Any]): The shape of the link path. The ``"arc"`` shape draws a circular arc between the two points. The apex of the arc resides on the left side of the line that connects the two points. The ``"dome"`` shape draws a vertical or horizontal arc with a specific height. The primary positional channel determines the apex of the arc and the secondary determines the endpoint placement. The ``"diagonal"`` shape draws an "S"-shaped curve between the two points. The ``"line"`` shape draws a straight line between the two points. See an example of the different shapes below. **Default value:** ``"arc"``
            maxChordLength (float | ExprRef | dict[str, Any]): The maximum length of ``"arc"`` shape's chord in pixels. The chord is the line segment between the two points that define the arc. Limiting the chord length serves two purposes when zooming in close enough: 1) it prevents the arc from becoming a straight line and 2) it mitigates the limited precision of floating point numbers in arc rendering. **Default value:** ``50000``
            minArcHeight (float | ExprRef | dict[str, Any]): The minimum height of an ``"arc"`` shape. Makes very short links more clearly visible. **Default value:** ``1.5``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minPickingSize (float | ExprRef | dict[str, Any]): The minimum picking size invisibly increases the stroke width or point diameter of marks when pointing them with the mouse cursor, making it easier to select them. The valus is the minimum size in pixels. **Default value:** ``3.0`` for ``"link"`` and ``2.0`` for ``"point"``
            noFadingOnPointSelection (bool | ExprRef | dict[str, Any]): Disables fading of the link when an mark instance is subject to any point selection. As the fading distance is unavailable as a visual channel, this property allows for enhancing the visibility of the selected links. **Default value:** ``true``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            orient (Literal['vertical'] | Literal['horizontal'] | ExprRef | dict[str, Any]): The orientation of the link path. Either ``"vertical"`` or ``"horizontal"``. Only applies to diagonal links. **Default value:** ``"vertical"``
            segments (float | ExprRef | dict[str, Any]): The number of segments in the bézier curve. Affects the rendering quality and performance. Use a higher value for a smoother curve. **Default value:** ``101``
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "arcFadingDistance": arcFadingDistance,
            "arcHeightFactor": arcHeightFactor,
            "buildIndex": buildIndex,
            "clampApex": clampApex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "linkShape": linkShape,
            "maxChordLength": maxChordLength,
            "minArcHeight": minArcHeight,
            "minBufferSize": minBufferSize,
            "minPickingSize": minPickingSize,
            "noFadingOnPointSelection": noFadingOnPointSelection,
            "opacity": opacity,
            "orient": orient,
            "segments": segments,
            "size": size,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("link", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_mark(
        self,
        value: core.MarkConfig | MarkConfigKwds | None | object = Undefined,
        /,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``mark`` config updated.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "minBufferSize": minBufferSize,
            "opacity": opacity,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("mark", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_point(
        self,
        value: core.PointConfig | PointConfigKwds | None | object = Undefined,
        /,
        *,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dy: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillGradientStrength: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        filled: bool | UndefinedType = Undefined,
        geometricZoomBound: float | UndefinedType = Undefined,
        inwardStroke: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minPickingSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        sampleFacetPadding: float | UndefinedType = Undefined,
        semanticScore: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        semanticZoomFraction: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shape: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``point`` config updated.

        Args:
            angle (float | ExprRef | dict[str, Any]): The rotation angle in degrees. **Default value:** ``0``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            dx (float | ExprRef | dict[str, Any]): Horizontal offset in pixels. **Default value:** ``0``
            dy (float | ExprRef | dict[str, Any]): Vertical offset in pixels. **Default value:** ``0``
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillGradientStrength (float | ExprRef | dict[str, Any]): Gradient strength controls the amount of the gradient eye-candy effect in the fill color. Valid values are between ``0`` and ``1``. **Default value:** ``0``
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            geometricZoomBound (float): Enables geometric zooming. The value is the base two logarithmic zoom level where the maximum point size is reached. **Default value:** ``0``
            inwardStroke (bool | ExprRef | dict[str, Any]): Should the stroke only grow inwards, e.g, the diameter/outline is not affected by the stroke width. Thus, a point that has a zero size has no visible stroke. This allows strokes to be used with geometric zoom, etc. **Default value:** ``false``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minPickingSize (float | ExprRef | dict[str, Any]): The minimum picking size invisibly increases the stroke width or point diameter of marks when pointing them with the mouse cursor, making it easier to select them. The valus is the minimum size in pixels. **Default value:** ``3.0`` for ``"link"`` and ``2.0`` for ``"point"``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            sampleFacetPadding (float): Additional padding used by sample facets. **Default value:** ``0.1``
            semanticScore (float | ExprRef | dict[str, Any]): The semantic score used by semantic zooming in the point mark. This is primarily intended for internal use. **Default value:** ``0``
            semanticZoomFraction (float | ExprRef | dict[str, Any]): TODO **Default value:** ``0.02``
            shape (str | ExprRef | dict[str, Any]): One of ``"circle"``, ``"square"``, ``"cross"``, ``"x"``, ``"+"``, ``"diamond"``, ``"triangle-up"``, ``"triangle-down"``, ``"triangle-right"``, ``"triangle-left"``, ``"tick-up"``, ``"tick-down"``, ``"tick-right"``, or ``"tick-left"``. The ``"x"`` and ``"+"`` shapes are stroke-only and use ``strokeWidth`` for their line thickness. **Default value:** ``"circle"``
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "angle": angle,
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "dx": dx,
            "dy": dy,
            "fill": fill,
            "fillGradientStrength": fillGradientStrength,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "geometricZoomBound": geometricZoomBound,
            "inwardStroke": inwardStroke,
            "minBufferSize": minBufferSize,
            "minPickingSize": minPickingSize,
            "opacity": opacity,
            "sampleFacetPadding": sampleFacetPadding,
            "semanticScore": semanticScore,
            "semanticZoomFraction": semanticZoomFraction,
            "shape": shape,
            "size": size,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("point", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_range(
        self,
        value: core.RangeConfig | RangeConfigKwds | None | object = Undefined,
        /,
        *,
        angle: Sequence[float] | UndefinedType = Undefined,
        diverging: str
        | core.SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        heatmap: str | core.SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        ramp: str | core.SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        shape: Sequence[str] | UndefinedType = Undefined,
        size: Sequence[float] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``range`` config updated.

        Args:
            angle (Sequence[float]): Named range for ``angle`` channels.
            diverging (str | SchemeParams | SchemeParamsKwds): Named range for diverging color encodings.
            heatmap (str | SchemeParams | SchemeParamsKwds): Named range for quantitative rect-like color encodings such as heatmaps.
            ramp (str | SchemeParams | SchemeParamsKwds): Named range for quantitative ramp color encodings.
            shape (Sequence[str]): Named range for ``shape`` channels.
            size (Sequence[float]): Named range for ``size`` channels.
        """
        defined = {
            "angle": angle,
            "diverging": diverging,
            "heatmap": heatmap,
            "ramp": ramp,
            "shape": shape,
            "size": size,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("range", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_rect(
        self,
        value: core.RectConfig | RectConfigKwds | None | object = Undefined,
        /,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadius: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cornerRadiusBottomLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusBottomRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cornerRadiusTopRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fill: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fillOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
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
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minHeight: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOffsetY: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        stroke: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeWidth: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``rect`` config updated.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cornerRadius (float | ExprRef | dict[str, Any]): Radius of the rounded corners. **Default value:** ``0``
            cornerRadiusBottomLeft (float | ExprRef | dict[str, Any]): Radius of the bottom left rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusBottomRight (float | ExprRef | dict[str, Any]): Radius of the bottom right rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusTopLeft (float | ExprRef | dict[str, Any]): Radius of the top left rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cornerRadiusTopRight (float | ExprRef | dict[str, Any]): Radius of the top right rounded corner. Has higher precedence than ``cornerRadius``. **Default value:** (None)
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            fill (str | ExprRef | dict[str, Any]): The fill color.
            fillOpacity (float | ExprRef | dict[str, Any]): The fill opacity. Value between ``0`` and ``1``.
            filled (bool): Whether the ``color`` represents the ``fill`` color (``true``) or the ``stroke`` color (``false``).
            hatch (Literal['none'] | Literal['diagonal'] | Literal['antiDiagonal'] | Literal['cross'] | Literal['vertical'] | Literal['horizontal'] | Literal['grid'] | Literal['dots'] | Literal['rings'] | Literal['ringsLarge'] | ExprRef | dict[str, Any]): A hatch pattern drawn inside the mark using the stroke width, color, and opacity. The pattern is aligned in screen space and scaled by the stroke width. **Default value:** ``"none"``
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minHeight (float | ExprRef | dict[str, Any]): The minimum height of a rectangle in pixels. The property clamps rectangles' heights. **Default value:** ``0``
            minOpacity (float | ExprRef | dict[str, Any]): Clamps the minimum size-dependent opacity. The property does not affect the ``opacity`` channel. Valid values are between ``0`` and ``1``. When a rectangle would be smaller than what is specified in ``minHeight`` and ``minWidth``, it is faded out proportionally. Example: a rectangle would be rendered as one pixel wide, but ``minWidth`` clamps it to five pixels. The rectangle is actually rendered as five pixels wide, but its opacity is multiplied by 0.2. With this setting, you can limit the factor to, for example, 0.5 to keep the rectangles more clearly visible. **Default value:** ``0``
            minWidth (float | ExprRef | dict[str, Any]): The minimum width of a rectangle in pixels. The property clamps rectangles' widths when the viewport is zoomed out. This property also reduces flickering of very narrow rectangles when zooming. The value should generally be at least one. **Default value:** ``1``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            shadowBlur (float | ExprRef | dict[str, Any]): The blur radius of the drop shadow in pixels. Higher values produce a more diffuse shadow. **Default value:** ``0``
            shadowColor (str | ExprRef | dict[str, Any]): The color of the drop shadow. Any valid CSS color string is allowed. **Default value:** ``"black"``
            shadowOffsetX (float | ExprRef | dict[str, Any]): The horizontal offset of the drop shadow in pixels. Positive values move the shadow to the right. **Default value:** ``0``
            shadowOffsetY (float | ExprRef | dict[str, Any]): The vertical offset of the drop shadow in pixels. Positive values move the shadow downward. **Default value:** ``0``
            shadowOpacity (float | ExprRef | dict[str, Any]): The opacity of the drop shadow. Value between ``0`` (fully transparent) and ``1`` (fully opaque). **Default value:** ``0`` (disabled)
            stroke (str | ExprRef | dict[str, Any]): The stroke color
            strokeOpacity (float | ExprRef | dict[str, Any]): The stroke opacity. Value between ``0`` and ``1``.
            strokeWidth (float | ExprRef | dict[str, Any]): The stroke width in pixels.
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cornerRadius": cornerRadius,
            "cornerRadiusBottomLeft": cornerRadiusBottomLeft,
            "cornerRadiusBottomRight": cornerRadiusBottomRight,
            "cornerRadiusTopLeft": cornerRadiusTopLeft,
            "cornerRadiusTopRight": cornerRadiusTopRight,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "filled": filled,
            "hatch": hatch,
            "minBufferSize": minBufferSize,
            "minHeight": minHeight,
            "minOpacity": minOpacity,
            "minWidth": minWidth,
            "opacity": opacity,
            "shadowBlur": shadowBlur,
            "shadowColor": shadowColor,
            "shadowOffsetX": shadowOffsetX,
            "shadowOffsetY": shadowOffsetY,
            "shadowOpacity": shadowOpacity,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("rect", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_rule(
        self,
        value: core.RuleConfig | RuleConfigKwds | None | object = Undefined,
        /,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``rule`` config updated.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minLength (float | ExprRef | dict[str, Any]): The minimum stroke length in pixels. Use this property to ensure that very short strokes remain visible even when the user zooms out. **Default value:** ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            size (float | ExprRef | dict[str, Any]): Stroke width of ``"link"`` and ``"rule"`` marks in pixels, the area of the bounding square of ``"point"`` mark, or the font size of ``"text"`` mark.
            strokeCap (Literal['butt'] | Literal['square'] | Literal['round'] | ExprRef | dict[str, Any]): The style of stroke ends. Available choices: ``"butt"``, ``"round``", and ``"square"``. **Default value:** ``"butt"``
            strokeDash (Sequence[float]): An array of of alternating stroke and gap lengths or ``null`` for solid strokes. **Default value:** ``null``
            strokeDashOffset (float): An offset for the stroke dash pattern. **Default value:** ``0``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "minBufferSize": minBufferSize,
            "minLength": minLength,
            "opacity": opacity,
            "size": size,
            "strokeCap": strokeCap,
            "strokeDash": strokeDash,
            "strokeDashOffset": strokeDashOffset,
            "style": style,
            "tooltip": tooltip,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("rule", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_scale(
        self,
        value: core.ScaleConfig | ScaleConfigKwds | None | object = Undefined,
        /,
        *,
        align: float | UndefinedType = Undefined,
        assembly: str
        | core.UrlGenomeDefinition
        | dict[str, Any]
        | core.InlineGenomeDefinition
        | UndefinedType = Undefined,
        base: float | UndefinedType = Undefined,
        bins: Sequence[float] | UndefinedType = Undefined,
        clamp: bool | UndefinedType = Undefined,
        constant: float | UndefinedType = Undefined,
        domain: ScalarDomain_T
        | Sequence[core.ChromosomalLocus | dict[str, Any]]
        | core.SelectionDomainRef
        | dict[str, Any]
        | core.ViewportDomainRef
        | core.ExprRef
        | Sequence[float | str | bool | core.ExprRef | dict[str, Any]]
        | UndefinedType = Undefined,
        domainMax: float | UndefinedType = Undefined,
        domainMid: float | UndefinedType = Undefined,
        domainMin: float | UndefinedType = Undefined,
        domainTransition: bool | UndefinedType = Undefined,
        exponent: float | UndefinedType = Undefined,
        index: dict[str, Any] | UndefinedType = Undefined,
        interpolate: ScaleInterpolate_T
        | core.ScaleInterpolateParams
        | ScaleInterpolateParamsKwds
        | UndefinedType = Undefined,
        locus: dict[str, Any] | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        nice: bool | float | dict[str, Any] | UndefinedType = Undefined,
        nominal: dict[str, Any] | UndefinedType = Undefined,
        nominalColorScheme: str
        | core.SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        numberingOffset: float | UndefinedType = Undefined,
        ordinal: dict[str, Any] | UndefinedType = Undefined,
        ordinalColorScheme: str
        | core.SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingInner: float | UndefinedType = Undefined,
        paddingOuter: float | UndefinedType = Undefined,
        quantitative: dict[str, Any] | UndefinedType = Undefined,
        quantitativeColorScheme: str
        | core.SchemeParams
        | SchemeParamsKwds
        | UndefinedType = Undefined,
        range: Sequence[float | str | core.ExprRef | dict[str, Any]]
        | str
        | UndefinedType = Undefined,
        reverse: bool | UndefinedType = Undefined,
        round: bool | UndefinedType = Undefined,
        scheme: str | core.SchemeParams | SchemeParamsKwds | UndefinedType = Undefined,
        type: ScaleType_T | UndefinedType = Undefined,
        zero: bool | UndefinedType = Undefined,
        zoom: bool | core.ZoomParams | ZoomParamsKwds | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``scale`` config updated.

        Args:
            align (float): The alignment of the steps within the scale range. This value must lie in the range ``[0,1]``. A value of ``0.5`` indicates that the steps should be centered within the range. A value of ``0`` or ``1`` may be used to shift the bands to one side, say to position them adjacent to an axis. __Default value:__ ``0.5``
            assembly (str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition): Genome assembly definition for locus scales. This can be: - A string reference to a named assembly (built-in or root-configured). - An inline anonymous assembly that defines either ``contigs`` or ``url``. If undefined, the default genome from the genome store is used.
            base (float): The logarithm base of the ``log`` scale (default ``10``).
            bins (Sequence[float]): An array of bin boundaries over the scale domain. If provided, axes and legends will use the bin boundaries to inform the choice of tick marks and text labels.
            clamp (bool): If ``true``, values that exceed the data domain are clamped to either the minimum or maximum range value __Default value:__ derived from the Vega-Lite scale config's ``clamp`` (``true`` by default).
            constant (float): A constant determining the slope of the symlog function around zero. Only used for ``symlog`` scales. __Default value:__ ``1``
            domain (ScalarDomain_T | Sequence[ChromosomalLocus | dict[str, Any]] | SelectionDomainRef | dict[str, Any] | ViewportDomainRef | ExprRef | Sequence[float | str | bool | ExprRef | dict[str, Any]]): Customized domain values. For quantitative fields, ``domain`` can take the form of a two-element array with minimum and maximum values. Vega-Lite piecewise scales can be created by providing a ``domain`` with more than two entries. For ordinal and nominal fields, ``domain`` can be an array that lists valid input values. The domain can also be defined by an expression reference that evaluates to the domain array. Array elements may also be expression references.
            domainMax (float): Sets the maximum value in the scale domain, overriding the ``domain`` property. This property is only intended for use with scales having continuous domains.
            domainMid (float): Inserts a single mid-point value into a two-element domain. The mid-point value must lie between the domain minimum and maximum values. This property can be useful for setting a midpoint for Vega-Lite diverging color scales. The domainMid property is only intended for use with scales supporting continuous, piecewise domains.
            domainMin (float): Sets the minimum value in the scale domain, overriding the domain property. This property is only intended for use with scales having continuous domains.
            domainTransition (bool): Controls whether domain updates are applied immediately or with a smooth transition. Set this to ``false`` to apply domain updates immediately. The default is ``true``, except for domains that include ``ExprRef``s, which default to ``false`` unless overridden. __Default value:__ ``true``, except ``false`` for ``ExprRef``-driven domains.
            exponent (float): The exponent of the ``pow`` scale.
            index (dict[str, Any]): Defaults for GenomeSpy's ``index`` scales.
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            locus (dict[str, Any]): Defaults for GenomeSpy's ``locus`` scales.
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            nominal (dict[str, Any]): Defaults for nominal scales.
            nominalColorScheme (str | SchemeParams | SchemeParamsKwds): Default color scheme for nominal color scales.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            ordinal (dict[str, Any]): Defaults for ordinal scales.
            ordinalColorScheme (str | SchemeParams | SchemeParamsKwds): Default color scheme for ordinal color scales.
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
            quantitative (dict[str, Any]): Defaults for quantitative scales.
            quantitativeColorScheme (str | SchemeParams | SchemeParamsKwds): Default color scheme for quantitative color scales when no named range such as ``"heatmap"`` or ``"ramp"`` applies.
            range (Sequence[float | str | ExprRef | dict[str, Any]] | str): The range of the scale. One of: - A string indicating a pre-defined named scale range from Vega-Lite (e.g., example, ``"symbol"``, or ``"diverging"``). - For Vega-Lite continuous scales, two-element array indicating minimum and maximum values, or an array with more than two entries for specifying a Vega-Lite piecewise scale. Array elements may also be expression references. - For Vega-Lite discrete and Vega-Lite discretizing scales, an array of desired output values. Array elements may also be expression references. __Notes:__ 1) For color scales you can also specify a color ``scheme`` instead of ``range``. 2) Any directly specified ``range`` for ``x`` and ``y`` channels will be ignored. Range can be customized via the view's corresponding Vega-Lite size (``width`` and ``height``).
            reverse (bool): If true, reverses the order of the scale range. __Default value:__ ``false``.
            round (bool): If ``true``, rounds numeric output values to integers. This can be helpful for snapping to the pixel grid. __Default value:__ ``false``.
            scheme (str | SchemeParams | SchemeParamsKwds): A string indicating a color Vega-Lite scheme name (e.g., ``"category10"`` or ``"blues"``) or a Vega-Lite scheme parameter object. Discrete color schemes may be used with Vega-Lite discrete or Vega-Lite discretizing scales. Continuous color schemes are intended for use with color scales. For the full list of supported schemes, please refer to the Vega Scheme reference.
            type (ScaleType_T): The type of scale. GenomeSpy follows the Vega-Lite scale model; the links below refer to the Vega-Lite documentation: 1) **Continuous Scales** -- mapping continuous domains to continuous output ranges (``"linear"``, ``"pow"``, ``"sqrt"``, ``"symlog"``, ``"log"``, ``"time"``, ``"utc"``). 2) **Discrete Scales** -- mapping discrete domains to discrete (``"ordinal"``) or continuous (``"band"`` and ``"point"``) output ranges. 3) **Discretizing Scales** -- mapping continuous domains to discrete output ranges ``"bin-ordinal"``, ``"quantile"``, ``"quantize"`` and ``"threshold"``. GenomeSpy also provides index and locus scales for sequence and genomic coordinates. __Default value:__ please see the Vega-Lite scale type table.
            zero (bool): If ``true``, ensures that a zero baseline value is included in the scale domain. __Default value:__ ``true`` for x and y channels if the quantitative field is not binned and no custom ``domain`` is provided; ``false`` otherwise. __Note:__ Log scales do not support ``zero``.
            zoom (bool | ZoomParams | ZoomParamsKwds): If ``true`` and the scale is used on a positional channel, it can bee zoomed and translated interactively.
        """
        defined = {
            "align": align,
            "assembly": assembly,
            "base": base,
            "bins": bins,
            "clamp": clamp,
            "constant": constant,
            "domain": domain,
            "domainMax": domainMax,
            "domainMid": domainMid,
            "domainMin": domainMin,
            "domainTransition": domainTransition,
            "exponent": exponent,
            "index": index,
            "interpolate": interpolate,
            "locus": locus,
            "name": name,
            "nice": nice,
            "nominal": nominal,
            "nominalColorScheme": nominalColorScheme,
            "numberingOffset": numberingOffset,
            "ordinal": ordinal,
            "ordinalColorScheme": ordinalColorScheme,
            "padding": padding,
            "paddingInner": paddingInner,
            "paddingOuter": paddingOuter,
            "quantitative": quantitative,
            "quantitativeColorScheme": quantitativeColorScheme,
            "range": range,
            "reverse": reverse,
            "round": round,
            "scheme": scheme,
            "type": type,
            "zero": zero,
            "zoom": zoom,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("scale", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_style(
        self,
        value: dict[str, Any],
    ) -> Self:
        """Return a chart with ``style`` config updated."""
        return self._configure_property("style", value)  # type: ignore[attr-defined, no-any-return]

    def configure_text(
        self,
        value: core.TextConfig | TextConfigKwds | None | object = Undefined,
        /,
        *,
        align: Align_T | UndefinedType = Undefined,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        fitToBand: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushX: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        flushY: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        logoLetters: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingX: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        paddingY: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        size: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        squeeze: bool | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        text: Scalar_T | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceBottom: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeDistanceTop: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthBottom: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthLeft: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthRight: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        viewportEdgeFadeWidthTop: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``text`` config updated.

        Args:
            align (Align_T): The horizontal alignment of the text. One of ``"left"``, ``"center"``, or ``"right"``. **Default value:** ``"left"``
            angle (float | ExprRef | dict[str, Any]): The rotation angle in degrees. **Default value:** ``0``
            baseline (Baseline_T): The vertical alignment of the text. One of ``"top"``, ``"middle"``, ``"bottom"``. **Default value:** ``"bottom"``
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            dx (float): The horizontal offset between the text and its anchor point, in pixels. Applied after the rotation by ``angle``.
            dy (float): The vertical offset between the text and its anchor point, in pixels. Applied after the rotation by ``angle``.
            fitToBand (bool | ExprRef | dict[str, Any]): If true, sets the secondary positional channel that allows the text to be squeezed (see the ``squeeze`` property). Can be used when: 1) ``"band"``, ``"index"``, or ``"locus"`` scale is being used and 2) only the primary positional channel is specified. **Default value:** ``false``
            flushX (bool | ExprRef | dict[str, Any]): If true, the text is kept inside the viewport when the range of ``x`` and ``x2`` intersect the viewport.
            flushY (bool | ExprRef | dict[str, Any]): If true, the text is kept inside the viewport when the range of ``y`` and ``y2`` intersect the viewport.
            font (str): The font typeface. GenomeSpy uses SDF versions of Google Fonts. Check their availability at the A-Frame Fonts repository. System fonts are **not** supported. **Default value:** ``"Lato"``
            fontStyle (FontStyle_T): The font style. Valid values: ``"normal"`` and ``"italic"``. **Default value:** ``"normal"``
            fontWeight (FontWeight_T): The font weight. The following strings and numbers are valid values: ``"thin"`` (``100``), ``"light"`` (``300``), ``"regular"`` (``400``), ``"normal"`` (``400``), ``"medium"`` (``500``), ``"bold"`` (``700``), ``"black"`` (``900``) **Default value:** ``"regular"``
            logoLetters (bool | ExprRef | dict[str, Any]): Stretch letters so that they can be used with sequence logos, etc...
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            paddingX (float | ExprRef | dict[str, Any]): The horizontal padding, in pixels, when the ``x2`` channel is used for ranged text. **Default value:** ``0``
            paddingY (float | ExprRef | dict[str, Any]): The vertical padding, in pixels, when the ``y2`` channel is used for ranged text. **Default value:** ``0``
            size (float | ExprRef | dict[str, Any]): The font size in pixels. **Default value:** ``11``
            squeeze (bool | ExprRef | dict[str, Any]): If the ``squeeze`` property is true and secondary positional channels (``x2`` and/or ``y2``) are used, the text is scaled to fit mark's width and/or height. **Default value:** ``true``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            text (Scalar_T | ExprRef | dict[str, Any]): The text to display. The format of numeric data can be customized by setting a format specifier to channel definition's ``format`` property. **Default value:** ``""``
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            viewportEdgeFadeDistanceBottom (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceBottom`` property.
            viewportEdgeFadeDistanceLeft (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceLeft`` property.
            viewportEdgeFadeDistanceRight (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceRight`` property.
            viewportEdgeFadeDistanceTop (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeDistanceTop`` property.
            viewportEdgeFadeWidthBottom (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthBottom`` property.
            viewportEdgeFadeWidthLeft (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthLeft`` property.
            viewportEdgeFadeWidthRight (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthRight`` property.
            viewportEdgeFadeWidthTop (float | ExprRef | dict[str, Any]): Schema-defined ``viewportEdgeFadeWidthTop`` property.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2 (float | ExprRef | dict[str, Any]): The secondary position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2 (float | ExprRef | dict[str, Any]): The secondary position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "align": align,
            "angle": angle,
            "baseline": baseline,
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "dx": dx,
            "dy": dy,
            "fitToBand": fitToBand,
            "flushX": flushX,
            "flushY": flushY,
            "font": font,
            "fontStyle": fontStyle,
            "fontWeight": fontWeight,
            "logoLetters": logoLetters,
            "minBufferSize": minBufferSize,
            "opacity": opacity,
            "paddingX": paddingX,
            "paddingY": paddingY,
            "size": size,
            "squeeze": squeeze,
            "style": style,
            "text": text,
            "tooltip": tooltip,
            "viewportEdgeFadeDistanceBottom": viewportEdgeFadeDistanceBottom,
            "viewportEdgeFadeDistanceLeft": viewportEdgeFadeDistanceLeft,
            "viewportEdgeFadeDistanceRight": viewportEdgeFadeDistanceRight,
            "viewportEdgeFadeDistanceTop": viewportEdgeFadeDistanceTop,
            "viewportEdgeFadeWidthBottom": viewportEdgeFadeWidthBottom,
            "viewportEdgeFadeWidthLeft": viewportEdgeFadeWidthLeft,
            "viewportEdgeFadeWidthRight": viewportEdgeFadeWidthRight,
            "viewportEdgeFadeWidthTop": viewportEdgeFadeWidthTop,
            "x": x,
            "x2": x2,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2": y2,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("text", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_tick(
        self,
        value: core.TickConfig | dict[str, Any] | None | object = Undefined,
        /,
        *,
        buildIndex: bool | UndefinedType = Undefined,
        clip: bool
        | Literal["x"]
        | Literal["y"]
        | Literal["never"]
        | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        cullByVisibleRange: bool
        | Literal["x"]
        | Literal["y"]
        | UndefinedType = Undefined,
        cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        minBufferSize: float | UndefinedType = Undefined,
        minLength: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        opacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        orient: Literal["vertical", "horizontal"] | UndefinedType = Undefined,
        strokeCap: Literal["butt"]
        | Literal["square"]
        | Literal["round"]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        strokeDash: Sequence[float] | UndefinedType = Undefined,
        strokeDashOffset: float | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        thickness: float | UndefinedType = Undefined,
        tooltip: core.HandledTooltip
        | HandledTooltipKwds
        | None
        | Literal[False]
        | UndefinedType = Undefined,
        x: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        x2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        xOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        y2Offset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        yOffset: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``tick`` config updated.

        Args:
            buildIndex (bool): Whether the x channel should build an index for efficient subset rendering. If omitted, GenomeSpy enables indexing automatically for positional x encodings.
            clip (bool | Literal['x'] | Literal['y'] | Literal['never']): Controls whether the mark is clipped to the UnitView's rectangle. The values ``"x"`` and ``"y"`` clip only in the corresponding screen-space direction. Inherited clipping from parent containers still applies unless ``"never"`` is used. __Default value:__ the direction of zoomable positional scales
            color (str | ExprRef | dict[str, Any]): Color of the mark. Affects either ``fill`` or ``stroke``, depending on the ``filled`` property.
            cullByVisibleRange (bool | Literal['x'] | Literal['y']): Hide point-like mark instances whose anchor falls outside the inherited visible range in the given screen-space direction.
            cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is over the mark. Mark cursor takes precedence over enclosing view cursors. __Default value:__ browser default
            minBufferSize (float): Minimum size for WebGL buffers (number of data items). Allows for using ``bufferSubData()`` to update graphics. This property is intended for internal use.
            minLength (float | ExprRef | dict[str, Any]): The minimum stroke length in pixels. Use this property to ensure that very short strokes remain visible even when the user zooms out. **Default value:** ``0``
            opacity (float | ExprRef | dict[str, Any]): Opacity of the mark. Affects ``fillOpacity`` or ``strokeOpacity``, depending on the ``filled`` property.
            orient (Literal['vertical', 'horizontal']): The orientation of the tick mark. If omitted, GenomeSpy infers the orientation when one positional channel uses a band-like scale and the other does not, or when the orthogonal channel is omitted. Specify ``orient`` explicitly when both ``x`` and ``y`` use band-like scales. **Default value:** inferred
            strokeCap (Literal['butt'] | Literal['square'] | Literal['round'] | ExprRef | dict[str, Any]): The style of stroke ends. Available choices: ``"butt"``, ``"round``", and ``"square"``. **Default value:** ``"butt"``
            strokeDash (Sequence[float]): An array of of alternating stroke and gap lengths or ``null`` for solid strokes. **Default value:** ``null``
            strokeDashOffset (float): An offset for the stroke dash pattern. **Default value:** ``0``
            style (str | Sequence[str]): Named style reference(s) resolved from ``config.style``. If an array is provided, later styles override earlier ones.
            thickness (float): The thickness of the tick mark in pixels. Equivalent to the ``size`` of the underlying rule mark. **Default value:** ``1``
            tooltip (HandledTooltip | HandledTooltipKwds | None | Literal[False]): Tooltip handler. If ``null``, no tooltip is shown. If string, specifies the tooltip handler to use.
            x (float | ExprRef | dict[str, Any]): Position on the x axis.
            x2Offset (float | ExprRef | dict[str, Any]): Offset of the ``x2`` coordinate in logical pixels. When ``x2`` is implicit, it inherits ``xOffset`` unless this property is specified. **Default value:** inherited from ``xOffset`` for an implicit ``x2``, otherwise ``0``
            xOffset (float | ExprRef | dict[str, Any]): Offset of the ``x`` coordinate in logical pixels. **Default value:** ``0``
            y (float | ExprRef | dict[str, Any]): Position on the y axis.
            y2Offset (float | ExprRef | dict[str, Any]): Offset of the ``y2`` coordinate in logical pixels. When ``y2`` is implicit, it inherits ``yOffset`` unless this property is specified. **Default value:** inherited from ``yOffset`` for an implicit ``y2``, otherwise ``0``
            yOffset (float | ExprRef | dict[str, Any]): Offset of the ``y`` coordinate in logical pixels. **Default value:** ``0``
        """
        defined = {
            "buildIndex": buildIndex,
            "clip": clip,
            "color": color,
            "cullByVisibleRange": cullByVisibleRange,
            "cursor": cursor,
            "minBufferSize": minBufferSize,
            "minLength": minLength,
            "opacity": opacity,
            "orient": orient,
            "strokeCap": strokeCap,
            "strokeDash": strokeDash,
            "strokeDashOffset": strokeDashOffset,
            "style": style,
            "thickness": thickness,
            "tooltip": tooltip,
            "x": x,
            "x2Offset": x2Offset,
            "xOffset": xOffset,
            "y": y,
            "y2Offset": y2Offset,
            "yOffset": yOffset,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("tick", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_title(
        self,
        value: core.TitleConfig | TitleConfigKwds | None | object = Undefined,
        /,
        *,
        align: Align_T | UndefinedType = Undefined,
        anchor: TitleAnchor_T | UndefinedType = Undefined,
        angle: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        baseline: Baseline_T | UndefinedType = Undefined,
        color: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        dx: float | UndefinedType = Undefined,
        dy: float | UndefinedType = Undefined,
        font: str | UndefinedType = Undefined,
        fontSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        fontStyle: FontStyle_T | UndefinedType = Undefined,
        fontWeight: FontWeight_T | UndefinedType = Undefined,
        frame: TitleFrame_T | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: TitleOrient_T | UndefinedType = Undefined,
        reserve: bool | UndefinedType = Undefined,
        style: str | Sequence[str] | UndefinedType = Undefined,
        subtitle: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        subtitleFont: str | UndefinedType = Undefined,
        subtitleFontSize: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        subtitleFontStyle: FontStyle_T | UndefinedType = Undefined,
        subtitleFontWeight: FontWeight_T | UndefinedType = Undefined,
        subtitlePadding: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``title`` config updated.

        Args:
            align (Align_T): Horizontal text alignment for title text. One of ``"left"``, ``"center"``, or ``"right"``.
            anchor (TitleAnchor_T): The anchor position for placing the title and subtitle text. One of ``"start"``, ``"middle"``, or ``"end"``. For example, with an orientation of top these anchor positions map to a left-, center-, or right-aligned title.
            angle (float | ExprRef | dict[str, Any]): Angle in degrees of title and subtitle text.
            baseline (Baseline_T): Vertical text baseline for title and subtitle text. One of ``"alphabetic"`` (default), ``"top"``, ``"middle"``, or ``"bottom"``.
            color (str | ExprRef | dict[str, Any]): Text color for title text.
            dx (float): Delta offset for title and subtitle text x-coordinate.
            dy (float): Delta offset for title and subtitle text y-coordinate.
            font (str): Font name for title text.
            fontSize (float | ExprRef | dict[str, Any]): Font size in pixels for title text.
            fontStyle (FontStyle_T): Font style for title text.
            fontWeight (FontWeight_T): Font weight for title text. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            frame (TitleFrame_T): The reference frame for the title anchor. ``"group"`` anchors the title along the plot area. ``"bounds"`` anchors the title along the full bounds, including axes, legends, and other reserved space. __Default value:__ ``"group"``
            offset (float): The orthogonal offset in pixels by which to displace the title group from its position along the edge of the chart.
            orient (TitleOrient_T): Default title orientation (``"none"``, ``"top"``, ``"bottom"``, ``"left"``, or ``"right"``)
            reserve (bool): Whether the title reserves layout space outside the plot area. Reserved titles are placed outside axes, legends, and other guide space on the same side. Setting this to ``false`` lets the title render without affecting layout, enabling wilder layouts where titles may overlap nearby content. __Default value:__ ``true``
            style (str | Sequence[str]): A mark style property to apply to the title text mark. If not specified, a default style of ``"group-title"`` is applied.
            subtitle (str | ExprRef | dict[str, Any]): The subtitle text.
            subtitleColor (str | ExprRef | dict[str, Any]): Text color for subtitle text.
            subtitleFont (str): Font name for subtitle text.
            subtitleFontSize (float | ExprRef | dict[str, Any]): Font size in pixels for subtitle text.
            subtitleFontStyle (FontStyle_T): Font style for subtitle text.
            subtitleFontWeight (FontWeight_T): Font weight for subtitle text. This can be either a string (e.g ``"bold"``, ``"normal"``) or a number (``100``, ``200``, ``300``, ..., ``900`` where ``"normal"`` = ``400`` and ``"bold"`` = ``700``).
            subtitlePadding (float): Padding in pixels between title and subtitle text. __Default value:__ ``3``
            zindex (float): Z-order of the title relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``1``
        """
        defined = {
            "align": align,
            "anchor": anchor,
            "angle": angle,
            "baseline": baseline,
            "color": color,
            "dx": dx,
            "dy": dy,
            "font": font,
            "fontSize": fontSize,
            "fontStyle": fontStyle,
            "fontWeight": fontWeight,
            "frame": frame,
            "offset": offset,
            "orient": orient,
            "reserve": reserve,
            "style": style,
            "subtitle": subtitle,
            "subtitleColor": subtitleColor,
            "subtitleFont": subtitleFont,
            "subtitleFontSize": subtitleFontSize,
            "subtitleFontStyle": subtitleFontStyle,
            "subtitleFontWeight": subtitleFontWeight,
            "subtitlePadding": subtitlePadding,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("title", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def configure_view(
        self,
        value: core.ViewConfig | ViewConfigKwds | None | object = Undefined,
        /,
        *,
        continuousHeight: float | UndefinedType = Undefined,
        continuousWidth: float | UndefinedType = Undefined,
        discreteHeight: float | core.Step | StepKwds | UndefinedType = Undefined,
        discreteWidth: float | core.Step | StepKwds | UndefinedType = Undefined,
        fill: str | UndefinedType = Undefined,
        fillOpacity: float | UndefinedType = Undefined,
        shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        shadowOffsetX: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOffsetY: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        shadowOpacity: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        step: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        stroke: str | UndefinedType = Undefined,
        strokeOpacity: float | UndefinedType = Undefined,
        strokeWidth: float | UndefinedType = Undefined,
        strokeZindex: float | UndefinedType = Undefined,
        zindex: float | UndefinedType = Undefined,
    ) -> Self:
        """Return a chart with ``view`` config updated.

        Args:
            continuousHeight (float): The default height when the view has a continuous y scale. __Default value:__ ``"container"``
            continuousWidth (float): The default width when the view has a continuous x scale. __Default value:__ ``"container"``
            discreteHeight (float | Step | StepKwds): The default height when the view has a discrete y scale or no y scale. This may be a fixed height or a step size for each discrete domain value. __Default value:__ ``"container"``
            discreteWidth (float | Step | StepKwds): The default width when the view has a discrete x scale or no x scale. This may be a fixed width or a step size for each discrete domain value. __Default value:__ ``"container"``
            fill (str): Fill color of the view background.
            fillOpacity (float): Opacity of the view background fill.
            shadowBlur (float | ExprRef | dict[str, Any]): The blur radius of the drop shadow in pixels. Higher values produce a more diffuse shadow. **Default value:** ``0``
            shadowColor (str | ExprRef | dict[str, Any]): The color of the drop shadow. Any valid CSS color string is allowed. **Default value:** ``"black"``
            shadowOffsetX (float | ExprRef | dict[str, Any]): The horizontal offset of the drop shadow in pixels. Positive values move the shadow to the right. **Default value:** ``0``
            shadowOffsetY (float | ExprRef | dict[str, Any]): The vertical offset of the drop shadow in pixels. Positive values move the shadow downward. **Default value:** ``0``
            shadowOpacity (float | ExprRef | dict[str, Any]): The opacity of the drop shadow. Value between ``0`` (fully transparent) and ``1`` (fully opaque). **Default value:** ``0`` (disabled)
            step (float | ExprRef | dict[str, Any]): Default step size for discrete view sizes. __Default value:__ none
            stroke (str): Stroke color of the view background.
            strokeOpacity (float): Opacity of the view background stroke.
            strokeWidth (float): Stroke width of the view background border.
            strokeZindex (float): Z-order of the stroke relative to the view content. Values greater than ``0`` render the stroke after the view marks. Values less than or equal to ``0`` render before the marks. The default value depends on the element type.
            zindex (float): Z-order relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. The default value depends on the element type.
        """
        defined = {
            "continuousHeight": continuousHeight,
            "continuousWidth": continuousWidth,
            "discreteHeight": discreteHeight,
            "discreteWidth": discreteWidth,
            "fill": fill,
            "fillOpacity": fillOpacity,
            "shadowBlur": shadowBlur,
            "shadowColor": shadowColor,
            "shadowOffsetX": shadowOffsetX,
            "shadowOffsetY": shadowOffsetY,
            "shadowOpacity": shadowOpacity,
            "step": step,
            "stroke": stroke,
            "strokeOpacity": strokeOpacity,
            "strokeWidth": strokeWidth,
            "strokeZindex": strokeZindex,
            "zindex": zindex,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._configure_nested("view", value, **defined)  # type: ignore[attr-defined, no-any-return]


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
        """Add a ``alignmentMismatches`` transform.

        Args:
            cigar (Field_T): The CIGAR string. __Default value:__ ``"cigar"``
            copyFields (Sequence[str]): Top-level input fields copied to the emitted mismatch rows. If omitted, all input fields are copied. This can be used to avoid copying bulky fields such as read sequence or base quality arrays while still allowing the transform to read its input fields.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            md (Field_T): MD tag field. __Default value:__ ``"md"``
            quality (Field_T): Base quality field. __Default value:__ ``"qual"``
            sequence (Field_T): Read sequence field. __Default value:__ ``"seq"``
            start (Field_T): The read's reference start coordinate. __Default value:__ ``"start"``
        """
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
        """Add a ``aggregate`` transform.

        Args:
            as\\_ (Sequence[str]): The names for the output fields corresponding to each aggregated field. If not provided, names will be automatically created using the operation and field names (e.g., ``sum_field``, ``average_field``).
            description (str): A description of the transform step. Can be used for documentation and agent context.
            fields (Sequence[Field_T]): The data fields to apply aggregate functions to. This array should correspond with the ``ops`` and ``as`` arrays. If no fields or operations are specified, a count aggregation will be applied by default.
            groupby (Sequence[Field_T]): The fields by which to group the data. If these are not defined, all data objects will be grouped into a single category.
            ops (Sequence[AggregateOp_T]): The aggregation operations to be performed on the fields, such as ``"sum"``, ``"q1"``, ``"median"``, ``"q3"``, or ``"count"``.
        """
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
        """Add a ``collect`` transform.

        Args:
            description (str): A description of the transform step. Can be used for documentation and agent context.
            groupby (Sequence[Field_T]): Arranges the data into consecutive batches based on the groups. This is mainly intended for internal use so that faceted data can be handled as batches.
            sort (CompareParams | CompareParamsKwds): The sort order.
        """
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
        """Add a ``coverage`` transform.

        Args:
            end (Field_T): The field representing the end coordinate of the segment (exclusive).
            start (Field_T): The field representing the start coordinate of the segment (inclusive).
            as\\_ (str): The output field for the computed coverage.
            asChrom (str): The output field for the chromosome. **Default:** Same as ``chrom``
            asEnd (str): The output field for the end coordinate. **Default:** Same as ``end``
            asStart (str): The output field for the start coordinate. **Default:** Same as ``start``
            chrom (Field_T): An optional chromosome field that is passed through. TODO: groupby
            description (str): A description of the transform step. Can be used for documentation and agent context.
            weight (Field_T): A field representing an optional weight for the segment. Can be used with copy ratios, for example.
        """
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
        """Add a ``coordinateLookup`` transform.

        Args:
            from\\_ (CoordinateLookupInput | dict[str, Any]): The lazy side input and its optional transforms. Rows outside the loaded side-input domain are not passed through.
            key (Field_T | Sequence[Field_T]): Coordinate field or ``[chrom, pos]`` fields in the lazy side input. The same fields in the primary data determine both the exact match and whether a row is within the loaded side-input interval.
            as\\_ (Sequence[str]): Output field names. Defaults to ``values``. Requires an explicit ``values`` array.
            channel (PrimaryPositionalChannel_T): The positional channel shared with the lazy side input. __Default value:__ ``"x"``
            default (Any): Value written when no side-input row matches. __Default value:__ ``null``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            fields (Field_T | Sequence[Field_T] | None): Coordinate field or ``[chrom, pos]`` fields in the primary data. Defaults to ``key``.
            values (Sequence[Field_T] | None): Fields to copy from a matching side-input row. Defaults to all fields except ``key``.
        """
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

    def transform_cross(
        self,
        *,
        from_: core.CrossInput | dict[str, Any],
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``cross`` transform.

        Args:
            from\\_ (CrossInput | dict[str, Any]): The finite eager foreign data and its optional preprocessing transforms.
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
        transform: dict[str, Any] = {"type": "cross"}
        transform["from"] = from_
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_displace1d(
        self,
        *,
        length: float | Field_T | core.ExprRef | dict[str, Any],
        pos: Field_T,
        as_: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        extent: Sequence[float]
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        positionFactor: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``displace1d`` transform.

        Args:
            length (float | Field_T | ExprRef | dict[str, Any]): The full collision length, including any desired spacing, or a field containing that length. The value uses the same units as the scaled positions and output displacement. An expression provides a reactive scalar length shared by all rows.
            pos (Field_T): The field containing the original position. Input rows must be ordered by ascending ``pos * positionFactor``.
            as\\_ (str): The output field for signed displacement. __Default value:__ ``"displacement"``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            extent (Sequence[float] | ExprRef | dict[str, Any]): Preferred outer bounds for the placed collision intervals, expressed in the original ``pos`` coordinate system. The bounds are multiplied by ``positionFactor`` together with the item positions. When all items cannot fit, they remain non-overlapping and extend beyond the bounds by the minimum necessary amount. An expression can update the bounds reactively.
            positionFactor (float | ExprRef | dict[str, Any]): A multiplier applied to ``pos`` before placement. An expression can convert position units to logical pixels and react to zoom or layout changes. Use an ascending ``pos`` sort for a positive factor and a descending sort for a negative factor. Place a ``collect`` transform before this transform to buffer input for expression-driven updates. __Default value:__ ``1``
        """
        transform: dict[str, Any] = {"type": "displace1d"}
        transform["length"] = length
        transform["pos"] = pos
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
        if extent is not Undefined:
            transform["extent"] = extent
        if positionFactor is not Undefined:
            transform["positionFactor"] = positionFactor
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_flatten_delimited(
        self,
        *,
        field: Sequence[Field_T] | Field_T,
        separator: Sequence[str] | str,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flattenDelimited`` transform.

        Args:
            field (Sequence[Field_T] | Field_T): The field(s) to split and flatten
            separator (Sequence[str] | str): Separator(s) used on the field(s) TODO: Rename to delimiter
            as\\_ (Sequence[str] | str): The output field name(s) for the flattened field. **Default:** the input fields.
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
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
        """Add a ``formula`` transform.

        Args:
            as\\_ (str): The (new) field where the computed value is written to
            expr (str): An expression string
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
        transform: dict[str, Any] = {"type": "formula"}
        transform["as"] = as_
        transform["expr"] = expr
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_calculate(
        self,
        as_: str | UndefinedType = Undefined,
        calculate: str | UndefinedType = Undefined,
        **kwargs: str,
    ) -> Self:
        """Add a ``formula`` transform.

        Args:
            as\\_ (str): The (new) field where the computed value is written to
            calculate (str): An expression string
        """
        has_output = as_ is not Undefined
        has_value = calculate is not Undefined
        if has_output != has_value:
            raise TypeError(
                "transform_calculate requires 'as_' and 'calculate' together."
            )
        result = self
        if has_output and has_value:
            transform: dict[str, Any] = {"type": "formula"}
            transform["as"] = as_
            transform["expr"] = calculate
            result = result._append_transform(transform)  # type: ignore[attr-defined]
        for output, value in kwargs.items():
            transform = {"type": "formula"}
            transform["as"] = output
            transform["expr"] = value
            result = result._append_transform(transform)  # type: ignore[attr-defined]
        return result

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
        """Add a ``lookup`` transform.

        Args:
            from\\_ (UrlData | dict[str, Any] | InlineData | NamedData | DynamicCallbackData | LazyData | LookupSelfInput): The non-lazy data source that provides the lookup table, or the current input data.
            key (Field_T | Sequence[Field_T]): The key field or fields in the lookup table. When multiple fields are provided, they form a composite key.
            as\\_ (Sequence[str]): Output field names. Defaults to ``values``. Requires an explicit ``values`` array.
            default (Any): Value written when no side-input row matches. __Default value:__ ``null``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            fields (Field_T | Sequence[Field_T] | None): The fields in the input data to match against the lookup-table key. This array must have the same length and order as ``key``. Defaults to ``key``.
            values (Sequence[Field_T] | None): Fields to copy from a matching side-input row. Defaults to all fields except ``key``.
        """
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
        """Add a ``filter`` transform.

        Args:
            description (str): A description of the transform step. Can be used for documentation and agent context.
            empty (bool): If true, the filter retains all data objects when the selection is empty. **Default:** ``true``
            expr (str): An expression string. The data object is removed if the expression evaluates to false.
            fields (dict[str, Any]): An optional mapping of positional channels to fields. Used to determine which fields are checked against the selection intervals.
            param (str): A selection parameter. The data object is removed if it is not part of the selection.
        """
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

    def transform_axis_label_layout(
        self,
        *,
        channel: PrimaryPositionalChannel_T,
        labelAlign: Literal["left", "center", "right"],
        labelAngle: float,
        labelBaseline: Baseline_T,
        labelFlush: Literal[False] | float,
        labelFlushOffset: float,
        labelFlushZoomExtent: bool,
        labelFontSize: float,
        labelOffset: str,
        labelOverlap: Literal[False, "auto", "parity", "greedy"],
        labelSeparation: float,
        labelVisible: str,
        labelWidth: Field_T,
        chromLabelAlign: Literal["left", "center", "right"] | UndefinedType = Undefined,
        chromLabelPadding: float | UndefinedType = Undefined,
        chromLabelSpacing: float | UndefinedType = Undefined,
        chromLabelWidth: Field_T | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``axisLabelLayout`` transform.

        Args:
            channel (PrimaryPositionalChannel_T): Schema-defined ``channel`` property.
            labelAlign (Literal['left', 'center', 'right']): Schema-defined ``labelAlign`` property.
            labelAngle (float): Schema-defined ``labelAngle`` property.
            labelBaseline (Baseline_T): Schema-defined ``labelBaseline`` property.
            labelFlush (Literal[False] | float): Schema-defined ``labelFlush`` property.
            labelFlushOffset (float): Schema-defined ``labelFlushOffset`` property.
            labelFlushZoomExtent (bool): Schema-defined ``labelFlushZoomExtent`` property.
            labelFontSize (float): Schema-defined ``labelFontSize`` property.
            labelOffset (str): Schema-defined ``labelOffset`` property.
            labelOverlap (Literal[False, 'auto', 'parity', 'greedy']): Schema-defined ``labelOverlap`` property.
            labelSeparation (float): Schema-defined ``labelSeparation`` property.
            labelVisible (str): Schema-defined ``labelVisible`` property.
            labelWidth (Field_T): Schema-defined ``labelWidth`` property.
            chromLabelAlign (Literal['left', 'center', 'right']): Schema-defined ``chromLabelAlign`` property.
            chromLabelPadding (float): Schema-defined ``chromLabelPadding`` property.
            chromLabelSpacing (float): Schema-defined ``chromLabelSpacing`` property.
            chromLabelWidth (Field_T): Schema-defined ``chromLabelWidth`` property.
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
        transform: dict[str, Any] = {"type": "axisLabelLayout"}
        transform["channel"] = channel
        transform["labelAlign"] = labelAlign
        transform["labelAngle"] = labelAngle
        transform["labelBaseline"] = labelBaseline
        transform["labelFlush"] = labelFlush
        transform["labelFlushOffset"] = labelFlushOffset
        transform["labelFlushZoomExtent"] = labelFlushZoomExtent
        transform["labelFontSize"] = labelFontSize
        transform["labelOffset"] = labelOffset
        transform["labelOverlap"] = labelOverlap
        transform["labelSeparation"] = labelSeparation
        transform["labelVisible"] = labelVisible
        transform["labelWidth"] = labelWidth
        if chromLabelAlign is not Undefined:
            transform["chromLabelAlign"] = chromLabelAlign
        if chromLabelPadding is not Undefined:
            transform["chromLabelPadding"] = chromLabelPadding
        if chromLabelSpacing is not Undefined:
            transform["chromLabelSpacing"] = chromLabelSpacing
        if chromLabelWidth is not Undefined:
            transform["chromLabelWidth"] = chromLabelWidth
        if description is not Undefined:
            transform["description"] = description
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
        """Add a ``filterScoredLabels`` transform.

        Args:
            pos (Field_T): The field representing element's start position on the domain.
            score (Field_T): The field representing the score used for prioritization.
            width (Field_T): The field representing element's width in pixels.
            asMidpoint (str): Outputs the average of pos and pos2 as the midpoint of the element. This is useful for elements that have a width, such as transcripts. The midpoint is clamped to the visible region of the element.
            channel (Literal['x', 'y']): **Default:** ``"x"``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            lane (Field_T): An optional field representing element's lane, e.g., if transcripts are shown using a piled up layout. Each line is processed separately.
            padding (float): Padding (in pixels) around the element. **Default:** ``0``
            pos2 (Field_T): The field representing element's end position on the domain. If not specified, the ``pos`` field is used.
        """
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
        fields: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        *,
        description: str | UndefinedType = Undefined,
        index: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``flatten`` transform.

        Args:
            fields (Sequence[Field_T] | Field_T): The field(s) to flatten. If no field is defined, the data object itself is treated as an array to be flattened.
            as\\_ (Sequence[str] | str): The output field name(s) for the flattened field. **Default:** the input fields.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            index (str): The output field name for the zero-based index of the array values. If unspecified, an index field is not added.
        """
        transform: dict[str, Any] = {"type": "flatten"}
        if fields is not Undefined:
            transform["fields"] = fields
        if as_ is not Undefined:
            transform["as"] = as_
        if description is not Undefined:
            transform["description"] = description
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
        """Add a ``flattenCompressedExons`` transform.

        Args:
            as\\_ (Sequence[str]): Field names for the flattened exons. **Default:** ``["exonStart", "exonEnd"]``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            exons (Field_T): The field containing the exons. **Default:** ``"exons"``
            start (Field_T): Start coordinate of the gene body. **Default:** ``"start"``
        """
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
        """Add a ``flattenCigar`` transform.

        Args:
            cigar (Field_T): The CIGAR string. __Default value:__ ``"cigar"``
            copyFields (Sequence[str]): Top-level input fields copied to the emitted CIGAR operation rows. If omitted, all input fields are copied. This can be used to avoid copying bulky fields such as read sequence or base quality arrays while still allowing the transform to read its input fields.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            start (Field_T): The read's reference start coordinate. __Default value:__ ``"start"``
        """
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
        """Add a ``flattenSequence`` transform.

        Args:
            as\\_ (Sequence[str]): Name of the fields where the zero-based index number and flattened sequence letter are written to. **Default:** ``["pos", "sequence"]``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            field (Field_T): The field to flatten. **Default:** ``"sequence"``
        """
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
        """Add a ``identifier`` transform.

        Args:
            as\\_ (str): The field where the identifier is stored. __Default value:__ ``"_uniqueId"``
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
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
        """Add a ``linearizeGenomicCoordinate`` transform.

        Args:
            as\\_ (str | Sequence[str]): The output field or fields for linearized coordinates.
            chrom (Field_T): The chromosome/contig field
            pos (Field_T | Sequence[Field_T]): The field or fields that contain intra-chromosomal positions
            channel (Literal['x', 'y']): Get the genome assembly from the scale of the channel. **Default:** ``"x"``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            offset (float | Sequence[float]): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
        """
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
        """Add a ``measureText`` transform.

        Args:
            as\\_ (str): The output field where the measured width is written.
            field (Field_T): The field that contains the text to be measured.
            fontSize (float | ExprRef | dict[str, Any]): The font size in pixels.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            font (str): The font typeface. Uses the same asynchronously loaded SDF fonts as the ``"text"`` mark. **Default:** ``"Lato"``
            fontStyle (FontStyle_T): The font style. Valid values: ``"normal"`` and ``"italic"``. **Default:** ``"normal"``
            fontWeight (FontWeight_T): The font weight. The following strings and numbers are valid values: ``"thin"`` (``100``), ``"light"`` (``300``), ``"regular"`` (``400``), ``"normal"`` (``400``), ``"medium"`` (``500``), ``"bold"`` (``700``), ``"black"`` (``900``) **Default:** ``"regular"``
        """
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
        """Add a ``truncateText`` transform.

        Args:
            field (Field_T): The field that contains the text to be truncated.
            fontSize (float): The font size in pixels.
            as\\_ (str): The output field where the truncated text is written. **Default:** Same as ``field``.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            ellipsis (str): Text appended after truncation. **Default:** ``"..."``.
            font (str): The font typeface. Uses the same asynchronously loaded SDF fonts as the ``"text"`` mark. **Default:** ``"Lato"``
            fontStyle (FontStyle_T): The font style. Valid values: ``"normal"`` and ``"italic"``. **Default:** ``"normal"``
            fontWeight (FontWeight_T): The font weight. **Default:** ``"regular"``
            limit (float): Maximum text width in pixels.
        """
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
        """Add a ``packLegendLabels`` transform.

        Args:
            labelWidth (Field_T): The field that contains measured label width in pixels.
            columnPadding (float): Padding between columns in pixels. **Default:** ``0``
            columns (float): The number of columns in which to arrange entries.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            direction (Literal['vertical', 'horizontal']): The direction in which entries are laid out. **Default:** ``"vertical"``
            fontSize (float): Label font size in pixels. **Default:** ``10``
            labelOffset (float): Offset between the symbol and label in pixels. **Default:** ``0``
            rowPadding (float): Padding between rows in pixels. **Default:** ``0``
            symbolOffset (float): Horizontal offset for generated symbol coordinates in pixels. **Default:** ``0``
            symbolSize (float | Field_T): Symbol size in pixels squared, or a field containing per-entry symbol sizes in pixels squared. **Default:** ``100``
            symbolStrokeWidth (float | Field_T): Symbol stroke width in pixels, or a field containing per-entry stroke widths in pixels. **Default:** ``0``
            xOffset (float): Horizontal offset for all generated entry coordinates in pixels. **Default:** ``0``
            yExtent (float | ExprRef | dict[str, Any]): Height of the pixel-space layout area. When provided, the transform also emits inverted y coordinates for GenomeSpy's unit y range.
            yOffset (float): Vertical offset for all generated entry coordinates in pixels. **Default:** ``0``
        """
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
        """Add a ``mergeFacets`` transform.

        Args:
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
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
        """Add a ``pileup`` transform.

        Args:
            end (Field_T): The field representing the end coordinate of the segment (exclusive).
            start (Field_T): The field representing the start coordinate of the segment (inclusive).
            as\\_ (str): The output field name for the computed lane. **Default:** ``"lane"``.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            preference (Field_T): An optional field indicating the preferred lane. Use together with the ``preferredOrder`` property.
            preferredOrder (Sequence[str] | Sequence[float] | Sequence[bool]): The order of the lane preferences. The first element contains the value that should place the segment on the first lane and so forth. If the preferred lane is occupied, the first available lane is taken.
            spacing (float): The spacing between adjacent segments on the same lane in coordinate units. **Default:** ``1``.
        """
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
        """Add a ``project`` transform.

        Args:
            fields (Sequence[Field_T]): The fields to be projected.
            as\\_ (Sequence[str]): New names for the projected fields. If omitted, the names of the source fields are used.
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
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
        """Add a ``regexExtract`` transform.

        Args:
            as\\_ (str | Sequence[str]): The new field or an array of fields where the extracted values are written.
            field (Field_T): The source field
            regex (str): A valid JavaScript regular expression with at least one group. For example: ``"^Sample(\\d+)$"``. Read more at: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
            description (str): A description of the transform step. Can be used for documentation and agent context.
            skipInvalidInput (bool): Do not complain about invalid input. Just skip it and leave the new fields undefined on the affected datum. **Default:** ``false``
        """
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
        """Add a ``regexFold`` transform.

        Args:
            asValue (Sequence[str] | str): A new column name for the extracted values.
            columnRegex (Sequence[str] | str): A regular expression that matches to column names. The regex must have one capturing group that is used for extracting the key (e.g., a sample id) from the column name.
            asKey (str): **Default:** ``"sample"``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            skipRegex (str): An optional regex that matches to fields that should not be included in the new folded data objects.
        """
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
        size: float | UndefinedType = Undefined,
        *,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``sample`` transform.

        Args:
            size (float): The maximum sample size. **Default:** ``500``
            description (str): A description of the transform step. Can be used for documentation and agent context.
        """
        transform: dict[str, Any] = {"type": "sample"}
        if size is not Undefined:
            transform["size"] = size
        if description is not Undefined:
            transform["description"] = description
        return self._append_transform(transform)  # type: ignore[attr-defined, no-any-return]

    def transform_set_intersection(
        self,
        *,
        element: Field_T | Sequence[Field_T],
        set: Field_T,
        description: str | UndefinedType = Undefined,
        membership: Field_T | UndefinedType = Undefined,
    ) -> Self:
        """Add a ``setIntersection`` transform.

        Args:
            element (Field_T | Sequence[Field_T]): Field identifying an element. Multiple fields form a compound identifier.
            set (Field_T): Field identifying a set.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            membership (Field_T): Optional field containing a Boolean membership value. The values ``0`` and ``1`` are also accepted. When omitted, every input row denotes membership.
        """
        transform: dict[str, Any] = {"type": "setIntersection"}
        transform["element"] = element
        transform["set"] = set
        if description is not Undefined:
            transform["description"] = description
        if membership is not Undefined:
            transform["membership"] = membership
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
        """Add a ``stack`` transform.

        Args:
            groupby (Sequence[Field_T]): The fields to be used for forming groups for different stacks.
            as\\_ (Sequence[str]): Fields to write the stacked values. **Default:** ``["y0", "y1"]``
            baseField (Field_T): The field that contains the base or amino acid. Used for information content calculation when the offset is ``"information"``. The data objects that have ``null`` in the baseField are considered gaps and they are taken into account when scaling the the locus' information content.
            cardinality (float): Cardinality, e.g., the number if distinct bases or amino acids. Used for information content calculation when the offset is ``"information"``. **Default:** ``4``
            description (str): A description of the transform step. Can be used for documentation and agent context.
            field (Field_T): The field to stack. If no field is defined, a constant value of one is assumed.
            offset (Literal['zero', 'center', 'normalize', 'information']): How to offset the values in a stack. ``"zero"`` (default) starts stacking at 0. ``"center"`` centers the values around zero. ``"normalize"`` computes intra-stack percentages and normalizes the values to the range of ``[0, 1]``. ``"information"`` computes a layout for a sequence logo. The total height of the stack reflects the group's information content.
            sort (CompareParams | CompareParamsKwds): The sort order of data in each stack.
        """
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
        """Add a ``window`` transform.

        Args:
            ops (Sequence[WindowOp_T]): Window and aggregate operations to calculate. Entries align with ``fields``, ``params``, and ``as``.
            as\\_ (Sequence[str | None]): Output field names. A missing or ``null`` entry uses the operation and field name joined with an underscore, such as ``sum_score``. Operations without a field use only the operation name, such as ``rank``.
            description (str): A description of the transform step. Can be used for documentation and agent context.
            fields (Sequence[Field_T | None]): Input fields for operations that use a field. Use ``null`` for operations such as ``rank`` and ``count`` that do not use one.
            frame (Sequence[float | None]): Inclusive offsets from the current sorted row that define the window. ``null`` leaves the corresponding side unbounded. __Default value:__ ``[null, 0]``
            groupby (Sequence[Field_T]): Fields that divide the input into independent window partitions.
            ignorePeers (bool): Use row offsets without expanding frame boundaries to include sorted rows with equal values. __Default value:__ ``false``
            params (Sequence[float | None]): Optional operation parameters. ``lag`` and ``lead`` use an offset, while ``ntile`` and ``nth_value`` use a positive integer.
            sort (CompareParams | CompareParamsKwds): Fields used to sort rows before window functions are calculated. Without sorting, rows retain their input order and no rows are peers.
        """
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


__all__ = [
    "ConcatPropertiesMixin",
    "ConfigMethodMixin",
    "EncodingMethodMixin",
    "HConcatPropertiesMixin",
    "ImportedViewConstructorMixin",
    "LayerPropertiesMixin",
    "MarkMethodMixin",
    "MultiscalePropertiesMixin",
    "ResolutionMethodMixin",
    "TopLevelMergeMixin",
    "TransformMethodMixin",
    "UnitPropertiesMixin",
    "VConcatPropertiesMixin",
]
