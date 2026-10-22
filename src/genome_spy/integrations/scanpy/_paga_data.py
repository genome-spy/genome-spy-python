"""Stored PAGA graphs and node tables, with layout computation owned by Scanpy."""

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import matrix_array, number, numeric_values
from genome_spy.integrations.scanpy._style import _palette, native_color

CONTEXT = "gsc.pl.paga"


def _graph(adata: Any, key: str, count: int, threshold: float) -> tuple[Any, Any]:
    """Return a layout-ready sparse source and thresholded graph without changing stored data."""
    import networkx as nx
    from scipy import sparse

    if not isinstance(key, str):
        raise TypeError(f"{CONTEXT}: graph keys must be strings.")
    matrix = adata.uns["paga"].get(key)
    if not sparse.issparse(matrix) or matrix.shape != (count, count):
        raise ValueError(
            f"{CONTEXT}: paga[{key!r}] must be a {count}-by-{count} SciPy sparse graph."
        )
    source = matrix if matrix.format in {"csr", "csc"} else matrix.tocsr()
    # COO preserves stored edge order and gives every format the same filtering path.
    matrix = matrix.tocoo(copy=True)
    if not np.isfinite(matrix.data).all():
        raise ValueError(f"{CONTEXT}: graph weights must be finite.")
    if threshold > 0:
        matrix.data[matrix.data < threshold] = 0
        matrix.eliminate_zeros()
    graph = nx.Graph(matrix)
    if any(a == b for a, b in graph.edges):
        raise NotImplementedError(f"{CONTEXT}: self-loops are unsupported.")
    if any(weight < 0 for _, _, weight in graph.edges(data="weight")):
        raise ValueError(f"{CONTEXT}: retained graph weights must be nonnegative.")
    return source, graph


def prepare_paga(
    adata: Any,
    *,
    threshold: float | None,
    solid_edges: str,
    dashed_edges: str | None,
    pos: Any,
    layout: Any,
    layout_kwds: Mapping[str, Any],
    init_pos: Any,
    root: Any,
    random_state: Any,
) -> tuple[str, np.ndarray, Any, Any]:
    """Read stored graphs and return group key, positions and graphs; never run PAGA analysis."""
    from anndata import AnnData
    import scanpy as sc

    if not isinstance(adata, AnnData):
        raise TypeError(f"{CONTEXT}: adata must be AnnData.")
    stored = adata.uns.get("paga", {})
    if not isinstance(stored, Mapping):
        raise ValueError(f"{CONTEXT}: paga must contain stored graph metadata.")
    key = stored.get("groups")
    if (
        not isinstance(key, str)
        or key not in adata.obs
        or not isinstance(adata.obs[key].dtype, pd.CategoricalDtype)
    ):
        raise ValueError(
            f"{CONTEXT}: stored PAGA results and categorical groups are required; run sc.tl.paga explicitly."
        )
    count = len(adata.obs[key].cat.categories)
    if not count:
        raise ValueError(f"{CONTEXT}: at least one PAGA group is required.")
    threshold = number(
        0.01 if threshold is None else threshold,
        "threshold",
        context=CONTEXT,
        minimum=-np.inf,
    )
    source, solid = _graph(adata, solid_edges, count, threshold)
    dashed = None
    if dashed_edges is not None:
        _, dashed = _graph(adata, dashed_edges, count, threshold)
    if pos is None:
        # Compute layout without copying expression or opening a figure.
        graph_data = AnnData(
            obs=adata.obs[[key]], uns={"paga": {**stored, solid_edges: source}}
        )
        sc.pl.paga(
            graph_data,
            threshold=threshold,
            solid_edges=solid_edges,
            layout=layout,
            layout_kwds=layout_kwds,
            init_pos=init_pos,
            root=root,
            random_state=random_state,
            plot=False,
            add_pos=True,
            show=False,
            save=False,
        )
        pos = graph_data.uns["paga"]["pos"]
    positions = numeric_values(
        pd.DataFrame(matrix_array(pos, context=CONTEXT)), context=CONTEXT
    )
    if positions.shape != (count, 2) or not np.isfinite(positions).all():
        raise ValueError(
            f"{CONTEXT}: pos must contain two finite coordinates per group."
        )
    return key, positions, solid, dashed


def paga_nodes(
    adata: Any,
    key: str,
    positions: np.ndarray,
    *,
    color: Any,
    labels: Any,
    node_size_scale: float,
    node_size_power: float,
) -> pd.DataFrame:
    """Return node labels, CSS colors and Scanpy-sized areas using stored group sizes."""
    categories = adata.obs[key].cat.categories
    count = len(categories)
    if labels is None:
        labels = list(map(str, categories))
    if (
        isinstance(labels, (str, Mapping))
        or not isinstance(labels, (Sequence, pd.Index, np.ndarray))
        or len(labels) != count
    ):
        raise ValueError(f"{CONTEXT}: labels requires one string label per group.")
    if any(not isinstance(label, str) for label in labels):
        raise TypeError(f"{CONTEXT}: labels must be strings.")
    if color is None or isinstance(color, str) and color == key:
        cached = adata.uns.get(f"{key}_colors")
        if cached is not None and len(cached) != count:
            raise ValueError(
                f"{CONTEXT}: cached group palette must match the group count."
            )
        colors, _ = _palette(adata, key, categories, None, context=CONTEXT)
    elif isinstance(color, str):
        colors = (native_color(color, "color", context=CONTEXT),) * count
    elif isinstance(color, (Sequence, np.ndarray)) and len(color) == count:
        colors = tuple(native_color(c, "color", context=CONTEXT) for c in color)
    else:
        raise NotImplementedError(
            f"{CONTEXT}: color supports the PAGA grouping, one CSS color or one CSS color per node; numeric annotations, other categorical annotations and pies are unsupported."
        )
    sizes = numeric_values(
        pd.DataFrame(adata.uns.get(f"{key}_sizes", np.ones(count))), context=CONTEXT
    ).ravel()
    if (
        len(sizes) != count
        or not np.isfinite(sizes).all()
        or (sizes < 0).any()
        or np.median(sizes) <= 0
    ):
        raise ValueError(
            f"{CONTEXT}: stored group sizes require nonnegative values and a positive median."
        )
    scale = number(node_size_scale, "node_size_scale", context=CONTEXT)
    power = number(node_size_power, "node_size_power", context=CONTEXT, minimum=-np.inf)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        areas = (
            2000 / (np.sqrt(count) + 10) * scale * (sizes / np.median(sizes)) ** power
        )
    if not np.isfinite(areas).all():
        raise ValueError(f"{CONTEXT}: node sizing must produce finite areas.")
    return pd.DataFrame(
        {
            "_id": np.arange(count),
            "_group": list(map(str, categories)),
            "_label": list(labels),
            "_x": positions[:, 0],
            "_y": positions[:, 1],
            "_color": colors,
            "_area": areas,
            "_cells": adata.obs[key]
            .value_counts()
            .reindex(categories, fill_value=0)
            .to_numpy(),
        }
    )


def paga_edges(
    graph: Any,
    positions: np.ndarray,
    *,
    edge_width_scale: float,
    min_edge_width: float | None,
    max_edge_width: float | None,
) -> pd.DataFrame:
    """Return stored edge endpoints and widths in Scanpy's NetworkX drawing order."""
    scale = number(edge_width_scale, "edge_width_scale", context=CONTEXT)
    low = (
        number(min_edge_width, "min_edge_width", context=CONTEXT)
        if min_edge_width is not None
        else None
    )
    high = (
        number(max_edge_width, "max_edge_width", context=CONTEXT)
        if max_edge_width is not None
        else None
    )
    rows = []
    for a, b, weight in graph.edges(data="weight"):
        width = float(np.clip(7.5 * scale * weight, low, high))
        rows.append((a, b, *positions[a], *positions[b], weight, width))
    return pd.DataFrame(
        rows,
        columns=["_source", "_target", "_x", "_y", "_x2", "_y2", "_weight", "_width"],
    )
