"""Point shapes and styles.

Vary point shape, fill, size, outline, and rotation in a small grid.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Basics", "order": 29, "height": 360}

# Create positions for 20 columns and eight rows of points.
data = pd.DataFrame({"z": np.arange(160)})
chart = (
    gs.Chart(data)
    .transform_calculate(x=gs.datum.z % 20, y=gs.expr.floor(gs.datum.z / 20))
    .mark_point(stroke="black")
    .encode(
        x=gs.X("x:O").axis(None),
        y=gs.Y("y:O").axis(None),
        shape=gs.Shape("x:N"),
        fill=gs.Fill("x:N"),
        # Change shape, color, and size across columns.
        size=gs.Size("x:Q").scale(type="pow", exponent=2, range=[0, 900]),
        # Change outline thickness and angle down the rows.
        strokeWidth=gs.StrokeWidth("y:Q").scale(range=[0, 4]),
        angle=gs.Angle("y:Q").scale(range=[0, 45]),
    )
    .configure_legend(disable=True)
)
