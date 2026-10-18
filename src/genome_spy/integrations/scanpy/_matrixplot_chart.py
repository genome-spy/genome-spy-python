"""Native matrixplot tiles on shared grouped-expression slots and guides."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grouped_chart import (
    color_legend,
    finish_grouped_chart,
    grouped_axes,
    plot_dimensions,
    summary_records,
)
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup

from genome_spy.integrations.scanpy._style import (
    POINTS_TO_PIXELS as _PT,
    color_bounds,
    native_color,
    native_scheme,
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
    value_title: str,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    tree: DendrogramData | None = None,
) -> gs.TopLevelSpec:
    """Build a native tile chart from displayed means and marker groups.

    Return the shared grouped layout with optional tree and summary hover, without
    reading AnnData or recomputing means.
    """
    context = "gsc.pl.matrixplot"
    rows, columns = colors.shape
    scheme = native_scheme("viridis" if cmap is None else cmap, "cmap", context=context)
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
    )
    low, high, _ = color_bounds(
        colors.to_numpy(dtype=float, na_value=float("nan")),
        vmin,
        vmax,
        context=context,
    )
    # Tiles fill their slots; missing means leave an empty slot with its label.
    x, y = grouped_axes(rows, columns, xpadding=0, ypadding=0)
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
            .scale(
                type="linear",
                domain=[low, high],
                nice=False,
                zero=False,
                clamp=True,
                scheme=scheme,
            )
            .legend(
                color_legend(
                    colorbar_title,
                    feature_groups,
                    swap_axes=swap_axes,
                    tree=tree is not None,
                )
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
        tiles,
        colors,
        feature_groups,
        x,
        y,
        swap_axes=swap_axes,
        rotation=rotation,
        title=title,
        width=width,
        height=height,
        frame_width=1.5,
        tree=tree,
    )
