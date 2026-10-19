"""Optional hover, shared navigation, and linked interval brushing."""

from __future__ import annotations

import genome_spy as gs

from genome_spy.integrations.scanpy._embedding_data import Panel, PreparedEmbedding
from genome_spy.integrations.scanpy._style import EmbeddingStyle


def point_interactions(
    chart: gs.Chart,
    panel: Panel,
    index: int,
    *,
    axis_labels: tuple[str, ...],
    row_label: str,
    hover: bool,
    selection: gs.Parameter | None,
    opacity: float,
    stroke_opacity: float,
) -> gs.Chart:
    """Return a point chart with requested hover and brush highlighting applied.

    Use the panel's prepared fields and shared selection without dropping cells.
    """
    if hover:
        x, y = panel.dimensions
        chart = chart.encode(
            tooltip=[
                gs.Tooltip("_obs_id:N", title=f"{row_label} ID"),
                gs.Tooltip("_obs_label:N", title=row_label),
                gs.Tooltip(
                    f"_value_{index}:N" if panel.categorical else f"_value_{index}:Q",
                    title=f"{panel.key or 'Color'} ({panel.source})",
                ),
                gs.Tooltip(f"_coord_{x}:Q", title=axis_labels[x]),
                gs.Tooltip(f"_coord_{y}:Q", title=axis_labels[y]),
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


def validate_brush(prepared: PreparedEmbedding) -> None:
    """Check prepared panels use the same coordinate pair; raise if linking is unsafe."""
    if len({panel.dimensions for panel in prepared.panels}) != 1:
        raise NotImplementedError(
            "Scanpy embedding: linked brushing requires the same dimensions in all panels."
        )


def with_brush_count(
    chart: gs.TopLevelSpec,
    prepared: PreparedEmbedding,
    style: EmbeddingStyle,
    selection: gs.Parameter,
) -> gs.TopLevelSpec:
    """Return the embedding chart with a count row driven by the supplied brush.

    Count prepared cells in the browser using the same bounds as point highlighting.
    """
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
        .properties(name=f"{prepared.basis}-count-{name}", width=style.width, height=24)
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
    chart: gs.Chart | gs.LayerChart, selection: gs.Parameter, basis: str
) -> gs.Chart | gs.LayerChart:
    """Return the first panel with control of the supplied shared brush.

    Write to the outer selection so the other panels and count see the same value.
    """
    # Other panels only observe the shared value.
    return chart.add_params(
        selection.copy(name=selection.name, push="outer")
    ).properties(name=f"{basis}-brush-{selection.name}")
