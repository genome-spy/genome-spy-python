"""Positive and negative bars.

Draw bars from zero and color them according to their sign.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Basic charts and composition", "order": 30, "height": 340}

data = pd.DataFrame({"x": np.arange(60)})
chart = (
    gs.Chart(data)
    .transform_calculate(y=gs.expr.sin((gs.datum.x - 30) / 4) + (gs.datum.x - 30) / 30)
    .mark_rect()
    .encode(
        x=gs.X("x:I").scale(padding=0.1),
        y=gs.Y("y:Q"),
        # A data-space zero makes every bar start at the same baseline.
        y2=gs.Y2({"datum": 0}),
        color=gs.Color("y:Q")
        .scale(type="threshold", domain=[0], range=["#ed553b", "#20639b"])
        .legend(None),
    )
)
