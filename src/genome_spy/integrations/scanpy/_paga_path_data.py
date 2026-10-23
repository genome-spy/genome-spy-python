"""Ordered PAGA path profiles from stored groups and pseudotime, without analysis."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from numbers import Integral
from typing import Any

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import numeric_values
from genome_spy.integrations.scanpy._grouped_data import (
    MAX_HEATMAP_VALUES,
    grouped_expression,
)

CONTEXT = "gsc.pl.paga_path"


@dataclass(frozen=True, slots=True)
class PagaPathData:
    values: pd.DataFrame
    groups: np.ndarray
    annotations: pd.DataFrame
    boundaries: np.ndarray
    node_names: tuple[str, ...]
    group_key: str


def running_average(values: np.ndarray, window: int) -> np.ndarray:
    """Return full-window averages along rows, preserving Scanpy's cumulative missing-value behavior."""
    summed = np.cumsum(values, axis=0, dtype=float)
    summed[window:] -= summed[:-window]
    return summed[window - 1 :] / window


def prepare_paga_path(
    adata: Any,
    nodes: Sequence[str | int],
    keys: Sequence[str],
    *,
    use_raw: bool,
    annotations: Sequence[str],
    n_avg: int,
    groups_key: str | None,
    normalize_to_zero_one: bool,
) -> PagaPathData:
    """Return detached profiles, original group bands and smoothed annotations in supplied path order."""
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError(f"{CONTEXT}: adata must be AnnData.")
    for name, entries in (
        ("nodes", nodes),
        ("keys", keys),
        ("annotations", annotations),
    ):
        if isinstance(entries, str) or not isinstance(
            entries, (Sequence, np.ndarray, pd.Index)
        ):
            raise TypeError(f"{CONTEXT}: {name} must be a sequence.")
    if not len(nodes) or not len(keys) or not all(isinstance(key, str) for key in keys):
        raise ValueError(f"{CONTEXT}: provide nonempty nodes and string keys.")
    if groups_key is None:
        stored = adata.uns.get("paga", {})
        groups_key = stored.get("groups") if isinstance(stored, Mapping) else None
    if not isinstance(groups_key, str) or groups_key not in adata.obs:
        raise ValueError(f"{CONTEXT}: stored PAGA groups or groups_key are required.")
    groups = adata.obs[groups_key]
    if not isinstance(groups.dtype, pd.CategoricalDtype):
        raise TypeError(f"{CONTEXT}: groups_key must be categorical.")
    if "dpt_pseudotime" not in adata.obs:
        raise ValueError(
            f"{CONTEXT}: stored dpt_pseudotime is required; run sc.tl.dpt explicitly."
        )
    pseudotime = numeric_values(adata.obs[["dpt_pseudotime"]], context=CONTEXT).ravel()
    categories = groups.cat.categories
    if all(isinstance(node, str) for node in nodes):
        indices = categories.get_indexer(nodes)
    elif all(
        isinstance(node, Integral) and not isinstance(node, bool) for node in nodes
    ):
        indices = np.asarray(nodes, dtype=int)
    else:
        raise TypeError(
            f"{CONTEXT}: nodes must be all group names or all integer indices."
        )
    if np.any((indices < 0) | (indices >= len(categories))):
        raise ValueError(f"{CONTEXT}: each node must identify an existing group.")

    # Each occurrence of a node retains its cells, ordered only within that group.
    ordered = []
    for index in indices:
        positions = np.flatnonzero(groups.cat.codes.to_numpy() == index)
        if not len(positions):
            raise ValueError(
                f"{CONTEXT}: node {categories[index]!r} contains no cells."
            )
        ordered.append(positions[np.argsort(pseudotime[positions])])
    order = np.concatenate(ordered)
    if (
        isinstance(n_avg, bool)
        or not isinstance(n_avg, Integral)
        or not 1 <= n_avg <= len(order)
    ):
        raise ValueError(
            f"{CONTEXT}: n_avg must be an integer between 1 and the path cell count."
        )
    if len(keys) < 2 or len(order) - n_avg + 1 < 2:
        raise NotImplementedError(
            f"{CONTEXT}: this preview requires at least two keys and two smoothed cells."
        )
    if len(order) * (len(keys) + len(annotations)) > MAX_HEATMAP_VALUES:
        raise ValueError(
            f"{CONTEXT}: at most {MAX_HEATMAP_VALUES:,} path cell–key values are supported; subset explicitly."
        )
    if len(annotations) > 1:
        raise NotImplementedError(
            f"{CONTEXT}: multiple annotation tracks are not supported yet."
        )
    for name in annotations:
        if not isinstance(name, str) or name not in adata.obs:
            raise ValueError(
                f"{CONTEXT}: each annotation must name an observation column."
            )
        if isinstance(adata.obs[name].dtype, pd.CategoricalDtype):
            raise NotImplementedError(
                f"{CONTEXT}: categorical annotation tracks are not supported yet."
            )

    # Shared Scanpy access selects only requested columns, with raw falling back to X.
    table = grouped_expression(
        adata[order], keys, groups_key, use_raw=use_raw and adata.raw is not None
    ).values
    values = numeric_values(table, context=CONTEXT)
    annotation_values = numeric_values(
        adata.obs.loc[:, list(annotations)].iloc[order], context=CONTEXT
    )
    if n_avg > 1:
        values = running_average(values, n_avg)
        annotation_values = running_average(annotation_values, n_avg)
    if normalize_to_zero_one:
        values = values - values.min(axis=0)
        maximum = values.max(axis=0)
        if np.any(maximum == 0):
            raise ValueError(
                f"{CONTEXT}: normalize_to_zero_one requires nonconstant profiles."
            )
        values = values / maximum
    return PagaPathData(
        pd.DataFrame(values, columns=list(keys)),
        groups.cat.codes.to_numpy()[order],
        pd.DataFrame(annotation_values, columns=list(annotations)),
        np.r_[0, np.cumsum([len(part) for part in ordered])],
        tuple(str(categories[index]) for index in indices),
        groups_key,
    )
