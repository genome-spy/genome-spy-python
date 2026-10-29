"""Read Scanpy trees, delegate missing computations and share plot permutations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any
import warnings

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy

from genome_spy.integrations.scanpy._data import require_resident_expression
from genome_spy.integrations.scanpy._expression.grouped_data import (
    FeatureGroup,
    _categories,
)


@dataclass(frozen=True, slots=True)
class TreeData:
    """Ordered branch coordinates shared by group and individual-item trees."""

    order: tuple[Any, ...]
    icoord: np.ndarray
    dcoord: np.ndarray


@dataclass(frozen=True, slots=True)
class DendrogramData(TreeData):
    """Stored Scanpy group tree, including its correlation matrix."""

    categories: tuple[Any, ...]
    linkage: np.ndarray
    correlation: np.ndarray


def _grouping(
    adata: Any, groupby: str | Sequence[str]
) -> tuple[list[str], pd.Categorical]:
    """Check AnnData's grouping columns and return their keys and ordered groups.

    Require categorical columns with distinct labels and at least two observed groups.
    """
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
        # Scanpy sorts combined group labels alphabetically when computing trees.
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


def _compute_dendrogram(adata: Any, keys: list[str]) -> Any:
    """Return a Scanpy tree result for the grouping keys without saving it in AnnData.

    Require existing dense data so plotting cannot fit PCA or make sparse X dense.
    """
    import scanpy as sc

    # Choose an existing representation so Scanpy cannot silently fit PCA.
    use_rep = "X" if adata.n_vars <= sc.settings.N_PCS else "X_pca"
    if use_rep == "X_pca" and use_rep not in adata.obsm:
        raise ValueError(
            "Dendrogram: missing X_pca; run sc.pp.pca or sc.tl.dendrogram explicitly. Plotting never fits PCA."
        )
    if adata.isbacked:
        raise TypeError(
            "Dendrogram: Scanpy cannot compute a tree on backed data; compute sc.tl.dendrogram before backing, then plot the stored result."
        )
    matrix = (
        require_resident_expression(adata, False, None, context="Dendrogram")
        if use_rep == "X"
        else adata.obsm[use_rep]
    )
    if not isinstance(matrix, (np.ndarray, pd.DataFrame)):
        raise TypeError(
            "Dendrogram: automatic Scanpy computation needs a resident dense representation; prepare a tree explicitly with sc.tl.dendrogram and a dense obsm representation. Sparse expression is never densified here."
        )
    try:
        return sc.tl.dendrogram(adata, keys, use_rep=use_rep, inplace=False)
    except (ValueError, TypeError, KeyError) as error:
        raise ValueError(
            "Dendrogram: Scanpy could not compute a tree from these groups/profiles; prepare sc.tl.dendrogram explicitly with a suitable representation."
        ) from error


def prepare_dendrogram(
    adata: Any, groupby: str | Sequence[str], key: str | None = None
) -> DendrogramData:
    """Return copied tree data for AnnData's groups from a stored or new Scanpy result.

    Check its structure and align labels without recomputing stored results or
    changing AnnData.
    """
    keys, groups = _grouping(adata, groupby)
    if key is not None and (not isinstance(key, str) or not key):
        raise TypeError("Dendrogram: dendrogram_key must be a nonempty string or None.")

    # A stored tree is a snapshot; do not recompute it to check whether it is fresh.
    key = key or f"dendrogram_{'_'.join(keys)}"
    result = adata.uns[key] if key in adata.uns else _compute_dendrogram(adata, keys)
    message = f"Dendrogram: cache {key!r} is malformed or incompatible with the groups; recompute sc.tl.dendrogram explicitly."
    try:
        if not isinstance(result, Mapping) or list(result["groupby"]) != keys:
            raise ValueError(message)

        # Match by label so changing category order does not attach the wrong leaves.
        labels = list(map(str, result["categories_ordered"]))
        indices = np.asarray(result["categories_idx_ordered"])
        n = len(groups.categories)
        if indices.dtype.kind not in "iu" or sorted(indices.tolist()) != list(range(n)):
            raise ValueError(message)
        current = {str(value): value for value in groups.categories}
        if len(labels) != n or len(set(labels)) != n or set(labels) != set(current):
            raise ValueError(message)
        categories = [None] * n
        for i, label in zip(indices, labels, strict=True):
            categories[i] = current[label]

        # Check stored arrays without rebuilding the tree or reading expression.
        linkage = np.array(result["linkage"], dtype=float, copy=True)
        if linkage.shape != (n - 1, 4) or not hierarchy.is_valid_linkage(linkage):
            raise ValueError(message)
        info = result["dendrogram_info"]
        if (
            list(map(str, info["ivl"])) != labels
            or list(info["leaves"]) != indices.tolist()
        ):
            raise ValueError(message)
        icoord = np.array(info["icoord"], dtype=float, copy=True)
        dcoord = np.array(info["dcoord"], dtype=float, copy=True)
        correlation = np.array(result["correlation_matrix"], dtype=float, copy=True)
        if (
            icoord.shape != (n - 1, 4)
            or dcoord.shape != (n - 1, 4)
            or correlation.shape != (n, n)
            or not all(
                np.isfinite(a).all() for a in (linkage, icoord, dcoord, correlation)
            )
            or (dcoord < 0).any()
            or not np.allclose(correlation, correlation.T)
            or not np.allclose(np.diag(correlation), 1)
            or (np.abs(correlation) > 1).any()
        ):
            raise ValueError(message)
    except (KeyError, TypeError, ValueError, IndexError) as error:
        raise ValueError(message) from error

    # Correlation rows and columns must follow the current category order.
    positions = [categories.index(value) for value in groups.categories]
    return DendrogramData(
        categories=tuple(groups.categories),
        order=tuple(current[label] for label in labels),
        linkage=linkage,
        correlation=correlation[np.ix_(positions, positions)],
        icoord=icoord,
        dcoord=dcoord,
    )


def attached_dendrogram(
    adata: Any, groupby: str | Sequence[str], option: bool | str, count: int
) -> DendrogramData | None:
    """Return tree data for the requested grouped plot, or None when not attached.

    Interpret the boolean or stored-result key and match Scanpy's small-group rule.
    """
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
    """Reorder a summary table and matching marker brackets to follow a tree.

    Return both plus gene positions so dot sizes can follow the same ordering.
    """

    # Put groups on rows temporarily so both plot orientations use the same order.
    table = colors.T if swapped else colors
    table = table.loc[list(tree.order)]
    groups, slots = reorder_features(tree, groups, table.shape[1])
    table = table.iloc[:, slots]
    return table.T if swapped else table, groups, slots


def reorder_features(
    tree: DendrogramData, groups: tuple[FeatureGroup, ...], count: int
) -> tuple[tuple[FeatureGroup, ...], list[int]]:
    """Return marker brackets and gene positions in matching tree order.

    Share the same feature ordering across summary plots and cell heatmaps.
    """
    slots = list(range(count))

    # Reorder marker blocks only when their labels match the cell groups.
    if groups and set(g.label for g in groups) == set(tree.order):
        slots, ordered = [], []
        for category in tree.order:
            group = next(g for g in groups if g.label == category)
            start = len(slots)
            slots.extend(range(group.start, group.end + 1))
            ordered.append(FeatureGroup(group.label, start, len(slots) - 1))
        groups = tuple(ordered)
    return groups, slots
