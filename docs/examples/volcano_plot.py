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

# --- Visualization -------------------------------------------------------------

association_colors = Scale(
    domain=["protective", "n.s.", "risk"],
    range=["#3e8cb6", "#c9d1d9", "#c53b2c"],
)

points = (
    gs.Chart(data)
    .mark_point(size=16, filled=True, opacity=0.6)
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
    gs.Chart([{"x": -EFFECT_CUTOFF}, {"x": EFFECT_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(x=gs.X("x:Q").scale(domain=X_DOMAIN, zoom=True).title("Effect size (beta)"))
)

significance_cutoff = (
    gs.Chart([{"y": NEGLOG_P_CUTOFF}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(
        y=gs.Y("y:Q").scale(reverse=False, domain=Y_DOMAIN, zoom=True).title("−log10 p")
    )
)

chart = (effect_cutoffs + significance_cutoff + points).properties(
    title="HapMap association volcano",
    description="Effect size versus significance, classified by effect-size and p-value cutoffs.",
)
