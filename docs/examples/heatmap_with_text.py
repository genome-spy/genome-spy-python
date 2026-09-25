"""Heatmap with zoomable values.

Zoom into a patterned heatmap to reveal the value of each cell.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Interaction and exploration", "order": 25, "height": 480}

# Create one row for each cell in a 200 × 200 grid.
grid = pd.DataFrame({"i": np.arange(40000)})

tiles = gs.Chart().mark_rect().encode(color=gs.Color("z:Q").scale(scheme="viridis"))

# Values appear when cells are large enough; dark cells get white text.
values = (
    gs.Chart()
    .mark_text(size=12, opacity=0.8, fitToBand=True, paddingX=4, paddingY=3)
    .encode(
        text=gs.Text("z:Q", format=".2f"),
        color=gs.Color("z:Q")
        .scale(type="threshold", domain=[0], range=["white", "black"])
        .legend(None),
    )
)

# Hide the hint as the reader zooms in.
hint = (
    gs.Chart(gs.Data(values=[{}]))
    .mark_text(
        size=13,
        color="white",
        align="left",
        baseline="bottom",
        dx=5,
        dy=-5,
        text="Zoom in using the mouse wheel!",
    )
    .encode(x=gs.value(0), y=gs.value(0))
    .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[0.1, 0.05], values=[1, 0]))
)

# Share the grid and positions, but keep tile and text colors separate.
chart = (
    (tiles + values + hint)
    .properties(data=grid)
    .transform_calculate(x=gs.datum.i % 200, y=gs.expr.floor(gs.datum.i / 200))
    .transform_project(fields=["x", "y"])
    .transform_calculate(
        z=gs.expr.sin(
            (
                gs.expr.sin(gs.datum.x / 30)
                + gs.expr.cos(gs.datum.y / 25 - 0.5 + gs.expr.sin(gs.datum.x / 40) * 2)
            )
            * 4
        )
    )
    .encode(x=gs.X("x:I"), y=gs.Y("y:I"))
    .resolve_scale(color="independent")
    # Let the plot fit the gallery container, including its axes and legend.
    .properties(title="Heatmap with zoomable values")
)
