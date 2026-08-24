"""Link mark.

Dome-shaped links connect paired positions and demonstrate interval-style
relationships in a compact view.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import link_data

META = {
    "category": "Basics",
    "order": 40,
    "height": 300,
}

data = link_data()

chart = (
    gs.Chart(data)
    .mark_link(linkShape="dome", size=2)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 18], zoom=True).title("Start"),
        x2=gs.X2("x2:Q"),
    )
    .properties(title="Dome-shaped links")
)
