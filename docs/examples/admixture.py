"""Admixture bar plot.

Per-individual ancestry proportions as a stacked bar plot. Each bar sums to one
across the ancestral components, individuals are grouped by population, and thin
white rules separate the groups. The stack positions are precomputed so the
visualization uses plain ``rect`` marks with ``y`` and ``y2``.
"""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.schema import Scale

META = {
    "category": "Population structure plots",
    "tags": ("stack", "rect", "layer"),
    "order": 10,
    "height": 340,
}

POPULATIONS = ["Pop 1", "Pop 2", "Pop 3", "Pop 4", "Pop 5"]
PER_POP = 24
K = 5


def admixture_stacks(seed: int = 5) -> pd.DataFrame:
    """Long, pre-stacked ancestry proportions with x/x2 columns and cumulative y."""
    rng = np.random.default_rng(seed)
    records = []
    index = 0
    for dominant, population in enumerate(POPULATIONS):
        block = []
        for _ in range(PER_POP):
            alpha = np.full(K, 0.3)
            alpha[dominant] = 6.0
            block.append(rng.dirichlet(alpha))
        # Sort within the population by the dominant component for clean bands.
        block.sort(key=lambda props: props[dominant])
        for proportions in block:
            cumulative = 0.0
            for component, value in enumerate(proportions):
                records.append(
                    {
                        "x0": index,
                        "x1": index + 1,
                        "y0": cumulative,
                        "y1": cumulative + value,
                        "ancestry": f"K{component + 1}",
                        "population": population,
                    }
                )
                cumulative += value
            index += 1
    return pd.DataFrame(records)


data = admixture_stacks()
separators = [PER_POP * i for i in range(1, len(POPULATIONS))]

# --- Visualization -------------------------------------------------------------

ancestry_colors = (
    Scale()
    .domain([f"K{i + 1}" for i in range(K)])
    .range(["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#b07aa1"])
)

bars = (
    gs.Chart(data)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q").scale(zoom=True).title("Individual"),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q").scale(reverse=False, domain=[0, 1]).title("Ancestry proportion"),
        y2=gs.Y2("y1"),
        color=gs.Color("ancestry:N").scale(ancestry_colors).legend(title="Component"),
    )
)

group_separators = (
    gs.Chart([{"x": boundary} for boundary in separators])
    .mark_rule(color="white", size=1.5)
    .encode(x=gs.X("x:Q").scale(zoom=True))
)

chart = (bars + group_separators).properties(
    title="Ancestry proportions across five populations",
    description="A stacked admixture bar plot grouped by population.",
)
