"""Chart traversal and reference paths shared by integration tests and generators."""

from pathlib import Path
import re
from typing import Any


def reference_paths(family: str, output: Path | None) -> tuple[Path, Path]:
    """Return image and metadata directories for a reference family.

    Explicit refreshes keep metadata in fixtures and images ignored; test overrides
    put both in a temporary directory without changing tracked reference metadata.
    """
    images = (
        output
        if output is not None
        else Path(__file__).resolve().parents[3] / "tmp" / "scanpy-references" / family
    )
    images.mkdir(parents=True, exist_ok=True)
    metadata = output if output is not None else Path(__file__).with_name("fixtures")
    return images, metadata


def units(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return leaf views while retaining layers as one plotting panel."""
    if "surround" in spec:
        return units(spec["spec"])
    for composition in ("concat", "hconcat", "vconcat"):
        if composition in spec:
            return [unit for child in spec[composition] for unit in units(child)]
    return [spec]


def leaf_marks(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return leaf marks in draw order, including nested value layers."""
    if "surround" in spec:
        sides = [
            track
            for side in spec["surround"].values()
            for track in (side["views"] if isinstance(side, dict) else side)
        ]
        return [mark for child in [spec["spec"], *sides] for mark in leaf_marks(child)]
    if "layer" in spec:
        return [mark for child in spec["layer"] for mark in leaf_marks(child)]
    return [spec]


def points(panel: dict[str, Any]) -> dict[str, Any]:
    """Find the point mark that owns the native color scale and guide."""
    return next(
        layer
        for layer in leaf_marks(panel)
        if "scale" in layer.get("encoding", {}).get("color", {})
    )


def index_position(slot, count, padding, extent, cuts=()):
    """Project an expected slot through fixed four-pixel gaps, independently of Core."""
    step = (extent - 4 * len(cuts)) / (count + 2 * padding)
    return (slot + padding) * step + 4 * sum(cut <= slot for cut in cuts)


def tree_paths(root):
    """Read complete native tree paths, checking that each elbow has two straight legs."""
    paths = []
    for group in root.iter():
        if group.get("stroke") != "#555555":
            continue
        for element in group:
            path = element.get("d", "")
            assert re.fullmatch(r"M[-+\d., eE]+L[-+\d., eE]+L[-+\d., eE]+", path), path
            values = list(
                map(float, re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", path))
            )
            assert len(values) == 6, element.attrib
            points = [values[i : i + 2] for i in range(0, 6, 2)]
            assert all(a[0] == b[0] or a[1] == b[1] for a, b in zip(points, points[1:]))
            paths.append(points)
    return paths


def tree_segments(root):
    """Return the nonzero legs of native tree paths for alignment checks."""
    return [
        [*start, *stop]
        for path in tree_paths(root)
        for start, stop in zip(path, path[1:])
        if start != stop
    ]
