"""Stored density metadata mapped onto the shared embedding table and panels."""

from collections.abc import Mapping, Sequence
from numbers import Integral
from typing import Any

from anndata import AnnData
import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import numeric_values
from genome_spy.integrations.scanpy._embedding.data import (
    Panel,
    PreparedEmbedding,
    _axis_labels,
    _observations,
    _panel_inputs,
    embedding_key,
    panel_values,
    _sizes,
)
from genome_spy.integrations.scanpy._style import continuous_colors, draw_order


def prepare_density(
    adata: AnnData,
    basis: str,
    *,
    key: str | None,
    groupby: str | None,
    group: str | Sequence[str] | None,
    color_map: Any,
    bg_dotsize: float,
    fg_dotsize: float,
    vmin: Any,
    vmax: Any,
    vcenter: Any,
    title: str | None,
    marker: Any,
    sort_order: bool,
    obs_id: str | None,
    colorbar_loc: str | None,
) -> PreparedEmbedding:
    """Return stored density panels with gray background cells; never run KDE or modify AnnData."""
    context = "gsc.pl.embedding_density"
    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: adata must be AnnData.")
    if not adata.n_obs or not adata.obs.columns.is_unique:
        raise ValueError(f"{context}: require cells and unique obs column names.")
    coordinate_key = f"X_{basis}"
    if coordinate_key not in adata.obsm:
        raise ValueError(
            f"{context}: missing obsm[{coordinate_key!r}]; compute the embedding explicitly first."
        )
    coordinate_key = embedding_key(adata, basis, context=context)
    # The pinned plotting function always starts its default key with umap_density.
    key = ("umap_density" if key is None else key) + (
        f"_{groupby}" if groupby is not None else ""
    )
    params = adata.uns.get(f"{key}_params")
    if key not in adata.obs or not isinstance(params, Mapping):
        raise ValueError(
            f"{context}: stored obs[{key!r}] and uns[{key + '_params'!r}] are required; run sc.tl.embedding_density explicitly first."
        )
    if "covariate" not in params or "components" not in params:
        raise ValueError(
            f"{context}: stored density params require covariate and components."
        )
    components = params["components"]
    if (
        not isinstance(components, (list, tuple, np.ndarray))
        or np.shape(components) != (2,)
        or any(isinstance(c, bool) or not isinstance(c, Integral) for c in components)
    ):
        raise ValueError(
            f"{context}: stored components must contain two one-based integers."
        )
    pair = tuple(int(c) - 1 for c in components)
    # Check coordinate/marker choices through the same helper as ordinary embeddings.
    inputs = _panel_inputs(adata.obsm[coordinate_key].shape[1], key, None, pair, marker)
    if len(inputs) != 1:
        raise NotImplementedError(
            f"{context}: provide one marker shared by all groups."
        )
    _, pair, marker = inputs[0]
    covariate = params["covariate"]
    labels = None
    if covariate is not None:
        if (
            not isinstance(covariate, str)
            or covariate not in adata.obs
            or not isinstance(adata.obs[covariate].dtype, pd.CategoricalDtype)
        ):
            raise ValueError(
                f"{context}: stored covariate must name a categorical obs column."
            )
        labels = adata.obs[covariate]
    if isinstance(group, str) and group == "all":
        groups = [None] if labels is None else list(labels.cat.categories)
    elif group is None:
        if labels is not None:
            raise ValueError(
                f"{context}: group=None requires an ungrouped density result."
            )
        groups = [None]
    else:
        if labels is None:
            raise ValueError(
                f"{context}: explicit groups require grouped density results."
            )
        groups = [group] if isinstance(group, str) else list(group)
    if not groups or (
        labels is not None
        and any(
            not isinstance(g, str) or g not in labels.cat.categories for g in groups
        )
    ):
        raise ValueError(
            f"{context}: select nonempty string groups from the stored covariate categories."
        )
    density = numeric_values(adata.obs[[key]], context=context).ravel()
    if not np.isfinite(density).all() or ((density < 0) | (density > 1)).any():
        raise ValueError(
            f"{context}: stored densities must be finite values in [0, 1]."
        )
    table = _observations(adata, coordinate_key, [pair], obs_id)
    panels = []
    for index, name in enumerate(groups):
        foreground = (
            np.ones(adata.n_obs, dtype=bool)
            if labels is None
            else labels.eq(name).to_numpy()
        )
        plotted = np.where(foreground, density, -1.0)
        colors = continuous_colors(
            plotted,
            cmap=color_map,
            mask=None,
            vmin=vmin,
            vmax=vmax,
            vcenter=vcenter,
            index=0,
            count=1,
            colorbar=colorbar_loc is not None,
            sort_order=sort_order,
        )
        # Native color layers preserve overlap order only when their ranges are sorted.
        low, high = colors.domain[0], colors.domain[-1]
        if (
            not sort_order
            and sum(
                (
                    (plotted < low).any(),
                    ((low <= plotted) & (plotted <= high)).any(),
                    (plotted > high).any(),
                )
            )
            > 1
        ):
            raise NotImplementedError(
                f"{context}: sort_order=False with under/over colors cannot preserve point overlap order in native layers."
            )
        sizes = _sizes(np.where(foreground, fg_dotsize, bg_dotsize), adata.n_obs)
        panel_values(
            table,
            index,
            colors,
            draw_order(plotted, categorical=False, sort=sort_order),
            sizes,
        )
        # Hover reports the stored density, while color retains Scanpy's background sentinel.
        table[f"_value_{index}"] = density
        panels.append(
            Panel(
                key,
                f"obs[{key!r}]",
                pair,
                False,
                colors.domain,
                colors.palette,
                colors.scheme,
                (),
                marker,
                title if title is not None else name,
                color_extremes=("lightgray", "black"),
            )
        )
    axis_labels = _axis_labels(
        adata, basis, adata.obsm[coordinate_key].shape[1], False, max(pair) + 1
    )
    return PreparedEmbedding(table, tuple(panels), axis_labels, basis)
