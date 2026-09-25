"""Horizontal stacked bars.

Compare barley yields by variety, with each growing site shown as a segment.
"""

import genome_spy as gs

META = {"category": "Basic charts and composition", "order": 26, "height": 400}

# Load the same barley table used by the upstream example.
data = gs.Data(url="https://cdn.jsdelivr.net/npm/vega-datasets@2.9.0/data/barley.json")

chart = (
    gs.Chart(data)
    # Sum the years for each site, then place the site totals side by side.
    .transform_aggregate(
        groupby=["variety", "site"], fields=["yield"], ops=["sum"], as_=["yieldSum"]
    )
    .transform_stack(
        field="yieldSum",
        groupby=["variety"],
        sort=gs.compare("site"),
        as_=["yieldStart", "yieldEnd"],
    )
    .mark_rect()
    .encode(
        x=gs.X("yieldStart:Q").title("Sum of yield"),
        x2=gs.X2("yieldEnd"),
        y=gs.Y("variety:N").scale(padding=0.1),
        color=gs.Color("site:N"),
    )
    .configure_legend(disable=False, orient="bottom", direction="horizontal", offset=18)
    .properties(background="#fafafa")
)
