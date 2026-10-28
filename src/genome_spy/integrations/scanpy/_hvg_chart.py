"""Paired native scatter panels for stored variable-gene statistics."""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import coordinate_domain
from genome_spy.integrations.scanpy._style import (
    AXIS_TEXT,
    FONT,
    POINTS_TO_PIXELS,
    zoom_point_size,
)


def _log_domains(table: pd.DataFrame, statistic: str) -> list[list[float]]:
    """Return shared log-axis limits from means and raw scores, rejecting invalid values."""
    raw = table[statistic].to_numpy()
    means = table["means"].to_numpy()
    if not np.isfinite(means).all() or not np.isfinite(raw).all() or (means <= 0).any():
        raise NotImplementedError(
            "gsc.pl.highly_variable_genes: log=True requires finite positive means and finite raw statistics."
        )
    low = 0.95 * raw.min() if raw.min() > 0 else 0.1
    high = 1.05 * raw.max()
    if not 0 < low < high:
        raise NotImplementedError(
            "gsc.pl.highly_variable_genes: log=True requires positive increasing raw-statistic limits."
        )

    # Scanpy uses the raw statistic's limits on both logarithmic panels.
    return [[0.95 * means.min(), 1.05 * means.max()], [low, high]]


def _cutoff_count(source: gs.Chart, width: float) -> gs.Chart:
    """Return a count label from the shared preview source, before hiding points."""
    return (
        source.transform_aggregate(fields=["_above"], ops=["sum"], as_=["_count"])
        .transform_calculate(_label="datum._count + ' genes above cutoff (preview)'")
        .mark_text(align="left", baseline="middle", size=12, font=FONT, tooltip=None)
        .encode(x=gs.value(0), y=gs.value(0.5), text="_label:N")
        .properties(width=2.3 * width, height=24)
    )


def build_variable_genes(
    table: pd.DataFrame,
    statistic: str,
    *,
    log: bool,
    hover: bool,
    zoom: bool,
    threshold_slider: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Return normalized/raw panels from stored statistics, retaining Scanpy's log limits."""
    width, height = 300 if width is None else width, 300 if height is None else height
    log_domains = None
    if log:
        log_domains = _log_domains(table, statistic)

    # The optional cutoff previews a choice without changing saved selections.
    cutoff = None
    normalized = f"{statistic}_norm"
    if threshold_slider:
        scores = table[normalized].dropna().to_numpy()
        if len(scores) < 2 or scores.min() == scores.max():
            raise ValueError(
                "gsc.pl.highly_variable_genes: threshold_slider needs a varying normalized score."
            )
        initial = float(f"{np.median(scores):.3g}")
        initial = float(np.clip(initial, scores.min(), scores.max()))
        cutoff = gs.param(
            "hvg_cutoff",
            value=initial,
            bind=gs.binding_range(
                min=float(scores.min()),
                max=float(scores.max()),
                name="Preview score cutoff: ",
            ),
        )
    statuses = (
        ["Above cutoff", "Below cutoff"]
        if threshold_slider
        else ["highly variable genes", "other genes"]
    )
    colors = gs.Scale(
        type="ordinal",
        domain=statuses,
        range=["#2563a6", "#cbd5e1"],
    )

    # One numeric flag drives both point colors and the cutoff count.
    source = gs.Chart(table)
    if cutoff is not None:
        source = source.transform_calculate(
            _above=gs.expr.if_(
                gs.expr.isValid(gs.datum[normalized])
                & (gs.datum[normalized] >= cutoff),
                1,
                0,
            ),
        ).transform_calculate(_preview_status=gs.expr.if_(gs.datum._above, *statuses))

    # Both score panels share colors but keep independent axes.
    panels = []
    for index, field in enumerate((f"{statistic}_norm", statistic)):
        valid = table[["means", field]].dropna()
        axes = {}
        score_label = (
            f"{'Normalized ' if index == 0 else ''}{statistic.removesuffix('s')}"
        )
        for axis, key, label in (
            ("x", "means", "Mean expression"),
            ("y", field, score_label),
        ):
            domain: list[float] | tuple[float, float]
            if log_domains is not None:
                domain = log_domains[0 if axis == "x" else 1]
            else:
                observed = valid[key].to_numpy() if len(valid) else np.array([0.0])
                domain = coordinate_domain(observed, 0.05)
            channel = gs.X if axis == "x" else gs.Y
            axes[axis] = (
                channel(f"{key}:Q")
                .scale(
                    type="log" if log else "linear",
                    domain=[float(value) for value in domain],
                    nice=False,
                    zero=False,
                    zoom=zoom,
                )
                .axis(title=label, domain=False)
            )
        panel: gs.Chart | gs.LayerChart = (
            source.transform_filter(
                f"isValid(datum.means) && isValid(datum.{field})"
                + (f" && datum.means > 0 && datum.{field} > 0" if log else "")
            )
            .transform_collect(
                sort={
                    "field": "_above" if cutoff is not None else "_selected",
                    "order": "ascending",
                }
            )
            .mark_point(
                filled=True,
                size=zoom_point_size(9, zoom),
                strokeWidth=0,
                minPickingSize=5,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                **axes,
                key=gs.Key("_obs_id"),
                fill=gs.Fill(
                    "_preview_status:N" if cutoff is not None else "_status:N",
                    scale=colors,
                ).legend(gs.Legend(title=None)),
            )
            .properties(width=width, height=height)
        )
        if hover:
            tooltips = [
                gs.Tooltip("_obs_id:N", title="Gene ID"),
                gs.Tooltip("_obs_label:N", title="Gene"),
                gs.Tooltip("_status:N", title="Selection"),
                gs.Tooltip("means:Q", title="Mean expression", format=".4g"),
                gs.Tooltip(
                    f"{field}:Q",
                    title=f"{statistic} ({'normalized' if index == 0 else 'not normalized'})",
                    format=".4g",
                ),
            ]
            if cutoff is not None:
                tooltips.append(gs.Tooltip("_preview_status:N", title="Preview"))
            panel = panel.encode(tooltip=tooltips)
        if cutoff is not None and index == 0:
            rule = (
                gs.Chart([{}])
                .transform_calculate(_cutoff=cutoff)
                .mark_rule(
                    color="#64748b", size=1, strokeDash=[4, 4], clip=True, tooltip=None
                )
                .encode(y=axes["y"].field("_cutoff"))
            )
            panel = gs.layer(rule, panel).properties(width=width, height=height)
        panels.append(panel)

    # Collect the legend once below the two panels.
    result: gs.HConcatChart | gs.VConcatChart = gs.hconcat(
        *panels, spacing=0.3 * width
    ).resolve_scale(x="independent", y="independent", fill="shared")
    if cutoff is not None:
        count = _cutoff_count(source, width)
        result = gs.vconcat(result, count, spacing=8).add_params(cutoff)
    return (
        result.resolve_scale(
            x="independent", y="independent", fill="shared", stroke="shared"
        )
        .resolve_legend(default="collected")
        .configure_axis(
            AXIS_TEXT,
        )
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_legend(
            orient="bottom",
            direction="horizontal",
            labelFont=FONT,
            labelFontSize=10 * POINTS_TO_PIXELS,
            symbolSize=36 * POINTS_TO_PIXELS**2,
        )
    )
