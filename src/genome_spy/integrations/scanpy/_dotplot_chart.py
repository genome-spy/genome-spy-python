"""Native dotplot marks, slot labels, brackets and size/color guides."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._grid_interactions import zoom_axes
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grouped_chart import (
    color_legend,
    finish_grouped_chart,
    grouped_axes,
    index_scales,
    feature_gaps,
    plot_dimensions,
    summary_records,
    totals_track,
)
from genome_spy.integrations.scanpy._style import (
    POINTS_TO_PIXELS as _PT,
    color_bounds,
    native_scheme,
    native_color,
)

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData


def dot_size_scale(
    fractions: np.ndarray,
    dot_min: float | None,
    dot_max: float | None,
    smallest: float,
    largest: float = 200,
    exponent: float = 1.5,
) -> tuple[list[float], list[float], list[float]]:
    """Return percentage positions, dot areas and legend ticks from cell fractions.

    Apply Scanpy's clipping and size curve once so dots and legend symbols agree.
    """
    smallest = number(smallest, "smallest_dot", context="gsc.pl.dotplot")
    largest = number(largest, "largest_dot", context="gsc.pl.dotplot")
    exponent = number(exponent, "size_exponent", context="gsc.pl.dotplot")
    if exponent == 0:
        raise ValueError("gsc.pl.dotplot: size_exponent must be positive.")
    if smallest > largest:
        raise ValueError(
            f"gsc.pl.dotplot: smallest_dot cannot exceed the largest dot ({largest:g})."
        )
    valid = fractions[np.isfinite(fractions)]
    if not valid.size:
        raise ValueError("gsc.pl.dotplot: fractions need at least one finite value.")
    low = (
        0.0 if dot_min is None else number(dot_min, "dot_min", context="gsc.pl.dotplot")
    )
    high = (
        float(np.ceil(valid.max() * 10) / 10)
        if dot_max is None
        else number(dot_max, "dot_max", context="gsc.pl.dotplot")
    )
    if low > 1 or high > 1 or high <= low:
        raise ValueError(
            "gsc.pl.dotplot: require 0 <= dot_min < dot_max <= 1. "
            "For all-zero fractions, set dot_max=1 explicitly."
        )
    difference = high - low
    # Match Scanpy's spacing between percentage labels.
    if difference <= 0.3:
        step = 0.05
    elif difference <= 0.6:
        step = 0.1
    else:
        step = 0.2
    ticks = np.arange(high, low, -step)[::-1]
    ticks = np.round(ticks * 100, 10) / 100
    # Use the same percentage-to-area lookup for dots and legend symbols.
    domain = np.unique(np.concatenate([fractions[np.isfinite(fractions)], ticks]))
    areas = smallest + ((np.clip(domain, low, high) - low) / difference) ** exponent * (
        largest - smallest
    )
    return (domain * 100).tolist(), (areas * _PT**2).tolist(), (ticks * 100).tolist()


def build_dotplot(
    colors: pd.DataFrame,
    fractions: pd.DataFrame,
    feature_groups: tuple[FeatureGroup, ...],
    *,
    swap_axes: bool,
    title: str | None,
    colorbar_title: str | None = "Mean expression",
    size_title: str | None = "Cells expressing (%)",
    cmap: Any,
    vmin: float | None,
    vmax: float | None,
    dot_min: float | None = None,
    dot_max: float | None = None,
    smallest_dot: float = 0,
    hover: bool,
    zoom: bool | Literal["xy"],
    highlight: bool,
    value_title: str,
    linewidth: float | None,
    rotation: float | None,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    tree: DendrogramData | None = None,
    tree_size: float = 80,
    totals: pd.DataFrame | None = None,
    largest_dot: float = 200,
    size_exponent: float = 1.5,
    edge_color: str | None = "black",
    grid: bool = False,
    x_padding: float = 0.8,
    y_padding: float = 1,
    show_size_legend: bool = True,
    show_colorbar: bool = True,
    legend_width: float = 150,
    group_gap: float = 0,
) -> gs.TopLevelSpec:
    """Build a native dotplot from displayed colors, cell fractions and marker groups.

    Return a chart with shared grouped layout, optional tree and summary hover;
    this step reads no AnnData and computes no expression statistics.
    """
    rows, columns = colors.shape
    scheme = native_scheme(
        "viridis" if cmap is None else cmap, "cmap", context="gsc.pl.dotplot"
    )
    linewidth = number(
        0 if linewidth is None else linewidth, "linewidth", context="gsc.pl.dotplot"
    )
    group_gap = number(group_gap, "group_gap", context="gsc.pl.dotplot")
    no_edge = edge_color is None or edge_color == "none"
    edge_color = (
        "black"
        if no_edge
        else native_color(edge_color, "dot_edge_color", context="gsc.pl.dotplot")
    )
    for name, flag in {
        "grid": grid,
        "show_size_legend": show_size_legend,
        "show_colorbar": show_colorbar,
    }.items():
        if not isinstance(flag, bool):
            raise TypeError(f"gsc.pl.dotplot: {name} must be boolean.")
    x_padding = number(x_padding, "x_padding", minimum=0.5, context="gsc.pl.dotplot")
    y_padding = number(y_padding, "y_padding", minimum=0.5, context="gsc.pl.dotplot")
    if rotation is not None:
        rotation = number(
            rotation, "var_group_rotation", minimum=-360, context="gsc.pl.dotplot"
        )
    width, height = plot_dimensions(
        rows,
        columns,
        swap_axes=swap_axes,
        width=width,
        height=height,
        figsize=figsize,
        context="gsc.pl.dotplot",
        legend_width=legend_width,
    )
    for name, value in {
        "title": title,
        "size_title": size_title,
        "colorbar_title": colorbar_title,
    }.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"gsc.pl.dotplot: {name} must be a string or None.")
    # Calculate both scales before drawing so the dots and guides agree.
    values = colors.to_numpy(dtype=float, na_value=np.nan)
    low, high, constant_color = color_bounds(
        values, vmin, vmax, context="gsc.pl.dotplot"
    )
    domain, areas, ticks = dot_size_scale(
        fractions.to_numpy(dtype=float, na_value=np.nan),
        dot_min,
        dot_max,
        smallest_dot,
        largest_dot,
        size_exponent,
    )
    table = summary_records(colors, swap_axes=swap_axes, context="gsc.pl.dotplot")
    table["_percent"] = fractions.to_numpy(dtype=float, na_value=np.nan).ravel() * 100
    if constant_color:
        # Scanpy freezes dot colors before its colorbar expands constant bounds.
        table["_paint"] = low
    x, y = grouped_axes(
        rows, columns, xpadding=x_padding - 0.5, ypadding=y_padding - 0.5
    )
    if grid:
        x, y = (
            axis.axis(grid=True, gridColor="gray", gridWidth=0.1 * _PT)
            for axis in (x, y)
        )
    x, y = zoom_axes(x, y, enabled=zoom, name=None)
    gaps = feature_gaps(feature_groups, rows if swap_axes else columns)
    scales = index_scales(
        x,
        y,
        xgaps=[] if swap_axes else gaps,
        ygaps=gaps if swap_axes else [],
        gap_width=group_gap,
    )
    # The surround owns the scale definitions; marks retain fields and ticks.
    x, y = (
        gs.X("_x:I", axis=x.to_dict()["axis"]),
        gs.Y("_y:I", axis=y.to_dict()["axis"]),
    )
    dots = (
        gs.Chart(table)
        .transform_filter("isValid(datum._mean) && isValid(datum._percent)")
        .mark_point(
            filled=True,
            stroke=edge_color,
            strokeWidth=linewidth * _PT,
            strokeOpacity=0 if no_edge else Undefined,
            inwardStroke=False,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
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
                color_legend(colorbar_title).gradientLength(legend_width)
                if show_colorbar
                else None
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
                    offset=12,
                )
                if show_size_legend
                else None
            ),
        )
    )
    if smallest_dot == 0:
        # A zero-area dot must not leave a visible or hoverable outline.
        dots = dots.transform_filter(f"datum._percent > {100 * (dot_min or 0)}")
    # Hover reports the actual percentage, even when dot sizes are clipped.
    if hover:
        dots = dots.encode(
            tooltip=[
                gs.Tooltip("_gene:N", title="Gene"),
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip("_mean:Q", title=value_title, format=".4g"),
                gs.Tooltip("_percent:Q", title="Expressing cells (%)", format=".1f"),
            ]
        )
    center = gs.layer(dots).properties(
        view=gs.view(stroke="black", strokeWidth=1.5 * _PT)
    )
    if highlight:
        # The plot container owns the ruler so it also tracks gaps between dots.
        center = center.add_params(
            gs.ruler(
                "grid_cursor",
                encodings=["x", "y"],
                display="center",
                extent="view",
                persist=False,
                mark=gs.RulerMarkConfig(
                    stroke="#4682b4", opacity=0.55, strokeWidth=1, zindex=0
                ),
            )
        )
    chart = finish_grouped_chart(
        center,
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
        name="dotplot",
        legend_anchor="middle",
        legend_spacing=16,
        tree=tree,
        zoom=bool(zoom),
        tree_size=tree_size,
        group_track=totals_track(
            totals, swapped=swap_axes, size=tree_size, hover=hover, name="dotplot"
        )
        if totals is not None
        else None,
    )
    return chart
