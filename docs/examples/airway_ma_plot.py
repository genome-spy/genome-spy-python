"""Airway RNA-seq MA plot.

An MA view from the real Himes et al. airway RNA-seq dataset:
dexamethasone-treated airway smooth muscle cells versus matched controls across
four cell lines. The example uses pandas for wrangling, SciPy's paired t-test,
and statsmodels' Benjamini-Hochberg correction to keep the analysis code short
and library-backed. The plot colors points by raw p-value significance while
still computing adjusted p-values for reference; with only four matched pairs,
FDR-only coloring would make the MA plot visually flat. It is still a compact
visualization-oriented example, not a replacement for DESeq2 or edgeR.

Data: real bulk RNA-seq counts from the Bioconductor `airway` teaching dataset
(GEO GSE52778), vendored as scaled counts plus sample metadata. See
`docs/_static/data/README.md` for provenance.
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
    "tags": ("ma-plot", "real-data"),
    "order": 11,
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
ma_x_domain = [
    float(np.floor(data["log10_base_mean"].min() * 2) / 2),
    float(np.ceil(data["log10_base_mean"].max() * 2) / 2),
]
ma_y_domain = [-log2fc_extent, log2fc_extent]

direction_colors = Scale(
    domain=["down in dex", "n.s.", "up in dex"],
    range=["#3e8cb6", "#c9d1d9", "#c53b2c"],
)

ma_points = (
    gs.Chart(data)
    .mark_point(size=14, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log10_base_mean:Q")
        .scale(domain=ma_x_domain, zoom=True)
        .title("log10 mean count"),
        y=gs.Y("log2fc:Q")
        .scale(reverse=False, domain=ma_y_domain, zoom=True)
        .title("log2 fold change"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
    )
)

ma_fc_rules = (
    gs.Chart([{"y": -LOG2FC_CUTOFF}, {"y": 0.0}, {"y": LOG2FC_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q").scale(reverse=False, domain=ma_y_domain, zoom=True),
    )
)

chart = (ma_fc_rules + ma_points).properties(
    title="Airway dexamethasone response: MA plot",
    description="A paired differential-expression MA plot from real airway RNA-seq counts, using SciPy and statsmodels for inference.",
)
