"""Ranged rule mark.

Intervals are represented by rules with start and end encodings, a useful
pattern for compact feature and confidence-interval tracks.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import ranged_rule_data

META = {
    "category": "Basics",
    "order": 30,
    "height": 280,
}

data = ranged_rule_data()

chart = (
    gs.Chart(data)
    .mark_rule(size=10, strokeCap="round")
    .encode(
        x=gs.X("x:Q").scale(zoom=True).title("Start"),
        x2=gs.X2("x2"),
        y=gs.Y("y:N").scale(zoom=True).title("Interval"),
    )
    .properties(title="Ranged rule mark")
)
