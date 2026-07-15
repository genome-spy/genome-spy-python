"""QQ plot.

Observed and expected −log10 p-values on matched axes. A dashed identity line
marks the null expectation, while departures in the upper tail reveal enriched
signal.
"""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.datasets import load_dataset
from genome_spy.schema import Scale

META = {
    "category": "Association plots",
    "tags": ("quantiles", "layer", "real-data", "vconcat"),
    "order": 20,
    "height": 560,
    "max_width": 840,
}


def hapmap_qq() -> pd.DataFrame:
    """Observed vs. expected −log10 p from the HapMap association p-values."""
    pvals = np.sort(
        load_dataset("hapmap_gwas", as_format="dataframe")
        .query("P > 0")["P"]
        .to_numpy()
    )
    ranks = np.arange(1, len(pvals) + 1)
    data = pd.DataFrame(
        {
            "expected": -np.log10((ranks - 0.5) / len(pvals)),
            "observed": -np.log10(pvals),
        }
    )
    data["delta"] = data["observed"] - data["expected"]
    data["pattern"] = np.where(
        data["delta"] > 0.45, "Tail enrichment", "Null-like bulk"
    )
    return data


def qq_deviation_bins(data: pd.DataFrame, *, bins: int = 45) -> pd.DataFrame:
    """Summarize QQ deviations into x-bins for a compact lower panel."""
    edges = np.linspace(0.0, float(data["expected"].max()), bins + 1)
    binned = (
        data.assign(
            bin=pd.cut(
                data["expected"],
                bins=edges,
                include_lowest=True,
                duplicates="drop",
            )
        )
        .groupby("bin", observed=True, as_index=False)
        .agg(delta_mean=("delta", "mean"))
    )
    intervals = binned["bin"]
    binned["x0"] = intervals.map(lambda interval: float(interval.left))
    binned["x1"] = intervals.map(lambda interval: float(interval.right))
    binned["zero"] = 0.0
    binned["direction"] = np.where(
        binned["delta_mean"] >= 0, "Observed > expected", "Observed < expected"
    )
    return binned[["x0", "x1", "zero", "delta_mean", "direction"]]


data = hapmap_qq()
deviation = qq_deviation_bins(data)
limit = float(max(data["expected"].max(), data["observed"].max())) * 1.02
annotation_x = round(limit * 0.54, 2)
delta_limit = float(max(abs(deviation["delta_mean"]).max(), 0.25)) * 1.1

pattern_colors = (
    Scale().domain(["Null-like bulk", "Tail enrichment"]).range(["#7fbbdd", "#c53b2c"])
)

deviation_colors = (
    Scale()
    .domain(["Observed > expected", "Observed < expected"])
    .range(["#c53b2c", "#7fbbdd"])
)

# --- Visualization -------------------------------------------------------------

diagonal = (
    gs.Chart([{"x": 0, "y": 0, "x2": limit, "y2": limit}])
    .mark_link(color="#6b7280", size=1.3, linkShape="line")
    .encode(
        x=gs.X("x:Q").scale(domain=[0, limit], zoom=True).axis(None).title(None),
        y=gs.Y("y:Q").scale(reverse=False, zoom=True).title("Observed −log10 p"),
        x2=gs.X2("x2"),
        y2=gs.Y2("y2"),
    )
)

points = (
    gs.Chart(data)
    .mark_point(size=18, filled=True, opacity=0.72)
    .encode(
        x=gs.X("expected:Q").scale(domain=[0, limit], zero=True, zoom=True).axis(None),
        y=gs.Y("observed:Q")
        .scale(reverse=False, domain=[0, limit], zero=True, zoom=True)
        .title("Observed −log10 p"),
        color=gs.Color("pattern:N").scale(pattern_colors).legend(title="Pattern"),
    )
)

line_label = (
    gs.Chart(
        [{"x": annotation_x, "y": annotation_x + 0.16, "label": "Null expectation"}]
    )
    .mark_text(color="#6b7280", align="left", baseline="bottom", size=11)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, limit], zero=True, zoom=True),
        y=gs.Y("y:Q").scale(reverse=False, domain=[0, limit], zero=True, zoom=True),
        text=gs.Text("label:N"),
    )
)

tail_label = (
    gs.Chart(
        [
            {
                "x": annotation_x,
                "y": round(limit * 0.93, 2),
                "label": "Upward tail suggests associated variants",
            }
        ]
    )
    .mark_text(color="#c53b2c", align="left", baseline="bottom", size=11)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, limit], zero=True, zoom=True),
        y=gs.Y("y:Q").scale(reverse=False, domain=[0, limit], zero=True, zoom=True),
        text=gs.Text("label:N"),
    )
)

deviation_zero = (
    gs.Chart([{"y": 0.0}])
    .mark_rule(color="#6b7280", size=1)
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=[-delta_limit, delta_limit], zero=True)
        .title("Observed − expected")
    )
)

deviation_bars = (
    gs.Chart(deviation)
    .mark_rect(stroke="white", strokeWidth=0.8)
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=[0, limit], zero=True, zoom=True)
        .title("Expected −log10 p"),
        x2=gs.X2("x1"),
        y=gs.Y("zero:Q").scale(reverse=False, domain=[-delta_limit, delta_limit]),
        y2=gs.Y2("delta_mean"),
        color=gs.Color("direction:N").scale(deviation_colors).legend(title="Deviation"),
    )
)

top = (diagonal + points + line_label + tail_label).properties(title="QQ pattern")
bottom = (deviation_zero + deviation_bars).properties(
    title="Deviation from the null line"
)

chart = gs.vconcat(top, bottom).properties(
    title="QQ plot of HapMap association p-values",
    description="Observed versus expected −log10 p values, paired with a lower deviation track. Most variants follow the null line, while the upper tail shows where association signals accumulate.",
)
