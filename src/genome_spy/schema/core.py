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

    def with_description(self, value: Any) -> AggregateParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(self, value: Any) -> AggregateParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_groupby(self, value: Any) -> AggregateParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_ops(self, value: Any) -> AggregateParams:
        """Return a copy with ``ops`` updated."""
        return self._with_property("ops", value)

    def with_type(self, value: Any) -> AggregateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_domain(self, value: Any) -> Axis:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Any) -> Axis:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: Any) -> Axis:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Any) -> Axis:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: Any) -> Axis:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: Any) -> Axis:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: Any) -> Axis:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: Any) -> Axis:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Any) -> Axis:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: Any) -> Axis:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Any) -> Axis:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: Any) -> Axis:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: Any) -> Axis:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: Any) -> Axis:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``Align`` labelAlign."""
        return self._with_property("labelAlign", value, **kwargs)

    def with_labelAngle(self, value: Any) -> Axis:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``Baseline`` labelBaseline."""
        return self._with_property("labelBaseline", value, **kwargs)

    def with_labelColor(self, value: Any) -> Axis:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: Any) -> Axis:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: Any) -> Axis:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``FontStyle`` labelFontStyle."""
        return self._with_property("labelFontStyle", value, **kwargs)

    def with_labelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``FontWeight`` labelFontWeight."""
        return self._with_property("labelFontWeight", value, **kwargs)

    def with_labelLimit(self, value: Any) -> Axis:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: Any) -> Axis:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: Any) -> Axis:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: Any) -> Axis:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: Any) -> Axis:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: Any) -> Axis:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: AxisOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``AxisOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_placement(
        self,
        value: AxisPlacement | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``AxisPlacement`` placement."""
        return self._with_property("placement", value, **kwargs)

    def with_style(self, value: Any) -> Axis:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Any) -> Axis:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: Any) -> Axis:
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

    def with_tickDash(self, value: Any) -> Axis:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: Any) -> Axis:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: Any) -> Axis:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: Any) -> Axis:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: Any) -> Axis:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: Any) -> Axis:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: Any) -> Axis:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: Any) -> Axis:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Any) -> Axis:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: Any) -> Axis:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: Any) -> Axis:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``FontStyle`` titleFontStyle."""
        return self._with_property("titleFontStyle", value, **kwargs)

    def with_titleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Axis:
        """Return a copy with a ``FontWeight`` titleFontWeight."""
        return self._with_property("titleFontWeight", value, **kwargs)

    def with_titleOpacity(self, value: Any) -> Axis:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: Any) -> Axis:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Any) -> Axis:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: Any) -> Axis:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_chromGrid(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``Align`` chromLabelAlign."""
        return self._with_property("chromLabelAlign", value, **kwargs)

    def with_chromLabelColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontStyle`` chromLabelFontStyle."""
        return self._with_property("chromLabelFontStyle", value, **kwargs)

    def with_chromLabelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontWeight`` chromLabelFontWeight."""
        return self._with_property("chromLabelFontWeight", value, **kwargs)

    def with_chromLabelPadding(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: Any) -> AxisConfig:
        """Return a copy with ``chromTicks`` updated."""
        return self._with_property("chromTicks", value)

    def with_domain(self, value: Any) -> AxisConfig:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Any) -> AxisConfig:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Any) -> AxisConfig:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: Any) -> AxisConfig:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: Any) -> AxisConfig:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: Any) -> AxisConfig:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: Any) -> AxisConfig:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: Any) -> AxisConfig:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``Align`` labelAlign."""
        return self._with_property("labelAlign", value, **kwargs)

    def with_labelAngle(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``Baseline`` labelBaseline."""
        return self._with_property("labelBaseline", value, **kwargs)

    def with_labelColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontStyle`` labelFontStyle."""
        return self._with_property("labelFontStyle", value, **kwargs)

    def with_labelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontWeight`` labelFontWeight."""
        return self._with_property("labelFontWeight", value, **kwargs)

    def with_labelLimit(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: Any) -> AxisConfig:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: Any) -> AxisConfig:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: Any) -> AxisConfig:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: Any) -> AxisConfig:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: Any) -> AxisConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: AxisOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``AxisOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_placement(
        self,
        value: AxisPlacement | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``AxisPlacement`` placement."""
        return self._with_property("placement", value, **kwargs)

    def with_style(self, value: Any) -> AxisConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: Any) -> AxisConfig:
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

    def with_tickDash(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: Any) -> AxisConfig:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: Any) -> AxisConfig:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: Any) -> AxisConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: Any) -> AxisConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Any) -> AxisConfig:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: Any) -> AxisConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: Any) -> AxisConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontStyle`` titleFontStyle."""
        return self._with_property("titleFontStyle", value, **kwargs)

    def with_titleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisConfig:
        """Return a copy with a ``FontWeight`` titleFontWeight."""
        return self._with_property("titleFontWeight", value, **kwargs)

    def with_titleOpacity(self, value: Any) -> AxisConfig:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: Any) -> AxisConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Any) -> AxisConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: Any) -> AxisConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


class AxisGenomeData(GenomeSpySchema):
    """Generated wrapper for ``AxisGenomeData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("AxisGenomeData", {})

    def __init__(
        self, channel: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(channel=channel, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisGenomeData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_type(self, value: Any) -> AxisGenomeData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_axis(
        self,
        value: Axis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisTicksData:
        """Return a copy with a ``Axis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> AxisTicksData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_type(self, value: Any) -> AxisTicksData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BamData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> BamData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BamData:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_type(self, value: Any) -> BamData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: SingleUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BamData:
        """Return a copy with a ``SingleUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(self, value: Any) -> BamData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


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

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BedDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> BedDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_columns(self, value: Any) -> BedpeDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BedpeDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> BedpeDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> BigBedData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_type(self, value: Any) -> BigBedData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigBedData:
        """Return a copy with a ``ExprRef`` windowSize."""
        return self._with_property("windowSize", value, **kwargs)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigWigData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> BigWigData:
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

    def with_type(self, value: Any) -> BigWigData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> BigWigData:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)


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

    def with_debounce(self, value: Any) -> BindCheckbox:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: Any) -> BindCheckbox:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Any) -> BindCheckbox:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_name(self, value: Any) -> BindCheckbox:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


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

    def with_autocomplete(self, value: Any) -> BindInput:
        """Return a copy with ``autocomplete`` updated."""
        return self._with_property("autocomplete", value)

    def with_debounce(self, value: Any) -> BindInput:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: Any) -> BindInput:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Any) -> BindInput:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_name(self, value: Any) -> BindInput:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_placeholder(self, value: Any) -> BindInput:
        """Return a copy with ``placeholder`` updated."""
        return self._with_property("placeholder", value)


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

    def with_debounce(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_labels(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_name(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_options(self, value: Any) -> BindRadioSelect:
        """Return a copy with ``options`` updated."""
        return self._with_property("options", value)


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

    def with_debounce(self, value: Any) -> BindRange:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: Any) -> BindRange:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Any) -> BindRange:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_max(self, value: Any) -> BindRange:
        """Return a copy with ``max`` updated."""
        return self._with_property("max", value)

    def with_min(self, value: Any) -> BindRange:
        """Return a copy with ``min`` updated."""
        return self._with_property("min", value)

    def with_name(self, value: Any) -> BindRange:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_step(self, value: Any) -> BindRange:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


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

    def with_autocomplete(self, value: Any) -> Binding:
        """Return a copy with ``autocomplete`` updated."""
        return self._with_property("autocomplete", value)

    def with_debounce(self, value: Any) -> Binding:
        """Return a copy with ``debounce`` updated."""
        return self._with_property("debounce", value)

    def with_description(self, value: Any) -> Binding:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_input(self, value: Any) -> Binding:
        """Return a copy with ``input`` updated."""
        return self._with_property("input", value)

    def with_labels(self, value: Any) -> Binding:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_max(self, value: Any) -> Binding:
        """Return a copy with ``max`` updated."""
        return self._with_property("max", value)

    def with_min(self, value: Any) -> Binding:
        """Return a copy with ``min`` updated."""
        return self._with_property("min", value)

    def with_name(self, value: Any) -> Binding:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_options(self, value: Any) -> Binding:
        """Return a copy with ``options`` updated."""
        return self._with_property("options", value)

    def with_placeholder(self, value: Any) -> Binding:
        """Return a copy with ``placeholder`` updated."""
        return self._with_property("placeholder", value)

    def with_step(self, value: Any) -> Binding:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


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

    def with_clip(self, value: Any) -> BrushConfig:
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

    def with_fill(self, value: Any) -> BrushConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: Any) -> BrushConfig:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_measure(self, value: Any) -> BrushConfig:
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

    def with_stroke(self, value: Any) -> BrushConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: Any) -> BrushConfig:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: Any) -> BrushConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_zindex(self, value: Any) -> BrushConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> ChromPosDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``FieldName`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_description(self, value: Any) -> ChromPosDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ChromPosDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_offset(self, value: Any) -> ChromPosDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``FieldName`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ChromPosDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ChromPosDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(self, value: Any) -> ChromPosDef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


class ChromosomalLocus(GenomeSpySchema):
    """Generated wrapper for ``ChromosomalLocus``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ChromosomalLocus", {})

    def __init__(
        self, chrom: Any = Undefined, pos: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)

    def with_chrom(self, value: Any) -> ChromosomalLocus:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_pos(self, value: Any) -> ChromosomalLocus:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)


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

    def with_description(self, value: Any) -> CollectParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_groupby(self, value: Any) -> CollectParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_sort(
        self,
        value: CompareParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CollectParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_type(self, value: Any) -> CollectParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_band(self, value: Any) -> ColorDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> ColorDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ColorDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> ColorDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> ColorDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ColorDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ColorDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_count(self, value: Any) -> ColorSchemeConfig:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_extent(self, value: Any) -> ColorSchemeConfig:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_name(self, value: Any) -> ColorSchemeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


class CompareParams(GenomeSpySchema):
    """Generated wrapper for ``CompareParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("CompareParams", {})

    def __init__(
        self, field: Any = Undefined, order: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(field=field, order=order)
        if kwds:
            self._kwds.update(kwds)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CompareParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_order(
        self,
        value: SortOrder | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CompareParams:
        """Return a copy with a ``SortOrder`` order."""
        return self._with_property("order", value, **kwargs)


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

    def with_axes(self, value: Any) -> ConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> ConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: Any) -> ConcatSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(self, value: Any) -> ConcatSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> ConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: Any) -> ConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: Any) -> ConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> ConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> ConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> ConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: Any) -> ConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: Any) -> ConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> ConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> ConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_band(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefType:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalMarkPropExprDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefType:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropExprDefTypeForShape:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalMarkPropFieldDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefType:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: TypeForShape | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalMarkPropFieldDefTypeForShape:
        """Return a copy with a ``TypeForShape`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalScaleDatumDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalScaleDatumDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalScaleDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalScaleDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalScaleDatumDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalValueDefNumberExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: Any) -> ConditionalValueDefNumberExprRef:
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

    def with_description(self, value: Any) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalValueDefStringNullExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: Any) -> ConditionalValueDefStringNullExprRef:
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

    def with_band(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefType:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(
        self, value: Any
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: Any) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_param(self, value: Any) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropExprDefTypeForShape:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefType:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_field(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_param(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: Any
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: TypeForShape | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterMarkPropFieldDefTypeForShape:
        """Return a copy with a ``TypeForShape`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_empty(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ConditionalParameterScaleDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ConditionalParameterScaleDatumDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalParameterValueDefNumberExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: Any) -> ConditionalParameterValueDefNumberExprRef:
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

    def with_description(
        self, value: Any
    ) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_param(self, value: Any) -> ConditionalParameterValueDefStringNullExprRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_title(self, value: Any) -> ConditionalParameterValueDefStringNullExprRef:
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


class Contig(GenomeSpySchema):
    """Generated wrapper for ``Contig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Contig", {})

    def __init__(
        self, name: Any = Undefined, size: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(name=name, size=size)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: Any) -> Contig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_size(self, value: Any) -> Contig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)


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

    def with_assembly(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``assembly`` updated."""
        return self._with_property("assembly", value)

    def with_axes(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_background(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``background`` updated."""
        return self._with_property("background", value)

    def with_baseUrl(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_datasets(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``datasets`` updated."""
        return self._with_property("datasets", value)

    def with_description(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_genome(
        self,
        value: GenomeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``GenomeConfig`` genome."""
        return self._with_property("genome", value, **kwargs)

    def with_genomes(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``genomes`` updated."""
        return self._with_property("genomes", value)

    def with_hconcat(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``MarkType`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_multiscale(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: ViewOpacityDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``ViewOpacityDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_stops(
        self,
        value: MultiscaleStopsDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``MultiscaleStopsDef`` stops."""
        return self._with_property("stops", value, **kwargs)

    def with_templates(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_theme(
        self,
        value: BuiltInThemeName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``BuiltInThemeName`` theme."""
        return self._with_property("theme", value, **kwargs)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_view(
        self,
        value: ViewBackground | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> CoreRootSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoreRootSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_asChrom(self, value: Any) -> CoverageParams:
        """Return a copy with ``asChrom`` updated."""
        return self._with_property("asChrom", value)

    def with_asEnd(self, value: Any) -> CoverageParams:
        """Return a copy with ``asEnd`` updated."""
        return self._with_property("asEnd", value)

    def with_asStart(self, value: Any) -> CoverageParams:
        """Return a copy with ``asStart`` updated."""
        return self._with_property("asStart", value)

    def with_chrom(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoverageParams:
        """Return a copy with a ``Field`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_description(self, value: Any) -> CoverageParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_end(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoverageParams:
        """Return a copy with a ``Field`` end."""
        return self._with_property("end", value, **kwargs)

    def with_start(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoverageParams:
        """Return a copy with a ``Field`` start."""
        return self._with_property("start", value, **kwargs)

    def with_type(self, value: Any) -> CoverageParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_weight(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CoverageParams:
        """Return a copy with a ``Field`` weight."""
        return self._with_property("weight", value, **kwargs)


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

    def with_columns(self, value: Any) -> CsvDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> CsvDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> CsvDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> Data:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: Any) -> Data:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_lazy(
        self,
        value: LazyDataParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``LazyDataParams`` lazy."""
        return self._with_property("lazy", value, **kwargs)

    def with_name(self, value: Any) -> Data:
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
        value: UrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``UrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_values(
        self,
        value: InlineDataset | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Data:
        """Return a copy with a ``InlineDataset`` values."""
        return self._with_property("values", value, **kwargs)


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

    def with_columns(self, value: Any) -> DataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_delimiter(self, value: Any) -> DataFormat:
        """Return a copy with ``delimiter`` updated."""
        return self._with_property("delimiter", value)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_property(self, value: Any) -> DataFormat:
        """Return a copy with ``property`` updated."""
        return self._with_property("property", value)

    def with_type(self, value: Any) -> DataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> DataSource:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: Any) -> DataSource:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_lazy(
        self,
        value: LazyDataParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``LazyDataParams`` lazy."""
        return self._with_property("lazy", value, **kwargs)

    def with_name(self, value: Any) -> DataSource:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(
        self,
        value: UrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``UrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_values(
        self,
        value: InlineDataset | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DataSource:
        """Return a copy with a ``InlineDataset`` values."""
        return self._with_property("values", value, **kwargs)


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

    def with_expr(self, value: Any) -> DomainValue:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


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

    def with_columns(self, value: Any) -> DsvDataFormat:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_delimiter(self, value: Any) -> DsvDataFormat:
        """Return a copy with ``delimiter`` updated."""
        return self._with_property("delimiter", value)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DsvDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> DsvDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> DynamicCallbackData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_dynamicCallbackSource(self, value: Any) -> DynamicCallbackData:
        """Return a copy with ``dynamicCallbackSource`` updated."""
        return self._with_property("dynamicCallbackSource", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DynamicCallbackData:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_name(self, value: Any) -> DynamicCallbackData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> DynamicOpacity:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_unitsPerPixel(self, value: Any) -> DynamicOpacity:
        """Return a copy with ``unitsPerPixel`` updated."""
        return self._with_property("unitsPerPixel", value)

    def with_values(self, value: Any) -> DynamicOpacity:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_angle(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_color(
        self,
        value: ColorDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``ColorDef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_dx(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` dx."""
        return self._with_property("dx", value, **kwargs)

    def with_dy(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` dy."""
        return self._with_property("dy", value, **kwargs)

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
        value: ColorDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``ColorDef`` fill."""
        return self._with_property("fill", value, **kwargs)

    def with_fillOpacity(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` fillOpacity."""
        return self._with_property("fillOpacity", value, **kwargs)

    def with_key(
        self,
        value: KeyDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``KeyDef`` key."""
        return self._with_property("key", value, **kwargs)

    def with_opacity(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

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
        value: SearchDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``SearchDef`` search."""
        return self._with_property("search", value, **kwargs)

    def with_semanticScore(self, value: Any) -> Encoding:
        """Return a copy with ``semanticScore`` updated."""
        return self._with_property("semanticScore", value)

    def with_shape(
        self,
        value: ShapeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``ShapeDef`` shape."""
        return self._with_property("shape", value, **kwargs)

    def with_size(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` size."""
        return self._with_property("size", value, **kwargs)

    def with_stroke(
        self,
        value: ColorDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``ColorDef`` stroke."""
        return self._with_property("stroke", value, **kwargs)

    def with_strokeOpacity(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` strokeOpacity."""
        return self._with_property("strokeOpacity", value, **kwargs)

    def with_strokeWidth(
        self,
        value: NumericMarkPropDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``NumericMarkPropDef`` strokeWidth."""
        return self._with_property("strokeWidth", value, **kwargs)

    def with_text(
        self,
        value: TextDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``TextDef`` text."""
        return self._with_property("text", value, **kwargs)

    def with_uniqueId(
        self,
        value: FieldDefWithoutScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``FieldDefWithoutScale`` uniqueId."""
        return self._with_property("uniqueId", value, **kwargs)

    def with_x(self, value: Any) -> Encoding:
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
        value: PositionDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``PositionDef`` y."""
        return self._with_property("y", value, **kwargs)

    def with_y2(
        self,
        value: Position2Def | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Encoding:
        """Return a copy with a ``Position2Def`` y2."""
        return self._with_property("y2", value, **kwargs)


class EventConfig(GenomeSpySchema):
    """Generated wrapper for ``EventConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("EventConfig", {})

    def __init__(
        self, filter: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(filter=filter, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_filter(self, value: Any) -> EventConfig:
        """Return a copy with ``filter`` updated."""
        return self._with_property("filter", value)

    def with_type(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> EventConfig:
        """Return a copy with a ``DomEventType`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> ExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> ExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: Any) -> ExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_title(self, value: Any) -> ExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ExprDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> ExprFilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: Any) -> ExprFilterParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_type(self, value: Any) -> ExprFilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


class ExprRef(GenomeSpySchema):
    """Generated wrapper for ``ExprRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ExprRef", {})

    def __init__(self, expr: Any = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: Any) -> ExprRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


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

    def with_description(self, value: Any) -> FieldDefWithoutScale:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Any) -> FieldDefWithoutScale:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: Any) -> FieldDefWithoutScale:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


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

    def with_condition(
        self,
        value: ConditionalValueDefStringNullExprRef
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``ConditionalValueDefStringNullExprRef`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeStringNull:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_condition(
        self,
        value: ConditionalValueDefNumberExprRef
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``ConditionalValueDefNumberExprRef`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeNumber:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_condition(
        self,
        value: ConditionalValueDefStringNullExprRef
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``ConditionalValueDefStringNullExprRef`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: TypeForShape | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionMarkPropFieldDefTypeForShapeStringNull:
        """Return a copy with a ``TypeForShape`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalValueDefStringNullExprRef
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``ConditionalValueDefStringNullExprRef`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefStringNull:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_band(self, value: Any) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalValueDefNumberExprRef
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``ConditionalValueDefNumberExprRef`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(
        self, value: Any
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FieldOrDatumDefWithConditionScaleDatumDefNumber:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> FilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> FilterParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_expr(self, value: Any) -> FilterParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_fields(self, value: Any) -> FilterParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_param(self, value: Any) -> FilterParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_type(self, value: Any) -> FilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_asMidpoint(self, value: Any) -> FilterScoredLabelsParams:
        """Return a copy with ``asMidpoint`` updated."""
        return self._with_property("asMidpoint", value)

    def with_channel(self, value: Any) -> FilterScoredLabelsParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_description(self, value: Any) -> FilterScoredLabelsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_lane(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FilterScoredLabelsParams:
        """Return a copy with a ``Field`` lane."""
        return self._with_property("lane", value, **kwargs)

    def with_padding(self, value: Any) -> FilterScoredLabelsParams:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_pos(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FilterScoredLabelsParams:
        """Return a copy with a ``Field`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_pos2(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FilterScoredLabelsParams:
        """Return a copy with a ``Field`` pos2."""
        return self._with_property("pos2", value, **kwargs)

    def with_score(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FilterScoredLabelsParams:
        """Return a copy with a ``Field`` score."""
        return self._with_property("score", value, **kwargs)

    def with_type(self, value: Any) -> FilterScoredLabelsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_width(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FilterScoredLabelsParams:
        """Return a copy with a ``Field`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_description(self, value: Any) -> FlattenCompressedExonsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_exons(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FlattenCompressedExonsParams:
        """Return a copy with a ``Field`` exons."""
        return self._with_property("exons", value, **kwargs)

    def with_start(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FlattenCompressedExonsParams:
        """Return a copy with a ``Field`` start."""
        return self._with_property("start", value, **kwargs)

    def with_type(self, value: Any) -> FlattenCompressedExonsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> FlattenDelimitedParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FlattenDelimitedParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_separator(self, value: Any) -> FlattenDelimitedParams:
        """Return a copy with ``separator`` updated."""
        return self._with_property("separator", value)

    def with_type(self, value: Any) -> FlattenDelimitedParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> FlattenParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FlattenParams:
        """Return a copy with a ``Field`` fields."""
        return self._with_property("fields", value, **kwargs)

    def with_index(self, value: Any) -> FlattenParams:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_type(self, value: Any) -> FlattenParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> FlattenSequenceParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> FlattenSequenceParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_type(self, value: Any) -> FlattenSequenceParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> FormulaParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: Any) -> FormulaParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_type(self, value: Any) -> FormulaParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> Generator:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: Any) -> Generator:
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

    def with_chromGrid(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``Align`` chromLabelAlign."""
        return self._with_property("chromLabelAlign", value, **kwargs)

    def with_chromLabelColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontStyle`` chromLabelFontStyle."""
        return self._with_property("chromLabelFontStyle", value, **kwargs)

    def with_chromLabelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontWeight`` chromLabelFontWeight."""
        return self._with_property("chromLabelFontWeight", value, **kwargs)

    def with_chromLabelPadding(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: Any) -> GenomeAxis:
        """Return a copy with ``chromTicks`` updated."""
        return self._with_property("chromTicks", value)

    def with_domain(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: Any) -> GenomeAxis:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_format(self, value: Any) -> GenomeAxis:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_grid(self, value: Any) -> GenomeAxis:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: Any) -> GenomeAxis:
        """Return a copy with ``gridWidth`` updated."""
        return self._with_property("gridWidth", value)

    def with_labelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``Align`` labelAlign."""
        return self._with_property("labelAlign", value, **kwargs)

    def with_labelAngle(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``Baseline`` labelBaseline."""
        return self._with_property("labelBaseline", value, **kwargs)

    def with_labelColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontStyle`` labelFontStyle."""
        return self._with_property("labelFontStyle", value, **kwargs)

    def with_labelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontWeight`` labelFontWeight."""
        return self._with_property("labelFontWeight", value, **kwargs)

    def with_labelLimit(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelPadding(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: Any) -> GenomeAxis:
        """Return a copy with ``labels`` updated."""
        return self._with_property("labels", value)

    def with_maxExtent(self, value: Any) -> GenomeAxis:
        """Return a copy with ``maxExtent`` updated."""
        return self._with_property("maxExtent", value)

    def with_minExtent(self, value: Any) -> GenomeAxis:
        """Return a copy with ``minExtent`` updated."""
        return self._with_property("minExtent", value)

    def with_offset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: AxisOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``AxisOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_placement(
        self,
        value: AxisPlacement | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``AxisPlacement`` placement."""
        return self._with_property("placement", value, **kwargs)

    def with_style(self, value: Any) -> GenomeAxis:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tickCap(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: Any) -> GenomeAxis:
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

    def with_tickDash(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: Any) -> GenomeAxis:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: Any) -> GenomeAxis:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: Any) -> GenomeAxis:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontStyle`` titleFontStyle."""
        return self._with_property("titleFontStyle", value, **kwargs)

    def with_titleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeAxis:
        """Return a copy with a ``FontWeight`` titleFontWeight."""
        return self._with_property("titleFontWeight", value, **kwargs)

    def with_titleOpacity(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titlePadding(self, value: Any) -> GenomeAxis:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Any) -> GenomeAxis:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_zindex(self, value: Any) -> GenomeAxis:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_contigs(self, value: Any) -> GenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_name(self, value: Any) -> GenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(self, value: Any) -> GenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


class GenomeConfigBase(GenomeSpySchema):
    """Generated wrapper for ``GenomeConfigBase``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeConfigBase", {})

    def __init__(self, name: Any = Undefined, **kwds: Any) -> None:
        super().__init__(name=name)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: Any) -> GenomeConfigBase:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


class GenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``GenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("GenomeDefinition", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(self, value: Any) -> GenomeDefinition:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: Any) -> GenomeDefinition:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


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

    def with_axis(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_axisBottom(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisBottom."""
        return self._with_property("axisBottom", value, **kwargs)

    def with_axisIndex(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisIndex."""
        return self._with_property("axisIndex", value, **kwargs)

    def with_axisLeft(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisLeft."""
        return self._with_property("axisLeft", value, **kwargs)

    def with_axisLocus(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisLocus."""
        return self._with_property("axisLocus", value, **kwargs)

    def with_axisNominal(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisNominal."""
        return self._with_property("axisNominal", value, **kwargs)

    def with_axisOrdinal(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisOrdinal."""
        return self._with_property("axisOrdinal", value, **kwargs)

    def with_axisQuantitative(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisQuantitative."""
        return self._with_property("axisQuantitative", value, **kwargs)

    def with_axisRight(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisRight."""
        return self._with_property("axisRight", value, **kwargs)

    def with_axisTop(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisTop."""
        return self._with_property("axisTop", value, **kwargs)

    def with_axisX(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisX."""
        return self._with_property("axisX", value, **kwargs)

    def with_axisY(
        self,
        value: AxisConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``AxisConfig`` axisY."""
        return self._with_property("axisY", value, **kwargs)

    def with_legend(
        self,
        value: LegendConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LegendConfig`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_legendTrack(
        self,
        value: LegendConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LegendConfig`` legendTrack."""
        return self._with_property("legendTrack", value, **kwargs)

    def with_link(
        self,
        value: LinkConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``LinkConfig`` link."""
        return self._with_property("link", value, **kwargs)

    def with_mark(
        self,
        value: MarkConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``MarkConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_point(
        self,
        value: PointConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``PointConfig`` point."""
        return self._with_property("point", value, **kwargs)

    def with_range(
        self,
        value: RangeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RangeConfig`` range."""
        return self._with_property("range", value, **kwargs)

    def with_rect(
        self,
        value: RectConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RectConfig`` rect."""
        return self._with_property("rect", value, **kwargs)

    def with_rule(
        self,
        value: RuleConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``RuleConfig`` rule."""
        return self._with_property("rule", value, **kwargs)

    def with_scale(
        self,
        value: ScaleConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``ScaleConfig`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_style(self, value: Any) -> GenomeSpyConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(
        self,
        value: TextConfig | dict[str, Any] | None | Any = Undefined,
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
        value: TitleConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``TitleConfig`` title."""
        return self._with_property("title", value, **kwargs)

    def with_view(
        self,
        value: ViewConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a copy with a ``ViewConfig`` view."""
        return self._with_property("view", value, **kwargs)


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

    def with_addChrPrefix(self, value: Any) -> Gff3Data:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Gff3Data:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> Gff3Data:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Gff3Data:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_type(self, value: Any) -> Gff3Data:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Gff3Data:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(self, value: Any) -> Gff3Data:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


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

    def with_axes(self, value: Any) -> HConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> HConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> HConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> HConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_hconcat(self, value: Any) -> HConcatSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: Any) -> HConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: Any) -> HConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> HConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> HConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> HConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: Any) -> HConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: Any) -> HConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> HConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> HConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> HConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


class HandledTooltip(GenomeSpySchema):
    """Generated wrapper for ``HandledTooltip``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("HandledTooltip", {})

    def __init__(
        self, handler: Any = Undefined, params: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(handler=handler, params=params)
        if kwds:
            self._kwds.update(kwds)

    def with_handler(self, value: Any) -> HandledTooltip:
        """Return a copy with ``handler`` updated."""
        return self._with_property("handler", value)

    def with_params(self, value: Any) -> HandledTooltip:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)


class IdentifierParams(GenomeSpySchema):
    """Generated wrapper for ``IdentifierParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IdentifierParams", {})

    def __init__(
        self, description: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: Any) -> IdentifierParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_type(self, value: Any) -> IdentifierParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ImportSpec:
        """Return a copy with a ``GenomeSpyConfig`` config."""
        return self._with_property("config", value, **kwargs)

    def with_name(self, value: Any) -> ImportSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_params(self, value: Any) -> ImportSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_visible(self, value: Any) -> ImportSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)


class IndexUrlSourceRef(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlSourceRef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlSourceRef", {})

    def __init__(
        self, expr: Any = Undefined, template: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(expr=expr, template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: Any) -> IndexUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_template(self, value: Any) -> IndexUrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


class IndexUrlTemplate(GenomeSpySchema):
    """Generated wrapper for ``IndexUrlTemplate``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("IndexUrlTemplate", {})

    def __init__(self, template: Any = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_template(self, value: Any) -> IndexUrlTemplate:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IndexedFastaData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> IndexedFastaData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IndexedFastaData:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_type(self, value: Any) -> IndexedFastaData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: SingleUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IndexedFastaData:
        """Return a copy with a ``SingleUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(self, value: Any) -> IndexedFastaData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


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

    def with_description(self, value: Any) -> InlineData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> InlineData:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_name(self, value: Any) -> InlineData:
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

    def with_contigs(self, value: Any) -> InlineGenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_name(self, value: Any) -> InlineGenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


class InlineGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``InlineGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineGenomeDefinition", {})

    def __init__(self, contigs: Any = Undefined, **kwds: Any) -> None:
        super().__init__(contigs=contigs)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(self, value: Any) -> InlineGenomeDefinition:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)


class InlineLocusAssembly(GenomeSpySchema):
    """Generated wrapper for ``InlineLocusAssembly``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("InlineLocusAssembly", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(self, value: Any) -> InlineLocusAssembly:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: Any) -> InlineLocusAssembly:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


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

    def with_clear(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``DomEventType`` clear."""
        return self._with_property("clear", value, **kwargs)

    def with_encodings(self, value: Any) -> IntervalSelectionConfig:
        """Return a copy with ``encodings`` updated."""
        return self._with_property("encodings", value)

    def with_extent(
        self,
        value: SelectionExtent | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``SelectionExtent`` extent."""
        return self._with_property("extent", value, **kwargs)

    def with_mark(
        self,
        value: BrushConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``BrushConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_on(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``DomEventType`` on."""
        return self._with_property("on", value, **kwargs)

    def with_type(self, value: Any) -> IntervalSelectionConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_zoom(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> IntervalSelectionConfig:
        """Return a copy with a ``DomEventType`` zoom."""
        return self._with_property("zoom", value, **kwargs)


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

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> JsonDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_property(self, value: Any) -> JsonDataFormat:
        """Return a copy with ``property`` updated."""
        return self._with_property("property", value)

    def with_type(self, value: Any) -> JsonDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_description(self, value: Any) -> KeyDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Any) -> KeyDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: Any) -> KeyDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


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

    def with_axes(self, value: Any) -> LayerSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> LayerSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> LayerSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> LayerSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(self, value: Any) -> LayerSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: Any) -> LayerSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: Any) -> LayerSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: ViewOpacityDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``ViewOpacityDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> LayerSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> LayerSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> LayerSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_templates(self, value: Any) -> LayerSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> LayerSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> LayerSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LayerSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


class LazyData(GenomeSpySchema):
    """Generated wrapper for ``LazyData``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("LazyData", {})

    def __init__(
        self, description: Any = Undefined, lazy: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, lazy=lazy)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: Any) -> LazyData:
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

    def with_addChrPrefix(self, value: Any) -> LazyDataParams:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_axis(
        self,
        value: Axis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``Axis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_columns(self, value: Any) -> LazyDataParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_count(self, value: Any) -> LazyDataParams:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_dataType(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``Type`` dataType."""
        return self._with_property("dataType", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> LazyDataParams:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_format(self, value: Any) -> LazyDataParams:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
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

    def with_sizeMode(self, value: Any) -> LazyDataParams:
        """Return a copy with ``sizeMode`` updated."""
        return self._with_property("sizeMode", value)

    def with_type(self, value: Any) -> LazyDataParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LazyDataParams:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_values(self, value: Any) -> LazyDataParams:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_windowSize(self, value: Any) -> LazyDataParams:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


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

    def with_backgroundFill(self, value: Any) -> Legend:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: Any) -> Legend:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: Any) -> Legend:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: Any) -> Legend:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: Any) -> Legend:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_columns(self, value: Any) -> Legend:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_direction(
        self,
        value: LegendDirection | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Legend:
        """Return a copy with a ``LegendDirection`` direction."""
        return self._with_property("direction", value, **kwargs)

    def with_labelLimit(self, value: Any) -> Legend:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_offset(self, value: Any) -> Legend:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: LegendOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Legend:
        """Return a copy with a ``LegendOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_padding(self, value: Any) -> Legend:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_style(self, value: Any) -> Legend:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_symbolSize(self, value: Any) -> Legend:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolType(self, value: Any) -> Legend:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_title(self, value: Any) -> Legend:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleOrient(
        self,
        value: LegendTitleOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Legend:
        """Return a copy with a ``LegendTitleOrient`` titleOrient."""
        return self._with_property("titleOrient", value, **kwargs)

    def with_values(self, value: Any) -> Legend:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_backgroundFill(self, value: Any) -> LegendConfig:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: Any) -> LegendConfig:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: Any) -> LegendConfig:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: Any) -> LegendConfig:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: Any) -> LegendConfig:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_columnPadding(self, value: Any) -> LegendConfig:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: Any) -> LegendConfig:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_direction(
        self,
        value: LegendDirection | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``LegendDirection`` direction."""
        return self._with_property("direction", value, **kwargs)

    def with_disable(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``ExprRef`` disable."""
        return self._with_property("disable", value, **kwargs)

    def with_labelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``Align`` labelAlign."""
        return self._with_property("labelAlign", value, **kwargs)

    def with_labelBaseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``Baseline`` labelBaseline."""
        return self._with_property("labelBaseline", value, **kwargs)

    def with_labelColor(self, value: Any) -> LegendConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: Any) -> LegendConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: Any) -> LegendConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``FontStyle`` labelFontStyle."""
        return self._with_property("labelFontStyle", value, **kwargs)

    def with_labelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``FontWeight`` labelFontWeight."""
        return self._with_property("labelFontWeight", value, **kwargs)

    def with_labelLimit(self, value: Any) -> LegendConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelOffset(self, value: Any) -> LegendConfig:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_offset(self, value: Any) -> LegendConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: LegendOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``LegendOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_padding(self, value: Any) -> LegendConfig:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_rowPadding(self, value: Any) -> LegendConfig:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_spacing(self, value: Any) -> LegendConfig:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_style(self, value: Any) -> LegendConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_symbolBaseFillColor(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolBaseFillColor`` updated."""
        return self._with_property("symbolBaseFillColor", value)

    def with_symbolBaseStrokeColor(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolBaseStrokeColor`` updated."""
        return self._with_property("symbolBaseStrokeColor", value)

    def with_symbolOffset(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_symbolType(self, value: Any) -> LegendConfig:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_title(self, value: Any) -> LegendConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: Any) -> LegendConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFont(self, value: Any) -> LegendConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: Any) -> LegendConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``FontStyle`` titleFontStyle."""
        return self._with_property("titleFontStyle", value, **kwargs)

    def with_titleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``FontWeight`` titleFontWeight."""
        return self._with_property("titleFontWeight", value, **kwargs)

    def with_titleLimit(self, value: Any) -> LegendConfig:
        """Return a copy with ``titleLimit`` updated."""
        return self._with_property("titleLimit", value)

    def with_titleOrient(
        self,
        value: LegendTitleOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LegendConfig:
        """Return a copy with a ``LegendTitleOrient`` titleOrient."""
        return self._with_property("titleOrient", value, **kwargs)

    def with_titlePadding(self, value: Any) -> LegendConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_values(self, value: Any) -> LegendConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_channel(self, value: Any) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_chrom(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with a ``Field`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_description(self, value: Any) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_offset(self, value: Any) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinearizeGenomicCoordinateParams:
        """Return a copy with a ``Field`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_type(self, value: Any) -> LinearizeGenomicCoordinateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_buildIndex(self, value: Any) -> LinkConfig:
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

    def with_clip(self, value: Any) -> LinkConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> LinkConfig:
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

    def with_minBufferSize(self, value: Any) -> LinkConfig:
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

    def with_style(self, value: Any) -> LinkConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

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

    def with_xOffset(self, value: Any) -> LinkConfig:
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

    def with_yOffset(self, value: Any) -> LinkConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> LinkProps:
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

    def with_clip(self, value: Any) -> LinkProps:
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

    def with_cullByVisibleRange(self, value: Any) -> LinkProps:
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

    def with_minBufferSize(self, value: Any) -> LinkProps:
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

    def with_style(self, value: Any) -> LinkProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> LinkProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> LinkProps:
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

    def with_xOffset(self, value: Any) -> LinkProps:
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

    def with_yOffset(self, value: Any) -> LinkProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> MarkConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> MarkConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> MarkConfig:
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

    def with_minBufferSize(self, value: Any) -> MarkConfig:
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

    def with_style(self, value: Any) -> MarkConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: Any) -> MarkConfig:
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

    def with_yOffset(self, value: Any) -> MarkConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_band(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``ConditionalMarkPropFieldDefTypeForShape`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNullTypeForShape:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_band(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> MarkPropDefStringNull:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefStringNull:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_band(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> MarkPropDefNumber:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropDefNumber:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_band(self, value: Any) -> MarkPropExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> MarkPropExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> MarkPropExprDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: Any) -> MarkPropExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropExprDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropExprDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> MarkPropExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkPropExprDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

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

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_buildIndex(self, value: Any) -> MarkProps:
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

    def with_clip(self, value: Any) -> MarkProps:
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

    def with_cullByVisibleRange(self, value: Any) -> MarkProps:
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

    def with_filled(self, value: Any) -> MarkProps:
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

    def with_font(self, value: Any) -> MarkProps:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_geometricZoomBound(self, value: Any) -> MarkProps:
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

    def with_minBufferSize(self, value: Any) -> MarkProps:
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

    def with_sampleFacetPadding(self, value: Any) -> MarkProps:
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

    def with_strokeDash(self, value: Any) -> MarkProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> MarkProps:
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

    def with_style(self, value: Any) -> MarkProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``Scalar`` text."""
        return self._with_property("text", value, **kwargs)

    def with_thickness(self, value: Any) -> MarkProps:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MarkProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> MarkProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: Any) -> MarkProps:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: Any) -> MarkProps:
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

    def with_xOffset(self, value: Any) -> MarkProps:
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

    def with_yOffset(self, value: Any) -> MarkProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_description(self, value: Any) -> MeasureTextParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MeasureTextParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_font(self, value: Any) -> MeasureTextParams:
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

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MeasureTextParams:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MeasureTextParams:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_type(self, value: Any) -> MeasureTextParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


class MergeFacetsParams(GenomeSpySchema):
    """Generated wrapper for ``MergeFacetsParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("MergeFacetsParams", {})

    def __init__(
        self, description: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(description=description, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_description(self, value: Any) -> MergeFacetsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_type(self, value: Any) -> MergeFacetsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_attach(self, value: Any) -> MultiUrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: Any) -> MultiUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiUrlSourceRef:
        """Return a copy with a ``FieldName`` field."""
        return self._with_property("field", value, **kwargs)

    def with_maxValues(self, value: Any) -> MultiUrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Any) -> MultiUrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: Any) -> MultiUrlSourceRef:
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

    def with_axes(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_multiscale(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: ViewOpacityDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``ViewOpacityDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_stops(
        self,
        value: MultiscaleStopsDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``MultiscaleStopsDef`` stops."""
        return self._with_property("stops", value, **kwargs)

    def with_templates(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> MultiscaleSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleStops:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_fade(self, value: Any) -> MultiscaleStops:
        """Return a copy with ``fade`` updated."""
        return self._with_property("fade", value)

    def with_metric(self, value: Any) -> MultiscaleStops:
        """Return a copy with ``metric`` updated."""
        return self._with_property("metric", value)

    def with_values(self, value: Any) -> MultiscaleStops:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> MultiscaleStopsDef:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_fade(self, value: Any) -> MultiscaleStopsDef:
        """Return a copy with ``fade`` updated."""
        return self._with_property("fade", value)

    def with_metric(self, value: Any) -> MultiscaleStopsDef:
        """Return a copy with ``metric`` updated."""
        return self._with_property("metric", value)

    def with_values(self, value: Any) -> MultiscaleStopsDef:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_description(self, value: Any) -> NamedData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NamedData:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_name(self, value: Any) -> NamedData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


class NamedGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``NamedGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NamedGenomeConfig", {})

    def __init__(
        self, contigs: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(contigs=contigs, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_contigs(self, value: Any) -> NamedGenomeConfig:
        """Return a copy with ``contigs`` updated."""
        return self._with_property("contigs", value)

    def with_url(self, value: Any) -> NamedGenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


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

    def with_band(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> NumericMarkPropDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> NumericMarkPropDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


class NumericStopDef(GenomeSpySchema):
    """Generated wrapper for ``NumericStopDef``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("NumericStopDef", {})

    def __init__(self, expr: Any = Undefined, **kwds: Any) -> None:
        super().__init__(expr=expr)
        if kwds:
            self._kwds.update(kwds)

    def with_expr(self, value: Any) -> NumericStopDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)


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

    def with_description(self, value: Any) -> NumericValueDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> NumericValueDef:
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


class OtherDataFormat(GenomeSpySchema):
    """Generated wrapper for ``OtherDataFormat``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("OtherDataFormat", {})

    def __init__(
        self, parse: Any = Undefined, type: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(parse=parse, type=type)
        if kwds:
            self._kwds.update(kwds)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> OtherDataFormat:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> OtherDataFormat:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_columnPadding(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_description(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_direction(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_fontSize(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_labelOffset(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelWidth(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PackLegendLabelsParams:
        """Return a copy with a ``Field`` labelWidth."""
        return self._with_property("labelWidth", value, **kwargs)

    def with_rowPadding(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_symbolOffset(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PackLegendLabelsParams:
        """Return a copy with a ``Field`` symbolSize."""
        return self._with_property("symbolSize", value, **kwargs)

    def with_symbolStrokeWidth(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PackLegendLabelsParams:
        """Return a copy with a ``Field`` symbolStrokeWidth."""
        return self._with_property("symbolStrokeWidth", value, **kwargs)

    def with_type(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_xOffset(self, value: Any) -> PackLegendLabelsParams:
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

    def with_yOffset(self, value: Any) -> PackLegendLabelsParams:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_bottom(self, value: Any) -> PaddingConfig:
        """Return a copy with ``bottom`` updated."""
        return self._with_property("bottom", value)

    def with_left(self, value: Any) -> PaddingConfig:
        """Return a copy with ``left`` updated."""
        return self._with_property("left", value)

    def with_right(self, value: Any) -> PaddingConfig:
        """Return a copy with ``right`` updated."""
        return self._with_property("right", value)

    def with_top(self, value: Any) -> PaddingConfig:
        """Return a copy with ``top`` updated."""
        return self._with_property("top", value)


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

    def with_bottom(self, value: Any) -> Paddings:
        """Return a copy with ``bottom`` updated."""
        return self._with_property("bottom", value)

    def with_left(self, value: Any) -> Paddings:
        """Return a copy with ``left`` updated."""
        return self._with_property("left", value)

    def with_right(self, value: Any) -> Paddings:
        """Return a copy with ``right`` updated."""
        return self._with_property("right", value)

    def with_top(self, value: Any) -> Paddings:
        """Return a copy with ``top`` updated."""
        return self._with_property("top", value)


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

    def with_bind(
        self,
        value: Binding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``Binding`` bind."""
        return self._with_property("bind", value, **kwargs)

    def with_description(self, value: Any) -> Parameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: Any) -> Parameter:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_name(self, value: Any) -> Parameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: Any) -> Parameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Any) -> Parameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_ruler(
        self,
        value: RulerConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``RulerConfig`` ruler."""
        return self._with_property("ruler", value, **kwargs)

    def with_select(
        self,
        value: SelectionType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``SelectionType`` select."""
        return self._with_property("select", value, **kwargs)

    def with_value(
        self,
        value: RulerInitMapping | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Parameter:
        """Return a copy with a ``RulerInitMapping`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_description(self, value: Any) -> PileupParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_end(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PileupParams:
        """Return a copy with a ``Field`` end."""
        return self._with_property("end", value, **kwargs)

    def with_preference(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PileupParams:
        """Return a copy with a ``Field`` preference."""
        return self._with_property("preference", value, **kwargs)

    def with_preferredOrder(self, value: Any) -> PileupParams:
        """Return a copy with ``preferredOrder`` updated."""
        return self._with_property("preferredOrder", value)

    def with_spacing(self, value: Any) -> PileupParams:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_start(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PileupParams:
        """Return a copy with a ``Field`` start."""
        return self._with_property("start", value, **kwargs)

    def with_type(self, value: Any) -> PileupParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_buildIndex(self, value: Any) -> PointConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> PointConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> PointConfig:
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

    def with_filled(self, value: Any) -> PointConfig:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_geometricZoomBound(self, value: Any) -> PointConfig:
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

    def with_minBufferSize(self, value: Any) -> PointConfig:
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

    def with_sampleFacetPadding(self, value: Any) -> PointConfig:
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

    def with_style(self, value: Any) -> PointConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: Any) -> PointConfig:
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

    def with_yOffset(self, value: Any) -> PointConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_buildIndex(self, value: Any) -> PointProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> PointProps:
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

    def with_cullByVisibleRange(self, value: Any) -> PointProps:
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

    def with_filled(self, value: Any) -> PointProps:
        """Return a copy with ``filled`` updated."""
        return self._with_property("filled", value)

    def with_geometricZoomBound(self, value: Any) -> PointProps:
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

    def with_minBufferSize(self, value: Any) -> PointProps:
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

    def with_sampleFacetPadding(self, value: Any) -> PointProps:
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

    def with_style(self, value: Any) -> PointProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> PointProps:
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

    def with_xOffset(self, value: Any) -> PointProps:
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

    def with_yOffset(self, value: Any) -> PointProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_clear(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointSelectionConfig:
        """Return a copy with a ``DomEventType`` clear."""
        return self._with_property("clear", value, **kwargs)

    def with_on(
        self,
        value: DomEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PointSelectionConfig:
        """Return a copy with a ``DomEventType`` on."""
        return self._with_property("on", value, **kwargs)

    def with_toggle(self, value: Any) -> PointSelectionConfig:
        """Return a copy with ``toggle`` updated."""
        return self._with_property("toggle", value)

    def with_type(self, value: Any) -> PointSelectionConfig:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> Position2Def:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``FieldName`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> Position2Def:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> Position2Def:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: Any) -> Position2Def:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: Any) -> Position2Def:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_offset(self, value: Any) -> Position2Def:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``FieldName`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> Position2Def:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Position2Def:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> PositionDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> PositionDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> PositionDatumDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> PositionDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDatumDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> PositionDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``FieldName`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> PositionDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> PositionDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: Any) -> PositionDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: Any) -> PositionDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_offset(self, value: Any) -> PositionDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``FieldName`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> PositionDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionExprDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> PositionExprDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> PositionExprDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> PositionExprDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: Any) -> PositionExprDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_title(self, value: Any) -> PositionExprDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionExprDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> PositionFieldDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_description(self, value: Any) -> PositionFieldDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> PositionFieldDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> PositionFieldDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> PositionFieldDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> PositionFieldDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> PositionValueDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> PositionValueDef:
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

    def with_description(self, value: Any) -> ProjectParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_fields(self, value: Any) -> ProjectParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_type(self, value: Any) -> ProjectParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_angle(self, value: Any) -> RangeConfig:
        """Return a copy with ``angle`` updated."""
        return self._with_property("angle", value)

    def with_diverging(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RangeConfig:
        """Return a copy with a ``ColorSchemeConfig`` diverging."""
        return self._with_property("diverging", value, **kwargs)

    def with_heatmap(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RangeConfig:
        """Return a copy with a ``ColorSchemeConfig`` heatmap."""
        return self._with_property("heatmap", value, **kwargs)

    def with_ramp(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RangeConfig:
        """Return a copy with a ``ColorSchemeConfig`` ramp."""
        return self._with_property("ramp", value, **kwargs)

    def with_shape(self, value: Any) -> RangeConfig:
        """Return a copy with ``shape`` updated."""
        return self._with_property("shape", value)

    def with_size(self, value: Any) -> RangeConfig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)


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

    def with_buildIndex(self, value: Any) -> RectConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> RectConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> RectConfig:
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

    def with_filled(self, value: Any) -> RectConfig:
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

    def with_minBufferSize(self, value: Any) -> RectConfig:
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

    def with_style(self, value: Any) -> RectConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

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

    def with_xOffset(self, value: Any) -> RectConfig:
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

    def with_yOffset(self, value: Any) -> RectConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> RectProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> RectProps:
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

    def with_cullByVisibleRange(self, value: Any) -> RectProps:
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

    def with_filled(self, value: Any) -> RectProps:
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

    def with_minBufferSize(self, value: Any) -> RectProps:
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

    def with_style(self, value: Any) -> RectProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RectProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> RectProps:
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

    def with_xOffset(self, value: Any) -> RectProps:
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

    def with_yOffset(self, value: Any) -> RectProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_description(self, value: Any) -> RegexExtractParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RegexExtractParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_regex(self, value: Any) -> RegexExtractParams:
        """Return a copy with ``regex`` updated."""
        return self._with_property("regex", value)

    def with_skipInvalidInput(self, value: Any) -> RegexExtractParams:
        """Return a copy with ``skipInvalidInput`` updated."""
        return self._with_property("skipInvalidInput", value)

    def with_type(self, value: Any) -> RegexExtractParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_asKey(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``asKey`` updated."""
        return self._with_property("asKey", value)

    def with_asValue(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``asValue`` updated."""
        return self._with_property("asValue", value)

    def with_columnRegex(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``columnRegex`` updated."""
        return self._with_property("columnRegex", value)

    def with_description(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_skipRegex(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``skipRegex`` updated."""
        return self._with_property("skipRegex", value)

    def with_type(self, value: Any) -> RegexFoldParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_buildIndex(self, value: Any) -> RuleConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> RuleConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> RuleConfig:
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

    def with_minBufferSize(self, value: Any) -> RuleConfig:
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

    def with_strokeDash(self, value: Any) -> RuleConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> RuleConfig:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: Any) -> RuleConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

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

    def with_xOffset(self, value: Any) -> RuleConfig:
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

    def with_yOffset(self, value: Any) -> RuleConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> RuleProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> RuleProps:
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

    def with_cullByVisibleRange(self, value: Any) -> RuleProps:
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

    def with_minBufferSize(self, value: Any) -> RuleProps:
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

    def with_strokeDash(self, value: Any) -> RuleProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> RuleProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: Any) -> RuleProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RuleProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> RuleProps:
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

    def with_xOffset(self, value: Any) -> RuleProps:
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

    def with_yOffset(self, value: Any) -> RuleProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


class RulerChannelValue(GenomeSpySchema):
    """Generated wrapper for ``RulerChannelValue``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("RulerChannelValue", {})

    def __init__(
        self, chrom: Any = Undefined, pos: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(chrom=chrom, pos=pos)
        if kwds:
            self._kwds.update(kwds)

    def with_chrom(self, value: Any) -> RulerChannelValue:
        """Return a copy with ``chrom`` updated."""
        return self._with_property("chrom", value)

    def with_pos(self, value: Any) -> RulerChannelValue:
        """Return a copy with ``pos`` updated."""
        return self._with_property("pos", value)


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

    def with_clear(
        self,
        value: RulerClear | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerClear`` clear."""
        return self._with_property("clear", value, **kwargs)

    def with_display(
        self,
        value: RulerDisplay | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerDisplay`` display."""
        return self._with_property("display", value, **kwargs)

    def with_encodings(self, value: Any) -> RulerConfig:
        """Return a copy with ``encodings`` updated."""
        return self._with_property("encodings", value)

    def with_extent(
        self,
        value: RulerExtent | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerExtent`` extent."""
        return self._with_property("extent", value, **kwargs)

    def with_mark(
        self,
        value: RulerMarkConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerMarkConfig`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_on(
        self,
        value: RulerEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerEventType`` on."""
        return self._with_property("on", value, **kwargs)

    def with_snap(
        self,
        value: RulerSnap | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerSnap`` snap."""
        return self._with_property("snap", value, **kwargs)

    def with_source(
        self,
        value: RulerSource | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerConfig:
        """Return a copy with a ``RulerSource`` source."""
        return self._with_property("source", value, **kwargs)


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

    def with_filter(self, value: Any) -> RulerEventConfig:
        """Return a copy with ``filter`` updated."""
        return self._with_property("filter", value)

    def with_type(
        self,
        value: RulerEventType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerEventConfig:
        """Return a copy with a ``RulerEventType`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_x(
        self,
        value: RulerChannelValue | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerInitMapping:
        """Return a copy with a ``RulerChannelValue`` x."""
        return self._with_property("x", value, **kwargs)

    def with_y(
        self,
        value: RulerChannelValue | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> RulerInitMapping:
        """Return a copy with a ``RulerChannelValue`` y."""
        return self._with_property("y", value, **kwargs)


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

    def with_fill(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``fillOpacity`` updated."""
        return self._with_property("fillOpacity", value)

    def with_opacity(self, value: Any) -> RulerMarkConfig:
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

    def with_stroke(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeDash(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeWidth(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_zindex(self, value: Any) -> RulerMarkConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_description(self, value: Any) -> RulerParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: Any) -> RulerParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: Any) -> RulerParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Any) -> RulerParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_ruler(
        self,
        value: RulerConfig | dict[str, Any] | None | Any = Undefined,
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

    def with_description(self, value: Any) -> SampleParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_size(self, value: Any) -> SampleParams:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_type(self, value: Any) -> SampleParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_align(self, value: Any) -> Scale:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_assembly(
        self,
        value: InlineLocusAssembly | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``InlineLocusAssembly`` assembly."""
        return self._with_property("assembly", value, **kwargs)

    def with_base(self, value: Any) -> Scale:
        """Return a copy with ``base`` updated."""
        return self._with_property("base", value)

    def with_bins(self, value: Any) -> Scale:
        """Return a copy with ``bins`` updated."""
        return self._with_property("bins", value)

    def with_clamp(self, value: Any) -> Scale:
        """Return a copy with ``clamp`` updated."""
        return self._with_property("clamp", value)

    def with_constant(self, value: Any) -> Scale:
        """Return a copy with ``constant`` updated."""
        return self._with_property("constant", value)

    def with_domain(
        self,
        value: ScalarDomain | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``ScalarDomain`` domain."""
        return self._with_property("domain", value, **kwargs)

    def with_domainMax(self, value: Any) -> Scale:
        """Return a copy with ``domainMax`` updated."""
        return self._with_property("domainMax", value)

    def with_domainMid(self, value: Any) -> Scale:
        """Return a copy with ``domainMid`` updated."""
        return self._with_property("domainMid", value)

    def with_domainMin(self, value: Any) -> Scale:
        """Return a copy with ``domainMin`` updated."""
        return self._with_property("domainMin", value)

    def with_domainTransition(self, value: Any) -> Scale:
        """Return a copy with ``domainTransition`` updated."""
        return self._with_property("domainTransition", value)

    def with_exponent(self, value: Any) -> Scale:
        """Return a copy with ``exponent`` updated."""
        return self._with_property("exponent", value)

    def with_interpolate(
        self,
        value: ScaleInterpolate | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``ScaleInterpolate`` interpolate."""
        return self._with_property("interpolate", value, **kwargs)

    def with_name(self, value: Any) -> Scale:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_nice(self, value: Any) -> Scale:
        """Return a copy with ``nice`` updated."""
        return self._with_property("nice", value)

    def with_numberingOffset(self, value: Any) -> Scale:
        """Return a copy with ``numberingOffset`` updated."""
        return self._with_property("numberingOffset", value)

    def with_padding(self, value: Any) -> Scale:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_paddingInner(self, value: Any) -> Scale:
        """Return a copy with ``paddingInner`` updated."""
        return self._with_property("paddingInner", value)

    def with_paddingOuter(self, value: Any) -> Scale:
        """Return a copy with ``paddingOuter`` updated."""
        return self._with_property("paddingOuter", value)

    def with_range(self, value: Any) -> Scale:
        """Return a copy with ``range`` updated."""
        return self._with_property("range", value)

    def with_reverse(self, value: Any) -> Scale:
        """Return a copy with ``reverse`` updated."""
        return self._with_property("reverse", value)

    def with_round(self, value: Any) -> Scale:
        """Return a copy with ``round`` updated."""
        return self._with_property("round", value)

    def with_scheme(
        self,
        value: SchemeParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``SchemeParams`` scheme."""
        return self._with_property("scheme", value, **kwargs)

    def with_type(
        self,
        value: ScaleType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``ScaleType`` type."""
        return self._with_property("type", value, **kwargs)

    def with_zero(self, value: Any) -> Scale:
        """Return a copy with ``zero`` updated."""
        return self._with_property("zero", value)

    def with_zoom(
        self,
        value: ZoomParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Scale:
        """Return a copy with a ``ZoomParams`` zoom."""
        return self._with_property("zoom", value, **kwargs)


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

    def with_align(self, value: Any) -> ScaleConfig:
        """Return a copy with ``align`` updated."""
        return self._with_property("align", value)

    def with_assembly(
        self,
        value: InlineLocusAssembly | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``InlineLocusAssembly`` assembly."""
        return self._with_property("assembly", value, **kwargs)

    def with_base(self, value: Any) -> ScaleConfig:
        """Return a copy with ``base`` updated."""
        return self._with_property("base", value)

    def with_bins(self, value: Any) -> ScaleConfig:
        """Return a copy with ``bins`` updated."""
        return self._with_property("bins", value)

    def with_clamp(self, value: Any) -> ScaleConfig:
        """Return a copy with ``clamp`` updated."""
        return self._with_property("clamp", value)

    def with_constant(self, value: Any) -> ScaleConfig:
        """Return a copy with ``constant`` updated."""
        return self._with_property("constant", value)

    def with_domain(
        self,
        value: ScalarDomain | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ScalarDomain`` domain."""
        return self._with_property("domain", value, **kwargs)

    def with_domainMax(self, value: Any) -> ScaleConfig:
        """Return a copy with ``domainMax`` updated."""
        return self._with_property("domainMax", value)

    def with_domainMid(self, value: Any) -> ScaleConfig:
        """Return a copy with ``domainMid`` updated."""
        return self._with_property("domainMid", value)

    def with_domainMin(self, value: Any) -> ScaleConfig:
        """Return a copy with ``domainMin`` updated."""
        return self._with_property("domainMin", value)

    def with_domainTransition(self, value: Any) -> ScaleConfig:
        """Return a copy with ``domainTransition`` updated."""
        return self._with_property("domainTransition", value)

    def with_exponent(self, value: Any) -> ScaleConfig:
        """Return a copy with ``exponent`` updated."""
        return self._with_property("exponent", value)

    def with_index(self, value: Any) -> ScaleConfig:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_interpolate(
        self,
        value: ScaleInterpolate | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ScaleInterpolate`` interpolate."""
        return self._with_property("interpolate", value, **kwargs)

    def with_locus(self, value: Any) -> ScaleConfig:
        """Return a copy with ``locus`` updated."""
        return self._with_property("locus", value)

    def with_name(self, value: Any) -> ScaleConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_nice(self, value: Any) -> ScaleConfig:
        """Return a copy with ``nice`` updated."""
        return self._with_property("nice", value)

    def with_nominal(self, value: Any) -> ScaleConfig:
        """Return a copy with ``nominal`` updated."""
        return self._with_property("nominal", value)

    def with_nominalColorScheme(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ColorSchemeConfig`` nominalColorScheme."""
        return self._with_property("nominalColorScheme", value, **kwargs)

    def with_numberingOffset(self, value: Any) -> ScaleConfig:
        """Return a copy with ``numberingOffset`` updated."""
        return self._with_property("numberingOffset", value)

    def with_ordinal(self, value: Any) -> ScaleConfig:
        """Return a copy with ``ordinal`` updated."""
        return self._with_property("ordinal", value)

    def with_ordinalColorScheme(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ColorSchemeConfig`` ordinalColorScheme."""
        return self._with_property("ordinalColorScheme", value, **kwargs)

    def with_padding(self, value: Any) -> ScaleConfig:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_paddingInner(self, value: Any) -> ScaleConfig:
        """Return a copy with ``paddingInner`` updated."""
        return self._with_property("paddingInner", value)

    def with_paddingOuter(self, value: Any) -> ScaleConfig:
        """Return a copy with ``paddingOuter`` updated."""
        return self._with_property("paddingOuter", value)

    def with_quantitative(self, value: Any) -> ScaleConfig:
        """Return a copy with ``quantitative`` updated."""
        return self._with_property("quantitative", value)

    def with_quantitativeColorScheme(
        self,
        value: ColorSchemeConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ColorSchemeConfig`` quantitativeColorScheme."""
        return self._with_property("quantitativeColorScheme", value, **kwargs)

    def with_range(self, value: Any) -> ScaleConfig:
        """Return a copy with ``range`` updated."""
        return self._with_property("range", value)

    def with_reverse(self, value: Any) -> ScaleConfig:
        """Return a copy with ``reverse`` updated."""
        return self._with_property("reverse", value)

    def with_round(self, value: Any) -> ScaleConfig:
        """Return a copy with ``round`` updated."""
        return self._with_property("round", value)

    def with_scheme(
        self,
        value: SchemeParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``SchemeParams`` scheme."""
        return self._with_property("scheme", value, **kwargs)

    def with_type(
        self,
        value: ScaleType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ScaleType`` type."""
        return self._with_property("type", value, **kwargs)

    def with_zero(self, value: Any) -> ScaleConfig:
        """Return a copy with ``zero`` updated."""
        return self._with_property("zero", value)

    def with_zoom(
        self,
        value: ZoomParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ScaleConfig:
        """Return a copy with a ``ZoomParams`` zoom."""
        return self._with_property("zoom", value, **kwargs)


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

    def with_gamma(self, value: Any) -> ScaleInterpolateParams:
        """Return a copy with ``gamma`` updated."""
        return self._with_property("gamma", value)

    def with_type(self, value: Any) -> ScaleInterpolateParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_count(self, value: Any) -> SchemeParams:
        """Return a copy with ``count`` updated."""
        return self._with_property("count", value)

    def with_extent(self, value: Any) -> SchemeParams:
        """Return a copy with ``extent`` updated."""
        return self._with_property("extent", value)

    def with_name(self, value: Any) -> SchemeParams:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)


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

    def with_description(self, value: Any) -> SearchDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(self, value: Any) -> SearchDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_title(self, value: Any) -> SearchDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


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

    def with_axis(
        self,
        value: GenomeAxis | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SecondaryChromPosDef:
        """Return a copy with a ``GenomeAxis`` axis."""
        return self._with_property("axis", value, **kwargs)

    def with_band(self, value: Any) -> SecondaryChromPosDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_chrom(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SecondaryChromPosDef:
        """Return a copy with a ``FieldName`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_description(self, value: Any) -> SecondaryChromPosDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> SecondaryChromPosDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_offset(self, value: Any) -> SecondaryChromPosDef:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_pos(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SecondaryChromPosDef:
        """Return a copy with a ``FieldName`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_title(self, value: Any) -> SecondaryChromPosDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)


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

    def with_encoding(self, value: Any) -> SelectionDomainRef:
        """Return a copy with ``encoding`` updated."""
        return self._with_property("encoding", value)

    def with_initial(
        self,
        value: ScalarDomain | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SelectionDomainRef:
        """Return a copy with a ``ScalarDomain`` initial."""
        return self._with_property("initial", value, **kwargs)

    def with_param(self, value: Any) -> SelectionDomainRef:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)


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

    def with_description(self, value: Any) -> SelectionFilterParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_empty(self, value: Any) -> SelectionFilterParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_fields(self, value: Any) -> SelectionFilterParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_param(self, value: Any) -> SelectionFilterParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_type(self, value: Any) -> SelectionFilterParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


class SelectionInitIntervalMapping(GenomeSpySchema):
    """Generated wrapper for ``SelectionInitIntervalMapping``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get(
        "SelectionInitIntervalMapping", {}
    )

    def __init__(self, x: Any = Undefined, y: Any = Undefined, **kwds: Any) -> None:
        super().__init__(x=x, y=y)
        if kwds:
            self._kwds.update(kwds)

    def with_x(self, value: Any) -> SelectionInitIntervalMapping:
        """Return a copy with ``x`` updated."""
        return self._with_property("x", value)

    def with_y(self, value: Any) -> SelectionInitIntervalMapping:
        """Return a copy with ``y`` updated."""
        return self._with_property("y", value)


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

    def with_description(self, value: Any) -> SelectionParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: Any) -> SelectionParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: Any) -> SelectionParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Any) -> SelectionParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_select(
        self,
        value: SelectionType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SelectionParameter:
        """Return a copy with a ``SelectionType`` select."""
        return self._with_property("select", value, **kwargs)

    def with_value(
        self,
        value: SelectionInitIntervalMapping | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SelectionParameter:
        """Return a copy with a ``SelectionInitIntervalMapping`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_buildIndex(self, value: Any) -> SeparatorProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> SeparatorProps:
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

    def with_cullByVisibleRange(self, value: Any) -> SeparatorProps:
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

    def with_includePlotMargin(self, value: Any) -> SeparatorProps:
        """Return a copy with ``includePlotMargin`` updated."""
        return self._with_property("includePlotMargin", value)

    def with_minBufferSize(self, value: Any) -> SeparatorProps:
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

    def with_strokeDash(self, value: Any) -> SeparatorProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> SeparatorProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: Any) -> SeparatorProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SeparatorProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> SeparatorProps:
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

    def with_xOffset(self, value: Any) -> SeparatorProps:
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

    def with_yOffset(self, value: Any) -> SeparatorProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)

    def with_zindex(self, value: Any) -> SeparatorProps:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_description(self, value: Any) -> SequenceGenerator:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_name(self, value: Any) -> SequenceGenerator:
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

    def with_band(self, value: Any) -> ShapeDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``ConditionalMarkPropFieldDefTypeForShape`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> ShapeDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ShapeDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> ShapeDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> ShapeDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_legend(
        self,
        value: Legend | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Legend`` legend."""
        return self._with_property("legend", value, **kwargs)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> ShapeDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ShapeDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_attach(self, value: Any) -> SingleUrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: Any) -> SingleUrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> SingleUrlSourceRef:
        """Return a copy with a ``FieldName`` field."""
        return self._with_property("field", value, **kwargs)

    def with_maxValues(self, value: Any) -> SingleUrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Any) -> SingleUrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: Any) -> SingleUrlSourceRef:
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

    def with_grow(self, value: Any) -> SizeDef:
        """Return a copy with ``grow`` updated."""
        return self._with_property("grow", value)

    def with_maxPx(self, value: Any) -> SizeDef:
        """Return a copy with ``maxPx`` updated."""
        return self._with_property("maxPx", value)

    def with_minPx(self, value: Any) -> SizeDef:
        """Return a copy with ``minPx`` updated."""
        return self._with_property("minPx", value)

    def with_px(self, value: Any) -> SizeDef:
        """Return a copy with ``px`` updated."""
        return self._with_property("px", value)


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

    def with_baseField(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StackParams:
        """Return a copy with a ``Field`` baseField."""
        return self._with_property("baseField", value, **kwargs)

    def with_cardinality(self, value: Any) -> StackParams:
        """Return a copy with ``cardinality`` updated."""
        return self._with_property("cardinality", value)

    def with_description(self, value: Any) -> StackParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StackParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_groupby(self, value: Any) -> StackParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_offset(self, value: Any) -> StackParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_sort(
        self,
        value: CompareParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StackParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_type(self, value: Any) -> StackParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


class Step(GenomeSpySchema):
    """Generated wrapper for ``Step``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("Step", {})

    def __init__(self, step: Any = Undefined, **kwds: Any) -> None:
        super().__init__(step=step)
        if kwds:
            self._kwds.update(kwds)

    def with_step(self, value: Any) -> Step:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)


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

    def with_band(self, value: Any) -> StringDatumDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringDatumDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> StringDatumDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(self, value: Any) -> StringDatumDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringDatumDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringDatumDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> StringDatumDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringDatumDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_description(self, value: Any) -> StringFieldDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> StringFieldDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_field(self, value: Any) -> StringFieldDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> StringFieldDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_title(self, value: Any) -> StringFieldDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StringFieldDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

    def with_anchor(
        self,
        value: TitleAnchor | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``TitleAnchor`` anchor."""
        return self._with_property("anchor", value, **kwargs)

    def with_angle(self, value: Any) -> StyleConfig:
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

    def with_backgroundFill(self, value: Any) -> StyleConfig:
        """Return a copy with ``backgroundFill`` updated."""
        return self._with_property("backgroundFill", value)

    def with_backgroundFillOpacity(self, value: Any) -> StyleConfig:
        """Return a copy with ``backgroundFillOpacity`` updated."""
        return self._with_property("backgroundFillOpacity", value)

    def with_backgroundStroke(self, value: Any) -> StyleConfig:
        """Return a copy with ``backgroundStroke`` updated."""
        return self._with_property("backgroundStroke", value)

    def with_backgroundStrokeOpacity(self, value: Any) -> StyleConfig:
        """Return a copy with ``backgroundStrokeOpacity`` updated."""
        return self._with_property("backgroundStrokeOpacity", value)

    def with_backgroundStrokeWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``backgroundStrokeWidth`` updated."""
        return self._with_property("backgroundStrokeWidth", value)

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_buildIndex(self, value: Any) -> StyleConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_chromGrid(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGrid`` updated."""
        return self._with_property("chromGrid", value)

    def with_chromGridCap(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridCap`` updated."""
        return self._with_property("chromGridCap", value)

    def with_chromGridColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridColor`` updated."""
        return self._with_property("chromGridColor", value)

    def with_chromGridDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridDash`` updated."""
        return self._with_property("chromGridDash", value)

    def with_chromGridDashOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridDashOffset`` updated."""
        return self._with_property("chromGridDashOffset", value)

    def with_chromGridFillEven(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridFillEven`` updated."""
        return self._with_property("chromGridFillEven", value)

    def with_chromGridFillOdd(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridFillOdd`` updated."""
        return self._with_property("chromGridFillOdd", value)

    def with_chromGridOpacity(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridOpacity`` updated."""
        return self._with_property("chromGridOpacity", value)

    def with_chromGridWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromGridWidth`` updated."""
        return self._with_property("chromGridWidth", value)

    def with_chromLabelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Align`` chromLabelAlign."""
        return self._with_property("chromLabelAlign", value, **kwargs)

    def with_chromLabelColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromLabelColor`` updated."""
        return self._with_property("chromLabelColor", value)

    def with_chromLabelFont(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromLabelFont`` updated."""
        return self._with_property("chromLabelFont", value)

    def with_chromLabelFontSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromLabelFontSize`` updated."""
        return self._with_property("chromLabelFontSize", value)

    def with_chromLabelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontStyle`` chromLabelFontStyle."""
        return self._with_property("chromLabelFontStyle", value, **kwargs)

    def with_chromLabelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontWeight`` chromLabelFontWeight."""
        return self._with_property("chromLabelFontWeight", value, **kwargs)

    def with_chromLabelPadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromLabelPadding`` updated."""
        return self._with_property("chromLabelPadding", value)

    def with_chromLabels(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromLabels`` updated."""
        return self._with_property("chromLabels", value)

    def with_chromTickColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromTickColor`` updated."""
        return self._with_property("chromTickColor", value)

    def with_chromTickDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromTickDash`` updated."""
        return self._with_property("chromTickDash", value)

    def with_chromTickDashOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromTickDashOffset`` updated."""
        return self._with_property("chromTickDashOffset", value)

    def with_chromTickSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromTickSize`` updated."""
        return self._with_property("chromTickSize", value)

    def with_chromTickWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``chromTickWidth`` updated."""
        return self._with_property("chromTickWidth", value)

    def with_chromTicks(self, value: Any) -> StyleConfig:
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

    def with_clip(self, value: Any) -> StyleConfig:
        """Return a copy with ``clip`` updated."""
        return self._with_property("clip", value)

    def with_color(self, value: Any) -> StyleConfig:
        """Return a copy with ``color`` updated."""
        return self._with_property("color", value)

    def with_columnPadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columns(self, value: Any) -> StyleConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> StyleConfig:
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

    def with_direction(
        self,
        value: LegendDirection | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``LegendDirection`` direction."""
        return self._with_property("direction", value, **kwargs)

    def with_disable(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``ExprRef`` disable."""
        return self._with_property("disable", value, **kwargs)

    def with_domain(self, value: Any) -> StyleConfig:
        """Return a copy with ``domain`` updated."""
        return self._with_property("domain", value)

    def with_domainCap(self, value: Any) -> StyleConfig:
        """Return a copy with ``domainCap`` updated."""
        return self._with_property("domainCap", value)

    def with_domainColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``domainColor`` updated."""
        return self._with_property("domainColor", value)

    def with_domainDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``domainDash`` updated."""
        return self._with_property("domainDash", value)

    def with_domainDashOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``domainDashOffset`` updated."""
        return self._with_property("domainDashOffset", value)

    def with_domainWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``domainWidth`` updated."""
        return self._with_property("domainWidth", value)

    def with_dx(self, value: Any) -> StyleConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: Any) -> StyleConfig:
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

    def with_filled(self, value: Any) -> StyleConfig:
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

    def with_font(self, value: Any) -> StyleConfig:
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

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_format(self, value: Any) -> StyleConfig:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_frame(
        self,
        value: TitleFrame | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``TitleFrame`` frame."""
        return self._with_property("frame", value, **kwargs)

    def with_geometricZoomBound(self, value: Any) -> StyleConfig:
        """Return a copy with ``geometricZoomBound`` updated."""
        return self._with_property("geometricZoomBound", value)

    def with_grid(self, value: Any) -> StyleConfig:
        """Return a copy with ``grid`` updated."""
        return self._with_property("grid", value)

    def with_gridCap(self, value: Any) -> StyleConfig:
        """Return a copy with ``gridCap`` updated."""
        return self._with_property("gridCap", value)

    def with_gridColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``gridColor`` updated."""
        return self._with_property("gridColor", value)

    def with_gridDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``gridDash`` updated."""
        return self._with_property("gridDash", value)

    def with_gridDashOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``gridDashOffset`` updated."""
        return self._with_property("gridDashOffset", value)

    def with_gridOpacity(self, value: Any) -> StyleConfig:
        """Return a copy with ``gridOpacity`` updated."""
        return self._with_property("gridOpacity", value)

    def with_gridWidth(self, value: Any) -> StyleConfig:
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

    def with_labelAlign(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Align`` labelAlign."""
        return self._with_property("labelAlign", value, **kwargs)

    def with_labelAngle(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelAngle`` updated."""
        return self._with_property("labelAngle", value)

    def with_labelBaseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Baseline`` labelBaseline."""
        return self._with_property("labelBaseline", value, **kwargs)

    def with_labelColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelColor`` updated."""
        return self._with_property("labelColor", value)

    def with_labelFont(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelFont`` updated."""
        return self._with_property("labelFont", value)

    def with_labelFontSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelFontSize`` updated."""
        return self._with_property("labelFontSize", value)

    def with_labelFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontStyle`` labelFontStyle."""
        return self._with_property("labelFontStyle", value, **kwargs)

    def with_labelFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontWeight`` labelFontWeight."""
        return self._with_property("labelFontWeight", value, **kwargs)

    def with_labelLimit(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelLimit`` updated."""
        return self._with_property("labelLimit", value)

    def with_labelOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelPadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``labelPadding`` updated."""
        return self._with_property("labelPadding", value)

    def with_labels(self, value: Any) -> StyleConfig:
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

    def with_maxExtent(self, value: Any) -> StyleConfig:
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

    def with_minBufferSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``minBufferSize`` updated."""
        return self._with_property("minBufferSize", value)

    def with_minExtent(self, value: Any) -> StyleConfig:
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

    def with_offset(self, value: Any) -> StyleConfig:
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
        value: AxisOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``AxisOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_padding(self, value: Any) -> StyleConfig:
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

    def with_placement(
        self,
        value: AxisPlacement | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``AxisPlacement`` placement."""
        return self._with_property("placement", value, **kwargs)

    def with_reserve(self, value: Any) -> StyleConfig:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_rowPadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_sampleFacetPadding(self, value: Any) -> StyleConfig:
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

    def with_size(self, value: Any) -> StyleConfig:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_spacing(self, value: Any) -> StyleConfig:
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

    def with_strokeDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> StyleConfig:
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

    def with_style(self, value: Any) -> StyleConfig:
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

    def with_subtitleFont(self, value: Any) -> StyleConfig:
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

    def with_subtitleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontStyle`` subtitleFontStyle."""
        return self._with_property("subtitleFontStyle", value, **kwargs)

    def with_subtitleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontWeight`` subtitleFontWeight."""
        return self._with_property("subtitleFontWeight", value, **kwargs)

    def with_subtitlePadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``subtitlePadding`` updated."""
        return self._with_property("subtitlePadding", value)

    def with_symbolBaseFillColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolBaseFillColor`` updated."""
        return self._with_property("symbolBaseFillColor", value)

    def with_symbolBaseStrokeColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolBaseStrokeColor`` updated."""
        return self._with_property("symbolBaseStrokeColor", value)

    def with_symbolOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolSize`` updated."""
        return self._with_property("symbolSize", value)

    def with_symbolStrokeWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolStrokeWidth`` updated."""
        return self._with_property("symbolStrokeWidth", value)

    def with_symbolType(self, value: Any) -> StyleConfig:
        """Return a copy with ``symbolType`` updated."""
        return self._with_property("symbolType", value)

    def with_text(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Scalar`` text."""
        return self._with_property("text", value, **kwargs)

    def with_thickness(self, value: Any) -> StyleConfig:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tickCap(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickCap`` updated."""
        return self._with_property("tickCap", value)

    def with_tickColor(self, value: Any) -> StyleConfig:
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

    def with_tickDash(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickDash`` updated."""
        return self._with_property("tickDash", value)

    def with_tickDashOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickDashOffset`` updated."""
        return self._with_property("tickDashOffset", value)

    def with_tickMinStep(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickMinStep`` updated."""
        return self._with_property("tickMinStep", value)

    def with_tickSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickSize`` updated."""
        return self._with_property("tickSize", value)

    def with_tickWidth(self, value: Any) -> StyleConfig:
        """Return a copy with ``tickWidth`` updated."""
        return self._with_property("tickWidth", value)

    def with_ticks(self, value: Any) -> StyleConfig:
        """Return a copy with ``ticks`` updated."""
        return self._with_property("ticks", value)

    def with_title(self, value: Any) -> StyleConfig:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_titleColor(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleColor`` updated."""
        return self._with_property("titleColor", value)

    def with_titleFit(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleFit`` updated."""
        return self._with_property("titleFit", value)

    def with_titleFont(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleFont`` updated."""
        return self._with_property("titleFont", value)

    def with_titleFontSize(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleFontSize`` updated."""
        return self._with_property("titleFontSize", value)

    def with_titleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontStyle`` titleFontStyle."""
        return self._with_property("titleFontStyle", value, **kwargs)

    def with_titleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``FontWeight`` titleFontWeight."""
        return self._with_property("titleFontWeight", value, **kwargs)

    def with_titleLimit(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleLimit`` updated."""
        return self._with_property("titleLimit", value)

    def with_titleOpacity(self, value: Any) -> StyleConfig:
        """Return a copy with ``titleOpacity`` updated."""
        return self._with_property("titleOpacity", value)

    def with_titleOrient(
        self,
        value: LegendTitleOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``LegendTitleOrient`` titleOrient."""
        return self._with_property("titleOrient", value, **kwargs)

    def with_titlePadding(self, value: Any) -> StyleConfig:
        """Return a copy with ``titlePadding`` updated."""
        return self._with_property("titlePadding", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> StyleConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_values(self, value: Any) -> StyleConfig:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: Any) -> StyleConfig:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: Any) -> StyleConfig:
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

    def with_xOffset(self, value: Any) -> StyleConfig:
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

    def with_yOffset(self, value: Any) -> StyleConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)

    def with_zindex(self, value: Any) -> StyleConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_addChrPrefix(self, value: Any) -> TabixTsvData:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_columns(self, value: Any) -> TabixTsvData:
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

    def with_debounceMode(self, value: Any) -> TabixTsvData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_parse(
        self,
        value: Parse | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``Parse`` parse."""
        return self._with_property("parse", value, **kwargs)

    def with_type(self, value: Any) -> TabixTsvData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TabixTsvData:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(self, value: Any) -> TabixTsvData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


class TemplateImport(GenomeSpySchema):
    """Generated wrapper for ``TemplateImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("TemplateImport", {})

    def __init__(self, template: Any = Undefined, **kwds: Any) -> None:
        super().__init__(template=template)
        if kwds:
            self._kwds.update(kwds)

    def with_template(self, value: Any) -> TemplateImport:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_buildIndex(self, value: Any) -> TextConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> TextConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> TextConfig:
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

    def with_dx(self, value: Any) -> TextConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: Any) -> TextConfig:
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

    def with_font(self, value: Any) -> TextConfig:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_minBufferSize(self, value: Any) -> TextConfig:
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

    def with_style(self, value: Any) -> TextConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``Scalar`` text."""
        return self._with_property("text", value, **kwargs)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_viewportEdgeFadeDistanceBottom(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: Any) -> TextConfig:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: Any) -> TextConfig:
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

    def with_xOffset(self, value: Any) -> TextConfig:
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

    def with_yOffset(self, value: Any) -> TextConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_band(self, value: Any) -> TextDef:
        """Return a copy with ``band`` updated."""
        return self._with_property("band", value)

    def with_datum(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``Scalar`` datum."""
        return self._with_property("datum", value, **kwargs)

    def with_description(self, value: Any) -> TextDef:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> TextDef:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_expr(self, value: Any) -> TextDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(self, value: Any) -> TextDef:
        """Return a copy with ``field`` updated."""
        return self._with_property("field", value)

    def with_format(self, value: Any) -> TextDef:
        """Return a copy with ``format`` updated."""
        return self._with_property("format", value)

    def with_resolutionChannel(
        self,
        value: ChannelWithScale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``ChannelWithScale`` resolutionChannel."""
        return self._with_property("resolutionChannel", value, **kwargs)

    def with_scale(
        self,
        value: Scale | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``Scale`` scale."""
        return self._with_property("scale", value, **kwargs)

    def with_title(self, value: Any) -> TextDef:
        """Return a copy with ``title`` updated."""
        return self._with_property("title", value)

    def with_type(
        self,
        value: Type | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``Type`` type."""
        return self._with_property("type", value, **kwargs)

    def with_value(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextDef:
        """Return a copy with a ``ExprRef`` value."""
        return self._with_property("value", value, **kwargs)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_buildIndex(self, value: Any) -> TextProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> TextProps:
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

    def with_cullByVisibleRange(self, value: Any) -> TextProps:
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

    def with_dx(self, value: Any) -> TextProps:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: Any) -> TextProps:
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

    def with_font(self, value: Any) -> TextProps:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_logoLetters(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``ExprRef`` logoLetters."""
        return self._with_property("logoLetters", value, **kwargs)

    def with_minBufferSize(self, value: Any) -> TextProps:
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

    def with_style(self, value: Any) -> TextProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_text(
        self,
        value: Scalar | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``Scalar`` text."""
        return self._with_property("text", value, **kwargs)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TextProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> TextProps:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_viewportEdgeFadeDistanceBottom(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceBottom`` updated."""
        return self._with_property("viewportEdgeFadeDistanceBottom", value)

    def with_viewportEdgeFadeDistanceLeft(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceLeft`` updated."""
        return self._with_property("viewportEdgeFadeDistanceLeft", value)

    def with_viewportEdgeFadeDistanceRight(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceRight`` updated."""
        return self._with_property("viewportEdgeFadeDistanceRight", value)

    def with_viewportEdgeFadeDistanceTop(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeDistanceTop`` updated."""
        return self._with_property("viewportEdgeFadeDistanceTop", value)

    def with_viewportEdgeFadeWidthBottom(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthBottom`` updated."""
        return self._with_property("viewportEdgeFadeWidthBottom", value)

    def with_viewportEdgeFadeWidthLeft(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthLeft`` updated."""
        return self._with_property("viewportEdgeFadeWidthLeft", value)

    def with_viewportEdgeFadeWidthRight(self, value: Any) -> TextProps:
        """Return a copy with ``viewportEdgeFadeWidthRight`` updated."""
        return self._with_property("viewportEdgeFadeWidthRight", value)

    def with_viewportEdgeFadeWidthTop(self, value: Any) -> TextProps:
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

    def with_xOffset(self, value: Any) -> TextProps:
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

    def with_yOffset(self, value: Any) -> TextProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> TickConfig:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> TickConfig:
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

    def with_cullByVisibleRange(self, value: Any) -> TickConfig:
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

    def with_minBufferSize(self, value: Any) -> TickConfig:
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

    def with_orient(self, value: Any) -> TickConfig:
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

    def with_strokeDash(self, value: Any) -> TickConfig:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> TickConfig:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: Any) -> TickConfig:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_thickness(self, value: Any) -> TickConfig:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_x(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickConfig:
        """Return a copy with a ``ExprRef`` x."""
        return self._with_property("x", value, **kwargs)

    def with_xOffset(self, value: Any) -> TickConfig:
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

    def with_yOffset(self, value: Any) -> TickConfig:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_buildIndex(self, value: Any) -> TickProps:
        """Return a copy with ``buildIndex`` updated."""
        return self._with_property("buildIndex", value)

    def with_clip(self, value: Any) -> TickProps:
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

    def with_cullByVisibleRange(self, value: Any) -> TickProps:
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

    def with_minBufferSize(self, value: Any) -> TickProps:
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

    def with_orient(self, value: Any) -> TickProps:
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

    def with_strokeDash(self, value: Any) -> TickProps:
        """Return a copy with ``strokeDash`` updated."""
        return self._with_property("strokeDash", value)

    def with_strokeDashOffset(self, value: Any) -> TickProps:
        """Return a copy with ``strokeDashOffset`` updated."""
        return self._with_property("strokeDashOffset", value)

    def with_style(self, value: Any) -> TickProps:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_thickness(self, value: Any) -> TickProps:
        """Return a copy with ``thickness`` updated."""
        return self._with_property("thickness", value)

    def with_tooltip(
        self,
        value: Tooltip | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TickProps:
        """Return a copy with a ``Tooltip`` tooltip."""
        return self._with_property("tooltip", value, **kwargs)

    def with_type(self, value: Any) -> TickProps:
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

    def with_xOffset(self, value: Any) -> TickProps:
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

    def with_yOffset(self, value: Any) -> TickProps:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

    def with_anchor(
        self,
        value: TitleAnchor | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``TitleAnchor`` anchor."""
        return self._with_property("anchor", value, **kwargs)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_dx(self, value: Any) -> Title:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: Any) -> Title:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_font(self, value: Any) -> Title:
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

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_frame(
        self,
        value: TitleFrame | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``TitleFrame`` frame."""
        return self._with_property("frame", value, **kwargs)

    def with_offset(self, value: Any) -> Title:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: TitleOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``TitleOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_reserve(self, value: Any) -> Title:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_style(self, value: Any) -> Title:
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

    def with_subtitleFont(self, value: Any) -> Title:
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

    def with_subtitleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``FontStyle`` subtitleFontStyle."""
        return self._with_property("subtitleFontStyle", value, **kwargs)

    def with_subtitleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> Title:
        """Return a copy with a ``FontWeight`` subtitleFontWeight."""
        return self._with_property("subtitleFontWeight", value, **kwargs)

    def with_subtitlePadding(self, value: Any) -> Title:
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

    def with_zindex(self, value: Any) -> Title:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_align(
        self,
        value: Align | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``Align`` align."""
        return self._with_property("align", value, **kwargs)

    def with_anchor(
        self,
        value: TitleAnchor | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``TitleAnchor`` anchor."""
        return self._with_property("anchor", value, **kwargs)

    def with_angle(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` angle."""
        return self._with_property("angle", value, **kwargs)

    def with_baseline(
        self,
        value: Baseline | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``Baseline`` baseline."""
        return self._with_property("baseline", value, **kwargs)

    def with_color(
        self,
        value: ExprRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``ExprRef`` color."""
        return self._with_property("color", value, **kwargs)

    def with_dx(self, value: Any) -> TitleConfig:
        """Return a copy with ``dx`` updated."""
        return self._with_property("dx", value)

    def with_dy(self, value: Any) -> TitleConfig:
        """Return a copy with ``dy`` updated."""
        return self._with_property("dy", value)

    def with_font(self, value: Any) -> TitleConfig:
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

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_frame(
        self,
        value: TitleFrame | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``TitleFrame`` frame."""
        return self._with_property("frame", value, **kwargs)

    def with_offset(self, value: Any) -> TitleConfig:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_orient(
        self,
        value: TitleOrient | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``TitleOrient`` orient."""
        return self._with_property("orient", value, **kwargs)

    def with_reserve(self, value: Any) -> TitleConfig:
        """Return a copy with ``reserve`` updated."""
        return self._with_property("reserve", value)

    def with_style(self, value: Any) -> TitleConfig:
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

    def with_subtitleFont(self, value: Any) -> TitleConfig:
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

    def with_subtitleFontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``FontStyle`` subtitleFontStyle."""
        return self._with_property("subtitleFontStyle", value, **kwargs)

    def with_subtitleFontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TitleConfig:
        """Return a copy with a ``FontWeight`` subtitleFontWeight."""
        return self._with_property("subtitleFontWeight", value, **kwargs)

    def with_subtitlePadding(self, value: Any) -> TitleConfig:
        """Return a copy with ``subtitlePadding`` updated."""
        return self._with_property("subtitlePadding", value)

    def with_zindex(self, value: Any) -> TitleConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_handler(self, value: Any) -> Tooltip:
        """Return a copy with ``handler`` updated."""
        return self._with_property("handler", value)

    def with_params(self, value: Any) -> Tooltip:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)


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

    def with_asChrom(self, value: Any) -> TransformParams:
        """Return a copy with ``asChrom`` updated."""
        return self._with_property("asChrom", value)

    def with_asEnd(self, value: Any) -> TransformParams:
        """Return a copy with ``asEnd`` updated."""
        return self._with_property("asEnd", value)

    def with_asKey(self, value: Any) -> TransformParams:
        """Return a copy with ``asKey`` updated."""
        return self._with_property("asKey", value)

    def with_asMidpoint(self, value: Any) -> TransformParams:
        """Return a copy with ``asMidpoint`` updated."""
        return self._with_property("asMidpoint", value)

    def with_asStart(self, value: Any) -> TransformParams:
        """Return a copy with ``asStart`` updated."""
        return self._with_property("asStart", value)

    def with_asValue(self, value: Any) -> TransformParams:
        """Return a copy with ``asValue`` updated."""
        return self._with_property("asValue", value)

    def with_baseField(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` baseField."""
        return self._with_property("baseField", value, **kwargs)

    def with_cardinality(self, value: Any) -> TransformParams:
        """Return a copy with ``cardinality`` updated."""
        return self._with_property("cardinality", value)

    def with_channel(self, value: Any) -> TransformParams:
        """Return a copy with ``channel`` updated."""
        return self._with_property("channel", value)

    def with_chrom(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` chrom."""
        return self._with_property("chrom", value, **kwargs)

    def with_columnPadding(self, value: Any) -> TransformParams:
        """Return a copy with ``columnPadding`` updated."""
        return self._with_property("columnPadding", value)

    def with_columnRegex(self, value: Any) -> TransformParams:
        """Return a copy with ``columnRegex`` updated."""
        return self._with_property("columnRegex", value)

    def with_columns(self, value: Any) -> TransformParams:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_description(self, value: Any) -> TransformParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_direction(self, value: Any) -> TransformParams:
        """Return a copy with ``direction`` updated."""
        return self._with_property("direction", value)

    def with_ellipsis(self, value: Any) -> TransformParams:
        """Return a copy with ``ellipsis`` updated."""
        return self._with_property("ellipsis", value)

    def with_empty(self, value: Any) -> TransformParams:
        """Return a copy with ``empty`` updated."""
        return self._with_property("empty", value)

    def with_end(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` end."""
        return self._with_property("end", value, **kwargs)

    def with_exons(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` exons."""
        return self._with_property("exons", value, **kwargs)

    def with_expr(self, value: Any) -> TransformParams:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_fields(self, value: Any) -> TransformParams:
        """Return a copy with ``fields`` updated."""
        return self._with_property("fields", value)

    def with_font(self, value: Any) -> TransformParams:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(self, value: Any) -> TransformParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_groupby(self, value: Any) -> TransformParams:
        """Return a copy with ``groupby`` updated."""
        return self._with_property("groupby", value)

    def with_index(self, value: Any) -> TransformParams:
        """Return a copy with ``index`` updated."""
        return self._with_property("index", value)

    def with_labelOffset(self, value: Any) -> TransformParams:
        """Return a copy with ``labelOffset`` updated."""
        return self._with_property("labelOffset", value)

    def with_labelWidth(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` labelWidth."""
        return self._with_property("labelWidth", value, **kwargs)

    def with_lane(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` lane."""
        return self._with_property("lane", value, **kwargs)

    def with_limit(self, value: Any) -> TransformParams:
        """Return a copy with ``limit`` updated."""
        return self._with_property("limit", value)

    def with_offset(self, value: Any) -> TransformParams:
        """Return a copy with ``offset`` updated."""
        return self._with_property("offset", value)

    def with_ops(self, value: Any) -> TransformParams:
        """Return a copy with ``ops`` updated."""
        return self._with_property("ops", value)

    def with_padding(self, value: Any) -> TransformParams:
        """Return a copy with ``padding`` updated."""
        return self._with_property("padding", value)

    def with_param(self, value: Any) -> TransformParams:
        """Return a copy with ``param`` updated."""
        return self._with_property("param", value)

    def with_pos(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` pos."""
        return self._with_property("pos", value, **kwargs)

    def with_pos2(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` pos2."""
        return self._with_property("pos2", value, **kwargs)

    def with_preference(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` preference."""
        return self._with_property("preference", value, **kwargs)

    def with_preferredOrder(self, value: Any) -> TransformParams:
        """Return a copy with ``preferredOrder`` updated."""
        return self._with_property("preferredOrder", value)

    def with_regex(self, value: Any) -> TransformParams:
        """Return a copy with ``regex`` updated."""
        return self._with_property("regex", value)

    def with_rowPadding(self, value: Any) -> TransformParams:
        """Return a copy with ``rowPadding`` updated."""
        return self._with_property("rowPadding", value)

    def with_score(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` score."""
        return self._with_property("score", value, **kwargs)

    def with_separator(self, value: Any) -> TransformParams:
        """Return a copy with ``separator`` updated."""
        return self._with_property("separator", value)

    def with_size(self, value: Any) -> TransformParams:
        """Return a copy with ``size`` updated."""
        return self._with_property("size", value)

    def with_skipInvalidInput(self, value: Any) -> TransformParams:
        """Return a copy with ``skipInvalidInput`` updated."""
        return self._with_property("skipInvalidInput", value)

    def with_skipRegex(self, value: Any) -> TransformParams:
        """Return a copy with ``skipRegex`` updated."""
        return self._with_property("skipRegex", value)

    def with_sort(
        self,
        value: CompareParams | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``CompareParams`` sort."""
        return self._with_property("sort", value, **kwargs)

    def with_spacing(self, value: Any) -> TransformParams:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_start(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` start."""
        return self._with_property("start", value, **kwargs)

    def with_symbolOffset(self, value: Any) -> TransformParams:
        """Return a copy with ``symbolOffset`` updated."""
        return self._with_property("symbolOffset", value)

    def with_symbolSize(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` symbolSize."""
        return self._with_property("symbolSize", value, **kwargs)

    def with_symbolStrokeWidth(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` symbolStrokeWidth."""
        return self._with_property("symbolStrokeWidth", value, **kwargs)

    def with_type(self, value: Any) -> TransformParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_weight(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` weight."""
        return self._with_property("weight", value, **kwargs)

    def with_width(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TransformParams:
        """Return a copy with a ``Field`` width."""
        return self._with_property("width", value, **kwargs)

    def with_xOffset(self, value: Any) -> TransformParams:
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

    def with_yOffset(self, value: Any) -> TransformParams:
        """Return a copy with ``yOffset`` updated."""
        return self._with_property("yOffset", value)


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

    def with_description(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_ellipsis(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``ellipsis`` updated."""
        return self._with_property("ellipsis", value)

    def with_field(
        self,
        value: Field | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TruncateTextParams:
        """Return a copy with a ``Field`` field."""
        return self._with_property("field", value, **kwargs)

    def with_font(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``font`` updated."""
        return self._with_property("font", value)

    def with_fontSize(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``fontSize`` updated."""
        return self._with_property("fontSize", value)

    def with_fontStyle(
        self,
        value: FontStyle | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TruncateTextParams:
        """Return a copy with a ``FontStyle`` fontStyle."""
        return self._with_property("fontStyle", value, **kwargs)

    def with_fontWeight(
        self,
        value: FontWeight | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> TruncateTextParams:
        """Return a copy with a ``FontWeight`` fontWeight."""
        return self._with_property("fontWeight", value, **kwargs)

    def with_limit(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``limit`` updated."""
        return self._with_property("limit", value)

    def with_type(self, value: Any) -> TruncateTextParams:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)


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

    def with_axes(self, value: Any) -> UnitSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> UnitSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> UnitSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> UnitSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: Any) -> UnitSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``MarkType`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_name(self, value: Any) -> UnitSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: ViewOpacityDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``ViewOpacityDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> UnitSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> UnitSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> UnitSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_templates(self, value: Any) -> UnitSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> UnitSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_view(
        self,
        value: ViewBackground | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> UnitSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UnitSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_description(self, value: Any) -> UrlData:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_format(
        self,
        value: DataFormat | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlData:
        """Return a copy with a ``DataFormat`` format."""
        return self._with_property("format", value, **kwargs)

    def with_name(self, value: Any) -> UrlData:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(
        self,
        value: UrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlData:
        """Return a copy with a ``UrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)


class UrlGenomeConfig(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeConfig``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeConfig", {})

    def __init__(
        self, name: Any = Undefined, url: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(name=name, url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_name(self, value: Any) -> UrlGenomeConfig:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_url(self, value: Any) -> UrlGenomeConfig:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


class UrlGenomeDefinition(GenomeSpySchema):
    """Generated wrapper for ``UrlGenomeDefinition``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlGenomeDefinition", {})

    def __init__(self, url: Any = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_url(self, value: Any) -> UrlGenomeDefinition:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


class UrlImport(GenomeSpySchema):
    """Generated wrapper for ``UrlImport``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlImport", {})

    def __init__(self, url: Any = Undefined, **kwds: Any) -> None:
        super().__init__(url=url)
        if kwds:
            self._kwds.update(kwds)

    def with_url(self, value: Any) -> UrlImport:
        """Return a copy with ``url`` updated."""
        return self._with_property("url", value)


class UrlList(GenomeSpySchema):
    """Generated wrapper for ``UrlList``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("UrlList", {})

    def __init__(
        self, type: Any = Undefined, urlsFromFile: Any = Undefined, **kwds: Any
    ) -> None:
        super().__init__(type=type, urlsFromFile=urlsFromFile)
        if kwds:
            self._kwds.update(kwds)

    def with_type(self, value: Any) -> UrlList:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_urlsFromFile(self, value: Any) -> UrlList:
        """Return a copy with ``urlsFromFile`` updated."""
        return self._with_property("urlsFromFile", value)


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

    def with_attach(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_expr(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_field(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlSourceRef:
        """Return a copy with a ``FieldName`` field."""
        return self._with_property("field", value, **kwargs)

    def with_maxValues(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``template`` updated."""
        return self._with_property("template", value)

    def with_type(self, value: Any) -> UrlSourceRef:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_urlsFromFile(self, value: Any) -> UrlSourceRef:
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

    def with_attach(self, value: Any) -> UrlTemplate:
        """Return a copy with ``attach`` updated."""
        return self._with_property("attach", value)

    def with_field(
        self,
        value: FieldName | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> UrlTemplate:
        """Return a copy with a ``FieldName`` field."""
        return self._with_property("field", value, **kwargs)

    def with_maxValues(self, value: Any) -> UrlTemplate:
        """Return a copy with ``maxValues`` updated."""
        return self._with_property("maxValues", value)

    def with_onLoadError(self, value: Any) -> UrlTemplate:
        """Return a copy with ``onLoadError`` updated."""
        return self._with_property("onLoadError", value)

    def with_template(self, value: Any) -> UrlTemplate:
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

    def with_axes(self, value: Any) -> VConcatSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> VConcatSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> VConcatSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> VConcatSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_legends(self, value: Any) -> VConcatSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_name(self, value: Any) -> VConcatSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> VConcatSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> VConcatSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> VConcatSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: Any) -> VConcatSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_templates(self, value: Any) -> VConcatSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> VConcatSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(self, value: Any) -> VConcatSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> VConcatSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VConcatSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


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

    def with_description(self, value: Any) -> ValueDefNumber:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> ValueDefNumber:
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

    def with_description(self, value: Any) -> ValueDefString:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> ValueDefString:
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

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionStringNullType:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(self, value: Any) -> ValueDefWithConditionStringNullType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> ValueDefWithConditionStringNullType:
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

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefTypeForShape
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with a ``ConditionalMarkPropFieldDefTypeForShape`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(
        self, value: Any
    ) -> ValueDefWithConditionStringNullTypeForShape:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> ValueDefWithConditionStringNullTypeForShape:
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

    def with_condition(
        self,
        value: ConditionalMarkPropFieldDefType
        | dict[str, Any]
        | None
        | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ValueDefWithConditionNumberType:
        """Return a copy with a ``ConditionalMarkPropFieldDefType`` condition."""
        return self._with_property("condition", value, **kwargs)

    def with_description(self, value: Any) -> ValueDefWithConditionNumberType:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_title(self, value: Any) -> ValueDefWithConditionNumberType:
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

    def with_bind(
        self,
        value: Binding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VariableParameter:
        """Return a copy with a ``Binding`` bind."""
        return self._with_property("bind", value, **kwargs)

    def with_description(self, value: Any) -> VariableParameter:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_expr(self, value: Any) -> VariableParameter:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_name(self, value: Any) -> VariableParameter:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_persist(self, value: Any) -> VariableParameter:
        """Return a copy with ``persist`` updated."""
        return self._with_property("persist", value)

    def with_push(self, value: Any) -> VariableParameter:
        """Return a copy with ``push`` updated."""
        return self._with_property("push", value)

    def with_value(self, value: Any) -> VariableParameter:
        """Return a copy with ``value`` updated."""
        return self._with_property("value", value)


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

    def with_addChrPrefix(self, value: Any) -> VcfData:
        """Return a copy with ``addChrPrefix`` updated."""
        return self._with_property("addChrPrefix", value)

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VcfData:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

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

    def with_debounceMode(self, value: Any) -> VcfData:
        """Return a copy with ``debounceMode`` updated."""
        return self._with_property("debounceMode", value)

    def with_indexUrl(
        self,
        value: IndexUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VcfData:
        """Return a copy with a ``IndexUrlSourceRef`` indexUrl."""
        return self._with_property("indexUrl", value, **kwargs)

    def with_type(self, value: Any) -> VcfData:
        """Return a copy with ``type`` updated."""
        return self._with_property("type", value)

    def with_url(
        self,
        value: MultiUrlSourceRef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> VcfData:
        """Return a copy with a ``MultiUrlSourceRef`` url."""
        return self._with_property("url", value, **kwargs)

    def with_windowSize(self, value: Any) -> VcfData:
        """Return a copy with ``windowSize`` updated."""
        return self._with_property("windowSize", value)


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

    def with_fill(self, value: Any) -> ViewBackground:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: Any) -> ViewBackground:
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

    def with_stroke(self, value: Any) -> ViewBackground:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: Any) -> ViewBackground:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: Any) -> ViewBackground:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_strokeZindex(self, value: Any) -> ViewBackground:
        """Return a copy with ``strokeZindex`` updated."""
        return self._with_property("strokeZindex", value)

    def with_style(self, value: Any) -> ViewBackground:
        """Return a copy with ``style`` updated."""
        return self._with_property("style", value)

    def with_zindex(self, value: Any) -> ViewBackground:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_continuousHeight(self, value: Any) -> ViewConfig:
        """Return a copy with ``continuousHeight`` updated."""
        return self._with_property("continuousHeight", value)

    def with_continuousWidth(self, value: Any) -> ViewConfig:
        """Return a copy with ``continuousWidth`` updated."""
        return self._with_property("continuousWidth", value)

    def with_discreteHeight(
        self,
        value: Step | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``Step`` discreteHeight."""
        return self._with_property("discreteHeight", value, **kwargs)

    def with_discreteWidth(
        self,
        value: Step | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewConfig:
        """Return a copy with a ``Step`` discreteWidth."""
        return self._with_property("discreteWidth", value, **kwargs)

    def with_fill(self, value: Any) -> ViewConfig:
        """Return a copy with ``fill`` updated."""
        return self._with_property("fill", value)

    def with_fillOpacity(self, value: Any) -> ViewConfig:
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

    def with_step(self, value: Any) -> ViewConfig:
        """Return a copy with ``step`` updated."""
        return self._with_property("step", value)

    def with_stroke(self, value: Any) -> ViewConfig:
        """Return a copy with ``stroke`` updated."""
        return self._with_property("stroke", value)

    def with_strokeOpacity(self, value: Any) -> ViewConfig:
        """Return a copy with ``strokeOpacity`` updated."""
        return self._with_property("strokeOpacity", value)

    def with_strokeWidth(self, value: Any) -> ViewConfig:
        """Return a copy with ``strokeWidth`` updated."""
        return self._with_property("strokeWidth", value)

    def with_strokeZindex(self, value: Any) -> ViewConfig:
        """Return a copy with ``strokeZindex`` updated."""
        return self._with_property("strokeZindex", value)

    def with_zindex(self, value: Any) -> ViewConfig:
        """Return a copy with ``zindex`` updated."""
        return self._with_property("zindex", value)


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

    def with_channel(
        self,
        value: PrimaryPositionalChannel | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewOpacityDef:
        """Return a copy with a ``PrimaryPositionalChannel`` channel."""
        return self._with_property("channel", value, **kwargs)

    def with_expr(self, value: Any) -> ViewOpacityDef:
        """Return a copy with ``expr`` updated."""
        return self._with_property("expr", value)

    def with_unitsPerPixel(self, value: Any) -> ViewOpacityDef:
        """Return a copy with ``unitsPerPixel`` updated."""
        return self._with_property("unitsPerPixel", value)

    def with_values(self, value: Any) -> ViewOpacityDef:
        """Return a copy with ``values`` updated."""
        return self._with_property("values", value)


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

    def with_axes(self, value: Any) -> ViewSpec:
        """Return a copy with ``axes`` updated."""
        return self._with_property("axes", value)

    def with_baseUrl(self, value: Any) -> ViewSpec:
        """Return a copy with ``baseUrl`` updated."""
        return self._with_property("baseUrl", value)

    def with_columns(self, value: Any) -> ViewSpec:
        """Return a copy with ``columns`` updated."""
        return self._with_property("columns", value)

    def with_concat(self, value: Any) -> ViewSpec:
        """Return a copy with ``concat`` updated."""
        return self._with_property("concat", value)

    def with_config(
        self,
        value: GenomeSpyConfig | dict[str, Any] | None | Any = Undefined,
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
        value: Data | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``Data`` data."""
        return self._with_property("data", value, **kwargs)

    def with_description(self, value: Any) -> ViewSpec:
        """Return a copy with ``description`` updated."""
        return self._with_property("description", value)

    def with_domainInert(self, value: Any) -> ViewSpec:
        """Return a copy with ``domainInert`` updated."""
        return self._with_property("domainInert", value)

    def with_encoding(
        self,
        value: Encoding | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``Encoding`` encoding."""
        return self._with_property("encoding", value, **kwargs)

    def with_hconcat(self, value: Any) -> ViewSpec:
        """Return a copy with ``hconcat`` updated."""
        return self._with_property("hconcat", value)

    def with_height(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` height."""
        return self._with_property("height", value, **kwargs)

    def with_layer(self, value: Any) -> ViewSpec:
        """Return a copy with ``layer`` updated."""
        return self._with_property("layer", value)

    def with_legends(self, value: Any) -> ViewSpec:
        """Return a copy with ``legends`` updated."""
        return self._with_property("legends", value)

    def with_mark(
        self,
        value: MarkType | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``MarkType`` mark."""
        return self._with_property("mark", value, **kwargs)

    def with_multiscale(self, value: Any) -> ViewSpec:
        """Return a copy with ``multiscale`` updated."""
        return self._with_property("multiscale", value)

    def with_name(self, value: Any) -> ViewSpec:
        """Return a copy with ``name`` updated."""
        return self._with_property("name", value)

    def with_opacity(
        self,
        value: ViewOpacityDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``ViewOpacityDef`` opacity."""
        return self._with_property("opacity", value, **kwargs)

    def with_padding(
        self,
        value: PaddingConfig | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``PaddingConfig`` padding."""
        return self._with_property("padding", value, **kwargs)

    def with_params(self, value: Any) -> ViewSpec:
        """Return a copy with ``params`` updated."""
        return self._with_property("params", value)

    def with_resolve(self, value: Any) -> ViewSpec:
        """Return a copy with ``resolve`` updated."""
        return self._with_property("resolve", value)

    def with_scales(self, value: Any) -> ViewSpec:
        """Return a copy with ``scales`` updated."""
        return self._with_property("scales", value)

    def with_separator(
        self,
        value: SeparatorProps | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SeparatorProps`` separator."""
        return self._with_property("separator", value, **kwargs)

    def with_spacing(self, value: Any) -> ViewSpec:
        """Return a copy with ``spacing`` updated."""
        return self._with_property("spacing", value)

    def with_stops(
        self,
        value: MultiscaleStopsDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``MultiscaleStopsDef`` stops."""
        return self._with_property("stops", value, **kwargs)

    def with_templates(self, value: Any) -> ViewSpec:
        """Return a copy with ``templates`` updated."""
        return self._with_property("templates", value)

    def with_title(
        self,
        value: Title | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``Title`` title."""
        return self._with_property("title", value, **kwargs)

    def with_transform(self, value: Any) -> ViewSpec:
        """Return a copy with ``transform`` updated."""
        return self._with_property("transform", value)

    def with_vconcat(self, value: Any) -> ViewSpec:
        """Return a copy with ``vconcat`` updated."""
        return self._with_property("vconcat", value)

    def with_view(
        self,
        value: ViewBackground | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``ViewBackground`` view."""
        return self._with_property("view", value, **kwargs)

    def with_viewportHeight(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` viewportHeight."""
        return self._with_property("viewportHeight", value, **kwargs)

    def with_viewportWidth(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` viewportWidth."""
        return self._with_property("viewportWidth", value, **kwargs)

    def with_visible(self, value: Any) -> ViewSpec:
        """Return a copy with ``visible`` updated."""
        return self._with_property("visible", value)

    def with_width(
        self,
        value: SizeDef | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ViewSpec:
        """Return a copy with a ``SizeDef`` width."""
        return self._with_property("width", value, **kwargs)


class ZoomParams(GenomeSpySchema):
    """Generated wrapper for ``ZoomParams``."""

    _schema = _ROOT_SCHEMA.get("definitions", {}).get("ZoomParams", {})

    def __init__(self, extent: Any = Undefined, **kwds: Any) -> None:
        super().__init__(extent=extent)
        if kwds:
            self._kwds.update(kwds)

    def with_extent(
        self,
        value: ScalarDomain | dict[str, Any] | None | Any = Undefined,
        /,
        **kwargs: Any,
    ) -> ZoomParams:
        """Return a copy with a ``ScalarDomain`` extent."""
        return self._with_property("extent", value, **kwargs)


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
