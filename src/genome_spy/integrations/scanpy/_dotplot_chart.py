"""Native dotplot marks, slot labels, brackets and size/color guides."""

from __future__ import annotations

from math import isfinite
from numbers import Real
from typing import Any

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._colors import native_scheme
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup

_PT = 100 / 72
_FONT = "Lato"
_TICK = 10 * 0.833 * _PT


def _number(value: Any, name: str, *, minimum: float = 0) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not isfinite(value)
        or value < minimum
    ):
        raise ValueError(
            f"gsc.pl.dotplot: {name} must be a finite number >= {minimum}."
        )
    return float(value)


def dot_size_scale(
    fractions: np.ndarray, dot_min: float | None, dot_max: float | None, smallest: float
) -> tuple[list[float], list[float], list[float]]:
    """Map exact percentage values to areas, including clipped power scaling."""
    smallest = _number(smallest, "smallest_dot")
    if smallest > 200:
        raise ValueError(
            "gsc.pl.dotplot: smallest_dot cannot exceed the largest dot (200)."
        )
    valid = fractions[np.isfinite(fractions)]
    if not valid.size:
        raise ValueError("gsc.pl.dotplot: fractions need at least one finite value.")
    low = 0.0 if dot_min is None else _number(dot_min, "dot_min")
    high = (
        float(np.ceil(valid.max() * 10) / 10)
        if dot_max is None
        else _number(dot_max, "dot_max")
    )
    if low > 1 or high > 1 or high <= low:
        raise ValueError(
            "gsc.pl.dotplot: require 0 <= dot_min < dot_max <= 1. "
            "For all-zero fractions, set dot_max=1 explicitly."
        )
    difference = high - low
    step = 0.1 if 0.3 < difference <= 0.6 else 0.05 if difference <= 0.3 else 0.2
    ticks = np.arange(high, low, -step)[::-1]
    ticks = np.round(ticks * 100, 10) / 100
    # Explicit lookup keeps the clipped power mapping identical in dots and guides.
    domain = np.unique(np.concatenate([fractions[np.isfinite(fractions)], ticks]))
    areas = smallest + ((np.clip(domain, low, high) - low) / difference) ** 1.5 * (
        200 - smallest
    )
    return (domain * 100).tolist(), (areas * _PT**2).tolist(), (ticks * 100).tolist()


def _coordinate(
    channel: Any, field: str, count: int, padding: float, *, reverse: bool = False
) -> Any:
    return (
        channel(f"{field}:Q")
        .scale(
            domain=[-padding, count + padding],
            reverse=reverse,
            nice=False,
            zero=False,
            zoom=False,
        )
        .axis(None)
    )


def _slot_labels(labels: list[str], coordinate: Any, *, horizontal: bool) -> gs.Chart:
    table = [{"slot": i + 0.5, "label": label} for i, label in enumerate(labels)]
    if horizontal:
        return (
            gs.Chart(table)
            .mark_text(
                font=_FONT,
                size=_TICK,
                angle=-90,
                align="right",
                baseline="middle",
                dy=8,
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
            dx=-8,
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
    table = [
        {
            "start": group.start + 0.2,
            "end": group.end + 0.7,
            "slot": (group.start + group.end + 0.9) / 2,
            "label": group.label,
        }
        for group in groups
    ]
    ends = [{"slot": row[key]} for row in table for key in ("start", "end")]
    line = gs.Chart(table).mark_rule(
        color="black",
        size=1.5 * _PT,
        clip="never",
        tooltip=None,
        xOffset=4 if swapped else 0,
        x2Offset=4 if swapped else 0,
        yOffset=0 if swapped else -4,
        y2Offset=0 if swapped else -4,
    )
    caps = gs.Chart(ends).mark_rule(
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
        dx=8 if swapped else 0,
        dy=0 if swapped else -8,
        clip="never",
        tooltip=None,
    )
    if swapped:
        line = line.encode(
            y=coordinate.field("start"),
            y2=gs.Y2("end:Q"),
            x=gs.value(1),
            x2=gs.value(1),
        )
        caps = caps.encode(
            y=coordinate.field("slot"),
            y2=gs.Y2("slot:Q"),
            x=gs.value(1),
            x2=gs.value(1),
        )
        text = text.encode(y=coordinate.field("slot"), x=gs.value(1), text="label:N")
    else:
        line = line.encode(
            x=coordinate.field("start"),
            x2=gs.X2("end:Q"),
            y=gs.value(1),
            y2=gs.value(1),
        )
        caps = caps.encode(
            x=coordinate.field("slot"),
            x2=gs.X2("slot:Q"),
            y=gs.value(1),
            y2=gs.value(1),
        )
        text = text.encode(x=coordinate.field("slot"), y=gs.value(1), text="label:N")
    return [line, caps, text]


def build_dotplot(
    colors: pd.DataFrame,
    fractions: pd.DataFrame,
    feature_groups: tuple[FeatureGroup, ...],
    *,
    swap_axes: bool,
    title: str | None,
    colorbar_title: str | None,
    size_title: str | None,
    cmap: Any,
    vmin: float | None,
    vmax: float | None,
    dot_min: float | None,
    dot_max: float | None,
    smallest_dot: float,
    linewidth: float,
    rotation: float | None,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
) -> gs.TopLevelSpec:
    rows, columns = colors.shape
    scheme = native_scheme(
        "viridis" if cmap is None else cmap, "cmap", context="gsc.pl.dotplot"
    )
    linewidth = _number(linewidth, "linewidth")
    if rotation is not None:
        rotation = _number(rotation, "var_group_rotation", minimum=-360)
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                "gsc.pl.dotplot: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError("gsc.pl.dotplot: figsize needs (width, height) inches.")
        width = _number(figsize[0], "figsize width") * 100 - 150
        height = _number(figsize[1], "figsize height") * 100
    width = (
        columns * (35 if swap_axes else 37)
        if width is None
        else _number(width, "width")
    )
    height = (
        rows * (37 if swap_axes else 35)
        if height is None
        else _number(height, "height")
    )
    if width <= 0 or height <= 0:
        raise ValueError("gsc.pl.dotplot: plot width and height must be positive.")
    for name, value in {
        "title": title,
        "size_title": size_title,
        "colorbar_title": colorbar_title,
    }.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"gsc.pl.dotplot: {name} must be a string or None.")
    values = colors.to_numpy(dtype=float, na_value=np.nan)
    valid = values[np.isfinite(values)]
    if not valid.size:
        raise ValueError("gsc.pl.dotplot: colors need at least one finite value.")
    low = (
        float(valid.min())
        if vmin is None
        else _number(vmin, "vmin", minimum=-float("inf"))
    )
    high = (
        float(valid.max())
        if vmax is None
        else _number(vmax, "vmax", minimum=-float("inf"))
    )
    if low > high:
        raise ValueError("gsc.pl.dotplot: vmin cannot exceed vmax.")
    constant_color = low == high
    if constant_color:
        delta = abs(low) * 0.1 or 0.1
        low, high = low - delta, high + delta
    domain, areas, ticks = dot_size_scale(
        fractions.to_numpy(dtype=float, na_value=np.nan), dot_min, dot_max, smallest_dot
    )
    yy, xx = np.indices(colors.shape)
    table = pd.DataFrame(
        {
            "_x": xx.ravel() + 0.5,
            "_y": yy.ravel() + 0.5,
            "_mean": values.ravel(),
            "_percent": fractions.to_numpy(dtype=float, na_value=np.nan).ravel() * 100,
        }
    )
    if constant_color:
        # Scanpy freezes dot colors before its colorbar expands constant bounds.
        table["_paint"] = low
    x = _coordinate(gs.X, "_x", columns, 0.3)
    y = _coordinate(gs.Y, "_y", rows, 0.5, reverse=True)
    x_axis = x.axis(
        values=(np.arange(columns) + 0.5).tolist(),
        labels=False,
        title=None,
        domain=False,
        tickColor="black",
        tickSize=3.5 * _PT,
        tickWidth=0.8 * _PT,
    )
    y_axis = y.axis(
        values=(np.arange(rows) + 0.5).tolist(),
        labels=False,
        title=None,
        domain=False,
        tickColor="black",
        tickSize=3.5 * _PT,
        tickWidth=0.8 * _PT,
    )
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    if len(set(ylabels if not swap_axes else xlabels)) != (
        rows if not swap_axes else columns
    ):
        raise ValueError(
            "gsc.pl.dotplot: group labels collide when serialized as strings."
        )
    bracket_space = (
        max((len(g.label) for g in feature_groups), default=0) * _TICK * 0.65 + 12
    )
    guide_offset = bracket_space + 12 if feature_groups and swap_axes else 12
    dots = (
        gs.Chart(table)
        .transform_filter("isValid(datum._mean) && isValid(datum._percent)")
        .mark_point(
            filled=True,
            stroke="black",
            strokeWidth=linewidth * _PT,
            inwardStroke=False,
            tooltip=None,
        )
        .encode(
            x=x_axis,
            y=y_axis,
            color=gs.Color("_paint:Q" if constant_color else "_mean:Q")
            .scale(
                type="linear",
                domain=[low, high],
                nice=False,
                zero=False,
                clamp=True,
                scheme=scheme,
            )
            .legend(
                gs.Legend(
                    title=colorbar_title.replace("\n", " ")
                    if colorbar_title
                    else colorbar_title,
                    orient="right",
                    direction="horizontal",
                    gradientLength=150,
                    gradientThickness=15,
                    offset=guide_offset,
                )
            ),
            size=gs.Size("_percent:Q")
            .scale(type="ordinal", domain=domain, range=areas)
            .legend(
                gs.Legend(
                    title=size_title.replace("\n", " ") if size_title else size_title,
                    orient="right",
                    direction="horizontal",
                    columns=len(ticks),
                    values=ticks,
                    symbolFillColor="gray",
                    symbolStrokeColor="black",
                    symbolStrokeWidth=linewidth * _PT,
                    offset=guide_offset,
                )
            ),
        )
    )
    if smallest_dot == 0:
        # A zero-area dot must not leave a stroke-only picking/raster footprint.
        dots = dots.transform_filter(f"datum._percent > {100 * (dot_min or 0)}")
    layers: list[gs.Chart] = [
        dots,
        _slot_labels(xlabels, x, horizontal=True),
        _slot_labels(ylabels, y, horizontal=False),
    ]
    if feature_groups:
        layers.extend(
            _brackets(
                feature_groups,
                y if swap_axes else x,
                swapped=swap_axes,
                rotation=rotation,
            )
        )
    chart = gs.layer(*layers).properties(
        width=width,
        height=height,
        padding={
            "left": max(map(len, ylabels)) * _TICK * 0.65 + 12,
            "bottom": max(map(len, xlabels)) * _TICK * 0.65 + 12,
            "top": bracket_space if feature_groups and not swap_axes else 10,
            "right": 10,
        },
    )
    if title:
        chart = chart.properties(
            title=gs.title(
                title,
                font=_FONT,
                fontSize=12 * _PT,
                offset=bracket_space + 10 if feature_groups and not swap_axes else 10,
            )
        )
    return chart.configure_view(stroke="black", strokeWidth=0.8 * _PT).configure_legend(
        labelFont=_FONT,
        labelFontSize=_TICK,
        titleFont=_FONT,
        titleFontSize=_TICK,
        titleFontWeight="normal",
        layout={"anchor": "end", "direction": "vertical", "wrap": False},
        spacing=25,
    )
