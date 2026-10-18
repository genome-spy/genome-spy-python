"""Read existing UMAP plot inputs without running analysis or choosing layout."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from numbers import Integral
from typing import Any
import warnings

import numpy as np
import pandas as pd

from genome_spy.anndata import from_anndata
from genome_spy.integrations.scanpy._colors import native_color
from genome_spy.integrations.scanpy._data import (
    require_resident_expression,
    resolve_use_raw,
)
from genome_spy.integrations.scanpy._umap_colors import (
    _categorical,
    categorical_colors,
    continuous_colors,
)


@dataclass(frozen=True, slots=True)
class Panel:
    key: str | None
    source: str
    dimensions: tuple[int, int]
    categorical: bool
    domain: tuple[Any, ...]
    palette: tuple[str, ...]
    scheme: str | None
    legend_values: tuple[str, ...]
    marker: str
    title: str | None


@dataclass(frozen=True, slots=True)
class PreparedUMAP:
    table: pd.DataFrame
    panels: tuple[Panel, ...]


def dimensions_for(
    components: Any, dimensions: Any, count: int
) -> list[tuple[int, int]]:
    pairs: Any
    if components is not None and dimensions is not None:
        raise ValueError(
            "gsc.pl.umap: components and dimensions are mutually exclusive."
        )
    if components == "all":
        pairs = list(combinations(range(count), 2))
    elif components is not None:
        entries = [components] if isinstance(components, str) else components
        try:
            pairs = [tuple(int(x) - 1 for x in pair.split(",")) for pair in entries]
        except (ValueError, AttributeError) as error:
            raise ValueError(
                "gsc.pl.umap: expected one-based component pairs."
            ) from error
    else:
        values = (0, 1) if dimensions is None else dimensions
        pairs = (
            [values] if all(isinstance(x, Integral) for x in values) else list(values)
        )
    if not pairs or any(
        len(p) != 2
        or any(
            isinstance(x, bool)
            or not isinstance(x, Integral)
            or not 0 <= int(x) < count
            for x in p
        )
        for p in pairs
    ):
        raise ValueError(
            f"gsc.pl.umap: expected valid 2D components in an embedding with {count} columns."
        )
    return [(int(p[0]), int(p[1])) for p in pairs]


def draw_order(values: np.ndarray, *, categorical: bool, sort: bool) -> np.ndarray:
    if not sort:
        return np.arange(len(values))
    if categorical:
        return np.argsort(~pd.isna(values), kind="stable")
    # Reversing a stable descending sort also reverses equal-value ties.
    return np.argsort(-values, kind="stable")[::-1]


def _expression(
    adata: Any, key: str, use_raw: bool, layer: str | None, symbols: str | None
) -> tuple[Any, str]:
    if key in adata.obs:
        if list(adata.obs.columns).count(key) != 1:
            raise ValueError(f"gsc.pl.umap: observation field {key!r} is ambiguous.")
        if key in adata.var_names or (use_raw and key in adata.raw.var_names):
            raise ValueError(
                f"gsc.pl.umap: {key!r} occurs in both observation and gene names."
            )
        return adata.obs[key].copy(), f"obs[{key!r}]"
    resolved = key
    if symbols is not None and key not in adata.var_names:
        if symbols not in adata.var or list(adata.var.columns).count(symbols) != 1:
            raise ValueError(
                f"gsc.pl.umap: gene-symbol column {symbols!r} is missing or ambiguous."
            )
        matches = np.flatnonzero(adata.var[symbols].eq(key).to_numpy())
        if len(matches) != 1:
            raise ValueError(
                f"gsc.pl.umap: gene symbol {key!r} is missing or ambiguous."
            )
        resolved = str(adata.var_names[matches[0]])
    names = adata.raw.var_names if use_raw else adata.var_names
    matches = np.flatnonzero(names == resolved)
    if len(matches) != 1:
        raise ValueError(
            f"gsc.pl.umap: gene {key!r} is missing or ambiguous in the selected representation."
        )
    require_resident_expression(adata, use_raw, layer, context="gsc.pl.umap")
    # Use the same public vector access as Scanpy's embedding plots.
    if use_raw:
        values = adata.raw.obs_vector(resolved)
        source = "raw.X"
    else:
        values = adata.obs_vector(resolved, layer=layer)
        source = "X" if layer is None else f"layers[{layer!r}]"
    return np.asarray(values).copy(), source


def _panel_inputs(
    adata: Any, color: Any, components: Any, dimensions: Any, marker: Any
) -> list[tuple[Any, tuple[int, int], str]]:
    basis = "umap" if "umap" in adata.obsm else "X_umap"
    if basis not in adata.obsm:
        raise ValueError(
            "gsc.pl.umap: missing umap/X_umap in obsm; compute the embedding explicitly with Scanpy first."
        )
    pairs = dimensions_for(components, dimensions, adata.obsm[basis].shape[1])
    keys = color
    keys = [keys] if keys is None or isinstance(keys, str) else list(keys)
    if not keys or any(key is not None and not isinstance(key, str) for key in keys):
        raise ValueError("gsc.pl.umap: color must contain observation or gene keys.")
    if components is not None:
        combinations = list(product(keys, pairs))
        keys = [key for key, _ in combinations]
        pairs = [pair for _, pair in combinations]
    markers = marker
    markers = [markers] if isinstance(markers, str) else list(markers)
    count = max(len(keys), len(pairs), len(markers))
    if any(len(values) not in (1, count) for values in (keys, pairs, markers)):
        raise ValueError(
            "gsc.pl.umap: color, dimensions, and marker lists cannot be broadcast."
        )
    keys, pairs, markers = [
        values * count if len(values) == 1 else values
        for values in (keys, pairs, markers)
    ]
    if any(marker not in (".", "o") for marker in markers):
        raise NotImplementedError(
            "gsc.pl.umap: only '.' and 'o' markers are supported yet."
        )
    return list(zip(keys, pairs, markers, strict=True))


def _observations(
    adata: Any, pairs: list[tuple[int, int]], obs_id: str | None
) -> pd.DataFrame:
    basis = "umap" if "umap" in adata.obsm else "X_umap"
    needed = sorted({dimension for pair in pairs for dimension in pair})
    # obs_df rejects unrelated duplicate genes even for coordinate-only requests.
    coordinates = from_anndata(
        adata, obs=[], obsm_keys=[(basis, dimension) for dimension in needed]
    )
    table = pd.DataFrame(
        {
            f"_coord_{dimension}": coordinates[f"{basis}-{dimension}"].to_numpy().copy()
            for dimension in needed
        }
    )
    if not np.isfinite(table.to_numpy()).all():
        raise ValueError("gsc.pl.umap: coordinates must be finite.")
    if obs_id is None:
        ids = adata.obs_names.to_numpy().copy()
        if not adata.obs_names.is_unique:
            ids = np.array([f"row-{i}" for i in range(len(adata))])
    else:
        if list(adata.obs.columns).count(obs_id) != 1:
            raise ValueError(
                f"gsc.pl.umap: obs_id column {obs_id!r} is missing or ambiguous."
            )
        values = adata.obs[obs_id]
        if values.isna().any() or not values.is_unique:
            raise ValueError(
                "gsc.pl.umap: obs_id values must be unique and nonmissing."
            )
        ids = values.astype(str).to_numpy()
        if len(set(ids)) != len(ids):
            raise ValueError(
                "gsc.pl.umap: obs_id values collide when serialized as strings."
            )
    table["_obs_id"] = ids
    table["_obs_label"] = adata.obs_names.to_numpy().copy()
    return table


def _mask(adata: Any, mask: Any) -> np.ndarray | None:
    if mask is None:
        return None
    if isinstance(mask, str):
        if list(adata.obs.columns).count(mask) != 1:
            raise ValueError(
                f"gsc.pl.umap: mask_obs field {mask!r} is missing or ambiguous."
            )
        mask = adata.obs[mask]
    if isinstance(mask, pd.Series) and not mask.index.equals(adata.obs_names):
        raise ValueError("gsc.pl.umap: mask_obs index must match observation order.")
    mask = np.asarray(mask)
    if mask.shape != (len(adata),) or mask.dtype != np.bool_:
        raise ValueError(
            "gsc.pl.umap: mask_obs must be a nonmissing boolean vector with one entry per observation."
        )
    return np.asarray(mask)


def _sizes(size: Any, count: int) -> np.ndarray:
    values = np.asarray(120000 / count if size is None else size, dtype=float)
    if values.ndim > 1 or (values.ndim == 1 and values.shape != (count,)):
        raise ValueError("gsc.pl.umap: size must be scalar or one per observation.")
    if not np.isfinite(values).all() or np.any(values < 0):
        raise ValueError("gsc.pl.umap: size must be finite and nonnegative.")
    return values


def _title(title: Any, key: str | None, index: int) -> str | None:
    if title is None:
        return key
    if isinstance(title, str):
        return title
    if index < len(title):
        return str(title[index])
    warnings.warn(
        "gsc.pl.umap: title list is shorter than the panel count; using color keys.",
        UserWarning,
        stacklevel=3,
    )
    return key


def prepare_umap(
    adata: Any,
    *,
    color: Any,
    mask_obs: Any,
    gene_symbols: str | None,
    use_raw: bool | None,
    layer: str | None,
    groups: Any,
    components: Any,
    dimensions: Any,
    size: Any,
    marker: Any,
    palette: Any,
    cmap: Any,
    na_color: str,
    na_in_legend: bool,
    sort_order: bool,
    vmin: Any,
    vmax: Any,
    title: Any,
    obs_id: str | None,
    colorbar_loc: str | None,
) -> PreparedUMAP:
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError("gsc.pl.umap: expected AnnData.")
    if adata.n_obs == 0:
        raise ValueError("gsc.pl.umap: at least one observation is required.")
    use_raw = resolve_use_raw(adata, use_raw, layer, context="gsc.pl.umap")
    inputs = _panel_inputs(adata, color, components, dimensions, marker)
    table = _observations(adata, [dimensions for _, dimensions, _ in inputs], obs_id)
    mask = _mask(adata, mask_obs)
    size = _sizes(size, len(adata))
    na_color = native_color(na_color, "na_color")
    extracted = {}
    panels = []

    for index, (key, dimensions, marker) in enumerate(inputs):
        if key is None:
            values, source = pd.Categorical([None] * len(adata)), "none"
        else:
            if key not in extracted:
                extracted[key] = _expression(adata, key, use_raw, layer, gene_symbols)
            values, source = extracted[key]
        categorical = _categorical(values)
        if categorical is not None:
            colors = categorical_colors(
                adata,
                key,
                categorical,
                palette=palette,
                groups=groups,
                mask=mask,
                na_color=na_color,
                na_in_legend=na_in_legend,
            )
        else:
            colors = continuous_colors(
                values,
                cmap=cmap,
                mask=mask,
                vmin=vmin,
                vmax=vmax,
                index=index,
                count=len(inputs),
                colorbar=colorbar_loc is not None,
            )

        table[f"_value_{index}"] = colors.values
        table[f"_color_{index}"] = colors.values
        if colors.categorical:
            table[f"_color_{index}"] = [
                "NA" if pd.isna(value) else value for value in colors.values
            ]
        order = draw_order(
            colors.values, categorical=colors.categorical, sort=sort_order
        )
        rank = np.empty(len(order), dtype=int)
        rank[order] = np.arange(len(order))
        table[f"_order_{index}"] = rank
        table[f"_size_{index}"] = size
        # Preserve Scanpy 1.11.5's size-vector carry between panels.
        if size.ndim == 1:
            size = size[order]
        panels.append(
            Panel(
                key,
                source,
                dimensions,
                colors.categorical,
                colors.domain,
                colors.palette,
                colors.scheme,
                colors.legend_values,
                marker,
                _title(title, key, index),
            )
        )
    return PreparedUMAP(table, tuple(panels))
