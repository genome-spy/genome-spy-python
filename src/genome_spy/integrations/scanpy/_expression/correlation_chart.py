"""Native correlation tiles, numbers and labels with an optional Python tree."""

from typing import Any

import numpy as np

import genome_spy as gs
from genome_spy.schema.core import SchemeParams
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._data import figsize_pixels, number
from genome_spy.integrations.scanpy._grid_interactions import with_values
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
    color_bounds,
    native_color,
    native_scheme,
)
from genome_spy.integrations.scanpy._expression.grouped_chart import (
    coordinate,
    index_scales,
    _slot_labels,
)


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
    """Return a correlation chart from prepared tree data and appearance options.

    Keep tiles, labels, optional numbers and branches in the same group order;
    use stored correlations rather than computing them during rendering.
    """
    context = "gsc.pl.correlation_matrix"
    n = len(tree.order)
    if figsize is not None:
        width, height = figsize_pixels(figsize, width, height, context=context)
        width -= 180 if dendrogram else 0
        height -= 20
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

    # Both matrix axes must follow the same leaf order when a tree is shown.
    labels = list(tree.order if dendrogram else tree.categories)
    index = [tree.categories.index(label) for label in labels]
    values = tree.correlation[np.ix_(index, index)]

    # Scanpy uses the full correlation range unless the user supplies a bound.
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
    scales = index_scales(x, y)
    x, y = gs.X("_x:I").axis(None), gs.Y("_y:I").axis(None)
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

    # Labels and branches own viewports and inherit the same ordered slots.
    names = list(map(str, labels))
    sides = {
        "top": [
            _slot_labels(names, x, horizontal=True, opposite=True, font_size=10 * _PT)
        ],
        "right": [
            _slot_labels(names, y, horizontal=False, opposite=True, font_size=10 * _PT)
        ],
    }
    center = with_values(tiles, "_correlation") if numbers else gs.layer(tiles)
    if dendrogram:
        sides["left"] = [
            tree_track(tree, list(range(n)), horizontal=False, size=180, reverse=True)
        ]
    return (
        gs.surround(
            center.properties(width=width, height=height, name="correlation-cells"),
            surround=gs.SurroundSides(**sides),
            spacing=0,
        )
        .properties(scales=scales)
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_legend(labelFont=_FONT, labelFontSize=_TICK)
    )
