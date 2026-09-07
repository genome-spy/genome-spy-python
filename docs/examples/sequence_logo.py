"""Sequence logo.

Letter marks are stacked by information content to show a compact sequence
motif summary.
"""

import genome_spy as gs
from genome_spy.datasets._grammar import sequence_logo_data
from genome_spy.schema import Scale

META = {
    "category": "Basics",
    "order": 50,
    "height": 300,
}

# Load example base counts at each position.
data = sequence_logo_data()

base_colors = Scale(
    domain=["A", "C", "T", "G"],
    range=["#7bd56c", "#ff9b9b", "#86bbf1", "#ffc56c"],
)

# Stack the base letters: taller stacks indicate more consistent positions.
chart = (
    gs.Chart(data)
    .transform_stack(
        field="count",
        groupby=["pos"],
        offset="information",
        as_=["_y0", "_y1"],
        baseField="base",
        sort=gs.compare("count", order="ascending"),
    )
    # Stretch each letter to fill its share of the stack.
    .mark_text(
        font="Source Sans Pro",
        fontWeight=700,
        size=90,
        squeeze=True,
        fitToBand=True,
        paddingX=0,
        paddingY=0,
        logoLetters=True,
    )
    .encode(
        x=gs.X("pos:O").title("Position"),
        y=gs.Y("_y0:Q").scale(domain=[0, 2], zoom=True).title("Information"),
        y2=gs.Y2("_y1"),
        text=gs.Text("base:N"),
        color=gs.Color("base:N").scale(base_colors).legend(None),
    )
    .properties(title="Sequence logo")
)
