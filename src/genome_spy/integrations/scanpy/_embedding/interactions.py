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


def brush_membership(selection: gs.Parameter, fields: tuple[str, str]) -> gs.Expression:
    """Return the native interval test used by cell counts and point highlighting."""
    x, y = fields
    name = selection.name
    # Match the shader's lower-inclusive, upper-exclusive point membership.
    return gs.Expression(
        f"{name}.intervals.x && {name}.intervals.y && "
        f"{name}.intervals.x[0] <= datum.{x} && datum.{x} < {name}.intervals.x[1] && "
        f"{name}.intervals.y[0] <= datum.{y} && datum.{y} < {name}.intervals.y[1]"
    )


def brush_count(
    selection: gs.Parameter,
    fields: tuple[str, str],
    *,
    name: str,
    width: float,
    within_brush: bool = False,
    cell_filter: gs.Expression | None = None,
) -> gs.Chart:
    """Return native count text inheriting its cell data from the composition.

    Optionally fit the text inside the brush using native ranged-text encodings.
    """
    parameter = selection.name
    predicate = str(brush_membership(selection, fields))
    active = f"{parameter}.intervals.x && {parameter}.intervals.y"
    label = (
        "format(datum.count, ',') + ' cells'"
        if within_brush
        else "datum.count + ' cells selected'"
    )
    if cell_filter is not None:
        predicate = str(gs.Expression(predicate) & cell_filter)
    count = (
        gs.Chart()
        .transform_collect()
        .transform_filter(predicate)
        .transform_aggregate(as_=["count"])
        .transform_formula(expr=label, as_="label")
    )
    if within_brush:
        return (
            count.transform_calculate(
                _brush_x=f"({active}) ? {parameter}.intervals.x[0] : 0",
                _brush_x2=f"({active}) ? {parameter}.intervals.x[1] : 0",
                _brush_y=f"({active}) ? {parameter}.intervals.y[1] : 0",
                _brush_y2=f"({active}) ? {parameter}.intervals.y[0] : 0",
            )
            .mark_text(
                align="left",
                baseline="top",
                size=12,
                color="black",
                paddingX=6,
                paddingY=5,
                squeeze=False,
                clip=True,
                tooltip=None,
            )
            .encode(
                x="_brush_x:Q",
                x2="_brush_x2:Q",
                y="_brush_y:Q",
                y2="_brush_y2:Q",
                text="label:N",
            )
            .properties(name=name)
        )
    return (
        count.mark_text(align="left", baseline="middle", size=12, tooltip=None)
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
        .add_params(brush_value(selection))
    )


def brush_value(selection: gs.Parameter) -> gs.Parameter:
    """Return the outer native interval value shared by controllers and consumers."""
    return gs.param(
        selection.name, value={"type": "interval", "intervals": {"x": None, "y": None}}
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
