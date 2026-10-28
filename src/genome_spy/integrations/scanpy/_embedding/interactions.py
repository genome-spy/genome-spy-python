"""Optional hover, shared navigation, and linked interval brushing."""

from __future__ import annotations

import genome_spy as gs

from genome_spy.integrations.scanpy._embedding.data import Panel, PreparedEmbedding
from genome_spy.integrations.scanpy._style import EmbeddingStyle


def point_hover(
    chart: gs.Chart,
    panel: Panel,
    index: int,
    *,
    axis_labels: tuple[str, ...],
    row_label: str,
    hover: bool,
) -> gs.Chart:
    """Return a point chart with the requested native hover fields.

    Use the panel's prepared fields without dropping cells.
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
    return chart


def validate_brush(prepared: PreparedEmbedding) -> None:
    """Check prepared panels use the same coordinate pair; raise if linking is unsafe."""
    if len({panel.dimensions for panel in prepared.panels}) != 1:
        raise NotImplementedError(
            "Scanpy embedding: linked brushing requires the same dimensions in all panels."
        )


def brush_count(
    selection: gs.Parameter,
    fields: tuple[str, str],
    *,
    name: str,
    width: float,
) -> gs.Chart:
    """Return a native count row inheriting its cell data from the composition.

    Read the brush bounds without changing the point marks.
    """
    x, y = fields
    parameter = selection.name
    # shortcut: sum preserves zero counts in Core 1.2.0; replace after its fix ships.
    # Match the shader's lower-inclusive, upper-exclusive point membership.
    predicate = (
        f"{parameter}.intervals.x && {parameter}.intervals.y && "
        f"{parameter}.intervals.x[0] <= datum.{x} && datum.{x} < {parameter}.intervals.x[1] && "
        f"{parameter}.intervals.y[0] <= datum.{y} && datum.{y} < {parameter}.intervals.y[1]"
    )
    return (
        gs.Chart()
        .transform_collect()
        .transform_formula(expr=f"({predicate}) ? 1 : 0", as_="selected")
        .transform_aggregate(fields=["selected"], ops=["sum"], as_=["count"])
        .transform_formula(expr="datum.count + ' cells selected'", as_="label")
        .mark_text(align="left", baseline="middle", size=12, tooltip=None)
        .encode(x=gs.value(0), y=gs.value(0.5), text="label:N")
        .properties(name=name, width=width, height=24)
    )


def with_brush_count(
    chart: gs.TopLevelSpec,
    prepared: PreparedEmbedding,
    style: EmbeddingStyle,
    selection: gs.Parameter,
) -> gs.TopLevelSpec:
    """Return the embedding chart with a count row driven by the supplied brush.

    Count prepared cells in the browser without changing point appearance.
    """
    x, y = (f"_coord_{d}" for d in prepared.panels[0].dimensions)
    name = selection.name
    count = brush_count(
        selection, (x, y), name=f"{prepared.basis}-count-{name}", width=style.width
    )
    return (
        gs.vconcat(chart, count, spacing=8)
        .properties(data=prepared.table)
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
