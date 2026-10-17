"""Chart traversal shared by integration tests and explicit benchmarks."""

from typing import Any


def units(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return leaf views while retaining layers as one plotting panel."""
    for composition in ("concat", "hconcat", "vconcat"):
        if composition in spec:
            return [unit for child in spec[composition] for unit in units(child)]
    return [spec]


def points(panel: dict[str, Any]) -> dict[str, Any]:
    """Find the point mark that owns the native color scale and guide."""
    return next(
        layer
        for layer in panel.get("layer", [panel])
        if "scale" in layer.get("encoding", {}).get("color", {})
    )
