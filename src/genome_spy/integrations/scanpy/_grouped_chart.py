"""Native index slots, labels and layout shared by grouped expression plots."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal
from collections.abc import Sequence

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup
from genome_spy.integrations.scanpy._grid_interactions import index_offset
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
)

if TYPE_CHECKING:
    from genome_spy.schema._kwds import ScalesKwds
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
    opposite: bool = False,
    positions: Sequence[float] | None = None,
    font_size: float = _TICK,
    clip: bool | Literal["x", "y"] = True,
) -> gs.Chart:
    """Return a side view placing labels at the supplied row or column positions.

    Separate text avoids merging repeated names into a single axis tick.
    """
    table = [{"slot": i, "label": label} for i, label in enumerate(labels)]
    if positions is not None:
        table = [
            {"slot": int(np.floor(slot)), "fraction": slot % 1, "label": label}
            for slot, label in zip(positions, labels, strict=True)
        ]
    chart = gs.Chart(table)
    if positions is not None:
        axis = "x" if horizontal else "y"
        chart = chart.encode(**{f"{axis}Offset": index_offset(axis, "fraction")})
    space = max(map(len, labels), default=0) * font_size * 0.65 + 12
    if horizontal:
        chart = chart.mark_text(
            font=_FONT,
            size=font_size,
            angle=-90,
            align="left" if opposite else "right",
            baseline="middle",
            yOffset=-8 if opposite else 8,
            clip=clip,
            tooltip=None,
        ).encode(
            x=coordinate.field("slot"),
            y=gs.value(0 if opposite else 1),
            text="label:N",
        )
        return chart.properties(height=space)
    chart = chart.mark_text(
        font=_FONT,
        size=font_size,
        align="left" if opposite else "right",
        baseline="middle",
        xOffset=8 if opposite else -8,
        clip=clip,
        tooltip=None,
    ).encode(
        x=gs.value(0 if opposite else 1),
        y=coordinate.field("slot"),
        text="label:N",
    )
    return chart.properties(width=space)


def _brackets(
    groups: tuple[FeatureGroup, ...],
    coordinate: Any,
    *,
    swapped: bool,
    rotation: float | None,
    end_band: float = 0.7,
    zoom: bool = False,
) -> list[gs.Chart]:
    """Return native rules and labels for marker groups at the supplied positions.

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
    edge = gs.value(0)
    chart = gs.Chart(table)
    # A span ends before the next slot's gap; caps use single slot anchors.
    axis, extent = ("y", "height") if swapped else ("x", "width")
    end_offset = gs.expr(f"{end_band - 1:g} * bandwidth('{axis}') * {extent}")
    line = chart.mark_rule(
        color="black",
        size=1.5 * _PT,
        clip=True,
        tooltip=None,
        xOffset=4 if swapped else 0,
        x2Offset=4 if swapped else end_offset,
        yOffset=0 if swapped else -4,
        y2Offset=end_offset if swapped else -4,
    )
    caps = chart.mark_rule(
        color="black",
        size=1.5 * _PT,
        clip=True,
        tooltip=None,
        x2Offset=4 if swapped else 0,
        y2Offset=0 if swapped else -4,
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
        clip=True,
        tooltip=None,
    )
    if swapped:
        line = line.encode(
            y=coordinate.field("start").band(0.2),
            y2=gs.Y2("stop:I").band(0),
            x=edge,
            x2=edge,
        )
        left = caps.encode(
            y=coordinate.field("start").band(0.2),
            x=edge,
            x2=edge,
        )
        right = left.encode(y=coordinate.field("end").band(end_band))
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
            x2=gs.X2("stop:I").band(0),
            y=edge,
            y2=edge,
        )
        left = caps.encode(
            x=coordinate.field("start").band(0.2),
            y=edge,
            y2=edge,
        )
        right = left.encode(x=coordinate.field("end").band(end_band))
        text = text.encode(
            x=coordinate.field("slot").band(0),
            xOffset=gs.XOffset(
                gs.expr("datum.band * bandwidth('x') * width"), type="quantitative"
            ).scale(None),
            y=edge,
            text="label:N",
        )
    layers = [line, left, right, text]
    if zoom:
        predicate = (
            "scale('y', datum.end) - bandwidth('y') >= 0 && scale('y', datum.start) <= 1"
            if swapped
            else "scale('x', datum.start) >= 0 && scale('x', datum.end) + bandwidth('x') <= 1"
        )
        layers = [chart.transform_filter(predicate) for chart in layers]
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


def index_scales(
    x: Any, y: Any, *, xgaps: Sequence[int] = (), ygaps: Sequence[int] = ()
) -> ScalesKwds:
    """Move the supplied index definitions to a surround's shared scale owner.

    Native four-pixel gaps keep every aligned track on the same slot positions.
    """
    return gs.scales(
        x=gs.Scale(
            type="index",
            **x.scale(gapPositions=list(xgaps), gapWidth=4).to_dict()["scale"],
        ),
        y=gs.Scale(
            type="index",
            **y.scale(gapPositions=list(ygaps), gapWidth=4).to_dict()["scale"],
        ),
    )


def color_legend(title: str | None) -> gs.Legend:
    """Return a native color guide; surround layout reserves its track space."""
    return gs.Legend(
        title=title.replace("\n", " ") if title else title,
        orient="right",
        direction="horizontal",
        gradientLength=150,
        gradientThickness=15,
        offset=12,
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
    center: gs.LayerChart,
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
    scales: ScalesKwds,
    name: str,
    tree: DendrogramData | None = None,
    zoom: bool = False,
) -> gs.TopLevelSpec:
    """Combine summary marks, table labels and optional brackets/tree into a chart.

    Use the supplied axes and size to align layers and leave room for annotations.
    """
    xlabels, ylabels = [str(v) for v in colors.columns], [str(v) for v in colors.index]
    center = center.properties(
        width=width,
        height=height,
        name=f"{name}-cells",
    )
    # Each annotation owns a viewport and inherits the center's aligned scale.
    sides: dict[str, Any] = {
        "bottom": [_slot_labels(xlabels, x.axis(None), horizontal=True)],
        "left": [_slot_labels(ylabels, y.axis(None), horizontal=False)],
    }
    if groups:
        brackets = gs.layer(
            *_brackets(
                groups,
                (y if swap_axes else x).axis(None),
                swapped=swap_axes,
                rotation=rotation,
                zoom=zoom,
            )
        )
        brackets = brackets.properties(name=f"{name}-brackets")
        sides["right" if swap_axes else "top"] = [
            brackets.properties(width=bracket_space(groups))
            if swap_axes
            else brackets.properties(height=bracket_space(groups))
        ]
    if tree is not None:
        count = len(xlabels) if swap_axes else len(ylabels)
        sides["top" if swap_axes else "right"] = [
            tree_track(
                tree, list(range(count)), horizontal=swap_axes, size=80
            ).properties(name=f"{name}-tree")
        ]
    chart = gs.surround(
        center, surround=gs.SurroundSides(**sides), spacing=0
    ).properties(scales=scales)
    if title:
        chart = chart.properties(
            title=gs.title(title, font=_FONT, fontSize=12 * _PT, offset=10)
        )
    return (
        chart.resolve_legend(color="collected", size="collected")
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_legend(
            labelFont=_FONT,
            labelFontSize=_TICK,
            titleFont=_FONT,
            titleFontSize=_TICK,
            titleFontWeight="normal",
            titleOrient="top",
            layout={"anchor": "end", "direction": "vertical", "wrap": False},
            spacing=25,
        )
    )
