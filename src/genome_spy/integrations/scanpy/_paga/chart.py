"""Native group nodes, labels and weighted straight edges for stored PAGA graphs."""

from typing import Any, Literal

import numpy as np
import pandas as pd
import genome_spy as gs
from genome_spy.schemapi import Undefined

from genome_spy.integrations.scanpy._labels import displaced_labels
from genome_spy.integrations.scanpy._data import coordinate_domain, number
from genome_spy.integrations.scanpy._grid_interactions import zoom_axes
from genome_spy.integrations.scanpy._style import (
    AXIS_TEXT,
    FONT,
    POINTS_TO_PIXELS as PT,
    ColorData,
    color_bounds,
    zoom_point_size,
)

CONTEXT = "gsc.pl.paga"


def build_paga_adjacency(
    values: np.ndarray,
    points: pd.DataFrame,
    *,
    as_heatmap: bool,
    color_map: Any,
    hover: bool,
    zoom: bool | Literal["xy"],
    show_values: bool,
    width: float | None,
    height: float | None,
    labels: list[str] | None = None,
) -> gs.TopLevelSpec:
    """Render stored adjacency with shared tiles or labeled connectivity points."""
    from genome_spy.integrations.scanpy._expression.matrix_chart import build_matrix
    from genome_spy.integrations.scanpy._paga.data import adjacency_points

    context = "gsc.pl.paga_adjacency"
    if not as_heatmap:
        points = adjacency_points(values, points)
    if labels is not None:
        points = points.assign(
            _source_label=np.asarray(labels)[points["_x"]],
            _target_label=np.asarray(labels)[
                points["_y"] if as_heatmap else points["_target"]
            ],
        )
    maximum = None
    if as_heatmap:
        # Keep tree dots inside their cells even in dense matrices.
        maximum = gs.expr.pow(
            0.6
            * gs.expr.min(
                gs.Expression("width * bandstep('x', width)"),
                gs.Expression("height * bandstep('y', height)"),
            ),
            2,
        )
    size = zoom_point_size(16, bool(zoom), maximum=maximum)
    dots = gs.Chart(points).mark_point(
        filled=True,
        color="black",
        size=size,
        strokeWidth=0,
        minPickingSize=5,
        clip=True,
        tooltip={"handler": "default"} if hover else None,
    )
    if hover:
        dots = dots.encode(
            tooltip=[
                gs.Tooltip("_x:Q", title="Source group", format="d"),
                gs.Tooltip(
                    "_y:Q" if as_heatmap else "_target:Q",
                    title="Target group",
                    format="d",
                ),
            ]
            + (
                [
                    gs.Tooltip("_source_label:N", title="Source"),
                    gs.Tooltip("_target_label:N", title="Target"),
                ]
                if labels is not None
                else []
            )
            + (
                []
                if as_heatmap
                else [
                    gs.Tooltip("_y:Q", title="Connectivity", format=".4g"),
                    gs.Tooltip("_kind:N", title="Edge"),
                ]
            )
        )
    if not as_heatmap:
        width = number(496 if width is None else width, "width", context=context)
        height = number(369.6 if height is None else height, "height", context=context)
        if not width or not height:
            raise ValueError(f"{context}: width and height must be positive.")
        visible = points.loc[np.isfinite(points["_y"])]
        # Empty plots retain Matplotlib's default limits around zero.
        extent = visible[["_x", "_y"]].to_numpy() if len(visible) else np.zeros((1, 2))
        # Named groups use slots; numeric calls retain Scanpy's original limits.
        if labels is None:
            x = gs.X("_x:Q").scale(
                domain=list(coordinate_domain(extent[:, 0], 0.05)),
                zero=False,
                nice=False,
            )
        else:
            from genome_spy.integrations.scanpy._expression.grouped_chart import (
                coordinate,
            )

            x = coordinate(gs.X, "_x", len(values), 0)
        y = gs.Y("_y:Q").scale(
            domain=list(coordinate_domain(extent[:, 1], 0.05)), zero=False, nice=False
        )
        x, y = zoom_axes(x, y, enabled=zoom, name=None)
        colors = gs.Scale(
            type="ordinal", domain=["Adjacency", "Tree"], range=["#cbd5e1", "#2563a6"]
        )
        chart: gs.Chart | gs.SurroundChart = (
            dots.transform_filter("isValid(datum._y)")
            .encode(
                x=x.axis(
                    title="Source group" if labels is None else None,
                    labels=labels is None,
                ),
                y=y.axis(title="Connectivity"),
                fill=gs.Fill("_kind:N", scale=colors).legend(
                    gs.Legend(
                        title=None,
                        orient="bottom",
                        direction="horizontal",
                        symbolSize=36,
                    )
                ),
                stroke=gs.Stroke("_kind:N", scale=colors).legend(None),
            )
            .properties(
                width=width,
                height=height,
                view={"stroke": "transparent", "strokeWidth": 0},
            )
            .configure_axis(
                AXIS_TEXT,
                titleFontWeight="normal",
            )
        )
        if labels is not None:
            from genome_spy.integrations.scanpy._expression.grouped_chart import (
                _slot_labels,
            )

            source_labels = _slot_labels(
                labels, x.axis(None), horizontal=True
            ).properties(
                title=gs.Title(
                    text="Source group",
                    orient="bottom",
                    offset=4,
                    font=FONT,
                    fontSize=10 * PT,
                    fontWeight="normal",
                )
            )
            chart = gs.surround(
                chart,
                surround=gs.SurroundSides(bottom=[source_labels]),
                spacing=0,
            ).resolve_legend(default="collected")
        return chart.configure_legend(labelFont=FONT, labelFontSize=10 * PT)
    return build_matrix(
        values,
        xlabel=None,
        ylabel=None,
        xticks=labels,
        yticks=labels,
        title=None,
        colorbar_shrink=0.5,
        color_map=color_map,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
        context="gsc.pl.paga_adjacency",
        overlay=dots.encode(x="_x:I", y="_y:I"),
    )


def _network_axes(
    nodes: pd.DataFrame,
    solid: pd.DataFrame,
    dashed: pd.DataFrame,
    *,
    zoom: bool,
) -> tuple[gs.X, gs.Y]:
    """Return axes from node and edge coordinates, retaining Scanpy's initial margins."""
    # Include connected edge endpoints when choosing the initial frame.
    extent = nodes[["_x", "_y"]].to_numpy()
    for edges in (solid, dashed):
        if not edges.empty:
            points = edges[["_x", "_y", "_x2", "_y2"]].to_numpy().reshape(-1, 2)

            # NetworkX adds five percent around edge endpoints before the axes apply their margin.
            padding = np.ptp(points, axis=0) * 0.05
            extent = np.vstack(
                [extent, points.min(axis=0) - padding, points.max(axis=0) + padding]
            )
    x = (
        gs.X("_x:Q")
        .scale(
            domain=list(coordinate_domain(extent[:, 0], 0.05)), zero=False, nice=False
        )
        .axis(None)
    )
    y = (
        gs.Y("_y:Q")
        .scale(
            domain=list(coordinate_domain(extent[:, 1], 0.05)), zero=False, nice=False
        )
        .axis(None)
    )
    x, y = zoom_axes(x, y, enabled="xy" if zoom else False, name=None)
    return x, y


def build_paga(
    nodes: pd.DataFrame,
    solid: pd.DataFrame,
    dashed: pd.DataFrame,
    *,
    fontsize: Any,
    fontweight: str,
    frameon: bool,
    title: str | None,
    hover: bool,
    zoom: bool,
    width: float | None,
    height: float | None,
    cmap: str,
    colorbar: bool,
    group_key: str,
    group_labels: list[str],
    color_title: str,
    color_data: ColorData | None = None,
    edge_slider: bool = False,
    show_node_labels: bool = True,
) -> gs.TopLevelSpec:
    """Return native graph layers with shared coordinates, fixed marker sizes and optional navigation."""
    width = number(548 if width is None else width, "width", context=CONTEXT)
    height = number(384 if height is None else height, "height", context=CONTEXT)
    fontsize = number(10 if fontsize is None else fontsize, "fontsize", context=CONTEXT)
    if not width or not height or not fontsize:
        raise ValueError(f"{CONTEXT}: width, height and fontsize must be positive.")
    if fontweight not in ("normal", "bold"):
        raise NotImplementedError(f"{CONTEXT}: fontweight supports 'normal' or 'bold'.")
    if title is not None and not isinstance(title, str):
        raise TypeError(f"{CONTEXT}: title must be a string or None.")
    x, y = _network_axes(nodes, solid, dashed, zoom=zoom)
    charts = []
    cutoff = None
    if edge_slider:
        weights = [
            float(edges["_weight"].max())
            for edges in (solid, dashed)
            if not edges.empty
        ]
        if not weights:
            raise ValueError(
                f"{CONTEXT}: edge_slider needs at least one stored edge above threshold."
            )
        cutoff = gs.param(
            "paga_edge_cutoff",
            value=0,
            bind=gs.binding_range(
                min=0, max=max(1, *weights), step=0.01, name="Displayed edge cutoff: "
            ),
        )
    edge_maximum = max(
        [1.0]
        + [float(edges["_width"].max()) for edges in (solid, dashed) if not edges.empty]
    )
    for edges, is_dashed in ((dashed, True), (solid, False)):
        if edges.empty:
            continue
        rules = (
            gs.Chart(edges)
            .mark_rule(
                color="grey" if is_dashed else "#999999",
                opacity=0.5 if is_dashed else 1,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
                strokeDash=[round(v * PT) for v in (3.7, 1.6)]
                if is_dashed
                else Undefined,
            )
            .encode(
                x2="_x2:Q",
                y2="_y2:Q",
                size=gs.Size("_width:Q")
                .scale(
                    domain=[0, edge_maximum],
                    range=[0, edge_maximum * PT],
                    zero=True,
                    nice=False,
                )
                .legend(None),
            )
        )
        if cutoff is not None:
            rules = rules.transform_filter(gs.datum._weight >= cutoff)
        if hover:
            rules = rules.encode(
                tooltip=[
                    gs.Tooltip("_source:Q", title="Source group", format="d"),
                    gs.Tooltip("_target:Q", title="Target group", format="d"),
                    gs.Tooltip("_weight:Q", title="Connectivity", format=".4g"),
                ]
            )
        charts.append(rules)
    numeric = color_data is None and pd.api.types.is_numeric_dtype(nodes["_color"])
    colors: dict[str, Any]
    fill, stroke = gs.Fill("_group:N"), gs.Stroke("_group:N")
    legend: gs.Legend | None = gs.Legend(
        title=group_key,
        values=nodes["_group"].tolist(),
        symbolSize=49,
        orient="bottom",
        direction="horizontal",
        columns=2,
    )
    if color_data is not None:
        colors = dict(type="ordinal", domain=group_labels, scheme=color_data.scheme)
    elif numeric:
        low, high, constant = color_bounds(
            nodes["_color"].to_numpy(),
            None,
            None,
            context=CONTEXT,
            expand_constant=colorbar,
        )
        fill, stroke = gs.Fill("_color:Q"), gs.Stroke("_color:Q")
        legend = None
        if constant and not colorbar:
            # Scanpy maps a constant range without a guide to the first palette color.
            _, high, _ = color_bounds(
                nodes["_color"].to_numpy(), None, None, context=CONTEXT
            )
        colors = dict(
            type="linear",
            domain=[low, high],
            scheme=cmap,
            zero=False,
            nice=False,
            clamp=True,
        )
        if colorbar:
            legend = gs.Legend(
                title=color_title,
                titleOrient="right",
                gradientThickness=15,
                gradientStrokeColor="black",
                gradientStrokeWidth=0.8 * PT,
            )
    else:
        colors = dict(
            type="ordinal",
            domain=nodes["_group"].tolist(),
            range=nodes["_color"].tolist(),
        )
    maximum = max(1.0, float(nodes["_area"].max()))
    points = (
        gs.Chart(nodes)
        .transform_filter(
            "datum._area > 0 && isValid(datum._color)" if numeric else "datum._area > 0"
        )
        .mark_point(
            filled=True,
            strokeWidth=PT,
            inwardStroke=False,
            clip=True,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            key=gs.Key("_id"),
            fill=fill.scale(**colors).legend(legend),
            stroke=stroke.scale(**colors).legend(None),
            size=gs.Size("_area:Q")
            .scale(
                domain=[0, maximum], range=[0, maximum * PT**2], zero=True, nice=False
            )
            .legend(None),
        )
    )
    if hover:
        tooltips = [
            gs.Tooltip("_group:N", title="Group"),
            gs.Tooltip("_label:N", title="Label"),
            gs.Tooltip("_cells:Q", title="Cells", format="d"),
        ]
        if numeric:
            tooltips.append(gs.Tooltip("_color:Q", title="Color value", format=".4g"))
        points = points.encode(tooltip=tooltips)
    layers = [*charts, points]
    if show_node_labels:
        # Make room for painted nodes and their outlines; hidden nodes need no obstacle.
        source = gs.Chart(nodes).transform_calculate(
            _node_extent=gs.expr.if_(
                (gs.datum._area > 0) & gs.expr.isValid(gs.datum._color),
                (gs.expr.sqrt(gs.datum._area) + 2) * PT,
                0,
            )
        )
        layers.append(
            displaced_labels(
                source,
                key="_id",
                text="_label",
                x="_x",
                y="_y",
                size=fontsize * PT,
                fontweight="bold" if fontweight == "bold" else "normal",
                anchor_size="_node_extent",
            )
        )
    result = (
        gs.layer(*layers)
        .encode(x=x, y=y)
        .resolve_scale(size="independent")
        .properties(
            width=width,
            height=height,
            view={
                "stroke": "black" if frameon else "transparent",
                "strokeWidth": 0.8 * PT if frameon else 0,
            },
        )
        .configure_legend(labelFont=FONT, labelFontSize=10 * PT, labelLimit=300)
    )
    if cutoff is not None:
        result = result.add_params(cutoff)
    if title is not None:
        result = result.properties(title=gs.title(title, font=FONT, fontSize=12 * PT))
    return result
