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

ma_points = (
    gs.Chart()
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

ma_fc_rules = (
    gs.Chart([{"side": -1}, {"side": 0}, {"side": 1}])
    .transform_formula(expr=gs.datum.side * effect_cutoff, as_="y")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q")
        .scale(reverse=False, domain=domains["ma_y"], zoom=True)
        .title("log2 fold change"),
    )
)

ma_callout_lines = (
    gs.Chart()
    .transform_filter(gs.datum.ma_label)
    .mark_rule(color="#3f4750", size=1, tooltip=None)
    .encode(
        x=gs.X("log10_base_mean:Q")
        .scale(domain=domains["ma_x"], zoom=True)
        .title("log10 mean count"),
        xOffset=gs.XOffset("ma_x_offset:Q").scale(None),
        y=gs.Y("log2fc:Q")
        .scale(reverse=False, domain=domains["ma_y"], zoom=True)
        .title("log2 fold change"),
        yOffset=gs.YOffset("ma_y_offset:Q").scale(None),
        x2=gs.X2("log10_base_mean"),
        y2=gs.Y2("log2fc"),
    )
    .properties(name="ma-callout-lines")
)


def ma_callout_label(*, side: str, name: str) -> gs.Chart:
    """Build one label layer just beyond its shortened leader line."""
    return (
        gs.Chart()
        .transform_filter(gs.datum.ma_label & (gs.datum.ma_label_side == side))
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
            x=gs.X("log10_base_mean:Q")
            .scale(domain=domains["ma_x"], zoom=True)
            .title("log10 mean count"),
            xOffset=gs.XOffset("ma_x_offset:Q").scale(None),
            y=gs.Y("log2fc:Q")
            .scale(reverse=False, domain=domains["ma_y"], zoom=True)
            .title("log2 fold change"),
            yOffset=gs.YOffset("ma_y_offset:Q").scale(None),
            text=gs.Text("ma_label:N"),
        )
        .properties(name=name)
    )


ma_callout_labels = [
    ma_callout_label(
        side=side,
        name=f"ma-label-{side}",
    )
    for side in ("left", "right")
]

chart = (
    gs.layer(
        ma_fc_rules,
        ma_points,
        ma_callout_lines,
        *ma_callout_labels,
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
