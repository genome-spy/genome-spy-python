"""Native embedding marks, guides, and panel composition."""

from __future__ import annotations

from typing import Literal

import numpy as np

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._embedding_data import Panel, PreparedEmbedding
from genome_spy.integrations.scanpy._embedding_interactions import (
    brush_owner,
    point_interactions,
    validate_brush,
    with_brush_count,
)
from genome_spy.integrations.scanpy._style import (
    EMBEDDING_MARKERS,
    POINTS_TO_PIXELS,
    EmbeddingStyle,
)


def coordinate_domain(values: np.ndarray, margin: float) -> tuple[float, float]:
    """Return coordinate limits with the requested margin, widening constant values."""
    low, high = float(values.min()), float(values.max())
    if low == high:
        padding = abs(low) * 0.05 or 0.05
        low, high = low - padding, high + padding
    padding = (high - low) * margin
    return low - padding, high + padding


def _coordinate(
    field: str,
    dimension: int,
    values: np.ndarray,
    style: EmbeddingStyle,
    zoom: bool,
    *,
    horizontal: bool,
    label: str,
    basis: str,
    show_ticks: bool,
) -> gs.X | gs.Y:
    """Return an x or y encoding from a panel's coordinates and style.

    Set fixed initial limits and optional zoom so the stored embedding is retained.
    """
    channel = gs.X if horizontal else gs.Y
    margin = style.xmargin if horizontal else style.ymargin
    result = channel(f"{field}:Q").scale(
        domain=list(coordinate_domain(values, margin)),
        zero=False,
        nice=False,
        zoom=zoom,
    )
    if zoom:
        result = result.scale(name=f"{basis}-{'x' if horizontal else 'y'}-{dimension}")
    if not style.frameon:
        return result.axis(None)
    return result.axis(
        title=label,
        ticks=show_ticks,
        labels=show_ticks,
        labelFontSize=style.tick_fontsize,
        labelFont=style.font,
        domain=False,
        titleFontSize=style.axis_fontsize,
        titleFont=style.font,
    )


def _legend(panel: Panel, style: EmbeddingStyle) -> gs.Legend | None:
    """Return the panel's category legend or colorbar from its data and style.

    Return None when the requested placement does not use an external guide.
    """
    if panel.categorical:
        if panel.key is None or style.legend_loc != "right margin":
            return None
        count = len(panel.legend_values)
        # Add columns only when a single column would make the legend too tall.
        columns = 1
        if count > 30:
            columns = 3
        elif count > 14:
            columns = 2
        legend = gs.Legend(
            title=None,
            values=list(panel.legend_values),
            symbolOpacity=1 if style.outline_width is not None else style.alpha,
            labelLimit=1000,
        )
        if style.legend_symbol_type is None and panel.marker == "D":
            # Scatter legends retain the diamond path's diagonal width too.
            legend = legend.symbolSize(
                style.legend_symbol_size
                * (POINTS_TO_PIXELS * EMBEDDING_MARKERS[panel.marker][1]) ** 2
            )
        # Moving the continuous guide must not move categorical legends.
        if style.colorbar_loc not in (None, "right"):
            legend = legend.orient("right").direction("vertical")
        return legend.columns(columns) if columns > 1 else legend
    if style.colorbar_loc is None:
        return None
    return gs.Legend(title=None, gradientOpacity=style.alpha)


def _color(panel: Panel, index: int, style: EmbeddingStyle) -> gs.Color:
    """Return a color encoding and guide from a prepared panel and its table index.

    Keep category palettes, numeric ranges and constant-value colors faithful.
    """
    color = gs.Color(f"_color_{index}:N" if panel.categorical else f"_color_{index}:Q")
    color = color.scale(
        type="ordinal" if panel.categorical else "linear",
        domain=list(panel.domain),
        nice=False,
    )
    if panel.scheme is not None:
        color = color.scale(scheme=panel.scheme)
    else:
        color = color.scale(range=list(panel.palette))
    if not panel.categorical:
        color = color.scale(zero=False, clamp=True)
        # Without a guide, a constant range uses the last color only when centered.
        if panel.domain[0] == panel.domain[-1] and panel.scheme is not None:
            return gs.Color(
                {"datum": 1 if len(panel.domain) == 3 else 0, "type": "quantitative"}
            ).scale(
                type="linear",
                domain=[0, 1],
                scheme=panel.scheme,
                zero=False,
                nice=False,
            )
    return color.legend(_legend(panel, style))


def _panel(
    prepared: PreparedEmbedding,
    panel: Panel,
    index: int,
    style: EmbeddingStyle,
    *,
    hover: bool,
    zoom: bool,
    selection: gs.Parameter | None,
    edges: gs.Chart | None,
) -> gs.TopLevelSpec:
    """Return one embedding panel from prepared cells, panel settings and style.

    Draw points, missing values and labels in order, adding only requested interactions.
    """
    table = prepared.table
    x_field, y_field = [f"_coord_{d}" for d in panel.dimensions]
    visible = table
    if not panel.categorical and not panel.show_missing:
        visible = table.loc[table[f"_value_{index}"].notna()]
    limits = visible[[x_field, y_field]].to_numpy()
    if prepared.edges is not None and not prepared.edges.empty:
        # NetworkX pads edge endpoints before applying the usual axis margins.
        connected = table.loc[
            table["_obs_id"].isin(prepared.edges.to_numpy().ravel()), [x_field, y_field]
        ].to_numpy()
        low, high = connected.min(axis=0), connected.max(axis=0)
        padding = (high - low) * 0.05
        limits = np.vstack([limits, low - padding, high + padding])
    x = _coordinate(
        x_field,
        panel.dimensions[0],
        limits[:, 0],
        style,
        zoom,
        horizontal=True,
        label=prepared.axis_labels[panel.dimensions[0]],
        basis=prepared.basis,
        show_ticks=prepared.show_ticks,
    )
    y = _coordinate(
        y_field,
        panel.dimensions[1],
        limits[:, 1],
        style,
        zoom,
        horizontal=False,
        label=prepared.axis_labels[panel.dimensions[1]],
        basis=prepared.basis,
        show_ticks=prepared.show_ticks,
    )
    # Scanpy uses square points for size; GenomeSpy uses square pixels.
    maximum_size = max(1.0, float(table[f"_size_{index}"].max()))
    shape, path_width = EMBEDDING_MARKERS[panel.marker]
    diameter = POINTS_TO_PIXELS * path_width
    points = (
        gs.Chart(table)
        .transform_collect(sort={"field": f"_order_{index}", "order": "ascending"})
        .mark_point(
            filled=True,
            fillOpacity=style.alpha,
            stroke=style.stroke,
            strokeOpacity=0
            if style.outline_width is not None
            else style.stroke_opacity,
            strokeWidth=0 if style.outline_width is not None else style.stroke_width,
            inwardStroke=False,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
            key=gs.Key("_obs_id"),
            size=gs.Size(f"_size_{index}:Q")
            .scale(
                domain=[0, maximum_size],
                range=[0, maximum_size * diameter**2],
                nice=False,
                zero=True,
            )
            .legend(None),
        )
        .properties(width=style.width, height=style.height)
    )
    if shape != "circle":
        points = points.encode(shape=gs.value(shape))
    layers: list[gs.TopLevelSpec] = []
    if edges is not None:
        layers.append(
            edges.encode(
                x=x.field("_edge_x"),
                x2=gs.X2("_edge_x2"),
                y=y.field("_edge_y"),
                y2=gs.Y2("_edge_y2"),
            )
        )
    source = {}
    if style.outline_width is not None:
        # Share one source and sort across both opaque outlines and the foreground.
        source = {"data": points._kwds["data"], "transform": points._kwds["transform"]}
        points = points._copy(deep=False, data=Undefined, transform=Undefined)
        background, gap = style.outline_width
        for factor, color in zip(
            (1 + 2 * gap + 2 * background, 1 + 2 * gap),
            style.outline_color,
            strict=True,
        ):
            # Zero-size observations must not leave a painted outline edge.
            outline = (
                points.transform_filter(f"datum._size_{index} > 0")
                .mark_point(
                    filled=True,
                    fillOpacity=1,
                    stroke=style.stroke,
                    strokeOpacity=style.stroke_opacity,
                    strokeWidth=style.stroke_width if style.stroke_opacity else 0,
                    inwardStroke=False,
                    tooltip=None,
                )
                .encode(
                    color=gs.value(color),
                    size=gs.Size(f"_size_{index}:Q")
                    .scale(
                        domain=[0, maximum_size],
                        range=[0, maximum_size * (diameter * factor) ** 2],
                        nice=False,
                        zero=True,
                    )
                    .legend(None),
                )
            )
            layers.append(
                point_interactions(
                    outline,
                    panel,
                    index,
                    axis_labels=prepared.axis_labels,
                    row_label=prepared.row_label,
                    hover=False,
                    selection=selection,
                    opacity=1,
                    stroke_opacity=style.stroke_opacity,
                )
            )
    points = point_interactions(
        points,
        panel,
        index,
        axis_labels=prepared.axis_labels,
        row_label=prepared.row_label,
        hover=hover,
        selection=selection,
        opacity=style.alpha,
        stroke_opacity=0 if style.outline_width is not None else style.stroke_opacity,
    )
    colored = points.encode(color=_color(panel, index, style))
    # Draw missing values separately because numeric color scales cannot color them.
    separate_missing = (
        panel.scheme is not None and table[f"_value_{index}"].isna().any()
    )
    if separate_missing:
        if panel.show_missing:
            layers.append(
                points.transform_filter(f"!isValid(datum._value_{index})").encode(
                    color=gs.value(style.na_color)
                )
            )
        colored = colored.transform_filter(f"isValid(datum._value_{index})")
    layers.append(colored)
    # Place each group label at the middle of its cells, as Scanpy does.
    if panel.categorical and style.legend_loc == "on data":
        labels = [
            {
                "label": label,
                "x": float(
                    table.loc[table[f"_color_{index}"] == label, x_field].median()
                ),
                "y": float(
                    table.loc[table[f"_color_{index}"] == label, y_field].median()
                ),
            }
            for label in panel.legend_values
            if (table[f"_color_{index}"] == label).any()
        ]
        layers.append(
            gs.Chart(labels)
            .mark_text(size=style.legend_fontsize, font=style.font, fontWeight="normal")
            .encode(x=x.field("x"), y=y.field("y"), text="label:N")
        )
    result = (gs.layer(*layers) if len(layers) > 1 else colored).properties(
        width=style.width, height=style.height
    )
    if style.outline_width is not None:
        result = result.properties(**source).resolve_scale(size="independent")
    # Only the first panel edits the brush; other panels show its selection.
    if selection is not None and index == 0:
        result = brush_owner(result, selection, prepared.basis)
    if panel.title:
        result = result.properties(
            title=gs.title(panel.title, fontSize=style.title_fontsize, font=style.font)
        )
    return result.configure_view(
        stroke=style.frame_color if style.frameon else "transparent",
        strokeWidth=style.frame_width if style.frameon else 0,
    ).configure_legend(
        labelFont=style.font,
        labelFontSize=style.legend_fontsize
        if panel.categorical
        else style.tick_fontsize,
        rowPadding=style.legend_labelspacing * style.legend_fontsize,
        labelOffset=style.legend_handletextpad * style.legend_fontsize,
        layout={"anchor": "middle", "wrap": False},
    )


def _compose(
    charts: list[gs.TopLevelSpec], style: EmbeddingStyle, *, share_coordinates: bool
) -> gs.TopLevelSpec:
    """Arrange panel charts into rows using the supplied size and spacing settings.

    Return one chart, sharing coordinates only when requested and keeping colors separate.
    """
    if len(charts) == 1:
        return charts[0]
    position: Literal["shared", "independent"] = (
        "shared" if share_coordinates else "independent"
    )
    resolutions: dict[str, Literal["shared", "independent"]] = dict(
        x=position,
        y=position,
        color="independent",
        size="independent",
    )
    rows = [
        gs.hconcat(
            *charts[start : start + style.ncols], spacing=style.wspace * style.width
        ).resolve_scale(**resolutions)
        for start in range(0, len(charts), style.ncols)
    ]
    combined = (
        rows[0]
        if len(rows) == 1
        else gs.vconcat(*rows, spacing=style.hspace * style.height).resolve_scale(
            **resolutions
        )
    )
    return combined.resolve_legend(default="independent")


def build_embedding(
    prepared: PreparedEmbedding,
    style: EmbeddingStyle,
    *,
    hover: bool,
    zoom: bool,
    selection: gs.Parameter | None = None,
) -> gs.TopLevelSpec:
    """Return a composed embedding chart from prepared data, style and interaction options.

    Share zoom for matching coordinates and add the linked brush count when requested.
    """
    if selection is not None:
        validate_brush(prepared)
    edges = None
    if prepared.edges is not None and not prepared.edges.empty:
        # Both endpoints look up the shared cell table; coordinates are sent once.
        cells = {"values": prepared.table.to_dict("records")}
        edges = (
            gs.Chart(prepared.edges)
            .transform_lookup(
                from_=cells,
                key="_obs_id",
                fields="_source",
                values=["_coord_0", "_coord_1"],
                as_=["_edge_x", "_edge_y"],
            )
            .transform_lookup(
                from_=cells,
                key="_obs_id",
                fields="_target",
                values=["_coord_0", "_coord_1"],
                as_=["_edge_x2", "_edge_y2"],
            )
            .mark_rule(
                color=style.edges_color, size=style.edges_width, clip=True, tooltip=None
            )
        )
    charts = [
        _panel(
            prepared,
            panel,
            i,
            style,
            hover=hover,
            zoom=zoom,
            selection=selection,
            edges=edges,
        )
        for i, panel in enumerate(prepared.panels)
    ]
    # Share zoom only when the panels show the same coordinate pair.
    share_coordinates = zoom and len({p.dimensions for p in prepared.panels}) == 1
    chart = _compose(charts, style, share_coordinates=share_coordinates)
    if selection is not None:
        chart = with_brush_count(chart, prepared, style, selection)
    horizontal = style.colorbar_loc in ("top", "bottom")
    gradient_length = style.width if horizontal else style.height
    # Keep presentation defaults overridable through native chart configuration.
    return chart._configure_nested(
        "legend",
        orient=style.colorbar_loc or "right",
        direction="horizontal" if horizontal else "vertical",
        symbolSize=style.legend_symbol_size * POINTS_TO_PIXELS**2,
        symbolType=style.legend_symbol_type
        if style.legend_symbol_type is not None
        else Undefined,
        gradientLength=gradient_length,
        gradientThickness=gradient_length / 30,
        gradientStrokeColor=style.frame_color,
        gradientStrokeWidth=style.frame_width,
    )
