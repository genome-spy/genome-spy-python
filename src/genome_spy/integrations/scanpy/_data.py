"""Shared numeric-table validation and AnnData source checks for plotting."""

from __future__ import annotations

from math import isfinite
from numbers import Real
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


def coordinate_domain(
    values: np.ndarray, margin: float, *, log: bool = False
) -> tuple[float, float]:
    """Return padded coordinate limits; widen constants in linear units or log decades."""
    import numpy as np

    low, high = float(values.min()), float(values.max())
    if log:
        low, high = float(np.log10(low)), float(np.log10(high))
        if low == high:
            low, high = float(np.ceil(low) - 1), float(np.floor(high) + 1)
    elif low == high:
        padding = abs(low) * 0.05 or 0.05
        low, high = low - padding, high + padding
    padding = (high - low) * margin
    low, high = low - padding, high + padding
    return (10**low, 10**high) if log else (low, high)


def number(value: Any, name: str, *, context: str, minimum: float = 0) -> float:
    """Return a finite numeric option at or above minimum, or raise a named error."""
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not isfinite(value)
        or value < minimum
    ):
        raise ValueError(f"{context}: {name} must be a finite number >= {minimum}.")
    return float(value)


def figsize_pixels(
    figsize: tuple[float, float],
    width: float | None,
    height: float | None,
    *,
    context: str,
) -> tuple[float, float]:
    """Return pixels from an inch-based figsize, rejecting width/height overrides."""
    if width is not None or height is not None:
        raise TypeError(f"{context}: figsize cannot be combined with width or height.")
    if len(figsize) != 2:
        raise ValueError(f"{context}: figsize needs width and height in inches.")
    return (
        number(figsize[0], "figsize width", context=context) * 100,
        number(figsize[1], "figsize height", context=context) * 100,
    )


def numeric_values(table: pd.DataFrame, *, context: str) -> np.ndarray:
    """Return a table's numeric values, allowing missing values but not infinity.

    Check without changing the table so callers keep its labels and data types.
    """
    import numpy as np
    import pandas as pd

    if not all(
        pd.api.types.is_numeric_dtype(dtype)
        and not pd.api.types.is_complex_dtype(dtype)
        for dtype in table.dtypes
    ):
        raise TypeError(f"{context}: values must be real numbers.")
    values: np.ndarray = table.to_numpy(dtype=float, na_value=np.nan)
    if np.isinf(values).any():
        raise ValueError(f"{context}: values must be finite or missing.")
    return values


def matrix_array(matrix: Any, *, context: str, allow_vector: bool = False) -> Any:
    """Return resident 2D values, promoting a vector only when requested.

    Reject other sources before reading or densifying them.
    """
    import numpy as np
    import pandas as pd

    if not isinstance(matrix, (np.ndarray, pd.DataFrame, list, tuple)):
        raise TypeError(f"{context}: supply a resident 2D numeric array or table.")
    array = matrix if isinstance(matrix, pd.DataFrame) else np.asanyarray(matrix)
    if allow_vector and array.ndim == 1:
        array = array.reshape(-1, 1)
    if array.ndim != 2 or not all(array.shape):
        raise ValueError(f"{context}: matrix must have two nonempty dimensions.")
    return array


def resolve_use_raw(
    adata: Any, requested: bool | None, layer: str | None, *, context: str
) -> bool:
    """Resolve use_raw from AnnData, the request and layer; return the final choice.

    Match Scanpy's raw default and reject conflicting or unavailable sources.
    """
    if requested is not None and not isinstance(requested, bool):
        raise TypeError(f"{context}: use_raw must be True, False, or None.")
    if requested is True and layer is not None:
        raise ValueError(f"{context}: use_raw=True and layer are incompatible.")
    if requested is True and adata.raw is None:
        raise ValueError(f"{context}: use_raw=True requires adata.raw.")

    # An explicit layer takes priority over the default raw matrix.
    if requested is None:
        return adata.raw is not None and layer is None
    return requested


def require_resident_expression(
    adata: Any, use_raw: bool, layer: str | None, *, context: str
) -> Any:
    """Return AnnData's selected raw, layer or X matrix if it is already in memory.

    Reject disk-backed or lazy data before access can load unrequested genes.
    """
    import numpy as np
    from scipy import sparse

    if layer is not None and layer not in adata.layers:
        raise ValueError(f"{context}: layer {layer!r} is missing.")

    # Reading X from a disk-backed view can load many unrequested genes.
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
