"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Literal

from genome_spy.channels import Channel, _MISSING, channel
from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType
from genome_spy.schema import core
from genome_spy.schema._typing import (
    Align_T,
    ArrowDirection_T,
    AxisOrient_T,
    AxisPlacement_T,
    Baseline_T,
    ChannelWithScale_T,
    FieldName_T,
    Field_T,
    FontStyle_T,
    FontWeight_T,
    LegendDirection_T,
    LegendOrient_T,
    LegendTitleOrient_T,
    ScalarDomain_T,
    Scalar_T,
    ScaleInterpolate_T,
    ScaleType_T,
    SortOrder_T,
    Type_T,
)
from genome_spy.schema.core import (
    CompareParams,
    ConditionalParameterMarkPropExprDefType,
    ConditionalParameterMarkPropExprDefTypeForShape,
    ConditionalParameterMarkPropFieldDefType,
    ConditionalParameterMarkPropFieldDefTypeForShape,
    ConditionalParameterScaleDatumDef,
    ConditionalParameterValueDefNumberExprRef,
    ConditionalParameterValueDefStringNullExprRef,
    ExprRef,
    GenomeAxis,
    Legend,
    Scale,
)
from genome_spy.schema._kwds import (
    CompareParamsKwds,
    GenomeAxisKwds,
    LegendKwds,
    ScaleInterpolateParamsKwds,
    ScaleKwds,
    SchemeParamsKwds,
    ZoomParamsKwds,
)


class Angle(Channel):
    """Generated wrapper for the ``angle`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``angle`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="angle", **defined)
        super().__init__(wrapped.definition, encoding_name="angle")

    def band(
        self,
        value: float,
    ) -> Angle:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> Angle:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Angle:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Angle:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Angle:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Angle:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Angle:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Angle:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Angle:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Angle:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Angle:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Angle:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Angle:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Angle:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Angle:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Color(Channel):
    """Generated wrapper for the ``color`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``color`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefStringNullExprRef | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | None | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="color", **defined)
        super().__init__(wrapped.definition, encoding_name="color")

    def band(
        self,
        value: float,
    ) -> Color:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> Color:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Color:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Color:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Color:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Color:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Color:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Color:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Color:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Color:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Color:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | None | ExprRef | dict[str, Any],
    ) -> Color:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Color:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Color:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Color:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Direction(Channel):
    """Generated wrapper for the ``direction`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``direction`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (ArrowDirection_T | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="direction", **defined)
        super().__init__(wrapped.definition, encoding_name="direction")

    def band(
        self,
        value: float,
    ) -> Direction:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Direction:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Direction:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Direction:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def field(
        self,
        value: str,
    ) -> Direction:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Direction:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Direction:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Direction:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Direction:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: ArrowDirection_T | ExprRef | dict[str, Any],
    ) -> Direction:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Direction:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Direction:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Dx(Channel):
    """Generated wrapper for the ``dx`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``dx`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded expression. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="dx", **defined)
        super().__init__(wrapped.definition, encoding_name="dx")

    def band(
        self,
        value: float,
    ) -> Dx:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> Dx:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Dx:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Dx:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Dx:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Dx:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Dx:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Dx:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Dx:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Dx:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Dx:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Dx:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Dx:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Dx:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Dx:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Dy(Channel):
    """Generated wrapper for the ``dy`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``dy`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded expression. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="dy", **defined)
        super().__init__(wrapped.definition, encoding_name="dy")

    def band(
        self,
        value: float,
    ) -> Dy:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> Dy:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Dy:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Dy:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Dy:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Dy:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Dy:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Dy:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Dy:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Dy:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Dy:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Dy:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Dy:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Dy:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Dy:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class FacetIndex(Channel):
    """Generated wrapper for the ``facetIndex`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``facetIndex`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="facetIndex", **defined)
        super().__init__(wrapped.definition, encoding_name="facetIndex")

    def description(
        self,
        value: str,
    ) -> FacetIndex:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> FacetIndex:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> FacetIndex:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> FacetIndex:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class Fill(Channel):
    """Generated wrapper for the ``fill`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``fill`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefStringNullExprRef | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | None | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="fill", **defined)
        super().__init__(wrapped.definition, encoding_name="fill")

    def band(
        self,
        value: float,
    ) -> Fill:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> Fill:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Fill:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Fill:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Fill:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Fill:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Fill:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Fill:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Fill:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Fill:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Fill:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | None | ExprRef | dict[str, Any],
    ) -> Fill:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Fill:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Fill:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Fill:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class FillOpacity(Channel):
    """Generated wrapper for the ``fillOpacity`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``fillOpacity`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="fillOpacity", **defined)
        super().__init__(wrapped.definition, encoding_name="fillOpacity")

    def band(
        self,
        value: float,
    ) -> FillOpacity:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> FillOpacity:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> FillOpacity:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> FillOpacity:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> FillOpacity:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> FillOpacity:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> FillOpacity:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> FillOpacity:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> FillOpacity:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> FillOpacity:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> FillOpacity:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> FillOpacity:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> FillOpacity:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> FillOpacity:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> FillOpacity:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Key(Channel):
    """Generated wrapper for the ``key`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``key`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="key", **defined)
        super().__init__(wrapped.definition, encoding_name="key")

    def description(
        self,
        value: str,
    ) -> Key:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> Key:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> Key:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Key:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class Opacity(Channel):
    """Generated wrapper for the ``opacity`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``opacity`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="opacity", **defined)
        super().__init__(wrapped.definition, encoding_name="opacity")

    def band(
        self,
        value: float,
    ) -> Opacity:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> Opacity:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Opacity:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Opacity:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Opacity:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Opacity:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Opacity:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Opacity:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Opacity:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Opacity:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Opacity:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Opacity:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Opacity:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Opacity:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Opacity:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Sample(Channel):
    """Generated wrapper for the ``sample`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``sample`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="sample", **defined)
        super().__init__(wrapped.definition, encoding_name="sample")

    def description(
        self,
        value: str,
    ) -> Sample:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> Sample:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> Sample:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Sample:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class Search(Channel):
    """Generated wrapper for the ``search`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``search`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="search", **defined)
        super().__init__(wrapped.definition, encoding_name="search")

    def description(
        self,
        value: str,
    ) -> Search:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> Search:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> Search:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Search:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class SemanticScore(Channel):
    """Generated wrapper for the ``semanticScore`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``semanticScore`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
            "type": type,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="semanticScore", **defined)
        super().__init__(wrapped.definition, encoding_name="semanticScore")

    def description(
        self,
        value: str,
    ) -> SemanticScore:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> SemanticScore:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> SemanticScore:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> SemanticScore:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> SemanticScore:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class Shape(Channel):
    """Generated wrapper for the ``shape`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``shape`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefTypeForShape | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefTypeForShape | ConditionalParameterValueDefStringNullExprRef | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | None | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="shape", **defined)
        super().__init__(wrapped.definition, encoding_name="shape")

    def band(
        self,
        value: float,
    ) -> Shape:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefTypeForShape
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> Shape:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Shape:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Shape:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Shape:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Shape:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Shape:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Shape:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Shape:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Shape:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Shape:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | None | ExprRef | dict[str, Any],
    ) -> Shape:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Shape:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Shape:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Shape:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Size(Channel):
    """Generated wrapper for the ``size`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``size`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="size", **defined)
        super().__init__(wrapped.definition, encoding_name="size")

    def band(
        self,
        value: float,
    ) -> Size:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> Size:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Size:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Size:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Size:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Size:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Size:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Size:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Size:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Size:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Size:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Size:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Size:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Size:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Size:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Stroke(Channel):
    """Generated wrapper for the ``stroke`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``stroke`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefStringNullExprRef | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | None | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="stroke", **defined)
        super().__init__(wrapped.definition, encoding_name="stroke")

    def band(
        self,
        value: float,
    ) -> Stroke:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefStringNullExprRef
        | Sequence[ConditionalParameterValueDefStringNullExprRef | dict[str, Any]],
    ) -> Stroke:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Stroke:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Stroke:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Stroke:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Stroke:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Stroke:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Stroke:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Stroke:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Stroke:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Stroke:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | None | ExprRef | dict[str, Any],
    ) -> Stroke:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Stroke:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> Stroke:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Stroke:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class StrokeOpacity(Channel):
    """Generated wrapper for the ``strokeOpacity`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``strokeOpacity`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="strokeOpacity", **defined)
        super().__init__(wrapped.definition, encoding_name="strokeOpacity")

    def band(
        self,
        value: float,
    ) -> StrokeOpacity:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> StrokeOpacity:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> StrokeOpacity:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> StrokeOpacity:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> StrokeOpacity:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> StrokeOpacity:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> StrokeOpacity:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> StrokeOpacity:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> StrokeOpacity:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> StrokeOpacity:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> StrokeOpacity:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> StrokeOpacity:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> StrokeOpacity:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> StrokeOpacity:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> StrokeOpacity:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class StrokeWidth(Channel):
    """Generated wrapper for the ``strokeWidth`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``strokeWidth`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="strokeWidth", **defined)
        super().__init__(wrapped.definition, encoding_name="strokeWidth")

    def band(
        self,
        value: float,
    ) -> StrokeWidth:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> StrokeWidth:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> StrokeWidth:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> StrokeWidth:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> StrokeWidth:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> StrokeWidth:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> StrokeWidth:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> StrokeWidth:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> StrokeWidth:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> StrokeWidth:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> StrokeWidth:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> StrokeWidth:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> StrokeWidth:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> StrokeWidth:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> StrokeWidth:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Text(Channel):
    """Generated wrapper for the ``text`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``text`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="text", **defined)
        super().__init__(wrapped.definition, encoding_name="text")

    def band(
        self,
        value: float,
    ) -> Text:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Text:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Text:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Text:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Text:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Text:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Text:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Text:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Text:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Text:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | ExprRef | dict[str, Any],
    ) -> Text:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Text:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Text:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Tooltip(Channel):
    """Generated wrapper for the ``tooltip`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``tooltip`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (str | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="tooltip", **defined)
        super().__init__(wrapped.definition, encoding_name="tooltip")

    def band(
        self,
        value: float,
    ) -> Tooltip:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Tooltip:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Tooltip:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Tooltip:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Tooltip:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Tooltip:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> Tooltip:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Tooltip:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Tooltip:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Tooltip:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: str | ExprRef | dict[str, Any],
    ) -> Tooltip:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Tooltip:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Tooltip:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class UniqueId(Channel):
    """Generated wrapper for the ``uniqueId`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        description: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``uniqueId`` encoding channel.

        Args:
            description (str): A description of the encoded field. Can be used for documentation and to explain the meaning of the channel mapping.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
        """
        properties = {
            "description": description,
            "field": field,
            "title": title,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="uniqueId", **defined)
        super().__init__(wrapped.definition, encoding_name="uniqueId")

    def description(
        self,
        value: str,
    ) -> UniqueId:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def field(
        self,
        value: str,
    ) -> UniqueId:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def title(
        self,
        value: str | None,
    ) -> UniqueId:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> UniqueId:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)


class X(Channel):
    """Generated wrapper for the ``x`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        buildIndex: bool | UndefinedType = _MISSING,
        chrom: FieldName_T | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        offset: float | UndefinedType = _MISSING,
        pos: FieldName_T | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``x`` encoding channel.

        Args:
            axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            buildIndex (bool): Builds and index for efficient rendering of subsets of the data. This setting is useful when rendering large amounts of data and often only a small subset of the data is visible. An example of such a situation is a scatter plot spanning the whole genome. This setting implicitly sorts the data by the field assigned on the ``x`` channel.
            chrom (FieldName_T): The field having the chromosome or contig.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
            pos (FieldName_T): The field having an intra-chromosomal position.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "buildIndex": buildIndex,
            "chrom": chrom,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "offset": offset,
            "pos": pos,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "axis": axis,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="x", **defined)
        super().__init__(wrapped.definition, encoding_name="x")

    def band(
        self,
        value: float,
    ) -> X:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def buildIndex(
        self,
        value: bool,
    ) -> X:
        """Return a channel with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def chrom(
        self,
        value: FieldName_T,
    ) -> X:
        """Return a channel with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> X:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> X:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> X:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> X:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> X:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def offset(
        self,
        value: float,
    ) -> X:
        """Return a channel with ``offset`` updated."""
        return self._with_property("offset", value)

    def pos(
        self,
        value: FieldName_T,
    ) -> X:
        """Return a channel with ``pos`` updated."""
        return self._with_property("pos", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> X:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> X:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> X:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> X:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> X:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
    ) -> X:
        """Return a channel with a ``GenomeAxis`` axis.

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
        return self._with_nested("axis", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> X:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class X2(Channel):
    """Generated wrapper for the ``x2`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        chrom: FieldName_T | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        offset: float | UndefinedType = _MISSING,
        pos: FieldName_T | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``x2`` encoding channel.

        Args:
            axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            chrom (FieldName_T): The field having the chromosome or contig.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
            pos (FieldName_T): The field having an intra-chromosomal position.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "chrom": chrom,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "offset": offset,
            "pos": pos,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "axis": axis,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="x2", **defined)
        super().__init__(wrapped.definition, encoding_name="x2")

    def band(
        self,
        value: float,
    ) -> X2:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def chrom(
        self,
        value: FieldName_T,
    ) -> X2:
        """Return a channel with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> X2:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> X2:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> X2:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> X2:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> X2:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def offset(
        self,
        value: float,
    ) -> X2:
        """Return a channel with ``offset`` updated."""
        return self._with_property("offset", value)

    def pos(
        self,
        value: FieldName_T,
    ) -> X2:
        """Return a channel with ``pos`` updated."""
        return self._with_property("pos", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> X2:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> X2:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> X2:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> X2:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> X2:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
    ) -> X2:
        """Return a channel with a ``GenomeAxis`` axis.

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
        return self._with_nested("axis", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> X2:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class XOffset(Channel):
    """Generated wrapper for the ``xOffset`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``xOffset`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded expression. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="xOffset", **defined)
        super().__init__(wrapped.definition, encoding_name="xOffset")

    def band(
        self,
        value: float,
    ) -> XOffset:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> XOffset:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> XOffset:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> XOffset:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> XOffset:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> XOffset:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> XOffset:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> XOffset:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> XOffset:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> XOffset:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> XOffset:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> XOffset:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> XOffset:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> XOffset:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> XOffset:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Y(Channel):
    """Generated wrapper for the ``y`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        chrom: FieldName_T | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        offset: float | UndefinedType = _MISSING,
        pos: FieldName_T | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``y`` encoding channel.

        Args:
            axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            chrom (FieldName_T): The field having the chromosome or contig.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
            pos (FieldName_T): The field having an intra-chromosomal position.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "chrom": chrom,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "offset": offset,
            "pos": pos,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "axis": axis,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="y", **defined)
        super().__init__(wrapped.definition, encoding_name="y")

    def band(
        self,
        value: float,
    ) -> Y:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def chrom(
        self,
        value: FieldName_T,
    ) -> Y:
        """Return a channel with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Y:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Y:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Y:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Y:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Y:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def offset(
        self,
        value: float,
    ) -> Y:
        """Return a channel with ``offset`` updated."""
        return self._with_property("offset", value)

    def pos(
        self,
        value: FieldName_T,
    ) -> Y:
        """Return a channel with ``pos`` updated."""
        return self._with_property("pos", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Y:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Y:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Y:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Y:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Y:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
    ) -> Y:
        """Return a channel with a ``GenomeAxis`` axis.

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
        return self._with_nested("axis", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Y:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class Y2(Channel):
    """Generated wrapper for the ``y2`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        chrom: FieldName_T | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        offset: float | UndefinedType = _MISSING,
        pos: FieldName_T | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        axis: GenomeAxis | GenomeAxisKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``y2`` encoding channel.

        Args:
            axis (GenomeAxis | GenomeAxisKwds | None): An object defining properties of axis's gridlines, ticks and labels. If ``null``, the axis for the encoding channel will be removed. __Default value:__ If undefined, default axis properties are applied. __See also:__ ``axis`` documentation.
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            chrom (FieldName_T): The field having the chromosome or contig.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded value. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            offset (float): An offset or offsets that allow for adjusting the numbering base. The offset is subtracted from the positions. GenomeSpy uses internally zero-based indexing with half-open intervals. UCSC-based formats (BED, etc.) generally use this scheme. However, for example, VCF files use one-based indexing and must be adjusted by setting the offset to ``1``. **Default:** ``0``
            pos (FieldName_T): The field having an intra-chromosomal position.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "chrom": chrom,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "offset": offset,
            "pos": pos,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "axis": axis,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="y2", **defined)
        super().__init__(wrapped.definition, encoding_name="y2")

    def band(
        self,
        value: float,
    ) -> Y2:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def chrom(
        self,
        value: FieldName_T,
    ) -> Y2:
        """Return a channel with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> Y2:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> Y2:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> Y2:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> Y2:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> Y2:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def offset(
        self,
        value: float,
    ) -> Y2:
        """Return a channel with ``offset`` updated."""
        return self._with_property("offset", value)

    def pos(
        self,
        value: FieldName_T,
    ) -> Y2:
        """Return a channel with ``pos`` updated."""
        return self._with_property("pos", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> Y2:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> Y2:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> Y2:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> Y2:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> Y2:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = Undefined,
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
    ) -> Y2:
        """Return a channel with a ``GenomeAxis`` axis.

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
        return self._with_nested("axis", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> Y2:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


class YOffset(Channel):
    """Generated wrapper for the ``yOffset`` encoding channel."""

    def __init__(
        self,
        value: Channel | SchemaBase | str | dict[str, Any],
        /,
        *,
        band: float | UndefinedType = _MISSING,
        condition: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]
        | UndefinedType = _MISSING,
        datum: Scalar_T | ExprRef | dict[str, Any] | UndefinedType = _MISSING,
        description: str | UndefinedType = _MISSING,
        domainInert: bool | UndefinedType = _MISSING,
        expr: str | UndefinedType = _MISSING,
        field: str | UndefinedType = _MISSING,
        format: str | UndefinedType = _MISSING,
        resolutionChannel: ChannelWithScale_T | UndefinedType = _MISSING,
        title: str | None | UndefinedType = _MISSING,
        type: Type_T | UndefinedType = _MISSING,
        legend: Legend | LegendKwds | None | UndefinedType = _MISSING,
        scale: Scale | ScaleKwds | None | UndefinedType = _MISSING,
    ) -> None:
        """Create a ``yOffset`` encoding channel.

        Args:
            band (float): Relative position on band scale. For example, the marks will be positioned at the beginning of the band if set to ``0``, and at the middle of the band if set to ``0.5``.
            condition (ConditionalParameterMarkPropFieldDefType | dict[str, Any] | ConditionalParameterScaleDatumDef | ConditionalParameterMarkPropExprDefType | ConditionalParameterValueDefNumberExprRef | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]]): A field definition or one or more value definition(s) with a parameter predicate.
            datum (Scalar_T | ExprRef | dict[str, Any]): A constant value in data domain.
            description (str): A description of the encoded expression. Can be used for documentation and to explain the meaning of the channel mapping.
            domainInert (bool): Whether the field or evaluated expr should be excluded from the scale's domain. Prefer the view-level ``domainInert`` when an entire subtree should be excluded. **Default value:** ``false``
            expr (str): An expression. Properties of the data can be accessed through the ``datum`` object.
            field (str): __Required.__ A string defining the name of the field from which to pull a data value. __See also:__ ``field`` documentation. __Notes:__ 1) Dots (``.``) and brackets (``[`` and ``]``) can be used to access nested objects (e.g., ``"field": "foo.bar"`` and ``"field": "foo['bar']"``). If field names contain dots or brackets but are not nested, you can use ``\\`` to escape dots and brackets (e.g., ``"a\\.b"`` and ``"a\\[0\\]"``). See more details about escaping in the Vega-Lite field documentation.
            format (str): When used with the default ``"number"`` format type, the text formatting pattern for labels of guides (axes, legends, headers) and text marks. - If the format type is ``"number"`` (e.g., for quantitative fields), this is D3's number format pattern. See the Vega-Lite format documentation for more examples.
            legend (Legend | LegendKwds | None): Legend properties for the encoding channel. If ``null``, the legend for the channel is removed. If an object is provided, a legend is created even when legends are disabled by default in the config. __Default value:__ If undefined, configured legend defaults are applied.
            resolutionChannel (ChannelWithScale_T): An alternative channel for scale resolution. This is mainly for internal use and allows using ``color`` channel to resolve ``fill`` and ``stroke`` channels under certain circumstances.
            scale (Scale | ScaleKwds | None): An object defining properties of the channel's scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels. If ``null``, the scale will be disabled and the data value will be directly encoded. __Default value:__ If undefined, default scale properties are applied. __See also:__ ``scale`` documentation.
            title (str | None): A title for the field. If ``null``, the title will be removed.
            type (Type_T): Schema-defined ``type`` property.
            value (float | ExprRef | dict[str, Any]): A constant value in visual domain (e.g., ``"red"`` / ``"#0099ff"``, values between ``0`` to ``1`` for opacity).
        """
        properties = {
            "band": band,
            "condition": condition,
            "datum": datum,
            "description": description,
            "domainInert": domainInert,
            "expr": expr,
            "field": field,
            "format": format,
            "resolutionChannel": resolutionChannel,
            "title": title,
            "type": type,
            "legend": legend,
            "scale": scale,
        }
        defined = {
            key: item for key, item in properties.items() if item is not _MISSING
        }
        wrapped = channel(value, encoding_name="yOffset", **defined)
        super().__init__(wrapped.definition, encoding_name="yOffset")

    def band(
        self,
        value: float,
    ) -> YOffset:
        """Return a channel with ``band`` updated."""
        return self._with_property("band", value)

    def condition(
        self,
        value: ConditionalParameterMarkPropFieldDefType
        | dict[str, Any]
        | ConditionalParameterScaleDatumDef
        | ConditionalParameterMarkPropExprDefType
        | ConditionalParameterValueDefNumberExprRef
        | Sequence[ConditionalParameterValueDefNumberExprRef | dict[str, Any]],
    ) -> YOffset:
        """Return a channel with ``condition`` updated."""
        return self._with_property("condition", value)

    def datum(
        self,
        value: Scalar_T | ExprRef | dict[str, Any],
    ) -> YOffset:
        """Return a channel with ``datum`` updated."""
        return self._with_property("datum", value)

    def description(
        self,
        value: str,
    ) -> YOffset:
        """Return a channel with ``description`` updated."""
        return self._with_property("description", value)

    def domainInert(
        self,
        value: bool,
    ) -> YOffset:
        """Return a channel with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def expr(
        self,
        value: str,
    ) -> YOffset:
        """Return a channel with ``expr`` updated."""
        return self._with_property("expr", value)

    def field(
        self,
        value: str,
    ) -> YOffset:
        """Return a channel with ``field`` updated."""
        return self._with_property("field", value)

    def format(
        self,
        value: str,
    ) -> YOffset:
        """Return a channel with ``format`` updated."""
        return self._with_property("format", value)

    def resolutionChannel(
        self,
        value: ChannelWithScale_T,
    ) -> YOffset:
        """Return a channel with ``resolutionChannel`` updated."""
        return self._with_property("resolutionChannel", value)

    def title(
        self,
        value: str | None,
    ) -> YOffset:
        """Return a channel with ``title`` updated."""
        return self._with_property("title", value)

    def type(
        self,
        value: Type_T,
    ) -> YOffset:
        """Return a channel with ``type`` updated."""
        return self._with_property("type", value)

    def value(
        self,
        value: float | ExprRef | dict[str, Any],
    ) -> YOffset:
        """Return a channel with ``value`` updated."""
        return self._with_property("value", value)

    def sort(
        self,
        value: CompareParams
        | CompareParamsKwds
        | str
        | list[str]
        | None
        | object = _MISSING,
        /,
        *,
        field: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        order: Sequence[SortOrder_T] | SortOrder_T | UndefinedType = Undefined,
    ) -> YOffset:
        """Return a channel with a ``sort`` configuration."""
        properties = {
            "field": field,
            "order": order,
        }
        defined = {
            key: item for key, item in properties.items() if item is not Undefined
        }
        return self._with_sort(value, defined)

    def legend(
        self,
        value: Legend | LegendKwds | None | object = Undefined,
        /,
        *,
        backgroundFill: str | UndefinedType = Undefined,
        backgroundFillOpacity: float | UndefinedType = Undefined,
        backgroundStroke: str | UndefinedType = Undefined,
        backgroundStrokeOpacity: float | UndefinedType = Undefined,
        backgroundStrokeWidth: float | UndefinedType = Undefined,
        columns: float | UndefinedType = Undefined,
        direction: LegendDirection_T | UndefinedType = Undefined,
        gradientLength: float | UndefinedType = Undefined,
        gradientOpacity: float | UndefinedType = Undefined,
        gradientStrokeColor: str | UndefinedType = Undefined,
        gradientStrokeWidth: float | UndefinedType = Undefined,
        gradientThickness: float | UndefinedType = Undefined,
        labelLimit: float | UndefinedType = Undefined,
        offset: float | UndefinedType = Undefined,
        orient: LegendOrient_T
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        padding: float | UndefinedType = Undefined,
        style: str | Sequence[str] | None | UndefinedType = Undefined,
        symbolSize: float | UndefinedType = Undefined,
        symbolType: str | UndefinedType = Undefined,
        tickCount: float | UndefinedType = Undefined,
        title: str | None | UndefinedType = Undefined,
        titleOrient: LegendTitleOrient_T | UndefinedType = Undefined,
        values: Sequence[str | float | bool] | UndefinedType = Undefined,
    ) -> YOffset:
        """Return a channel with a ``Legend`` legend.

        Args:
            backgroundFill (str): Fill color of the legend background.
            backgroundFillOpacity (float): Opacity of the legend background fill.
            backgroundStroke (str): Stroke color of the legend background.
            backgroundStrokeOpacity (float): Opacity of the legend background stroke.
            backgroundStrokeWidth (float): Stroke width of the legend background border.
            columns (float): The number of columns in which to arrange symbol legend entries.
            direction (LegendDirection_T): The direction in which legend entries are laid out. This is independent of ``orient``, which selects the legend region. __Default value:__ ``"vertical"``
            gradientLength (float): Fixed length of the gradient ramp in pixels. This is the width of a horizontal ramp and the height of a vertical ramp. When omitted, the ramp fills available space when its direction is parallel to its legend region. Otherwise its natural length is 200 pixels.
            gradientOpacity (float): Opacity of the gradient ramp. __Default value:__ ``1``
            gradientStrokeColor (str): Stroke color of the gradient ramp border.
            gradientStrokeWidth (float): Stroke width of the gradient ramp border in pixels. __Default value:__ ``0``
            gradientThickness (float): Thickness of the gradient ramp in pixels. __Default value:__ ``12``
            labelLimit (float): Maximum label text width in pixels.
            offset (float): External gap in pixels between the legend and the plot edge.
            orient (LegendOrient_T | ExprRef | dict[str, Any]): The plot side or inside corner where the legend is placed. Side legends are placed outside the plot area. Corner legends are placed inside the plot area.
            padding (float): Internal padding in pixels around the legend content and background.
            style (str | Sequence[str] | None): Named style reference or references resolved from ``config.style``. If an array is provided, later styles override earlier ones. Set to ``null`` to reset inherited legend styles.
            symbolSize (float): Symbol size in pixels squared.
            symbolType (str): Symbol shape.
            tickCount (float): Desired number of ticks for a quantitative gradient legend. Explicit ``values`` take precedence over this property. __Default value:__ ``5``
            title (str | None): Title text for the legend. If ``null``, the title is removed.
            titleOrient (LegendTitleOrient_T): The side of the legend on which to place the title.
            values (Sequence[str | float | bool]): Explicit values to show in the legend. For discrete symbol legends, the values define an ordered subset of entries. For quantitative symbol and gradient legends, the values define the shown representative values or ticks.
        """
        defined = {
            "backgroundFill": backgroundFill,
            "backgroundFillOpacity": backgroundFillOpacity,
            "backgroundStroke": backgroundStroke,
            "backgroundStrokeOpacity": backgroundStrokeOpacity,
            "backgroundStrokeWidth": backgroundStrokeWidth,
            "columns": columns,
            "direction": direction,
            "gradientLength": gradientLength,
            "gradientOpacity": gradientOpacity,
            "gradientStrokeColor": gradientStrokeColor,
            "gradientStrokeWidth": gradientStrokeWidth,
            "gradientThickness": gradientThickness,
            "labelLimit": labelLimit,
            "offset": offset,
            "orient": orient,
            "padding": padding,
            "style": style,
            "symbolSize": symbolSize,
            "symbolType": symbolType,
            "tickCount": tickCount,
            "title": title,
            "titleOrient": titleOrient,
            "values": values,
        }
        defined = {key: item for key, item in defined.items() if item is not Undefined}
        return self._with_nested("legend", value, **defined)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = Undefined,
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
    ) -> YOffset:
        """Return a channel with a ``Scale`` scale.

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
            interpolate (ScaleInterpolate_T | ScaleInterpolateParams | ScaleInterpolateParamsKwds): The interpolation method for range values. By default, a general interpolator for numbers, dates, strings and colors (in HCL space) is used. For color ranges, this property allows interpolation in alternative color spaces. Legal values include ``rgb``, ``hsl``, ``hsl-long``, ``lab``, ``hcl``, ``hcl-long``, ``cubehelix`` and ``cubehelix-long`` ('-long' variants use longer paths in polar coordinate spaces). If object-valued, this property accepts an object with a string-valued type property and an optional numeric gamma property applicable to rgb and cubehelix interpolators. For more, see the d3-interpolate documentation. __Default value:__ ``hcl``
            name (str): The name of the scale. Names are optional but allow the scales to be referenced and found with the API.
            nice (bool | float | dict[str, Any]): Extending the domain so that it starts and ends on nice round values. This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data and may be irregular. For example, for a domain of [0.201479…, 0.996679…], a nice domain might be [0.2, 1.0]. For quantitative scales such as linear, ``nice`` can be either a boolean flag or a number. If ``nice`` is a number, it will represent a desired tick count. This allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. __Default value:__ ``true`` for unbinned quantitative fields; ``false`` otherwise.
            numberingOffset (float): The offset added to data values when formatting tick labels on index and locus scales. This property does not transform data values. __Default value:__ ``0``
            padding (float): For Vega-Lite continuous scales, expands the scale domain to accommodate the specified number of pixels on each of the scale range. The scale range must represent pixels for this parameter to function as intended. Padding adjustment is performed prior to all other adjustments, including the effects of the ``zero``, ``nice``, ``domainMin``, and ``domainMax`` properties. For Vega-Lite band scales, shortcut for setting ``paddingInner`` and ``paddingOuter`` to the same value. For Vega-Lite point scales, alias for ``paddingOuter``. __Default value:__ For continuous scales, derived from the Vega-Lite scale config's ``continuousPadding``. For band and point scales, see ``paddingInner`` and ``paddingOuter``. By default, Vega-Lite sets padding such that width/height = number of unique values * step.
            paddingInner (float): The inner padding (spacing) within each band step of band scales, as a fraction of the step size. This value must lie in the range [0,1]. For point scale, this property is invalid as point scales do not have internal band widths (only step sizes between bands). __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingInner``.
            paddingOuter (float): The outer padding (spacing) at the ends of the range of band and point scales, as a fraction of the step size. This value must lie in the range [0,1]. __Default value:__ derived from the Vega-Lite scale config's ``bandPaddingOuter`` for band scales and ``pointPadding`` for point scales. By default, Vega-Lite sets outer padding such that width/height = number of unique values * step.
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
        return self._with_nested("scale", value, **defined)


__all__ = [
    "Angle",
    "Color",
    "Direction",
    "Dx",
    "Dy",
    "FacetIndex",
    "Fill",
    "FillOpacity",
    "Key",
    "Opacity",
    "Sample",
    "Search",
    "SemanticScore",
    "Shape",
    "Size",
    "Stroke",
    "StrokeOpacity",
    "StrokeWidth",
    "Text",
    "Tooltip",
    "UniqueId",
    "X",
    "X2",
    "XOffset",
    "Y",
    "Y2",
    "YOffset",
]
