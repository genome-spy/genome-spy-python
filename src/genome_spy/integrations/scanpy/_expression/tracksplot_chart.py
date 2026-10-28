"""Native per-cell expression tracks with shared cell positions and side guides."""

from typing import Any

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import (
    coordinate_domain,
    figsize_pixels,
    number,
)
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._expression.grouped_data import (
    FeatureGroup,
    HeatmapData,
)
from genome_spy.integrations.scanpy._expression.grouped_chart import _category_strip
from genome_spy.integrations.scanpy._style import FONT


def _track_bars(
    values: np.ndarray,
    field: str,
    name: str,
    color: gs.Color,
    *,
    log: bool,
    hover: bool,
) -> gs.Chart:
    """Return one gene's bars with its own value range and optional cell tooltips.

    Log tracks hide nonpositive values and use the bottom edge as their baseline.
    """
    finite = values[np.isfinite(values)]
    if log:
        positive = finite[finite > 0]
        domain = coordinate_domain(
            positive if positive.size else np.array([1.0, 10.0]), 0.05, log=True
        )
    else:
        domain = coordinate_domain(np.append(finite, 0), 0.05)

    # Scanpy masks nonpositive log values; their baseline is the viewport bottom.
    bars = (
        gs.Chart()
        .transform_filter(
            f"isValid(datum.{field})" + (f" && datum.{field} > 0" if log else "")
        )
        .mark_rect(
            minWidth=0,
            minHeight=0,
            minOpacity=1,
            clip=True,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=gs.X("_cell:I").axis(None),
            y=gs.Y(f"{field}:Q")
            .scale(
                type="log" if log else "linear",
                domain=list(domain),
                nice=False,
                zero=False,
                zoom=False,
            )
            .axis(
                title=None,
                orient="right",
                values=[int(domain[1]) if not log or domain[1] >= 1 else domain[1]],
                labelBaseline="top",
                grid=False,
                domain=False,
                labelFontSize=10,
            ),
            y2=gs.value(0) if log else gs.Y2(datum=0),
            color=color,
        )
    )
    if hover:
        bars = bars.encode(
            tooltip=[
                gs.Tooltip("_obs_id:N", title="Cell ID"),
                gs.Tooltip("_obs_label:N", title="Cell"),
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip(
                    f"{field}:Q",
                    title=f"{name} expression" + (" (log1p)" if log else ""),
                    format=".4g",
                ),
            ]
        )
    return bars


def build_tracksplot(
    prepared: HeatmapData,
    feature_groups: tuple[FeatureGroup, ...],
    observation_names: np.ndarray,
    observation_ids: np.ndarray,
    *,
    groupby: str,
    categories: list[str],
    palette: tuple[str, ...],
    tree: DendrogramData | None,
    log: bool,
    hover: bool,
    zoom: bool,
    group_gap: float,
    spacing: float,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
    cell_data: pd.DataFrame | None = None,
    value_fields: list[str] | None = None,
    color_scale: gs.Scale | None = None,
    highlight: dict[str, Any] | None = None,
    show_legend: bool = True,
) -> gs.VConcatChart:
    """Return one rect per cell and gene, with independent expression scales.

    Share cell slots across tracks, the category strip and optional group tree.
    Linked charts can supply their cell table and a native selection filter.
    """
    context = "gsc.pl.tracksplot"
    values = prepared.values
    cells, genes = values.shape
    if figsize is not None:
        width, height = figsize_pixels(figsize, width, height, context=context)
        height -= (100 if tree else 0) + 24 + spacing * (genes + int(tree is not None))
    width = number(1200 if width is None else width, "width", context=context)
    height = number(genes * 25 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    if feature_groups and [
        slot for group in feature_groups for slot in range(group.start, group.end + 1)
    ] != list(range(genes)):
        raise NotImplementedError(
            f"{context}: marker spans must cover every gene once, in order."
        )

    # Send cell metadata once; each track reads one selected expression column.
    numeric = values.to_numpy(dtype=float, na_value=np.nan)
    if value_fields is None:
        value_fields = [f"_value_{i}" for i in range(genes)]
    table = (
        cell_data
        if cell_data is not None
        else pd.DataFrame(numeric, columns=value_fields).assign(
            _cell=np.arange(cells),
            _group=np.asarray(values.index.astype(str)),
            _obs_id=observation_ids,
            _obs_label=observation_names,
        )
    )
    if color_scale is None:
        color_scale = gs.Scale(domain=categories, range=list(palette))
    color = gs.Color("_group:N", scale=color_scale).legend(None)
    group_colors = dict(zip(categories, palette, strict=True)) if feature_groups else {}
    # Validated marker spans already follow the displayed gene order.
    marker_colors: list[str] = []
    for block, group in enumerate(feature_groups):
        label = prepared.intervals["label"].iloc[min(block, len(palette) - 1)]
        marker_colors.extend([group_colors[label]] * (group.end - group.start + 1))
    boundaries = (
        gs.Chart(
            [{"_boundary": int(stop)} for stop in prepared.intervals["stop"].iloc[:-1]]
        )
        .mark_rule(
            color="#777777", size=0.5, strokeDash=[3, 3], clip=True, tooltip=None
        )
        .encode(
            x=gs.X("_boundary:I", band=0).axis(None),
            y=gs.value(0),
            y2=gs.value(1),
        )
    )

    # Every gene uses the same zero-line mark on its own value scale.
    baseline = (
        gs.Chart([{}])
        .mark_rule(color="#999999", size=0.5, tooltip=None)
        .encode(y=gs.value(0) if log else gs.Y(datum=0, type="quantitative"))
    )

    # Each gene keeps its own value range while sharing cell positions.
    tracks: list[gs.TopLevelSpec] = []
    for slot, name in enumerate(values.columns):
        field = value_fields[slot]
        bars = _track_bars(
            numeric[:, slot], field, str(name), color, log=log, hover=hover
        )
        marks = [bars]
        if highlight is not None:
            # Keep the full profile as context; selected cells retain their fixed slots.
            marks = [
                bars.encode(opacity=gs.value(0.15)).properties(
                    name=f"tracks-all-{slot}"
                ),
                bars.transform_filter(**highlight).properties(
                    name=f"tracks-selected-{slot}"
                ),
            ]
        track: gs.LayerChart | gs.SurroundChart = gs.layer(
            *marks, baseline, boundaries
        ).properties(width=width, height=height / genes)
        if feature_groups:
            marker = (
                gs.Chart([{}])
                .mark_rect(
                    color=marker_colors[slot],
                    tooltip=None,
                )
                .properties(width=10)
            )
            track = gs.surround(
                track, surround=gs.SurroundSides(right=[marker]), spacing=4
            )
        tracks.append(
            track.properties(
                title=gs.Title(
                    text=str(name),
                    orient="left",
                    angle=0,
                    align="right",
                    font=FONT,
                    fontSize=11,
                    fontWeight="normal",
                    offset=8,
                )
            )
        )

    # Group labels and the tree follow the same positions as every track.
    strip_color = gs.Color("label:N", scale=color_scale).legend(
        gs.Legend(title=groupby, orient="bottom", columns=2) if show_legend else None
    )
    strip = _category_strip(
        list(values.index.astype(str)),
        gs.X("slot:I").axis(None),
        strip_color,
        horizontal=True,
        title=groupby,
        hover=hover,
    )
    if tree is not None:
        tracks.insert(
            0,
            tree_track(
                tree, prepared.intervals["center"].tolist(), horizontal=True, size=100
            ).properties(width=width),
        )
    return (
        gs.vconcat(*tracks, strip, spacing=spacing)
        .properties(
            data=table,
            width=width,
            scales=gs.scales(
                x=gs.Scale(
                    type="index",
                    domain=[0, cells - 1],
                    paddingOuter=0,
                    zoom=zoom,
                    gapPositions=prepared.intervals["stop"].iloc[:-1].tolist(),
                    gapWidth=group_gap,
                )
            ),
        )
        .resolve_scale(x="shared", y="independent", color="shared")
        .resolve_axis(x="independent", y="independent")
        .resolve_legend(default="collected")
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_axis(labelFont=FONT)
        .configure_legend(labelFont=FONT, layout={"anchor": "middle"})
    )
