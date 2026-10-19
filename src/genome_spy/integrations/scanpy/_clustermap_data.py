"""Bounded expression access and SciPy row/column trees for clustermap."""

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy import sparse

from genome_spy.integrations.scanpy._data import (
    numeric_values,
    require_resident_expression,
    resolve_use_raw,
)
from genome_spy.integrations.scanpy._dendrogram_data import TreeData
from genome_spy.integrations.scanpy._style import _categorical, _palette, native_color

CONTEXT = "gsc.pl.clustermap"
MAX_VALUES = 250_000
MAX_DISTANCES = 1_000_000


@dataclass(frozen=True, slots=True)
class ClusteredMatrix:
    """Detached values and aligned annotations in clustered row/column order."""

    values: pd.DataFrame
    mask: np.ndarray
    row_order: tuple[int, ...]
    col_order: tuple[int, ...]
    row_tree: TreeData | None
    col_tree: TreeData | None
    row_colors: pd.DataFrame
    col_colors: pd.DataFrame


def _tree(values: np.ndarray, linkage: Any, *, method: str, metric: str) -> TreeData:
    """Return ordered branches from supplied linkage or SciPy's public computation.

    Validate supplied leaves instead of recomputing a caller's tree.
    """
    if linkage is None:
        linkage = hierarchy.linkage(values, method=method, metric=metric)
    else:
        linkage = np.array(linkage, dtype=float, copy=True)
        hierarchy.is_valid_linkage(linkage, throw=True, name="supplied linkage")
        if (
            hierarchy.num_obs_linkage(linkage) != len(values)
            or not np.isfinite(linkage).all()
        ):
            raise ValueError(
                f"{CONTEXT}: supplied linkage must match the axis length and be finite."
            )
    info = hierarchy.dendrogram(linkage, no_plot=True, color_threshold=-np.inf)
    return TreeData(
        tuple(info["leaves"]), np.asarray(info["icoord"]), np.asarray(info["dcoord"])
    )


def _annotation_colors(colors: Any, index: pd.Index, name: str) -> pd.DataFrame:
    """Return CSS color tracks aligned to original labels or positional input.

    Match pandas inputs by index; missing annotations are white, as in Seaborn.
    """
    if colors is None:
        return pd.DataFrame(index=index)
    if isinstance(colors, (pd.DataFrame, pd.Series)):
        if not colors.index.equals(index):
            if not colors.index.is_unique:
                raise ValueError(
                    f"{CONTEXT}: {name} has ambiguous duplicate index labels."
                )
            colors = colors.reindex(index)
        frame = (
            colors.to_frame(name="" if colors.name is None else colors.name)
            if isinstance(colors, pd.Series)
            else colors.copy()
        )
    else:
        array = np.asarray(colors, dtype=object)
        if array.ndim == 1:
            array = array[np.newaxis, :]
        if array.ndim != 2 or array.shape[1] != len(index):
            raise ValueError(
                f"{CONTEXT}: {name} needs one CSS color per item in each track."
            )
        frame = pd.DataFrame(array.T, index=index, columns=[""] * len(array))
    frame = frame.astype(object).fillna("white")
    return frame.map(lambda color: native_color(color, name, context=CONTEXT))


def prepare_clustermap(
    adata: Any,
    obs_keys: str | None,
    use_raw: bool | None,
    *,
    method: str = "average",
    metric: str = "euclidean",
    z_score: int | None = None,
    standard_scale: int | None = None,
    row_cluster: bool = True,
    col_cluster: bool = True,
    row_linkage: Any = None,
    col_linkage: Any = None,
    row_colors: Any = None,
    col_colors: Any = None,
    mask: Any = None,
) -> ClusteredMatrix:
    """Return detached, ordered values, masks, color tracks and two optional trees.

    Scale before clustering; masks only hide values and never change distances.
    """
    from anndata import AnnData

    # Check flags before reading expression or computing distances.
    if not isinstance(adata, AnnData):
        raise TypeError(f"{CONTEXT}: expected AnnData.")
    if obs_keys is not None and not isinstance(obs_keys, str):
        raise TypeError(
            f"{CONTEXT}: obs_keys supports one categorical observation key."
        )
    if not isinstance(method, str) or not isinstance(metric, str):
        raise TypeError(f"{CONTEXT}: method and metric must be SciPy names.")
    for name, enabled in (("row_cluster", row_cluster), ("col_cluster", col_cluster)):
        if not isinstance(enabled, bool):
            raise TypeError(f"{CONTEXT}: {name} must be boolean.")
    for name, value in (("z_score", z_score), ("standard_scale", standard_scale)):
        if value is not None and (isinstance(value, bool) or value not in (0, 1)):
            raise ValueError(
                f"{CONTEXT}: {name} must be None, 0 (rows), or 1 (columns)."
            )
    if z_score is not None and standard_scale is not None:
        raise ValueError(f"{CONTEXT}: z_score and standard_scale cannot be combined.")
    raw = resolve_use_raw(adata, use_raw, None, context=CONTEXT)
    shape = (adata.n_obs, adata.raw.n_vars if raw else adata.n_vars)
    # Bound both tile transport and quadratic clustering before reading expression.
    if not all(shape) or shape[0] * shape[1] > MAX_VALUES:
        raise ValueError(
            f"{CONTEXT}: preview supports 1–{MAX_VALUES:,} values; subset AnnData explicitly."
        )
    if shape[1] != adata.n_vars:
        raise ValueError(
            f"{CONTEXT}: raw and X must have the same number of variables, as required by Scanpy's clustermap; use_raw=False or prepare matching data."
        )
    for count, enabled, linkage in (
        (shape[0], row_cluster, row_linkage),
        (shape[1], col_cluster, col_linkage),
    ):
        if enabled and linkage is None and count * (count - 1) // 2 > MAX_DISTANCES:
            raise ValueError(
                f"{CONTEXT}: automatic clustering exceeds {MAX_DISTANCES:,} pairwise distances; subset explicitly or supply linkage."
            )
    matrix = require_resident_expression(adata, raw, None, context=CONTEXT)
    # Clustermap requests the whole supplied matrix; only that bounded subset densifies.
    values = pd.DataFrame(
        matrix.toarray() if sparse.issparse(matrix) else matrix,
        index=adata.obs_names,
        columns=adata.var_names,
    ).copy()
    numeric_values(values, context=CONTEXT)
    # Scale the detached table before either tree is computed.
    if z_score is not None or standard_scale is not None:
        axis = z_score if z_score is not None else standard_scale
        frame = values if axis == 1 else values.T
        if z_score is not None:
            frame = (frame - frame.mean()) / frame.std()
        else:
            frame = (frame - frame.min()) / (frame.max() - frame.min())
        values = frame if axis == 1 else frame.T

    # Display masks never change the values used for linkage.
    if isinstance(mask, pd.DataFrame) and (
        not mask.index.equals(values.index) or not mask.columns.equals(values.columns)
    ):
        raise ValueError(f"{CONTEXT}: mask labels must match the input matrix.")
    hidden = np.zeros(shape, dtype=bool) if mask is None else np.asarray(mask)
    if hidden.shape != shape or hidden.dtype.kind != "b":
        raise ValueError(
            f"{CONTEXT}: mask must be a boolean array matching the matrix."
        )
    hidden = hidden | values.isna().to_numpy()

    # Resolve colors against original labels, then apply the same tree permutation.
    if obs_keys is not None:
        if row_colors is not None:
            raise TypeError(f"{CONTEXT}: obs_keys and row_colors cannot be combined.")
        if obs_keys not in adata.obs:
            raise ValueError(f"{CONTEXT}: obs_keys {obs_keys!r} is missing.")
        categories = _categorical(adata.obs[obs_keys], context=CONTEXT)
        if categories is None:
            raise TypeError(f"{CONTEXT}: obs_keys must name categorical metadata.")
        palette, _ = _palette(
            adata, obs_keys, categories.categories, None, context=CONTEXT
        )
        row_colors = pd.Series(
            ["white" if code < 0 else palette[code] for code in categories.codes],
            index=adata.obs_names,
            name=obs_keys,
        )
    rows = _annotation_colors(row_colors, values.index, "row_colors")
    columns = _annotation_colors(col_colors, values.columns, "col_colors")
    # Linkage sees scaled values, including cells hidden by a display mask.
    try:
        row_tree = (
            _tree(values.to_numpy(), row_linkage, method=method, metric=metric)
            if row_cluster
            else None
        )
        col_tree = (
            _tree(values.to_numpy().T, col_linkage, method=method, metric=metric)
            if col_cluster
            else None
        )
    except ValueError as error:
        raise ValueError(
            f"{CONTEXT}: cannot cluster the supplied values/linkage: {error}"
        ) from error
    row_order = row_tree.order if row_tree else tuple(range(shape[0]))
    col_order = col_tree.order if col_tree else tuple(range(shape[1]))
    return ClusteredMatrix(
        values.iloc[list(row_order), list(col_order)].copy(),
        hidden[np.ix_(row_order, col_order)],
        row_order,
        col_order,
        row_tree,
        col_tree,
        rows.iloc[list(row_order)],
        columns.iloc[list(col_order)],
    )
