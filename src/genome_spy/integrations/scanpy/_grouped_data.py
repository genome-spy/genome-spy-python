"""Detached grouped expression and statistics, independent of chart construction."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from collections import Counter
from dataclasses import dataclass
from numbers import Integral
from typing import Any, Literal

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import (
    number,
    numeric_values,
    require_resident_expression,
    resolve_use_raw,
)


@dataclass(frozen=True, slots=True)
class FeatureGroup:
    label: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class GroupedExpression:
    values: pd.DataFrame
    feature_groups: tuple[FeatureGroup, ...]


def _feature_slots(
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    labels: Sequence[str] | None,
    positions: Sequence[tuple[int, int]] | None,
) -> tuple[list[str], tuple[FeatureGroup, ...]]:
    groups = []
    names: list[str]
    # A marker dictionary sets both gene order and bracket positions.
    if isinstance(var_names, Mapping):
        if labels is not None or positions is not None:
            raise TypeError(
                "Grouped plotting: mapping var_names already defines brackets."
            )
        names = []
        for label, entries in var_names.items():
            entries = [entries] if isinstance(entries, str) else list(entries)
            if not entries:
                raise ValueError(
                    "Grouped plotting: each feature group must be nonempty."
                )
            groups.append(
                FeatureGroup(label, len(names), len(names) + len(entries) - 1)
            )
            names.extend(entries)
    else:
        names = [var_names] if isinstance(var_names, str) else list(var_names)
        if (labels is None) != (positions is None):
            raise ValueError(
                "Grouped plotting: provide both bracket labels and positions."
            )
        if labels is not None and positions is not None:
            if len(labels) != len(positions):
                raise ValueError(
                    "Grouped plotting: bracket labels and positions differ in length."
                )
            if any(len(pair) != 2 for pair in positions):
                raise ValueError(
                    "Grouped plotting: bracket positions need (start, end) pairs."
                )
            groups = [
                FeatureGroup(label, *pair) for label, pair in zip(labels, positions)
            ]
    if not names or not all(isinstance(name, str) for name in names):
        raise ValueError(
            "Grouped plotting: var_names must contain string feature keys."
        )
    for group in groups:
        if (
            not isinstance(group.label, str)
            or any(
                isinstance(x, bool) or not isinstance(x, Integral)
                for x in (group.start, group.end)
            )
            or not 0 <= group.start <= group.end < len(names)
        ):
            raise ValueError(
                "Grouped plotting: brackets need string labels and valid inclusive slot positions."
            )
    return names, tuple(groups)


def _categories(frame: pd.DataFrame, keys: list[str]) -> pd.Categorical:
    if len(keys) == 1:
        values = frame[keys[0]]
        return pd.Categorical(values)
    if any(not isinstance(frame[key].dtype, pd.CategoricalDtype) for key in keys):
        raise TypeError(
            "Grouped plotting: multiple groupby keys require categorical string annotations."
        )
    if frame[keys].isna().any().any():
        raise ValueError(
            "Grouped plotting: missing multi-key groups are unsupported; filter or label them explicitly."
        )
    try:
        joined = frame[keys].astype(object).agg("_".join, axis=1)
    except TypeError as error:
        raise TypeError(
            "Grouped plotting: multiple groupby keys require string categories."
        ) from error
    # Keep category order without inventing groups that have no cells.
    combinations = frame[keys].drop_duplicates().sort_values(keys)
    order = combinations.astype(object).agg("_".join, axis=1)
    if not order.is_unique:
        raise ValueError("Grouped plotting: group labels collide when joined with '_'.")
    return pd.Categorical(joined, categories=order)


def grouped_expression(
    adata: Any,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str | Sequence[str],
    *,
    use_raw: bool | None = None,
    layer: str | None = None,
    gene_symbols: str | None = None,
    log: bool = False,
    num_categories: int = 7,
    categories_order: Sequence[Any] | None = None,
    var_group_labels: Sequence[str] | None = None,
    var_group_positions: Sequence[tuple[int, int]] | None = None,
) -> GroupedExpression:
    """Read selected values once; preserve observation order and repeated slots."""
    from anndata import AnnData
    from scanpy.get import obs_df

    if not isinstance(adata, AnnData):
        raise TypeError("Grouped plotting: expected AnnData.")
    if adata.n_obs == 0:
        raise ValueError("Grouped plotting: at least one observation is required.")
    if not isinstance(log, bool):
        raise TypeError("Grouped plotting: log must be True or False.")
    names, feature_groups = _feature_slots(
        var_names, var_group_labels, var_group_positions
    )
    keys = [groupby] if isinstance(groupby, str) else list(groupby)
    if (
        not keys
        or not all(isinstance(key, str) for key in keys)
        or len(set(keys)) != len(keys)
    ):
        raise ValueError(
            "Grouped plotting: groupby must contain distinct observation keys."
        )
    for key in keys:
        if key == adata.obs.index.name and key in adata.obs:
            raise ValueError(
                f"Grouped plotting: groupby {key!r} is both an index name and a column."
            )
        if key not in adata.obs and key != adata.obs.index.name:
            raise ValueError(
                f"Grouped plotting: groupby {key!r} is missing from observations."
            )

    # Check expression storage only when the requested values include genes.
    use_raw = resolve_use_raw(adata, use_raw, layer, context="Grouped plotting")
    if any(name not in adata.obs for name in names):
        from scipy.sparse import sparray

        matrix = require_resident_expression(
            adata, use_raw, layer, context="Grouped plotting"
        )
        if isinstance(matrix, sparray):
            raise NotImplementedError(
                "Grouped plotting: Scanpy 1.11.5 obs_df does not support sparse arrays; "
                "use an in-memory CSR/CSC matrix for the selected representation."
            )

    # Read each requested column once; restore repeated genes below.
    columns = [key for key in keys if key != adata.obs.index.name]
    frame = obs_df(
        adata,
        keys=list(dict.fromkeys([*columns, *names])),
        use_raw=use_raw,
        layer=layer,
        gene_symbols=gene_symbols,
    )

    # Convert strings on this separate table so AnnData stays unchanged.
    adata.strings_to_categoricals(frame)
    if adata.obs.index.name in keys:
        frame = frame.reset_index()

    # Scanpy groups numeric annotations into bins rather than one group per value.
    if len(keys) == 1 and pd.api.types.is_numeric_dtype(frame[keys[0]]):
        if (
            isinstance(num_categories, bool)
            or not isinstance(num_categories, Integral)
            or num_categories < 1
        ):
            raise ValueError(
                "Grouped plotting: num_categories must be a positive integer."
            )
        groups = pd.Categorical(pd.cut(frame[keys[0]], num_categories))
    else:
        groups = _categories(frame, keys)
    if categories_order is not None:
        groups = groups.reorder_categories(list(categories_order))

    # Repeated genes keep separate positions in the final plot.
    table = frame.loc[:, names].copy()
    table.index = pd.CategoricalIndex(groups, name="_".join(keys))
    numeric = numeric_values(table, context="Grouped plotting: expression")

    # Scanpy applies log1p to cell values before computing group means.
    if log:
        if np.any(numeric <= -1):
            raise ValueError(
                "Grouped plotting: log=True requires values greater than -1."
            )
        table = np.log1p(table)
    return GroupedExpression(table, feature_groups)


def _cutoff(value: float) -> None:
    number(
        value, "expression_cutoff", context="Grouped plotting", minimum=-float("inf")
    )


def group_means(
    values: pd.DataFrame, *, expression_cutoff: float | None = None
) -> pd.DataFrame:
    """Average observed groups; optionally include only values above a cutoff."""
    if expression_cutoff is not None:
        _cutoff(expression_cutoff)
        values = values.where(values > expression_cutoff)
    # Match Scanpy's plotting means, which skip missing values.
    means = values.groupby(level=0, observed=True).mean()
    return means if expression_cutoff is None else means.fillna(0)


def expression_fractions(
    values: pd.DataFrame, *, expression_cutoff: float = 0.0
) -> pd.DataFrame:
    """Use Scanpy's comparison/count denominator, including implicit zeros."""
    _cutoff(expression_cutoff)
    # Count values strictly above the cutoff, including zeros in the denominator.
    expressed = values > expression_cutoff
    groups = expressed.groupby(level=0, observed=True)
    return groups.sum() / groups.count()


def scale_means(
    means: pd.DataFrame, standard_scale: Literal["var", "group"] | None
) -> pd.DataFrame:
    """Min–max scale aggregated means; zero-range entries become zero."""
    if standard_scale is None:
        return means.copy()
    if standard_scale not in ("var", "group"):
        raise ValueError(
            "Grouped plotting: standard_scale must be 'var', 'group', or None."
        )
    # Plot scaling maps each range to 0–1; sc.pp.scale would change the meaning.
    axis = 0 if standard_scale == "var" else 1
    shifted = means.sub(means.min(axis=axis), axis=1 - axis)
    return shifted.div(shifted.max(axis=axis), axis=1 - axis).fillna(0)


def matrixplot_statistics(
    values: pd.DataFrame,
    *,
    standard_scale: Literal["var", "group"] | None,
    values_df: pd.DataFrame | None,
    categories_order: Sequence[str] | None,
    swap_axes: bool,
) -> pd.DataFrame:
    """Scale computed means once; supplied tables retain their values and order."""
    # Supplied means replace computed means and must not be scaled again.
    if values_df is not None:
        if not isinstance(values_df, pd.DataFrame):
            raise TypeError("gsc.pl.matrixplot: values_df must be a pandas DataFrame.")
        if (
            not values_df.index.is_unique
            or set(values_df.index) != set(values.index.categories)
            or Counter(values_df.columns) != Counter(values.columns)
        ):
            raise ValueError(
                "gsc.pl.matrixplot: values_df needs exactly the plotted group/feature "
                "labels and repeated feature slots, with unique group labels."
            )
        means = values_df.copy()
        numeric_values(means, context="gsc.pl.matrixplot: values_df")
        if categories_order is not None:
            means = means.loc[list(categories_order)]
        return means.T if swap_axes else means

    # Only observed groups have means; empty categories need an explicit cleanup.
    means = group_means(values)
    if means.empty:
        raise ValueError("gsc.pl.matrixplot: no observed groups to plot.")
    if len(means) != len(values.index.categories):
        raise ValueError(
            "gsc.pl.matrixplot: unused categories have no statistics; "
            "remove unused categories explicitly before plotting."
        )
    means = scale_means(means, standard_scale)
    return means.T if swap_axes else means


def dotplot_statistics(
    values: pd.DataFrame,
    *,
    expression_cutoff: float,
    mean_only_expressed: bool,
    standard_scale: Literal["var", "group"] | None,
    dot_color_df: pd.DataFrame | None,
    swap_axes: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return displayed colors/fractions, including the pinned render-time scaling."""
    # Dot sizes always describe the cells, even when colors are supplied.
    fractions = expression_fractions(values, expression_cutoff=expression_cutoff)
    if fractions.empty:
        raise ValueError("gsc.pl.dotplot: no observed groups to plot.")
    if len(fractions) != len(values.index.categories):
        raise ValueError(
            "gsc.pl.dotplot: unused categories have no statistics; "
            "remove unused categories explicitly before plotting."
        )

    # Supplied colors skip the first scaling pass, as in Scanpy.
    if dot_color_df is None:
        colors = group_means(
            values,
            expression_cutoff=expression_cutoff if mean_only_expressed else None,
        )
        colors = scale_means(colors, standard_scale)
    else:
        if not isinstance(dot_color_df, pd.DataFrame):
            raise TypeError("gsc.pl.dotplot: dot_color_df must be a pandas DataFrame.")
        if not dot_color_df.index.is_unique or (
            set(dot_color_df.index) != set(fractions.index)
            or set(dot_color_df.columns) != set(fractions.columns)
        ):
            raise ValueError(
                "gsc.pl.dotplot: dot_color_df needs exactly the plotted group/feature labels."
            )
        # Repeated genes share the first supplied column, as in Scanpy 1.11.5.
        unique = dot_color_df.loc[:, ~dot_color_df.columns.duplicated()]
        colors = unique.loc[fractions.index, fractions.columns].copy()
        numeric_values(colors, context="gsc.pl.dotplot: dot_color_df")
    if swap_axes:
        colors, fractions = colors.T, fractions.T
    # Scanpy also scales the displayed table after a possible transpose.
    return scale_means(colors, standard_scale), fractions
