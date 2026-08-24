"""MA plot.

Mean expression against log2 fold change, with color highlighting genes that
pass a simple significance cutoff. This is the classic expression-change view
for spotting strong shifts across the dynamic range.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._airway import airway_differential_expression
from genome_spy.schema import Scale

META = {
    "category": "Volcano and MA plots",
    "order": 11,
    "height": 420,
    "max_width": 760,
}

LOG2FC_CUTOFF = 1.0
PVALUE_CUTOFF = 0.01
PADJ_CUTOFF = 0.1
MIN_BASE_MEAN = 10.0
MAX_GENES = 12_000

data, domains = airway_differential_expression(
    min_base_mean=MIN_BASE_MEAN,
    max_genes=MAX_GENES,
    log2fc_cutoff=LOG2FC_CUTOFF,
    pvalue_cutoff=PVALUE_CUTOFF,
    padj_alpha=PADJ_CUTOFF,
)

direction_colors = (
    Scale()
    .domain(["down in dex", "n.s.", "up in dex"])
    .range(["#3e8cb6", "#c9d1d9", "#c53b2c"])
)

ma_points = (
    gs.Chart(data)
    .mark_point(size=14, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log10_base_mean:Q")
        .scale(domain=domains["ma_x"], zoom=True)
        .title("log10 mean count"),
        y=gs.Y("log2fc:Q")
        .scale(reverse=False, domain=domains["ma_y"], zoom=True)
        .title("log2 fold change"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
    )
)

ma_fc_rules = (
    gs.Chart([{"y": -LOG2FC_CUTOFF}, {"y": 0.0}, {"y": LOG2FC_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q").scale(reverse=False, domain=domains["ma_y"], zoom=True),
    )
)

chart = (ma_fc_rules + ma_points).properties(
    title="Airway dexamethasone response: MA plot",
    description="A paired differential-expression MA plot showing mean expression against fold change.",
)
