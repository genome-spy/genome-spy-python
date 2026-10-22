"""Native observed/simulated Scrublet histograms and threshold rules."""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import coordinate_domain
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS as PT


def build_scrublet(
    bins: pd.DataFrame,
    thresholds: list[float | None],
    *,
    scales: tuple[str, str],
    hover: bool,
    zoom: bool,
    width: float,
    height: float,
) -> gs.TopLevelSpec:
    """Return one observed/simulated pair per batch from prepared densities and cutoffs."""
    panels = []
    for index, rows in bins.groupby("panel", sort=False):
        index = int(index)
        scale = scales[index % 2]
        threshold = thresholds[index]
        density = rows.density.to_numpy()
        if scale == "log":
            ydomain = coordinate_domain(density[density > 0], 0.05, log=True)
        else:
            ydomain = (0.0, float(density.max()) * 1.05)
        xdomain = coordinate_domain(
            np.array([0, 1, threshold] if threshold is not None else [0, 1]), 0.05
        )
        x = (
            gs.X("start:Q")
            .scale(
                type="linear",
                domain=list(xdomain),
                nice=False,
                zero=False,
                zoom=zoom,
                name=f"scrublet-x-{index}",
            )
            .axis(title="Doublet score", domain=False)
        )
        y = (
            gs.Y("density:Q")
            .scale(
                type="log" if scale == "log" else "linear",
                domain=list(ydomain),
                nice=False,
                zero=False,
                name=f"scrublet-y-{index}",
            )
            .axis(title="Prob. density", domain=False)
        )
        bars = (
            gs.Chart(bins)
            .transform_filter(f"datum.panel == {index} && datum.density > 0")
            .mark_rect(
                color="gray",
                minHeight=0,
                minWidth=0,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                x=x,
                x2="end:Q",
                y=y,
                y2=gs.Y2(
                    datum=ydomain[0] if scale == "log" else 0, type="quantitative"
                ),
            )
        )
        if hover:
            bars = bars.encode(
                tooltip=[
                    gs.Tooltip("batch:N", title="Batch"),
                    gs.Tooltip("sample:N", title="Sample"),
                    gs.Tooltip("start:Q", title="Bin start", format=".4g"),
                    gs.Tooltip("end:Q", title="Bin end", format=".4g"),
                    gs.Tooltip("count:Q", title="Count", format="d"),
                    gs.Tooltip("density:Q", title="Probability density", format=".4g"),
                ]
            )
        panel = gs.layer(bars)
        if threshold is not None:
            rule = (
                gs.Chart([{"threshold": threshold}])
                .mark_rule(color="black", size=PT, clip=True, tooltip=None)
                .encode(x="threshold:Q", y=gs.value(0), y2=gs.value(1))
            )
            panel = panel + rule
        panels.append(
            panel.properties(
                width=width,
                height=height,
                title=gs.Title(
                    text=rows.title.iloc[0],
                    anchor="middle",
                    font=FONT,
                    fontSize=12 * PT,
                    fontWeight="normal",
                ),
            )
        )
    pairs = [
        gs.hconcat(*panels[i : i + 2], spacing=60).resolve_scale(
            x="independent", y="independent"
        )
        for i in range(0, len(panels), 2)
    ]
    return (
        gs.vconcat(*pairs, spacing=60)
        .resolve_scale(x="independent", y="independent")
        .configure_axis(
            labelFont=FONT,
            titleFont=FONT,
            labelFontSize=10 * PT,
            titleFontSize=10 * PT,
            titleFontWeight="normal",
            labelPadding=4,
        )
        .configure_view(stroke="black", strokeWidth=0.8 * PT)
    )
