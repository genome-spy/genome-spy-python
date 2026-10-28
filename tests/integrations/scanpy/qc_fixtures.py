"""Small QC inputs shared by semantic and browser tests."""

from __future__ import annotations

import anndata as ad
import numpy as np
import pandas as pd
from anndata import AnnData
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


def make_hvg_result(storage="frame", flavor="seurat"):
    """Return the same eight gene statistics as a frame, AnnData or legacy records."""
    statistic = "variances" if flavor == "seurat_v3" else "dispersions"
    frame = pd.DataFrame(
        {
            "means": np.array([0.1, 0.3, 0.8, 1.4, 2, 3.5, 6, 10], dtype=np.float32),
            statistic: np.array([0.5, 0.7, 1, 1.2, 2, 3, 5, 8], dtype=np.float32),
            f"{statistic}_norm": np.array(
                [0.8, 2, 0.5, 4, 1.3, 5, 2.5, 8], dtype=np.float32
            ),
            "highly_variable": [True, False, True, False, True, False, False, True],
            "gene_subset": [False, True, False, True, False, True, True, False],
        },
        index=[f"gene-{i}" for i in range(8)],
    )
    if storage == "adata":
        result = AnnData(np.zeros((2, len(frame))), var=frame)
        result.uns["hvg"] = {"flavor": flavor}
        return result
    return frame.to_records(index=False) if storage == "records" else frame


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
