"""Vertical concatenation.

Two related views are stacked vertically while sharing the same input table.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import sincos_data

META = {
    "category": "Basics",
    "order": 60,
    "height": 460,
}

data = sincos_data()

sin_chart = (
    gs.Chart(data)
    .transform_formula(expr=gs.expr.sin(gs.datum.x / 4), as_="value")
    .mark_point(size=45)
    .encode(
        x=gs.X("x:Q").scale(zoom=True),
        y=gs.Y("value:Q").scale(zoom=True).title("sin"),
    )
    .with_view(stroke="lightgray")
)
cos_chart = (
    gs.Chart(data)
    .transform_formula(expr=gs.expr.cos(gs.datum.x / 5), as_="value")
    .mark_point(size=45, color="#c53b2c")
    .encode(
        x=gs.X("x:Q").scale(zoom=True).title("Position"),
        y=gs.Y("value:Q").scale(zoom=True).title("cos"),
    )
    .with_view(stroke="lightgray")
)

chart = gs.vconcat(sin_chart, cos_chart, spacing=20).properties(
    title="Vertical concatenation"
)
