"""Native matrixplot tiles on shared grouped-expression slots and guides."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._grid_interactions import grid_interactions
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._expression.grouped_chart import (
    color_legend,
    finish_grouped_chart,
    grouped_axes,
    plot_dimensions,
    summary_records,
    totals_track,
)
from genome_spy.integrations.scanpy._expression.grouped_data import FeatureGroup
from genome_spy.integrations.scanpy._expression.colors import expression_scale

from genome_spy.integrations.scanpy._style import (
    POINTS_TO_PIXELS as _PT,
    native_color,
)

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData


def build_matrixplot(
    colors: pd.DataFrame,
    feature_groups: tuple[FeatureGroup, ...],
    *,
    swap_axes: bool,
    title: str | None,
    colorbar_title: str | None,
    cmap: Any,
    vmin: float | None,
    vmax: float | None,
    edgecolor: Any,
    linewidth: float,
    rotation: float | None,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    highlight: bool | Literal["outline"] = False,
    value_title: str,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    tree: DendrogramData | None = None,
    tree_size: float = 80,
    totals: pd.DataFrame | None = None,
    show_colorbar: bool = True,
    legend_width: float = 150,
) -> gs.TopLevelSpec:
    """Build a native tile chart from displayed means and marker groups.

    Return the shared grouped layout with optional tree and summary hover, without
    reading AnnData or recomputing means.
    """
    context = "gsc.pl.matrixplot"
    rows, columns = colors.shape
    no_edge = isinstance(edgecolor, str) and edgecolor.lower() == "none"
    stroke = (
        "gray" if no_edge else native_color(edgecolor, "edgecolor", context=context)
    )
    linewidth = number(linewidth, "linewidth", context=context)
    if rotation is not None:
        rotation = number(rotation, "var_group_rotation", minimum=-360, context=context)
    for name, value in {"title": title, "colorbar_title": colorbar_title}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    width, height = plot_dimensions(
        rows,
        columns,
        swap_axes=swap_axes,
        width=width,
        height=height,
        figsize=figsize,
        context=context,
        legend_width=legend_width,
    )
    scale = expression_scale(
        colors.to_numpy(dtype=float, na_value=float("nan")),
        cmap,
        vmin,
        vmax,
        context=context,
    )

    # Tiles fill their slots; missing means leave an empty slot with its label.
    x, y, scales = grouped_axes(rows, columns, xpadding=0, ypadding=0, zoom=zoom)
    tiles = (
        gs.Chart(summary_records(colors, swap_axes=swap_axes, context=context))
        .transform_filter("isValid(datum._mean)")
        .mark_rect(
            stroke=stroke,
            strokeOpacity=0 if no_edge else 1,
            strokeWidth=linewidth * _PT,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
            color=gs.Color("_mean:Q")
            .scale(scale)
            .legend(
                color_legend(colorbar_title).gradientLength(legend_width)
                if show_colorbar
                else None
            ),
        )
    )
    if hover:
        tiles = tiles.encode(
            tooltip=[
                gs.Tooltip("_gene:N", title="Gene"),
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip("_mean:Q", title=value_title, format=".4g"),
            ]
        )

    # Reuse the dotplot's labels, marker brackets, guides and tree placement.
    return finish_grouped_chart(
        grid_interactions(tiles, highlight, values="_mean" if show_values else None),
        colors,
        feature_groups,
        x,
        y,
        swap_axes=swap_axes,
        rotation=rotation,
        title=title,
        width=width,
        height=height,
        scales=scales,
        name="matrixplot",
        tree=tree,
        zoom=bool(zoom),
        tree_size=tree_size,
        group_track=totals_track(
            totals, swapped=swap_axes, size=tree_size, hover=hover, name="matrixplot"
        )
        if totals is not None
        else None,
    )
