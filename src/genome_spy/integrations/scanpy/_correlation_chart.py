"""Native correlation tiles, numbers and labels with an optional Python tree."""

from typing import Any

import numpy as np

import genome_spy as gs
from genome_spy.schema.core import SchemeParams
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._dendrogram_chart import tree_overlay
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
    color_bounds,
    native_color,
    native_scheme,
)
from genome_spy.integrations.scanpy._grouped_chart import coordinate


def build_correlation_matrix(
    tree: DendrogramData,
    *,
    dendrogram: bool,
    numbers: bool,
    cmap: Any,
    edgecolors: Any,
    linewidth: float,
    vmin: float | None,
    vmax: float | None,
    hover: bool,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
) -> gs.TopLevelSpec:
    context = "gsc.pl.correlation_matrix"
    n = len(tree.order)
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{context}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{context}: figsize needs width and height in inches.")
        width = number(figsize[0], "figsize width", context=context) * 100 - (
            180 if dendrogram else 0
        )
        height = number(figsize[1], "figsize height", context=context) * 100 - 20
    width = number(n * 60 if width is None else width, "width", context=context)
    height = number(n * 60 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    scheme = (
        SchemeParams(name="redblue", extent=[1, 0])
        if cmap is None
        else native_scheme(cmap, "cmap", context=context)
    )
    if edgecolors is None:
        edgecolors = "none" if n > 30 else "black"
    no_edge = isinstance(edgecolors, str) and edgecolors.lower() == "none"
    edge = (
        "black" if no_edge else native_color(edgecolors, "edgecolors", context=context)
    )
    linewidth = number(linewidth, "linewidth", context=context)
    labels = list(tree.order if dendrogram else tree.categories)
    index = [tree.categories.index(label) for label in labels]
    values = tree.correlation[np.ix_(index, index)]
    low, high, _ = color_bounds(
        values,
        -1 if vmin is None and vmax is None else vmin,
        1 if vmax is None and vmin is None else vmax,
        context=context,
    )
    yy, xx = np.indices((n, n))
    table = [
        {
            "_x": int(x),
            "_y": int(y),
            "_row": str(labels[y]),
            "_column": str(labels[x]),
            "_correlation": float(values[y, x]),
        }
        for x, y in zip(xx.ravel(), yy.ravel(), strict=True)
    ]
    x, y = coordinate(gs.X, "_x", n, 0), coordinate(gs.Y, "_y", n, 0)
    tiles = (
        gs.Chart(table)
        .mark_rect(
            stroke=edge,
            strokeWidth=linewidth * _PT,
            strokeOpacity=0 if no_edge else 1,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
            color=gs.Color("_correlation:Q")
            .scale(
                type="linear",
                domain=[low, high],
                nice=False,
                zero=False,
                clamp=True,
                scheme=scheme,
            )
            .legend(
                gs.Legend(
                    orient="bottom",
                    direction="horizontal",
                    gradientLength=width,
                    gradientThickness=20,
                    title=None,
                    offset=12,
                )
            ),
        )
    )
    if hover:
        tiles = tiles.encode(
            tooltip=[
                gs.Tooltip("_row:N", title="Row group"),
                gs.Tooltip("_column:N", title="Column group"),
                gs.Tooltip("_correlation:Q", title="Correlation", format=".4g"),
            ]
        )
    label_table = [{"slot": i, "label": str(label)} for i, label in enumerate(labels)]
    top_labels = (
        gs.Chart(label_table)
        .mark_text(
            font=_FONT,
            size=10 * _PT,
            angle=-45,
            align="left",
            baseline="middle",
            yOffset=-8,
            clip="never",
            tooltip=None,
        )
        .encode(x=x.field("slot"), y=gs.value(1), text="label:N")
    )
    right_labels = (
        gs.Chart(label_table)
        .mark_text(
            font=_FONT,
            size=10 * _PT,
            align="left",
            baseline="middle",
            xOffset=8,
            clip="never",
            tooltip=None,
        )
        .encode(x=gs.value(1), y=y.field("slot"), text="label:N")
    )
    layers: list[gs.Chart | gs.LayerChart] = [tiles, top_labels, right_labels]
    if numbers:
        layers.append(
            gs.Chart(table)
            .mark_text(font=_FONT, size=10 * _PT, color="black", tooltip=None)
            .encode(x=x, y=y, text=gs.Text("_correlation:Q", format=".2f"))
        )
    if dendrogram:
        layers.append(tree_overlay(tree, orientation="left", size=180))
    space = max(len(str(label)) for label in labels) * 10 * _PT * 0.65 + 12
    return (
        gs.layer(*layers)
        .properties(
            width=width,
            height=height,
            padding={
                "left": 190 if dendrogram else 10,
                "top": space,
                "right": space,
                "bottom": 10,
            },
        )
        .configure_view(stroke="black", strokeWidth=0.8 * _PT)
        .configure_legend(labelFont=_FONT, labelFontSize=_TICK)
    )
