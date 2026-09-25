"""Points that grow when zooming.

Explore 200,000 generated points without losing them as you zoom in.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Interaction and exploration", "order": 32, "height": 360}

# A fixed seed keeps the noisy wave the same each time.
rng = np.random.default_rng(42)
data = pd.DataFrame({"x": np.arange(200000), "u": rng.random(200000) * 0.682})
zoom = gs.Expression("zoomLevel")

chart = (
    gs.Chart(data)
    # Calculate the wave from the prepared positions and noise.
    .transform_calculate(
        y=(
            gs.expr.if_(gs.datum.u % 1e-8 > 5e-9, 1, -1)
            * (gs.expr.sqrt(-gs.expr.log(gs.expr.max(1e-9, gs.datum.u))) - 0.618)
        )
        * 1.618
        + gs.expr.sin(gs.datum.x / 10000)
    )
    # Increase point size with zoom, up to a readable maximum.
    .mark_point(size=gs.expr(gs.expr.min(0.5 * gs.expr.pow(zoom, 1.5), 200)))
    .encode(
        x=gs.X("x:Q").scale(zoom=True).axis(format="~s", labelFlush=True),
        y=gs.Y("y:Q"),
        opacity=gs.value(0.6),
    )
)
