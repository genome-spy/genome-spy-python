"""Native embedding marks, guides, and panel composition."""

from __future__ import annotations

from typing import Literal

import numpy as np

import genome_spy as gs
from genome_spy.schema.core import LegendConfig
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._data import coordinate_domain
from genome_spy.integrations.scanpy._embedding.data import Panel, PreparedEmbedding
from genome_spy.integrations.scanpy._embedding.interactions import (
    brush_owner,
    point_hover,
    validate_brush,
    with_brush_count,
)
from genome_spy.integrations.scanpy._labels import displaced_labels
from genome_spy.integrations.scanpy._style import (
    EMBEDDING_MARKERS,
    POINTS_TO_PIXELS,
    EmbeddingStyle,
    zoom_point_size,
)


def _coordinate(
    field: str,
    values: np.ndarray,
    style: EmbeddingStyle,
    zoom: bool,
    *,
    horizontal: bool,
    label: str,
    show_ticks: bool,
    domain: tuple[float, float] | None = None,
) -> gs.X | gs.Y:
    """Return an x or y encoding from a panel's coordinates and style.

    Set fixed initial limits and optional zoom so the stored embedding is retained.
    """
    channel = gs.X if horizontal else gs.Y
    margin = style.xmargin if horizontal else style.ymargin
    result = channel(f"{field}:Q").scale(
        domain=list(coordinate_domain(values, margin) if domain is None else domain),
        zero=False,
        nice=False,
        zoom=zoom,
    )
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
        if panel.marker == "D":
            # Legend diamonds retain the point path's diagonal width too.
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


def _legend_typography(panel: Panel, style: EmbeddingStyle) -> LegendConfig:
    """Return shared guide text settings, retaining separate colorbar tick sizing."""
    return LegendConfig(
        labelFont=style.font,
        labelFontSize=style.legend_fontsize
        if panel.categorical
        else style.tick_fontsize,
        rowPadding=style.legend_labelspacing * style.legend_fontsize,
        labelOffset=style.legend_handletextpad * style.legend_fontsize,
        layout={"anchor": "middle", "wrap": False},
    )


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


def _point_size(index: int, maximum: float, diameter: float, *, zoom: bool) -> gs.Size:
    """Map prepared point areas to pixels, sharing zoom sizing with the outlines."""
    return (
        gs.Size(f"_size_{index}:Q")
        .scale(
            domain=[0, maximum],
            range=[0, zoom_point_size(maximum * diameter**2, zoom)],
            nice=False,
            zero=True,
        )
        .legend(None)
    )


def _outline_layers(
    points: gs.Chart,
    index: int,
    style: EmbeddingStyle,
    maximum_size: float,
    diameter: float,
    *,
    zoom: bool,
) -> list[gs.Chart]:
    """Return the two background point layers from outline widths and colors.

    Keep zero-size cells hidden and use the same zoom sizing as the foreground.
    """
    assert style.outline_width is not None
    layers = []
    background, gap = style.outline_width
    for factor, color in zip(
        (1 + 2 * gap + 2 * background, 1 + 2 * gap),
        style.outline_color,
        strict=True,
    ):
        outline = points.mark_point(
            filled=True,
            fillOpacity=1,
            stroke=style.stroke,
            strokeOpacity=style.stroke_opacity,
            strokeWidth=style.stroke_width if style.stroke_opacity else 0,
            inwardStroke=False,
            tooltip=None,
        ).encode(
            color=gs.value(color),
            size=_point_size(index, maximum_size, diameter * factor, zoom=zoom),
        )
        layers.append(outline)
    return layers


def _color_layers(
    points: gs.Chart,
    prepared: PreparedEmbedding,
    panel: Panel,
    index: int,
    style: EmbeddingStyle,
) -> list[gs.Chart]:
    """Return point layers for regular, missing and out-of-range colors.

    Separate missing values because numeric scales cannot assign their color.
    """
    table = prepared.table
    layers = []
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
    if panel.color_extremes is not None:
        field = f"datum._color_{index}"
        low, high = panel.domain[0], panel.domain[-1]
        if (table[f"_color_{index}"] < low).any():
            layers.append(
                points.transform_filter(f"{field} < {low!r}").encode(
                    color=gs.value(panel.color_extremes[0])
                )
            )
        layers.append(
            colored.transform_filter(f"{low!r} <= {field} && {field} <= {high!r}")
        )
        if (table[f"_color_{index}"] > high).any():
            layers.append(
                points.transform_filter(f"{field} > {high!r}").encode(
                    color=gs.value(panel.color_extremes[1])
                )
            )
    else:
        layers.append(colored)
    return layers


def _panel_limits(prepared: PreparedEmbedding, panel: Panel, index: int) -> np.ndarray:
    """Return visible coordinates with padding around stored graph endpoints.

    Missing-value cells and graph edges affect Scanpy's initial plot limits.
    """
    table = prepared.table
    fields = [f"_coord_{d}" for d in panel.dimensions]
    visible = table
    if not panel.categorical and not panel.show_missing:
        visible = table.loc[table[f"_value_{index}"].notna()]
    limits: np.ndarray = visible[fields].to_numpy()
    if prepared.edges is None or prepared.edges.empty:
        return limits

    # NetworkX pads edge endpoints before applying the usual axis margins.
    connected = table.loc[
        table["_obs_id"].isin(prepared.edges.to_numpy().ravel()), fields
    ].to_numpy()
    low, high = connected.min(axis=0), connected.max(axis=0)
    padding = (high - low) * 0.05
    return np.vstack([limits, low - padding, high + padding])


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
    coordinate_domains: tuple[tuple[float, float], tuple[float, float]] | None = None,
) -> gs.TopLevelSpec:
    """Return one embedding panel from prepared cells, panel settings and style.

    Draw points, missing values and labels in order, adding only requested interactions.
    """
    table = prepared.table
    x_field, y_field = [f"_coord_{d}" for d in panel.dimensions]
    limits = _panel_limits(prepared, panel, index)
    x = _coordinate(
        x_field,
        limits[:, 0],
        style,
        zoom,
        horizontal=True,
        label=prepared.axis_labels[panel.dimensions[0]],
        show_ticks=prepared.show_ticks,
        domain=None if coordinate_domains is None else coordinate_domains[0],
    )
    y = _coordinate(
        y_field,
        limits[:, 1],
        style,
        zoom,
        horizontal=False,
        label=prepared.axis_labels[panel.dimensions[1]],
        show_ticks=prepared.show_ticks,
        domain=None if coordinate_domains is None else coordinate_domains[1],
    )

    # Scanpy uses square points for size; GenomeSpy uses square pixels.
    maximum_size = max(1.0, float(table[f"_size_{index}"].max()))
    shape, path_width = EMBEDDING_MARKERS[panel.marker]
    diameter = POINTS_TO_PIXELS * path_width
    points = (
        gs.Chart(table)
        # Keep browser-side row copies small by dropping other panels' fields.
        .transform_project(
            fields=[
                "_obs_id",
                "_obs_label",
                x_field,
                y_field,
                f"_value_{index}",
                f"_color_{index}",
                f"_size_{index}",
                f"_order_{index}",
            ]
        )
        # Invisible observations must not become hover targets.
        .transform_filter(f"datum._size_{index} > 0")
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
            minPickingSize=5,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
            key=gs.Key("_obs_id"),
            size=_point_size(index, maximum_size, diameter, zoom=zoom),
        )
        .properties(width=style.width, height=style.height)
    )
    if shape != "circle":
        points = points.encode(shape=gs.value(shape))

    # Keep edges behind all point layers, including outlines.
    layers: list[gs.Chart] = []
    if edges is not None:
        layers.append(
            edges.encode(
                x=x.field("_edge_x"),
                x2=gs.X2("_edge_x2"),
                y=y.field("_edge_y"),
                y2=gs.Y2("_edge_y2"),
            )
        )

    # Outlines and extreme colors must inherit the same source and draw order.
    source = {}
    if style.outline_width is not None or panel.color_extremes is not None:
        source = {"data": points._kwds["data"], "transform": points._kwds["transform"]}
        points = points._copy(deep=False, data=Undefined, transform=Undefined)
    if style.outline_width is not None:
        layers.extend(
            _outline_layers(points, index, style, maximum_size, diameter, zoom=zoom)
        )

    # Only foreground points expose cell details.
    points = point_hover(
        points,
        panel,
        index,
        axis_labels=prepared.axis_labels,
        row_label=prepared.row_label,
        hover=hover,
    )
    layers.extend(_color_layers(points, prepared, panel, index, style))

    # Keep group medians as anchors while native layout separates their labels.
    if panel.categorical and style.legend_loc == "on data":
        labels = []
        for label in panel.legend_values:
            members = table[f"_color_{index}"] == label
            if not members.any():
                continue
            labels.append(
                {
                    "label": label,
                    "x": float(table.loc[members, x_field].median()),
                    "y": float(table.loc[members, y_field].median()),
                }
            )
        layers.append(
            displaced_labels(
                gs.Chart(labels),
                key="label",
                text="label",
                x="x",
                y="y",
                size=style.legend_fontsize,
                font=style.font,
            ).encode(x=x.field("x"), y=y.field("y"))
        )

    # Size ranges use each mark's zoom, so layers keep their own size scales.
    result = (
        gs.layer(*layers).resolve_scale(size="independent")
        if len(layers) > 1
        else layers[0]
    ).properties(width=style.width, height=style.height)
    if source:
        result = result.properties(**source)

    # Only the first panel edits the shared brush bounds.
    if selection is not None and index == 0:
        result = brush_owner(result, selection, prepared.basis)
    if panel.title:
        result = result.properties(
            title=gs.title(panel.title, fontSize=style.title_fontsize, font=style.font)
        )
    return result.configure_view(
        stroke=style.frame_color if style.frameon else "transparent",
        strokeWidth=style.frame_width if style.frameon else 0,
    ).configure_legend(_legend_typography(panel, style))


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
    coordinate_domains: tuple[tuple[float, float], tuple[float, float]] | None = None,
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
            coordinate_domains=coordinate_domains,
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

    # A single panel is also the root, so retain its text settings when configuring it.
    legend = (
        _legend_typography(prepared.panels[0], style)
        if len(charts) == 1
        else LegendConfig()
    )

    # Keep presentation defaults overridable through native chart configuration.
    return chart._configure_nested(
        "legend",
        legend,
        orient=style.colorbar_loc or "right",
        direction="horizontal" if horizontal else "vertical",
        symbolSize=style.legend_symbol_size * POINTS_TO_PIXELS**2,
        gradientLength=gradient_length,
        gradientThickness=gradient_length / 30,
        gradientStrokeColor=style.frame_color,
        gradientStrokeWidth=style.frame_width,
    )
