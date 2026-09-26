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
    "category": "Differential analysis",
    "order": 10,
    "height": 420,
    "max_width": 760,
}

LOG2FC_CUTOFF = 1.0
PVALUE_CUTOFF = 0.01
PADJ_CUTOFF = 0.1
MIN_BASE_MEAN = 10.0
MAX_GENES = 12_000
# Grow points gently when zooming in, without letting them become too large.
ZOOM_LEVEL = gs.Expression("zoomLevel")
POINT_SIZE = gs.expr(gs.expr.min(14 * gs.expr.pow(ZOOM_LEVEL, 0.75), 64))

# Load gene results with fold changes, p-values, and selected gene labels.
data, domains = airway_differential_expression(
    min_base_mean=MIN_BASE_MEAN,
    max_genes=MAX_GENES,
    log2fc_cutoff=LOG2FC_CUTOFF,
    pvalue_cutoff=PVALUE_CUTOFF,
    padj_alpha=PADJ_CUTOFF,
)
# Add sliders to change the cutoffs and see point colors update immediately.
effect_cutoff = gs.param(
    "airwayVolcanoEffectCutoff",
    value=LOG2FC_CUTOFF,
    bind=gs.binding_range(
        min=0,
        max=3,
        step=0.1,
        name="Absolute log2 fold-change cutoff: ",
    ),
)
significance_cutoff = gs.param(
    "airwayVolcanoSignificanceCutoff",
    value=domains["pvalue_cutoff"][0],
    bind=gs.binding_range(
        min=0,
        max=domains["volcano_y"][1],
        step=0.25,
        name="−log10 p cutoff: ",
    ),
)
# Label genes as up or down only when they pass both cutoffs.
DIRECTION_EXPRESSION = gs.expr.if_(
    (gs.datum.neglog10_pvalue >= significance_cutoff)
    & (gs.expr.abs(gs.datum.log2fc) >= effect_cutoff),
    gs.expr.if_(gs.datum.log2fc < 0, "down in dex", "up in dex"),
    "n.s.",
)

# Use blue for decreases, red for increases, and grey for the remaining genes.
direction_colors = (
    Scale()
    .domain(["down in dex", "n.s.", "up in dex"])
    .range(["#3e8cb6", "#c9d1d9", "#c53b2c"])
)

# Choose the gene details to show on hover.
airway_tooltip = [
    gs.Tooltip("ensgene:N"),
    gs.Tooltip("base_mean:Q"),
    gs.Tooltip("log2fc:Q"),
    gs.Tooltip("pvalue:Q"),
    gs.Tooltip("padj:Q"),
    gs.Tooltip("neglog10_pvalue:Q"),
    gs.Tooltip("neglog10_padj:Q"),
    gs.Tooltip("direction:N"),
]

# Plot each gene's fold change against its significance.
volcano_points = (
    gs.Chart()
    .transform_collect()
    .transform_formula(expr=DIRECTION_EXPRESSION, as_="direction")
    .mark_point(size=POINT_SIZE, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log2fc:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)"),
        y=gs.Y("neglog10_pvalue_plot:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
        tooltip=airway_tooltip,
    )
)

# Mark the fold-change cutoff on both sides of zero.
volcano_fc_rules = (
    gs.Chart([{"side": -1}, {"side": 1}])
    .transform_collect()
    .transform_formula(expr=gs.datum.side * effect_cutoff, as_="x")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        x=gs.X("x:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)")
    )
)

# Move the horizontal significance line with its slider.
volcano_padj_rule = (
    gs.Chart([{}])
    .transform_collect()
    .transform_formula(expr=significance_cutoff, as_="y")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value")
    )
)

# Share the displaced layout between labels and their shortened leader lines.
volcano_callout_lines = (
    gs.Chart()
    .mark_rule(color="#3f4750", size=1, tooltip=None)
    .encode(
        x2=gs.X2("log2fc"),
        y2=gs.Y2("neglog10_pvalue_plot"),
        xOffset=gs.XOffset("leader_dx:Q").scale(None),
        yOffset=gs.YOffset("leader_dy:Q").scale(None),
    )
    .properties(name="volcano-callout-lines")
)

volcano_callout_labels = (
    gs.Chart()
    .mark_text(
        align="center",
        baseline="middle",
        size=14,
        fontWeight="bold",
        color="#20262d",
        tooltip=None,
    )
    .encode(
        text=gs.Text("volcano_label:N"),
        xOffset=gs.XOffset("label_dx:Q").scale(None),
        yOffset=gs.YOffset("label_dy:Q").scale(None),
    )
    .properties(name="volcano-labels")
)

volcano_annotations = (
    (volcano_callout_lines + volcano_callout_labels)
    .transform_filter(gs.datum.volcano_label)
    .transform_measure_text(
        field="volcano_label", fontSize=14, fontWeight="bold", as_="label_width"
    )
    .transform_formula(expr=gs.datum.label_width + 4, as_="label_width")
    .transform_collect()
    .transform_filter(
        gs.expr.inrange(gs.datum.log2fc, gs.expr.domain("x"))
        & gs.expr.inrange(gs.datum.neglog10_pvalue_plot, gs.expr.domain("y"))
    )
    # Tight collision boxes reduce unnecessary separation during zooming.
    .transform_displace2d(
        key="ensgene",
        x="log2fc",
        y="neglog10_pvalue_plot",
        width="label_width",
        height=16,
        anchorWidth=8,
        anchorHeight=8,
        as_=["label_dx", "label_dy"],
    )
    # Stop each leader at the padded label box instead of crossing the text.
    .transform_formula(
        expr=gs.expr.max(
            0,
            1
            - gs.expr.min(
                gs.datum.label_width / 2 / gs.expr.max(abs(gs.datum.label_dx), 1e-6),
                8 / gs.expr.max(abs(gs.datum.label_dy), 1e-6),
            ),
        ),
        as_="leader_scale",
    )
    .transform_formula(expr=gs.datum.label_dx * gs.datum.leader_scale, as_="leader_dx")
    .transform_formula(expr=gs.datum.label_dy * gs.datum.leader_scale, as_="leader_dy")
    .encode(
        x=gs.X("log2fc:Q").title("log2 fold change (treated / control)"),
        y=gs.Y("neglog10_pvalue_plot:Q").title("-log10 p-value"),
    )
    .properties(name="volcano-annotations")
)

# Put the points, guides, and labels together, then attach the sliders.
chart = (
    gs.layer(
        volcano_fc_rules,
        volcano_padj_rule,
        volcano_points,
        volcano_annotations,
    )
    .properties(
        data=data,
        title="Airway dexamethasone response: volcano plot",
        description=(
            "A paired differential-expression volcano plot showing fold change "
            "against significance, with interactive thresholds and selected "
            "genes identified by callouts."
        ),
    )
    .add_params(effect_cutoff, significance_cutoff)
)
