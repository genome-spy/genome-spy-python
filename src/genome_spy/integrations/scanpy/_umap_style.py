"""Explicit native UMAP presentation defaults, independent of rcParams."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from typing import Any

from genome_spy.integrations.scanpy._colors import native_color

POINTS_TO_PIXELS = 100 / 72


@dataclass(frozen=True, slots=True)
class UMAPStyle:
    width: float
    height: float
    frameon: bool
    legend_loc: str | None
    colorbar_loc: str | None
    legend_fontsize: float
    ncols: int
    hspace: float
    wspace: float
    alpha: float
    stroke: str
    na_color: str
    stroke_opacity: float
    stroke_width: float
    font: str = "Lato"
    axis_fontsize: float = 10 * POINTS_TO_PIXELS
    title_fontsize: float = 12 * POINTS_TO_PIXELS
    tick_fontsize: float = 10 * POINTS_TO_PIXELS
    legend_labelspacing: float = 0.5
    legend_handletextpad: float = 0.8
    frame_color: str = "#000000"
    frame_width: float = 0.8 * POINTS_TO_PIXELS
    xmargin: float = 0.05
    ymargin: float = 0.05


def _number(value: Any, name: str, *, minimum: float = 0) -> float:
    if not isinstance(value, Real) or not isfinite(value) or value < minimum:
        raise ValueError(f"gsc.pl.umap: {name} must be a finite number >= {minimum}.")
    return float(value)


def _font_size(value: float | str | None) -> float:
    sizes = {
        "xx-small": 5.79,
        "x-small": 6.94,
        "small": 8.33,
        "medium": 10,
        "large": 12,
        "x-large": 14.4,
        "xx-large": 17.28,
    }
    if isinstance(value, str):
        if value not in sizes:
            raise ValueError(f"gsc.pl.umap: unknown legend_fontsize {value!r}.")
        value = sizes[value]
    return _number(10 if value is None else value, "legend_fontsize") * POINTS_TO_PIXELS


def umap_style(
    *,
    count: int,
    width: float | None,
    height: float | None,
    frameon: bool,
    legend_loc: str | None,
    colorbar_loc: str | None,
    legend_fontsize: float | str | None,
    ncols: int,
    hspace: float,
    wspace: float | None,
    alpha: Any,
    edgecolor: Any,
    linewidth: Any,
    na_color: Any,
) -> UMAPStyle:
    if isinstance(ncols, bool) or not isinstance(ncols, Integral) or ncols < 1:
        raise ValueError("gsc.pl.umap: ncols must be a positive integer.")
    opacity = _number(1 if alpha is None else alpha, "alpha")
    if opacity > 1:
        raise ValueError("gsc.pl.umap: alpha must be a scalar between 0 and 1.")
    no_edge = isinstance(edgecolor, str) and edgecolor.lower() == "none"
    edge = "black" if no_edge else native_color(edgecolor, "edgecolor")
    return UMAPStyle(
        width=300 if width is None else width,
        height=300 if height is None else height,
        frameon=frameon,
        legend_loc=legend_loc,
        colorbar_loc=colorbar_loc,
        legend_fontsize=_font_size(legend_fontsize),
        ncols=min(ncols, count),
        hspace=_number(hspace, "hspace"),
        wspace=0.2 if wspace is None else _number(wspace, "wspace"),
        alpha=opacity,
        stroke=edge,
        na_color=native_color(na_color, "na_color"),
        stroke_opacity=0 if no_edge else opacity,
        stroke_width=_number(1.5 if linewidth is None else linewidth, "linewidth")
        * POINTS_TO_PIXELS,
    )
