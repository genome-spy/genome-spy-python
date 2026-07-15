"""Volcano plot.

Log2 fold change against −log10 p-value, with color separating upregulated,
downregulated, and background genes. Dashed guide lines mark the significance
and fold-change cutoffs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import fdrcorrection

import genome_spy as gs
from genome_spy.datasets._airway import airway_paired_logcounts
from genome_spy.schema import Scale

META = {
    "category": "Volcano and MA plots",
    "tags": ("volcano", "real-data"),
    "order": 10,
    "height": 420,
    "max_width": 760,
}

LOG2FC_CUTOFF = 1.0
PVALUE_CUTOFF = 0.01
PADJ_CUTOFF = 0.1
MIN_BASE_MEAN = 10.0
MAX_GENES = 12_000

# Use pandas reshaping for the paired design, then delegate the actual
# statistics to SciPy and statsmodels.
base_mean, treated, control = airway_paired_logcounts(min_base_mean=MIN_BASE_MEAN)
log2fc = treated.subtract(control).mean(axis=1)
test = ttest_rel(treated.to_numpy(), control.to_numpy(), axis=1, nan_policy="omit")
pvalue = np.asarray(test.pvalue, dtype=float)
pvalue = np.where(
    ~np.isfinite(pvalue) & np.isclose(log2fc.to_numpy(), 0.0), 1.0, pvalue
)
pvalue = np.where(~np.isfinite(pvalue), 0.0, pvalue)
_rejected, padj = fdrcorrection(pvalue, alpha=PADJ_CUTOFF)

data = pd.DataFrame(
    {
        "ensgene": treated.index,
        "base_mean": base_mean.loc[treated.index].to_numpy(),
        "log2fc": log2fc.to_numpy(),
        "pvalue": pvalue,
        "padj": padj,
    }
)
data["neglog10_pvalue"] = -np.log10(np.clip(data["pvalue"], 1e-300, 1.0))
data["neglog10_padj"] = -np.log10(np.clip(data["padj"], 1e-300, 1.0))
data["log10_base_mean"] = np.log10(data["base_mean"])
passes = (data["pvalue"] < PVALUE_CUTOFF) & (data["log2fc"].abs() >= LOG2FC_CUTOFF)
data["direction"] = np.where(
    passes & (data["log2fc"] > 0),
    "up in dex",
    np.where(passes & (data["log2fc"] < 0), "down in dex", "n.s."),
)
data = data.nlargest(MAX_GENES, "base_mean").sort_values("log10_base_mean")
log2fc_extent = float(np.ceil(data["log2fc"].abs().max() * 2) / 2)
x_domain = [-log2fc_extent, log2fc_extent]
volcano_y_max = float(np.ceil(np.quantile(data["neglog10_pvalue"], 0.995) / 5) * 5)
volcano_y_domain = [0.0, volcano_y_max]
data["neglog10_pvalue_plot"] = np.minimum(data["neglog10_pvalue"], volcano_y_max)

direction_colors = (
    Scale()
    .domain(["down in dex", "n.s.", "up in dex"])
    .range(["#3e8cb6", "#c9d1d9", "#c53b2c"])
)

volcano_points = (
    gs.Chart(data)
    .mark_point(size=14, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log2fc:Q")
        .scale(domain=x_domain, zoom=True)
        .title("log2 fold change (treated / control)"),
        y=gs.Y("neglog10_pvalue_plot:Q")
        .scale(reverse=False, domain=volcano_y_domain, zoom=True)
        .title("-log10 p-value"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
    )
)

volcano_fc_rules = (
    gs.Chart([{"x": -LOG2FC_CUTOFF}, {"x": LOG2FC_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(x=gs.X("x:Q").scale(domain=x_domain, zoom=True))
)

volcano_padj_rule = (
    gs.Chart([{"y": -np.log10(PVALUE_CUTOFF)}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=volcano_y_domain, zoom=True)
        .title("-log10 p-value")
    )
)

chart = (volcano_fc_rules + volcano_padj_rule + volcano_points).properties(
    title="Airway dexamethasone response: volcano plot",
    description="A paired differential-expression volcano plot from real airway RNA-seq counts, using SciPy and statsmodels for inference.",
)
