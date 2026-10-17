"""Scanpy color semantics; no figures, artists, or global style settings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any
import warnings

import numpy as np
import pandas as pd


@dataclass(frozen=True, slots=True)
class ColorData:
    values: np.ndarray
    domain: tuple[Any, ...]
    palette: tuple[str, ...]
    scheme: str | None
    legend_values: tuple[str, ...]
    categorical: bool


def _bound(
    bound: Any, index: int, count: int, values: np.ndarray, default: float
) -> float:
    if isinstance(bound, Sequence) and not isinstance(bound, str):
        if len(bound) not in (1, count):
            raise ValueError(
                "gsc.pl.umap: color-bound lists must have one value or one per panel."
            )
        bound = bound[0 if len(bound) == 1 else index]
    if bound is None:
        return default
    if callable(bound):
        raise NotImplementedError(
            "gsc.pl.umap: callable color bounds are not supported yet."
        )
    if isinstance(bound, str):
        if not bound.startswith("p"):
            raise ValueError("gsc.pl.umap: percentile bounds must start with 'p'.")
        bound = float(np.nanpercentile(values, float(bound[1:])))
    result = float(bound)
    if not np.isfinite(result):
        raise ValueError("gsc.pl.umap: color bounds must be finite.")
    return result


def _categorical(values: Any) -> pd.Categorical | None:
    if isinstance(getattr(values, "dtype", None), pd.CategoricalDtype):
        return pd.Categorical(values).copy()
    if pd.api.types.is_bool_dtype(values.dtype):
        return pd.Categorical(pd.Series(values).map({True: "True", False: "False"}))
    if pd.api.types.is_string_dtype(values.dtype) or values.dtype.kind in "OUS":
        from natsort import natsorted

        nonmissing = pd.Series(values).dropna()
        if not all(isinstance(x, str) for x in nonmissing):
            raise TypeError(
                "gsc.pl.umap: color metadata must be numeric, boolean, string, or categorical."
            )
        return pd.Categorical(values, categories=natsorted(nonmissing.unique()))
    return None


# Scheme names shipped by the bundled GenomeSpy/Vega runtime.
_SCHEMES = frozenset(
    """
accent category10 category20 category20b category20c dark2 observable10 paired
pastel1 pastel2 set1 set2 set3 tableau10 tableau20 blues greens greys oranges
purples reds bluegreen bluepurple greenblue orangered purpleblue purplebluegreen
purplered redpurple yellowgreen yelloworangebrown yelloworangered blueorange
brownbluegreen purplegreen purpleorange redblue redgrey yellowgreenblue
redyellowblue redyellowgreen pinkyellowgreen spectral viridis magma inferno
plasma cividis rainbow sinebow turbo browns tealblues teals warmgreys goldgreen
goldorange goldred lightgreyred lightgreyteal lightmulti lightorange lighttealblue
darkblue darkgold darkgreen darkmulti darkred
""".split()
)


def native_scheme(value: Any, name: str) -> str:
    if not isinstance(value, str) or value.lower() not in _SCHEMES:
        raise NotImplementedError(
            f"gsc.pl.umap: {name} requires a GenomeSpy scheme name, such as "
            "'viridis', 'redblue', or 'set1'; Matplotlib colormaps are unsupported."
        )
    return value.lower()


def native_color(value: Any, name: str) -> str:
    # Keep parsing in GenomeSpy; exclude Matplotlib forms and entry alpha.
    if isinstance(value, str):
        named = (
            value.isalpha()
            and len(value) > 2
            and value.lower() not in ("transparent", "none")
        )
        hex_color = value.startswith("#") and len(value) in (4, 7)
        if named or hex_color:
            return value
    raise NotImplementedError(
        f"gsc.pl.umap: {name} requires an opaque CSS color name or #RGB/#RRGGBB. "
        "Matplotlib colors and per-color alpha are unsupported; use scalar alpha."
    )


def _palette(
    adata: Any, key: str, categories: pd.Index, palette: Any
) -> tuple[tuple[str, ...], str | None]:
    count = len(categories)
    if isinstance(palette, str):
        return (), native_scheme(palette, "palette")
    if isinstance(palette, Mapping):
        try:
            selected = [palette[c] for c in categories]
        except KeyError as error:
            raise ValueError(
                "gsc.pl.umap: palette mapping is missing a category."
            ) from error
    elif palette is not None:
        if not isinstance(palette, (Sequence, np.ndarray)):
            raise NotImplementedError(
                "gsc.pl.umap: palette requires CSS colors or a native scheme; color cyclers are unsupported."
            )
        selected = list(palette)
        if not selected:
            raise ValueError("gsc.pl.umap: palette cannot be empty.")
        if len(selected) < count:
            warnings.warn(
                "gsc.pl.umap: palette has fewer colors than categories; colors repeat.",
                UserWarning,
                stacklevel=3,
            )
        selected = [selected[i % len(selected)] for i in range(count)]
    else:
        import scanpy as sc

        cached = adata.uns.get(f"{key}_colors", ())
        # Reuse public Scanpy palette values, without invoking color utilities.
        defaults = [
            sc.pl.palettes.vega_10,
            sc.pl.palettes.default_20,
            sc.pl.palettes.default_28,
            sc.pl.palettes.default_102,
        ]
        selected = (
            cached[:count]
            if len(cached) >= count
            else next(
                (p[:count] for p in defaults if len(p) >= count), ["grey"] * count
            )
        )
    return tuple(native_color(c, "palette") for c in selected), None


def categorical_colors(
    adata: Any,
    key: str | None,
    values: pd.Categorical,
    *,
    palette: Any,
    groups: Any,
    mask: Any,
    na_color: str,
    na_in_legend: bool,
) -> ColorData:
    categories = values.categories
    original, scheme = (
        _palette(adata, key, categories, palette) if key is not None else ((), None)
    )
    palette_map = dict(zip(categories, original))
    original_names = tuple(str(category) for category in categories)
    if groups is not None:
        groups = [groups] if isinstance(groups, str) else list(groups)
        values = values.remove_categories(categories.difference(groups))
    if mask is not None:
        values[~mask] = np.nan

    names = tuple(str(category) for category in values.categories)
    if len(set(names)) != len(names):
        raise ValueError(
            "gsc.pl.umap: category labels collide when serialized as strings."
        )
    palette_colors = (
        tuple(palette_map[category] for category in values.categories)
        if scheme is None
        else ()
    )
    legend_values = names
    missing = pd.isna(values)
    if missing.any() or key is None:
        if "NA" in names:
            raise NotImplementedError(
                "gsc.pl.umap: a category named 'NA' conflicts with missing values."
            )
        if scheme is not None and na_in_legend:
            raise NotImplementedError(
                "gsc.pl.umap: a missing-category legend with a named scheme is not supported yet; "
                "pass an explicit CSS palette or na_in_legend=False."
            )
        if scheme is None:
            names += ("NA",)
            palette_colors += (na_color,)
        if na_in_legend and key is not None:
            legend_values += ("NA",)

    measurements = np.asarray(
        [
            None if absent else str(value)
            for value, absent in zip(values, missing, strict=True)
        ],
        dtype=object,
    )
    return ColorData(
        measurements,
        original_names if scheme is not None else names,
        palette_colors,
        scheme,
        legend_values,
        True,
    )


def continuous_colors(
    values: Any,
    *,
    cmap: Any,
    mask: Any,
    vmin: Any,
    vmax: Any,
    index: int,
    count: int,
    colorbar: bool,
) -> ColorData:
    if isinstance(values, pd.Series):
        values = values.to_numpy(na_value=np.nan)
    values = np.asarray(values).copy()
    if values.dtype.kind not in "fiu" or (
        mask is not None and values.dtype.kind != "f"
    ):
        values = values.astype(float)
    if mask is not None:
        values[~mask] = np.nan
    if np.isinf(values).any() or np.isnan(values).all():
        raise ValueError(
            "gsc.pl.umap: continuous colors require finite values and at least one nonmissing value."
        )
    low = _bound(vmin, index, count, values, float(np.nanmin(values)))
    high = _bound(vmax, index, count, values, float(np.nanmax(values)))
    if low > high:
        raise ValueError("gsc.pl.umap: vmin cannot exceed vmax.")
    # Scanpy expands a constant range when it displays a colorbar.
    if low == high and colorbar:
        delta = abs(low) * 0.1 if low else 0.1
        low, high = low - delta, high + delta
    scheme = native_scheme("viridis" if cmap is None else cmap, "cmap")
    return ColorData(values, (low, high), (), scheme, (), False)
