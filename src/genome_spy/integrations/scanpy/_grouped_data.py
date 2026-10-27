"""Detached grouped expression and statistics, independent of chart construction."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from collections import Counter
from dataclasses import dataclass
from numbers import Integral
from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import (
    number,
    numeric_values,
    require_resident_expression,
    resolve_use_raw,
)

if TYPE_CHECKING:
    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData


@dataclass(frozen=True, slots=True)
class FeatureGroup:
    label: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class GroupedExpression:
    values: pd.DataFrame
    feature_groups: tuple[FeatureGroup, ...]
    counts: pd.Series


MAX_HEATMAP_VALUES = 250_000


@dataclass(frozen=True, slots=True)
class HeatmapData:
    values: pd.DataFrame
    observation_positions: np.ndarray
    intervals: pd.DataFrame


def _feature_slots(
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    labels: Sequence[str] | None,
    positions: Sequence[tuple[int, int]] | None,
) -> tuple[list[str], tuple[FeatureGroup, ...]]:
    """Turn gene names or a marker dictionary into ordered names and bracket spans.

    Keep repeated names so each requested occurrence has its own plot position.
    """
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
    """Return ordered groups from the table's groupby columns.

    Combine multiple labels without creating groups that have no cells.
    """
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
    value_limit: int | None = None,
    read_values: bool = True,
    observation_positions: np.ndarray | None = None,
) -> GroupedExpression:
    """Return requested AnnData values in a separate grouped table with marker brackets.

    Preserve cell order and repeated genes; value_limit rejects oversized requests
    before expression access, without changing AnnData. read_values=False returns
    only category/slot metadata after zero-row feature validation.
    observation_positions selects/reorders rows after column access, before validation.
    """
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
    # Stop oversized heatmaps before selecting or copying expression columns.
    if value_limit is not None and adata.n_obs * len(names) > value_limit:
        raise ValueError(
            f"gsc.pl.heatmap: at most {value_limit:,} cell–gene values are supported; "
            "subset cells or genes explicitly before plotting. No values were loaded."
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
    source = adata if read_values else adata[:0]
    frame = obs_df(
        source,
        keys=list(dict.fromkeys([*columns, *names])),
        use_raw=use_raw,
        layer=layer,
        gene_symbols=gene_symbols,
    )
    if not read_values:
        # Zero rows validate feature lookup; only group annotations need cell rows.
        frame = obs_df(adata, keys=columns, use_raw=use_raw)
    if observation_positions is not None:
        frame = frame.iloc[observation_positions]

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

    counts = pd.CategoricalIndex(groups).value_counts(sort=False)

    # Repeated genes keep separate positions in the final plot.
    if not read_values:
        index = pd.CategoricalIndex(
            [], categories=groups.categories, name="_".join(keys)
        )
        return GroupedExpression(
            pd.DataFrame(index=index, columns=names, dtype=float),
            feature_groups,
            counts,
        )
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
    return GroupedExpression(table, feature_groups, counts)


def _cutoff(value: float) -> None:
    """Check an expression cutoff; raise for invalid values, allowing negatives."""
    number(
        value, "expression_cutoff", context="Grouped plotting", minimum=-float("inf")
    )


def group_means(
    values: pd.DataFrame, *, expression_cutoff: float | None = None
) -> pd.DataFrame:
    """Return group means from cell values indexed by group, skipping missing data.

    With a cutoff, average only expressing cells and fill empty means with zero,
    matching Scanpy's mean_only_expressed behavior.
    """
    if expression_cutoff is not None:
        _cutoff(expression_cutoff)
        values = values.where(values > expression_cutoff)
    # Match Scanpy's plotting means, which skip missing values.
    means = values.groupby(level=0, observed=True).mean()
    return means if expression_cutoff is None else means.fillna(0)


def expression_fractions(
    values: pd.DataFrame, *, expression_cutoff: float = 0.0
) -> pd.DataFrame:
    """Return each group's fraction of cell values strictly above the cutoff.

    Use Scanpy's comparison and count rules so zeros and missing values contribute
    to the denominator in the same way.
    """
    _cutoff(expression_cutoff)
    # Count values strictly above the cutoff, including zeros in the denominator.
    expressed = values > expression_cutoff
    groups = expressed.groupby(level=0, observed=True)
    return groups.sum() / groups.count()


def scale_values(
    values: pd.DataFrame, standard_scale: Literal["var", "group"] | None
) -> pd.DataFrame:
    """Return table values scaled to 0–1 by column or row, or copied when off.

    Use 'var' for columns and 'group' for rows; constant ranges become zero.
    """
    if standard_scale is None:
        return values.copy()
    if standard_scale not in ("var", "group"):
        raise ValueError(
            "Grouped plotting: standard_scale must be 'var', 'group', or None."
        )
    # Plot scaling maps each range to 0–1; sc.pp.scale would change the meaning.
    axis = 0 if standard_scale == "var" else 1
    shifted = values.sub(values.min(axis=axis), axis=1 - axis)
    return shifted.div(shifted.max(axis=axis), axis=1 - axis).fillna(0)


def matrixplot_statistics(
    values: pd.DataFrame,
    *,
    standard_scale: Literal["var", "group"] | None,
    values_df: pd.DataFrame | None,
    categories_order: Sequence[str] | None,
) -> pd.DataFrame:
    """Return group-by-feature means from cell values or supplied summaries.

    Scale computed means once and preserve supplied values. The builder owns
    display transposition.
    """
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
        return means

    # Only observed groups have means; empty categories need an explicit cleanup.
    means = group_means(values)
    if means.empty:
        raise ValueError("gsc.pl.matrixplot: no observed groups to plot.")
    if len(means) != len(values.index.categories):
        raise ValueError(
            "gsc.pl.matrixplot: unused categories have no statistics; "
            "remove unused categories explicitly before plotting."
        )
    return scale_values(means, standard_scale)


def dotplot_summaries(
    values: pd.DataFrame,
    *,
    expression_cutoff: float,
    mean_only_expressed: bool,
    standard_scale: Literal["var", "group"] | None,
    dot_color_df: pd.DataFrame | None,
    dot_size_df: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return detached color summaries and fractions in their original orientation.

    Honor supplied values, expressed-only means and Scanpy's first scaling pass;
    rendering applies the second pass after ordering and optional transposition.
    """
    # Dot sizes always describe the cells, even when colors are supplied.
    fractions = expression_fractions(values, expression_cutoff=expression_cutoff)
    if fractions.empty:
        raise ValueError("gsc.pl.dotplot: no observed groups to plot.")
    if len(fractions) != len(values.index.categories):
        raise ValueError(
            "gsc.pl.dotplot: unused categories have no statistics; "
            "remove unused categories explicitly before plotting."
        )

    if dot_size_df is not None:
        if not isinstance(dot_size_df, pd.DataFrame):
            raise TypeError("gsc.pl.DotPlot: dot_size_df must be a pandas DataFrame.")
        if (
            not dot_size_df.index.is_unique
            or set(dot_size_df.index) != set(fractions.index)
            or list(dot_size_df.columns) != list(fractions.columns)
        ):
            raise ValueError(
                "gsc.pl.DotPlot: dot_size_df needs exactly the plotted groups and feature slots."
            )
        fractions = dot_size_df.loc[fractions.index].copy()
        sizes = numeric_values(fractions, context="gsc.pl.DotPlot: dot_size_df")
        if not np.isfinite(sizes).all() or (sizes < 0).any() or (sizes > 1).any():
            raise ValueError(
                "gsc.pl.DotPlot: dot_size_df fractions must be finite and between zero and one."
            )

    # Supplied colors skip the first scaling pass, as in Scanpy.
    if dot_color_df is None:
        colors = group_means(
            values,
            expression_cutoff=expression_cutoff if mean_only_expressed else None,
        )
        colors = scale_values(colors, standard_scale)
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
    return colors, fractions


def heatmap_values(
    values: pd.DataFrame,
    *,
    standard_scale: Literal["var", "obs"] | None,
    category_order: Sequence[Any] | None = None,
    feature_order: Sequence[int] | None = None,
    context: str = "gsc.pl.heatmap",
) -> HeatmapData:
    """Return ordered cell values, original row positions and group spans.

    Scale before sorting so every annotation can follow one explicit permutation.
    """
    if values.index.isna().any():
        raise ValueError(
            f"{context}: missing groups are unsupported; label or filter them explicitly."
        )
    counts = values.index.value_counts(sort=False)
    if (counts == 0).any():
        raise ValueError(
            f"{context}: remove unused categories explicitly before plotting."
        )

    # Heatmap calls row scaling 'obs'; summary plots call the same operation 'group'.
    scale = "group" if standard_scale == "obs" else standard_scale
    scaled = scale_values(values, scale)
    # Scanpy scales across all requested genes before marker blocks can omit any.
    if feature_order is not None:
        scaled = scaled.iloc[:, list(feature_order)]
    if scaled.size > MAX_HEATMAP_VALUES:
        raise ValueError(
            f"{context}: reordered marker blocks exceed the 250,000-value limit; subset markers explicitly."
        )
    if category_order is not None:
        scaled.index = scaled.index.reorder_categories(
            list(category_order), ordered=True
        )
    if len(counts) > 1:
        positions = (
            pd.Series(np.arange(len(values)), index=scaled.index)
            .sort_index()
            .to_numpy()
        )
    else:
        positions = np.arange(len(values))
    scaled = scaled.iloc[positions]

    # Keep labels and tree leaves at the same center of each cell block.
    counts = scaled.index.value_counts(sort=False)
    stops = counts.cumsum().to_numpy()
    starts = stops - counts.to_numpy()
    intervals = pd.DataFrame(
        {
            "label": [str(label) for label in counts.index],
            "start": starts,
            "stop": stops,
            "center": (starts + stops - 1) / 2,
        }
    )
    if not intervals["label"].is_unique:
        raise ValueError(f"{context}: group labels collide when converted to strings.")
    return HeatmapData(scaled, positions, intervals)


def ordered_cell_expression(
    adata: Any,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str | Sequence[str],
    *,
    dendrogram: bool | str,
    standard_scale: Literal["var", "obs"] | None = None,
    context: str,
    **options: Any,
) -> tuple[HeatmapData, tuple[FeatureGroup, ...], DendrogramData | None]:
    """Return cell values, marker spans and a tree in one shared display order.

    Read selected genes once; keep original row positions for cell identities.
    """
    from genome_spy.integrations.scanpy._dendrogram_data import (
        prepare_dendrogram,
        reorder_features,
    )

    selected = grouped_expression(
        adata, var_names, groupby, value_limit=MAX_HEATMAP_VALUES, **options
    )
    tree = None
    # Cell plots attach two-group trees too, unlike grouped summary plots.
    if dendrogram is not False and len(selected.counts) > 1:
        tree = prepare_dendrogram(
            adata, groupby, dendrogram if isinstance(dendrogram, str) else None
        )
    groups, slots = selected.feature_groups, None
    if tree is not None:
        groups, slots = reorder_features(tree, groups, selected.values.shape[1])
    prepared = heatmap_values(
        selected.values,
        standard_scale=standard_scale,
        category_order=tree.order if tree else None,
        feature_order=slots,
        context=context,
    )
    return prepared, groups, tree
