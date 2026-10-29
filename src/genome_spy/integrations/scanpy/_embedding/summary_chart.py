"""Native transforms and composition for detached embedding summaries."""

from __future__ import annotations

from dataclasses import replace
import json
from typing import Any, Literal

import numpy as np

import genome_spy as gs
from genome_spy.schemapi import Undefined, UndefinedType
from genome_spy.integrations.scanpy._data import coordinate_domain
from genome_spy.integrations.scanpy._embedding.chart import build_embedding
from genome_spy.integrations.scanpy._embedding.data import PreparedEmbedding
from genome_spy.integrations.scanpy._embedding.interactions import (
    brush_count,
    brush_owner,
    brush_value,
)
from genome_spy.integrations.scanpy._expression.colors import expression_scale
from genome_spy.integrations.scanpy._embedding.summary_data import (
    Observation,
    prepare_tracks,
)
from genome_spy.integrations.scanpy._grid_interactions import with_values
from genome_spy.integrations.scanpy._style import embedding_style


def _gene_controls(
    options: dict[str, Any], fields: dict[str, str], panel: str, *, offset: int = 0
) -> list[gs.Parameter]:
    """Keep gene choices in native parameters owned by this composition."""
    if not options["gene_controls"]:
        return []
    return [
        gs.param(
            f"{panel}_gene_{i + offset}",
            value=gene,
            bind=gs.binding_select(
                options=list(fields), name=f"{panel.title()} gene {i + offset + 1}"
            ),
        )
        for i, gene in enumerate(options["genes"])
    ]


def _heatmap(
    selected: gs.Chart,
    prepared: PreparedEmbedding,
    fields: dict[str, str],
    groups: list[str],
    options: dict[str, Any],
    show_legend: bool,
    controls: list[gs.Parameter],
) -> gs.Chart | gs.LayerChart:
    """Return selected-cell gene means as tiles, with optional gene controls and values."""
    genes = options["genes"]
    selected_fields = (
        list(fields.values()) if controls else [fields[gene] for gene in genes]
    )
    gene_expression = "[" + ",".join(control.name for control in controls) + "]"
    domain = gs.expr(gene_expression) if controls else genes
    values = prepared.table[selected_fields].to_numpy(dtype=float, na_value=np.nan)
    if not np.isfinite(values).any():
        values = np.array([-1.0, 1.0])
    scale = expression_scale(
        values,
        options["cmap"],
        options["vmin"],
        options["vmax"],
        context="gsc.pl.EmbeddingSummary",
    )
    labels = {field.removeprefix("_expr_"): gene for gene, field in fields.items()}
    indices = "|".join(field.removeprefix("_expr_") for field in selected_fields)
    tiles = (
        selected.transform_project(fields=["_group", *selected_fields])
        .transform_regex_fold(
            columnRegex=f"^_expr_({indices})$", asKey="_feature", asValue="expression"
        )
        .transform_filter("isValid(datum.expression) && isValid(datum._group)")
        .transform_calculate(gene=f"({json.dumps(labels)})[datum._feature]")
    )
    if controls:
        tiles = tiles.transform_filter(f"indexof({gene_expression}, datum.gene) >= 0")
    tiles = (
        tiles.transform_aggregate(
            groupby=["_group", "gene"],
            fields=["expression", "expression"],
            ops=["mean", "count"],
            as_=["mean", "cells"],
        )
        .mark_rect()
        .encode(
            x=gs.X("_group:N", title=prepared.panels[0].key)
            .scale(type="band", domain=groups, padding=0.04)
            .axis(labelAngle=-40, labelLimit=125),
            y=gs.Y("gene:N", title=None).scale(
                type="band", domain=domain, padding=0.04
            ),
            color=gs.Color("mean:Q", title="Mean expression", scale=scale).legend(
                gs.Legend() if show_legend else None
            ),
            tooltip=[
                gs.Tooltip("_group:N", title=prepared.panels[0].key),
                gs.Tooltip("gene:N", title="Gene"),
                gs.Tooltip("mean:Q", title="Mean expression", format=".2f"),
                gs.Tooltip("cells:Q", title="Valid expression values", format="d"),
            ],
        )
        .properties(name="selected-expression")
    )
    chart = with_values(tiles, "mean") if options["show_values"] else tiles
    return chart.properties(
        title=options["title"],
        width=options["width"],
        height=options["height"],
    )


def _percentages(source: gs.Chart, groupby: list[str], cohort: str) -> gs.Chart:
    """Count categories/bins and normalize within the unchanged input cohort."""
    return (
        source.transform_aggregate(groupby=groupby, as_=["count"])
        .transform_window(
            ops=["sum"], fields=["count"], as_=["total"], frame=[None, None]
        )
        .transform_calculate(
            percent=100 * gs.datum.count / gs.datum.total, cohort=json.dumps(cohort)
        )
    )


def _tracks_panel(
    prepared: PreparedEmbedding,
    fields: dict[str, str],
    groups: list[str],
    options: dict[str, Any],
    color_scale: gs.Scale,
    brush: gs.Parameter,
) -> gs.TopLevelSpec:
    """Reuse the tracks renderer and native cell filter without changing cell order."""
    from genome_spy.integrations.scanpy._expression.tracksplot_chart import (
        build_tracksplot,
    )

    genes = options["genes"]
    ordered = prepare_tracks(prepared.table, fields, genes, groups)

    # Map original observation rows to fixed track slots; UMAP draw order is unchanged.
    prepared.table["_cell"] = np.argsort(ordered.observation_positions)
    positions = ordered.observation_positions
    return build_tracksplot(
        ordered,
        (),
        prepared.table["_obs_label"].to_numpy()[positions],
        prepared.table["_obs_id"].to_numpy()[positions],
        groupby=str(prepared.panels[0].key),
        categories=groups,
        palette=prepared.panels[0].palette,
        tree=None,
        log=False,
        hover=True,
        zoom=options["zoom"],
        group_gap=options["group_gap"],
        spacing=options["spacing"],
        width=options["width"],
        height=options["height"],
        figsize=None,
        cell_data=prepared.table,
        value_fields=[fields[gene] for gene in genes],
        color_scale=color_scale,
        highlight={
            "param": brush.name,
            "fields": {"x": "_coord_0", "y": "_coord_1"},
            "empty": True,
        },
        show_legend=False,
    ).properties(name="marker-tracks", title=options["title"])


def _histogram(
    prepared: PreparedEmbedding,
    selected: gs.Chart,
    options: dict[str, Any],
    show_legend: bool,
    *,
    fields: dict[str, str],
    gene: gs.Parameter | None = None,
    suffix: str = "",
) -> gs.TopLevelSpec:
    """Return all-cell and selected-cell distributions with the same bin boundaries."""
    field, width, kind = (options[key] for key in ("field", "bin_width", "kind"))
    values = prepared.table[
        list(fields.values()) if gene is not None else [field]
    ].to_numpy(dtype=float, na_value=np.nan)
    missing = np.isnan(values).any()
    values = values[np.isfinite(values)]
    source = gs.Chart()
    if gene is not None:
        field = "_histogram_value"
        lookup = f"datum[({json.dumps(fields)})[{gene.name}]]"
        source = source.transform_calculate(_histogram_value=lookup)
        selected = selected.transform_calculate(_histogram_value=lookup)
    domain = (
        [
            float(np.floor(values.min() / width) * width),
            float((np.floor(values.max() / width) + 1) * width),
        ]
        if values.size
        else [-width, width]
    )

    def cohort(chart: gs.Chart, label: str, name: str) -> gs.Chart:
        source = chart.transform_filter(f"isValid(datum.{field})").transform_calculate(
            bin_start=f"floor(datum.{field} / {width!r}) * {width!r}"
        )
        return (
            _percentages(source, ["bin_start"], label)
            .transform_calculate(
                bin_end=gs.datum.bin_start + width,
                variable=gene.name
                if gene is not None
                else json.dumps(options["label"]),
            )
            .mark_rect(opacity=0.75, minWidth=0, minHeight=0)
            .encode(
                x=gs.X(
                    "bin_start:Q",
                    title="Expression" if gene is not None else options["label"],
                ).scale(domain=domain, nice=False, zero=False),
                x2="bin_end:Q",
                y=gs.Y("percent:Q", title="Valid cells (%)").scale(
                    domain=[0, 100], nice=False
                ),
                y2=gs.value(0),
                color=gs.Color("cohort:N", title="Distribution")
                .scale(domain=["All cells", "Selected"], range=["#cbd5e1", "#2563eb"])
                .legend(gs.Legend() if show_legend else None),
                tooltip=[
                    gs.Tooltip("variable:N", title="Variable"),
                    "cohort:N",
                    "count:Q",
                    gs.Tooltip("total:Q", title="Valid cohort cells"),
                    gs.Tooltip("percent:Q", format=".1f"),
                ],
            )
            .properties(name=name)
        )

    chart = (
        cohort(source, "All cells", f"all-{kind}-histogram{suffix}")
        + cohort(selected, "Selected", f"selected-{kind}-histogram{suffix}")
    ).properties(
        title=options["title"],
        width=options["width"],
        height=options["height"],
    )
    if missing:

        def coverage(source: gs.Chart, cohort: str) -> gs.Chart:
            return (
                source.transform_project(fields=[field])
                .transform_calculate(
                    _valid=f"isValid(datum.{field}) ? 1 : 0",
                    _missing=f"isValid(datum.{field}) ? 0 : 1",
                )
                .transform_aggregate(
                    fields=["_valid", "_missing"],
                    ops=["sum", "sum"],
                    as_=["valid", "missing"],
                )
                .transform_calculate(
                    label=f"{json.dumps(cohort + ': ')} + datum.valid + ' valid, ' + datum.missing + ' missing'"
                )
                .mark_text(align="left", baseline="middle", size=10, tooltip=None)
                .encode(x=gs.value(0), y=gs.value(0.5), text="label:N")
                .properties(
                    name=f"{cohort.lower().replace(' ', '-')}-{kind}-coverage{suffix}",
                    height=16,
                )
            )

        return gs.vconcat(
            chart,
            coverage(source, "All cells"),
            coverage(selected, "Selected"),
            spacing=2,
        ).resolve_scale(x="independent", y="independent", color="shared")
    return chart


def _composition(
    selected: gs.Chart,
    observation: Observation,
    options: dict[str, Any],
    show_legend: bool,
) -> gs.LayerChart:
    """Return paired group percentages, preserving the observation's colors and order."""
    assert observation.color is not None
    field = observation.field
    domain = observation.color.to_dict()["domain"]

    def cohort(source: gs.Chart, label: str, name: str) -> gs.Chart:
        return (
            _percentages(source.transform_project(fields=[field]), [field], label)
            .mark_rect(minWidth=0, minHeight=0)
            .encode(
                x=gs.X("percent:Q", title="Share of cohort (%)").scale(
                    domain=[0, 100], nice=False
                ),
                x2=gs.value(0),
                y=gs.Y(f"{field}:N", title=options["key"])
                .scale(type="band", domain=domain, padding=0.15)
                .axis(labelLimit=130),
                yOffset=gs.YOffset("cohort:N").scale(
                    type="band", domain=["All cells", "Selected"], padding=0.1
                ),
                color=gs.Color(f"{field}:N", scale=observation.color).legend(None),
                opacity=gs.Opacity("cohort:N", title="Cohort")
                .scale(
                    type="ordinal", domain=["All cells", "Selected"], range=[0.25, 0.85]
                )
                .legend(gs.Legend() if show_legend else None),
                tooltip=[
                    gs.Tooltip(f"{field}:N", title=options["key"]),
                    "cohort:N",
                    "count:Q",
                    gs.Tooltip("total:Q", title="Cohort cells"),
                    gs.Tooltip("percent:Q", format=".1f"),
                ],
            )
            .properties(name=name)
        )

    return (
        cohort(gs.Chart(), "All cells", "all-composition")
        + cohort(selected, "Selected", "selected-composition")
    ).properties(
        title=options["title"],
        width=options["width"],
        height=options["height"],
    )


def _histogram_panels(
    prepared: PreparedEmbedding,
    selected: gs.Chart,
    fields: dict[str, str],
    histograms: list[dict[str, Any]],
    *,
    legend_show: bool,
    spacing: float,
) -> tuple[list[tuple[gs.TopLevelSpec, str]], list[gs.Parameter]]:
    """Return histogram panels and their gene controls from the requested summaries.

    Keep control names unique and stack charts according to their chosen side.
    """
    panels: list[tuple[gs.TopLevelSpec, str]] = []
    gene_parameters: list[gs.Parameter] = []
    histogram_count = sum(max(1, len(panel["genes"])) for panel in histograms)
    offset = 0
    for histogram in histograms:
        controls = _gene_controls(histogram, fields, "histogram", offset=offset)
        gene_parameters.extend(controls)
        charts: list[gs.TopLevelSpec] = []
        genes = histogram["genes"]
        for i in range(max(1, len(genes))):
            options = dict(histogram)
            control = controls[i] if controls else None
            if genes:
                options.update(field=fields[genes[i]], label=f"{genes[i]} expression")
            if len(genes) > 1:
                options["title"] = (
                    gs.Title(text=gs.expr(control.name))
                    if control is not None
                    else genes[i]
                )
            charts.append(
                _histogram(
                    prepared,
                    selected,
                    options,
                    legend_show and offset == 0,
                    fields=fields,
                    gene=control,
                    suffix=f"-{offset + i}" if histogram_count > 1 else "",
                )
            )
        concat = (
            gs.vconcat if histogram["position"] in ("left", "right") else gs.hconcat
        )
        distributions = (
            concat(*charts, spacing=spacing)
            .resolve_scale(x="independent", y="independent", color="shared")
            .properties(title=histogram["title"])
            if len(charts) > 1
            else charts[0]
        )
        panels.append(
            (
                distributions,
                histogram["position"],
            )
        )
        offset += len(charts)
    return panels, gene_parameters


def _place_panels(
    center: gs.HConcatChart | gs.VConcatChart,
    panels: list[tuple[gs.TopLevelSpec, str]],
    spacing: float,
) -> gs.HConcatChart | gs.VConcatChart:
    """Return panels around the embedding, with top/bottom spanning the whole row."""
    result = center

    # Place side panels first so top and bottom panels span the complete row.
    for panel, side in sorted(panels, key=lambda item: item[1] in ("top", "bottom")):
        children = [panel, result] if side in ("left", "top") else [result, panel]
        result = (
            gs.hconcat(*children, spacing=spacing)
            if side in ("left", "right")
            else gs.vconcat(*children, spacing=spacing)
        ).resolve_scale(
            x="independent", y="independent", color="independent", size="independent"
        )
    return result


def build_summary(
    prepared: PreparedEmbedding,
    fields: dict[str, str],
    groups: list[str],
    *,
    heatmap: dict[str, Any] | None,
    tracks: dict[str, Any] | None,
    histograms: list[dict[str, Any]],
    composition: dict[str, Any] | None,
    observations: dict[str, Observation],
    title: str | UndefinedType,
    show_count: bool,
    zoom: bool,
    size: float,
    point_size: float,
    alpha: float,
    spacing: float,
    legend_position: Literal["left", "right", "top", "bottom"],
    legend_show: bool,
) -> gs.TopLevelSpec:
    """Build a chart with one outer brush owner and independent summary axes."""
    table = prepared.table.copy()
    table["_size_0"] = point_size
    prepared = replace(prepared, table=table)
    style = embedding_style(
        count=1,
        width=size,
        height=size,
        frameon=True,
        legend_loc="right margin" if legend_show else None,
        colorbar_loc="right",
        legend_fontsize=7,
        ncols=1,
        hspace=0,
        wspace=0,
        alpha=alpha,
        edgecolor="none",
        linewidth=0,
        na_color="lightgray",
    )

    # Keep coordinate units equal in the square embedding.
    limits = [coordinate_domain(table[f"_coord_{i}"].to_numpy(), 0.05) for i in (0, 1)]
    span = max(high - low for low, high in limits)
    domains = tuple(
        ((low + high - span) / 2, (low + high + span) / 2) for low, high in limits
    )

    # Use Core's Shift-drag gesture when ordinary dragging pans.
    brush = gs.selection_interval(
        "cells", encodings=["x", "y"], on=Undefined if zoom else "mousedown", zoom=False
    )
    direction: Literal["horizontal", "vertical"] = (
        "horizontal" if legend_position in ("top", "bottom") else "vertical"
    )
    embedding = (
        build_embedding(
            prepared,
            style,
            hover=True,
            zoom=zoom,
            coordinate_domains=(domains[0], domains[1]),
        )
        ._with_properties(
            {
                "data": Undefined,
                "name": f"{prepared.basis}-points",
                "title": Undefined,
            }
        )
        ._configure_nested("legend", orient=legend_position, direction=direction)
    )
    layers: list[gs.TopLevelSpec] = [embedding]
    if show_count:
        layers.append(
            brush_count(
                brush,
                ("_coord_0", "_coord_1"),
                name=f"{prepared.basis}-count-cells",
                width=size,
                within_brush=True,
            )
        )
    overlay = brush_owner(
        gs.layer(*layers)
        .properties(
            width=size,
            height=size,
            title=gs.title(
                title,
                fontSize=style.title_fontsize,
                font=style.font,
            )
            if isinstance(title, str)
            else Undefined,
        )
        .configure_view(stroke=style.frame_color, strokeWidth=style.frame_width),
        brush,
        prepared.basis,
    )
    chart = gs.vconcat(overlay).resolve_scale(x="independent", y="independent")

    # All summaries read the same brush-filtered cell table.
    selected = gs.Chart().transform_filter(
        brush, fields={"x": "_coord_0", "y": "_coord_1"}, empty=False
    )
    panels: list[tuple[gs.TopLevelSpec, str]] = []
    gene_parameters: list[gs.Parameter] = []
    if heatmap is not None:
        controls = _gene_controls(heatmap, fields, "heatmap")
        gene_parameters.extend(controls)
        panels.append(
            (
                _heatmap(
                    selected, prepared, fields, groups, heatmap, legend_show, controls
                ),
                heatmap["position"],
            )
        )
    if tracks is not None:
        key = prepared.panels[0].key
        assert key is not None
        color_scale = observations[key].color
        assert color_scale is not None
        panels.append(
            (
                _tracks_panel(prepared, fields, groups, tracks, color_scale, brush),
                tracks["position"],
            )
        )

    # Keep gene controls with the panels they update.
    distributions, controls = _histogram_panels(
        prepared, selected, fields, histograms, legend_show=legend_show, spacing=spacing
    )
    panels.extend(distributions)
    gene_parameters.extend(controls)

    if composition is not None:
        panels.append(
            (
                _composition(
                    selected, observations[composition["key"]], composition, legend_show
                ),
                composition["position"],
            )
        )
    result = _place_panels(chart, panels, spacing)
    return (
        result.properties(data=table)
        .add_params(brush_value(brush), *gene_parameters)
        .resolve_legend(default="collected")
        .configure_legend(
            orient=legend_position,
            direction=direction,
            columns=1,
            labelFontSize=9,
            titleFontSize=10,
        )
    )
