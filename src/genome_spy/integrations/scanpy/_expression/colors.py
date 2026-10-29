"""Native expression scales shared by cell and group heatmaps."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import genome_spy as gs
from genome_spy.integrations.scanpy._style import color_bounds, native_scheme

if TYPE_CHECKING:
    import numpy as np


def expression_scale(
    values: np.ndarray,
    cmap: Any,
    vmin: float | None,
    vmax: float | None,
    *,
    context: str,
) -> gs.Scale:
    """Return a native scheme or zero-centered Seurat magenta–black–yellow scale."""
    low, high, _ = color_bounds(values, vmin, vmax, context=context)
    scale = gs.Scale(type="linear", nice=False, zero=False, clamp=True)
    if isinstance(cmap, str) and cmap.lower() == "seurat":
        extent = max(abs(low), abs(high))
        low = -extent if vmin is None else low
        high = extent if vmax is None else high
        if not low < 0 < high:
            raise ValueError(f"{context}: seurat requires vmin < 0 < vmax.")
        return (
            scale.domain([low, 0, high])
            .range(["#ff00ff", "#000000", "#ffff00"])
            .interpolate("rgb")
        )
    return scale.domain([low, high]).scheme(
        native_scheme("viridis" if cmap is None else cmap, "cmap", context=context)
    )
