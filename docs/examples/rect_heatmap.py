"""Rect heatmap.

A dense quantitative grid rendered with rect marks and a continuous color
scale.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import heatmap_data
from genome_spy.schema import Scale

META = {
    "category": "Basics",
    "tags": ("rect", "heatmap", "color"),
    "order": 20,
    "height": 360,
}

data = heatmap_data()

chart = (
    gs.Chart(data)
    .mark_rect()
    .encode(
        x=gs.X("x:O").scale(zoom=True).axis(None),
        y=gs.Y("y:O").scale(zoom=True).axis(None),
        color=gs.Color("z:Q").scale(Scale(scheme="magma")).title("value"),
    )
    .properties(title="Rect heatmap")
)
