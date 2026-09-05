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
# zoomLevel is 1 at the initial domain. The exponent makes growth gradual,
# while the cap prevents points from becoming oversized at deep zoom levels.
ZOOM_LEVEL = gs.Expression("zoomLevel")
POINT_SIZE = gs.expr(gs.expr.min(14 * gs.expr.pow(ZOOM_LEVEL, 0.75), 64))

data, domains = airway_differential_expression(
    min_base_mean=MIN_BASE_MEAN,
    max_genes=MAX_GENES,
    log2fc_cutoff=LOG2FC_CUTOFF,
    pvalue_cutoff=PVALUE_CUTOFF,
    padj_alpha=PADJ_CUTOFF,
)
# The sliders are named parameters. Their handles drive both the guide lines
# and the browser-side classification below.
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
DIRECTION_EXPRESSION = gs.expr.if_(
    (gs.datum.neglog10_pvalue >= significance_cutoff)
    & (gs.expr.abs(gs.datum.log2fc) >= effect_cutoff),
    gs.expr.if_(gs.datum.log2fc < 0, "down in dex", "up in dex"),
    "n.s.",
)

direction_colors = (
    Scale()
    .domain(["down in dex", "n.s.", "up in dex"])
    .range(["#3e8cb6", "#c9d1d9", "#c53b2c"])
)

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

volcano_points = (
    gs.Chart()
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

volcano_fc_rules = (
    gs.Chart([{"side": -1}, {"side": 1}])
    .transform_formula(expr=gs.datum.side * effect_cutoff, as_="x")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        x=gs.X("x:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)")
    )
)

volcano_padj_rule = (
    gs.Chart([{}])
    .transform_formula(expr=significance_cutoff, as_="y")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value")
    )
)

# Offsets are logical pixels, so zooming the data scales does not move labels.
# The shifted label endpoint uses the primary channels; the point is x2/y2.
volcano_callout_lines = (
    gs.Chart()
    .transform_filter(gs.datum.volcano_label)
    .mark_rule(color="#3f4750", size=1, tooltip=None)
    .encode(
        x=gs.X("log2fc:Q")
        .scale(domain=domains["volcano_x"], zoom=True)
        .title("log2 fold change (treated / control)"),
        xOffset=gs.XOffset("volcano_x_offset:Q").scale(None),
        y=gs.Y("neglog10_pvalue_plot:Q")
        .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
        .title("-log10 p-value"),
        yOffset=gs.YOffset("volcano_y_offset:Q").scale(None),
        x2=gs.X2("log2fc"),
        y2=gs.Y2("neglog10_pvalue_plot"),
    )
    .properties(name="volcano-callout-lines")
)


def volcano_callout_label(*, side: str, name: str) -> gs.Chart:
    """Build one label layer just beyond its shortened leader line."""
    return (
        gs.Chart()
        .transform_filter(
            gs.datum.volcano_label & (gs.datum.volcano_label_side == side)
        )
        .mark_text(
            align="right" if side == "left" else "left",
            baseline="middle",
            dx=-4 if side == "left" else 4,
            dy=0,
            fontWeight="bold",
            color="#20262d",
            tooltip=None,
        )
        .encode(
            x=gs.X("log2fc:Q")
            .scale(domain=domains["volcano_x"], zoom=True)
            .title("log2 fold change (treated / control)"),
            xOffset=gs.XOffset("volcano_x_offset:Q").scale(None),
            y=gs.Y("neglog10_pvalue_plot:Q")
            .scale(reverse=False, domain=domains["volcano_y"], zoom=True)
            .title("-log10 p-value"),
            yOffset=gs.YOffset("volcano_y_offset:Q").scale(None),
            text=gs.Text("volcano_label:N"),
        )
        .properties(name=name)
    )


volcano_callout_labels = [
    volcano_callout_label(
        side=side,
        name=f"volcano-label-{side}",
    )
    for side in ("left", "right")
]

chart = (
    gs.layer(
        volcano_fc_rules,
        volcano_padj_rule,
        volcano_points,
        volcano_callout_lines,
        *volcano_callout_labels,
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
