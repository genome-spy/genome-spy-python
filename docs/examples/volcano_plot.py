"""Volcano plot.

Effect size against −log10 p-value, with color highlighting points that clear
both an effect-size and a significance cutoff.
"""

import genome_spy as gs
from genome_spy.datasets._hapmap import hapmap_volcano_data
from genome_spy.schema import Scale

META = {
    "category": "Volcano and MA plots",
    "order": 30,
    "height": 440,
}

data, domains = hapmap_volcano_data()
X_DOMAIN = domains["x_domain"]
Y_DOMAIN = domains["y_domain"]
EFFECT_CUTOFF = domains["effect_cutoff"]
NEGLOG_P_CUTOFF = domains["neglog_pvalue_cutoff"]
# zoomLevel is 1 at the initial domain. The exponent makes growth gradual,
# while the cap prevents points from becoming oversized at deep zoom levels.
ZOOM_LEVEL = gs.Expression("zoomLevel")
POINT_SIZE = gs.expr(gs.expr.min(16 * gs.expr.pow(ZOOM_LEVEL, 0.75), 64))
ASSOCIATION_EXPRESSION = gs.Expression(
    "datum.neglog >= hapmapSignificanceCutoff && "
    "abs(datum.EFFECTSIZE) >= hapmapEffectCutoff "
    "? (datum.EFFECTSIZE < 0 ? 'protective' : 'risk') : 'n.s.'"
)

# --- Visualization -------------------------------------------------------------

association_colors = Scale(
    domain=["protective", "n.s.", "risk"],
    range=["#3e8cb6", "#c9d1d9", "#c53b2c"],
)

points = (
    gs.Chart()
    .transform_formula(expr=ASSOCIATION_EXPRESSION, as_="association")
    .mark_point(size=POINT_SIZE, filled=True, opacity=0.6)
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
    gs.Chart([{"side": -1}, {"side": 1}])
    .transform_formula(expr=gs.Expression("datum.side * hapmapEffectCutoff"), as_="x")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(x=gs.X("x:Q").scale(domain=X_DOMAIN, zoom=True).title("Effect size (beta)"))
)

significance_cutoff = (
    gs.Chart([{}])
    .transform_formula(expr=gs.Expression("hapmapSignificanceCutoff"), as_="y")
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q").scale(reverse=False, domain=Y_DOMAIN, zoom=True).title("−log10 p")
    )
)

chart = (effect_cutoffs + significance_cutoff + points).properties(
    title="HapMap association volcano",
    data=data,
    params=[
        gs.param(
            "hapmapEffectCutoff",
            value=EFFECT_CUTOFF,
            bind={
                "input": "range",
                "min": 0,
                "max": X_DOMAIN[1],
                "step": 0.1,
                "name": "Absolute effect cutoff: ",
            },
        ),
        gs.param(
            "hapmapSignificanceCutoff",
            value=NEGLOG_P_CUTOFF,
            bind={
                "input": "range",
                "min": 0,
                "max": Y_DOMAIN[1],
                "step": 0.25,
                "name": "−log10 p cutoff: ",
            },
        ),
    ],
    description=(
        "Effect size versus significance, with interactive effect-size and "
        "p-value cutoffs controlling the guide lines and point colors."
    ),
)
