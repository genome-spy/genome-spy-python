"""Native horizontal boxes, whiskers and outliers for count percentages."""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import coordinate_domain
from genome_spy.integrations.scanpy._style import (
    AXIS_TEXT,
    POINTS_TO_PIXELS as PT,
)


def build_highest_expression(
    boxes: pd.DataFrame,
    outliers: pd.DataFrame,
    limits: tuple[float, float, float],
    *,
    n_top: int,
    log: bool,
    hover: bool,
    zoom: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Return a count-percentage boxplot with native gene labels and optional x zoom."""
    low, high, positive = limits
    if log and high <= 0:
        raise ValueError(
            "gsc.pl.highest_expr_genes: log=True needs positive percentages."
        )
    domain = list(
        coordinate_domain(np.array([positive if log else low, high]), 0.05, log=log)
    )
    x = (
        gs.X("lower:Q")
        .scale(
            type="log" if log else "linear",
            domain=domain,
            nice=False,
            zero=False,
            zoom=zoom,
            name="highest-expression-x",
        )
        .axis(title="% of total counts", domain=False)
    )
    genes = boxes.gene.tolist()
    y = (
        gs.Y("gene:N")
        .scale(
            type="band",
            domain=genes,
            reverse=True,
            paddingInner=0,
            paddingOuter=0,
        )
        .axis(title=None, domain=False, tickSize=0)
    )
    base = gs.Chart(boxes).encode(x=x, y=y)
    stroke = "#3d3d3d"
    rule = base.mark_rule(color=stroke, size=PT, clip=True, tooltip=None)
    line = rule.encode(x2="upper:Q")
    box = base.mark_rect(
        stroke=stroke,
        strokeWidth=PT,
        clip=True,
        tooltip={"handler": "default"} if hover else None,
    ).encode(
        x="q1:Q",
        x2="q3:Q",
        y=gs.Y("gene:N", band=0.8),
        fill=gs.Fill("gene:N").scale(domain=genes, scheme="category10").legend(None),
    )
    if hover:
        box = box.encode(
            tooltip=[
                gs.Tooltip("gene:N", title="Gene"),
                gs.Tooltip("gene_id:N", title="Gene ID"),
                *[
                    gs.Tooltip(f"{key}:Q", title=label, format=".4g")
                    for key, label in (
                        ("mean", "Mean (%)"),
                        ("median", "Median (%)"),
                        ("q1", "25th percentile (%)"),
                        ("q3", "75th percentile (%)"),
                        ("lower", "Lower whisker (%)"),
                        ("upper", "Upper whisker (%)"),
                    )
                ],
            ]
        )
    marks = [line, box]
    for field in ("lower", "upper", "median"):
        band = 0.1 if field == "median" else 0.3
        marks.append(
            rule.encode(
                x=f"{field}:Q",
                y=gs.Y("gene:N", band=band),
                y2=gs.Y2("gene:N", band=1 - band),
            )
        )
    if len(outliers):
        dots = (
            gs.Chart(outliers)
            .mark_point(
                shape="circle",
                filled=False,
                color="black",
                size=PT**2,
                strokeWidth=PT,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(x="percent:Q", y="gene:N")
        )
        if hover:
            dots = dots.encode(
                tooltip=[
                    gs.Tooltip("gene:N", title="Gene"),
                    gs.Tooltip("cell_id:N", title="Cell ID"),
                    gs.Tooltip("cell:N", title="Cell"),
                    gs.Tooltip("percent:Q", title="Counts (%)", format=".4g"),
                ]
            )
        marks.append(dots)
    return (
        gs.layer(*marks)
        .properties(
            width=387.5 if width is None else width,
            height=(n_top * 0.2 + 1.5) * 77 if height is None else height,
        )
        .configure_axis(
            AXIS_TEXT,
            titleFontWeight="normal",
            labelPadding=4,
        )
        .configure_view(strokeWidth=0)
    )
