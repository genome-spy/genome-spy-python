"""Small deterministic tables used by grammar gallery examples."""

from __future__ import annotations

import math

import pandas as pd


def sincos_data() -> pd.DataFrame:
    """Return a compact table for point and composition examples."""
    return pd.DataFrame({"x": range(31)})


def heatmap_data() -> pd.DataFrame:
    """Return a deterministic grid with a smooth quantitative value."""
    rows = [
        {"x": x, "y": y, "z": math.sin(x / 8) + math.cos(y / 10 - 0.5)}
        for y in range(20)
        for x in range(40)
    ]
    return pd.DataFrame(rows)


def ranged_rule_data() -> pd.DataFrame:
    """Return intervals for the ranged-rule example."""
    return pd.DataFrame(
        [
            {"y": "A", "x": 2, "x2": 7},
            {"y": "B", "x": 0, "x2": 3},
            {"y": "B", "x": 5, "x2": 6},
            {"y": "C", "x": 4, "x2": 8},
            {"y": "D", "x": 1, "x2": 5},
        ]
    )


def link_data() -> pd.DataFrame:
    """Return interval pairs for the link-mark example."""
    return pd.DataFrame(
        [
            {"x": 1, "x2": 5},
            {"x": 3, "x2": 8},
            {"x": 5, "x2": 11},
            {"x": 7, "x2": 13},
            {"x": 9, "x2": 16},
        ]
    )


def sequence_logo_data() -> pd.DataFrame:
    """Return base counts for a small sequence-logo example."""
    return pd.DataFrame(
        [
            {"pos": 1, "base": "A", "count": 2},
            {"pos": 1, "base": "C", "count": 3},
            {"pos": 1, "base": "T", "count": 5},
            {"pos": 2, "base": "A", "count": 7},
            {"pos": 2, "base": "C", "count": 3},
            {"pos": 3, "base": "A", "count": 10},
            {"pos": 4, "base": "T", "count": 9},
            {"pos": 4, "base": "G", "count": 1},
            {"pos": 5, "base": "G", "count": 8},
            {"pos": 6, "base": "G", "count": 7},
        ]
    )
