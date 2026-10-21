"""Original stored gene-selection results for paired QC diagnostics."""

import numpy as np
import pandas as pd
from anndata import AnnData


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
