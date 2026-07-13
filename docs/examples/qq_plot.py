"""QQ plot.

Quantile-quantile plot of a HapMap association scan: observed −log10 p against
the values expected under the null. Points hug the diagonal except for a tail of
associated variants that lifts away from it. A dashed identity line marks the
null expectation.

Data: real HapMap coordinates and gene annotations with simulated association
statistics, from the `manhattanly` R package via Plotly's Dash Bio datasets
(MIT). See `docs/_static/data/README.md` for provenance.
"""

from pathlib import Path

import numpy as np
import pandas as pd

import genome_spy as gs

META = {
    "category": "GWAS",
    "tags": ("quantiles", "layer", "real-data"),
    "order": 20,
    "height": 440,
}

DATA = Path(__file__).parent.parent / "_static" / "data" / "hapmap_gwas.csv"


def hapmap_qq() -> pd.DataFrame:
    """Observed vs. expected −log10 p from the HapMap association p-values."""
    pvals = np.sort(pd.read_csv(DATA).query("P > 0")["P"].to_numpy())
    ranks = np.arange(1, len(pvals) + 1)
    return pd.DataFrame(
        {
            "expected": -np.log10((ranks - 0.5) / len(pvals)),
            "observed": -np.log10(pvals),
        }
    )


data = hapmap_qq()
limit = float(max(data["expected"].max(), data["observed"].max())) * 1.02

# --- Visualization -------------------------------------------------------------

diagonal = (
    gs.Chart([{"x": 0, "y": 0, "x2": limit, "y2": limit}])
    .mark_link(color="#c53b2c", size=1.3, linkShape="line")
    .encode(
        x=gs.X("x:Q").scale(zoom=True).title("Expected −log10 p"),
        y=gs.Y("y:Q").scale(reverse=False, zoom=True).title("Observed −log10 p"),
        x2=gs.X2("x2"),
        y2=gs.Y2("y2"),
    )
)

points = (
    gs.Chart(data)
    .mark_point(size=16, filled=True, opacity=0.6)
    .encode(
        x=gs.X("expected:Q").scale(zero=True, zoom=True).title("Expected −log10 p"),
        y=gs.Y("observed:Q")
        .scale(reverse=False, zero=True, zoom=True)
        .title("Observed −log10 p"),
    )
)

chart = (diagonal + points).properties(
    title="QQ plot of HapMap association p-values",
    description="Observed versus expected −log10 p with a null identity line.",
)
