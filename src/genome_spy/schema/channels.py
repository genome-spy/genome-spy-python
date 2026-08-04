"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any

from genome_spy.channels import Channel, _MISSING, channel
from genome_spy.schemapi import SchemaBase
from genome_spy.schema._typing import (
    ArrowDirection_T,
    ChannelWithScale_T,
    FieldName_T,
    Scalar_T,
    Type_T,
)
from genome_spy.schema.core import (
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
from genome_spy.schema._kwds import GenomeAxisKwds, LegendKwds, ScaleKwds


class Angle(Channel):
    """Generated wrapper for the ``angle`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="angle", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Angle:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Angle:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Color(Channel):
    """Generated wrapper for the ``color`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="color", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Color:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Color:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Direction(Channel):
    """Generated wrapper for the ``direction`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="direction", **kwargs)
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

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Direction:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Dx(Channel):
    """Generated wrapper for the ``dx`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="dx", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Dx:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Dx:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Dy(Channel):
    """Generated wrapper for the ``dy`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="dy", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Dy:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Dy:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class FacetIndex(Channel):
    """Generated wrapper for the ``facetIndex`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="facetIndex", **kwargs)
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


class Fill(Channel):
    """Generated wrapper for the ``fill`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="fill", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Fill:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Fill:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class FillOpacity(Channel):
    """Generated wrapper for the ``fillOpacity`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="fillOpacity", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> FillOpacity:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> FillOpacity:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Key(Channel):
    """Generated wrapper for the ``key`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="key", **kwargs)
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


class Opacity(Channel):
    """Generated wrapper for the ``opacity`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="opacity", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Opacity:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Opacity:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Sample(Channel):
    """Generated wrapper for the ``sample`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="sample", **kwargs)
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


class Search(Channel):
    """Generated wrapper for the ``search`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="search", **kwargs)
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


class SemanticScore(Channel):
    """Generated wrapper for the ``semanticScore`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="semanticScore", **kwargs)
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


class Shape(Channel):
    """Generated wrapper for the ``shape`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="shape", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Shape:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Shape:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Size(Channel):
    """Generated wrapper for the ``size`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="size", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Size:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Size:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Stroke(Channel):
    """Generated wrapper for the ``stroke`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="stroke", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Stroke:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Stroke:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class StrokeOpacity(Channel):
    """Generated wrapper for the ``strokeOpacity`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="strokeOpacity", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> StrokeOpacity:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> StrokeOpacity:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class StrokeWidth(Channel):
    """Generated wrapper for the ``strokeWidth`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="strokeWidth", **kwargs)
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

    def legend(
        self,
        value: Legend | LegendKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> StrokeWidth:
        """Return a channel with a ``Legend`` legend."""
        return self._with_nested("legend", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> StrokeWidth:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Text(Channel):
    """Generated wrapper for the ``text`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="text", **kwargs)
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

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Text:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Tooltip(Channel):
    """Generated wrapper for the ``tooltip`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="tooltip", **kwargs)
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

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Tooltip:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class UniqueId(Channel):
    """Generated wrapper for the ``uniqueId`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="uniqueId", **kwargs)
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


class X(Channel):
    """Generated wrapper for the ``x`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="x", **kwargs)
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

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> X:
        """Return a channel with a ``GenomeAxis`` axis."""
        return self._with_nested("axis", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> X:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class X2(Channel):
    """Generated wrapper for the ``x2`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="x2", **kwargs)
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

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> X2:
        """Return a channel with a ``GenomeAxis`` axis."""
        return self._with_nested("axis", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> X2:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Y(Channel):
    """Generated wrapper for the ``y`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="y", **kwargs)
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

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Y:
        """Return a channel with a ``GenomeAxis`` axis."""
        return self._with_nested("axis", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Y:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class Y2(Channel):
    """Generated wrapper for the ``y2`` encoding channel."""

    def __init__(
        self, value: Channel | SchemaBase | str | dict[str, Any], /, **kwargs: Any
    ) -> None:
        wrapped = channel(value, encoding_name="y2", **kwargs)
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

    def axis(
        self,
        value: GenomeAxis | GenomeAxisKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Y2:
        """Return a channel with a ``GenomeAxis`` axis."""
        return self._with_nested("axis", value, **kwargs)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Y2:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


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
    "Y",
    "Y2",
]
