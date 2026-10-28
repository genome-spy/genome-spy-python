"""Native clustered tiles with two attached trees and ordered color tracks."""

from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._clustermap_data import ClusteredMatrix, CONTEXT
from genome_spy.integrations.scanpy._data import figsize_pixels, number, numeric_values
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._grouped_chart import (
    coordinate,
    index_scales,
    _slot_labels,
)
from genome_spy.integrations.scanpy._grid_interactions import (
    zoom_axes,
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
) -> gs.Chart | None:
    """Return in-bounds slot labels, skipping crowded ticks until zoom reveals them."""
    if option is False:
        return None
    names = list(map(str, labels))
    step = 1
    auto = isinstance(option, str) and option == "auto"
    if not auto and option is not True:
        if isinstance(option, int) and not isinstance(option, bool) and option > 0:
            step = option
        elif option is None or isinstance(option, (str, int)):
            raise ValueError(
                f"{CONTEXT}: tick labels need auto, a boolean, a positive stride, or a label list."
            )
        else:
            names = _labels(option, len(names), "tick labels", context=CONTEXT)
    chart = _slot_labels(names, axis, horizontal=horizontal, opposite=not horizontal)
    if auto:
        # Measure the bands after gaps, including before any zoom.
        channel, extent = ("x", "width") if horizontal else ("y", "height")
        chart = chart.transform_filter(
            f"datum.slot % max(1, ceil({TICK} / (bandwidth('{channel}') * {extent}))) == 0"
        )
    elif step > 1:
        chart = chart.transform_filter(f"datum.slot % {step} == 0")
    return chart


def _color_tracks(
    colors: pd.DataFrame,
    axis: Any,
    *,
    horizontal: bool,
    size: float,
    hover: bool,
    categories: pd.Series | None = None,
    palette: tuple[str, ...] = (),
) -> list[gs.Chart]:
    """Return one native side view per color track, with a category legend if known."""
    tracks = []
    for index, name in enumerate(colors.columns):
        labels = categories if categories is not None else colors.iloc[:, index]
        chart = gs.Chart(
            [{"slot": i, "_color": value} for i, value in enumerate(labels)]
        )
        chart = chart.mark_rect(
            clip=True,
            tooltip={"handler": "default"}
            if hover and categories is not None
            else None,
        ).encode(**{"x" if horizontal else "y": axis.field("slot")})
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
            # Missing annotations leave the white track background visible.
            chart = chart.transform_filter("isValid(datum._color)")
            if hover:
                chart = chart.encode(
                    tooltip=[gs.Tooltip("_color:N", title=str(categories.name))]
                )
        else:
            css_colors = list(dict.fromkeys(labels))
            color = color.scale(
                type="ordinal", domain=css_colors, range=css_colors
            ).legend(None)
        chart = chart.encode(color=color)
        chart = (
            chart.properties(height=size)
            if horizontal
            else chart.properties(width=size)
        )
        chart = chart.properties(
            name=f"clustermap-{'top' if horizontal else 'left'}-colors-{index}"
        )
        if name != "":
            chart = chart.properties(
                title=gs.Title(
                    text=str(name),
                    orient="right" if horizontal else "bottom",
                    angle=0 if horizontal else -90,
                    anchor="middle",
                    align="left" if horizontal else "right",
                    baseline="middle",
                    offset=8,
                    font=FONT,
                    fontSize=min(TICK, size),
                    fontWeight="normal",
                )
            )
        tracks.append(chart)
    return tracks


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
        width, height = figsize_pixels(figsize, width, height, context=CONTEXT)
        width *= fractions[0]
        height *= fractions[1]
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
        clip=True,
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
    scales = index_scales(x, y)
    # The surround owns both scales; tiles and side views only declare fields.
    x, y = gs.X("_x:I").axis(None), gs.Y("_y:I").axis(None)
    tiles = tiles.encode(x=x, y=y)
    center = with_values(tiles, "_value") if show_values else gs.layer(tiles)
    center = center.properties(name="clustermap-cells", width=width, height=height)
    sides: dict[str, Any] = {}
    for labels, option, axis, horizontal, side in (
        (data.values.columns, xticklabels, x, True, "bottom"),
        (data.values.index, yticklabels, y, False, "right"),
    ):
        ticks = _tick_labels(labels, option, axis, horizontal=horizontal)
        if ticks is not None:
            sides[side] = [ticks]
    # Trees and strips each own a viewport and share the center's gapped slots.
    for index, (tree, tracks, slot_axis, horizontal, extent) in enumerate(
        (
            (data.row_tree, data.row_colors, y, False, width),
            (data.col_tree, data.col_colors, x, True, height),
        )
    ):
        side = "top" if horizontal else "left"
        fraction = fractions[index]
        views: list[gs.Chart] = []
        if tree is not None:
            views.append(
                tree_track(
                    tree,
                    list(range(len(tracks))),
                    horizontal=horizontal,
                    size=extent * trees[index] / fraction,
                    reverse=not horizontal,
                    linewidth=0.5,
                ).properties(name=f"clustermap-{side}-tree")
            )
        views.extend(
            _color_tracks(
                tracks,
                slot_axis,
                horizontal=horizontal,
                size=extent * colors[index] / fraction,
                hover=hover,
                categories=data.obs_labels if not horizontal else None,
                palette=data.obs_palette if not horizontal else (),
            )
        )
        if views:
            sides[side] = gs.SurroundSideSpec(views=views, spacing=0)
    return (
        gs.surround(center, surround=gs.SurroundSides(**sides), spacing=0)
        .properties(scales=scales)
        .resolve_legend(color="collected")
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_legend(
            labelFont=FONT,
            labelFontSize=TICK,
            titleFont=FONT,
            layout={"anchor": "middle", "direction": "vertical", "wrap": False},
        )
    )
