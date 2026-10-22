"""Native group nodes, labels and weighted straight edges for stored PAGA graphs."""

from typing import Any

import numpy as np
import pandas as pd
import genome_spy as gs
from genome_spy.schemapi import Undefined

from genome_spy.integrations.scanpy._data import coordinate_domain, number
from genome_spy.integrations.scanpy._grid_interactions import zoom_axes
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS as PT

CONTEXT = "gsc.pl.paga"


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
    charts = []
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
                color="grey" if is_dashed else "black",
                opacity=0.5 if is_dashed else 1,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
                strokeDash=[round(v * PT) for v in (3.7, 1.6)]
                if is_dashed
                else Undefined,
            )
            .encode(
                x=x,
                y=y,
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
        if hover:
            rules = rules.encode(
                tooltip=[
                    gs.Tooltip("_source:Q", title="Source group", format="d"),
                    gs.Tooltip("_target:Q", title="Target group", format="d"),
                    gs.Tooltip("_weight:Q", title="Connectivity", format=".4g"),
                ]
            )
        charts.append(rules)
    colors = dict(
        type="ordinal", domain=nodes["_id"].tolist(), range=nodes["_color"].tolist()
    )
    maximum = max(1.0, float(nodes["_area"].max()))
    points = (
        gs.Chart(nodes)
        .transform_filter("datum._area > 0")
        .mark_point(
            filled=True,
            strokeWidth=PT,
            inwardStroke=False,
            clip=True,
            tooltip={"handler": "default"} if hover else None,
        )
        .encode(
            x=x,
            y=y,
            key=gs.Key("_id"),
            fill=gs.Fill("_id:N").scale(**colors).legend(None),
            stroke=gs.Stroke("_id:N").scale(**colors).legend(None),
            size=gs.Size("_area:Q")
            .scale(
                domain=[0, maximum], range=[0, maximum * PT**2], zero=True, nice=False
            )
            .legend(None),
        )
    )
    if hover:
        points = points.encode(
            tooltip=[
                gs.Tooltip("_group:N", title="Group"),
                gs.Tooltip("_label:N", title="Label"),
                gs.Tooltip("_cells:Q", title="Cells", format="d"),
            ]
        )
    labels = (
        gs.Chart(nodes)
        .mark_text(
            font=FONT,
            fontWeight="bold" if fontweight == "bold" else "normal",
            size=fontsize * PT,
            align="center",
            baseline="middle",
            clip=True,
            tooltip=None,
        )
        .encode(x=x, y=y, text="_label:N")
    )
    result = (
        gs.layer(*charts, points, labels)
        .resolve_scale(size="independent")
        .properties(
            width=width,
            height=height,
            view={
                "stroke": "black" if frameon else "transparent",
                "strokeWidth": 0.8 * PT if frameon else 0,
            },
        )
    )
    if title is not None:
        result = result.properties(title=gs.title(title, font=FONT, fontSize=12 * PT))
    return result
