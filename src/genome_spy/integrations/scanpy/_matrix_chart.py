"""Native tiles for a supplied numeric matrix, without AnnData computations."""

from collections.abc import Collection, Mapping
from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._grid_interactions import (
    zoom_axes,
    with_values,
    vertical_highlights,
    horizontal_tick_labels,
)
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._data import (
    coordinate_domain,
    matrix_array,
    number,
    numeric_values,
)
from genome_spy.integrations.scanpy._grouped_chart import (
    coordinate,
    index_scales,
    _slot_labels,
)
from genome_spy.integrations.scanpy._style import (
    FONT,
    GROUPED_FONT_SIZE as TICK,
    POINTS_TO_PIXELS as PT,
    color_bounds,
    native_scheme,
)


def build_matrix(
    matrix: Any,
    *,
    xlabel: str | None,
    ylabel: str | None,
    xticks: Collection[str] | None,
    yticks: Collection[str] | None,
    title: str | None,
    colorbar_shrink: float,
    color_map: Any,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    width: float | None,
    height: float | None,
    limits: tuple[tuple[float, float], tuple[float, float]] | None = None,
    reverse_y: bool = True,
    highlights_x: Collection[float] = (),
    context: str = "gsc.pl.matrix",
    xtick_labels: Mapping[float, str] | None = None,
    overlay: gs.Chart | None = None,
) -> gs.TopLevelSpec:
    """Return native tiles, labels and a color guide from a resident numeric matrix.

    Keep supplied values and order; only mask missing entries and normalize color.
    """
    array = matrix_array(matrix, context=context)
    # Pandas preserves numeric types and turns masked entries into missing values.
    values = numeric_values(pd.DataFrame(array), context=context)
    rows, columns = values.shape
    xlabels = _labels(xticks, columns, "xticks", context=context)
    ylabels = _labels(yticks, rows, "yticks", context=context)
    for name, value in {"xlabel": xlabel, "ylabel": ylabel, "title": title}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    shrink = number(colorbar_shrink, "colorbar_shrink", context=context)
    if not shrink:
        raise ValueError(f"{context}: colorbar_shrink must be positive.")
    scheme = native_scheme(
        "viridis" if color_map is None else color_map, "color_map", context=context
    )
    low, high, _ = color_bounds(values, None, None, context=context)
    # Fit square cells inside a 400-pixel area unless dimensions are specified.
    cell_size = min(400 / rows, 400 / columns)
    width = number(
        columns * cell_size if width is None else width, "width", context=context
    )
    height = number(
        rows * cell_size if height is None else height, "height", context=context
    )
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    x = coordinate(gs.X, "_x", columns, 0)
    y = coordinate(gs.Y, "_y", rows, 0, reverse=reverse_y)
    if limits is not None:
        x = gs.X("_x:Q").scale(
            type="linear", domain=list(limits[0]), zero=False, nice=False
        )
        y = gs.Y("_y:Q").scale(
            type="linear",
            domain=list(limits[1]),
            reverse=reverse_y,
            zero=False,
            nice=False,
        )
    name = context.rsplit(".", 1)[-1]
    # Unnamed scales let independent panels compose without global name collisions.
    x, y = zoom_axes(x, y, enabled=zoom, name=None)
    if limits is None:
        scales = index_scales(x, y)
        x, y = gs.X("_x:I"), gs.Y("_y:I")
    else:
        scales = gs.scales(
            x=gs.Scale(**x.to_dict()["scale"]), y=gs.Scale(**y.to_dict()["scale"])
        )
        x, y = gs.X("_x:Q"), gs.Y("_y:Q")
    axes = []
    sides = {}
    for axis, labels, names, axis_title, horizontal, side in (
        (x, xticks, xlabels, xlabel, True, "bottom"),
        (y, yticks, ylabels, ylabel, False, "left"),
    ):
        axes.append(
            axis.axis(
                title=axis_title if labels is None else None,
                titlePadding=8,
                labels=labels is None,
                values=list(range(columns if horizontal else rows))
                if labels is not None
                else Undefined,
                domain=False,
                tickSize=3.5 * PT,
                tickWidth=0.8 * PT,
                tickColor="black",
                labelFont=FONT,
                labelFontSize=TICK,
                titleFont=FONT,
                titleFontWeight="normal",
                titleFontSize=10 * PT,
            )
        )
        if horizontal and xtick_labels is not None:
            axes[-1] = axes[-1].axis(
                title=None, labels=False, values=list(xtick_labels)
            )
            sides[side] = [horizontal_tick_labels(xtick_labels, xlabel)]
        if labels is not None:
            ticks = _slot_labels(
                names,
                axis.axis(None),
                horizontal=horizontal,
                clip=True if limits is None else ("y" if horizontal else "x"),
            )
            if limits is not None:
                # Edge labels may straddle the cropped limit; hide only anchors outside it.
                channel = "x" if horizontal else "y"
                ticks = ticks.transform_filter(
                    f"inrange(datum.slot, domain('{channel}'))"
                )
            if axis_title is not None:
                ticks = ticks.properties(
                    title=gs.Title(
                        text=axis_title,
                        orient="bottom" if horizontal else "left",
                        angle=0 if horizontal else -90,
                        offset=8,
                        font=FONT,
                        fontSize=10 * PT,
                        fontWeight="normal",
                    )
                )
            sides[side] = [ticks]
    tiles = matrix_tiles(
        values,
        xlabels,
        ylabels,
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
        .legend(
            gs.Legend(
                title=None,
                orient="right",
                direction="vertical",
                gradientLength=height * shrink,
                gradientThickness=15,
                gradientStrokeColor="black",
                gradientStrokeWidth=0.8 * PT,
                offset=15,
            )
        ),
    ).encode(x=axes[0], y=axes[1])
    if limits is not None:
        # Explicit cell edges retain Scanpy's half-cell cropping and singleton limits.
        tiles = tiles.transform_calculate(
            _x0="datum._x - 0.5",
            _x1="datum._x + 0.5",
            _y0="datum._y - 0.5",
            _y1="datum._y + 0.5",
        ).encode(
            x=axes[0].field("_x0"),
            x2=gs.X2("_x1:Q"),
            y=axes[1].field("_y0"),
            y2=gs.Y2("_y1:Q"),
        )
    center = with_values(tiles, "_value") if show_values else tiles
    if overlay is not None:
        center = gs.layer(center, overlay)
    if len(highlights_x):
        center = gs.layer(center, vertical_highlights(highlights_x, 0, rows))
    center = center.properties(width=width, height=height, name=f"{name}-cells")
    chart = gs.surround(
        center, surround=gs.SurroundSides(**sides), spacing=0
    ).properties(scales=scales)
    if limits is not None:
        chart = chart.properties(padding={"top": TICK / 2, "bottom": TICK / 2})
    if title is not None:
        chart = chart.properties(title=gs.title(title, font=FONT, fontSize=12 * PT))
    return chart.configure_view(stroke="transparent", strokeWidth=0).configure_legend(
        labelFont=FONT,
        labelFontSize=TICK,
        layout={"anchor": "middle", "direction": "vertical", "wrap": False},
    )


def build_timeseries_heatmap(
    X: Any,
    *,
    var_names: Collection[str],
    highlights_x: Collection[float],
    color_map: Any,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    width: float | None,
    height: float | None,
    context: str = "gsc.pl.timeseries_as_heatmap",
    xtick_labels: Mapping[float, str] | None = None,
    xlabel: str | None = None,
) -> gs.TopLevelSpec:
    """Transpose supplied samples into variable rows, then reuse native matrix rendering."""
    array = matrix_array(X, context=context)
    if isinstance(var_names, (str, bytes)) or not isinstance(var_names, Collection):
        raise TypeError(
            f"{context}: var_names must be a collection of variable labels."
        )
    labels: Collection[str] | None = None
    if len(var_names):
        names = np.asarray(var_names)
        if names.ndim == 2 and names.shape[1]:
            names = names[:, 0]
        if names.ndim != 1:
            raise ValueError(
                f"{context}: var_names must be one-dimensional or a nonempty two-dimensional label array."
            )
        labels = names
    labels = _labels(labels, array.shape[1], "var_names", context=context)
    if isinstance(highlights_x, (str, bytes)) or not isinstance(
        highlights_x, Collection
    ):
        raise TypeError(
            f"{context}: highlights_x must be a collection of finite positions."
        )
    positions = [
        number(v, "highlights_x", context=context, minimum=-np.inf)
        for v in highlights_x
    ]
    # Scanpy's explicit center limits crop outer cells and expand singletons by 0.05.
    limits = tuple(coordinate_domain(np.array([0, n - 1]), 0) for n in array.shape)
    # Convert pandas columns before transposing so mixed numeric types stay numeric.
    if isinstance(array, pd.DataFrame):
        array = numeric_values(array, context=context)
    return build_matrix(
        np.asarray(array).T,
        xlabel=xlabel,
        ylabel=None,
        xticks=None,
        yticks=labels,
        title=None,
        colorbar_shrink=0.5,
        color_map=color_map,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=372 if width is None else width,
        height=616 if height is None else height,
        limits=(limits[0], limits[1]),
        reverse_y=False,
        highlights_x=positions,
        context=context,
        xtick_labels=xtick_labels,
    )


def matrix_tiles(
    values: np.ndarray,
    xlabels: list[str],
    ylabels: list[str],
    *,
    color: gs.Color,
    hover: bool,
) -> gs.Chart:
    """Return index-positioned numeric tiles and optional hover from a detached array.

    Keep labels separate from positions so duplicate names retain distinct cells.
    """
    yy, xx = np.indices(values.shape)
    table = pd.DataFrame(
        {
            "_x": xx.ravel(),
            "_y": yy.ravel(),
            "_value": values.ravel(),
            "_column": np.asarray(xlabels)[xx.ravel()],
            "_row": np.asarray(ylabels)[yy.ravel()],
        }
    )
    tiles = (
        gs.Chart(table)
        .transform_filter("isValid(datum._value)")
        .mark_rect(clip=True, tooltip={"handler": "default"} if hover else None)
        .encode(
            x=coordinate(gs.X, "_x", values.shape[1], 0),
            y=coordinate(gs.Y, "_y", values.shape[0], 0, reverse=True),
            color=color,
        )
    )
    if hover:
        tiles = tiles.encode(
            tooltip=[
                gs.Tooltip("_row:N", title="Row"),
                gs.Tooltip("_column:N", title="Column"),
                gs.Tooltip("_value:Q", title="Value", format=".4g"),
            ]
        )
    return tiles


def _labels(
    labels: Collection[str] | None,
    count: int,
    name: str,
    *,
    context: str = "gsc.pl.matrix",
) -> list[str]:
    """Return explicit tick labels or numeric positions, preserving repeated labels.

    Reject mismatched counts rather than displaying labels over the wrong cells.
    """
    if labels is None:
        return [str(index) for index in range(count)]
    if isinstance(labels, (str, bytes)) or len(labels) != count:
        raise ValueError(f"{context}: {name} must contain {count} labels.")
    return [str(label) for label in labels]
