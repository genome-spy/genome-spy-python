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
    "category": "Differential analysis",
    "order": 11,
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
    "airwayMaEffectCutoff",
    value=LOG2FC_CUTOFF,
    bind=gs.binding_range(
        min=0,
        max=3,
        step=0.1,
        name="Absolute log2 fold-change cutoff: ",
    ),
)
significance_cutoff = gs.param(
    "airwayMaSignificanceCutoff",
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

# Plot each gene's mean expression against its fold change.
ma_points = (
    gs.Chart()
    .transform_collect()
    .transform_formula(expr=DIRECTION_EXPRESSION, as_="direction")
    .mark_point(size=POINT_SIZE, filled=True, opacity=0.58)
    .encode(
        x=gs.X("log10_base_mean:Q")
        .scale(domain=domains["ma_x"], zoom=True)
        .title("log10 mean count"),
        y=gs.Y("log2fc:Q")
        .scale(reverse=False, domain=domains["ma_y"], zoom=True)
        .title("log2 fold change"),
        color=gs.Color("direction:N").scale(direction_colors).legend(title="Direction"),
        tooltip=airway_tooltip,
    )
)

# Draw the two fold-change cutoffs and a line at zero for no change.
ma_fc_rules = (
    gs.Chart([{"side": -1}, {"side": 0}, {"side": 1}])
    .transform_collect()
    .transform_formula(expr=gs.datum.side * effect_cutoff, as_="y")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=domains["ma_y"], zoom=True)
        .title("log2 fold change"),
    )
)

# Share the displaced layout between labels and their shortened leader lines.
ma_callout_lines = (
    gs.Chart()
    .mark_rule(color="#3f4750", size=1, tooltip=None)
    .encode(
        x2=gs.X2("log10_base_mean"),
        y2=gs.Y2("log2fc"),
        xOffset=gs.XOffset("leader_dx:Q").scale(None),
        yOffset=gs.YOffset("leader_dy:Q").scale(None),
    )
    .properties(name="ma-callout-lines")
)

ma_callout_labels = (
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
        text=gs.Text("ma_label:N"),
        xOffset=gs.XOffset("label_dx:Q").scale(None),
        yOffset=gs.YOffset("label_dy:Q").scale(None),
    )
    .properties(name="ma-labels")
)

ma_annotations = (
    (ma_callout_lines + ma_callout_labels)
    .transform_filter(gs.datum.ma_label)
    .transform_measure_text(
        field="ma_label", fontSize=14, fontWeight="bold", as_="label_width"
    )
    .transform_formula(expr=gs.datum.label_width + 4, as_="label_width")
    .transform_collect()
    .transform_filter(
        gs.expr.inrange(gs.datum.log10_base_mean, gs.expr.domain("x"))
        & gs.expr.inrange(gs.datum.log2fc, gs.expr.domain("y"))
    )
    # Tight collision boxes reduce unnecessary separation during zooming.
    .transform_displace2d(
        key="ensgene",
        x="log10_base_mean",
        y="log2fc",
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
        x=gs.X("log10_base_mean:Q").title("log10 mean count"),
        y=gs.Y("log2fc:Q").title("log2 fold change"),
    )
    .properties(name="ma-annotations")
)

# Put the points, guides, and labels together, then attach the sliders.
chart = (
    gs.layer(
        ma_fc_rules,
        ma_points,
        ma_annotations,
    )
    .properties(
        data=data,
        title="Airway dexamethasone response: MA plot",
        description=(
            "A paired differential-expression MA plot showing mean expression "
            "against fold change, with interactive thresholds and selected genes "
            "identified by callouts."
        ),
    )
    .add_params(effect_cutoff, significance_cutoff)
)
