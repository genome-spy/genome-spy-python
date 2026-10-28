"""Count percentages and box summaries for highest-expression QC."""

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy import sparse
import scanpy as sc

from genome_spy.integrations.scanpy._data import require_resident_expression
from genome_spy.integrations.scanpy._embedding.data import point_ids


def prepare_highest_expression(
    adata: AnnData, n_top: int, layer: str | None, gene_symbols: str | None
) -> tuple[pd.DataFrame, pd.DataFrame, tuple[float, float, float]]:
    """Return ranked boxes, outliers and limits from counts without changing AnnData."""
    context = "gsc.pl.highest_expr_genes"
    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: adata must be AnnData.")
    matrix = require_resident_expression(adata, False, layer, context=context)
    if not all(matrix.shape):
        raise ValueError(f"{context}: counts need at least one cell and gene.")
    if sparse.issparse(matrix):
        matrix = matrix.tocsr()
    values = matrix.data if sparse.issparse(matrix) else matrix
    if (
        values.dtype.kind not in "iuf"
        or not np.isfinite(values).all()
        or (values < 0).any()
    ):
        raise ValueError(f"{context}: counts must be finite nonnegative real numbers.")
    labels = adata.var_names
    if gene_symbols is not None:
        if gene_symbols not in adata.var:
            raise ValueError(
                f"{context}: gene_symbols {gene_symbols!r} is missing from var."
            )
        labels = adata.var[gene_symbols].astype("string")

    # Scanpy materializes views even with inplace=False; a metadata-free shell avoids that.
    percentages = sc.pp.normalize_total(
        AnnData(X=matrix), target_sum=100, inplace=False
    )["X"]
    means = np.asarray(percentages.mean(axis=0)).ravel()
    indices = np.argsort(means)[::-1][:n_top]
    labels = pd.Index(labels).take(indices)
    if labels.hasnans or not labels.is_unique:
        raise NotImplementedError(
            f"{context}: selected gene labels must be nonmissing and unique."
        )
    ids = point_ids(adata.obs_names)["_obs_id"].to_numpy()
    boxes, outliers = [], []
    low, high, positive = 100.0, 0.0, 100.0
    for index, label in zip(indices, labels, strict=True):
        column = percentages[:, index]
        column = (
            column.toarray().ravel()
            if sparse.issparse(column)
            else np.asarray(column).ravel()
        )
        if not np.isfinite(column).all():
            raise ValueError(
                f"{context}: normalization produced nonfinite percentages."
            )
        q1, median, q3 = np.percentile(column, [25, 50, 75])
        spread = 1.5 * (q3 - q1)
        lower = min(q1, column[column >= q1 - spread].min())
        upper = max(q3, column[column <= q3 + spread].max())
        boxes.append(
            {
                "gene": str(label),
                "gene_id": str(adata.var_names[index]),
                "mean": means[index],
                "q1": q1,
                "median": median,
                "q3": q3,
                "lower": lower,
                "upper": upper,
            }
        )
        flier = (column < lower) | (column > upper)
        for cell in np.flatnonzero(flier):
            outliers.append(
                {
                    "gene": str(label),
                    "cell_id": ids[cell],
                    "cell": str(adata.obs_names[cell]),
                    "percent": column[cell],
                }
            )
        low, high = min(low, column.min()), max(high, column.max())
        # Log limits depend on drawn coordinates, not hidden observations inside whiskers.
        drawn = np.concatenate(([q1, median, q3, lower, upper], column[flier]))
        if (drawn > 0).any():
            positive = min(positive, drawn[drawn > 0].min())
    return (
        pd.DataFrame(boxes),
        pd.DataFrame(outliers),
        (float(low), float(high), float(positive)),
    )
