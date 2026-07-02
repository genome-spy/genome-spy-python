"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
import json
from importlib.resources import files
from typing import Any, cast

from genome_spy.schemapi import SchemaBase, Undefined


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


class AggregateOp(GenomeSpySchema):
    """Generated wrapper for ``AggregateOp``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AggregateOp", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class AggregateParams(GenomeSpySchema):
    """Generated wrapper for ``AggregateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AggregateParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        fields: Any = Undefined,
        groupby: Any = Undefined,
        ops: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, fields=fields, groupby=groupby, ops=ops, type=type
        )
        if kwds:
            self._kwds.update(kwds)


class Align(GenomeSpySchema):
    """Generated wrapper for ``Align``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Align", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class Axis(GenomeSpySchema):
    """Generated wrapper for ``Axis``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Axis", {})

    def __init__(
        self,
        domain: Any = Undefined,
        domainCap: Any = Undefined,
        domainColor: Any = Undefined,
        domainDash: Any = Undefined,
        domainDashOffset: Any = Undefined,
        domainWidth: Any = Undefined,
        format: Any = Undefined,
        grid: Any = Undefined,
        gridCap: Any = Undefined,
        gridColor: Any = Undefined,
        gridDash: Any = Undefined,
        gridDashOffset: Any = Undefined,
        gridOpacity: Any = Undefined,
        gridWidth: Any = Undefined,
        labelAlign: Any = Undefined,
        labelAngle: Any = Undefined,
        labelBaseline: Any = Undefined,
        labelColor: Any = Undefined,
        labelFont: Any = Undefined,
        labelFontSize: Any = Undefined,
        labelFontStyle: Any = Undefined,
        labelFontWeight: Any = Undefined,
        labelLimit: Any = Undefined,
        labelPadding: Any = Undefined,
        labels: Any = Undefined,
        maxExtent: Any = Undefined,
        minExtent: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        placement: Any = Undefined,
        style: Any = Undefined,
        tickCap: Any = Undefined,
        tickColor: Any = Undefined,
        tickCount: Any = Undefined,
        tickDash: Any = Undefined,
        tickDashOffset: Any = Undefined,
        tickMinStep: Any = Undefined,
        tickSize: Any = Undefined,
        tickWidth: Any = Undefined,
        ticks: Any = Undefined,
        title: Any = Undefined,
        titleColor: Any = Undefined,
        titleFit: Any = Undefined,
        titleFont: Any = Undefined,
        titleFontSize: Any = Undefined,
        titleFontStyle: Any = Undefined,
        titleFontWeight: Any = Undefined,
        titleOpacity: Any = Undefined,
        titlePadding: Any = Undefined,
        values: Any = Undefined,
        zindex: Any = Undefined,
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


class AxisConfig(GenomeSpySchema):
    """Generated wrapper for ``AxisConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisConfig", {})

    def __init__(
        self,
        chromGrid: Any = Undefined,
        chromGridCap: Any = Undefined,
        chromGridColor: Any = Undefined,
        chromGridDash: Any = Undefined,
        chromGridDashOffset: Any = Undefined,
        chromGridFillEven: Any = Undefined,
        chromGridFillOdd: Any = Undefined,
        chromGridOpacity: Any = Undefined,
        chromGridWidth: Any = Undefined,
        chromLabelAlign: Any = Undefined,
        chromLabelColor: Any = Undefined,
        chromLabelFont: Any = Undefined,
        chromLabelFontSize: Any = Undefined,
        chromLabelFontStyle: Any = Undefined,
        chromLabelFontWeight: Any = Undefined,
        chromLabelPadding: Any = Undefined,
        chromLabels: Any = Undefined,
        chromTickColor: Any = Undefined,
        chromTickDash: Any = Undefined,
        chromTickDashOffset: Any = Undefined,
        chromTickSize: Any = Undefined,
        chromTickWidth: Any = Undefined,
        chromTicks: Any = Undefined,
        domain: Any = Undefined,
        domainCap: Any = Undefined,
        domainColor: Any = Undefined,
        domainDash: Any = Undefined,
        domainDashOffset: Any = Undefined,
        domainWidth: Any = Undefined,
        format: Any = Undefined,
        grid: Any = Undefined,
        gridCap: Any = Undefined,
        gridColor: Any = Undefined,
        gridDash: Any = Undefined,
        gridDashOffset: Any = Undefined,
        gridOpacity: Any = Undefined,
        gridWidth: Any = Undefined,
        labelAlign: Any = Undefined,
        labelAngle: Any = Undefined,
        labelBaseline: Any = Undefined,
        labelColor: Any = Undefined,
        labelFont: Any = Undefined,
        labelFontSize: Any = Undefined,
        labelFontStyle: Any = Undefined,
        labelFontWeight: Any = Undefined,
        labelLimit: Any = Undefined,
        labelPadding: Any = Undefined,
        labels: Any = Undefined,
        maxExtent: Any = Undefined,
        minExtent: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        placement: Any = Undefined,
        style: Any = Undefined,
        tickCap: Any = Undefined,
        tickColor: Any = Undefined,
        tickCount: Any = Undefined,
        tickDash: Any = Undefined,
        tickDashOffset: Any = Undefined,
        tickMinStep: Any = Undefined,
        tickSize: Any = Undefined,
        tickWidth: Any = Undefined,
        ticks: Any = Undefined,
        title: Any = Undefined,
        titleColor: Any = Undefined,
        titleFit: Any = Undefined,
        titleFont: Any = Undefined,
        titleFontSize: Any = Undefined,
        titleFontStyle: Any = Undefined,
        titleFontWeight: Any = Undefined,
        titleOpacity: Any = Undefined,
        titlePadding: Any = Undefined,
        values: Any = Undefined,
        zindex: Any = Undefined,
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


class AxisGenomeData(GenomeSpySchema):
    """Generated wrapper for ``AxisGenomeData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisGenomeData", {})

    def __init__(
        self, channel: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(channel=channel, type=type)
        if kwds:
            self._kwds.update(kwds)


class AxisOrient(GenomeSpySchema):
    """Generated wrapper for ``AxisOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class AxisPlacement(GenomeSpySchema):
    """Generated wrapper for ``AxisPlacement``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisPlacement", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class AxisTicksData(GenomeSpySchema):
    """Generated wrapper for ``AxisTicksData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisTicksData", {})

    def __init__(
        self,
        axis: Any = Undefined,
        channel: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(axis=axis, channel=channel, type=type)
        if kwds:
            self._kwds.update(kwds)


class BamData(GenomeSpySchema):
    """Generated wrapper for ``BamData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BamData", {})

    def __init__(
        self,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        indexUrl: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class Baseline(GenomeSpySchema):
    """Generated wrapper for ``Baseline``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Baseline", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class BedDataFormat(GenomeSpySchema):
    """Generated wrapper for ``BedDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BedDataFormat", {})

    def __init__(
        self, parse: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)


class BedpeDataFormat(GenomeSpySchema):
    """Generated wrapper for ``BedpeDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BedpeDataFormat", {})

    def __init__(
        self,
        columns: Any = Undefined,
        parse: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)


class BigBedData(GenomeSpySchema):
    """Generated wrapper for ``BigBedData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BigBedData", {})

    def __init__(
        self,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class BigWigData(GenomeSpySchema):
    """Generated wrapper for ``BigWigData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BigWigData", {})

    def __init__(
        self,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        pixelsPerBin: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
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


class BindCheckbox(GenomeSpySchema):
    """Generated wrapper for ``BindCheckbox``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindCheckbox", {})

    def __init__(
        self,
        debounce: Any = Undefined,
        description: Any = Undefined,
        input: Any = Undefined,
        name: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            debounce=debounce, description=description, input=input, name=name
        )
        if kwds:
            self._kwds.update(kwds)


class BindInput(GenomeSpySchema):
    """Generated wrapper for ``BindInput``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindInput", {})

    def __init__(
        self,
        autocomplete: Any = Undefined,
        debounce: Any = Undefined,
        description: Any = Undefined,
        input: Any = Undefined,
        name: Any = Undefined,
        placeholder: Any = Undefined,
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


class BindRadioSelect(GenomeSpySchema):
    """Generated wrapper for ``BindRadioSelect``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindRadioSelect", {})

    def __init__(
        self,
        debounce: Any = Undefined,
        description: Any = Undefined,
        input: Any = Undefined,
        labels: Any = Undefined,
        name: Any = Undefined,
        options: Any = Undefined,
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


class BindRange(GenomeSpySchema):
    """Generated wrapper for ``BindRange``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BindRange", {})

    def __init__(
        self,
        debounce: Any = Undefined,
        description: Any = Undefined,
        input: Any = Undefined,
        max: Any = Undefined,
        min: Any = Undefined,
        name: Any = Undefined,
        step: Any = Undefined,
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


class Binding(GenomeSpySchema):
    """Generated wrapper for ``Binding``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Binding", {})

    def __init__(
        self,
        autocomplete: Any = Undefined,
        debounce: Any = Undefined,
        description: Any = Undefined,
        input: Any = Undefined,
        labels: Any = Undefined,
        max: Any = Undefined,
        min: Any = Undefined,
        name: Any = Undefined,
        options: Any = Undefined,
        placeholder: Any = Undefined,
        step: Any = Undefined,
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


class BrushConfig(GenomeSpySchema):
    """Generated wrapper for ``BrushConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BrushConfig", {})

    def __init__(
        self,
        clip: Any = Undefined,
        cursor: Any = Undefined,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        measure: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        zindex: Any = Undefined,
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


class BuiltInThemeName(GenomeSpySchema):
    """Generated wrapper for ``BuiltInThemeName``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("BuiltInThemeName", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ChannelWithScale(GenomeSpySchema):
    """Generated wrapper for ``ChannelWithScale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChannelWithScale", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ChromPosDef(GenomeSpySchema):
    """Generated wrapper for ``ChromPosDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChromPosDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        chrom: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        offset: Any = Undefined,
        pos: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ChromosomalLocus(GenomeSpySchema):
    """Generated wrapper for ``ChromosomalLocus``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChromosomalLocus", {})

    def __init__(
        self, chrom: Any = Undefined, pos: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)


class CollectParams(GenomeSpySchema):
    """Generated wrapper for ``CollectParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CollectParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        groupby: Any = Undefined,
        sort: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, groupby=groupby, sort=sort, type=type)
        if kwds:
            self._kwds.update(kwds)


class ColorDef(GenomeSpySchema):
    """Generated wrapper for ``ColorDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ColorDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class ColorSchemeConfig(GenomeSpySchema):
    """Generated wrapper for ``ColorSchemeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ColorSchemeConfig", {})

    def __init__(
        self,
        count: Any = Undefined,
        extent: Any = Undefined,
        name: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(count=count, extent=extent, name=name)
        if kwds:
            self._kwds.update(kwds)


class CompareParams(GenomeSpySchema):
    """Generated wrapper for ``CompareParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CompareParams", {})

    def __init__(
        self, field: Any = Undefined, order: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(field=field, order=order)
        if kwds:
            self._kwds.update(kwds)


class ComplexDomain(GenomeSpySchema):
    """Generated wrapper for ``ComplexDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ComplexDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``ConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ConcatSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        columns: Any = Undefined,
        concat: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        height: Any = Undefined,
        legends: Any = Undefined,
        name: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        separator: Any = Undefined,
        spacing: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class ConditionalMarkPropExprDefType(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropExprDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropExprDef<Type>>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        expr: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalMarkPropExprDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropExprDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropExprDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        expr: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalMarkPropFieldDefType(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropFieldDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropFieldDef<Type>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalMarkPropFieldDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``Conditional<MarkPropFieldDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<MarkPropFieldDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalScaleDatumDef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ScaleDatumDef>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Conditional<ScaleDatumDef>", {})

    def __init__(
        self,
        band: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalValueDefNumberExprRef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ValueDef<(number|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<ValueDef<(number|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class ConditionalValueDefStringNullExprRef(GenomeSpySchema):
    """Generated wrapper for ``Conditional<ValueDef<(string|null|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "Conditional<ValueDef<(string|null|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class ConditionalParameterMarkPropExprDefType(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropExprDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropExprDef<Type>>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        expr: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalParameterMarkPropExprDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropExprDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropExprDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        expr: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalParameterMarkPropFieldDefType(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropFieldDef<Type>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropFieldDef<Type>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalParameterMarkPropFieldDefTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<MarkPropFieldDef<TypeForShape>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<MarkPropFieldDef<TypeForShape>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalParameterScaleDatumDef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ScaleDatumDef>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ScaleDatumDef>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class ConditionalParameterValueDefNumberExprRef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ValueDef<(number|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ValueDef<(number|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class ConditionalParameterValueDefStringNullExprRef(GenomeSpySchema):
    """Generated wrapper for ``ConditionalParameter<ValueDef<(string|null|ExprRef)>>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ConditionalParameter<ValueDef<(string|null|ExprRef)>>", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        param: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, param=param, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class Contig(GenomeSpySchema):
    """Generated wrapper for ``Contig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Contig", {})

    def __init__(
        self, name: Any = Undefined, size: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(name=name, size=size)
        if kwds:
            self._kwds.update(kwds)


class CoreRootSpec(GenomeSpySchema):
    """Generated wrapper for ``CoreRootSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CoreRootSpec", {})

    def __init__(
        self,
        assembly: Any = Undefined,
        axes: Any = Undefined,
        background: Any = Undefined,
        baseUrl: Any = Undefined,
        columns: Any = Undefined,
        concat: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        datasets: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        genome: Any = Undefined,
        genomes: Any = Undefined,
        hconcat: Any = Undefined,
        height: Any = Undefined,
        layer: Any = Undefined,
        legends: Any = Undefined,
        mark: Any = Undefined,
        multiscale: Any = Undefined,
        name: Any = Undefined,
        opacity: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        separator: Any = Undefined,
        spacing: Any = Undefined,
        stops: Any = Undefined,
        templates: Any = Undefined,
        theme: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        vconcat: Any = Undefined,
        view: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class CoverageParams(GenomeSpySchema):
    """Generated wrapper for ``CoverageParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CoverageParams", {})

    def __init__(
        self,
        asChrom: Any = Undefined,
        asEnd: Any = Undefined,
        asStart: Any = Undefined,
        chrom: Any = Undefined,
        description: Any = Undefined,
        end: Any = Undefined,
        start: Any = Undefined,
        type: Any = Undefined,
        weight: Any = Undefined,
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


class CsvDataFormat(GenomeSpySchema):
    """Generated wrapper for ``CsvDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CsvDataFormat", {})

    def __init__(
        self,
        columns: Any = Undefined,
        parse: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)


class Data(GenomeSpySchema):
    """Generated wrapper for ``Data``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Data", {})

    def __init__(
        self,
        description: Any = Undefined,
        dynamicCallbackSource: Any = Undefined,
        format: Any = Undefined,
        lazy: Any = Undefined,
        name: Any = Undefined,
        sequence: Any = Undefined,
        url: Any = Undefined,
        values: Any = Undefined,
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


class DataFormat(GenomeSpySchema):
    """Generated wrapper for ``DataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DataFormat", {})

    def __init__(
        self,
        columns: Any = Undefined,
        delimiter: Any = Undefined,
        parse: Any = Undefined,
        property: Any = Undefined,
        type: Any = Undefined,
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


class DataSource(GenomeSpySchema):
    """Generated wrapper for ``DataSource``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DataSource", {})

    def __init__(
        self,
        description: Any = Undefined,
        dynamicCallbackSource: Any = Undefined,
        format: Any = Undefined,
        lazy: Any = Undefined,
        name: Any = Undefined,
        url: Any = Undefined,
        values: Any = Undefined,
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


class DomEventType(GenomeSpySchema):
    """Generated wrapper for ``DomEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class DomainValue(GenomeSpySchema):
    """Generated wrapper for ``DomainValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomainValue", {})

    def __init__(self, expr: Any = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)


class DomainValueArray(GenomeSpySchema):
    """Generated wrapper for ``DomainValueArray``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DomainValueArray", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class DsvDataFormat(GenomeSpySchema):
    """Generated wrapper for ``DsvDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DsvDataFormat", {})

    def __init__(
        self,
        columns: Any = Undefined,
        delimiter: Any = Undefined,
        parse: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(columns=columns, delimiter=delimiter, parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)


class DynamicCallbackData(GenomeSpySchema):
    """Generated wrapper for ``DynamicCallbackData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DynamicCallbackData", {})

    def __init__(
        self,
        description: Any = Undefined,
        dynamicCallbackSource: Any = Undefined,
        format: Any = Undefined,
        name: Any = Undefined,
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


class DynamicOpacity(GenomeSpySchema):
    """Generated wrapper for ``DynamicOpacity``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("DynamicOpacity", {})

    def __init__(
        self,
        channel: Any = Undefined,
        unitsPerPixel: Any = Undefined,
        values: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, unitsPerPixel=unitsPerPixel, values=values)
        if kwds:
            self._kwds.update(kwds)


class Encoding(GenomeSpySchema):
    """Generated wrapper for ``Encoding``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Encoding", {})

    def __init__(
        self,
        angle: Any = Undefined,
        color: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        facetIndex: Any = Undefined,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        key: Any = Undefined,
        opacity: Any = Undefined,
        sample: Any = Undefined,
        search: Any = Undefined,
        semanticScore: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        text: Any = Undefined,
        uniqueId: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
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


class EventConfig(GenomeSpySchema):
    """Generated wrapper for ``EventConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("EventConfig", {})

    def __init__(
        self, filter: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(filter=filter, type=type)
        if kwds:
            self._kwds.update(kwds)


class ExprDef(GenomeSpySchema):
    """Generated wrapper for ``ExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        expr: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            band=band, description=description, expr=expr, title=title, type=type
        )
        if kwds:
            self._kwds.update(kwds)


class ExprFilterParams(GenomeSpySchema):
    """Generated wrapper for ``ExprFilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprFilterParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        expr: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, expr=expr, type=type)
        if kwds:
            self._kwds.update(kwds)


class ExprRef(GenomeSpySchema):
    """Generated wrapper for ``ExprRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprRef", {})

    def __init__(self, expr: Any = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)


class Field(GenomeSpySchema):
    """Generated wrapper for ``Field``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Field", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class FieldDefWithoutScale(GenomeSpySchema):
    """Generated wrapper for ``FieldDefWithoutScale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FieldDefWithoutScale", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        title: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)


class FieldName(GenomeSpySchema):
    """Generated wrapper for ``FieldName``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FieldName", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,(string|null)>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<Type>,number>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull(
    GenomeSpySchema
):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<MarkPropFieldDef<TypeForShape>,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<MarkPropFieldDef<TypeForShape>,(string|null)>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class FieldOrDatumDefWithConditionScaleDatumDefStringNull(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<ScaleDatumDef,(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<ScaleDatumDef,(string|null)>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class FieldOrDatumDefWithConditionScaleDatumDefNumber(GenomeSpySchema):
    """Generated wrapper for ``FieldOrDatumDefWithCondition<ScaleDatumDef,number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FieldOrDatumDefWithCondition<ScaleDatumDef,number>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class FilterParams(GenomeSpySchema):
    """Generated wrapper for ``FilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FilterParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        expr: Any = Undefined,
        fields: Any = Undefined,
        param: Any = Undefined,
        type: Any = Undefined,
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


class FilterScoredLabelsParams(GenomeSpySchema):
    """Generated wrapper for ``FilterScoredLabelsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FilterScoredLabelsParams", {})

    def __init__(
        self,
        asMidpoint: Any = Undefined,
        channel: Any = Undefined,
        description: Any = Undefined,
        lane: Any = Undefined,
        padding: Any = Undefined,
        pos: Any = Undefined,
        pos2: Any = Undefined,
        score: Any = Undefined,
        type: Any = Undefined,
        width: Any = Undefined,
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


class FlattenCompressedExonsParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenCompressedExonsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "FlattenCompressedExonsParams", {}
    )

    def __init__(
        self,
        description: Any = Undefined,
        exons: Any = Undefined,
        start: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, exons=exons, start=start, type=type)
        if kwds:
            self._kwds.update(kwds)


class FlattenDelimitedParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenDelimitedParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenDelimitedParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        separator: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, field=field, separator=separator, type=type
        )
        if kwds:
            self._kwds.update(kwds)


class FlattenParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        fields: Any = Undefined,
        index: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, fields=fields, index=index, type=type)
        if kwds:
            self._kwds.update(kwds)


class FlattenSequenceParams(GenomeSpySchema):
    """Generated wrapper for ``FlattenSequenceParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FlattenSequenceParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, type=type)
        if kwds:
            self._kwds.update(kwds)


class FontStyle(GenomeSpySchema):
    """Generated wrapper for ``FontStyle``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FontStyle", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class FontWeight(GenomeSpySchema):
    """Generated wrapper for ``FontWeight``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FontWeight", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class FormulaParams(GenomeSpySchema):
    """Generated wrapper for ``FormulaParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("FormulaParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        expr: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, expr=expr, type=type)
        if kwds:
            self._kwds.update(kwds)


class Generator(GenomeSpySchema):
    """Generated wrapper for ``Generator``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Generator", {})

    def __init__(
        self,
        description: Any = Undefined,
        name: Any = Undefined,
        sequence: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, name=name, sequence=sequence)
        if kwds:
            self._kwds.update(kwds)


class GenomeAxis(GenomeSpySchema):
    """Generated wrapper for ``GenomeAxis``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeAxis", {})

    def __init__(
        self,
        chromGrid: Any = Undefined,
        chromGridCap: Any = Undefined,
        chromGridColor: Any = Undefined,
        chromGridDash: Any = Undefined,
        chromGridDashOffset: Any = Undefined,
        chromGridFillEven: Any = Undefined,
        chromGridFillOdd: Any = Undefined,
        chromGridOpacity: Any = Undefined,
        chromGridWidth: Any = Undefined,
        chromLabelAlign: Any = Undefined,
        chromLabelColor: Any = Undefined,
        chromLabelFont: Any = Undefined,
        chromLabelFontSize: Any = Undefined,
        chromLabelFontStyle: Any = Undefined,
        chromLabelFontWeight: Any = Undefined,
        chromLabelPadding: Any = Undefined,
        chromLabels: Any = Undefined,
        chromTickColor: Any = Undefined,
        chromTickDash: Any = Undefined,
        chromTickDashOffset: Any = Undefined,
        chromTickSize: Any = Undefined,
        chromTickWidth: Any = Undefined,
        chromTicks: Any = Undefined,
        domain: Any = Undefined,
        domainCap: Any = Undefined,
        domainColor: Any = Undefined,
        domainDash: Any = Undefined,
        domainDashOffset: Any = Undefined,
        domainWidth: Any = Undefined,
        format: Any = Undefined,
        grid: Any = Undefined,
        gridCap: Any = Undefined,
        gridColor: Any = Undefined,
        gridDash: Any = Undefined,
        gridDashOffset: Any = Undefined,
        gridOpacity: Any = Undefined,
        gridWidth: Any = Undefined,
        labelAlign: Any = Undefined,
        labelAngle: Any = Undefined,
        labelBaseline: Any = Undefined,
        labelColor: Any = Undefined,
        labelFont: Any = Undefined,
        labelFontSize: Any = Undefined,
        labelFontStyle: Any = Undefined,
        labelFontWeight: Any = Undefined,
        labelLimit: Any = Undefined,
        labelPadding: Any = Undefined,
        labels: Any = Undefined,
        maxExtent: Any = Undefined,
        minExtent: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        placement: Any = Undefined,
        style: Any = Undefined,
        tickCap: Any = Undefined,
        tickColor: Any = Undefined,
        tickCount: Any = Undefined,
        tickDash: Any = Undefined,
        tickDashOffset: Any = Undefined,
        tickMinStep: Any = Undefined,
        tickSize: Any = Undefined,
        tickWidth: Any = Undefined,
        ticks: Any = Undefined,
        title: Any = Undefined,
        titleColor: Any = Undefined,
        titleFit: Any = Undefined,
        titleFont: Any = Undefined,
        titleFontSize: Any = Undefined,
        titleFontStyle: Any = Undefined,
        titleFontWeight: Any = Undefined,
        titleOpacity: Any = Undefined,
        titlePadding: Any = Undefined,
        values: Any = Undefined,
        zindex: Any = Undefined,
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


class GenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``GenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeConfig", {})

    def __init__(
        self,
        contigs: Any = Undefined,
        name: Any = Undefined,
        url: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(contigs=contigs, name=name, url=url)
        if kwds:
            self._kwds.update(kwds)


class GenomeConfigBase(GenomeSpySchema):
    """Generated wrapper for ``GenomeConfigBase``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeConfigBase", {})

    def __init__(self, name: Any = Undefined, **kwds: Any) -> None:
        super().__init__(name=name)
        if kwds:
            self._kwds.update(kwds)


class GenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``GenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeDefinition", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)


class GenomeSpyConfig(GenomeSpySchema):
    """Generated wrapper for ``GenomeSpyConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeSpyConfig", {})

    def __init__(
        self,
        axis: Any = Undefined,
        axisBottom: Any = Undefined,
        axisIndex: Any = Undefined,
        axisLeft: Any = Undefined,
        axisLocus: Any = Undefined,
        axisNominal: Any = Undefined,
        axisOrdinal: Any = Undefined,
        axisQuantitative: Any = Undefined,
        axisRight: Any = Undefined,
        axisTop: Any = Undefined,
        axisX: Any = Undefined,
        axisY: Any = Undefined,
        legend: Any = Undefined,
        legendTrack: Any = Undefined,
        link: Any = Undefined,
        mark: Any = Undefined,
        point: Any = Undefined,
        range: Any = Undefined,
        rect: Any = Undefined,
        rule: Any = Undefined,
        scale: Any = Undefined,
        style: Any = Undefined,
        text: Any = Undefined,
        tick: Any = Undefined,
        title: Any = Undefined,
        view: Any = Undefined,
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


class Gff3Data(GenomeSpySchema):
    """Generated wrapper for ``Gff3Data``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Gff3Data", {})

    def __init__(
        self,
        addChrPrefix: Any = Undefined,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        indexUrl: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class HConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``HConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("HConcatSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        hconcat: Any = Undefined,
        height: Any = Undefined,
        legends: Any = Undefined,
        name: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        separator: Any = Undefined,
        spacing: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class HandledTooltip(GenomeSpySchema):
    """Generated wrapper for ``HandledTooltip``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("HandledTooltip", {})

    def __init__(
        self, handler: Any = Undefined, params: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(handler=handler, params=params)
        if kwds:
            self._kwds.update(kwds)


class IdentifierParams(GenomeSpySchema):
    """Generated wrapper for ``IdentifierParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IdentifierParams", {})

    def __init__(
        self, description: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)


class ImportSpec(GenomeSpySchema):
    """Generated wrapper for ``ImportSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ImportSpec", {})

    def __init__(
        self,
        config: Any = Undefined,
        name: Any = Undefined,
        params: Any = Undefined,
        visible: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(config=config, name=name, params=params, visible=visible)
        if kwds:
            self._kwds.update(kwds)


class IndexUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlSourceRef", {})

    def __init__(
        self, expr: Any = Undefined, template: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(expr=expr, template=template)
        if kwds:
            self._kwds.update(kwds)


class IndexUrlTemplate(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlTemplate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlTemplate", {})

    def __init__(self, template: Any = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)


class IndexedFastaData(GenomeSpySchema):
    """Generated wrapper for ``IndexedFastaData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexedFastaData", {})

    def __init__(
        self,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        indexUrl: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class InlineData(GenomeSpySchema):
    """Generated wrapper for ``InlineData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineData", {})

    def __init__(
        self,
        description: Any = Undefined,
        format: Any = Undefined,
        name: Any = Undefined,
        values: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, format=format, name=name, values=values
        )
        if kwds:
            self._kwds.update(kwds)


class InlineDataset(GenomeSpySchema):
    """Generated wrapper for ``InlineDataset``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineDataset", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class InlineGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``InlineGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineGenomeConfig", {})

    def __init__(
        self, contigs: Any = Undefined, name: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, name=name)
        if kwds:
            self._kwds.update(kwds)


class InlineGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``InlineGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineGenomeDefinition", {})

    def __init__(self, contigs: Any = Undefined, **kwds: Any) -> None:
        super().__init__(contigs=contigs)
        if kwds:
            self._kwds.update(kwds)


class InlineLocusAssembly(GenomeSpySchema):
    """Generated wrapper for ``InlineLocusAssembly``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineLocusAssembly", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)


class InteractionEventType(GenomeSpySchema):
    """Generated wrapper for ``InteractionEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InteractionEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class IntervalSelectionConfig(GenomeSpySchema):
    """Generated wrapper for ``IntervalSelectionConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IntervalSelectionConfig", {})

    def __init__(
        self,
        clear: Any = Undefined,
        encodings: Any = Undefined,
        extent: Any = Undefined,
        mark: Any = Undefined,
        on: Any = Undefined,
        type: Any = Undefined,
        zoom: Any = Undefined,
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


class JsonDataFormat(GenomeSpySchema):
    """Generated wrapper for ``JsonDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("JsonDataFormat", {})

    def __init__(
        self,
        parse: Any = Undefined,
        property: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(parse=parse, property=property, type=type)
        if kwds:
            self._kwds.update(kwds)


class KeyDef(GenomeSpySchema):
    """Generated wrapper for ``KeyDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("KeyDef", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        title: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)


class LayerSpec(GenomeSpySchema):
    """Generated wrapper for ``LayerSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LayerSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        height: Any = Undefined,
        layer: Any = Undefined,
        legends: Any = Undefined,
        name: Any = Undefined,
        opacity: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        view: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class LazyData(GenomeSpySchema):
    """Generated wrapper for ``LazyData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LazyData", {})

    def __init__(
        self, description: Any = Undefined, lazy: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, lazy=lazy)
        if kwds:
            self._kwds.update(kwds)


class LazyDataParams(GenomeSpySchema):
    """Generated wrapper for ``LazyDataParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LazyDataParams", {})

    def __init__(
        self,
        addChrPrefix: Any = Undefined,
        axis: Any = Undefined,
        channel: Any = Undefined,
        columns: Any = Undefined,
        count: Any = Undefined,
        dataType: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        format: Any = Undefined,
        indexUrl: Any = Undefined,
        parse: Any = Undefined,
        pixelsPerBin: Any = Undefined,
        sizeMode: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        values: Any = Undefined,
        windowSize: Any = Undefined,
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


class Legend(GenomeSpySchema):
    """Generated wrapper for ``Legend``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Legend", {})

    def __init__(
        self,
        backgroundFill: Any = Undefined,
        backgroundFillOpacity: Any = Undefined,
        backgroundStroke: Any = Undefined,
        backgroundStrokeOpacity: Any = Undefined,
        backgroundStrokeWidth: Any = Undefined,
        columns: Any = Undefined,
        direction: Any = Undefined,
        labelLimit: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        padding: Any = Undefined,
        style: Any = Undefined,
        symbolSize: Any = Undefined,
        symbolType: Any = Undefined,
        title: Any = Undefined,
        titleOrient: Any = Undefined,
        values: Any = Undefined,
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


class LegendConfig(GenomeSpySchema):
    """Generated wrapper for ``LegendConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendConfig", {})

    def __init__(
        self,
        backgroundFill: Any = Undefined,
        backgroundFillOpacity: Any = Undefined,
        backgroundStroke: Any = Undefined,
        backgroundStrokeOpacity: Any = Undefined,
        backgroundStrokeWidth: Any = Undefined,
        columnPadding: Any = Undefined,
        columns: Any = Undefined,
        direction: Any = Undefined,
        disable: Any = Undefined,
        labelAlign: Any = Undefined,
        labelBaseline: Any = Undefined,
        labelColor: Any = Undefined,
        labelFont: Any = Undefined,
        labelFontSize: Any = Undefined,
        labelFontStyle: Any = Undefined,
        labelFontWeight: Any = Undefined,
        labelLimit: Any = Undefined,
        labelOffset: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        padding: Any = Undefined,
        rowPadding: Any = Undefined,
        spacing: Any = Undefined,
        style: Any = Undefined,
        symbolBaseFillColor: Any = Undefined,
        symbolBaseStrokeColor: Any = Undefined,
        symbolOffset: Any = Undefined,
        symbolSize: Any = Undefined,
        symbolStrokeWidth: Any = Undefined,
        symbolType: Any = Undefined,
        title: Any = Undefined,
        titleColor: Any = Undefined,
        titleFont: Any = Undefined,
        titleFontSize: Any = Undefined,
        titleFontStyle: Any = Undefined,
        titleFontWeight: Any = Undefined,
        titleLimit: Any = Undefined,
        titleOrient: Any = Undefined,
        titlePadding: Any = Undefined,
        values: Any = Undefined,
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


class LegendDirection(GenomeSpySchema):
    """Generated wrapper for ``LegendDirection``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendDirection", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class LegendOrient(GenomeSpySchema):
    """Generated wrapper for ``LegendOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class LegendTitleOrient(GenomeSpySchema):
    """Generated wrapper for ``LegendTitleOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LegendTitleOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class LinearizeGenomicCoordinateParams(GenomeSpySchema):
    """Generated wrapper for ``LinearizeGenomicCoordinateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "LinearizeGenomicCoordinateParams", {}
    )

    def __init__(
        self,
        channel: Any = Undefined,
        chrom: Any = Undefined,
        description: Any = Undefined,
        offset: Any = Undefined,
        pos: Any = Undefined,
        type: Any = Undefined,
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


class LinkConfig(GenomeSpySchema):
    """Generated wrapper for ``LinkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LinkConfig", {})

    def __init__(
        self,
        arcFadingDistance: Any = Undefined,
        arcHeightFactor: Any = Undefined,
        buildIndex: Any = Undefined,
        clampApex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        linkShape: Any = Undefined,
        maxChordLength: Any = Undefined,
        minArcHeight: Any = Undefined,
        minBufferSize: Any = Undefined,
        minPickingSize: Any = Undefined,
        noFadingOnPointSelection: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        segments: Any = Undefined,
        size: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class LinkProps(GenomeSpySchema):
    """Generated wrapper for ``LinkProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LinkProps", {})

    def __init__(
        self,
        arcFadingDistance: Any = Undefined,
        arcHeightFactor: Any = Undefined,
        buildIndex: Any = Undefined,
        clampApex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        linkShape: Any = Undefined,
        maxChordLength: Any = Undefined,
        minArcHeight: Any = Undefined,
        minBufferSize: Any = Undefined,
        minPickingSize: Any = Undefined,
        noFadingOnPointSelection: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        segments: Any = Undefined,
        size: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class MarkConfig(GenomeSpySchema):
    """Generated wrapper for ``MarkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkConfig", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        minBufferSize: Any = Undefined,
        opacity: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        yOffset: Any = Undefined,
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


class MarkPropDefStringNullTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<(string|null),TypeForShape>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "MarkPropDef<(string|null),TypeForShape>", {}
    )

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class MarkPropDefStringNull(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<(string|null)>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropDef<(string|null)>", {})

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class MarkPropDefNumber(GenomeSpySchema):
    """Generated wrapper for ``MarkPropDef<number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropDef<number>", {})

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class MarkPropExprDef(GenomeSpySchema):
    """Generated wrapper for ``MarkPropExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkPropExprDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        expr: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class MarkProps(GenomeSpySchema):
    """Generated wrapper for ``MarkProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkProps", {})

    def __init__(
        self,
        align: Any = Undefined,
        angle: Any = Undefined,
        arcFadingDistance: Any = Undefined,
        arcHeightFactor: Any = Undefined,
        baseline: Any = Undefined,
        buildIndex: Any = Undefined,
        clampApex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cornerRadius: Any = Undefined,
        cornerRadiusBottomLeft: Any = Undefined,
        cornerRadiusBottomRight: Any = Undefined,
        cornerRadiusTopLeft: Any = Undefined,
        cornerRadiusTopRight: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fill: Any = Undefined,
        fillGradientStrength: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        fitToBand: Any = Undefined,
        flushX: Any = Undefined,
        flushY: Any = Undefined,
        font: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        geometricZoomBound: Any = Undefined,
        hatch: Any = Undefined,
        inwardStroke: Any = Undefined,
        linkShape: Any = Undefined,
        logoLetters: Any = Undefined,
        maxChordLength: Any = Undefined,
        minArcHeight: Any = Undefined,
        minBufferSize: Any = Undefined,
        minHeight: Any = Undefined,
        minLength: Any = Undefined,
        minOpacity: Any = Undefined,
        minPickingSize: Any = Undefined,
        minWidth: Any = Undefined,
        noFadingOnPointSelection: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        paddingX: Any = Undefined,
        paddingY: Any = Undefined,
        sampleFacetPadding: Any = Undefined,
        segments: Any = Undefined,
        semanticScore: Any = Undefined,
        semanticZoomFraction: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
        squeeze: Any = Undefined,
        stroke: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        text: Any = Undefined,
        thickness: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        viewportEdgeFadeDistanceBottom: Any = Undefined,
        viewportEdgeFadeDistanceLeft: Any = Undefined,
        viewportEdgeFadeDistanceRight: Any = Undefined,
        viewportEdgeFadeDistanceTop: Any = Undefined,
        viewportEdgeFadeWidthBottom: Any = Undefined,
        viewportEdgeFadeWidthLeft: Any = Undefined,
        viewportEdgeFadeWidthRight: Any = Undefined,
        viewportEdgeFadeWidthTop: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class MarkType(GenomeSpySchema):
    """Generated wrapper for ``MarkType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MarkType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class MeasureTextParams(GenomeSpySchema):
    """Generated wrapper for ``MeasureTextParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MeasureTextParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        type: Any = Undefined,
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


class MergeFacetsParams(GenomeSpySchema):
    """Generated wrapper for ``MergeFacetsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MergeFacetsParams", {})

    def __init__(
        self, description: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)


class MultiUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``MultiUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiUrlSourceRef", {})

    def __init__(
        self,
        attach: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        maxValues: Any = Undefined,
        onLoadError: Any = Undefined,
        template: Any = Undefined,
        values: Any = Undefined,
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


class MultiscaleSpec(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        height: Any = Undefined,
        legends: Any = Undefined,
        multiscale: Any = Undefined,
        name: Any = Undefined,
        opacity: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        stops: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        view: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class MultiscaleStops(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleStops``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleStops", {})

    def __init__(
        self,
        channel: Any = Undefined,
        fade: Any = Undefined,
        metric: Any = Undefined,
        values: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, fade=fade, metric=metric, values=values)
        if kwds:
            self._kwds.update(kwds)


class MultiscaleStopsDef(GenomeSpySchema):
    """Generated wrapper for ``MultiscaleStopsDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MultiscaleStopsDef", {})

    def __init__(
        self,
        channel: Any = Undefined,
        fade: Any = Undefined,
        metric: Any = Undefined,
        values: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(channel=channel, fade=fade, metric=metric, values=values)
        if kwds:
            self._kwds.update(kwds)


class NamedData(GenomeSpySchema):
    """Generated wrapper for ``NamedData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NamedData", {})

    def __init__(
        self,
        description: Any = Undefined,
        format: Any = Undefined,
        name: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, format=format, name=name)
        if kwds:
            self._kwds.update(kwds)


class NamedGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``NamedGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NamedGenomeConfig", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)


class NumericDomain(GenomeSpySchema):
    """Generated wrapper for ``NumericDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class NumericMarkPropDef(GenomeSpySchema):
    """Generated wrapper for ``NumericMarkPropDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericMarkPropDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class NumericStopDef(GenomeSpySchema):
    """Generated wrapper for ``NumericStopDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericStopDef", {})

    def __init__(self, expr: Any = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)


class NumericValueDef(GenomeSpySchema):
    """Generated wrapper for ``NumericValueDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericValueDef", {})

    def __init__(
        self,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)


class OtherDataFormat(GenomeSpySchema):
    """Generated wrapper for ``OtherDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("OtherDataFormat", {})

    def __init__(
        self, parse: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)


class PackLegendLabelsParams(GenomeSpySchema):
    """Generated wrapper for ``PackLegendLabelsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PackLegendLabelsParams", {})

    def __init__(
        self,
        columnPadding: Any = Undefined,
        columns: Any = Undefined,
        description: Any = Undefined,
        direction: Any = Undefined,
        fontSize: Any = Undefined,
        labelOffset: Any = Undefined,
        labelWidth: Any = Undefined,
        rowPadding: Any = Undefined,
        symbolOffset: Any = Undefined,
        symbolSize: Any = Undefined,
        symbolStrokeWidth: Any = Undefined,
        type: Any = Undefined,
        xOffset: Any = Undefined,
        yExtent: Any = Undefined,
        yOffset: Any = Undefined,
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


class PaddingConfig(GenomeSpySchema):
    """Generated wrapper for ``PaddingConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PaddingConfig", {})

    def __init__(
        self,
        bottom: Any = Undefined,
        left: Any = Undefined,
        right: Any = Undefined,
        top: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(bottom=bottom, left=left, right=right, top=top)
        if kwds:
            self._kwds.update(kwds)


class Paddings(GenomeSpySchema):
    """Generated wrapper for ``Paddings``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Paddings", {})

    def __init__(
        self,
        bottom: Any = Undefined,
        left: Any = Undefined,
        right: Any = Undefined,
        top: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(bottom=bottom, left=left, right=right, top=top)
        if kwds:
            self._kwds.update(kwds)


class Parameter(GenomeSpySchema):
    """Generated wrapper for ``Parameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Parameter", {})

    def __init__(
        self,
        bind: Any = Undefined,
        description: Any = Undefined,
        expr: Any = Undefined,
        name: Any = Undefined,
        persist: Any = Undefined,
        push: Any = Undefined,
        ruler: Any = Undefined,
        select: Any = Undefined,
        value: Any = Undefined,
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


class Parse(GenomeSpySchema):
    """Generated wrapper for ``Parse``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Parse", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ParseValue(GenomeSpySchema):
    """Generated wrapper for ``ParseValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ParseValue", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class PileupParams(GenomeSpySchema):
    """Generated wrapper for ``PileupParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PileupParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        end: Any = Undefined,
        preference: Any = Undefined,
        preferredOrder: Any = Undefined,
        spacing: Any = Undefined,
        start: Any = Undefined,
        type: Any = Undefined,
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


class PointConfig(GenomeSpySchema):
    """Generated wrapper for ``PointConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointConfig", {})

    def __init__(
        self,
        angle: Any = Undefined,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fill: Any = Undefined,
        fillGradientStrength: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        geometricZoomBound: Any = Undefined,
        inwardStroke: Any = Undefined,
        minBufferSize: Any = Undefined,
        minPickingSize: Any = Undefined,
        opacity: Any = Undefined,
        sampleFacetPadding: Any = Undefined,
        semanticScore: Any = Undefined,
        semanticZoomFraction: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        yOffset: Any = Undefined,
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


class PointProps(GenomeSpySchema):
    """Generated wrapper for ``PointProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointProps", {})

    def __init__(
        self,
        angle: Any = Undefined,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fill: Any = Undefined,
        fillGradientStrength: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        geometricZoomBound: Any = Undefined,
        inwardStroke: Any = Undefined,
        minBufferSize: Any = Undefined,
        minPickingSize: Any = Undefined,
        opacity: Any = Undefined,
        sampleFacetPadding: Any = Undefined,
        semanticScore: Any = Undefined,
        semanticZoomFraction: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        yOffset: Any = Undefined,
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


class PointSelectionConfig(GenomeSpySchema):
    """Generated wrapper for ``PointSelectionConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PointSelectionConfig", {})

    def __init__(
        self,
        clear: Any = Undefined,
        on: Any = Undefined,
        toggle: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(clear=clear, on=on, toggle=toggle, type=type)
        if kwds:
            self._kwds.update(kwds)


class Position2Def(GenomeSpySchema):
    """Generated wrapper for ``Position2Def``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Position2Def", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        chrom: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        offset: Any = Undefined,
        pos: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class PositionDatumDef(GenomeSpySchema):
    """Generated wrapper for ``PositionDatumDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionDatumDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class PositionDef(GenomeSpySchema):
    """Generated wrapper for ``PositionDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        chrom: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        offset: Any = Undefined,
        pos: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class PositionExprDef(GenomeSpySchema):
    """Generated wrapper for ``PositionExprDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionExprDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        expr: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class PositionFieldDef(GenomeSpySchema):
    """Generated wrapper for ``PositionFieldDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionFieldDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class PositionValueDef(GenomeSpySchema):
    """Generated wrapper for ``PositionValueDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionValueDef", {})

    def __init__(
        self,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)


class PositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``PositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class PrimaryPositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``PrimaryPositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("PrimaryPositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ProjectParams(GenomeSpySchema):
    """Generated wrapper for ``ProjectParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ProjectParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        fields: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, fields=fields, type=type)
        if kwds:
            self._kwds.update(kwds)


class RangeConfig(GenomeSpySchema):
    """Generated wrapper for ``RangeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RangeConfig", {})

    def __init__(
        self,
        angle: Any = Undefined,
        diverging: Any = Undefined,
        heatmap: Any = Undefined,
        ramp: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
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


class RectConfig(GenomeSpySchema):
    """Generated wrapper for ``RectConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RectConfig", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cornerRadius: Any = Undefined,
        cornerRadiusBottomLeft: Any = Undefined,
        cornerRadiusBottomRight: Any = Undefined,
        cornerRadiusTopLeft: Any = Undefined,
        cornerRadiusTopRight: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        hatch: Any = Undefined,
        minBufferSize: Any = Undefined,
        minHeight: Any = Undefined,
        minOpacity: Any = Undefined,
        minWidth: Any = Undefined,
        opacity: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class RectProps(GenomeSpySchema):
    """Generated wrapper for ``RectProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RectProps", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cornerRadius: Any = Undefined,
        cornerRadiusBottomLeft: Any = Undefined,
        cornerRadiusBottomRight: Any = Undefined,
        cornerRadiusTopLeft: Any = Undefined,
        cornerRadiusTopRight: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        hatch: Any = Undefined,
        minBufferSize: Any = Undefined,
        minHeight: Any = Undefined,
        minOpacity: Any = Undefined,
        minWidth: Any = Undefined,
        opacity: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class RegexExtractParams(GenomeSpySchema):
    """Generated wrapper for ``RegexExtractParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RegexExtractParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        regex: Any = Undefined,
        skipInvalidInput: Any = Undefined,
        type: Any = Undefined,
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


class RegexFoldParams(GenomeSpySchema):
    """Generated wrapper for ``RegexFoldParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RegexFoldParams", {})

    def __init__(
        self,
        asKey: Any = Undefined,
        asValue: Any = Undefined,
        columnRegex: Any = Undefined,
        description: Any = Undefined,
        skipRegex: Any = Undefined,
        type: Any = Undefined,
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


class ResolutionBehavior(GenomeSpySchema):
    """Generated wrapper for ``ResolutionBehavior``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ResolutionBehavior", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RuleConfig(GenomeSpySchema):
    """Generated wrapper for ``RuleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RuleConfig", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        minBufferSize: Any = Undefined,
        minLength: Any = Undefined,
        opacity: Any = Undefined,
        size: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class RuleProps(GenomeSpySchema):
    """Generated wrapper for ``RuleProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RuleProps", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        minBufferSize: Any = Undefined,
        minLength: Any = Undefined,
        opacity: Any = Undefined,
        size: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class RulerChannelValue(GenomeSpySchema):
    """Generated wrapper for ``RulerChannelValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerChannelValue", {})

    def __init__(
        self, chrom: Any = Undefined, pos: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)


class RulerClear(GenomeSpySchema):
    """Generated wrapper for ``RulerClear``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerClear", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RulerConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerConfig", {})

    def __init__(
        self,
        clear: Any = Undefined,
        display: Any = Undefined,
        encodings: Any = Undefined,
        extent: Any = Undefined,
        mark: Any = Undefined,
        on: Any = Undefined,
        snap: Any = Undefined,
        source: Any = Undefined,
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


class RulerDisplay(GenomeSpySchema):
    """Generated wrapper for ``RulerDisplay``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerDisplay", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RulerEventConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerEventConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerEventConfig", {})

    def __init__(
        self, filter: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(filter=filter, type=type)
        if kwds:
            self._kwds.update(kwds)


class RulerEventType(GenomeSpySchema):
    """Generated wrapper for ``RulerEventType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerEventType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RulerExtent(GenomeSpySchema):
    """Generated wrapper for ``RulerExtent``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerExtent", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RulerInitMapping(GenomeSpySchema):
    """Generated wrapper for ``RulerInitMapping``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerInitMapping", {})

    def __init__(self, x: Any = Undefined, y: Any = Undefined, **kwds: Any) -> None:
        super().__init__(x=x, y=y)
        if kwds:
            self._kwds.update(kwds)


class RulerMarkConfig(GenomeSpySchema):
    """Generated wrapper for ``RulerMarkConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerMarkConfig", {})

    def __init__(
        self,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        opacity: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        stroke: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeWidth: Any = Undefined,
        zindex: Any = Undefined,
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


class RulerParameter(GenomeSpySchema):
    """Generated wrapper for ``RulerParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerParameter", {})

    def __init__(
        self,
        description: Any = Undefined,
        name: Any = Undefined,
        persist: Any = Undefined,
        push: Any = Undefined,
        ruler: Any = Undefined,
        value: Any = Undefined,
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


class RulerSnap(GenomeSpySchema):
    """Generated wrapper for ``RulerSnap``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerSnap", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class RulerSource(GenomeSpySchema):
    """Generated wrapper for ``RulerSource``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerSource", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class SampleParams(GenomeSpySchema):
    """Generated wrapper for ``SampleParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SampleParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        size: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, size=size, type=type)
        if kwds:
            self._kwds.update(kwds)


class Scalar(GenomeSpySchema):
    """Generated wrapper for ``Scalar``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Scalar", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ScalarDomain(GenomeSpySchema):
    """Generated wrapper for ``ScalarDomain``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScalarDomain", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class Scale(GenomeSpySchema):
    """Generated wrapper for ``Scale``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Scale", {})

    def __init__(
        self,
        align: Any = Undefined,
        assembly: Any = Undefined,
        base: Any = Undefined,
        bins: Any = Undefined,
        clamp: Any = Undefined,
        constant: Any = Undefined,
        domain: Any = Undefined,
        domainMax: Any = Undefined,
        domainMid: Any = Undefined,
        domainMin: Any = Undefined,
        domainTransition: Any = Undefined,
        exponent: Any = Undefined,
        interpolate: Any = Undefined,
        name: Any = Undefined,
        nice: Any = Undefined,
        numberingOffset: Any = Undefined,
        padding: Any = Undefined,
        paddingInner: Any = Undefined,
        paddingOuter: Any = Undefined,
        range: Any = Undefined,
        reverse: Any = Undefined,
        round: Any = Undefined,
        scheme: Any = Undefined,
        type: Any = Undefined,
        zero: Any = Undefined,
        zoom: Any = Undefined,
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


class ScaleConfig(GenomeSpySchema):
    """Generated wrapper for ``ScaleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleConfig", {})

    def __init__(
        self,
        align: Any = Undefined,
        assembly: Any = Undefined,
        base: Any = Undefined,
        bins: Any = Undefined,
        clamp: Any = Undefined,
        constant: Any = Undefined,
        domain: Any = Undefined,
        domainMax: Any = Undefined,
        domainMid: Any = Undefined,
        domainMin: Any = Undefined,
        domainTransition: Any = Undefined,
        exponent: Any = Undefined,
        index: Any = Undefined,
        interpolate: Any = Undefined,
        locus: Any = Undefined,
        name: Any = Undefined,
        nice: Any = Undefined,
        nominal: Any = Undefined,
        nominalColorScheme: Any = Undefined,
        numberingOffset: Any = Undefined,
        ordinal: Any = Undefined,
        ordinalColorScheme: Any = Undefined,
        padding: Any = Undefined,
        paddingInner: Any = Undefined,
        paddingOuter: Any = Undefined,
        quantitative: Any = Undefined,
        quantitativeColorScheme: Any = Undefined,
        range: Any = Undefined,
        reverse: Any = Undefined,
        round: Any = Undefined,
        scheme: Any = Undefined,
        type: Any = Undefined,
        zero: Any = Undefined,
        zoom: Any = Undefined,
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


class ScaleInterpolate(GenomeSpySchema):
    """Generated wrapper for ``ScaleInterpolate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleInterpolate", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class ScaleInterpolateParams(GenomeSpySchema):
    """Generated wrapper for ``ScaleInterpolateParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleInterpolateParams", {})

    def __init__(
        self, gamma: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(gamma=gamma, type=type)
        if kwds:
            self._kwds.update(kwds)


class ScaleType(GenomeSpySchema):
    """Generated wrapper for ``ScaleType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ScaleType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class SchemeParams(GenomeSpySchema):
    """Generated wrapper for ``SchemeParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SchemeParams", {})

    def __init__(
        self,
        count: Any = Undefined,
        extent: Any = Undefined,
        name: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(count=count, extent=extent, name=name)
        if kwds:
            self._kwds.update(kwds)


class SearchDef(GenomeSpySchema):
    """Generated wrapper for ``SearchDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SearchDef", {})

    def __init__(
        self,
        description: Any = Undefined,
        field: Any = Undefined,
        title: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, field=field, title=title)
        if kwds:
            self._kwds.update(kwds)


class SecondaryChromPosDef(GenomeSpySchema):
    """Generated wrapper for ``SecondaryChromPosDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SecondaryChromPosDef", {})

    def __init__(
        self,
        axis: Any = Undefined,
        band: Any = Undefined,
        chrom: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        offset: Any = Undefined,
        pos: Any = Undefined,
        title: Any = Undefined,
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


class SecondaryPositionalChannel(GenomeSpySchema):
    """Generated wrapper for ``SecondaryPositionalChannel``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SecondaryPositionalChannel", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class SelectionDomainRef(GenomeSpySchema):
    """Generated wrapper for ``SelectionDomainRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionDomainRef", {})

    def __init__(
        self,
        encoding: Any = Undefined,
        initial: Any = Undefined,
        param: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(encoding=encoding, initial=initial, param=param)
        if kwds:
            self._kwds.update(kwds)


class SelectionExtent(GenomeSpySchema):
    """Generated wrapper for ``SelectionExtent``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionExtent", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class SelectionFilterParams(GenomeSpySchema):
    """Generated wrapper for ``SelectionFilterParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionFilterParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        empty: Any = Undefined,
        fields: Any = Undefined,
        param: Any = Undefined,
        type: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            description=description, empty=empty, fields=fields, param=param, type=type
        )
        if kwds:
            self._kwds.update(kwds)


class SelectionInitIntervalMapping(GenomeSpySchema):
    """Generated wrapper for ``SelectionInitIntervalMapping``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "SelectionInitIntervalMapping", {}
    )

    def __init__(self, x: Any = Undefined, y: Any = Undefined, **kwds: Any) -> None:
        super().__init__(x=x, y=y)
        if kwds:
            self._kwds.update(kwds)


class SelectionParameter(GenomeSpySchema):
    """Generated wrapper for ``SelectionParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionParameter", {})

    def __init__(
        self,
        description: Any = Undefined,
        name: Any = Undefined,
        persist: Any = Undefined,
        push: Any = Undefined,
        select: Any = Undefined,
        value: Any = Undefined,
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


class SelectionType(GenomeSpySchema):
    """Generated wrapper for ``SelectionType``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SelectionType", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class SeparatorProps(GenomeSpySchema):
    """Generated wrapper for ``SeparatorProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SeparatorProps", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        includePlotMargin: Any = Undefined,
        minBufferSize: Any = Undefined,
        minLength: Any = Undefined,
        opacity: Any = Undefined,
        size: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        style: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
        zindex: Any = Undefined,
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


class SequenceGenerator(GenomeSpySchema):
    """Generated wrapper for ``SequenceGenerator``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SequenceGenerator", {})

    def __init__(
        self,
        description: Any = Undefined,
        name: Any = Undefined,
        sequence: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, name=name, sequence=sequence)
        if kwds:
            self._kwds.update(kwds)


class SequenceParams(GenomeSpySchema):
    """Generated wrapper for ``SequenceParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SequenceParams", {})

    def __init__(
        self,
        start: Any = Undefined,
        step: Any = Undefined,
        stop: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(start=start, step=step, stop=stop)
        if kwds:
            self._kwds.update(kwds)


class ShapeDef(GenomeSpySchema):
    """Generated wrapper for ``ShapeDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ShapeDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        condition: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        legend: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class SingleUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``SingleUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SingleUrlSourceRef", {})

    def __init__(
        self,
        attach: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        maxValues: Any = Undefined,
        onLoadError: Any = Undefined,
        template: Any = Undefined,
        values: Any = Undefined,
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


class SizeDef(GenomeSpySchema):
    """Generated wrapper for ``SizeDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SizeDef", {})

    def __init__(
        self,
        grow: Any = Undefined,
        maxPx: Any = Undefined,
        minPx: Any = Undefined,
        px: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(grow=grow, maxPx=maxPx, minPx=minPx, px=px)
        if kwds:
            self._kwds.update(kwds)


class SortOrder(GenomeSpySchema):
    """Generated wrapper for ``SortOrder``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("SortOrder", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class StackParams(GenomeSpySchema):
    """Generated wrapper for ``StackParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StackParams", {})

    def __init__(
        self,
        baseField: Any = Undefined,
        cardinality: Any = Undefined,
        description: Any = Undefined,
        field: Any = Undefined,
        groupby: Any = Undefined,
        offset: Any = Undefined,
        sort: Any = Undefined,
        type: Any = Undefined,
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


class Step(GenomeSpySchema):
    """Generated wrapper for ``Step``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Step", {})

    def __init__(self, step: Any = Undefined, **kwds: Any) -> None:
        super().__init__(step=step)
        if kwds:
            self._kwds.update(kwds)


class StringDatumDef(GenomeSpySchema):
    """Generated wrapper for ``StringDatumDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StringDatumDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        format: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class StringFieldDef(GenomeSpySchema):
    """Generated wrapper for ``StringFieldDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StringFieldDef", {})

    def __init__(
        self,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
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


class StyleConfig(GenomeSpySchema):
    """Generated wrapper for ``StyleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("StyleConfig", {})

    def __init__(
        self,
        align: Any = Undefined,
        anchor: Any = Undefined,
        angle: Any = Undefined,
        arcFadingDistance: Any = Undefined,
        arcHeightFactor: Any = Undefined,
        backgroundFill: Any = Undefined,
        backgroundFillOpacity: Any = Undefined,
        backgroundStroke: Any = Undefined,
        backgroundStrokeOpacity: Any = Undefined,
        backgroundStrokeWidth: Any = Undefined,
        baseline: Any = Undefined,
        buildIndex: Any = Undefined,
        chromGrid: Any = Undefined,
        chromGridCap: Any = Undefined,
        chromGridColor: Any = Undefined,
        chromGridDash: Any = Undefined,
        chromGridDashOffset: Any = Undefined,
        chromGridFillEven: Any = Undefined,
        chromGridFillOdd: Any = Undefined,
        chromGridOpacity: Any = Undefined,
        chromGridWidth: Any = Undefined,
        chromLabelAlign: Any = Undefined,
        chromLabelColor: Any = Undefined,
        chromLabelFont: Any = Undefined,
        chromLabelFontSize: Any = Undefined,
        chromLabelFontStyle: Any = Undefined,
        chromLabelFontWeight: Any = Undefined,
        chromLabelPadding: Any = Undefined,
        chromLabels: Any = Undefined,
        chromTickColor: Any = Undefined,
        chromTickDash: Any = Undefined,
        chromTickDashOffset: Any = Undefined,
        chromTickSize: Any = Undefined,
        chromTickWidth: Any = Undefined,
        chromTicks: Any = Undefined,
        clampApex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        columnPadding: Any = Undefined,
        columns: Any = Undefined,
        cornerRadius: Any = Undefined,
        cornerRadiusBottomLeft: Any = Undefined,
        cornerRadiusBottomRight: Any = Undefined,
        cornerRadiusTopLeft: Any = Undefined,
        cornerRadiusTopRight: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        direction: Any = Undefined,
        disable: Any = Undefined,
        domain: Any = Undefined,
        domainCap: Any = Undefined,
        domainColor: Any = Undefined,
        domainDash: Any = Undefined,
        domainDashOffset: Any = Undefined,
        domainWidth: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fill: Any = Undefined,
        fillGradientStrength: Any = Undefined,
        fillOpacity: Any = Undefined,
        filled: Any = Undefined,
        fitToBand: Any = Undefined,
        flushX: Any = Undefined,
        flushY: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        format: Any = Undefined,
        frame: Any = Undefined,
        geometricZoomBound: Any = Undefined,
        grid: Any = Undefined,
        gridCap: Any = Undefined,
        gridColor: Any = Undefined,
        gridDash: Any = Undefined,
        gridDashOffset: Any = Undefined,
        gridOpacity: Any = Undefined,
        gridWidth: Any = Undefined,
        hatch: Any = Undefined,
        inwardStroke: Any = Undefined,
        labelAlign: Any = Undefined,
        labelAngle: Any = Undefined,
        labelBaseline: Any = Undefined,
        labelColor: Any = Undefined,
        labelFont: Any = Undefined,
        labelFontSize: Any = Undefined,
        labelFontStyle: Any = Undefined,
        labelFontWeight: Any = Undefined,
        labelLimit: Any = Undefined,
        labelOffset: Any = Undefined,
        labelPadding: Any = Undefined,
        labels: Any = Undefined,
        linkShape: Any = Undefined,
        logoLetters: Any = Undefined,
        maxChordLength: Any = Undefined,
        maxExtent: Any = Undefined,
        minArcHeight: Any = Undefined,
        minBufferSize: Any = Undefined,
        minExtent: Any = Undefined,
        minHeight: Any = Undefined,
        minLength: Any = Undefined,
        minOpacity: Any = Undefined,
        minPickingSize: Any = Undefined,
        minWidth: Any = Undefined,
        noFadingOnPointSelection: Any = Undefined,
        offset: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        padding: Any = Undefined,
        paddingX: Any = Undefined,
        paddingY: Any = Undefined,
        placement: Any = Undefined,
        reserve: Any = Undefined,
        rowPadding: Any = Undefined,
        sampleFacetPadding: Any = Undefined,
        segments: Any = Undefined,
        semanticScore: Any = Undefined,
        semanticZoomFraction: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        shape: Any = Undefined,
        size: Any = Undefined,
        spacing: Any = Undefined,
        squeeze: Any = Undefined,
        stroke: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        style: Any = Undefined,
        subtitle: Any = Undefined,
        subtitleColor: Any = Undefined,
        subtitleFont: Any = Undefined,
        subtitleFontSize: Any = Undefined,
        subtitleFontStyle: Any = Undefined,
        subtitleFontWeight: Any = Undefined,
        subtitlePadding: Any = Undefined,
        symbolBaseFillColor: Any = Undefined,
        symbolBaseStrokeColor: Any = Undefined,
        symbolOffset: Any = Undefined,
        symbolSize: Any = Undefined,
        symbolStrokeWidth: Any = Undefined,
        symbolType: Any = Undefined,
        text: Any = Undefined,
        thickness: Any = Undefined,
        tickCap: Any = Undefined,
        tickColor: Any = Undefined,
        tickCount: Any = Undefined,
        tickDash: Any = Undefined,
        tickDashOffset: Any = Undefined,
        tickMinStep: Any = Undefined,
        tickSize: Any = Undefined,
        tickWidth: Any = Undefined,
        ticks: Any = Undefined,
        title: Any = Undefined,
        titleColor: Any = Undefined,
        titleFit: Any = Undefined,
        titleFont: Any = Undefined,
        titleFontSize: Any = Undefined,
        titleFontStyle: Any = Undefined,
        titleFontWeight: Any = Undefined,
        titleLimit: Any = Undefined,
        titleOpacity: Any = Undefined,
        titleOrient: Any = Undefined,
        titlePadding: Any = Undefined,
        tooltip: Any = Undefined,
        values: Any = Undefined,
        viewportEdgeFadeDistanceBottom: Any = Undefined,
        viewportEdgeFadeDistanceLeft: Any = Undefined,
        viewportEdgeFadeDistanceRight: Any = Undefined,
        viewportEdgeFadeDistanceTop: Any = Undefined,
        viewportEdgeFadeWidthBottom: Any = Undefined,
        viewportEdgeFadeWidthLeft: Any = Undefined,
        viewportEdgeFadeWidthRight: Any = Undefined,
        viewportEdgeFadeWidthTop: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
        zindex: Any = Undefined,
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


class TabixTsvData(GenomeSpySchema):
    """Generated wrapper for ``TabixTsvData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TabixTsvData", {})

    def __init__(
        self,
        addChrPrefix: Any = Undefined,
        channel: Any = Undefined,
        columns: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        indexUrl: Any = Undefined,
        parse: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class TemplateImport(GenomeSpySchema):
    """Generated wrapper for ``TemplateImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TemplateImport", {})

    def __init__(self, template: Any = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)


class TextConfig(GenomeSpySchema):
    """Generated wrapper for ``TextConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextConfig", {})

    def __init__(
        self,
        align: Any = Undefined,
        angle: Any = Undefined,
        baseline: Any = Undefined,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fitToBand: Any = Undefined,
        flushX: Any = Undefined,
        flushY: Any = Undefined,
        font: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        logoLetters: Any = Undefined,
        minBufferSize: Any = Undefined,
        opacity: Any = Undefined,
        paddingX: Any = Undefined,
        paddingY: Any = Undefined,
        size: Any = Undefined,
        squeeze: Any = Undefined,
        style: Any = Undefined,
        text: Any = Undefined,
        tooltip: Any = Undefined,
        viewportEdgeFadeDistanceBottom: Any = Undefined,
        viewportEdgeFadeDistanceLeft: Any = Undefined,
        viewportEdgeFadeDistanceRight: Any = Undefined,
        viewportEdgeFadeDistanceTop: Any = Undefined,
        viewportEdgeFadeWidthBottom: Any = Undefined,
        viewportEdgeFadeWidthLeft: Any = Undefined,
        viewportEdgeFadeWidthRight: Any = Undefined,
        viewportEdgeFadeWidthTop: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class TextDef(GenomeSpySchema):
    """Generated wrapper for ``TextDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextDef", {})

    def __init__(
        self,
        band: Any = Undefined,
        datum: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        format: Any = Undefined,
        resolutionChannel: Any = Undefined,
        scale: Any = Undefined,
        title: Any = Undefined,
        type: Any = Undefined,
        value: Any = Undefined,
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


class TextProps(GenomeSpySchema):
    """Generated wrapper for ``TextProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TextProps", {})

    def __init__(
        self,
        align: Any = Undefined,
        angle: Any = Undefined,
        baseline: Any = Undefined,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        fitToBand: Any = Undefined,
        flushX: Any = Undefined,
        flushY: Any = Undefined,
        font: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        logoLetters: Any = Undefined,
        minBufferSize: Any = Undefined,
        opacity: Any = Undefined,
        paddingX: Any = Undefined,
        paddingY: Any = Undefined,
        size: Any = Undefined,
        squeeze: Any = Undefined,
        style: Any = Undefined,
        text: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        viewportEdgeFadeDistanceBottom: Any = Undefined,
        viewportEdgeFadeDistanceLeft: Any = Undefined,
        viewportEdgeFadeDistanceRight: Any = Undefined,
        viewportEdgeFadeDistanceTop: Any = Undefined,
        viewportEdgeFadeWidthBottom: Any = Undefined,
        viewportEdgeFadeWidthLeft: Any = Undefined,
        viewportEdgeFadeWidthRight: Any = Undefined,
        viewportEdgeFadeWidthTop: Any = Undefined,
        x: Any = Undefined,
        x2: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        y2: Any = Undefined,
        yOffset: Any = Undefined,
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


class TickConfig(GenomeSpySchema):
    """Generated wrapper for ``TickConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TickConfig", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        minBufferSize: Any = Undefined,
        minLength: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        style: Any = Undefined,
        thickness: Any = Undefined,
        tooltip: Any = Undefined,
        x: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        yOffset: Any = Undefined,
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


class TickProps(GenomeSpySchema):
    """Generated wrapper for ``TickProps``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TickProps", {})

    def __init__(
        self,
        buildIndex: Any = Undefined,
        clip: Any = Undefined,
        color: Any = Undefined,
        cullByVisibleRange: Any = Undefined,
        cursor: Any = Undefined,
        minBufferSize: Any = Undefined,
        minLength: Any = Undefined,
        opacity: Any = Undefined,
        orient: Any = Undefined,
        strokeCap: Any = Undefined,
        strokeDash: Any = Undefined,
        strokeDashOffset: Any = Undefined,
        style: Any = Undefined,
        thickness: Any = Undefined,
        tooltip: Any = Undefined,
        type: Any = Undefined,
        x: Any = Undefined,
        xOffset: Any = Undefined,
        y: Any = Undefined,
        yOffset: Any = Undefined,
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


class Title(GenomeSpySchema):
    """Generated wrapper for ``Title``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Title", {})

    def __init__(
        self,
        align: Any = Undefined,
        anchor: Any = Undefined,
        angle: Any = Undefined,
        baseline: Any = Undefined,
        color: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        frame: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        reserve: Any = Undefined,
        style: Any = Undefined,
        subtitle: Any = Undefined,
        subtitleColor: Any = Undefined,
        subtitleFont: Any = Undefined,
        subtitleFontSize: Any = Undefined,
        subtitleFontStyle: Any = Undefined,
        subtitleFontWeight: Any = Undefined,
        subtitlePadding: Any = Undefined,
        text: Any = Undefined,
        zindex: Any = Undefined,
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


class TitleAnchor(GenomeSpySchema):
    """Generated wrapper for ``TitleAnchor``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleAnchor", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class TitleConfig(GenomeSpySchema):
    """Generated wrapper for ``TitleConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleConfig", {})

    def __init__(
        self,
        align: Any = Undefined,
        anchor: Any = Undefined,
        angle: Any = Undefined,
        baseline: Any = Undefined,
        color: Any = Undefined,
        dx: Any = Undefined,
        dy: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        frame: Any = Undefined,
        offset: Any = Undefined,
        orient: Any = Undefined,
        reserve: Any = Undefined,
        style: Any = Undefined,
        subtitle: Any = Undefined,
        subtitleColor: Any = Undefined,
        subtitleFont: Any = Undefined,
        subtitleFontSize: Any = Undefined,
        subtitleFontStyle: Any = Undefined,
        subtitleFontWeight: Any = Undefined,
        subtitlePadding: Any = Undefined,
        zindex: Any = Undefined,
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


class TitleFrame(GenomeSpySchema):
    """Generated wrapper for ``TitleFrame``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleFrame", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class TitleOrient(GenomeSpySchema):
    """Generated wrapper for ``TitleOrient``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TitleOrient", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class Tooltip(GenomeSpySchema):
    """Generated wrapper for ``Tooltip``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Tooltip", {})

    def __init__(
        self, handler: Any = Undefined, params: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(handler=handler, params=params)
        if kwds:
            self._kwds.update(kwds)


class TransformParams(GenomeSpySchema):
    """Generated wrapper for ``TransformParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TransformParams", {})

    def __init__(
        self,
        asChrom: Any = Undefined,
        asEnd: Any = Undefined,
        asKey: Any = Undefined,
        asMidpoint: Any = Undefined,
        asStart: Any = Undefined,
        asValue: Any = Undefined,
        baseField: Any = Undefined,
        cardinality: Any = Undefined,
        channel: Any = Undefined,
        chrom: Any = Undefined,
        columnPadding: Any = Undefined,
        columnRegex: Any = Undefined,
        columns: Any = Undefined,
        description: Any = Undefined,
        direction: Any = Undefined,
        ellipsis: Any = Undefined,
        empty: Any = Undefined,
        end: Any = Undefined,
        exons: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        fields: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        groupby: Any = Undefined,
        index: Any = Undefined,
        labelOffset: Any = Undefined,
        labelWidth: Any = Undefined,
        lane: Any = Undefined,
        limit: Any = Undefined,
        offset: Any = Undefined,
        ops: Any = Undefined,
        padding: Any = Undefined,
        param: Any = Undefined,
        pos: Any = Undefined,
        pos2: Any = Undefined,
        preference: Any = Undefined,
        preferredOrder: Any = Undefined,
        regex: Any = Undefined,
        rowPadding: Any = Undefined,
        score: Any = Undefined,
        separator: Any = Undefined,
        size: Any = Undefined,
        skipInvalidInput: Any = Undefined,
        skipRegex: Any = Undefined,
        sort: Any = Undefined,
        spacing: Any = Undefined,
        start: Any = Undefined,
        symbolOffset: Any = Undefined,
        symbolSize: Any = Undefined,
        symbolStrokeWidth: Any = Undefined,
        type: Any = Undefined,
        weight: Any = Undefined,
        width: Any = Undefined,
        xOffset: Any = Undefined,
        yExtent: Any = Undefined,
        yOffset: Any = Undefined,
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


class TruncateTextParams(GenomeSpySchema):
    """Generated wrapper for ``TruncateTextParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TruncateTextParams", {})

    def __init__(
        self,
        description: Any = Undefined,
        ellipsis: Any = Undefined,
        field: Any = Undefined,
        font: Any = Undefined,
        fontSize: Any = Undefined,
        fontStyle: Any = Undefined,
        fontWeight: Any = Undefined,
        limit: Any = Undefined,
        type: Any = Undefined,
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


class Type(GenomeSpySchema):
    """Generated wrapper for ``Type``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Type", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class TypeForShape(GenomeSpySchema):
    """Generated wrapper for ``TypeForShape``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TypeForShape", {})

    def __init__(self, **kwds: Any) -> None:
        super().__init__()
        if kwds:
            self._kwds.update(kwds)


class UnitSpec(GenomeSpySchema):
    """Generated wrapper for ``UnitSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UnitSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        height: Any = Undefined,
        legends: Any = Undefined,
        mark: Any = Undefined,
        name: Any = Undefined,
        opacity: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        view: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class UrlData(GenomeSpySchema):
    """Generated wrapper for ``UrlData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlData", {})

    def __init__(
        self,
        description: Any = Undefined,
        format: Any = Undefined,
        name: Any = Undefined,
        url: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, format=format, name=name, url=url)
        if kwds:
            self._kwds.update(kwds)


class UrlGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeConfig", {})

    def __init__(
        self, name: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(name=name, url=url)
        if kwds:
            self._kwds.update(kwds)


class UrlGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeDefinition", {})

    def __init__(self, url: Any = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)


class UrlImport(GenomeSpySchema):
    """Generated wrapper for ``UrlImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlImport", {})

    def __init__(self, url: Any = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)


class UrlList(GenomeSpySchema):
    """Generated wrapper for ``UrlList``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlList", {})

    def __init__(
        self, type: Any = Undefined, urlsFromFile: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(type=type, urlsFromFile=urlsFromFile)
        if kwds:
            self._kwds.update(kwds)


class UrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``UrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlSourceRef", {})

    def __init__(
        self,
        attach: Any = Undefined,
        expr: Any = Undefined,
        field: Any = Undefined,
        maxValues: Any = Undefined,
        onLoadError: Any = Undefined,
        template: Any = Undefined,
        type: Any = Undefined,
        urlsFromFile: Any = Undefined,
        values: Any = Undefined,
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


class UrlTemplate(GenomeSpySchema):
    """Generated wrapper for ``UrlTemplate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlTemplate", {})

    def __init__(
        self,
        attach: Any = Undefined,
        field: Any = Undefined,
        maxValues: Any = Undefined,
        onLoadError: Any = Undefined,
        template: Any = Undefined,
        values: Any = Undefined,
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


class VConcatSpec(GenomeSpySchema):
    """Generated wrapper for ``VConcatSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VConcatSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        height: Any = Undefined,
        legends: Any = Undefined,
        name: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        separator: Any = Undefined,
        spacing: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        vconcat: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class ValueDefNumber(GenomeSpySchema):
    """Generated wrapper for ``ValueDef<number>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ValueDef<number>", {})

    def __init__(
        self,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)


class ValueDefString(GenomeSpySchema):
    """Generated wrapper for ``ValueDef<string>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ValueDef<string>", {})

    def __init__(
        self,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(description=description, title=title, value=value)
        if kwds:
            self._kwds.update(kwds)


class ValueDefWithConditionStringNullType(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<(string|null),Type>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<(string|null),Type>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class ValueDefWithConditionStringNullTypeForShape(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<(string|null),TypeForShape>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<(string|null),TypeForShape>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class ValueDefWithConditionNumberType(GenomeSpySchema):
    """Generated wrapper for ``ValueDefWithCondition<number,Type>``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "ValueDefWithCondition<number,Type>", {}
    )

    def __init__(
        self,
        condition: Any = Undefined,
        description: Any = Undefined,
        title: Any = Undefined,
        value: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            condition=condition, description=description, title=title, value=value
        )
        if kwds:
            self._kwds.update(kwds)


class VariableParameter(GenomeSpySchema):
    """Generated wrapper for ``VariableParameter``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VariableParameter", {})

    def __init__(
        self,
        bind: Any = Undefined,
        description: Any = Undefined,
        expr: Any = Undefined,
        name: Any = Undefined,
        persist: Any = Undefined,
        push: Any = Undefined,
        value: Any = Undefined,
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


class VcfData(GenomeSpySchema):
    """Generated wrapper for ``VcfData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("VcfData", {})

    def __init__(
        self,
        addChrPrefix: Any = Undefined,
        channel: Any = Undefined,
        debounce: Any = Undefined,
        debounceDomainChange: Any = Undefined,
        debounceMode: Any = Undefined,
        indexUrl: Any = Undefined,
        type: Any = Undefined,
        url: Any = Undefined,
        windowSize: Any = Undefined,
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


class ViewBackground(GenomeSpySchema):
    """Generated wrapper for ``ViewBackground``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewBackground", {})

    def __init__(
        self,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        strokeZindex: Any = Undefined,
        style: Any = Undefined,
        zindex: Any = Undefined,
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


class ViewConfig(GenomeSpySchema):
    """Generated wrapper for ``ViewConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewConfig", {})

    def __init__(
        self,
        continuousHeight: Any = Undefined,
        continuousWidth: Any = Undefined,
        discreteHeight: Any = Undefined,
        discreteWidth: Any = Undefined,
        fill: Any = Undefined,
        fillOpacity: Any = Undefined,
        shadowBlur: Any = Undefined,
        shadowColor: Any = Undefined,
        shadowOffsetX: Any = Undefined,
        shadowOffsetY: Any = Undefined,
        shadowOpacity: Any = Undefined,
        step: Any = Undefined,
        stroke: Any = Undefined,
        strokeOpacity: Any = Undefined,
        strokeWidth: Any = Undefined,
        strokeZindex: Any = Undefined,
        zindex: Any = Undefined,
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


class ViewOpacityDef(GenomeSpySchema):
    """Generated wrapper for ``ViewOpacityDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewOpacityDef", {})

    def __init__(
        self,
        channel: Any = Undefined,
        expr: Any = Undefined,
        unitsPerPixel: Any = Undefined,
        values: Any = Undefined,
        **kwds: Any,
    ) -> None:
        super().__init__(
            channel=channel, expr=expr, unitsPerPixel=unitsPerPixel, values=values
        )
        if kwds:
            self._kwds.update(kwds)


class ViewSpec(GenomeSpySchema):
    """Generated wrapper for ``ViewSpec``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ViewSpec", {})

    def __init__(
        self,
        axes: Any = Undefined,
        baseUrl: Any = Undefined,
        columns: Any = Undefined,
        concat: Any = Undefined,
        config: Any = Undefined,
        cursor: Any = Undefined,
        data: Any = Undefined,
        description: Any = Undefined,
        domainInert: Any = Undefined,
        encoding: Any = Undefined,
        hconcat: Any = Undefined,
        height: Any = Undefined,
        layer: Any = Undefined,
        legends: Any = Undefined,
        mark: Any = Undefined,
        multiscale: Any = Undefined,
        name: Any = Undefined,
        opacity: Any = Undefined,
        padding: Any = Undefined,
        params: Any = Undefined,
        resolve: Any = Undefined,
        scales: Any = Undefined,
        separator: Any = Undefined,
        spacing: Any = Undefined,
        stops: Any = Undefined,
        templates: Any = Undefined,
        title: Any = Undefined,
        transform: Any = Undefined,
        vconcat: Any = Undefined,
        view: Any = Undefined,
        viewportHeight: Any = Undefined,
        viewportWidth: Any = Undefined,
        visible: Any = Undefined,
        width: Any = Undefined,
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


class ZoomParams(GenomeSpySchema):
    """Generated wrapper for ``ZoomParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ZoomParams", {})

    def __init__(self, extent: Any = Undefined, **kwds: Any) -> None:
        super().__init__(extent=extent)
        if kwds:
            self._kwds.update(kwds)


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
