"""Native points, guides and navigation for supplied time-series profiles."""

from collections.abc import Collection, Sequence
from typing import Any

import numpy as np

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grid_interactions import (
    vertical_highlights,
    zoom_axes,
)
from genome_spy.integrations.scanpy._style import (
    EMBEDDING_MARKERS,
    FONT,
    POINTS_TO_PIXELS as PT,
    native_scheme,
)
from genome_spy.integrations.scanpy._timeseries_data import CONTEXT, prepare_timeseries


def build_timeseries(
    X: Any,
    *,
    time: Any = None,
    color: Any = None,
    var_names: Collection[str] = (),
    highlights_x: Any = (),
    xlabel: str | None = "",
    ylabel: str | None = "gene expression",
    yticks: Any = None,
    xlim: Any = None,
    legend: bool = True,
    palette: Any = None,
    color_map: Any = "viridis",
    marker: Any = ".",
    hover: bool,
    zoom: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Return native points and guides from supplied profiles using Scanpy's defaults."""
    for name, value in {"xlabel": xlabel, "ylabel": ylabel}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{CONTEXT}: {name} must be a string or None.")
    if not isinstance(legend, bool):
        raise TypeError(f"{CONTEXT}: legend must be boolean.")
    marker_count = 1
    if not isinstance(marker, str) and isinstance(marker, (Sequence, np.ndarray)):
        marker = list(marker)
        marker_count = len(marker)
        if not marker or any(v != marker[0] for v in marker):
            raise NotImplementedError(
                f"{CONTEXT}: per-subset marker shapes are unsupported."
            )
        marker = marker[0]
    if not isinstance(marker, str) or marker not in EMBEDDING_MARKERS:
        raise NotImplementedError(
            f"{CONTEXT}: marker must be one of {tuple(EMBEDDING_MARKERS)}."
        )
    scheme = native_scheme(
        "viridis" if color_map is None else color_map, "color_map", context=CONTEXT
    )
    width = number(992 if width is None else width, "width", context=CONTEXT)
    height = number(739.2 if height is None else height, "height", context=CONTEXT)
    if not width or not height:
        raise ValueError(f"{CONTEXT}: width and height must be positive.")
    prepared, highlights = prepare_timeseries(
        X,
        time=time,
        color=color,
        var_names=var_names,
        highlights_x=highlights_x,
        xlim=xlim,
        yticks=yticks,
        palette=palette,
        legend=legend,
    )
    if marker_count not in (1, prepared.table["_series"].nunique()):
        raise ValueError(f"{CONTEXT}: marker needs one value or one per subset.")
    x = (
        gs.X("_time:Q")
        .scale(
            domain=sorted(prepared.x_domain),
            reverse=prepared.x_domain[0] > prepared.x_domain[1],
            zero=False,
            nice=False,
            zoom=False,
        )
        .axis(title=xlabel, domain=False)
    )
    y = (
        gs.Y("_value:Q")
        .scale(domain=list(prepared.y_domain), zero=False, nice=False, zoom=False)
        .axis(
            title=ylabel,
            values=prepared.yticks if prepared.yticks is not None else Undefined,
            domain=False,
        )
    )
    # Point plots use both axes for navigation, unlike the y-first matrix helper.
    x, y = zoom_axes(x, y, enabled="xy" if zoom else False, name="timeseries")
    shape, path_width = EMBEDDING_MARKERS[marker]
    size = 6 * (PT * path_width) ** 2
    guide = (
        gs.Legend(
            title=None,
            orient="bottom",
            direction="horizontal",
            symbolSize=size,
            symbolStrokeWidth=PT,
            symbolType=shape,
        )
        if prepared.legend
        else None
    )
    if prepared.color_domain is None:
        labels = list(dict.fromkeys(prepared.table["_series"]))
        scale = gs.Scale(type="ordinal", domain=labels, range=list(prepared.palette))
        paint: dict[str, Any] = {"field": "_series", "type": "nominal", "scale": scale}
    else:
        low, high = prepared.color_domain
        scale = gs.Scale(
            type="linear",
            domain=[low, high] if low != high else [0, 1],
            scheme=scheme,
            zero=False,
            nice=False,
            clamp=True,
        )
        paint = {"type": "quantitative", "scale": scale}
        # Matplotlib maps constant numeric colors to the start of the scheme.
        paint.update({"field": "_color"} if low != high else {"datum": 0})
    fill, stroke = gs.Fill(**paint), gs.Stroke(**paint)
    if "field" in paint:
        fill = fill.legend(guide if prepared.color_domain is None else None)
        stroke = stroke.legend(None)
    points = (
        gs.Chart(prepared.table)
        .transform_filter(
            "isValid(datum._time) && isValid(datum._value)"
            + (" && isValid(datum._color)" if prepared.color_domain is not None else "")
        )
        .mark_point(
            filled=True,
            size=size,
            strokeWidth=PT,
            inwardStroke=False,
            clip=True,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x, y=y, fill=fill, stroke=stroke, shape=gs.value(shape), key=gs.Key("_id")
        )
    )
    if prepared.color_domain is not None and guide is not None:
        first = prepared.table.iloc[0]
        visible = np.isfinite(
            first[["_time", "_value", "_color"]].to_numpy(dtype=float)
        ).all()
        ink = gs.expr(
            f"scale('fill', {float(first['_color']) if visible and prepared.color_domain[0] != prepared.color_domain[1] else 0})"
        )
        points = points.encode(
            shape=gs.Shape("_series:N")
            .scale(
                type="ordinal",
                domain=list(dict.fromkeys(prepared.table["_series"])),
                range=[shape],
            )
            .legend(
                guide.symbolFillColor(ink)
                .symbolStrokeColor(ink)
                .symbolOpacity(1 if visible else 0)
            )
        )
    if hover:
        points = points.encode(
            tooltip=[
                gs.Tooltip("_series:N", title="Series"),
                gs.Tooltip("_sample:Q", title="Sample", format="d"),
                gs.Tooltip("_time:Q", title="Time", format=".4g"),
                gs.Tooltip("_value:Q", title="Value", format=".4g"),
            ]
            + (
                [gs.Tooltip("_color:Q", title="Color", format=".4g")]
                if prepared.color_domain is not None
                else []
            )
        )
    chart = gs.layer(points)
    if highlights:
        chart = chart + vertical_highlights(highlights, *prepared.highlight_y)
    return (
        chart.properties(width=width, height=height)
        .configure_axis(
            labelFont=FONT,
            titleFont=FONT,
            labelFontSize=10 * PT,
            titleFontSize=10 * PT,
            titleFontWeight="normal",
        )
        .configure_legend(disable=True, labelFont=FONT, labelFontSize=10 * PT)
        .configure_view(stroke="black", strokeWidth=0.8 * PT)
    )
