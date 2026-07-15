"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from typing import Any

from genome_spy.channels import Channel, _MISSING, channel
from genome_spy.schema.core import GenomeAxis, Legend, Scale
from genome_spy.schema._kwds import GenomeAxisKwds, LegendKwds, ScaleKwds


class Angle(Channel):
    """Generated wrapper for the ``angle`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="angle", **kwargs)
        super().__init__(wrapped.definition, encoding_name="angle")

    def title(
        self,
        value: str | None,
    ) -> Angle:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="color", **kwargs)
        super().__init__(wrapped.definition, encoding_name="color")

    def title(
        self,
        value: str | None,
    ) -> Color:
        """Return a channel with a title."""
        return super().title(value)

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


class Dx(Channel):
    """Generated wrapper for the ``dx`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="dx", **kwargs)
        super().__init__(wrapped.definition, encoding_name="dx")

    def title(
        self,
        value: str | None,
    ) -> Dx:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="dy", **kwargs)
        super().__init__(wrapped.definition, encoding_name="dy")

    def title(
        self,
        value: str | None,
    ) -> Dy:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="facetIndex", **kwargs)
        super().__init__(wrapped.definition, encoding_name="facetIndex")

    def title(
        self,
        value: str | None,
    ) -> FacetIndex:
        """Return a channel with a title."""
        return super().title(value)


class Fill(Channel):
    """Generated wrapper for the ``fill`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="fill", **kwargs)
        super().__init__(wrapped.definition, encoding_name="fill")

    def title(
        self,
        value: str | None,
    ) -> Fill:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="fillOpacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="fillOpacity")

    def title(
        self,
        value: str | None,
    ) -> FillOpacity:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="key", **kwargs)
        super().__init__(wrapped.definition, encoding_name="key")

    def title(
        self,
        value: str | None,
    ) -> Key:
        """Return a channel with a title."""
        return super().title(value)


class Opacity(Channel):
    """Generated wrapper for the ``opacity`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="opacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="opacity")

    def title(
        self,
        value: str | None,
    ) -> Opacity:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="sample", **kwargs)
        super().__init__(wrapped.definition, encoding_name="sample")

    def title(
        self,
        value: str | None,
    ) -> Sample:
        """Return a channel with a title."""
        return super().title(value)


class Search(Channel):
    """Generated wrapper for the ``search`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="search", **kwargs)
        super().__init__(wrapped.definition, encoding_name="search")

    def title(
        self,
        value: str | None,
    ) -> Search:
        """Return a channel with a title."""
        return super().title(value)


class SemanticScore(Channel):
    """Generated wrapper for the ``semanticScore`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="semanticScore", **kwargs)
        super().__init__(wrapped.definition, encoding_name="semanticScore")

    def title(
        self,
        value: str | None,
    ) -> SemanticScore:
        """Return a channel with a title."""
        return super().title(value)


class Shape(Channel):
    """Generated wrapper for the ``shape`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="shape", **kwargs)
        super().__init__(wrapped.definition, encoding_name="shape")

    def title(
        self,
        value: str | None,
    ) -> Shape:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="size", **kwargs)
        super().__init__(wrapped.definition, encoding_name="size")

    def title(
        self,
        value: str | None,
    ) -> Size:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="stroke", **kwargs)
        super().__init__(wrapped.definition, encoding_name="stroke")

    def title(
        self,
        value: str | None,
    ) -> Stroke:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="strokeOpacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="strokeOpacity")

    def title(
        self,
        value: str | None,
    ) -> StrokeOpacity:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="strokeWidth", **kwargs)
        super().__init__(wrapped.definition, encoding_name="strokeWidth")

    def title(
        self,
        value: str | None,
    ) -> StrokeWidth:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="text", **kwargs)
        super().__init__(wrapped.definition, encoding_name="text")

    def title(
        self,
        value: str | None,
    ) -> Text:
        """Return a channel with a title."""
        return super().title(value)

    def scale(
        self,
        value: Scale | ScaleKwds | None | object = _MISSING,
        /,
        **kwargs: Any,
    ) -> Text:
        """Return a channel with a ``Scale`` scale."""
        return self._with_nested("scale", value, **kwargs)


class UniqueId(Channel):
    """Generated wrapper for the ``uniqueId`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="uniqueId", **kwargs)
        super().__init__(wrapped.definition, encoding_name="uniqueId")

    def title(
        self,
        value: str | None,
    ) -> UniqueId:
        """Return a channel with a title."""
        return super().title(value)


class X(Channel):
    """Generated wrapper for the ``x`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="x", **kwargs)
        super().__init__(wrapped.definition, encoding_name="x")

    def title(
        self,
        value: str | None,
    ) -> X:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="x2", **kwargs)
        super().__init__(wrapped.definition, encoding_name="x2")

    def title(
        self,
        value: str | None,
    ) -> X2:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="y", **kwargs)
        super().__init__(wrapped.definition, encoding_name="y")

    def title(
        self,
        value: str | None,
    ) -> Y:
        """Return a channel with a title."""
        return super().title(value)

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

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="y2", **kwargs)
        super().__init__(wrapped.definition, encoding_name="y2")

    def title(
        self,
        value: str | None,
    ) -> Y2:
        """Return a channel with a title."""
        return super().title(value)

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
    "UniqueId",
    "X",
    "X2",
    "Y",
    "Y2",
]
