"""Layered lollipop plot.

Combine rules and point marks to show positive and negative values.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Basic charts and composition", "order": 27, "height": 360}

# Generate regularly spaced positions along a sine wave.
data = pd.DataFrame({"x": np.arange(0, 6.284, 0.39269908169)})

baseline = (
    gs.Chart(gs.Data(values=[{"zero": 0}]))
    .mark_rule(color="lightgray")
    .encode(y=gs.Y("zero:Q").title(None))
)
stems = gs.Chart().mark_rule(size=3)

# Point upward or downward according to the sign; use diamonds near zero.
heads = (
    gs.Chart()
    .mark_point(size=500, filled=True)
    .encode(
        shape=gs.Shape("sin(x):N")
        .scale(
            type="threshold",
            domain=[-0.01, 0.01],
            range=["triangle-down", "diamond", "triangle-up"],
        )
        .legend(None)
    )
)
lollipops = (
    (stems + heads)
    .properties(data=data)
    .transform_calculate(**{"sin(x)": gs.expr.sin(gs.datum.x)})
    .encode(
        x=gs.X("x:Q"), y=gs.Y("sin(x):Q").scale(padding=0.1), color=gs.Color("sin(x):Q")
    )
)
chart = baseline + lollipops
