"""Native cell heatmap using shared positions, labels, palettes and tree branches."""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.schema import ViewBackground
from genome_spy.integrations.scanpy._grid_interactions import (
    zoom_axes,
    with_values,
)
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._grouped_chart import (
    _brackets,
    _slot_labels,
    bracket_space,
    coordinate,
    feature_gaps,
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
    zoom: bool | Literal["xy"],
    show_values: bool,
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
    x, y = zoom_axes(x, y, enabled=zoom, name="heatmap")
    cell_gaps = prepared.intervals["stop"].iloc[:-1].tolist()
    gene_gaps = feature_gaps(feature_groups, genes)
    scales = gs.scales(
        x=gs.Scale(
            type="index",
            **x.scale(gapPositions=cell_gaps if swap_axes else gene_gaps).to_dict()[
                "scale"
            ],
        ),
        y=gs.Scale(
            type="index",
            **y.scale(gapPositions=gene_gaps if swap_axes else cell_gaps).to_dict()[
                "scale"
            ],
        ),
    )
    # The surround owns the scales; marks only declare fields and axes.
    x, y = gs.X("_x:I").axis(None), gs.Y("_y:I").axis(None)
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
                    offset=15,
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
    center = (
        with_values(tiles, "_value", alpha=alpha) if show_values else gs.layer(tiles)
    )
    center = center.properties(
        name="heatmap-cells",
        width=width,
        height=height,
        view=ViewBackground(stroke="black", strokeWidth=0.8 * PT),
    )
    sides: dict[str, Any] = {}
    gene_axis, cell_axis = (y.axis(None), x) if swap_axes else (x.axis(None), y)
    gene_side, cell_side = ("left", "bottom") if swap_axes else ("bottom", "left")
    if show_gene_labels:
        sides[gene_side] = [
            _slot_labels(
                list(values.columns.astype(str)),
                gene_axis,
                horizontal=not swap_axes,
                in_bounds=True,
            ).properties(name="heatmap-genes")
        ]

    # All side views inherit the same final cell and gene slots as the tiles.
    intervals = prepared.intervals
    group_labels = intervals["label"].tolist()
    centers = intervals["center"].tolist()
    group_color = gs.Color("label:N").scale(domain=group_labels)
    group_color = (
        group_color.scale(scheme=palette_scheme)
        if palette_scheme
        else group_color.scale(range=list(palette))
    ).legend(None)
    if categorical:
        strip = _category_strip(
            list(values.index.astype(str)),
            cell_axis,
            group_color,
            horizontal=swap_axes,
            title=groupby,
            hover=hover,
        )
        labels = _slot_labels(
            group_labels,
            cell_axis,
            horizontal=swap_axes,
            positions=centers,
            in_bounds=True,
        ).properties(
            name="heatmap-groups",
            title=gs.Title(
                text=groupby,
                orient="bottom" if swap_axes else "left",
                angle=0 if swap_axes else -90,
                font=FONT,
                fontSize=10 * PT,
                fontWeight="normal",
            ),
        )
        tracks = [strip, labels] if swap_axes else [labels, strip]
        sides[cell_side] = gs.SurroundSideSpec(views=tracks, spacing=8)

    # Preserve Scanpy's colored marker strip for swapped heatmaps.
    if feature_groups and swap_axes:
        matched = {group.label for group in feature_groups}.issubset(group_labels)
        marker_rows = [
            {
                "slot": slot,
                "label": group.label
                if matched
                else group_labels[min(i, len(group_labels) - 1)],
            }
            for i, group in enumerate(feature_groups)
            for slot in range(group.start, group.end + 1)
        ]
        sides["right"] = [
            gs.Chart(marker_rows)
            .mark_rect(clip=True, tooltip=None)
            .encode(
                y=gene_axis.field("slot"),
                color=group_color,
            )
            .properties(width=12, name="heatmap-marker-strip")
        ]
    elif feature_groups:
        sides["top"] = [
            gs.layer(
                *_brackets(
                    feature_groups,
                    gene_axis,
                    swapped=False,
                    rotation=rotation,
                    end_band=0.8,
                    zoom=bool(zoom),
                    in_bounds=True,
                )
            ).properties(height=bracket_space(feature_groups), name="heatmap-brackets")
        ]
    if tree is not None:
        sides["top" if swap_axes else "right"] = [
            tree_track(
                tree,
                centers,
                horizontal=swap_axes,
                size=80 if swap_axes else 100,
            ).properties(name="heatmap-tree")
        ]

    return (
        gs.surround(center, surround=gs.SurroundSides(**sides), spacing=0)
        .properties(scales=scales)
        .resolve_legend(color="collected")
        .configure_legend(
            labelFont=FONT,
            labelFontSize=TICK,
            titleFont=FONT,
            layout={"anchor": "end", "direction": "vertical", "wrap": False},
        )
    )


def _category_strip(
    labels: list[str],
    coordinate: Any,
    color: gs.Color,
    *,
    horizontal: bool,
    title: str,
    hover: bool,
) -> gs.Chart:
    """Return one native category band per cell, sharing the gapped cell axis.

    A small metadata table keeps gaps and tooltips aligned without copying expression.
    """
    strip = gs.Chart([{"slot": i, "label": label} for i, label in enumerate(labels)])
    strip = strip.mark_rect(
        clip=True,
        minHeight=0,
        minOpacity=1,
        tooltip={"handler": "default"} if hover else None,
    ).encode(color=color, **{"x" if horizontal else "y": coordinate.field("slot")})
    if hover:
        strip = strip.encode(tooltip=[gs.Tooltip("label:N", title=title)])
    strip = strip.properties(name="heatmap-category-strip")
    return strip.properties(height=14) if horizontal else strip.properties(width=14)
