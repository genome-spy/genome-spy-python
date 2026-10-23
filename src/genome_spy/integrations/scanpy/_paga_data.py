"""Stored PAGA graphs and node tables, with layout computation owned by Scanpy."""

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, cast

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import matrix_array, number, numeric_values
from genome_spy.integrations.scanpy._style import ColorData, _palette, native_color

CONTEXT = "gsc.pl.paga"


def adjacency_values(
    adata: Any, adjacency: str, adjacency_tree: str
) -> tuple[np.ndarray, pd.DataFrame]:
    """Read two stored adjacency matrices; return bounded dense values and tree-point positions."""
    from anndata import AnnData
    from scipy import sparse

    context = "gsc.pl.paga_adjacency"
    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: adata must be AnnData.")
    matrices = []
    for key in (adjacency, adjacency_tree):
        if not isinstance(key, str):
            raise TypeError(f"{context}: adjacency keys must be strings.")
        matrix = adata.uns.get(key)
        if not sparse.issparse(matrix):
            raise ValueError(
                f"{context}: stored sparse uns[{key!r}] is required; "
                "supply the top-level adjacency matrices explicitly."
            )
        matrices.append(matrix)
    source, tree = matrices
    count = source.shape[0]
    if source.shape != (count, count) or not count or count * count > 250_000:
        raise ValueError(
            f"{context}: adjacency must be square with 1–250,000 values; subset explicitly."
        )
    if tree.shape != source.shape:
        raise ValueError(f"{context}: adjacency_tree must match the adjacency shape.")
    tree = tree.tocsr()
    weights = numeric_values(pd.DataFrame(tree.data), context=context)
    if not np.isfinite(weights).all():
        raise ValueError(f"{context}: adjacency_tree weights must be finite.")
    # Scanpy places a tree entry (row, column) at x=row, y=column.
    rows, columns = tree.nonzero()
    points = pd.DataFrame({"_x": rows, "_y": columns})
    return source.toarray(), points


def adjacency_points(values: np.ndarray, tree: pd.DataFrame) -> pd.DataFrame:
    """Return off-diagonal values and selected tree values in Scanpy's per-row draw order."""
    values = numeric_values(pd.DataFrame(values), context="gsc.pl.paga_adjacency")
    rows, columns = np.where(~np.eye(len(values), dtype=bool))
    background = pd.DataFrame(
        {
            "_x": rows,
            "_y": values[rows, columns],
            "_target": columns,
            "_kind": "Adjacency",
        }
    )
    selected = tree.assign(
        _y=values[tree["_x"], tree["_y"]],
        _target=tree["_y"],
        _kind="Tree",
    )
    # Stable sorting retains gray-before-black order within each source group.
    return pd.concat([background, selected], ignore_index=True).sort_values(
        "_x", kind="stable", ignore_index=True
    )


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
    solid: Any,
    dashed: Any,
    use_raw: bool,
    indices: np.ndarray | None = None,
    palette: Any = None,
) -> tuple[pd.DataFrame, bool, ColorData | None]:
    """Return node values, labels and areas, plus Scanpy's automatic colorbar choice."""
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
    colors, colorbar = _node_colors(adata, key, color, solid, dashed, use_raw, palette)
    color_data = colors if isinstance(colors, ColorData) else None
    if color_data is not None:
        colors = color_data.values
    sizes = numeric_values(
        pd.DataFrame(adata.uns.get(f"{key}_sizes", np.ones(count))), context=CONTEXT
    ).ravel()
    if len(sizes) != count or not np.isfinite(sizes).all() or (sizes < 0).any():
        raise ValueError(
            f"{CONTEXT}: stored group sizes require nonnegative values and a positive median."
        )
    slots = np.arange(count)
    if indices is not None:
        slots = indices
        categories = categories[slots]
        positions = positions[slots]
        labels = np.asarray(labels)[slots]
        colors = np.asarray(colors)[slots]
        sizes = sizes[slots]
        count = len(slots)
    if np.median(sizes) <= 0:
        raise ValueError(f"{CONTEXT}: displayed group sizes require a positive median.")
    scale = number(node_size_scale, "node_size_scale", context=CONTEXT)
    power = number(node_size_power, "node_size_power", context=CONTEXT, minimum=-np.inf)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        areas = (
            2000 / (np.sqrt(count) + 10) * scale * (sizes / np.median(sizes)) ** power
        )
    if not np.isfinite(areas).all():
        raise ValueError(f"{CONTEXT}: node sizing must produce finite areas.")
    nodes = pd.DataFrame(
        {
            "_id": slots,
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
    return nodes, colorbar, color_data


def largest_component(graph: Any) -> np.ndarray:
    """Return original node indices of the largest component, choosing the first on ties."""
    import networkx as nx

    components = cast(Iterable[set[int]], nx.connected_components(graph))
    largest = max(components, key=len)
    return np.array(sorted(largest), dtype=int)


def _node_colors(
    adata: Any,
    key: str,
    color: Any,
    solid: Any,
    dashed: Any,
    use_raw: bool,
    palette: Any,
) -> tuple[Any, bool]:
    """Return per-group colors and the default guide flag from a color key or CSS colors."""
    from genome_spy.integrations.scanpy._grouped_data import (
        grouped_expression,
        group_means,
    )

    categories = adata.obs[key].cat.categories
    count = len(categories)
    if color is None or isinstance(color, str) and color == key:
        cached = adata.uns.get(f"{key}_colors")
        if palette is None and cached is not None and len(cached) != count:
            raise ValueError(
                f"{CONTEXT}: cached group palette must match the group count."
            )
        colors, scheme = _palette(adata, key, categories, palette, context=CONTEXT)
        if scheme is not None:
            return ColorData(
                np.arange(count), tuple(range(count)), (), scheme, (), True
            ), False
        return colors, False
    if not isinstance(color, str):
        if isinstance(color, (Sequence, np.ndarray)) and len(color) == count:
            return tuple(
                native_color(c, "color", context=CONTEXT) for c in color
            ), False
        raise NotImplementedError(
            f"{CONTEXT}: mixtures/pies and multiple color panels are unsupported."
        )
    # CSS colors take precedence over annotation and gene names in Scanpy.
    try:
        css = native_color(color, "color", context=CONTEXT)
    except NotImplementedError:
        pass
    else:
        genes = adata.var_names if adata.raw is None else adata.raw.var_names
        if color in adata.obs or color in genes:
            raise NotImplementedError(
                f"{CONTEXT}: CSS colors that also name annotations or genes are unsupported."
            )
        return (css,) * count, False
    if color.startswith("degree"):
        if color not in {"degree_solid", "degree_dashed"}:
            raise ValueError(f"{CONTEXT}: use 'degree_solid' or 'degree_dashed'.")
        graph = solid if color == "degree_solid" else dashed
        if graph is None:
            raise ValueError(f"{CONTEXT}: degree_dashed requires dashed_edges.")
        degrees = np.array([d for _, d in graph.degree(weight="weight")], dtype=float)
        if np.ptp(degrees) == 0:
            raise ValueError(
                f"{CONTEXT}: equal weighted degrees have undefined 0–1 normalization."
            )
        return (degrees - degrees.min()) / np.ptp(degrees), False

    genes = adata.var_names if adata.raw is None else adata.raw.var_names
    gene = color in genes
    if not gene and color not in adata.obs:
        raise ValueError(
            f"{CONTEXT}: color {color!r} is not a gene, observation key or CSS color."
        )
    if not gene and isinstance(adata.obs[color].dtype, pd.CategoricalDtype):
        raise NotImplementedError(
            f"{CONTEXT}: other categorical annotations and mixtures/pies are unsupported."
        )
    table = grouped_expression(
        adata, [color], key, use_raw=gene and use_raw and adata.raw is not None
    ).values
    means = group_means(table).reindex(categories)[color]
    if gene:
        # Gene means propagate missing values; annotation means skip them in Scanpy.
        missing = (
            table.isna()
            .groupby(level=0, observed=True)
            .any()
            .reindex(categories, fill_value=False)[color]
        )
        means = means.mask(missing)
    return numeric_values(means.to_frame(), context=CONTEXT).ravel(), True


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
