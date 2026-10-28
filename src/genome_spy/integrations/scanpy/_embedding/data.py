"""Read stored embedding inputs without running analysis or choosing layout."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import combinations, product
from numbers import Integral
from typing import Any
import warnings

import numpy as np
import pandas as pd

from genome_spy.anndata import from_anndata
from genome_spy.integrations.scanpy._data import (
    require_resident_expression,
    resolve_use_raw,
)
from genome_spy.integrations.scanpy._style import (
    EMBEDDING_MARKERS,
    _categorical,
    ColorData,
    categorical_colors,
    continuous_colors,
    draw_order,
    native_color,
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
    show_missing: bool = True
    color_extremes: tuple[str, str] | None = None


@dataclass(frozen=True, slots=True)
class PreparedEmbedding:
    table: pd.DataFrame
    panels: tuple[Panel, ...]
    axis_labels: tuple[str, ...]
    basis: str
    row_label: str = "Observation"
    show_ticks: bool = False
    edges: pd.DataFrame | None = None


def embedding_key(adata: Any, basis: str, *, context: str) -> str:
    """Resolve an existing obsm key using Scanpy's direct-name then X_ precedence."""
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    if not isinstance(basis, str) or not basis:
        raise ValueError(f"{context}: basis must be a nonempty obsm name.")
    key = basis if basis in adata.obsm else f"X_{basis}"
    if key not in adata.obsm:
        raise ValueError(
            f"{context}: missing {basis}/X_{basis} in obsm; compute the embedding explicitly with Scanpy first."
        )
    if len(adata.obsm[key].shape) != 2:
        raise ValueError(f"{context}: embedding coordinates must be two-dimensional.")
    return key


def _axis_labels(
    adata: Any, basis: str, count: int, annotate: bool, needed: int
) -> tuple[str, ...]:
    """Name stored components, adding supplied PCA variance percentages when requested."""
    prefix = {"umap": "UMAP", "tsne": "tSNE", "diffmap": "DC", "pca": "PC"}.get(
        basis, basis
    )
    if "draw_graph" in basis:
        prefix = basis.replace("draw_graph_", "").upper()
    labels = [f"{prefix}{i + 1}" for i in range(count)]
    if annotate:
        stored = adata.uns.get("pca")
        ratios = np.asarray(
            stored.get("variance_ratio", []) if isinstance(stored, Mapping) else []
        )
        if (
            ratios.ndim != 1
            or not np.issubdtype(ratios.dtype, np.number)
            or np.iscomplexobj(ratios)
            or len(ratios) < needed
            or not np.isfinite(ratios).all()
        ):
            raise ValueError(
                "gsc.pl.pca: annotate_var_explained requires finite stored pca variance_ratio for each component."
            )
        labels = [
            f"{label} ({round(float(ratios[i]) * 100, 2)}%)"
            if i < len(ratios)
            else label
            for i, label in enumerate(labels)
        ]
    return tuple(labels)


def dimensions_for(
    components: Any, dimensions: Any, count: int
) -> list[tuple[int, int]]:
    """Return zero-based coordinate pairs from component options and column count.

    Convert Scanpy's one-based component strings and reject unavailable columns.
    """
    pairs: Any
    if components is not None and dimensions is not None:
        raise ValueError(
            "Scanpy embedding: components and dimensions are mutually exclusive."
        )
    if components == "all":
        pairs = list(combinations(range(count), 2))
    elif components is not None:
        # Scanpy's component strings count from one; array columns count from zero.
        entries = [components] if isinstance(components, str) else components
        try:
            pairs = [tuple(int(x) - 1 for x in pair.split(",")) for pair in entries]
        except (ValueError, AttributeError) as error:
            raise ValueError(
                "Scanpy embedding: expected one-based component pairs."
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
            f"Scanpy embedding: expected valid 2D components in an embedding with {count} columns."
        )
    return [(int(p[0]), int(p[1])) for p in pairs]


def _expression(
    adata: Any, key: str, use_raw: bool, layer: str | None, symbols: str | None
) -> tuple[Any, str]:
    """Return a copied observation or gene vector and its source label from AnnData.

    Resolve symbols and raw/layer choices using Scanpy's embedding lookup rules.
    """
    if key in adata.obs:
        if list(adata.obs.columns).count(key) != 1:
            raise ValueError(
                f"Scanpy embedding: observation field {key!r} is ambiguous."
            )
        if key in adata.var_names or (use_raw and key in adata.raw.var_names):
            raise ValueError(
                f"Scanpy embedding: {key!r} occurs in both observation and gene names."
            )
        return adata.obs[key].copy(), f"obs[{key!r}]"
    resolved = key

    # Match symbols against var before looking up the gene in the chosen source.
    if symbols is not None and key not in adata.var_names:
        if symbols not in adata.var or list(adata.var.columns).count(symbols) != 1:
            raise ValueError(
                f"Scanpy embedding: gene-symbol column {symbols!r} is missing or ambiguous."
            )
        matches = np.flatnonzero(adata.var[symbols].eq(key).to_numpy())
        if len(matches) != 1:
            raise ValueError(
                f"Scanpy embedding: gene symbol {key!r} is missing or ambiguous."
            )
        resolved = str(adata.var_names[matches[0]])
    names = adata.raw.var_names if use_raw else adata.var_names
    matches = np.flatnonzero(names == resolved)
    if len(matches) != 1:
        raise ValueError(
            f"Scanpy embedding: gene {key!r} is missing or ambiguous in the selected representation."
        )
    require_resident_expression(adata, use_raw, layer, context="Scanpy embedding")

    # Use the same public vector access as Scanpy's embedding plots.
    if use_raw:
        values = adata.raw.obs_vector(resolved)
        source = "raw.X"
    else:
        values = adata.obs_vector(resolved, layer=layer)
        source = "X" if layer is None else f"layers[{layer!r}]"
    return np.asarray(values).copy(), source


def _panel_inputs(
    count: int, color: Any, components: Any, dimensions: Any, marker: Any
) -> list[tuple[Any, tuple[int, int], str]]:
    """Return each panel's color key, coordinate pair and marker from plot options.

    Expand options using Scanpy's list rules without reading coordinates again.
    """
    pairs = dimensions_for(components, dimensions, count)
    keys = color
    keys = [keys] if keys is None or isinstance(keys, str) else list(keys)
    if not keys or any(key is not None and not isinstance(key, str) for key in keys):
        raise ValueError(
            "Scanpy embedding: color must contain observation or gene keys."
        )

    # components combines every color with every pair; dimensions pairs the lists.
    if components is not None:
        combinations = list(product(keys, pairs))
        keys = [key for key, _ in combinations]
        pairs = [pair for _, pair in combinations]
    markers = marker
    markers = [markers] if isinstance(markers, str) else list(markers)

    # One value can serve every panel, but longer lists must agree in length.
    count = max(len(keys), len(pairs), len(markers))
    if any(len(values) not in (1, count) for values in (keys, pairs, markers)):
        raise ValueError(
            "Scanpy embedding: color, dimensions, and marker lists cannot be broadcast."
        )
    keys, pairs, markers = [
        values * count if len(values) == 1 else values
        for values in (keys, pairs, markers)
    ]
    if any(
        not isinstance(marker, str) or marker not in EMBEDDING_MARKERS
        for marker in markers
    ):
        raise NotImplementedError(
            f"Scanpy embedding: marker must be one of {tuple(EMBEDDING_MARKERS)}."
        )
    return list(zip(keys, pairs, markers, strict=True))


def _observations(
    adata: Any, basis: str, pairs: list[tuple[int, int]], obs_id: str | None
) -> pd.DataFrame:
    """Return requested embedding columns and cell IDs as a table in observation order.

    Read no expression and keep duplicate cell names distinct for linked panels.
    """
    needed = sorted({dimension for pair in pairs for dimension in pair})

    # Read coordinates without rejecting unrelated duplicate gene names.
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
        raise ValueError("Scanpy embedding: coordinates must be finite.")

    values = None
    if obs_id is not None:
        if list(adata.obs.columns).count(obs_id) != 1:
            raise ValueError(
                f"Scanpy embedding: obs_id column {obs_id!r} is missing or ambiguous."
            )
        values = adata.obs[obs_id]
    return pd.concat([table, point_ids(adata.obs_names, values)], axis=1)


def point_ids(names: pd.Index, values: pd.Series | None = None) -> pd.DataFrame:
    """Return stable point IDs and original labels without changing their row order."""
    if values is None:
        ids = names.to_numpy().copy()
        if not names.is_unique:
            ids = np.array([f"row-{i}" for i in range(len(names))])
    else:
        if values.isna().any() or not values.is_unique:
            raise ValueError(
                "Scanpy embedding: obs_id values must be unique and nonmissing."
            )
        ids = values.astype(str).to_numpy()
        if len(set(ids)) != len(ids):
            raise ValueError(
                "Scanpy embedding: obs_id values collide when serialized as strings."
            )
    return pd.DataFrame({"_obs_id": ids, "_obs_label": names.to_numpy().copy()})


def panel_values(
    table: pd.DataFrame, index: int, colors: ColorData, order: np.ndarray, size: Any
) -> None:
    """Attach one panel's colors, painting order and sizes to the shared point table."""
    table[f"_value_{index}"] = colors.values
    table[f"_color_{index}"] = colors.values
    if colors.categorical:
        table[f"_color_{index}"] = [
            "NA" if pd.isna(value) else value for value in colors.values
        ]
    rank = np.empty(len(order), dtype=int)
    rank[order] = np.arange(len(order))
    table[f"_order_{index}"] = rank
    table[f"_size_{index}"] = size


def _mask(adata: Any, mask: Any) -> np.ndarray | None:
    """Return a checked cell mask from an obs key or vector, or None when unset.

    Require AnnData's row order so hiding colors cannot target the wrong cells.
    """
    if mask is None:
        return None
    if isinstance(mask, str):
        if list(adata.obs.columns).count(mask) != 1:
            raise ValueError(
                f"Scanpy embedding: mask_obs field {mask!r} is missing or ambiguous."
            )
        mask = adata.obs[mask]

    # A labeled mask must already follow the same cells in the same order.
    if isinstance(mask, pd.Series) and not mask.index.equals(adata.obs_names):
        raise ValueError(
            "Scanpy embedding: mask_obs index must match observation order."
        )
    mask = np.asarray(mask)
    if mask.shape != (len(adata),) or mask.dtype != np.bool_:
        raise ValueError(
            "Scanpy embedding: mask_obs must be a nonmissing boolean vector with one entry per observation."
        )
    return np.asarray(mask)


def _sizes(size: Any, count: int) -> np.ndarray:
    """Return checked scalar or per-cell areas for count cells, using Scanpy's default."""
    values = np.asarray(120000 / count if size is None else size, dtype=float)
    if values.ndim > 1 or (values.ndim == 1 and values.shape != (count,)):
        raise ValueError(
            "Scanpy embedding: size must be scalar or one per observation."
        )
    if not np.isfinite(values).all() or np.any(values < 0):
        raise ValueError("Scanpy embedding: size must be finite and nonnegative.")
    return values


def _neighbor_edges(
    adata: Any, table: pd.DataFrame, neighbors_key: str | None
) -> pd.DataFrame:
    """Return stored undirected edges as pairs of stable cell IDs, without analysis.

    Match Scanpy's NetworkX conversion and legacy/current connectivity storage.
    """
    import networkx as nx
    from scipy import sparse

    key = "neighbors" if neighbors_key is None else neighbors_key
    if not isinstance(key, str) or key not in adata.uns:
        raise ValueError(
            f"Scanpy embedding: missing neighbors metadata at uns[{key!r}]; "
            "compute neighbors explicitly with Scanpy first."
        )
    metadata = adata.uns[key]
    if not isinstance(metadata, Mapping):
        raise ValueError(f"Scanpy embedding: uns[{key!r}] must be a neighbors mapping.")
    connection_key = (
        "connectivities" if key == "neighbors" else metadata.get("connectivities_key")
    )
    if not isinstance(connection_key, str):
        raise ValueError(f"Scanpy embedding: uns[{key!r}] needs connectivities_key.")
    matrix = (
        adata.obsp[connection_key]
        if connection_key in adata.obsp
        else metadata.get(connection_key)
    )
    if matrix is None:
        raise ValueError(
            f"Scanpy embedding: missing stored {connection_key!r} connectivities."
        )
    if not isinstance(matrix, np.ndarray) and not sparse.issparse(matrix):
        raise NotImplementedError(
            "Scanpy embedding: connectivities require resident NumPy or SciPy arrays."
        )
    values = matrix.tocoo(copy=False).data if sparse.issparse(matrix) else matrix
    if (
        matrix.shape != (len(table), len(table))
        or matrix.dtype.kind not in "biuf"
        or not np.isfinite(values).all()
    ):
        raise ValueError(
            "Scanpy embedding: connectivities must be a finite real square matrix matching the cells."
        )

    # NetworkX also preserves asymmetric entries and explicitly stored sparse zeros.
    pairs = np.asarray(list(nx.Graph(matrix).edges()), dtype=np.int64).reshape(-1, 2)
    if np.any(pairs[:, 0] == pairs[:, 1]):
        raise NotImplementedError(
            "Scanpy embedding: self-loop edges are not supported yet."
        )
    ids = table["_obs_id"].to_numpy()
    return pd.DataFrame({"_source": ids[pairs[:, 0]], "_target": ids[pairs[:, 1]]})


def _title(title: Any, key: str | None, index: int) -> str | None:
    """Return a panel title from a string or list, falling back to its color key."""
    if title is None:
        return key
    if isinstance(title, str):
        return title
    if index < len(title):
        return str(title[index])
    warnings.warn(
        "Scanpy embedding: title list is shorter than the panel count; using color keys.",
        UserWarning,
        stacklevel=3,
    )
    return key


def prepare_embedding(
    adata: Any,
    *,
    basis: str,
    annotate_var_explained: bool = False,
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
    vcenter: Any,
    title: Any,
    obs_id: str | None,
    colorbar_loc: str | None,
    edges: bool = False,
    neighbors_key: str | None = None,
) -> PreparedEmbedding:
    """Return a shared cell table and panel settings from AnnData and embedding options.

    Read existing coordinates and selected colors, preserving cell identity and
    Scanpy draw order without changing AnnData or computing an embedding.
    """
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError("Scanpy embedding: expected AnnData.")
    if adata.n_obs == 0:
        raise ValueError("Scanpy embedding: at least one observation is required.")

    # All panels share the original coordinates and observation IDs.
    use_raw = resolve_use_raw(adata, use_raw, layer, context="Scanpy embedding")
    key = embedding_key(adata, basis, context="Scanpy embedding")
    count = adata.obsm[key].shape[1]
    inputs = _panel_inputs(count, color, components, dimensions, marker)
    if edges and any(pair != (0, 1) for _, pair, _ in inputs):
        raise NotImplementedError(
            "Scanpy embedding: edges require the first two stored components, "
            "dimensions=(0, 1); other pairs are not supported yet."
        )
    needed = max(d for _, pair, _ in inputs for d in pair) + 1
    labels = _axis_labels(adata, basis, count, annotate_var_explained, needed)
    table = _observations(
        adata, key, [dimensions for _, dimensions, _ in inputs], obs_id
    )
    mask = _mask(adata, mask_obs)
    size = _sizes(size, len(adata))
    na_color = native_color(na_color, "na_color")
    extracted = {}
    panels = []

    for index, (key, dimensions, marker) in enumerate(inputs):
        # Read each color field once even when several panels use it.
        if key is None:
            values, source = pd.Categorical([None] * len(adata)), "none"
        else:
            if key not in extracted:
                extracted[key] = _expression(adata, key, use_raw, layer, gene_symbols)
            values, source = extracted[key]

        # Categories need ordered labels; numeric values need continuous bounds.
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
                vcenter=vcenter,
                index=index,
                count=len(inputs),
                colorbar=colorbar_loc is not None,
                sort_order=sort_order,
            )

        order = draw_order(
            colors.values, categorical=colors.categorical, sort=sort_order
        )
        panel_values(table, index, colors, order, size)

        # Scanpy 1.11.5 carries the reordered size vector into the next panel.
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
    return PreparedEmbedding(
        table,
        tuple(panels),
        labels,
        basis,
        edges=_neighbor_edges(adata, table, neighbors_key) if edges else None,
    )
