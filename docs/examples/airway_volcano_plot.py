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
HALO_OFFSETS = [(-1.25, -1.25), (1.25, -1.25), (-1.25, 1.25), (1.25, 1.25)]

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


def volcano_callout_label(
    *, side: str, color: str, dx: float, dy: float, name: str
) -> gs.Chart:
    """Build one edge-anchored label or halo layer."""
    return (
        gs.Chart()
        .transform_filter(
            gs.datum.volcano_label & (gs.datum.volcano_label_side == side)
        )
        .mark_text(
            align="right" if side == "left" else "left",
            baseline="middle",
            dx=dx,
            dy=dy,
            fontWeight="bold",
            color=color,
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


volcano_callout_halos = [
    volcano_callout_label(
        side=side,
        color="white",
        dx=(-4 if side == "left" else 4) + halo_dx,
        dy=halo_dy,
        name=f"volcano-label-halo-{side}-{index}",
    )
    for side in ("left", "right")
    for index, (halo_dx, halo_dy) in enumerate(HALO_OFFSETS)
]
volcano_callout_labels = [
    volcano_callout_label(
        side=side,
        color="#20262d",
        dx=-4 if side == "left" else 4,
        dy=0,
        name=f"volcano-label-{side}",
    )
    for side in ("left", "right")
]

chart = gs.layer(
    volcano_fc_rules,
    volcano_padj_rule,
    volcano_points,
    volcano_callout_lines,
    *volcano_callout_halos,
    *volcano_callout_labels,
).properties(
    data=data,
    title="Airway dexamethasone response: volcano plot",
    description=(
        "A paired differential-expression volcano plot showing fold change "
        "against significance, with selected genes identified by callouts."
    ),
)
