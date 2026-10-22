"""Original stored scores with fixed-bin boundaries and batch-specific thresholds."""

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse


def make_scrublet(batched=False):
    """Return stored scores only; the sparse expression matrix is deliberately empty."""
    observed = np.array(
        [0, 1 / 49, 2 / 49, 0.2, 0.2, 0.25, 0.8, 0.8, 0.8, 1, np.nan, -0.2, 1.2]
    )
    edges = np.linspace(0, 1, 50)
    simulated = np.repeat(
        (edges[:-1] + edges[1:]) / 2, np.tile([1, 2, 5, 1, 3, 1, 4], 7)
    )
    scores = np.tile(observed, 2 if batched else 1)
    a = ad.AnnData(
        sparse.csr_matrix((len(scores), 20000)),
        obs=pd.DataFrame(
            {"doublet_score": scores}, index=[f"cell-{i}" for i in range(len(scores))]
        ),
    )
    a.uns["scrublet"] = {"doublet_scores_sim": simulated, "threshold": 0.3}
    if batched:
        a.obs["sample"] = pd.Categorical(
            ["A"] * len(observed) + ["B"] * len(observed), categories=["B", "A"]
        )
        a.uns["scrublet"] = {
            "batched_by": "sample",
            "batches": {
                "B": {"doublet_scores_sim": simulated, "threshold": 0.27},
                "A": {"doublet_scores_sim": simulated[::-1]},
            },
        }
    return a
