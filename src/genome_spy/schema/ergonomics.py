"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Self, Literal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genome_spy.channels import DatumChannel, LocusChannel, ValueChannel

from genome_spy._expressions import DatumExpression
from genome_spy.schema._typing import (
    Align_T,
    AxisOrient_T,
    AxisPlacement_T,
    Baseline_T,
    ChannelWithScale_T,
    FieldName_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    PrimaryPositionalChannel_T,
    ScalarDomain_T,
    Scalar_T,
    ScaleInterpolate_T,
    ScaleType_T,
    SelectionType_T,
    SortOrder_T,
    TitleAnchor_T,
    TitleFrame_T,
    TitleOrient_T,
    Type_T,
)
from genome_spy.schema._kwds import (
    AxisConfigKwds,
    BindCheckboxKwds,
    BindInputKwds,
    BindRadioSelectKwds,
    BindRangeKwds,
    GenomeAxisKwds,
    LegendConfigKwds,
    LinkConfigKwds,
    MarkConfigKwds,
    ParseKwds,
    PointConfigKwds,
    RangeConfigKwds,
    RectConfigKwds,
    RuleConfigKwds,
    RulerConfigKwds,
    ScaleConfigKwds,
    ScaleInterpolateParamsKwds,
    ScaleKwds,
    SchemeParamsKwds,
    StepKwds,
    TextConfigKwds,
    TitleConfigKwds,
    ViewConfigKwds,
    ZoomParamsKwds,
)
from genome_spy.schemapi import Undefined, UndefinedType
from genome_spy.schema import core


class DatumChannelMethodMixin:
    """Schema-derived methods for ``datum`` channels."""

    def axis(
        self,
        value: core.GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
        """Return a channel with a axis configuration.

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
        return self._with_nested("axis", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def band(
        self,
        value: float,
    ) -> Self:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)  # type: ignore[attr-defined, no-any-return]

    def buildIndex(
        self,
        value: bool,
    ) -> Self:
        """Return a channel with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)  # type: ignore[attr-defined, no-any-return]

    def condition(
        self,
        value: Any,
    ) -> Self:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)  # type: ignore[attr-defined, no-any-return]

    def description(
        self,
        value: str,
    ) -> Self:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)  # type: ignore[attr-defined, no-any-return]

    def domainInert(
        self,
        value: bool,
    ) -> Self:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)  # type: ignore[attr-defined, no-any-return]

    def format(
        self,
        value: str,
    ) -> Self:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)  # type: ignore[attr-defined, no-any-return]

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Self:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)  # type: ignore[attr-defined, no-any-return]

    def scale(
        self,
        value: core.Scale | ScaleKwds | None | object = Undefined,
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
        interpolate: ScaleInterpolate_T
        | core.ScaleInterpolateParams
        | ScaleInterpolateParamsKwds
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        nice: bool | float | dict[str, Any] | UndefinedType = Undefined,
        numberingOffset: float | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingInner: float | UndefinedType = Undefined,
        paddingOuter: float | UndefinedType = Undefined,
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
        """Return a channel with a scale configuration.

        Args:
            align (float): The alignment of the steps within the scale range. This value must lie in the range ``[0,1]``. A value of ``0.5`` indicates that the steps should be centered within the range. A value of ``0`` or ``1`` may be used to shift the bands to one side, say to position them adjacent to an axis. __Default value:__ ``0.5``
            assembly (str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition): Genome assembly definition for locus scales. This can be: - A string reference to a named assembly (built-in or root-configured). - An inline anonymous assembly that defines either ``contigs`` or ``url``. If undefined, the default genome from the genome store is used.
            base (float): The logarithm base of the ``log`` scale (default ``10``).
            bins (Sequence[float]): An array of bin boundaries over the scale domain. If provided, axes and legends will use the bin boundaries to inform the choice of tick marks and text labels.
            clamp (bool): If ``true``, values that exceed the data domain are clamped to either the minimum or maximum range value __Default value:__ derived from the Vega-Lite scale config's ``clamp`` (``true`` by default).
            constant (float): A constant determining the slope of the symlog function around zero. Only used for ``symlog`` scales. __Default value:__ ``1``
            domain (ScalarDomain_T | Sequence[ChromosomalLocus | dict[str, Any]] | SelectionDomainRef | dict[str, Any] | ViewportDomainRef | ExprRef | Sequence[float | str | bool | ExprRef | dict[str, Any]]): Customized domain values. For quantitative fields, ``domain`` can take the form of a two-element array with minimum and maximum values. Vega-Lite piecewise scales can be created by providing a ``domain`` with more than two entries. For ordinal and nominal fields, ``domain`` can be an array that lists valid input values. The domain can also be defined by an expression reference that evaluates to the domain array. Array elements may also be expression references. All parameter names referenced by a scale, including selection-domain parameters, resolve from the view that owns the scale resolution. For a shared scale, declare controlling parameters on that owning composed view or an ancestor.
            domainMax (float): Sets the maximum value in the scale domain, overriding the ``domain`` property. This property is only intended for use with scales having continuous domains.
            domainMid (float): Inserts a single mid-point value into a two-element domain. The mid-point value must lie between the domain minimum and maximum values. This property can be useful for setting a midpoint for Vega-Lite diverging color scales. The domainMid property is only intended for use with scales supporting continuous, piecewise domains.
            domainMin (float): Sets the minimum value in the scale domain, overriding the domain property. This property is only intended for use with scales having continuous domains.
            domainTransition (bool): Controls whether domain updates are applied immediately or with a smooth transition. Set this to ``false`` to apply domain updates immediately. The default is ``true``, except for domains that include ``ExprRef``s, which default to ``false`` unless overridden. __Default value:__ ``true``, except ``false`` for ``ExprRef``-driven domains.
            exponent (float): The exponent of the ``pow`` scale.
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
            range (Sequence[float | str | ExprRef | dict[str, Any]] | str): The range of the scale. One of: - A string indicating a pre-defined named scale range from Vega-Lite (e.g., example, ``"symbol"``, or ``"diverging"``). - For Vega-Lite continuous scales, two-element array indicating minimum and maximum values, or an array with more than two entries for specifying a Vega-Lite piecewise scale. Array elements may also be expression references, which use the parameter scope of the view that owns the scale resolution. - For Vega-Lite discrete and Vega-Lite discretizing scales, an array of desired output values. Array elements may also be expression references, which use the parameter scope of the view that owns the scale resolution. __Notes:__ 1) For color scales you can also specify a color ``scheme`` instead of ``range``. 2) Any directly specified ``range`` for ``x`` and ``y`` channels will be ignored. Range can be customized via the view's corresponding Vega-Lite size (``width`` and ``height``).
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
            "interpolate": interpolate,
            "name": name,
            "nice": nice,
            "numberingOffset": numberingOffset,
            "padding": padding,
            "paddingInner": paddingInner,
            "paddingOuter": paddingOuter,
            "range": range,
            "reverse": reverse,
            "round": round,
            "scheme": scheme,
            "type": type,
            "zero": zero,
            "zoom": zoom,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("scale", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def title(
        self,
        value: str | None,
    ) -> Self:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)  # type: ignore[attr-defined, no-any-return]

    def type(
        self,
        value: Type_T,
    ) -> Self:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)  # type: ignore[attr-defined, no-any-return]


class ValueChannelMethodMixin:
    """Schema-derived methods for ``value`` channels."""

    def buildIndex(
        self,
        value: bool,
    ) -> Self:
        """Return a channel with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)  # type: ignore[attr-defined, no-any-return]

    def condition(
        self,
        value: Any,
    ) -> Self:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)  # type: ignore[attr-defined, no-any-return]

    def description(
        self,
        value: str,
    ) -> Self:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)  # type: ignore[attr-defined, no-any-return]

    def title(
        self,
        value: str | None,
    ) -> Self:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)  # type: ignore[attr-defined, no-any-return]


class LocusChannelMethodMixin:
    """Schema-derived nested setters for locus channels."""

    def axis(
        self,
        value: core.GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
        """Return a locus channel with an axis configuration.

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
        return self._with_nested("axis", value, **defined)  # type: ignore[attr-defined, no-any-return]

    def scale(
        self,
        value: core.Scale | ScaleKwds | None | object = Undefined,
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
        interpolate: ScaleInterpolate_T
        | core.ScaleInterpolateParams
        | ScaleInterpolateParamsKwds
        | UndefinedType = Undefined,
        name: str | UndefinedType = Undefined,
        nice: bool | float | dict[str, Any] | UndefinedType = Undefined,
        numberingOffset: float | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        paddingInner: float | UndefinedType = Undefined,
        paddingOuter: float | UndefinedType = Undefined,
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
        """Return a locus channel with a scale configuration.

        Args:
            align (float): The alignment of the steps within the scale range. This value must lie in the range ``[0,1]``. A value of ``0.5`` indicates that the steps should be centered within the range. A value of ``0`` or ``1`` may be used to shift the bands to one side, say to position them adjacent to an axis. __Default value:__ ``0.5``
            assembly (str | UrlGenomeDefinition | dict[str, Any] | InlineGenomeDefinition): Genome assembly definition for locus scales. This can be: - A string reference to a named assembly (built-in or root-configured). - An inline anonymous assembly that defines either ``contigs`` or ``url``. If undefined, the default genome from the genome store is used.
            base (float): The logarithm base of the ``log`` scale (default ``10``).
            bins (Sequence[float]): An array of bin boundaries over the scale domain. If provided, axes and legends will use the bin boundaries to inform the choice of tick marks and text labels.
            clamp (bool): If ``true``, values that exceed the data domain are clamped to either the minimum or maximum range value __Default value:__ derived from the Vega-Lite scale config's ``clamp`` (``true`` by default).
            constant (float): A constant determining the slope of the symlog function around zero. Only used for ``symlog`` scales. __Default value:__ ``1``
            domain (ScalarDomain_T | Sequence[ChromosomalLocus | dict[str, Any]] | SelectionDomainRef | dict[str, Any] | ViewportDomainRef | ExprRef | Sequence[float | str | bool | ExprRef | dict[str, Any]]): Customized domain values. For quantitative fields, ``domain`` can take the form of a two-element array with minimum and maximum values. Vega-Lite piecewise scales can be created by providing a ``domain`` with more than two entries. For ordinal and nominal fields, ``domain`` can be an array that lists valid input values. The domain can also be defined by an expression reference that evaluates to the domain array. Array elements may also be expression references. All parameter names referenced by a scale, including selection-domain parameters, resolve from the view that owns the scale resolution. For a shared scale, declare controlling parameters on that owning composed view or an ancestor.
            domainMax (float): Sets the maximum value in the scale domain, overriding the ``domain`` property. This property is only intended for use with scales having continuous domains.
            domainMid (float): Inserts a single mid-point value into a two-element domain. The mid-point value must lie between the domain minimum and maximum values. This property can be useful for setting a midpoint for Vega-Lite diverging color scales. The domainMid property is only intended for use with scales supporting continuous, piecewise domains.
            domainMin (float): Sets the minimum value in the scale domain, overriding the domain property. This property is only intended for use with scales having continuous domains.
            domainTransition (bool): Controls whether domain updates are applied immediately or with a smooth transition. Set this to ``false`` to apply domain updates immediately. The default is ``true``, except for domains that include ``ExprRef``s, which default to ``false`` unless overridden. __Default value:__ ``true``, except ``false`` for ``ExprRef``-driven domains.
            exponent (float): The exponent of the ``pow`` scale.
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
            range (Sequence[float | str | ExprRef | dict[str, Any]] | str): The range of the scale. One of: - A string indicating a pre-defined named scale range from Vega-Lite (e.g., example, ``"symbol"``, or ``"diverging"``). - For Vega-Lite continuous scales, two-element array indicating minimum and maximum values, or an array with more than two entries for specifying a Vega-Lite piecewise scale. Array elements may also be expression references, which use the parameter scope of the view that owns the scale resolution. - For Vega-Lite discrete and Vega-Lite discretizing scales, an array of desired output values. Array elements may also be expression references, which use the parameter scope of the view that owns the scale resolution. __Notes:__ 1) For color scales you can also specify a color ``scheme`` instead of ``range``. 2) Any directly specified ``range`` for ``x`` and ``y`` channels will be ignored. Range can be customized via the view's corresponding Vega-Lite size (``width`` and ``height``).
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
            "interpolate": interpolate,
            "name": name,
            "nice": nice,
            "numberingOffset": numberingOffset,
            "padding": padding,
            "paddingInner": paddingInner,
            "paddingOuter": paddingOuter,
            "range": range,
            "reverse": reverse,
            "round": round,
            "scheme": scheme,
            "type": type,
            "zero": zero,
            "zoom": zoom,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("scale", value, **defined)  # type: ignore[attr-defined, no-any-return]


def locus(
    chrom: FieldName_T,
    pos: FieldName_T | None = None,
    /,
    *,
    axis: core.GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
    band: float | UndefinedType = Undefined,
    description: str | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    offset: float | UndefinedType = Undefined,
    resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
    scale: core.Scale | ScaleKwds | None | UndefinedType = Undefined,
    title: str | None | UndefinedType = Undefined,
) -> LocusChannel:
    """Create a GenomeSpy chromosomal locus channel definition.

    Args:
        axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
        band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
        description (str): A description of the encoded position. Can be used for documentation and to explain the meaning of the channel mapping.
        domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
        offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
        resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
        scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
        title (str | None): A title for the field. If ``null``, the title will be removed.
    """
    properties = {
        "axis": axis,
        "band": band,
        "description": description,
        "domainInert": domainInert,
        "offset": offset,
        "resolutionChannel": resolutionChannel,
        "scale": scale,
        "title": title,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    definition: dict[str, Any] = {"chrom": chrom, "type": "locus", **defined}
    if pos is not None:
        definition["pos"] = pos
    from genome_spy.channels import LocusChannel

    return LocusChannel(definition)


def Locus(
    chrom: FieldName_T,
    pos: FieldName_T | None = None,
    /,
    *,
    axis: core.GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
    band: float | UndefinedType = Undefined,
    description: str | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    offset: float | UndefinedType = Undefined,
    resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
    scale: core.Scale | ScaleKwds | None | UndefinedType = Undefined,
    title: str | None | UndefinedType = Undefined,
) -> LocusChannel:
    """Create a GenomeSpy chromosomal locus channel definition.

    Args:
        axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
        band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
        description (str): A description of the encoded position. Can be used for documentation and to explain the meaning of the channel mapping.
        domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
        offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
        resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
        scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
        title (str | None): A title for the field. If ``null``, the title will be removed.
    """
    properties = {
        "axis": axis,
        "band": band,
        "description": description,
        "domainInert": domainInert,
        "offset": offset,
        "resolutionChannel": resolutionChannel,
        "scale": scale,
        "title": title,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    definition: dict[str, Any] = {"chrom": chrom, "type": "locus", **defined}
    if pos is not None:
        definition["pos"] = pos
    from genome_spy.channels import LocusChannel

    return LocusChannel(definition)


def compare(
    field: Sequence[Field_T] | Field_T | None = None,
    *,
    order: Sequence[SortOrder_T] | SortOrder_T | None = None,
) -> core.CompareParams:
    """Create a sort/compare definition.

    Args:
        field (Sequence[Field_T] | Field_T): The field(s) to sort by
        order (Sequence[SortOrder_T] | SortOrder_T): The order(s) to use: ``"ascending"`` (default), ``"descending"``.
    """
    properties = {"field": field, "order": order}
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not None
    }
    return core.CompareParams(**defined)


class DatumType(DatumExpression):
    """Build datum expressions or constant-datum channels."""

    def __call__(
        self,
        datum: Scalar_T | core.ExprRef | dict[str, Any],
        /,
        *,
        axis: core.GenomeAxis | GenomeAxisKwds | None | UndefinedType = Undefined,
        band: float | UndefinedType = Undefined,
        buildIndex: bool | UndefinedType = Undefined,
        condition: Any | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        domainInert: bool | UndefinedType = Undefined,
        format: str | UndefinedType = Undefined,
        resolutionChannel: ChannelWithScale_T | UndefinedType = Undefined,
        scale: core.Scale | ScaleKwds | None | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        type: Type_T | UndefinedType = Undefined,
    ) -> DatumChannel:
        """Create a constant-datum encoding channel.

        Args:
            axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            buildIndex (bool): Builds and index for efficient rendering of subsets of the data. This setting is useful when rendering large amounts of data and often only a small subset of the data is visible. An example of such a situation is a scatter plot spanning the whole genome. This setting implicitly sorts the data by the field assigned on the ``x`` channel.
            condition (Any): One or more value definition(s) with a parameter. __Note:__ A field definition's ``condition`` property can only contain conditional value definitions since GenomeSpy only allows at most one encoded field per encoding channel.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded datum. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
        """
        properties = {
            "datum": datum,
            "axis": axis,
            "band": band,
            "buildIndex": buildIndex,
            "condition": condition,
            "description": description,
            "domainInert": domainInert,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "scale": scale,
            "title": title,
            "type": type,
        }
        defined = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        from genome_spy.channels import DatumChannel

        return DatumChannel(defined)


datum = DatumType()


def value(
    value: Any,
    /,
    *,
    buildIndex: bool | UndefinedType = Undefined,
    condition: Any | UndefinedType = Undefined,
    description: str | UndefinedType = Undefined,
    title: str | None | UndefinedType = Undefined,
) -> ValueChannel:
    """Create a constant-value encoding channel.

    Args:
        buildIndex (bool): Builds and index for efficient rendering of subsets of the data. This setting is useful when rendering large amounts of data and often only a small subset of the data is visible. An example of such a situation is a scatter plot spanning the whole genome. This setting implicitly sorts the data by the field assigned on the ``x`` channel.
        condition (Any): A field definition or one or more value definition(s) with a parameter predicate.
        description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
        title (str | None): A title for the field. If ``null``, the title will be removed.
        value (Any): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
    """
    properties = {
        "value": value,
        "buildIndex": buildIndex,
        "condition": condition,
        "description": description,
        "title": title,
    }
    defined = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.channels import ValueChannel

    return ValueChannel(defined)


def title(
    text: str | core.ExprRef | dict[str, Any],
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
    subtitleFontSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    subtitleFontStyle: FontStyle_T | UndefinedType = Undefined,
    subtitleFontWeight: FontWeight_T | UndefinedType = Undefined,
    subtitlePadding: float | UndefinedType = Undefined,
    zindex: float | UndefinedType = Undefined,
) -> core.Title:
    """Create a chart title object.

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
        text (str | ExprRef | dict[str, Any]): The title text.
        zindex (float): Z-order of the title relative to the view content. Values greater than ``0`` render after the view marks. Values less than or equal to ``0`` render before the marks. __Default value:__ ``1``
    """
    properties = {
        "text": text,
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
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.Title(**defined)


def dynamic_opacity(
    *,
    channel: PrimaryPositionalChannel_T | Literal["auto"] | UndefinedType = Undefined,
    unitsPerPixel: Sequence[float | core.ExprRef | dict[str, Any]]
    | UndefinedType = Undefined,
    values: Sequence[float] | UndefinedType = Undefined,
) -> core.DynamicOpacity:
    """Create a zoom-dependent opacity definition.

    Args:
        channel (PrimaryPositionalChannel_T | Literal['auto']): The positional channel whose scale domain controls the opacity. If set to ``"auto"``, both ``x`` and ``y`` scales may contribute. If omitted, ``x`` is used when available and ``y`` is used as a fallback.
        unitsPerPixel (Sequence[float | ExprRef | dict[str, Any]]): Opacity stops expressed as units (base pairs, for example) per pixel. The values must be positive. Each stop is paired with an opacity in ``values`` at the same index. Stops can be constants or expression references.
        values (Sequence[float]): Opacity values that match the given ``unitsPerPixel`` stops. Values outside the stop range are clamped to the nearest stop.
    """
    properties = {
        "channel": channel,
        "unitsPerPixel": unitsPerPixel,
        "values": values,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.DynamicOpacity(**defined)


def data_format(
    *,
    columns: Sequence[str] | UndefinedType = Undefined,
    delimiter: str | UndefinedType = Undefined,
    parse: core.Parse | ParseKwds | None | UndefinedType = Undefined,
    property: str | UndefinedType = Undefined,
    type: str | UndefinedType = Undefined,
) -> core.DataFormat:
    """Create a data-format wrapper.

    Args:
        columns (Sequence[str]): Optional ordered list of field names for headerless BEDPE input. If omitted, BEDPE fields are resolved from the default BEDPE column order or from a matching header row when present.
        delimiter (str): The delimiter between records. The delimiter must be a single character (i.e., a single 16-bit code unit); so, ASCII delimiters are fine, but emoji delimiters are not.
        parse (Parse | ParseKwds | None): If set to ``null``, disable type inference based on the spec and only use type inference based on the data. Alternatively, a parsing directive object can be provided for explicit data types. Each property of the object corresponds to a field name, and the value to the desired data type (one of ``"number"``, ``"boolean"``, ``"date"``, or null (do not parse the field)). For example, ``"parse": {"modified_on": "date"}`` parses the ``modified_on`` field in each input record a Date value. For ``"date"``, we parse data based using Javascript's ``Date.parse()``. Specific date formats can be provided (e.g., ``{foo: "date:'%m%d%Y'"}``), using the d3-time-format syntax. UTC date format parsing is supported similarly (e.g., ``{foo: "utc:'%m%d%Y'"}``). See more about UTC parsing in the Vega-Lite UTC time documentation.
        property (str): The JSON property containing the desired data. This parameter can be used when the loaded JSON file may have surrounding structure or meta-data. For example ``"property": "values.features"`` is equivalent to retrieving ``json.values.features`` from the loaded JSON object.
        type (str): Type of input data: ``"json"``, ``"csv"``, ``"tsv"``, ``"dsv"``. __Default value:__ The default format type is determined by the extension of the file URL. Compression suffixes such as ``.gz`` are ignored during inference. If no extension is detected, ``"json"`` will be used by default.
    """
    properties = {
        "columns": columns,
        "delimiter": delimiter,
        "parse": parse,
        "property": property,
        "type": type,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.DataFormat(**defined)


def param(
    name: str,
    /,
    *,
    bind: core.BindCheckbox
    | BindCheckboxKwds
    | core.BindRadioSelect
    | BindRadioSelectKwds
    | core.BindRange
    | BindRangeKwds
    | core.BindInput
    | BindInputKwds
    | UndefinedType = Undefined,
    description: str | UndefinedType = Undefined,
    expr: str | UndefinedType = Undefined,
    persist: bool | UndefinedType = Undefined,
    push: Literal["outer"] | UndefinedType = Undefined,
    ruler: core.RulerConfig | RulerConfigKwds | UndefinedType = Undefined,
    select: SelectionType_T
    | core.PointSelectionConfig
    | dict[str, Any]
    | core.IntervalSelectionConfig
    | UndefinedType = Undefined,
    transition: core.LerpTransition | dict[str, Any] | UndefinedType = Undefined,
    value: core.RulerInitMapping | dict[str, Any] | UndefinedType = Undefined,
) -> core.Parameter:
    """Create a parameter definition.

    Args:
        bind (BindCheckbox | BindCheckboxKwds | BindRadioSelect | BindRadioSelectKwds | BindRange | BindRangeKwds | BindInput | BindInputKwds): Binds the parameter to an external input element such as a slider, selection list or radio button group.
        description (str): A description of the parameter. Can be used for documentation and to explain the meaning of the control or selection.
        expr (str): An expression for the value of the parameter. This expression may include other parameters, in which case the parameter will automatically update in response to upstream parameter changes.
        name (str): A unique name for the variable parameter. Parameter names should be valid JavaScript identifiers: they should contain only alphanumeric characters (or "$", or "_") and may not start with a digit. Reserved keywords that may not be used as parameter names are: "datum".
        persist (bool): Whether the parameter should be persisted in bookmarks and provenance. This primarily affects GenomeSpy App behavior. Set to ``false`` for ephemeral params (e.g., hover selections) or when the selection cannot be persisted due to missing ``encoding.key``. __Default value:__ ``true``
        push (Literal['outer']): Reuses the nearest same-named parameter in an ancestor scope and writes updates to it. Declare the target parameter on the ancestor first. This is useful when interaction in a child view updates state owned by a composed view, such as a parameter that controls a shared scale.
        ruler (RulerConfig | RulerConfigKwds): Tracks a domain coordinate and displays it as a ruler in compatible views.
        select (SelectionType_T | PointSelectionConfig | dict[str, Any] | IntervalSelectionConfig): Determines the default event processing and data query for the selection. GenomeSpy supports two selection types, following the Vega-Lite model: - ``"point"`` -- to select multiple discrete data values; the first value is selected on ``click`` and additional values toggled on shift-click. - ``"interval"`` -- to select a continuous range of data values on ``drag``.
        transition (LerpTransition | dict[str, Any]): Smoothly follows numeric expression output values.
        value (RulerInitMapping | dict[str, Any]): Initial ruler value.
    """
    properties = {
        "name": name,
        "bind": bind,
        "description": description,
        "expr": expr,
        "persist": persist,
        "push": push,
        "ruler": ruler,
        "select": select,
        "transition": transition,
        "value": value,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.Parameter(**defined)


def view(
    *,
    fill: str | UndefinedType = Undefined,
    fillOpacity: float | UndefinedType = Undefined,
    shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOffsetX: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOffsetY: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    stroke: str | UndefinedType = Undefined,
    strokeOpacity: float | UndefinedType = Undefined,
    strokeWidth: float | UndefinedType = Undefined,
    strokeZindex: float | UndefinedType = Undefined,
    style: str | Sequence[str] | UndefinedType = Undefined,
    zindex: float | UndefinedType = Undefined,
) -> core.ViewBackground:
    """Create a view background configuration.

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
    properties = {
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
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.ViewBackground(**defined)


def view_config(
    *,
    continuousHeight: float | UndefinedType = Undefined,
    continuousWidth: float | UndefinedType = Undefined,
    discreteHeight: float | core.Step | StepKwds | UndefinedType = Undefined,
    discreteWidth: float | core.Step | StepKwds | UndefinedType = Undefined,
    fill: str | UndefinedType = Undefined,
    fillOpacity: float | UndefinedType = Undefined,
    shadowBlur: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowColor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOffsetX: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOffsetY: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    shadowOpacity: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    step: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    stroke: str | UndefinedType = Undefined,
    strokeOpacity: float | UndefinedType = Undefined,
    strokeWidth: float | UndefinedType = Undefined,
    strokeZindex: float | UndefinedType = Undefined,
    zindex: float | UndefinedType = Undefined,
) -> core.ViewConfig:
    """Create a top-level view config object.

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
    properties = {
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
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    return core.ViewConfig(**defined)


def config(
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
) -> core.GenomeSpyConfig:
    """Create a top-level GenomeSpy config object.

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
    properties = {
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
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    if isinstance(defined.get("view"), core.ViewBackground):
        defined["view"] = core.ViewConfig(**defined["view"].to_dict(validate=False))
    return core.GenomeSpyConfig(**defined)


__all__ = [
    "Locus",
    "locus",
    "compare",
    "datum",
    "value",
    "title",
    "dynamic_opacity",
    "data_format",
    "param",
    "view",
    "view_config",
    "config",
    "DatumChannelMethodMixin",
    "LocusChannelMethodMixin",
    "ValueChannelMethodMixin",
]
