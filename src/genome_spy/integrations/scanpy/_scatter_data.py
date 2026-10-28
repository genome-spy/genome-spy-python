"""Shared point-data access for Scanpy scatter and variable-gene QC."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import (
    numeric_values,
    require_resident_expression,
    resolve_use_raw,
)
from genome_spy.integrations.scanpy._embedding_data import (
    Panel,
    PreparedEmbedding,
    _axis_labels,
    _expression,
    _sizes,
    panel_values,
    point_ids,
)
from genome_spy.integrations.scanpy._style import (
    EMBEDDING_MARKERS,
    ColorData,
    _categorical,
    categorical_colors,
    continuous_colors,
    native_color,
)

_CONTEXT = "gsc.pl.scatter"


def prepare_variable_genes(result: Any, selected: bool) -> tuple[pd.DataFrame, str]:
    """Copy stored gene statistics and identities; return the table and statistic name."""
    from anndata import AnnData

    context = "gsc.pl.highly_variable_genes"

    # Scanpy infers variance results differently for AnnData, tables and records.
    if isinstance(result, AnnData):
        metadata = result.uns.get("hvg", {})
        if not isinstance(metadata, Mapping) or "flavor" not in metadata:
            raise ValueError(
                f"{context}: missing uns['hvg']['flavor']; run sc.pp.highly_variable_genes explicitly or supply the result DataFrame."
            )
        variance = metadata["flavor"] == "seurat_v3"
        result = result.var
    elif isinstance(result, pd.DataFrame):
        variance = "variances_norm" in result
    elif isinstance(result, np.recarray):
        result, variance = pd.DataFrame.from_records(result), False
    else:
        raise TypeError(f"{context}: expected AnnData, a DataFrame or a record array.")
    statistic = "variances" if variance else "dispersions"
    flag = "highly_variable" if selected else "gene_subset"
    columns = ["means", statistic, f"{statistic}_norm", flag]
    for column in columns:
        if list(result.columns).count(column) != 1:
            raise ValueError(
                f"{context}: missing or ambiguous stored field {column!r}."
            )
    if result.empty:
        raise ValueError(f"{context}: at least one gene is required.")
    if not pd.api.types.is_bool_dtype(result[flag]) or result[flag].isna().any():
        raise TypeError(f"{context}: {flag} must contain nonmissing boolean values.")
    if result.index.hasnans:
        raise ValueError(f"{context}: gene labels must be nonmissing.")

    # Copy only the plotted metadata; no expression vector is needed.
    table = result[columns[:3]].reset_index(drop=True).copy()
    numeric_values(table, context=context)
    table = pd.concat([table, point_ids(result.index)], axis=1)
    table["_selected"] = result[flag].to_numpy(dtype=bool)
    table["_status"] = np.where(
        table["_selected"], "highly variable genes", "other genes"
    )
    return table, statistic


def _layers(adata: Any, layers: Any, use_raw: bool) -> tuple[Any, ...]:
    """Resolve x/y/color layers, retaining scatter's explicit raw/layer conflict."""
    values = [layers] * 3 if layers is None or isinstance(layers, str) else list(layers)
    if len(values) != 3 or any(
        value not in (None, "X") and value not in adata.layers for value in values
    ):
        raise ValueError(
            f"{_CONTEXT}: layers must name X or an existing layer, once or as an x/y/color triple."
        )
    if use_raw and values not in ([None] * 3, ["X"] * 3):
        raise ValueError(f"{_CONTEXT}: use_raw must be False when layers are supplied.")
    return tuple(None if value == "X" else value for value in values)


def _vector(
    adata: Any, key: str, axis: str, use_raw: bool, layer: str | None
) -> tuple[Any, str]:
    """Read one annotation or expression vector using public AnnData accessors."""
    metadata = adata.obs if axis == "obs" else adata.var
    if key in metadata:
        if list(metadata.columns).count(key) != 1:
            raise ValueError(f"{_CONTEXT}: {axis} annotation {key!r} is ambiguous.")
        return metadata[key].copy(), f"{axis}[{key!r}]"
    if axis == "obs":
        return _expression(adata, key, use_raw, layer, None)
    if (adata.obs_names == key).sum() != 1:
        raise ValueError(
            f"{_CONTEXT}: observation name {key!r} is missing or ambiguous."
        )
    require_resident_expression(adata, False, layer, context=_CONTEXT)
    source = "X" if layer is None else f"layers[{layer!r}]"
    return np.asarray(adata.var_vector(key, layer=layer)).copy(), source


def _orientation(adata: Any, x: Any, y: Any, keys: list[str], use_raw: bool) -> str:
    """Choose cells before genes, requiring all requested annotation keys to agree."""
    if not all(isinstance(key, str) for key in (x, y)):
        raise ValueError(
            f"{_CONTEXT}: supply a basis or both x and y annotation names."
        )
    for axis in ("obs", "var"):
        metadata = adata.obs if axis == "obs" else adata.var
        names = (
            (adata.raw.var_names if use_raw else adata.var_names)
            if axis == "obs"
            else adata.obs_names
        )
        if x not in metadata and x not in names or y not in metadata and y not in names:
            continue
        for key in keys:
            if key not in metadata and key not in names:
                try:
                    native_color(key, "color", context=_CONTEXT)
                except NotImplementedError:
                    break
        else:
            return axis
    raise ValueError(
        f"{_CONTEXT}: x, y and color keys must all belong to observations or all to variables."
    )


def _coordinates(
    adata: Any, basis: Any, components: Any
) -> tuple[pd.DataFrame, tuple[str, str]]:
    """Read scatter's exact X_ basis and one component pair, skipping diffusion's first column."""
    entries = "1,2" if components is None else components
    entries = entries.split(",") if isinstance(entries, str) else list(entries)
    try:
        dims = [int(value) - 1 for value in entries]
    except (TypeError, ValueError) as error:
        raise ValueError(f"{_CONTEXT}: components must be a one-based pair.") from error
    if len(dims) != 2 or min(dims) < 0:
        raise ValueError(f"{_CONTEXT}: components must be a one-based pair.")
    key = f"X_{basis}"
    if not isinstance(basis, str) or key not in adata.obsm:
        raise ValueError(
            f"{_CONTEXT}: missing obsm[{key!r}]; prepare coordinates explicitly with Scanpy."
        )
    actual = [value + (basis == "diffmap") for value in dims]
    coordinates = adata.obsm[key]
    if max(actual) >= coordinates.shape[1]:
        raise ValueError(f"{_CONTEXT}: components exceed the stored {key} columns.")
    if hasattr(coordinates, "to_numpy"):
        coordinates = coordinates.to_numpy()
    table = pd.DataFrame(
        {
            f"_coord_{i}": np.asarray(coordinates[:, d]).copy()
            for i, d in enumerate(actual)
        }
    )
    labels = _axis_labels(adata, basis, max(dims) + 1, False, 0)
    return table, (labels[dims[0]], labels[dims[1]])


def _palette_at(palette: Any, index: int) -> Any:
    """Select a per-panel palette while keeping a flat CSS list shared across panels."""
    if (
        isinstance(palette, Sequence)
        and not isinstance(palette, str)
        and palette
        and not isinstance(palette[0], str)
    ):
        if index >= len(palette):
            raise ValueError(
                f"{_CONTEXT}: provide one nested palette per categorical panel."
            )
        return palette[index]
    if index and isinstance(palette, Sequence) and not isinstance(palette, str):
        raise NotImplementedError(
            f"{_CONTEXT}: use nested palettes for multiple categorical panels; pinned Scanpy applies a flat palette to only the first."
        )
    return palette


def _category_paint(
    adata: Any,
    key: str,
    values: pd.Categorical,
    *,
    groups: Any,
    palette: Any,
    index: int,
) -> tuple[ColorData, np.ndarray]:
    """Return category colors and draw order for a scatter panel.

    Reuse shared palettes, then paint gray points before the requested groups.
    """
    import scanpy as sc

    if groups is None:
        visible = list(values.categories)
    elif isinstance(groups, str):
        visible = [groups]
    else:
        visible = list(groups)
    if any(value not in values.categories for value in visible):
        raise ValueError(f"{_CONTEXT}: groups contains an unknown category.")
    if groups is None:
        visible = [
            value for value in visible if value not in sc.settings.categories_to_ignore
        ]
    colors = categorical_colors(
        adata,
        key,
        values,
        palette=_palette_at(palette, index),
        groups=visible,
        mask=None,
        na_color="lightgrey",
        na_in_legend=False,
    )

    # Scanpy paints gray points first, then whole groups in the requested order.
    labels_in_order = tuple(str(value) for value in visible)
    colors = replace(colors, legend_values=labels_in_order)
    ranks = {value: i + 1 for i, value in enumerate(labels_in_order)}
    order = np.argsort([ranks.get(value, 0) for value in colors.values], kind="stable")
    return colors, order


def _panel_appearance(
    marker: Any, title: Any, count: int
) -> tuple[list[str], list[Any] | None]:
    """Return checked markers and optional titles for the requested panel count."""
    markers = [marker] * count if isinstance(marker, str) else list(marker)
    if len(markers) == 1:
        markers *= count
    if len(markers) != count or any(
        not isinstance(value, str) or value not in EMBEDDING_MARKERS
        for value in markers
    ):
        raise NotImplementedError(
            f"{_CONTEXT}: marker requires {tuple(EMBEDDING_MARKERS)}, once or per panel."
        )
    if isinstance(title, str):
        titles = [title]
    elif title is not None:
        titles = list(title)
    else:
        titles = None
    if titles is not None and len(titles) < count:
        raise ValueError(f"{_CONTEXT}: title needs one entry per color panel.")
    return markers, titles


def prepare_scatter(
    adata: Any,
    *,
    x: Any,
    y: Any,
    basis: Any,
    color: Any,
    use_raw: Any,
    layers: Any,
    groups: Any,
    components: Any,
    size: Any,
    marker: Any,
    palette: Any,
    cmap: Any,
    title: Any,
) -> PreparedEmbedding:
    """Return detached points and panel settings using scatter's distinct lookup rules."""
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError(f"{_CONTEXT}: expected AnnData.")
    if len(adata.uns.get("highlights", [])):
        raise NotImplementedError(
            f"{_CONTEXT}: stored highlights are not supported yet."
        )

    # Resolve observation versus gene lookup before reading values.
    requested_raw = use_raw
    use_raw = resolve_use_raw(adata, use_raw, None, context=_CONTEXT)
    if color is None:
        keys = ["grey"]
    elif isinstance(color, str):
        keys = [color]
    else:
        keys = list(color)
    if not keys or any(not isinstance(key, str) for key in keys):
        raise TypeError(
            f"{_CONTEXT}: color must contain annotation keys or CSS color strings."
        )
    axis = "obs" if basis is not None else _orientation(adata, x, y, keys, use_raw)

    # Scanpy drops raw when choosing variable orientation; no transpose is needed here.
    if axis == "var":
        use_raw = requested_raw is True
    sources = _layers(adata, layers, use_raw)
    metadata = adata.obs if axis == "obs" else adata.var
    names = adata.obs_names if axis == "obs" else adata.var_names
    if not len(names):
        raise ValueError(f"{_CONTEXT}: at least one point is required.")

    # Repeated axis/color requests share the same selected vector.
    extracted: dict[tuple[str, bool, str | None], tuple[Any, str]] = {}

    def read(
        key: str, layer: str | None, raw: bool = use_raw and axis == "obs"
    ) -> tuple[Any, str]:
        """Return a cached vector, ignoring source choices for metadata fields."""
        token = (key, raw, layer) if key not in metadata else (key, False, None)
        if token not in extracted:
            extracted[token] = _vector(adata, key, axis, raw, layer)
        return extracted[token]

    if basis is None:
        table = pd.DataFrame(
            {
                f"_coord_{i}": np.asarray(read(key, sources[i])[0])
                for i, key in enumerate((x, y))
            }
        )
        labels = (x, y)
    else:
        table, labels = _coordinates(adata, basis, components)
    if not np.isfinite(numeric_values(table, context=_CONTEXT)).all():
        raise ValueError(f"{_CONTEXT}: coordinates must be finite.")
    table = pd.concat([table, point_ids(names)], axis=1)

    # Validate per-panel appearance after the shared coordinates are ready.
    areas = _sizes(size, len(names))
    if areas.ndim:
        raise NotImplementedError(f"{_CONTEXT}: size currently supports a scalar only.")
    markers, titles = _panel_appearance(marker, title, len(keys))

    # Constant colors, categories and numeric values have different lookup rules.
    panels = []
    categorical_index = 0
    for index, key in enumerate(keys):
        expression_names = adata.var_names if axis == "obs" else adata.obs_names
        raw_gene = axis == "obs" and use_raw and key in adata.raw.var_names
        flat = key not in metadata and key not in expression_names and not raw_gene
        if flat:
            paint = native_color(key, "color", context=_CONTEXT)
            colors = ColorData(
                np.full(len(names), paint), (paint,), (paint,), None, (), True
            )
            source, categorical, order = "CSS color", None, np.arange(len(names))
        else:
            values, source = read(key, sources[2], raw_gene)
            categorical = (
                None
                if pd.api.types.is_bool_dtype(values.dtype)
                else _categorical(values)
            )
            if categorical is not None:
                colors, order = _category_paint(
                    adata,
                    key,
                    categorical,
                    groups=groups,
                    palette=palette,
                    index=categorical_index,
                )
                categorical_index += 1
            else:
                colors = continuous_colors(
                    values,
                    cmap=cmap,
                    mask=None,
                    vmin=None,
                    vmax=None,
                    index=index,
                    count=len(keys),
                    colorbar=True,
                )

                # Pinned scatter does not forward sort_order to its plotting helper.
                order = np.argsort(colors.values)
        panel_values(table, index, colors, order, areas)
        if titles is not None:
            heading = titles[index]
        elif flat:
            heading = ""
        else:
            heading = key.replace("_", " ")
        panels.append(
            Panel(
                key=None if flat else key,
                source=source,
                dimensions=(0, 1),
                categorical=colors.categorical,
                domain=colors.domain,
                palette=colors.palette,
                scheme=colors.scheme,
                legend_values=colors.legend_values,
                marker=markers[index],
                title=heading,
                show_missing=categorical is not None,
            )
        )
    return PreparedEmbedding(
        table,
        tuple(panels),
        axis_labels=labels,
        basis="scatter",
        row_label="Observation" if axis == "obs" else "Variable",
        show_ticks=basis is None,
    )
