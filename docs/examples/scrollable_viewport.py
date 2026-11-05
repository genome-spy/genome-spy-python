"""Scrollable viewport.

A unit view keeps its row height while the outer container provides a vertical
viewport. It starts at the last rows and keeps their distance from the bottom.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import sincos_data

META = {
    "category": "Interaction and exploration",
    "order": 70,
    "height": 260,
}

# Load example positions, one for each row.
data = sincos_data()

# Plot a sine value on each row.
chart = (
    gs.Chart(data)
    .transform_formula(expr=gs.expr.sin(gs.datum.x / 4), as_="value")
    .mark_point(size=55)
    .encode(
        x=gs.X("value:Q").scale(zoom=True).title("Value"),
        y=gs.Y("x:O").title("Row"),
    )
    # Keep rows 20 pixels tall and scroll when they do not all fit.
    .properties(
        height=gs.step(20),
        viewportHeight=gs.ViewportSizeDef(grow=1, anchor="end"),
        title="Scrollable viewport",
    )
    .with_view(stroke="lightgray")
)

chart = chart.configure_legend(selectionLabel=False)
