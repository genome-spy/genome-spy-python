"""Detached observation columns for native linked summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import numeric_values
from genome_spy.integrations.scanpy._embedding.data import Panel, PreparedEmbedding
from genome_spy.integrations.scanpy._expression.grouped_data import (
    HeatmapData,
    heatmap_values,
)
from genome_spy.integrations.scanpy._style import (
    ColorData,
    _categorical,
    categorical_colors,
)


@dataclass(frozen=True, slots=True)
class Observation:
    field: str
    color: gs.Scale | None


def prepare_tracks(
    table: pd.DataFrame, fields: dict[str, str], genes: list[str], groups: list[str]
) -> HeatmapData:
    """Order detached marker columns by group and retain their original cell positions."""
    values = table[[fields[gene] for gene in genes]].set_axis(genes, axis=1)
    values.index = pd.CategoricalIndex(table["_group"], categories=groups, ordered=True)
    return heatmap_values(
        values, standard_scale=None, context="gsc.pl.EmbeddingSummary.add_tracks"
    )


def prepare_observations(
    adata: Any, keys: list[str], groupby: str, prepared: PreparedEmbedding
) -> dict[str, Observation]:
    """Snapshot requested obs columns, reusing the embedding's group colors/order."""
    result = {}
    colors: Panel | ColorData
    for i, key in enumerate([groupby, *keys]):
        if key == groupby:
            field, colors = "_color_0", prepared.panels[0]
        else:
            field = f"_obs_{i}"
            values = adata.obs[key].copy()
            categorical = _categorical(values, context="gsc.pl.EmbeddingSummary")
            if categorical is None:
                numeric_values(
                    values.to_frame(), context="gsc.pl.EmbeddingSummary: obs"
                )
                prepared.table[field] = values.to_numpy(copy=True)
                result[key] = Observation(field, None)
                continue
            colors = categorical_colors(
                adata,
                key,
                categorical,
                palette=None,
                groups=None,
                mask=None,
                na_color="lightgray",
                na_in_legend=True,
            )
            prepared.table[field] = [
                "NA" if pd.isna(value) else value for value in colors.values
            ]
        scale = gs.Scale(type="ordinal", domain=list(colors.domain), nice=False)
        scale = (
            scale.scheme(colors.scheme)
            if colors.scheme is not None
            else scale.range(list(colors.palette))
        )
        result[key] = Observation(field, scale)
    return result
