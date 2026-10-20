"""Native index slots, labels and layout shared by grouped expression plots."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from collections.abc import Sequence

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._dendrogram_chart import tree_overlay
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup
from genome_spy.integrations.scanpy._grid_interactions import (
    index_offset,
    slot_position,
    visible_slots,
    with_navigation,
)
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
)

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData


def coordinate(
    channel: Any, field: str, count: int, padding: float, *, reverse: bool = False
) -> Any:
    """Return an index position encoding from a field, count and outer padding.

    Use integer positions so repeated labels remain separate and layers align.
    """
    return (
        channel(f"{field}:I")
        .scale(
            domain=[0, count - 1],
            paddingOuter=padding,
            reverse=reverse,
            zoom=False,
        )
        .axis(None)
    )


def _slot_labels(
    labels: list[str],
    coordinate: Any,
    *,
    horizontal: bool,
    zoom: bool = False,
    opposite: bool = False,
    in_bounds: bool = False,
    positions: Sequence[float] | None = None,
) -> gs.Chart:
    """Return a text layer placing labels at the supplied row or column positions.

    Separate text avoids merging repeated names into a single axis tick.
    """
    table = [{"slot": i, "label": label} for i, label in enumerate(labels)]
    if positions is not None:
        table = [
            {"slot": int(np.floor(slot)), "fraction": slot % 1, "label": label}
            for slot, label in zip(positions, labels, strict=True)
        ]
    chart = gs.Chart(table)
    if zoom and not in_bounds:
        chart = visible_slots(chart, "x" if horizontal else "y", "datum.slot + 0.5")
    if positions is not None:
        axis = "x" if horizontal else "y"
        chart = chart.encode(**{f"{axis}Offset": index_offset(axis, "fraction")})
    space = max(map(len, labels), default=0) * _TICK * 0.65 + 12
    if horizontal:
        chart = chart.mark_text(
            font=_FONT,
            size=_TICK,
            angle=-90,
            align="right",
            baseline="middle",
            yOffset=8,
            clip=True if in_bounds else "never",
            tooltip=None,
        ).encode(
            x=coordinate.field("slot"),
            y=gs.value(1 if in_bounds else 0),
            text="label:N",
        )
        return chart.properties(height=space) if in_bounds else chart
    chart = chart.mark_text(
        font=_FONT,
        size=_TICK,
        align="left" if opposite else "right",
        baseline="middle",
        xOffset=8 if opposite else -8,
        clip=True if in_bounds else "never",
        tooltip=None,
    ).encode(
        x=gs.value(0 if opposite else 1)
        if in_bounds
        else gs.value(1 if opposite else 0),
        y=coordinate.field("slot"),
        text="label:N",
    )
    return chart.properties(width=space) if in_bounds else chart


def _brackets(
    groups: tuple[FeatureGroup, ...],
    coordinate: Any,
    *,
    swapped: bool,
    rotation: float | None,
    end_band: float = 0.7,
    zoom: bool = False,
    in_bounds: bool = False,
) -> list[gs.Chart]:
    """Return rule and text layers for marker groups at the supplied positions.

    Match bracket spans and label placement in either plot orientation.
    """
    # Place brackets by gene position so repeated names stay separate.
    table = [
        {
            "start": group.start,
            "end": group.end,
            "stop": group.end + 1,
            "slot": (group.start + group.end) // 2,
            "band": 0.45 + (group.start + group.end) % 2 / 2,
            "label": group.label,
        }
        for group in groups
    ]
    axis, extent = ("y", "height") if swapped else ("x", "width")
    end_offset = (
        0
        if in_bounds
        else gs.expr(f"{end_band - 1:g} * bandwidth('{axis}') * {extent}")
    )
    edge = gs.value(0 if in_bounds else 1)
    chart = gs.Chart(table)
    # Links anchor both bracket endpoints to their slots across gaps.
    draw = chart.mark_link if in_bounds else chart.mark_rule
    mark_options: dict[str, Any] = {"linkShape": "line"} if in_bounds else {}
    line = draw(
        color="black",
        size=1.5 * _PT,
        clip=True if in_bounds else "never",
        tooltip=None,
        xOffset=4 if swapped else 0,
        x2Offset=4 if swapped else end_offset,
        yOffset=0 if swapped else -4,
        y2Offset=end_offset if swapped else -4,
        **mark_options,
    )
    caps = draw(
        color="black",
        size=1.5 * _PT,
        clip=True if in_bounds else "never",
        tooltip=None,
        x2Offset=4 if swapped else 0,
        y2Offset=0 if swapped else -4,
        **mark_options,
    )
    if rotation is None:
        # Long labels need rotation to clear neighboring brackets.
        rotation = 0
        if swapped:
            rotation = 270
        elif any(len(g.label) > 4 for g in groups):
            rotation = 90
    text = gs.Chart(table).mark_text(
        font=_FONT,
        size=_TICK,
        angle=-rotation,
        align="left" if not swapped and rotation == 90 else "center",
        baseline="middle" if rotation else "bottom",
        # Offsets keep the label clear of the bracket after rotation.
        xOffset=16 if swapped else 0,
        yOffset=0 if swapped else -8,
        clip=True if in_bounds else "never",
        tooltip=None,
    )
    if swapped:
        line = line.encode(
            y=coordinate.field("start").band(0.2),
            y2=gs.Y2("end:I").band(end_band) if in_bounds else gs.Y2("stop:I").band(0),
            x=edge,
            x2=edge,
        )
        left = caps.encode(
            y=coordinate.field("start").band(0.2),
            y2=gs.Y2("start:I").band(0.2),
            x=edge,
            x2=edge,
        )
        right = left.encode(
            y=coordinate.field("end").band(end_band), y2=gs.Y2("end:I").band(end_band)
        )
        text = text.encode(
            y=coordinate.field("slot").band(0),
            yOffset=gs.YOffset(
                gs.expr("datum.band * bandwidth('y') * height"), type="quantitative"
            ).scale(None),
            x=edge,
            text="label:N",
        )
    else:
        line = line.encode(
            x=coordinate.field("start").band(0.2),
            x2=gs.X2("end:I").band(end_band) if in_bounds else gs.X2("stop:I").band(0),
            y=edge,
            y2=edge,
        )
        left = caps.encode(
            x=coordinate.field("start").band(0.2),
            x2=gs.X2("start:I").band(0.2),
            y=edge,
            y2=edge,
        )
        right = left.encode(
            x=coordinate.field("end").band(end_band), x2=gs.X2("end:I").band(end_band)
        )
        text = text.encode(
            x=coordinate.field("slot").band(0),
            xOffset=gs.XOffset(
                gs.expr("datum.band * bandwidth('x') * width"), type="quantitative"
            ).scale(None),
            y=edge,
            text="label:N",
        )
    layers = [line, left, right, text]
    if zoom and in_bounds:
        predicate = (
            "scale('y', datum.end) - bandwidth('y') >= 0 && scale('y', datum.start) <= 1"
            if swapped
            else "scale('x', datum.start) >= 0 && scale('x', datum.end) + bandwidth('x') <= 1"
        )
        layers = [chart.transform_filter(predicate) for chart in layers]
    elif zoom:
        axis = "y" if swapped else "x"
        layers = [
            visible_slots(chart, axis, "datum.start", "datum.end + 1")
            for chart in layers
        ]
    return layers


def plot_dimensions(
    rows: int,
    columns: int,
    *,
    swap_axes: bool,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    context: str,
) -> tuple[float, float]:
    """Return plot width and height from table shape and optional size overrides.

    Convert figsize to pixels while reserving space for guides.
    """
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{context}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{context}: figsize needs (width, height) inches.")
        # The overall figure width also includes space for the guides.
        width = number(figsize[0], "figsize width", context=context) * 100 - 150
        height = number(figsize[1], "figsize height", context=context) * 100
    width = (
        columns * (35 if swap_axes else 37)
        if width is None
        else number(width, "width", context=context)
    )
    height = (
        rows * (37 if swap_axes else 35)
        if height is None
        else number(height, "height", context=context)
    )
    if width <= 0 or height <= 0:
        raise ValueError(f"{context}: plot width and height must be positive.")
    return width, height


def summary_records(
    colors: pd.DataFrame, *, swap_axes: bool, context: str
) -> pd.DataFrame:
    """Turn a displayed summary matrix into rows for plotting and hover.

    Return positions, gene/group labels and values, keeping repeated genes separate.
    """
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    groups = xlabels if swap_axes else ylabels
    if len(set(groups)) != len(groups):
        raise ValueError(f"{context}: group labels collide when serialized as strings.")
    # Use positions so repeated gene names remain distinct chart entries.
    yy, xx = np.indices(colors.shape)
    return pd.DataFrame(
        {
            "_x": xx.ravel(),
            "_y": yy.ravel(),
            "_gene": np.asarray(ylabels if swap_axes else xlabels)[
                (yy if swap_axes else xx).ravel()
            ],
            "_group": np.asarray(groups)[(xx if swap_axes else yy).ravel()],
            "_mean": colors.to_numpy(dtype=float, na_value=np.nan).ravel(),
        }
    )


def bracket_space(groups: tuple[FeatureGroup, ...]) -> float:
    """Estimate space in pixels for marker-group labels so they clear the plot."""
    return max((len(g.label) for g in groups), default=0) * _TICK * 0.65 + 12


def feature_gaps(groups: tuple[FeatureGroup, ...], count: int) -> list[int]:
    """Return internal cuts when marker spans partition all feature slots.

    Arbitrary or overlapping brackets do not define grouping gaps.
    """
    ordered = sorted(groups, key=lambda group: group.start)
    ends = [int(group.end) + 1 for group in ordered]
    starts = [group.start for group in ordered]
    return ends[:-1] if ends and ends[-1] == count and starts == [0, *ends[:-1]] else []


def guide_offset(
    groups: tuple[FeatureGroup, ...], *, swap_axes: bool, tree: bool = False
) -> float:
    """Return guide spacing in pixels, allowing for marker brackets and a tree."""
    return (
        12
        + (bracket_space(groups) if groups and swap_axes else 0)
        + (80 if tree and not swap_axes else 0)
    )


def color_legend(
    title: str | None,
    groups: tuple[FeatureGroup, ...],
    *,
    swap_axes: bool,
    tree: bool = False,
) -> gs.Legend:
    """Return a color guide from its title and neighboring bracket/tree layout.

    Keep dotplot and matrixplot guides consistent and clear of annotations.
    """
    return gs.Legend(
        title=title.replace("\n", " ") if title else title,
        orient="right",
        direction="horizontal",
        gradientLength=150,
        gradientThickness=15,
        offset=guide_offset(groups, swap_axes=swap_axes, tree=tree),
    )


def grouped_axes(
    rows: int, columns: int, *, xpadding: float, ypadding: float
) -> tuple[Any, Any]:
    """Return x/y encodings from table shape and padding, with fixed index ticks.

    Reverse row positions so the first matrix row appears at the top.
    """
    axes = []
    for channel, field, count, padding, reverse in [
        (gs.X, "_x", columns, xpadding, False),
        (gs.Y, "_y", rows, ypadding, True),
    ]:
        axes.append(
            coordinate(channel, field, count, padding, reverse=reverse).axis(
                values=list(range(count)),
                labels=False,
                title=None,
                domain=False,
                tickColor="black",
                tickSize=3.5 * _PT,
                tickWidth=0.8 * _PT,
            )
        )
    return axes[0], axes[1]


def finish_grouped_chart(
    marks: Sequence[gs.Chart | gs.LayerChart],
    colors: pd.DataFrame,
    groups: tuple[FeatureGroup, ...],
    x: Any,
    y: Any,
    *,
    swap_axes: bool,
    rotation: float | None,
    title: str | None,
    width: float,
    height: float,
    frame_width: float,
    tree: DendrogramData | None = None,
    zoom: bool = False,
) -> gs.TopLevelSpec:
    """Combine summary marks, table labels and optional brackets/tree into a chart.

    Use the supplied axes and size to align layers and leave room for annotations.
    """
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    # Draw labels separately so repeated names do not collapse into one axis tick.
    layers: list[gs.Chart | gs.LayerChart] = [
        *marks,
        _slot_labels(xlabels, x.axis(None), horizontal=True, zoom=zoom),
        _slot_labels(ylabels, y.axis(None), horizontal=False, zoom=zoom),
    ]
    if groups:
        layers.extend(
            _brackets(
                groups,
                y if swap_axes else x,
                swapped=swap_axes,
                rotation=rotation,
                zoom=zoom,
            )
        )

    # Tree leaves must use the same row or column spacing as the matrix.
    if tree is not None:
        padding = (
            x.to_dict()["scale"]["paddingOuter"]
            if swap_axes
            else y.to_dict()["scale"]["paddingOuter"]
        )
        layers.append(
            tree_overlay(
                tree,
                orientation="top" if swap_axes else "right",
                padding=padding,
                reverse=not swap_axes,
                leaf_projection=slot_position(
                    "x" if swap_axes else "y", "datum.{field}"
                )
                if zoom
                else None,
            )
        )

    # Leave room above the plot for either a tree or marker brackets.
    top_space = 10.0
    if tree is not None and swap_axes:
        top_space = 90
    elif groups and not swap_axes:
        top_space = bracket_space(groups)
    chart = gs.layer(*layers).properties(
        width=width,
        height=height,
        padding={
            "left": max(map(len, ylabels)) * _TICK * 0.65 + 12,
            "bottom": max(map(len, xlabels)) * _TICK * 0.65 + 12,
            "top": top_space,
            "right": 10,
        },
    )
    if title:
        chart = chart.properties(
            title=gs.title(
                title,
                font=_FONT,
                fontSize=12 * _PT,
                offset=top_space + 10 if top_space > 10 else 10,
            )
        )
    chart = with_navigation(chart, enabled=zoom)
    return chart.configure_view(
        stroke="black", strokeWidth=frame_width * _PT
    ).configure_legend(
        labelFont=_FONT,
        labelFontSize=_TICK,
        titleFont=_FONT,
        titleFontSize=_TICK,
        titleFontWeight="normal",
        titleOrient="top",
        layout={"anchor": "end", "direction": "vertical", "wrap": False},
        spacing=25,
    )
