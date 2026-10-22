"""Small stored realizations with an incomplete final run."""

import numpy as np
import pandas as pd
from anndata import AnnData


def make_sim():
    """Return seven samples and two named profiles, with three samples per run."""
    return AnnData(
        np.array([[1, 8], [2, 6], [4, 3], [7, 2], [5, 4], [3, 5], [2, 7]], dtype=float),
        obs=pd.DataFrame(index=[f"sample-{i}" for i in range(7)]),
        var=pd.DataFrame(index=["A", "B"]),
        uns={"tmax_write": 3.0},
    )


def sim_cases():
    """Cover precedence, partial runs, numeric ticks and the shuffled point branch."""
    return {
        "points": {},
        "heatmap": {"as_heatmap": True},
        "override": {"tmax_realization": 4},
        "fractional": {"as_heatmap": True, "tmax_realization": 2.5},
        "long": {"tmax_realization": 20},
        "shuffle": {"shuffle": True, "marker": "o"},
        "shuffle_heatmap": {"shuffle": True, "as_heatmap": True},
    }
