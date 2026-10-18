"""Optional hover, shared navigation, and linked interval brushing."""

from __future__ import annotations

import genome_spy as gs

from genome_spy.integrations.scanpy._umap_data import Panel, PreparedUMAP
from genome_spy.integrations.scanpy._style import UMAPStyle


def point_interactions(
    chart: gs.Chart,
    panel: Panel,
    index: int,
    *,
    hover: bool,
    selection: gs.Parameter | None,
    opacity: float,
    stroke_opacity: float,
) -> gs.Chart:
    if hover:
        x, y = panel.dimensions
        chart = chart.encode(
            tooltip=[
                gs.Tooltip("_obs_id:N", title="Observation ID"),
                gs.Tooltip("_obs_label:N", title="Observation"),
                gs.Tooltip(
                    f"_value_{index}:N" if panel.categorical else f"_value_{index}:Q",
                    title=f"{panel.key or 'Color'} ({panel.source})",
                ),
                gs.Tooltip(f"_coord_{x}:Q", title=f"UMAP{x + 1}"),
                gs.Tooltip(f"_coord_{y}:Q", title=f"UMAP{y + 1}"),
            ]
        )
    if selection is not None:
        chart = chart.encode(
            fillOpacity=gs.when(selection)
            .then(gs.value(opacity))
            .otherwise(gs.value(opacity * 0.2)),
            strokeOpacity=gs.when(selection)
            .then(gs.value(stroke_opacity))
            .otherwise(gs.value(stroke_opacity * 0.2)),
        )
    return chart


def validate_brush(prepared: PreparedUMAP) -> None:
    if len({panel.dimensions for panel in prepared.panels}) != 1:
        raise NotImplementedError(
            "gsc.pl.umap: linked brushing requires the same dimensions in all panels."
        )


def with_brush_count(
    chart: gs.TopLevelSpec,
    prepared: PreparedUMAP,
    style: UMAPStyle,
    selection: gs.Parameter,
) -> gs.TopLevelSpec:
    x, y = [f"_coord_{d}" for d in prepared.panels[0].dimensions]
    name = selection.name
    # Match the shader's lower-inclusive, upper-exclusive point membership.
    predicate = (
        f"{name}.intervals.x && {name}.intervals.y && "
        f"{name}.intervals.x[0] <= datum.{x} && datum.{x} < {name}.intervals.x[1] && "
        f"{name}.intervals.y[0] <= datum.{y} && datum.{y} < {name}.intervals.y[1]"
    )
    count = (
        gs.Chart(prepared.table)
        .transform_collect()
        .transform_formula(expr=f"({predicate}) ? 1 : 0", as_="selected")
        .transform_aggregate(fields=["selected"], ops=["sum"], as_=["count"])
        .transform_formula(expr="datum.count + ' cells selected'", as_="label")
        .mark_text(align="left", baseline="middle", size=12, tooltip=None)
        .encode(x=gs.value(0), y=gs.value(0.5), text="label:N")
        .properties(name=f"umap-count-{name}", width=style.width, height=24)
    )
    return (
        gs.vconcat(chart, count, spacing=8)
        .resolve_scale(x="independent", y="independent")
        .add_params(
            gs.param(
                name, value={"type": "interval", "intervals": {"x": None, "y": None}}
            )
        )
    )


def brush_owner(
    chart: gs.Chart | gs.LayerChart, selection: gs.Parameter
) -> gs.Chart | gs.LayerChart:
    # Other panels only observe the shared value.
    return chart.add_params(
        selection.copy(name=selection.name, push="outer")
    ).properties(name=f"umap-brush-{selection.name}")
