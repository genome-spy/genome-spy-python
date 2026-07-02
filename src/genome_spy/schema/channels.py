"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from typing import Any

from genome_spy.channels import Channel, channel


class Angle(Channel):
    """Generated wrapper for the ``angle`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="angle", **kwargs)
        super().__init__(wrapped.definition, encoding_name="angle")


class Color(Channel):
    """Generated wrapper for the ``color`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="color", **kwargs)
        super().__init__(wrapped.definition, encoding_name="color")


class Dx(Channel):
    """Generated wrapper for the ``dx`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="dx", **kwargs)
        super().__init__(wrapped.definition, encoding_name="dx")


class Dy(Channel):
    """Generated wrapper for the ``dy`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="dy", **kwargs)
        super().__init__(wrapped.definition, encoding_name="dy")


class FacetIndex(Channel):
    """Generated wrapper for the ``facetIndex`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="facetIndex", **kwargs)
        super().__init__(wrapped.definition, encoding_name="facetIndex")


class Fill(Channel):
    """Generated wrapper for the ``fill`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="fill", **kwargs)
        super().__init__(wrapped.definition, encoding_name="fill")


class FillOpacity(Channel):
    """Generated wrapper for the ``fillOpacity`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="fillOpacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="fillOpacity")


class Key(Channel):
    """Generated wrapper for the ``key`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="key", **kwargs)
        super().__init__(wrapped.definition, encoding_name="key")


class Opacity(Channel):
    """Generated wrapper for the ``opacity`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="opacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="opacity")


class Sample(Channel):
    """Generated wrapper for the ``sample`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="sample", **kwargs)
        super().__init__(wrapped.definition, encoding_name="sample")


class Search(Channel):
    """Generated wrapper for the ``search`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="search", **kwargs)
        super().__init__(wrapped.definition, encoding_name="search")


class SemanticScore(Channel):
    """Generated wrapper for the ``semanticScore`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="semanticScore", **kwargs)
        super().__init__(wrapped.definition, encoding_name="semanticScore")


class Shape(Channel):
    """Generated wrapper for the ``shape`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="shape", **kwargs)
        super().__init__(wrapped.definition, encoding_name="shape")


class Size(Channel):
    """Generated wrapper for the ``size`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="size", **kwargs)
        super().__init__(wrapped.definition, encoding_name="size")


class Stroke(Channel):
    """Generated wrapper for the ``stroke`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="stroke", **kwargs)
        super().__init__(wrapped.definition, encoding_name="stroke")


class StrokeOpacity(Channel):
    """Generated wrapper for the ``strokeOpacity`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="strokeOpacity", **kwargs)
        super().__init__(wrapped.definition, encoding_name="strokeOpacity")


class StrokeWidth(Channel):
    """Generated wrapper for the ``strokeWidth`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="strokeWidth", **kwargs)
        super().__init__(wrapped.definition, encoding_name="strokeWidth")


class Text(Channel):
    """Generated wrapper for the ``text`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="text", **kwargs)
        super().__init__(wrapped.definition, encoding_name="text")


class UniqueId(Channel):
    """Generated wrapper for the ``uniqueId`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="uniqueId", **kwargs)
        super().__init__(wrapped.definition, encoding_name="uniqueId")


class X(Channel):
    """Generated wrapper for the ``x`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="x", **kwargs)
        super().__init__(wrapped.definition, encoding_name="x")


class X2(Channel):
    """Generated wrapper for the ``x2`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="x2", **kwargs)
        super().__init__(wrapped.definition, encoding_name="x2")


class Y(Channel):
    """Generated wrapper for the ``y`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="y", **kwargs)
        super().__init__(wrapped.definition, encoding_name="y")


class Y2(Channel):
    """Generated wrapper for the ``y2`` encoding channel."""

    def __init__(self, value: Channel | str | dict[str, Any], /, **kwargs: Any) -> None:
        wrapped = channel(value, encoding_name="y2", **kwargs)
        super().__init__(wrapped.definition, encoding_name="y2")


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
