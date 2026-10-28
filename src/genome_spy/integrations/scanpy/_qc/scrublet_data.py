"""Fixed-bin probability densities from stored Scrublet results."""

from collections.abc import Mapping

from anndata import AnnData
import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import number, numeric_values

CONTEXT = "gsc.pl.scrublet_score_distribution"


def prepare_scrublet(adata: AnnData) -> tuple[pd.DataFrame, list[float | None]]:
    """Return observed/simulated bin rows and thresholds in Scanpy's batch order."""
    if not isinstance(adata, AnnData):
        raise TypeError(f"{CONTEXT}: adata must be AnnData.")
    if not adata.obs.columns.is_unique:
        raise ValueError(f"{CONTEXT}: obs column names must be unique.")
    stored = adata.uns.get("scrublet")
    if not isinstance(stored, Mapping):
        raise ValueError(
            f"{CONTEXT}: stored scrublet results are required; run sc.pp.scrublet explicitly first."
        )
    if "doublet_score" not in adata.obs:
        raise ValueError(f"{CONTEXT}: obs['doublet_score'] is missing.")
    groups = [(None, adata.obs)]
    if "batched_by" in stored:
        key = stored["batched_by"]
        if not isinstance(key, str) or key not in adata.obs:
            raise ValueError(f"{CONTEXT}: stored batched_by must name an obs column.")
        batches = adata.obs[key].astype("category")
        if len(batches.cat.categories) != batches.nunique():
            raise NotImplementedError(
                f"{CONTEXT}: unused batch categories are unsupported; remove them explicitly."
            )
        groups = list(adata.obs.groupby(batches, observed=True))
    if not groups or not adata.n_obs:
        raise ValueError(f"{CONTEXT}: no observed cells/batches are available.")
    tables: list[pd.DataFrame] = []
    thresholds: list[float | None] = []
    for batch, observed in groups:
        result = stored
        if batch is not None:
            results = stored.get("batches", {})
            if not isinstance(results, Mapping) or batch not in results:
                raise ValueError(
                    f"{CONTEXT}: stored results for batch {batch!r} are missing."
                )
            result = results[batch]
        if not isinstance(result, Mapping) or "doublet_scores_sim" not in result:
            raise ValueError(
                f"{CONTEXT}: doublet_scores_sim is missing for batch {batch!r}."
            )
        threshold = result.get("threshold")
        if threshold is not None:
            threshold = number(
                threshold, "threshold", context=CONTEXT, minimum=-float("inf")
            )
        suffix = "" if batch is None else f" ({batch})"
        for sample, scores in (
            ("Observed transcriptomes", observed["doublet_score"]),
            ("Simulated doublets", result["doublet_scores_sim"]),
        ):
            bins = _score_bins(scores)
            bins["panel"] = len(tables)
            bins["batch"] = "All cells" if batch is None else str(batch)
            bins["sample"] = sample
            bins["title"] = f"{sample} {suffix}"
            tables.append(bins)
            thresholds.append(threshold)
    return pd.concat(tables, ignore_index=True), thresholds


def _score_bins(scores: object) -> pd.DataFrame:
    """Return 49 counts and densities from a stored score vector, keeping Scanpy's edges."""
    if (
        not isinstance(scores, (np.ndarray, pd.Series, list, tuple))
        or np.ndim(scores) != 1
    ):
        raise TypeError(
            f"{CONTEXT}: scores must be a resident one-dimensional numeric vector."
        )
    values = numeric_values(pd.DataFrame({"score": scores}), context=CONTEXT).ravel()
    counts, edges = np.histogram(values, bins=np.linspace(0, 1, 50))
    if not counts.sum():
        raise ValueError(
            f"{CONTEXT}: each score vector needs at least one score in [0, 1]."
        )
    return pd.DataFrame(
        {
            "start": edges[:-1],
            "end": edges[1:],
            "count": counts,
            "density": counts / np.diff(edges) / counts.sum(),
        }
    )
