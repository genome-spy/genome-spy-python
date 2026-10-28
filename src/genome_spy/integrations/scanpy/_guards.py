"""Shared plotting option guards and lazy Scanpy dependency checks."""

from __future__ import annotations

from collections.abc import Mapping
from importlib.metadata import PackageNotFoundError, version
from math import isfinite
from numbers import Real
from typing import Any, Literal


def _require_scanpy(context: str = "gsc.pl.umap") -> Any:
    """Return the supported Scanpy module, or raise an error naming the plotting call.

    Delay the optional import until a plot is requested to keep base imports light.
    """
    try:
        installed = version("scanpy")
    except PackageNotFoundError as error:
        raise ImportError(
            f"{context} requires genome-spy-python[scanpy] (Scanpy 1.11.5)."
        ) from error
    if installed != "1.11.5":
        raise ImportError(
            f"{context} supports Scanpy 1.11.5; found {installed}. "
            "Install genome-spy-python[scanpy]."
        )
    import scanpy

    return scanpy


def _check_kwargs(
    options: Mapping[str, Any], allowed: set[str], *, context: str
) -> None:
    """Check forwarded options against allowed names; raise a contextual error if invalid.

    Reject Matplotlib-only options explicitly rather than silently dropping them.
    """
    for name in ("ax", "return_fig"):
        if name in options:
            raise TypeError(
                f"{context}: {name} is omitted; use show=False and the native chart."
            )
    unknown = options.keys() - allowed
    if unknown:
        raise TypeError(
            f"{context}: unsupported option(s): {', '.join(sorted(unknown))}."
        )


def _check_grid_zoom(zoom: bool | Literal["xy"], *, context: str) -> None:
    """Reject invalid grid zoom modes before importing Scanpy or reading data."""
    if not isinstance(zoom, bool) and not (isinstance(zoom, str) and zoom == "xy"):
        raise TypeError(f"{context}: zoom must be False, True (y only), or 'xy'.")


def _check_grid_highlight(
    highlight: bool | Literal["outline"], *, context: str
) -> None:
    """Reject unsupported pointer feedback before reading plot data."""
    if not isinstance(highlight, bool) and not (
        isinstance(highlight, str) and highlight == "outline"
    ):
        raise TypeError(
            f"{context}: highlight must be False, True (ruler), or 'outline'."
        )


def _check_point_options(
    *,
    context: str,
    width: float | None,
    height: float | None,
    frameon: bool | None,
    **booleans: bool,
) -> None:
    """Reject invalid point dimensions and flags before loading optional dependencies."""
    for name, dimension in {"width": width, "height": height}.items():
        if dimension is not None and (
            isinstance(dimension, bool)
            or not isinstance(dimension, Real)
            or not isfinite(dimension)
            or dimension <= 0
        ):
            raise ValueError(
                f"{context}: {name} must be a positive finite number or None."
            )
    for name, option in booleans.items():
        if not isinstance(option, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if frameon is not None and not isinstance(frameon, bool):
        raise TypeError(f"{context}: frameon must be boolean or None.")
