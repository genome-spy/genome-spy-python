"""Native dotplot marks, slot labels, brackets and size/color guides."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._colors import native_scheme
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup
from genome_spy.integrations.scanpy._grouped_chart import (
    color_bounds,
    color_legend,
    finish_grouped_chart,
    grouped_axes,
    guide_offset,
    number,
    plot_dimensions,
    summary_records,
)

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData

_PT = 100 / 72


def dot_size_scale(
    fractions: np.ndarray, dot_min: float | None, dot_max: float | None, smallest: float
) -> tuple[list[float], list[float], list[float]]:
    """Map exact percentage values to areas, including clipped power scaling."""
    smallest = number(smallest, "smallest_dot", context="gsc.pl.dotplot")
    if smallest > 200:
        raise ValueError(
            "gsc.pl.dotplot: smallest_dot cannot exceed the largest dot (200)."
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
    step = 0.1 if 0.3 < difference <= 0.6 else 0.05 if difference <= 0.3 else 0.2
    ticks = np.arange(high, low, -step)[::-1]
    ticks = np.round(ticks * 100, 10) / 100
    # Explicit lookup keeps the clipped power mapping identical in dots and guides.
    domain = np.unique(np.concatenate([fractions[np.isfinite(fractions)], ticks]))
    areas = smallest + ((np.clip(domain, low, high) - low) / difference) ** 1.5 * (
        200 - smallest
    )
    return (domain * 100).tolist(), (areas * _PT**2).tolist(), (ticks * 100).tolist()


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
    hover: bool,
    value_title: str,
    linewidth: float,
    rotation: float | None,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    tree: DendrogramData | None = None,
) -> gs.TopLevelSpec:
    rows, columns = colors.shape
    scheme = native_scheme(
        "viridis" if cmap is None else cmap, "cmap", context="gsc.pl.dotplot"
    )
    linewidth = number(linewidth, "linewidth", context="gsc.pl.dotplot")
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
    )
    for name, value in {
        "title": title,
        "size_title": size_title,
        "colorbar_title": colorbar_title,
    }.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"gsc.pl.dotplot: {name} must be a string or None.")
    values = colors.to_numpy(dtype=float, na_value=np.nan)
    low, high, constant_color = color_bounds(
        values, vmin, vmax, context="gsc.pl.dotplot"
    )
    domain, areas, ticks = dot_size_scale(
        fractions.to_numpy(dtype=float, na_value=np.nan), dot_min, dot_max, smallest_dot
    )
    table = summary_records(colors, swap_axes=swap_axes, context="gsc.pl.dotplot")
    table["_percent"] = fractions.to_numpy(dtype=float, na_value=np.nan).ravel() * 100
    if constant_color:
        # Scanpy freezes dot colors before its colorbar expands constant bounds.
        table["_paint"] = low
    x, y = grouped_axes(rows, columns, xpadding=0.3, ypadding=0.5)
    offset = guide_offset(feature_groups, swap_axes=swap_axes, tree=tree is not None)
    dots = (
        gs.Chart(table)
        .transform_filter("isValid(datum._mean) && isValid(datum._percent)")
        .mark_point(
            filled=True,
            stroke="black",
            strokeWidth=linewidth * _PT,
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
                color_legend(
                    colorbar_title,
                    feature_groups,
                    swap_axes=swap_axes,
                    tree=tree is not None,
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
                    offset=offset,
                )
            ),
        )
    )
    if smallest_dot == 0:
        # A zero-area dot must not leave a stroke-only picking/raster footprint.
        dots = dots.transform_filter(f"datum._percent > {100 * (dot_min or 0)}")
    if hover:
        dots = dots.encode(
            tooltip=[
                gs.Tooltip("_gene:N", title="Gene"),
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip("_mean:Q", title=value_title, format=".4g"),
                gs.Tooltip("_percent:Q", title="Expressing cells (%)", format=".1f"),
            ]
        )
    return finish_grouped_chart(
        dots,
        colors,
        feature_groups,
        x,
        y,
        swap_axes=swap_axes,
        rotation=rotation,
        title=title,
        width=width,
        height=height,
        frame_width=0.8,
        tree=tree,
    )
