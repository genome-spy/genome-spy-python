"""Native tiles for a supplied numeric matrix, without AnnData computations."""

from collections.abc import Collection
from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._grid_interactions import (
    zoom_axes,
    with_values,
    with_navigation,
)
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._data import number, numeric_values
from genome_spy.integrations.scanpy._grouped_chart import coordinate, _slot_labels
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
) -> gs.TopLevelSpec:
    """Return native tiles, labels and a color guide from a resident numeric matrix.

    Keep supplied values and order; only mask missing entries and normalize color.
    """
    context = "gsc.pl.matrix"
    if not isinstance(matrix, (np.ndarray, pd.DataFrame, list, tuple)):
        raise TypeError(f"{context}: supply a resident 2D numeric array or table.")
    array = matrix if isinstance(matrix, pd.DataFrame) else np.asanyarray(matrix)
    if array.ndim != 2 or not all(array.shape):
        raise ValueError(f"{context}: matrix must have two nonempty dimensions.")
    # Pandas preserves numeric types and turns masked entries into missing values.
    values = numeric_values(pd.DataFrame(array), context=context)
    rows, columns = values.shape
    xlabels = _labels(xticks, columns, "xticks")
    ylabels = _labels(yticks, rows, "yticks")
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
    y = coordinate(gs.Y, "_y", rows, 0, reverse=True)
    x, y = zoom_axes(x, y, enabled=zoom, name="matrix")
    xspace = max(map(len, xlabels)) * TICK * 0.65 + 12 if xticks is not None else 25
    yspace = max(map(len, ylabels)) * TICK * 0.65 + 12 if yticks is not None else 25
    axes = []
    for axis, labels, axis_title, horizontal, space in (
        (x, xticks, xlabel, True, xspace),
        (y, yticks, ylabel, False, yspace),
    ):
        axes.append(
            axis.axis(
                title=axis_title,
                titlePadding=space + 8 if labels is not None else 8,
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
    layers: list[gs.Chart | gs.LayerChart] = [
        with_values(tiles, "_value") if show_values else tiles
    ]
    if xticks is not None:
        layers.append(_slot_labels(xlabels, axes[0], horizontal=True, zoom=bool(zoom)))
    if yticks is not None:
        layers.append(_slot_labels(ylabels, axes[1], horizontal=False, zoom=bool(zoom)))
    chart = gs.layer(*layers).properties(
        width=width,
        height=height,
        padding={
            # Titled axes already reserve the space for their labels.
            "left": yspace if yticks is not None and not ylabel else 10,
            "bottom": xspace if xticks is not None and not xlabel else 10,
            "top": 10,
            "right": 10,
        },
    )
    if title is not None:
        chart = chart.properties(title=gs.title(title, font=FONT, fontSize=12 * PT))
    chart = with_navigation(chart, enabled=bool(zoom))
    return chart.configure_view(stroke="black", strokeWidth=0.8 * PT).configure_legend(
        labelFont=FONT,
        labelFontSize=TICK,
        layout={"anchor": "middle", "direction": "vertical", "wrap": False},
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
        .mark_rect(tooltip={"handler": "default"} if hover else None)
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
