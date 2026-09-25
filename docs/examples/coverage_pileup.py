"""Coverage and interval pileup.

Show how overlapping intervals produce a coverage profile.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {"category": "Basic charts and composition", "order": 31, "height": 420}

data = pd.DataFrame({"start": np.arange(1, 100)})

# Count overlaps above and arrange the same intervals into rows below.
coverage = (
    gs.Chart()
    .transform_coverage(start="start", end="end", as_="coverage")
    .mark_rect()
    .encode(x=gs.X("start:I"), x2=gs.X2("end"), y=gs.Y("coverage:Q"))
)
pileup = (
    gs.Chart()
    .transform_pileup(start="start", end="end", as_="lane")
    .mark_rect()
    .encode(
        x=gs.X("start:I"),
        x2=gs.X2("end"),
        y=gs.Y("lane:I").scale(padding=0.2, reverse=True, zoom=False),
    )
)
chart = (
    (coverage & pileup)
    .properties(data=data)
    # A deterministic mix of lengths keeps the example repeatable.
    .transform_calculate(end=gs.datum.start + 1 + (gs.datum.start * 7) % 20)
    .resolve_scale(x="shared")
)
