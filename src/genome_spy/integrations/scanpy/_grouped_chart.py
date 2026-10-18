"""Native index slots, labels and layout shared by grouped expression plots."""

from __future__ import annotations

from math import isfinite
from numbers import Real
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData

_PT = 100 / 72
_FONT = "Lato"
_TICK = 10 * 0.833 * _PT


def number(value: Any, name: str, *, context: str, minimum: float = 0) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not isfinite(value)
        or value < minimum
    ):
        raise ValueError(f"{context}: {name} must be a finite number >= {minimum}.")
    return float(value)


def coordinate(
    channel: Any, field: str, count: int, padding: float, *, reverse: bool = False
) -> Any:
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


def _slot_labels(labels: list[str], coordinate: Any, *, horizontal: bool) -> gs.Chart:
    table = [{"slot": i, "label": label} for i, label in enumerate(labels)]
    if horizontal:
        return (
            gs.Chart(table)
            .mark_text(
                font=_FONT,
                size=_TICK,
                angle=-90,
                align="right",
                baseline="middle",
                yOffset=8,
                clip="never",
                tooltip=None,
            )
            .encode(x=coordinate.field("slot"), y=gs.value(0), text="label:N")
        )
    return (
        gs.Chart(table)
        .mark_text(
            font=_FONT,
            size=_TICK,
            align="right",
            baseline="middle",
            xOffset=-8,
            clip="never",
            tooltip=None,
        )
        .encode(x=gs.value(0), y=coordinate.field("slot"), text="label:N")
    )


def _brackets(
    groups: tuple[FeatureGroup, ...],
    coordinate: Any,
    *,
    swapped: bool,
    rotation: float | None,
) -> list[gs.Chart]:
    # Keep index spans half-open while retaining Scanpy's asymmetric bracket ends.
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
    line = gs.Chart(table).mark_rule(
        color="black",
        size=1.5 * _PT,
        clip="never",
        tooltip=None,
        xOffset=4 if swapped else 0,
        x2Offset=4 if swapped else gs.expr("-0.3 * bandwidth('x') * width"),
        yOffset=0 if swapped else -4,
        y2Offset=gs.expr("-0.3 * bandwidth('y') * height") if swapped else -4,
    )
    caps = gs.Chart(table).mark_rule(
        color="black",
        size=1.5 * _PT,
        clip="never",
        tooltip=None,
        x2Offset=4 if swapped else 0,
        y2Offset=0 if swapped else -4,
    )
    if rotation is None:
        rotation = (
            270 if swapped else 90 if any(len(g.label) > 4 for g in groups) else 0
        )
    text = gs.Chart(table).mark_text(
        font=_FONT,
        size=_TICK,
        angle=-rotation,
        align="left" if not swapped and rotation == 90 else "center",
        baseline="middle" if rotation else "bottom",
        # Positional offsets stay outside the plot when the text rotates.
        xOffset=16 if swapped else 0,
        yOffset=0 if swapped else -8,
        clip="never",
        tooltip=None,
    )
    if swapped:
        line = line.encode(
            y=coordinate.field("start").band(0.2),
            y2=gs.Y2("stop:I").band(0),
            x=gs.value(1),
            x2=gs.value(1),
        )
        left = caps.encode(
            y=coordinate.field("start").band(0.2),
            y2=gs.Y2("start:I").band(0.2),
            x=gs.value(1),
            x2=gs.value(1),
        )
        right = left.encode(
            y=coordinate.field("end").band(0.7), y2=gs.Y2("end:I").band(0.7)
        )
        text = text.encode(
            y=coordinate.field("slot").band(0),
            yOffset=gs.YOffset(
                gs.expr("datum.band * bandwidth('y') * height"), type="quantitative"
            ).scale(None),
            x=gs.value(1),
            text="label:N",
        )
    else:
        line = line.encode(
            x=coordinate.field("start").band(0.2),
            x2=gs.X2("stop:I").band(0),
            y=gs.value(1),
            y2=gs.value(1),
        )
        left = caps.encode(
            x=coordinate.field("start").band(0.2),
            x2=gs.X2("start:I").band(0.2),
            y=gs.value(1),
            y2=gs.value(1),
        )
        right = left.encode(
            x=coordinate.field("end").band(0.7), x2=gs.X2("end:I").band(0.7)
        )
        text = text.encode(
            x=coordinate.field("slot").band(0),
            xOffset=gs.XOffset(
                gs.expr("datum.band * bandwidth('x') * width"), type="quantitative"
            ).scale(None),
            y=gs.value(1),
            text="label:N",
        )
    return [line, left, right, text]


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
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{context}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{context}: figsize needs (width, height) inches.")
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


def color_bounds(
    values: np.ndarray, vmin: float | None, vmax: float | None, *, context: str
) -> tuple[float, float, bool]:
    valid = values[np.isfinite(values)]
    if not valid.size:
        raise ValueError(f"{context}: colors need at least one finite value.")
    low = (
        float(valid.min())
        if vmin is None
        else number(vmin, "vmin", minimum=-float("inf"), context=context)
    )
    high = (
        float(valid.max())
        if vmax is None
        else number(vmax, "vmax", minimum=-float("inf"), context=context)
    )
    if low > high:
        raise ValueError(f"{context}: vmin cannot exceed vmax.")
    constant = low == high
    if constant:
        delta = abs(low) * 0.1 or 0.1
        low, high = low - delta, high + delta
    return low, high, constant


def summary_records(
    colors: pd.DataFrame, *, swap_axes: bool, context: str
) -> pd.DataFrame:
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    groups = xlabels if swap_axes else ylabels
    if len(set(groups)) != len(groups):
        raise ValueError(f"{context}: group labels collide when serialized as strings.")
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
    return max((len(g.label) for g in groups), default=0) * _TICK * 0.65 + 12


def guide_offset(
    groups: tuple[FeatureGroup, ...], *, swap_axes: bool, tree: bool = False
) -> float:
    return (
        12
        + (bracket_space(groups) if groups and swap_axes else 0)
        + (88 if tree and not swap_axes else 0)
    )


def color_legend(
    title: str | None,
    groups: tuple[FeatureGroup, ...],
    *,
    swap_axes: bool,
    tree: bool = False,
) -> gs.Legend:
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
    marks: gs.Chart,
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
) -> gs.TopLevelSpec:
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    layers: list[gs.Chart | gs.LayerChart] = [
        marks,
        _slot_labels(xlabels, x.axis(None), horizontal=True),
        _slot_labels(ylabels, y.axis(None), horizontal=False),
    ]
    if groups:
        layers.extend(
            _brackets(
                groups, y if swap_axes else x, swapped=swap_axes, rotation=rotation
            )
        )
    if tree is not None:
        from genome_spy.integrations.scanpy._dendrogram_chart import tree_overlay

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
            )
        )
    space = bracket_space(groups)
    top_space = (
        98
        if tree is not None and swap_axes
        else space
        if groups and not swap_axes
        else 10
    )
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
