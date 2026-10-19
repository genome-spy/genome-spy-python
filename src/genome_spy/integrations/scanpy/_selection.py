"""Pure observation membership for native UMAP interval selections."""

from __future__ import annotations

from collections.abc import Mapping
from math import isfinite
from numbers import Integral, Real
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import numpy as np
    from anndata import AnnData
    from numpy.typing import NDArray


def selection_mask(
    adata: AnnData,
    snapshot: Mapping[str, Any] | None,
    *,
    dimensions: tuple[int, int] = (0, 1),
    basis: str = "umap",
) -> NDArray[np.bool_]:
    """Match an embedding brush to observations in their current row order.

    Description:
        Uses the same direct-name/``X_`` precedence as ``pl.embedding`` and tests
        lower-inclusive, upper-exclusive domain bounds. No active rectangle
        selects zero observations. Only embedding coordinates are read; no
        expression data is loaded and AnnData is not modified. Keep the plotted
        coordinates unchanged until retrieving IDs. Row reordering and slicing
        preserve membership when those coordinates are retained.

    Args:
        adata: AnnData containing the coordinates used for the plotted UMAP.
        snapshot: Interval value from ``widget.parameter_values``, or None
            before the widget has synchronized.
        dimensions: Zero-based component pair used in the plotted panels.
        basis: Embedding name used by the plotted panels; defaults to UMAP.

    Returns:
        Boolean mask suitable for ``adata[mask]``. Coincident observations
        remain distinct rows.

    Raises:
        TypeError: If adata or the snapshot has an invalid type.
        ValueError: If coordinates, dimensions, or interval bounds are invalid.

    Example:
        >>> mask = gsc.selection_mask(adata, view.parameter_values.get("cells"))
        >>> selected = adata[mask].copy()
    """
    import numpy as np
    from genome_spy.integrations.scanpy._embedding_data import embedding_key

    key = embedding_key(adata, basis, context="selection_mask")
    embedding = adata.obsm[key]
    if len(dimensions) != 2 or any(
        isinstance(d, bool)
        or not isinstance(d, Integral)
        or not 0 <= d < embedding.shape[1]
        for d in dimensions
    ):
        raise ValueError("selection_mask: expected a valid component pair.")
    if hasattr(embedding, "to_numpy"):
        embedding = embedding.to_numpy()
    coordinates = np.asarray(embedding[:, list(dimensions)])
    if not np.isfinite(coordinates).all():
        raise ValueError("selection_mask: coordinates must be finite.")
    # No brush, or a brush missing either axis, means no selected cells.
    mask: NDArray[np.bool_] = np.zeros(adata.n_obs, dtype=bool)
    if snapshot is None:
        return mask
    if not isinstance(snapshot, Mapping):
        raise TypeError("selection_mask: expected an interval snapshot or None.")
    intervals = snapshot.get("intervals")
    if snapshot.get("type", "interval") != "interval" or not isinstance(
        intervals, Mapping
    ):
        raise ValueError("selection_mask: expected an x/y interval selection.")
    bounds = [intervals.get(channel) for channel in ("x", "y")]
    if any(bound is None for bound in bounds):
        return mask
    ranges: list[tuple[float, float]] = []
    for bound in bounds:
        if (
            not isinstance(bound, (list, tuple))
            or len(bound) != 2
            or any(
                isinstance(v, bool) or not isinstance(v, Real) or not isfinite(v)
                for v in bound
            )
            or bound[0] > bound[1]
        ):
            raise ValueError(
                "selection_mask: bounds must be ordered finite number pairs."
            )
        ranges.append((float(bound[0]), float(bound[1])))
    # Match the chart: include the lower edge and exclude the upper edge.
    x, y = coordinates.T
    mask = (
        (x >= ranges[0][0])
        & (x < ranges[0][1])
        & (y >= ranges[1][0])
        & (y < ranges[1][1])
    )
    return mask
