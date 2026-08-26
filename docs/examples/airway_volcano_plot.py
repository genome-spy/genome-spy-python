"""Volcano plot.

Log2 fold change against −log10 p-value, with color separating upregulated,
downregulated, and background genes. Dashed guide lines mark the significance
and fold-change cutoffs.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._airway import airway_differential_expression
from genome_spy.schema import Scale

META = {
    "category": "Volcano and MA plots",
    "order": 10,
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

volcano_points = (
    gs.Chart(data)
    .mark_point(size=14, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log2fc:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)"),
        y=gs.Y("neglog10_pvalue_plot:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
    )
)

volcano_fc_rules = (
    gs.Chart([{"x": -LOG2FC_CUTOFF}, {"x": LOG2FC_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        x=gs.X("x:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)")
    )
)

volcano_padj_rule = (
    gs.Chart([{"y": domains["pvalue_cutoff"][0]}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value")
    )
)

volcano_callout_lines = (
    gs.Chart(data)
    .transform_filter("datum.volcano_label")
    .mark_rule(color="#3f4750", size=1)
    .encode(
        x=gs.X("log2fc:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)"),
        x2=gs.X2("volcano_label_x:Q"),
        y=gs.Y("neglog10_pvalue_plot:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value"),
        y2=gs.Y2("volcano_label_y:Q"),
    )
)

volcano_callout_labels = (
    gs.Chart(data)
    .transform_filter("datum.volcano_label")
    .mark_text(
        align="center",
        baseline="bottom",
        yOffset=-3,
        fontWeight="bold",
        color="#20262d",
    )
    .encode(
        x=gs.X("volcano_label_x:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)"),
        y=gs.Y("volcano_label_y:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value"),
        text=gs.Text("volcano_label:N"),
    )
)

chart = (
    volcano_fc_rules
    + volcano_padj_rule
    + volcano_points
    + volcano_callout_lines
    + volcano_callout_labels
).properties(
    title="Airway dexamethasone response: volcano plot",
    description=(
        "A paired differential-expression volcano plot showing fold change "
        "against significance, with selected genes identified by callouts."
    ),
)
