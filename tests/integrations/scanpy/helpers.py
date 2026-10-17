"""Chart traversal shared by integration tests and explicit benchmarks."""

from typing import Any


def units(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return leaf views while retaining layers as one plotting panel."""
    for composition in ("concat", "hconcat", "vconcat"):
        if composition in spec:
            return [unit for child in spec[composition] for unit in units(child)]
    return [spec]
