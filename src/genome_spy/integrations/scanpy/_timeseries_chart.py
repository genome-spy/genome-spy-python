"""Native points, guides and navigation for supplied time-series profiles."""

from collections.abc import Collection, Mapping, Sequence
from typing import Any
from math import ceil

import numpy as np

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grid_interactions import (
    vertical_highlights,
    zoom_axes,
    horizontal_tick_labels,
    profile_ruler,
    profile_segments,
    series_focus,
)
from genome_spy.integrations.scanpy._style import (
    AXIS_TEXT,
    EMBEDDING_MARKERS,
    FONT,
    POINTS_TO_PIXELS as PT,
    native_scheme,
    zoom_point_size,
    color_bounds,
)
from genome_spy.integrations.scanpy._timeseries_data import CONTEXT, prepare_timeseries


def _series_legend(
    size: float, shape: str, *, enabled: bool, style: gs.Legend | None
) -> gs.Legend | None:
    """Return a native series key from point dimensions and optional style overrides."""
    if not enabled:
        return None
    guide = gs.Legend(
        title=None,
        orient="bottom",
        direction="horizontal",
        symbolSize=size,
        symbolStrokeWidth=0,
        symbolType=shape,
    )
    if style is not None:
        guide = guide.copy(**style.to_dict())
    return guide


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
    context: str = CONTEXT,
    xtick_labels: Mapping[float, str] | None = None,
    series_select: bool = False,
    ruler: bool = False,
    realization_length: float | None = None,
    run_select: bool = False,
    connect: bool = False,
    colorbar: bool = False,
    legend_style: gs.Legend | None = None,
) -> gs.TopLevelSpec:
    """Return native points and guides from supplied profiles and plotting options."""
    for name, value in {"xlabel": xlabel, "ylabel": ylabel}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    if not isinstance(legend, bool):
        raise TypeError(f"{context}: legend must be boolean.")
    marker_count = 1
    if not isinstance(marker, str) and isinstance(marker, (Sequence, np.ndarray)):
        marker = list(marker)
        marker_count = len(marker)
        if not marker or any(v != marker[0] for v in marker):
            raise NotImplementedError(
                f"{context}: per-subset marker shapes are unsupported."
            )
        marker = marker[0]
    if not isinstance(marker, str) or marker not in EMBEDDING_MARKERS:
        raise NotImplementedError(
            f"{context}: marker must be one of {tuple(EMBEDDING_MARKERS)}."
        )
    scheme = native_scheme(
        "viridis" if color_map is None else color_map, "color_map", context=context
    )
    width = number(992 if width is None else width, "width", context=context)
    height = number(739.2 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
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
        context=context,
    )
    if marker_count not in (1, prepared.table["_series"].nunique()):
        raise ValueError(f"{context}: marker needs one value or one per subset.")
    x = (
        gs.X("_time:Q")
        .scale(
            domain=sorted(prepared.x_domain),
            reverse=prepared.x_domain[0] > prepared.x_domain[1],
            zero=False,
            nice=False,
            zoom=False,
        )
        .axis(
            title=xlabel if xtick_labels is None else None,
            domain=False,
            labels=xtick_labels is None,
            values=list(xtick_labels) if xtick_labels is not None else Undefined,
        )
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
    # Unnamed scales let independent panels compose without global name collisions.
    x, y = zoom_axes(x, y, enabled="xy" if zoom else False, name=None)
    shape, path_width = EMBEDDING_MARKERS[marker]
    size = 6 * (PT * path_width) ** 2
    focus = None
    opacity = gs.Expression("0.8")
    if series_select:
        focus, opacity = series_focus(
            list(dict.fromkeys(prepared.table["_series"])), "_series"
        )
    source = gs.Chart(prepared.table)
    run = None
    if realization_length is not None and (run_select or connect):
        source = source.transform_calculate(
            _run=gs.expr.format(
                gs.expr.floor(gs.datum._sample / realization_length) + 1, "d"
            )
        )
        if run_select:
            labels = [str(i + 1) for i in range(ceil(len(X) / realization_length))]
            run, run_opacity = series_focus(
                labels, "_run", name="simulation_run", title="Run: "
            )
            opacity = gs.expr.min(opacity, run_opacity)
    guide = _series_legend(
        size, shape, enabled=prepared.legend or colorbar, style=legend_style
    )
    if prepared.color_domain is None:
        labels = list(dict.fromkeys(prepared.table["_series"]))
        scale = gs.Scale(type="ordinal", domain=labels, range=list(prepared.palette))
        paint: dict[str, Any] = {"field": "_series", "type": "nominal", "scale": scale}
    else:
        low, high = prepared.color_domain
        if colorbar:
            low, high, _ = color_bounds(
                np.array([low, high]), None, None, context=context, expand_constant=True
            )
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
    if colorbar and prepared.color_domain is not None:
        fill = fill.legend(
            gs.Legend(
                title=ylabel,
                orient="right",
                gradientLength=height,
                gradientThickness=15,
            )
        )
    points = (
        source.transform_filter(
            "isValid(datum._time) && isValid(datum._value)"
            + (" && isValid(datum._color)" if prepared.color_domain is not None else "")
        )
        .mark_point(
            filled=True,
            size=zoom_point_size(size, zoom),
            strokeWidth=0,
            inwardStroke=False,
            minPickingSize=5,
            clip=True,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x, y=y, fill=fill, stroke=stroke, shape=gs.value(shape), key=gs.Key("_id")
        )
    )
    if focus is not None or run is not None:
        points = points.transform_calculate(_focus_opacity=opacity).encode(
            opacity=gs.Opacity("_focus_opacity:Q").scale(None).legend(None)
        )
    else:
        points = points.encode(opacity=gs.value(0.8))
    if prepared.color_domain is not None and guide is not None and not colorbar:
        first = prepared.table.iloc[0]
        visible = np.isfinite(
            first[["_time", "_value", "_color"]].to_numpy(dtype=float)
        ).all()
        low, high = prepared.color_domain
        color_value = float(first["_color"]) if visible and low != high else 0
        ink = gs.expr(f"scale('fill', {color_value})")
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
    if connect:
        lines = (
            profile_segments(source, ["_series", "_run"], "_time", "_value")
            .transform_calculate(_focus_opacity=opacity)
            .mark_rule(size=1.5, strokeCap="round", clip=True, tooltip=None)
            .encode(
                x=x,
                x2="_next_time:Q",
                y=y,
                y2="_next_value:Q",
                color=gs.Color(**paint).legend(None),
                opacity=gs.Opacity("_focus_opacity:Q").scale(None).legend(None),
            )
        )
        chart = gs.layer(lines, points)
    if highlights:
        chart = chart + vertical_highlights(highlights, *prepared.highlight_y)
    if ruler:
        chart = chart.add_params(profile_ruler())
    result: gs.LayerChart | gs.SurroundChart = chart.properties(
        width=width,
        height=height,
        view={"stroke": "transparent", "strokeWidth": 0},
    )
    if xtick_labels is not None:
        result = gs.surround(
            result,
            surround=gs.SurroundSides(
                bottom=[horizontal_tick_labels(xtick_labels, xlabel)]
            ),
            spacing=0,
        ).resolve_legend(default="collected")
    if focus is not None:
        result = result.add_params(focus)
    if run is not None:
        result = result.add_params(run)
    return result.configure_axis(
        AXIS_TEXT,
        titleFontWeight="normal",
    ).configure_legend(disable=True, labelFont=FONT, labelFontSize=10 * PT)
