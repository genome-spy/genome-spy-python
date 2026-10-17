"""Shared expression-source checks for Scanpy plotting inputs."""

from __future__ import annotations

from typing import Any


def resolve_use_raw(
    adata: Any, requested: bool | None, layer: str | None, *, context: str
) -> bool:
    if requested is not None and not isinstance(requested, bool):
        raise TypeError(f"{context}: use_raw must be True, False, or None.")
    if requested is True and layer is not None:
        raise ValueError(f"{context}: use_raw=True and layer are incompatible.")
    if requested is True and adata.raw is None:
        raise ValueError(f"{context}: use_raw=True requires adata.raw.")
    if requested is None:
        return adata.raw is not None and layer is None
    return requested


def require_resident_expression(
    adata: Any, use_raw: bool, layer: str | None, *, context: str
) -> Any:
    """Return the selected resident matrix without loading backed views."""
    import numpy as np
    from scipy import sparse

    if layer is not None and layer not in adata.layers:
        raise ValueError(f"{context}: layer {layer!r} is missing.")
    # Accessing X on a backed view can load an unnecessarily wide slice.
    if adata.isbacked:
        raise TypeError(
            f"{context}: backed/lazy expression is not supported yet; "
            "load the required expression into memory explicitly."
        )
    if use_raw:
        matrix = adata.raw.X
    elif layer is not None:
        matrix = adata.layers[layer]
    else:
        matrix = adata.X
    if not isinstance(matrix, np.ndarray) and not sparse.issparse(matrix):
        raise TypeError(
            f"{context}: selected expression requires in-memory NumPy or SciPy data; "
            "backed/lazy expression is not supported yet."
        )
    return matrix
