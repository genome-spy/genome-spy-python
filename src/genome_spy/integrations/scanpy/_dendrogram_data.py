"""Python group profiles, linkage, cache validation and shared plot permutations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any
import warnings

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

from genome_spy.integrations.scanpy._data import require_resident_expression
from genome_spy.integrations.scanpy._grouped_data import (
    FeatureGroup,
    _categories,
    group_means,
)


@dataclass(frozen=True, slots=True)
class DendrogramData:
    categories: tuple[Any, ...]
    order: tuple[Any, ...]
    linkage: np.ndarray
    correlation: np.ndarray
    icoord: np.ndarray
    dcoord: np.ndarray


def _grouping(
    adata: Any, groupby: str | Sequence[str]
) -> tuple[list[str], pd.Categorical]:
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError("Dendrogram: expected AnnData.")
    keys = [groupby] if isinstance(groupby, str) else list(groupby)
    if (
        not keys
        or len(set(keys)) != len(keys)
        or any(not isinstance(key, str) for key in keys)
    ):
        raise ValueError("Dendrogram: groupby needs distinct observation keys.")
    for key in keys:
        if key not in adata.obs or not isinstance(
            adata.obs[key].dtype, pd.CategoricalDtype
        ):
            raise ValueError(
                f"Dendrogram: {key!r} must be a categorical observation; prepare it explicitly in Scanpy."
            )
    groups = _categories(adata.obs, keys)
    if len(keys) > 1:
        # Scanpy's tree computation sorts joined categories lexically.
        groups = groups.reorder_categories(sorted(groups.categories))
    if len(groups.categories) < 2:
        raise ValueError("Dendrogram: at least two observed categories are required.")
    if len(set(map(str, groups.categories))) != len(groups.categories):
        raise ValueError(
            "Dendrogram: category labels collide when serialized as strings."
        )
    if len(np.unique(groups.codes[groups.codes >= 0])) != len(groups.categories):
        raise ValueError(
            "Dendrogram: unused categories have no profiles; remove them explicitly."
        )
    return keys, groups


def _profiles(adata: Any, groups: pd.Categorical, use_rep: str | None) -> pd.DataFrame:
    from scanpy import settings

    if use_rep is None:
        use_rep = "X" if adata.n_vars <= settings.N_PCS else "X_pca"
    if use_rep == "X":
        matrix = require_resident_expression(adata, False, None, context="Dendrogram")
    elif isinstance(use_rep, str) and use_rep in adata.obsm:
        matrix = adata.obsm[use_rep]
    else:
        raise ValueError(
            f"Dendrogram: missing representation {use_rep!r}; run sc.pp.pca(adata) or sc.tl.dendrogram(adata, ..., use_rep='existing_key') explicitly. Plotting never fits PCA."
        )
    if isinstance(matrix, pd.DataFrame):
        matrix = matrix.to_numpy(copy=False)
    if not isinstance(matrix, np.ndarray) and not sparse.issparse(matrix):
        raise TypeError(
            "Dendrogram: representation must be resident NumPy or SciPy data."
        )
    if len(matrix.shape) != 2 or matrix.shape[0] != adata.n_obs or matrix.shape[1] < 2:
        raise ValueError(
            "Dendrogram: representation needs observations by at least two components/features."
        )
    values = matrix.data if sparse.issparse(matrix) else matrix
    if values.dtype.kind not in "fiu" or np.isinf(values).any():
        raise ValueError(
            "Dendrogram: representation values must be real, finite or missing."
        )
    index = pd.CategoricalIndex(groups)
    if not sparse.issparse(matrix):
        return group_means(pd.DataFrame(matrix, index=index)).loc[groups.categories]
    # Aggregate sparse columns before densifying only the group-by-feature result.
    valid = groups.codes >= 0
    membership = sparse.csr_matrix(
        (np.ones(valid.sum()), (groups.codes[valid], np.flatnonzero(valid))),
        shape=(len(groups.categories), adata.n_obs),
    )
    counts = np.bincount(groups.codes[valid], minlength=len(groups.categories))[:, None]
    matrix = sparse.csr_matrix(matrix, copy=True)
    matrix.sum_duplicates()
    missing = np.isnan(matrix.data)
    denominator = np.broadcast_to(counts, (len(counts), matrix.shape[1]))
    if missing.any():
        absent = matrix.copy()
        absent.data = missing.astype(float)
        denominator = denominator - (membership @ absent).toarray()
        matrix.data[missing] = 0
    totals = (membership @ matrix).toarray()
    means = np.divide(
        totals, denominator, out=np.full_like(totals, np.nan), where=denominator > 0
    )
    return pd.DataFrame(means, index=groups.categories)


def _correlation(profiles: pd.DataFrame, method: str) -> np.ndarray:
    if method not in ("pearson", "spearman", "kendall"):
        raise ValueError("Dendrogram: unsupported cached correlation method.")
    correlation = profiles.T.corr(method=method).clip(-1, 1).to_numpy()
    if not np.isfinite(correlation).all():
        raise ValueError(
            "Dendrogram: missing or constant group profiles have undefined correlations; prepare a suitable representation explicitly."
        )
    return np.array(correlation, dtype=float)


def prepare_dendrogram(
    adata: Any, groupby: str | Sequence[str], key: str | None = None
) -> DendrogramData:
    """Return a verified stored tree or compute a local tree without AnnData writes."""
    keys, groups = _grouping(adata, groupby)
    if key is not None and (not isinstance(key, str) or not key):
        raise TypeError("Dendrogram: dendrogram_key must be a nonempty string or None.")
    key = key or f"dendrogram_{'_'.join(keys)}"
    cached = adata.uns.get(key)
    if key not in adata.uns:
        categories = tuple(groups.categories)
        correlation = _correlation(_profiles(adata, groups, None), "pearson")
        linkage = hierarchy.linkage(squareform(1 - correlation), method="complete")
        info = hierarchy.dendrogram(
            linkage, labels=list(map(str, categories)), no_plot=True
        )
        order = tuple(categories[i] for i in info["leaves"])
    else:
        message = f"Dendrogram: cache {key!r} is malformed, stale or cannot be verified; recompute sc.tl.dendrogram explicitly with the current grouping and all components of use_rep."
        try:
            if not isinstance(cached, Mapping) or list(cached["groupby"]) != keys:
                raise ValueError(message)
            labels = list(cached["categories_ordered"])
            indices = np.asarray(cached["categories_idx_ordered"])
            n = len(groups.categories)
            if indices.dtype.kind not in "iu" or sorted(indices.tolist()) != list(
                range(n)
            ):
                raise ValueError(message)
            current = {str(value): value for value in groups.categories}
            if len(labels) != n or len(set(labels)) != n or set(labels) != set(current):
                raise ValueError(message)
            categories_list = [None] * n
            for i, label in zip(indices, labels, strict=True):
                categories_list[i] = current[label]
            categories = tuple(categories_list)
            order = tuple(current[label] for label in labels)
            linkage = np.array(cached["linkage"], dtype=float, copy=True)
            if (
                linkage.shape != (n - 1, 4)
                or not hierarchy.is_valid_linkage(linkage)
                or not np.isfinite(linkage).all()
            ):
                raise ValueError(message)
            info = cached["dendrogram_info"]
            expected = hierarchy.dendrogram(
                linkage, labels=list(map(str, categories)), no_plot=True
            )
            if (
                list(info["ivl"]) != labels
                or list(info["leaves"]) != indices.tolist()
                or expected["leaves"] != indices.tolist()
            ):
                raise ValueError(message)
            for name in ("icoord", "dcoord"):
                coords = np.asarray(info[name], dtype=float)
                if (
                    coords.shape != (n - 1, 4)
                    or not np.isfinite(coords).all()
                    or not np.allclose(coords, expected[name], rtol=1e-10, atol=1e-12)
                ):
                    raise ValueError(message)
            profiles = _profiles(adata, groups, cached["use_rep"]).loc[list(categories)]
            correlation = np.array(cached["correlation_matrix"], dtype=float, copy=True)
            actual = _correlation(profiles, cached["cor_method"])
            if correlation.shape != (n, n) or not np.allclose(
                correlation, actual, rtol=1e-7, atol=1e-8
            ):
                raise ValueError(message)
            if cached["linkage_method"] not in (
                "single",
                "complete",
                "average",
                "weighted",
                "centroid",
                "median",
                "ward",
            ):
                raise ValueError(message)
        except (KeyError, TypeError, ValueError, IndexError) as error:
            raise ValueError(message) from error
    # Correlation labels follow current categories even if a valid cache predates reordering.
    positions = [categories.index(value) for value in groups.categories]
    return DendrogramData(
        tuple(groups.categories),
        order,
        linkage,
        correlation[np.ix_(positions, positions)],
        np.array(info["icoord"], dtype=float, copy=True),
        np.array(info["dcoord"], dtype=float, copy=True),
    )


def attached_dendrogram(
    adata: Any, groupby: str | Sequence[str], option: bool | str, count: int
) -> DendrogramData | None:
    if option is False:
        return None
    if not (option is True or isinstance(option, str) and option):
        raise TypeError(
            "Grouped plotting: dendrogram must be False, True, or a nonempty cache key."
        )
    if count <= 2:
        warnings.warn(
            "Dendrogram not added: Scanpy attaches trees only for more than two categories.",
            UserWarning,
            stacklevel=3,
        )
        return None
    return prepare_dendrogram(
        adata, groupby, option if isinstance(option, str) else None
    )


def reorder_grouped(
    tree: DendrogramData,
    colors: pd.DataFrame,
    groups: tuple[FeatureGroup, ...],
    *,
    swapped: bool,
) -> tuple[pd.DataFrame, tuple[FeatureGroup, ...], list[int]]:
    """Carry one leaf and optional marker-block permutation through all summaries."""
    table = colors.T if swapped else colors
    table = table.loc[list(tree.order)]
    slots = list(range(table.shape[1]))
    if groups and set(g.label for g in groups) == set(tree.order):
        slots, ordered = [], []
        for category in tree.order:
            group = next(g for g in groups if g.label == category)
            start = len(slots)
            slots.extend(range(group.start, group.end + 1))
            ordered.append(FeatureGroup(group.label, start, len(slots) - 1))
        table = table.iloc[:, slots]
        groups = tuple(ordered)
    return table.T if swapped else table, groups, slots
