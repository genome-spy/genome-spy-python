"""Native PAGA path heatmaps with shared tiles, labels and navigation."""

from collections.abc import Mapping
from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grid_interactions import with_values, zoom_axes
from genome_spy.integrations.scanpy._grouped_chart import _slot_labels
from genome_spy.integrations.scanpy._matrix_chart import matrix_tiles
from genome_spy.integrations.scanpy._paga_path_data import CONTEXT, PagaPathData
from genome_spy.integrations.scanpy._style import (
    FONT,
    POINTS_TO_PIXELS as PT,
    color_bounds,
    native_scheme,
)


def _path_color(values: np.ndarray, scheme: str, *, colorbar: bool) -> gs.Color:
    """Return a native value scale, keeping constant unguided colors at the palette start."""
    low, high, constant = color_bounds(values, None, None, context=CONTEXT)
    if constant and not colorbar:
        low += (high - low) / 2
    return gs.Color("_value:Q").scale(
        type="linear",
        domain=[low, high],
        scheme=scheme,
        zero=False,
        nice=False,
        clamp=True,
    )


def _path_track(
    values: Any, name: str, color: gs.Color, samples: int, height: float, hover: bool
) -> gs.Chart:
    """Stretch one original or smoothed annotation across the profile width, as Scanpy does."""
    edges = np.linspace(-0.5, samples - 0.5, len(values) + 1)
    track = (
        gs.Chart(
            pd.DataFrame({"_start": edges[:-1], "_end": edges[1:], "_value": values})
        )
        .transform_filter("isValid(datum._value)")
        .mark_rect(clip=True, tooltip={"handler": "default"} if hover else None)
        .encode(x=gs.X("_start:Q").axis(None), x2="_end:Q", color=color.legend(None))
        .properties(height=height)
    )
    if hover:
        track = track.encode(tooltip=[gs.Tooltip("_value", title=name)])
    return track


def build_paga_path(
    data: PagaPathData,
    *,
    categories: list[str],
    palette: tuple[str, ...],
    color_map: Any,
    color_maps_annotations: Mapping[str, Any],
    title: str | None,
    ytick_fontsize: float | None,
    title_fontsize: float | None,
    show_node_names: bool,
    show_yticks: bool,
    show_colorbar: bool,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Reuse numeric tiles and native surround tracks for prepared path profiles."""
    default_width = 358.4 if show_colorbar else 448
    width = number(default_width if width is None else width, "width", context=CONTEXT)
    height = number(369.6 if height is None else height, "height", context=CONTEXT)
    tick_size = (
        number(
            10 if ytick_fontsize is None else ytick_fontsize,
            "ytick_fontsize",
            context=CONTEXT,
        )
        * PT
    )
    title_size = (
        number(
            12 if title_fontsize is None else title_fontsize,
            "title_fontsize",
            context=CONTEXT,
        )
        * PT
    )
    if min(width, height, tick_size, title_size) <= 0:
        raise ValueError(f"{CONTEXT}: dimensions and font sizes must be positive.")
    values = data.values.to_numpy().T
    genes, samples = values.shape
    x, y = zoom_axes(
        gs.X("_x:Q").scale(
            type="linear", domain=[-0.5, samples - 0.5], nice=False, zero=False
        ),
        gs.Y("_y:I").scale(type="index", domain=[0, genes - 1], reverse=True),
        enabled=zoom,
        name=None,
    )
    color = _path_color(
        values,
        native_scheme(
            "viridis" if color_map is None else color_map, "color_map", context=CONTEXT
        ),
        colorbar=show_colorbar,
    ).legend(
        gs.Legend(
            title=None,
            orient="right",
            direction="vertical",
            gradientLength=height,
            gradientThickness=15,
            gradientStrokeColor="black",
            gradientStrokeWidth=0.8 * PT,
        )
        if show_colorbar
        else None
    )
    tiles = matrix_tiles(
        values,
        list(map(str, range(samples))),
        list(data.values.columns),
        color=color,
        hover=hover,
    )
    tiles = tiles.transform_calculate(
        _x0="datum._x - 0.5", _x1="datum._x + 0.5"
    ).encode(x=gs.X("_x0:Q").axis(None), x2="_x1:Q", y=gs.Y("_y:I").axis(None))
    center = with_values(tiles, "_value") if show_values else tiles
    center = center.properties(width=width, height=height, name="paga-path-values")
    group_values = np.asarray(categories)[data.groups]
    group_color = gs.Color("_value:N").scale(
        type="ordinal", domain=categories, range=list(palette)
    )
    groups: gs.Chart | gs.LayerChart = _path_track(
        group_values, data.group_key, group_color, samples, height / genes, hover
    )
    if show_node_names:
        # The original group image keeps its own sample count after smoothing.
        centers = (data.boundaries[:-1] + data.boundaries[1:]) / 2
        positions = (centers + 0.5) * samples / len(data.groups) - 0.5
        labels = (
            gs.Chart(pd.DataFrame({"_position": positions, "_label": data.node_names}))
            .mark_text(
                font=FONT,
                size=10 * PT,
                baseline="middle",
                align="center",
                clip=True,
                tooltip=None,
            )
            .encode(x=gs.X("_position:Q").axis(None), y=gs.value(0.5), text="_label:N")
        )
        groups = gs.layer(groups, labels).properties(height=height / genes)
    tracks = [groups.properties(name="paga-path-groups")]
    names = [data.group_key]
    for name in data.annotations:
        series = data.annotations[name]
        scheme = native_scheme(
            color_maps_annotations.get(name, "Greys"),
            f"annotation {name!r}",
            context=CONTEXT,
        )
        tracks.append(
            _path_track(
                series,
                name,
                _path_color(series.to_numpy(), scheme, colorbar=False),
                samples,
                height / genes,
                hover,
            ).properties(name=f"paga-path-annotation-{len(names) - 1}")
        )
        names.append(name)
    if show_yticks:
        tracks = [
            track.properties(
                title=gs.Title(
                    text=name,
                    orient="left",
                    angle=0,
                    anchor="middle",
                    align="right",
                    baseline="middle",
                    font=FONT,
                    fontSize=tick_size,
                    fontWeight="normal",
                    offset=8,
                )
            )
            for track, name in zip(tracks, names, strict=True)
        ]
    sides: dict[str, Any] = {"bottom": gs.SurroundSideSpec(views=tracks, spacing=0)}
    if show_yticks:
        sides["left"] = [
            _slot_labels(
                list(data.values.columns),
                gs.Y("_y:I").axis(None),
                horizontal=False,
                font_size=tick_size,
            )
        ]
    chart = (
        gs.surround(center, surround=gs.SurroundSides(**sides), spacing=0)
        .properties(
            scales=gs.scales(
                x=gs.Scale(**x.to_dict()["scale"]), y=gs.Scale(**y.to_dict()["scale"])
            )
        )
        .resolve_scale(color="independent")
        .resolve_legend(color="independent")
        .configure_view(stroke="transparent", strokeWidth=0)
    )
    if title is not None:
        chart = chart.properties(
            title=gs.Title(
                text=title, font=FONT, fontSize=title_size, fontWeight="normal"
            )
        )
    return chart.configure_legend(labelFont=FONT, labelFontSize=10 * PT)
