"""Native clustered tiles with two attached trees and ordered color tracks."""

from math import ceil
from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._clustermap_data import ClusteredMatrix, CONTEXT
from genome_spy.integrations.scanpy._data import number, numeric_values
from genome_spy.integrations.scanpy._dendrogram_chart import tree_overlay
from genome_spy.integrations.scanpy._grouped_chart import coordinate, _slot_labels
from genome_spy.integrations.scanpy._grid_interactions import (
    slot_position,
    zoom_axes,
    with_navigation,
    with_values,
)
from genome_spy.integrations.scanpy._matrix_chart import matrix_tiles, _labels
from genome_spy.integrations.scanpy._style import (
    FONT,
    GROUPED_FONT_SIZE as TICK,
    POINTS_TO_PIXELS as PT,
    color_bounds,
    native_color,
    native_scheme,
)


def _ratios(value: Any, name: str) -> tuple[float, float]:
    """Return row and column layout ratios from one number or a pair."""
    pair = (value, value) if np.isscalar(value) else value
    if not isinstance(pair, (list, tuple)) or len(pair) != 2:
        raise ValueError(f"{CONTEXT}: {name} needs a number or a pair.")
    result = tuple(number(v, name, context=CONTEXT) for v in pair)
    if max(result) >= 1:
        raise ValueError(f"{CONTEXT}: {name} must be below 1.")
    return result[0], result[1]


def _tick_labels(
    labels: pd.Index,
    option: Any,
    axis: Any,
    *,
    horizontal: bool,
    size: float,
    zoom: bool,
) -> tuple[gs.Chart | None, float]:
    """Return labels at ordered slots and their outside space, skipping crowded ticks."""
    if option is False:
        return None, 10
    names = list(map(str, labels))
    step = 1
    if isinstance(option, str) and option == "auto":
        step = max(1, ceil(len(names) * TICK / size))
    elif isinstance(option, int) and not isinstance(option, bool) and option > 0:
        step = option
    elif option is None or isinstance(option, (str, int)) and option is not True:
        raise ValueError(
            f"{CONTEXT}: tick labels need auto, a boolean, a positive stride, or a label list."
        )
    elif option is not True:
        names = _labels(option, len(names), "tick labels", context=CONTEXT)
    layer = _slot_labels(
        names, axis, horizontal=horizontal, opposite=not horizontal, zoom=zoom
    )
    if zoom and isinstance(option, str) and option == "auto":
        # Reveal more tick labels as their slots grow.
        channel, extent = ("x", "width") if horizontal else ("y", "height")
        layer = layer.transform_filter(
            f"datum.slot % max(1, ceil({TICK} / (grid_{channel}_step * {extent}))) == 0"
        )
    elif step > 1:
        layer = layer.transform_filter(f"datum.slot % {step} == 0")
    space = max(map(len, names[::step])) * TICK * 0.65 + 12
    return layer, space


def _color_strip(
    colors: pd.DataFrame,
    axis: Any,
    *,
    horizontal: bool,
    size: float,
    extent: float,
    zoom: bool,
    categories: pd.Series | None = None,
    palette: tuple[str, ...] = (),
) -> gs.LayerChart:
    """Return ordered color tracks, using category names for a native legend if supplied."""
    tracks = colors.shape[1]
    rows = [
        {
            "slot": i,
            "_color": categories.iloc[i] if categories is not None else color,
            "start": (tracks - j - 1) * size / extent,
            "end": (tracks - j) * size / extent,
        }
        for j in range(tracks)
        for i, color in enumerate(colors.iloc[:, j])
    ]
    strip = gs.Chart(rows).mark_rect(tooltip=None, clip="never")
    if horizontal:
        strip = strip.transform_calculate(
            _start="1 + datum.start", _end="1 + datum.end"
        ).encode(
            x=axis.field("slot"),
            y=gs.Y("_start:Q").scale(None).axis(None),
            y2="_end:Q",
        )
    else:
        strip = strip.transform_calculate(
            _start="-datum.end", _end="-datum.start"
        ).encode(
            y=axis.field("slot"),
            x=gs.X("_start:Q").scale(None).axis(None),
            x2="_end:Q",
        )
    if zoom:
        # Clip only the scrolling direction; strips remain outside the matrix.
        channel = "x" if horizontal else "y"
        strip = strip.transform_filter(
            f"{slot_position(channel, 'datum.slot + 1')} > 0 && "
            f"{slot_position(channel, 'datum.slot')} < 1"
        )
        start = f"clamp({slot_position(channel, 'datum.slot')}, 0, 1)"
        stop = f"clamp({slot_position(channel, 'datum.slot + 1')}, 0, 1)"
        strip = strip.transform_calculate(
            _slot_start=start if horizontal else f"1 - ({start})",
            _slot_stop=stop if horizontal else f"1 - ({stop})",
        ).encode(
            **{
                channel: (gs.X if horizontal else gs.Y)("_slot_start:Q")
                .scale(None)
                .axis(None),
                channel + "2": "_slot_stop:Q",
            }
        )
    # Named categories generate a native legend; plain CSS tracks have no labels.
    color = gs.Color("_color:N")
    if categories is not None:
        color = color.scale(
            type="ordinal",
            domain=categories.cat.categories.tolist(),
            range=list(palette),
        ).legend(
            gs.Legend(
                title=str(categories.name),
                orient="right",
                symbolType="square",
                labelLimit=1000,
            )
        )
        # Missing annotations leave the white strip background visible.
        strip = strip.transform_filter("isValid(datum._color)")
    else:
        css_colors = list(dict.fromkeys(colors.to_numpy().ravel()))
        color = color.scale(type="ordinal", domain=css_colors, range=css_colors).legend(
            None
        )
    strip = strip.encode(color=color)
    labels = [
        {"label": str(name), "position": (tracks - i - 0.5) * size / extent}
        for i, name in enumerate(colors.columns)
        if name != ""
    ]
    text = gs.Chart(labels).mark_text(
        font=FONT,
        size=TICK,
        align="left" if horizontal else "right",
        angle=0 if horizontal else -90,
        baseline="middle",
        xOffset=8 if horizontal else 0,
        yOffset=0 if horizontal else 8,
        clip="never",
        tooltip=None,
    )
    if horizontal:
        text = text.transform_calculate(_position="1 + datum.position").encode(
            x=gs.value(1), y=gs.Y("_position:Q").scale(None).axis(None), text="label:N"
        )
    else:
        text = text.transform_calculate(_position="-datum.position").encode(
            y=gs.value(0), x=gs.X("_position:Q").scale(None).axis(None), text="label:N"
        )
    outside_labels = (
        gs.layer(text)
        .resolve_scale(x="excluded", y="excluded")
        .resolve_axis(x="excluded", y="excluded")
    )
    layers = [strip, outside_labels] if labels else [strip]
    if zoom:
        return (
            gs.layer(*layers)
            .resolve_scale(x="excluded", y="excluded", color="excluded")
            .resolve_axis(x="excluded", y="excluded")
        )
    if horizontal:
        return (
            gs.layer(*layers)
            .resolve_scale(y="excluded", color="excluded")
            .resolve_axis(y="excluded")
        )
    return (
        gs.layer(*layers)
        .resolve_scale(x="excluded", color="excluded")
        .resolve_axis(x="excluded")
    )


def build_clustermap(
    data: ClusteredMatrix,
    *,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    width: float | None,
    height: float | None,
    cmap: Any = None,
    vmin: float | None = None,
    vmax: float | None = None,
    figsize: tuple[float, float] | None = None,
    dendrogram_ratio: Any = 0.2,
    colors_ratio: Any = 0.03,
    xticklabels: Any = "auto",
    yticklabels: Any = "auto",
    linewidths: float = 0,
    linecolor: str = "white",
    cbar_pos: Any = (0.02, 0.8, 0.05, 0.18),
    cbar_kws: Any = None,
) -> gs.TopLevelSpec:
    """Return a clustered heatmap from detached data, using shared native tiles and trees.

    Keep both trees, masks, labels and annotation tracks on the same permutations.
    """
    # Reserve tree and track space from the caller's size budget.
    trees = _ratios(dendrogram_ratio, "dendrogram_ratio")
    colors = _ratios(colors_ratio, "colors_ratio")
    fractions = [
        1 - trees[i] - colors[i] * count
        for i, count in enumerate((data.row_colors.shape[1], data.col_colors.shape[1]))
    ]
    if min(fractions) <= 0:
        raise ValueError(
            f"{CONTEXT}: tree and color ratios leave no room for the matrix."
        )
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{CONTEXT}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{CONTEXT}: figsize needs width and height in inches.")
        width, height = [
            number(v, "figsize", context=CONTEXT) * 100 * fraction
            for v, fraction in zip(figsize, fractions, strict=True)
        ]
    width = number(
        1000 * fractions[0] if width is None else width, "width", context=CONTEXT
    )
    height = number(
        1000 * fractions[1] if height is None else height, "height", context=CONTEXT
    )
    if min(width, height) <= 0:
        raise ValueError(f"{CONTEXT}: width and height must be positive.")
    # Keep only color-guide options that the native renderer can honor.
    if cbar_pos is not None and (
        not isinstance(cbar_pos, (list, tuple))
        or tuple(cbar_pos) != (0.02, 0.8, 0.05, 0.18)
    ):
        raise NotImplementedError(
            f"{CONTEXT}: custom cbar_pos is unsupported; the native guide is on the right, or use cbar_pos=None."
        )
    if cbar_kws is not None and (
        not isinstance(cbar_kws, dict) or set(cbar_kws) - {"label"}
    ):
        raise TypeError(f"{CONTEXT}: cbar_kws supports only label.")
    label = (cbar_kws or {}).get("label")
    if label is not None and not isinstance(label, str):
        raise TypeError(f"{CONTEXT}: colorbar label must be a string.")
    scheme = native_scheme("magma" if cmap is None else cmap, "cmap", context=CONTEXT)
    # Hidden cells do not influence the displayed color limits.
    values = numeric_values(data.values, context=CONTEXT).copy()
    values[data.mask] = np.nan
    low, high, _ = color_bounds(values, vmin, vmax, context=CONTEXT)
    guide = (
        gs.Legend(
            title=label,
            orient="right",
            direction="vertical",
            gradientLength=height * 0.3,
            gradientThickness=15,
        )
        if cbar_pos is not None
        else None
    )
    tiles = matrix_tiles(
        values,
        list(map(str, data.values.columns)),
        list(map(str, data.values.index)),
        hover=hover,
        color=gs.Color("_value:Q")
        .scale(
            type="linear",
            domain=[low, high],
            scheme=scheme,
            zero=False,
            nice=False,
            clamp=True,
        )
        .legend(guide),
    )
    tiles = tiles.mark_rect(
        tooltip={"handler": "default"} if hover else None,
        stroke=native_color(linecolor, "linecolor", context=CONTEXT),
        strokeWidth=number(linewidths, "linewidths", context=CONTEXT) * PT,
    )
    nrows, ncols = values.shape
    x, y = (
        coordinate(gs.X, "_x", ncols, 0),
        coordinate(gs.Y, "_y", nrows, 0, reverse=True),
    )
    x, y = zoom_axes(x, y, enabled=zoom, name="clustermap")
    tiles = tiles.encode(x=x, y=y)
    layers: list[gs.Chart | gs.LayerChart] = [
        with_values(tiles, "_value") if show_values else tiles
    ]
    xlabels, bottom = _tick_labels(
        data.values.columns,
        xticklabels,
        x,
        horizontal=True,
        size=width,
        zoom=bool(zoom),
    )
    ylabels, right = _tick_labels(
        data.values.index,
        yticklabels,
        y,
        horizontal=False,
        size=height,
        zoom=bool(zoom),
    )
    # Track titles can be longer than the matrix's visible tick labels.
    for names, horizontal in (
        (data.row_colors.columns, False),
        (data.col_colors.columns, True),
    ):
        space = max((len(str(name)) for name in names), default=0) * TICK * 0.65 + 12
        if horizontal:
            right = max(right, space)
        else:
            bottom = max(bottom, space)
    layers.extend(layer for layer in (xlabels, ylabels) if layer is not None)
    # Strips stay between the matrix and tree leaves, with no spare panel gap.
    row_track, col_track = (
        width * colors[0] / fractions[0],
        height * colors[1] / fractions[1],
    )
    row_space, col_space = (
        row_track * data.row_colors.shape[1],
        col_track * data.col_colors.shape[1],
    )
    for tracks, axis, horizontal, size, extent in (
        (data.row_colors, y, False, row_track, width),
        (data.col_colors, x, True, col_track, height),
    ):
        if tracks.shape[1]:
            layers.append(
                _color_strip(
                    tracks,
                    axis,
                    horizontal=horizontal,
                    size=size,
                    extent=extent,
                    zoom=bool(zoom),
                    categories=data.obs_labels if not horizontal else None,
                    palette=data.obs_palette if not horizontal else (),
                )
            )
    left, top = width * trees[0] / fractions[0], height * trees[1] / fractions[1]
    if data.row_tree is not None:
        layers.append(
            tree_overlay(
                data.row_tree,
                orientation="left",
                reverse=True,
                size=left,
                offset=row_space,
                linewidth=0.5,
                leaf_projection=slot_position("y", "datum.{field}") if zoom else None,
            )
        )
    if data.col_tree is not None:
        layers.append(
            tree_overlay(
                data.col_tree,
                orientation="top",
                size=top,
                offset=col_space,
                linewidth=0.5,
                leaf_projection=slot_position("x", "datum.{field}") if zoom else None,
            )
        )
    chart = (
        gs.layer(*layers)
        .properties(
            width=width,
            height=height,
            padding={
                "left": left + row_space + 10,
                "top": top + col_space + 10,
                "bottom": bottom,
                "right": right,
            },
        )
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_legend(
            labelFont=FONT,
            labelFontSize=TICK,
            titleFont=FONT,
            layout={"anchor": "start", "direction": "vertical", "wrap": False},
        )
    )
    return with_navigation(chart, enabled=bool(zoom))
