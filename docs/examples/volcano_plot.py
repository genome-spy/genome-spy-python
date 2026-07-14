"""Volcano plot (GWAS effect vs significance).

Effect size against −log10 p for a HapMap association scan. Variants are colored
by whether they clear both an effect-size and a significance cutoff, and dashed
rules mark those thresholds — the classic volcano used to spotlight candidate
associations.

Data: real HapMap coordinates and gene annotations with simulated association
statistics, from the `manhattanly` R package via Plotly's Dash Bio datasets
(MIT). See `docs/_static/data/README.md` for provenance.
"""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.datasets import load_dataset
from genome_spy.schema import Scale

META = {
    "category": "Volcano and MA plots",
    "tags": ("layer", "thresholds", "real-data"),
    "order": 30,
    "height": 440,
}

EFFECT_CUTOFF = 0.5
P_CUTOFF = 1e-5


def hapmap_effects() -> pd.DataFrame:
    """Load the HapMap table and classify variants by effect and significance."""
    data = load_dataset("hapmap_gwas", as_format="dataframe")
    data = data[data["P"] > 0].copy()
    data["neglog"] = -np.log10(data["P"])
    passes = (data["P"] < P_CUTOFF) & (data["EFFECTSIZE"].abs() >= EFFECT_CUTOFF)
    data["association"] = np.where(
        passes & (data["EFFECTSIZE"] > 0),
        "risk",
        np.where(passes & (data["EFFECTSIZE"] < 0), "protective", "n.s."),
    )
    return data


data = hapmap_effects()

# Explicit, shared domains from the data. Without them the shared scale collapses
# onto the tiny cutoff-line datasets and clips every point to the axis edges.
x_extent = float(np.ceil(data["EFFECTSIZE"].abs().max() * 10) / 10)
X_DOMAIN = [-x_extent, x_extent]
Y_DOMAIN = [0.0, float(np.ceil(data["neglog"].max()))]

# --- Visualization -------------------------------------------------------------

association_colors = Scale(
    domain=["protective", "n.s.", "risk"],
    range=["#3e8cb6", "#c9d1d9", "#c53b2c"],
)

points = (
    gs.Chart(data)
    .mark_point(size=16, filled=True, opacity=0.6)
    .encode(
        x=gs.X("EFFECTSIZE:Q")
        .scale(domain=X_DOMAIN, zoom=True)
        .title("Effect size (beta)"),
        y=gs.Y("neglog:Q")
        .scale(reverse=False, domain=Y_DOMAIN, zoom=True)
        .title("−log10 p"),
        color=gs.Color("association:N")
        .scale(association_colors)
        .legend(title="Association"),
    )
)

effect_cutoffs = (
    gs.Chart([{"x": -EFFECT_CUTOFF}, {"x": EFFECT_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(x=gs.X("x:Q").scale(domain=X_DOMAIN, zoom=True).title("Effect size (beta)"))
)

significance_cutoff = (
    gs.Chart([{"y": -np.log10(P_CUTOFF)}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q").scale(reverse=False, domain=Y_DOMAIN, zoom=True).title("−log10 p")
    )
)

chart = (effect_cutoffs + significance_cutoff + points).properties(
    title="HapMap association volcano",
    description="Effect size versus significance, classified by effect-size and p-value cutoffs.",
)
