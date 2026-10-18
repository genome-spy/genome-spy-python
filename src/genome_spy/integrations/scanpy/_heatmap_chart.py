"""Native cell heatmap using shared positions, labels, palettes and tree branches."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._dendrogram_chart import tree_overlay
from genome_spy.integrations.scanpy._grouped_chart import (
    _brackets,
    _slot_labels,
    bracket_space,
    coordinate,
)
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup, HeatmapData
from genome_spy.integrations.scanpy._style import (
    FONT,
    GROUPED_FONT_SIZE as TICK,
    POINTS_TO_PIXELS as PT,
    color_bounds,
    native_scheme,
)


def build_heatmap(
    prepared: HeatmapData,
    feature_groups: tuple[FeatureGroup, ...],
    observation_names: np.ndarray,
    observation_ids: np.ndarray,
    *,
    groupby: str,
    palette: tuple[str, ...],
    palette_scheme: str | None,
    tree: DendrogramData | None,
    swap_axes: bool,
    show_gene_labels: bool | None,
    rotation: float | None,
    cmap: Any,
    vmin: float | None,
    vmax: float | None,
    alpha: float | None,
    hover: bool,
    scaled: bool,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
) -> gs.TopLevelSpec:
    """Return cell tiles and aligned annotations from ordered heatmap data.

    Reuse grouped labels and tree branches while keeping each cell's identity.
    """
    context = "gsc.pl.heatmap"
    values = prepared.values
    cells, genes = values.shape
    show_gene_labels = genes <= 50 if show_gene_labels is None else show_gene_labels
    categorical = len(prepared.intervals) > 1
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{context}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{context}: figsize needs width and height in inches.")
        width = number(figsize[0], "figsize width", context=context) * 100
        height = number(figsize[1], "figsize height", context=context) * 100
        if swap_axes:
            height -= (80 if tree else 0) + (13 if categorical else 0)
        else:
            width -= (100 if tree else 0) + (20 if categorical else 0)
    # Default size depends on gene labels; cell count never changes the values.
    default_width = genes * 30 if show_gene_labels else 800
    default_height = 600
    if swap_axes:
        default_width = 1000
        default_height = genes * 18 if show_gene_labels else 400
    width = number(default_width if width is None else width, "width", context=context)
    height = number(
        default_height if height is None else height, "height", context=context
    )
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    if rotation is not None:
        rotation = number(rotation, "var_group_rotation", minimum=-360, context=context)
    alpha = number(1 if alpha is None else alpha, "alpha", context=context)
    if alpha > 1:
        raise ValueError(f"{context}: alpha must be between 0 and 1.")
    scheme = native_scheme("viridis" if cmap is None else cmap, "cmap", context=context)
    numeric = values.to_numpy(dtype=float, na_value=np.nan)
    low, high, _ = color_bounds(numeric, vmin, vmax, context=context)

    # Keep one row per cell–gene pair, including missing values and repeated genes.
    cell, gene = np.indices((cells, genes))
    table = pd.DataFrame(
        {
            "_x": (cell if swap_axes else gene).ravel(),
            "_y": (gene if swap_axes else cell).ravel(),
            "_gene": np.asarray(values.columns.astype(str))[gene.ravel()],
            "_group": np.asarray(values.index.astype(str))[cell.ravel()],
            "_obs_id": observation_ids[cell.ravel()],
            "_obs_label": observation_names[cell.ravel()],
            "_value": numeric.ravel(),
        }
    )
    x = coordinate(gs.X, "_x", cells if swap_axes else genes, 0)
    y = coordinate(gs.Y, "_y", genes if swap_axes else cells, 0, reverse=True)
    # Only genes have ticks; individual cell rows remain unlabeled.
    if show_gene_labels:
        gene_axis = (y if swap_axes else x).axis(
            values=list(range(genes)),
            labels=False,
            title=None,
            domain=False,
            tickColor="black",
            tickSize=(1 if swap_axes else 3.5) * PT,
            tickWidth=0.8 * PT,
        )
        if swap_axes:
            y = gene_axis
        else:
            x = gene_axis
    tiles = (
        gs.Chart(table)
        .transform_filter("isValid(datum._value)")
        .mark_rect(opacity=alpha, tooltip={"handler": "default"} if hover else None)
        .encode(
            x=x,
            y=y,
            color=gs.Color("_value:Q")
            .scale(
                type="linear",
                domain=[low, high],
                scheme=scheme,
                zero=False,
                nice=False,
                clamp=True,
            )
            .legend(
                gs.Legend(
                    title=None,
                    orient="right",
                    direction="vertical",
                    gradientLength=min(height, 400),
                    gradientThickness=15,
                    gradientStrokeColor="black",
                    gradientStrokeWidth=0.8 * PT,
                    offset=(110 if tree and not swap_axes else 15)
                    + (15 if feature_groups and swap_axes else 0),
                )
            ),
        )
    )
    if hover:
        tiles = tiles.encode(
            tooltip=[
                gs.Tooltip("_obs_id:N", title="Cell ID"),
                gs.Tooltip("_obs_label:N", title="Cell"),
                gs.Tooltip("_gene:N", title="Gene"),
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip(
                    "_value:Q",
                    title="Expression (scaled)" if scaled else "Expression",
                    format=".4g",
                ),
            ]
        )
    layers: list[gs.Chart | gs.LayerChart] = [tiles]
    if show_gene_labels:
        layers.append(
            _slot_labels(
                list(values.columns.astype(str)),
                y if swap_axes else x,
                horizontal=not swap_axes,
            )
        )

    # Category spans, labels and tree leaves follow the same cell permutation.
    intervals = prepared.intervals.copy()
    intervals["_start"] = intervals["start"] / cells
    intervals["_stop"] = intervals["stop"] / cells
    intervals["_center"] = intervals["center"] / cells
    group_labels = intervals["label"].tolist()
    group_color = gs.Color("label:N").scale(domain=group_labels)
    group_color = (
        group_color.scale(scheme=palette_scheme)
        if palette_scheme
        else group_color.scale(range=list(palette))
    )
    group_color = group_color.legend(None)
    if categorical:
        annotations = _category_strip(
            intervals, group_color, groupby, swap_axes=swap_axes
        )
        layers.append(annotations)
        boundaries = intervals.iloc[:-1]
        lines = gs.Chart(boundaries).mark_rule(color="black", size=PT, tooltip=None)
        if swap_axes:
            lines = lines.encode(
                x=gs.X("_stop:Q").scale(None).axis(None), y=gs.value(0), y2=gs.value(1)
            )
        else:
            lines = lines.transform_calculate(_boundary="1 - datum._stop").encode(
                y=gs.Y("_boundary:Q").scale(None).axis(None),
                x=gs.value(0),
                x2=gs.value(1),
            )
        layers.append(
            gs.layer(lines)
            .resolve_scale(x="excluded", y="excluded")
            .resolve_axis(x="excluded", y="excluded")
        )

    # Scanpy uses brackets above ordinary heatmaps and a gene strip when swapped.
    if feature_groups and not swap_axes:
        layers.extend(
            _brackets(feature_groups, x, swapped=False, rotation=rotation, end_band=0.8)
        )
    elif feature_groups:
        marker_rows: list[dict[str, Any]] = []
        matched = {group.label for group in feature_groups}.issubset(group_labels)
        for index, group in enumerate(feature_groups):
            color_label = (
                group.label
                if matched
                else group_labels[min(index, len(group_labels) - 1)]
            )
            marker_rows.extend(
                {"_gene": slot, "label": color_label}
                for slot in range(group.start, group.end + 1)
            )
        markers = (
            gs.Chart(marker_rows)
            .mark_rect(xOffset=8, x2Offset=20, clip="never", tooltip=None)
            .encode(
                x=gs.value(1), x2=gs.value(1), y=y.field("_gene"), color=group_color
            )
        )
        layers.append(markers)
    if tree is not None:
        layers.append(
            tree_overlay(
                tree,
                orientation="top" if swap_axes else "right",
                reverse=not swap_axes,
                size=80 if swap_axes else 100,
                leaf_positions=intervals["_center"].tolist(),
            )
        )
    gene_space = (
        max(map(len, map(str, values.columns))) * TICK * 0.65 + 12
        if show_gene_labels
        else 10
    )
    group_space = max(map(len, group_labels)) * TICK * 0.65 + 35 if categorical else 10
    top_space = 10.0
    if tree and swap_axes:
        top_space = 90
    elif feature_groups and not swap_axes:
        top_space = bracket_space(feature_groups)
    return (
        gs.layer(*layers)
        .properties(
            width=width,
            height=height,
            padding={
                "left": gene_space if swap_axes else group_space + 25,
                "bottom": group_space + 25 if swap_axes else gene_space,
                "top": top_space,
                "right": 25,
            },
        )
        .resolve_scale(color="independent")
        .configure_view(stroke="black", strokeWidth=0.8 * PT)
        .configure_legend(
            labelFont=FONT,
            labelFontSize=TICK,
            titleFont=FONT,
            layout={"anchor": "end", "direction": "vertical", "wrap": False},
        )
    )


def _category_strip(
    intervals: pd.DataFrame, color: gs.Color, title: str, *, swap_axes: bool
) -> gs.LayerChart:
    """Return category blocks, centered labels and a title outside the cell matrix.

    Use normalized group spans so the strip remains aligned after resizing.
    """
    strip = gs.Chart(intervals)
    labels = gs.Chart(intervals)
    title_chart = gs.Chart([{"label": title}])
    label_space = max(map(len, intervals["label"])) * TICK * 0.65 + 40
    if swap_axes:
        strip = strip.mark_rect(
            yOffset=8, y2Offset=21, clip="never", tooltip=None
        ).encode(
            x=gs.X("_start:Q").scale(None).axis(None),
            x2="_stop:Q",
            y=gs.value(0),
            y2=gs.value(0),
            color=color,
        )
        rotate = max(map(len, intervals["label"])) >= 3
        labels = labels.mark_text(
            font=FONT,
            size=TICK,
            clip="never",
            tooltip=None,
            angle=-90 if rotate else 0,
            align="right" if rotate else "center",
            baseline="middle" if rotate else "top",
            yOffset=30,
        ).encode(
            x=gs.X("_center:Q").scale(None).axis(None), y=gs.value(0), text="label:N"
        )
        title_chart = title_chart.mark_text(
            font=FONT, size=10 * PT, clip="never", tooltip=None, yOffset=label_space
        ).encode(x=gs.value(0.5), y=gs.value(0), text="label:N")
    else:
        strip = (
            strip.transform_calculate(
                _top="1 - datum._start", _bottom="1 - datum._stop"
            )
            .mark_rect(xOffset=-22, x2Offset=-8, clip="never", tooltip=None)
            .encode(
                y=gs.Y("_top:Q").scale(None).axis(None),
                y2="_bottom:Q",
                x=gs.value(0),
                x2=gs.value(0),
                color=color,
            )
        )
        labels = (
            labels.transform_calculate(_center_y="1 - datum._center")
            .mark_text(
                font=FONT,
                size=TICK,
                clip="never",
                tooltip=None,
                align="right",
                baseline="middle",
                xOffset=-30,
            )
            .encode(
                y=gs.Y("_center_y:Q").scale(None).axis(None),
                x=gs.value(0),
                text="label:N",
            )
        )
        title_chart = title_chart.mark_text(
            font=FONT,
            size=10 * PT,
            clip="never",
            tooltip=None,
            angle=-90,
            xOffset=-label_space,
        ).encode(x=gs.value(0), y=gs.value(0.5), text="label:N")
    return (
        gs.layer(strip, labels, title_chart)
        .resolve_scale(x="excluded", y="excluded")
        .resolve_axis(x="excluded", y="excluded")
    )
