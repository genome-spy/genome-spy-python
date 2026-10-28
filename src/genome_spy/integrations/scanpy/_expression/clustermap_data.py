"""Detached expression access and SciPy row/column trees for clustermap."""

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
    obs_labels: pd.Series | None
    obs_palette: tuple[str, ...]


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


def _observation_colors(
    adata: Any, key: str | None, supplied: Any
) -> tuple[pd.DataFrame, pd.Series | None, tuple[str, ...]]:
    """Return row colors, category labels and a palette from observation metadata.

    Keep category labels for the native legend; supplied colors need no categories.
    """
    if key is None:
        return _annotation_colors(supplied, adata.obs_names, "row_colors"), None, ()
    if supplied is not None:
        raise TypeError(f"{CONTEXT}: obs_keys and row_colors cannot be combined.")
    if key not in adata.obs:
        raise ValueError(f"{CONTEXT}: obs_keys {key!r} is missing.")
    categories = _categorical(adata.obs[key], context=CONTEXT)
    if categories is None:
        raise TypeError(f"{CONTEXT}: obs_keys must name categorical metadata.")
    palette, _ = _palette(adata, key, categories.categories, None, context=CONTEXT)
    labels = (
        pd.Series(categories, index=adata.obs_names, name=key)
        if len(categories.categories)
        else None
    )
    colors = pd.Series(
        ["white" if code < 0 else palette[code] for code in categories.codes],
        index=adata.obs_names,
        name=key,
    )
    return (
        _annotation_colors(colors, adata.obs_names, "row_colors"),
        labels,
        palette if labels is not None else (),
    )


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

    # Choose the expression source before preparing values and trees.
    raw = resolve_use_raw(adata, use_raw, None, context=CONTEXT)
    shape = (adata.n_obs, adata.raw.n_vars if raw else adata.n_vars)

    if not all(shape):
        raise ValueError(f"{CONTEXT}: at least one cell and one gene are required.")
    if shape[1] != adata.n_vars:
        raise ValueError(
            f"{CONTEXT}: raw and X must have the same number of variables, as required by Scanpy's clustermap; use_raw=False or prepare matching data."
        )
    matrix = require_resident_expression(adata, raw, None, context=CONTEXT)

    # Clustermap requests the whole supplied matrix; only that supplied matrix densifies.
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
            # Constant profiles stay missing here, matching Seaborn.
            minimum = frame.min()
            frame = (frame - minimum) / (frame.max() - minimum)
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
    rows, obs_labels, obs_palette = _observation_colors(adata, obs_keys, row_colors)
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
        obs_labels.iloc[list(row_order)].copy() if obs_labels is not None else None,
        obs_palette,
    )
