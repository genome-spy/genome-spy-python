"""Original fixed count data with a zero-total cell, ties and isolated outliers."""

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse


def make_counts(storage="dense"):
    """Return counts with known totals; storage changes no biological values."""
    values = np.zeros((21, 5), dtype=np.float64)
    values[1:, 0] = np.arange(1, 21) * 2
    values[1:, 1] = np.arange(20, 0, -1) * 2
    values[1:, 2] = 30
    values[-1, 2] = 450
    values[1:, 3] = 30
    values[1:, 4] = 1000 - values[1:, :4].sum(axis=1)
    matrix = (
        values if storage == "dense" else getattr(sparse, f"{storage}_matrix")(values)
    )
    return ad.AnnData(
        matrix,
        var=pd.DataFrame(
            {"symbol": ["A", "B", "C", "D", "E"]}, index=[f"gene-{i}" for i in range(5)]
        ),
    )
