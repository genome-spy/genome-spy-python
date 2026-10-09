"""Optional AnnData projections into the existing pandas table interface."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from anndata import AnnData
    from pandas import DataFrame

__all__ = ["AnnDataProjectionError", "from_anndata"]


class AnnDataProjectionError(ValueError):
    """A requested AnnData field cannot be projected without ambiguity.

    Description:
        Reports missing fields, invalid components, and output name collisions.

    Args:
        *args: Context describing the invalid projection.

    Returns:
        An exception describing the projection failure.

    Raises:
        No exceptions are raised directly here.

    Example:
        >>> raise AnnDataProjectionError("Gene 'MS4A1' is missing.")
    """


def _as_dataframe(data: Any) -> Any:
    """Use AnnData observation metadata without importing optional packages."""
    module = sys.modules.get("anndata")
    if module is not None and isinstance(data, getattr(module, "AnnData", ())):
        # AnnData views expose a pandas subclass; copy only the table container
        # so existing pandas recognition works without reading any matrix.
        return cast(Any, data).obs.copy(deep=False)
    return data


def from_anndata(
    adata: AnnData,
    *,
    obs: Sequence[str] | None = None,
    genes: Sequence[str] = (),
    obsm_keys: Sequence[tuple[str, int]] = (),
) -> DataFrame:
    """Prepare observation metadata, selected genes, and embedding components.

    Description:
        Returns a pandas snapshot with one row per observation in source order.
        Gene fields use exact ``var_names`` and read ``X``; embedding fields use
        Scanpy's ``<key>-<component>`` naming. Only selected expression columns
        are densified. No analysis, file loading, or AnnData mutation occurs.
        The index contains observation names; charts omit it unless explicitly
        exported with pandas ``reset_index()``.

    Args:
        adata: Source AnnData object or view.
        obs: Observation columns to include. ``None`` includes all; ``[]``
            includes none.
        genes: Exact variable names to extract from ``X``.
        obsm_keys: Embedding keys and zero-based integer component indices.

    Returns:
        A pandas table accepted by ``Chart``, Arrow export, and widget updates.

    Raises:
        ImportError: If AnnData is unavailable; install the ``anndata`` extra.
        TypeError: If the source is not AnnData or selected arrays are neither
            NumPy arrays, SciPy sparse arrays/matrices, nor pandas embeddings.
        AnnDataProjectionError: If fields are absent or ambiguous, components
            are invalid, or requested output names collide.

    Example:
        >>> import genome_spy as gs
        >>> from genome_spy.anndata import from_anndata
        >>> cells = from_anndata(
        ...     adata, obs=["cell_type"], genes=["MS4A1"],
        ...     obsm_keys=[("X_umap", 0), ("X_umap", 1)],
        ... )
        >>> chart = gs.Chart(cells).mark_point().encode(
        ...     x="X_umap-0", y="X_umap-1", color="MS4A1"
        ... )
    """
    try:
        from anndata import AnnData
    except ImportError as error:
        raise ImportError(
            "AnnData projection requires genome-spy-python[anndata]."
        ) from error

    import numpy as np
    import pandas as pd
    from scipy.sparse import issparse

    if not isinstance(adata, AnnData):
        raise TypeError(f"Expected AnnData, got {type(adata).__name__}.")
    if isinstance(obs, str) or isinstance(genes, str):
        raise AnnDataProjectionError("Pass obs and genes as sequences, not strings.")

    columns = list(adata.obs.columns if obs is None else obs)
    names = columns + list(genes) + [f"{key}-{index}" for key, index in obsm_keys]
    if len(names) != len(set(names)):
        raise AnnDataProjectionError(f"Requested output names collide: {names!r}.")
    for column in columns:
        if list(adata.obs.columns).count(column) != 1:
            raise AnnDataProjectionError(
                f"Observation column {column!r} is missing or ambiguous."
            )
    table = adata.obs.loc[:, columns].copy()

    if genes:
        positions = []
        for gene in genes:
            matches = np.flatnonzero(adata.var_names == gene)
            if len(matches) != 1:
                raise AnnDataProjectionError(f"Gene {gene!r} is missing or ambiguous.")
            positions.append(int(matches[0]))
        if not isinstance(adata.X, np.ndarray) and not issparse(adata.X):
            raise TypeError("Selected X values require a NumPy or SciPy sparse matrix.")
        expression = adata[:, positions].to_df()
        for gene in genes:
            table[gene] = expression[gene].to_numpy()

    for key, index in obsm_keys:
        if key not in adata.obsm:
            raise AnnDataProjectionError(f"Embedding {key!r} is missing from obsm.")
        embedding = adata.obsm[key]
        if (
            isinstance(index, bool)
            or not isinstance(index, int)
            or index < 0
            or len(embedding.shape) != 2
            or index >= embedding.shape[1]
        ):
            raise AnnDataProjectionError(
                f"Invalid component {index!r} for embedding {key!r} "
                f"with shape {embedding.shape!r}."
            )
        if isinstance(embedding, pd.DataFrame):
            values = embedding.iloc[:, index].to_numpy()
        elif isinstance(embedding, np.ndarray):
            values = np.asarray(embedding[:, index])
        elif issparse(embedding):
            values = embedding[:, [index]].toarray().ravel()
        else:
            raise TypeError(
                f"Embedding {key!r} requires a NumPy, SciPy, or pandas array."
            )
        # Positional assignment avoids pandas index alignment and AnnData's
        # ArrayView subclass semantics, including duplicate observation names.
        table[f"{key}-{index}"] = values
    return table
