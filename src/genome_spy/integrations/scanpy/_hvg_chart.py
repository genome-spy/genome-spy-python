"""Paired native scatter panels for stored variable-gene statistics."""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._embedding_chart import coordinate_domain
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS


def build_variable_genes(
    table: pd.DataFrame,
    statistic: str,
    *,
    log: bool,
    hover: bool,
    zoom: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Return normalized/raw panels from stored statistics, retaining Scanpy's log limits."""
    width, height = 300 if width is None else width, 300 if height is None else height
    log_domains = None
    if log:
        raw = table[statistic].to_numpy()
        means = table["means"].to_numpy()
        if (
            not np.isfinite(means).all()
            or not np.isfinite(raw).all()
            or (means <= 0).any()
        ):
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
        log_domains = [[0.95 * means.min(), 1.05 * means.max()], [low, high]]
    colors = gs.Scale(
        type="ordinal",
        domain=["highly variable genes", "other genes"],
        range=["black", "grey"],
    )
    panels = []
    for index, field in enumerate((f"{statistic}_norm", statistic)):
        valid = table[["means", field]].dropna()
        axes = {}
        for axis, key in (("x", "means"), ("y", field)):
            domain = (
                log_domains[0 if axis == "x" else 1]
                if log_domains is not None
                else coordinate_domain(
                    valid[key].to_numpy() if len(valid) else np.array([0.0]), 0.05
                )
            )
            label = (
                "mean expressions of genes"
                if axis == "x"
                else f"{statistic} of genes ({'' if index == 0 else 'not '}normalized)"
            )
            channel = gs.X if axis == "x" else gs.Y
            axes[axis] = (
                channel(f"{key}:Q")
                .scale(
                    type="log" if log else "linear",
                    domain=[float(value) for value in domain],
                    nice=False,
                    zero=False,
                    zoom=zoom,
                    name=f"hvg-{axis}-{index}",
                )
                .axis(title=label, domain=False)
            )
        panel = (
            gs.Chart(table)
            .transform_filter(
                f"isValid(datum.means) && isValid(datum.{field})"
                + (f" && datum.means > 0 && datum.{field} > 0" if log else "")
            )
            .transform_collect(sort={"field": "_selected", "order": "descending"})
            .mark_point(
                filled=True,
                size=POINTS_TO_PIXELS**2,
                strokeWidth=POINTS_TO_PIXELS,
                inwardStroke=False,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                **axes,
                key=gs.Key("_obs_id"),
                fill=gs.Fill("_status:N", scale=colors).legend(gs.Legend(title=None)),
                stroke=gs.Stroke("_status:N", scale=colors).legend(None),
            )
            .properties(width=width, height=height)
        )
        if hover:
            panel = panel.encode(
                tooltip=[
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
            )
        panels.append(panel)
    return (
        gs.hconcat(*panels, spacing=0.3 * width)
        .resolve_scale(x="independent", y="independent", fill="shared", stroke="shared")
        .resolve_legend(default="collected")
        .configure_axis(
            labelFont=FONT,
            titleFont=FONT,
            labelFontSize=10 * POINTS_TO_PIXELS,
            titleFontSize=10 * POINTS_TO_PIXELS,
        )
        .configure_view(stroke="black", strokeWidth=0.8 * POINTS_TO_PIXELS)
        .configure_legend(
            orient="bottom",
            direction="horizontal",
            labelFont=FONT,
            labelFontSize=10 * POINTS_TO_PIXELS,
            symbolSize=36 * POINTS_TO_PIXELS**2,
        )
    )
