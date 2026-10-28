"""Read stored gene rankings and select labels without running analysis."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from numbers import Integral
from typing import Any

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import number, numeric_values


@dataclass(frozen=True, slots=True)
class RankPanel:
    """Labels, scores and bounds for one detached ranking panel."""

    title: str
    values: pd.DataFrame
    x_domain: tuple[float, float]
    y_domain: tuple[float, float]
    hide_ticks: bool = False


def _count(value: Any, name: str, *, context: str, negative: bool = False) -> int:
    """Return a nonzero integer count, allowing tail selection when requested."""
    if (
        isinstance(value, bool)
        or not isinstance(value, Integral)
        or value == 0
        or (value < 0 and not negative)
    ):
        raise ValueError(
            f"{context}: {name} must be a {'nonzero' if negative else 'positive'} integer."
        )
    return int(value)


def _check_ranking_field(result: Mapping[str, Any], name: str, *, context: str) -> None:
    """Check a stored field against the ranking's gene-name rows and groups."""
    field = result.get(name)
    names = result["names"]
    if (
        not isinstance(field, np.ndarray)
        or field.shape != names.shape
        or set(field.dtype.names or ()) != set(names.dtype.names)
    ):
        raise ValueError(
            f"{context}: stored {name} must match the ranking names and groups."
        )


def stored_ranking(
    adata: Any, key: str | None, groups: Any, *, context: str
) -> tuple[Mapping[str, Any], list[str]]:
    """Return a validated stored result and requested groups, preserving their order."""
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    key = "rank_genes_groups" if key is None else key
    if not isinstance(key, str) or not key or key not in adata.uns:
        raise ValueError(
            f"{context}: stored ranking {key!r} is missing; run sc.tl.rank_genes_groups explicitly first."
        )
    result = adata.uns[key]
    if not isinstance(result, Mapping) or not isinstance(result.get("params"), Mapping):
        raise ValueError(f"{context}: ranking {key!r} needs stored params.")
    params = result["params"]
    for name in ("groupby", "method", "reference"):
        if not isinstance(params.get(name), str) or not params[name]:
            raise ValueError(f"{context}: ranking params need a nonempty {name!r}.")
    # Packaged Scanpy data also stores this flag as a one-element boolean array.
    source = np.asarray(params.get("use_raw"))
    if source.size != 1 or source.dtype.kind != "b":
        raise ValueError(f"{context}: ranking params need boolean use_raw.")
    layer = params.get("layer")
    if layer is not None and (not isinstance(layer, str) or bool(source.item())):
        raise ValueError(
            f"{context}: ranking params contain an invalid layer/use_raw combination."
        )
    names = result.get("names")
    if (
        not isinstance(names, np.ndarray)
        or names.ndim != 1
        or not names.size
        or not names.dtype.names
    ):
        raise ValueError(
            f"{context}: ranking names must be a nonempty structured array."
        )
    _check_ranking_field(result, "scores", context=context)
    if groups is None:
        chosen = list(names.dtype.names)
    else:
        chosen = [groups] if isinstance(groups, str) else list(groups)
    if (
        not chosen
        or any(not isinstance(g, str) for g in chosen)
        or len(set(chosen)) != len(chosen)
    ):
        raise ValueError(f"{context}: groups must contain distinct group names.")
    missing = set(chosen) - set(names.dtype.names)
    if missing:
        raise ValueError(
            f"{context}: groups are missing from the stored ranking: {sorted(missing)}."
        )
    return result, chosen


def _ranking_table(
    adata: Any,
    result: Mapping[str, Any],
    chosen: list[str],
    *,
    key: str | None,
    gene_symbols: str | None,
    min_logfoldchange: float | None,
    context: str,
) -> pd.DataFrame:
    """Read detached ranking rows through Scanpy, checking its required fields first."""
    from scanpy.get import rank_genes_groups_df

    method = result["params"]["method"]
    if method not in {"logreg", "t-test", "t-test_overestim_var", "wilcoxon"}:
        raise NotImplementedError(
            f"{context}: unsupported stored ranking method {method!r}."
        )
    if min_logfoldchange is not None:
        number(
            min_logfoldchange,
            "min_logfoldchange",
            minimum=-float("inf"),
            context=context,
        )
        if method == "logreg":
            raise ValueError(
                f"{context}: min_logfoldchange needs stored logfoldchanges; logreg results have none."
            )
    fields = [] if method == "logreg" else ["logfoldchanges", "pvals", "pvals_adj"]
    for name in fields:
        _check_ranking_field(result, name, context=context)
    table = rank_genes_groups_df(
        adata,
        chosen,
        key=key or "rank_genes_groups",
        gene_symbols=gene_symbols,
        log2fc_min=min_logfoldchange,
    )
    # Scanpy omits the group column when returning a single rank list.
    if len(chosen) == 1:
        table["group"] = chosen[0]
    return table


def ranked_features(
    adata: Any,
    groups: Any,
    *,
    key: str | None,
    n_genes: int | None,
    groupby: str | None,
    var_names: Any,
    gene_symbols: str | None,
    min_logfoldchange: float | None,
    context: str,
    table: pd.DataFrame | None = None,
) -> tuple[Any, str]:
    """Return marker slots and grouping key using Scanpy's public result getter."""
    if var_names is not None and n_genes is not None:
        raise ValueError(f"{context}: n_genes and var_names are mutually exclusive.")
    result, chosen = stored_ranking(adata, key, groups, context=context)
    grouping = result["params"]["groupby"] if groupby is None else groupby
    if var_names is not None:
        return var_names, grouping
    count = _count(
        10 if n_genes is None else n_genes, "n_genes", context=context, negative=True
    )
    if table is None:
        table = _ranking_table(
            adata,
            result,
            chosen,
            key=key,
            gene_symbols=gene_symbols,
            min_logfoldchange=min_logfoldchange,
            context=context,
        )
    else:
        # Filter the shared table only for marker selection, preserving color pairs.
        table = table.loc[table["group"].isin(chosen)]
        table = table.assign(group=pd.Categorical(table["group"], categories=chosen))
        if min_logfoldchange is not None:
            number(
                min_logfoldchange,
                "min_logfoldchange",
                minimum=-float("inf"),
                context=context,
            )
            if "logfoldchanges" not in table:
                raise ValueError(
                    f"{context}: min_logfoldchange needs stored logfoldchanges; logreg results have none."
                )
            table = table.loc[table["logfoldchanges"] > min_logfoldchange]
        table = table.sort_values("group", kind="stable")
    markers = {}
    for group, rows in table.groupby("group", sort=False, observed=True):
        labels = (
            rows["names" if gene_symbols is None else gene_symbols].dropna().tolist()
        )
        if not all(isinstance(label, str) for label in labels):
            raise ValueError(
                f"{context}: ranked gene labels must be strings or missing."
            )
        # Scanpy selects the tail in its stored order, without reversing it.
        selected = labels[:count] if count > 0 else labels[count:]
        if selected:
            markers[group] = selected
    if not markers:
        raise ValueError(f"{context}: no ranked genes remain after filtering.")
    return markers, grouping


def ranked_statistic(
    adata: Any,
    markers: Any,
    metric: str,
    *,
    key: str | None,
    gene_symbols: str | None,
    context: str,
    table: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Return stored statistic colors for every group and requested gene slot."""
    from genome_spy.integrations.scanpy._expression.grouped_data import _feature_slots

    options = {
        "scores",
        "logfoldchanges",
        "pvals",
        "pvals_adj",
        "log10_pvals",
        "log10_pvals_adj",
    }
    if not isinstance(metric, str) or metric not in options:
        raise ValueError(f"{context}: values_to_plot must be one of {sorted(options)}.")
    result, groups = stored_ranking(adata, key, None, context=context)
    field = metric.removeprefix("log10_")
    if field not in result:
        raise ValueError(
            f"{context}: stored ranking has no {field}; compute it explicitly first."
        )
    # Scanpy requires complete rankings, even when plotting a short marker list.
    if len(result["names"]) < adata.n_vars:
        raise ValueError(
            f"{context}: statistic colors need complete stored rankings; run "
            "sc.tl.rank_genes_groups explicitly with n_genes=adata.n_vars first."
        )
    if table is None:
        table = _ranking_table(
            adata,
            result,
            groups,
            key=key,
            gene_symbols=gene_symbols,
            min_logfoldchange=None,
            context=context,
        )
    label = "names" if gene_symbols is None else gene_symbols
    names, _ = _feature_slots(markers, None, None)
    selected = table.loc[table[label].isin(names)]
    if selected.duplicated([label, "group"]).any():
        raise ValueError(
            f"{context}: statistic colors need unambiguous gene labels within each group."
        )
    colors = selected.pivot(index="group", columns=label, values=field)
    # Scanpy's pivot sorts groups; the parent dotplot restores category order.
    colors = colors.reindex(index=sorted(groups), columns=names)
    values = numeric_values(colors, context=context)
    if not np.isfinite(values).all():
        raise ValueError(
            f"{context}: requested genes need finite stored {field} in every ranking group."
        )
    if field.startswith("pvals") and ((values < 0) | (values > 1)).any():
        raise ValueError(f"{context}: stored {field} must be between 0 and 1.")
    if metric.startswith("log10_"):
        if (values == 0).any():
            raise ValueError(
                f"{context}: {metric} needs positive p-values; zero would produce infinity."
            )
        colors = -np.log10(colors)
    return colors


def gene_rank_panels(
    adata: Any, groups: Any, *, key: str | None, n_genes: int, gene_symbols: str | None
) -> list[RankPanel]:
    """Return stored rank/score panels, looking up symbols in the ranking's source."""
    context = "gsc.pl.rank_genes_groups"
    count = _count(n_genes, "n_genes", context=context)
    result, chosen = stored_ranking(adata, key, groups, context=context)
    panels = []
    for group in chosen:
        scores = numeric_values(
            pd.DataFrame({"score": result["scores"][group][:count]}), context=context
        )[:, 0]
        names = result["names"][group][:count]
        if not np.isfinite(scores).all() or pd.isna(names).any():
            raise ValueError(
                f"{context}: panels require matching finite scores and nonmissing gene names; use a ranked expression plot for filtered results."
            )
        if gene_symbols is not None:
            use_raw = bool(np.asarray(result["params"]["use_raw"]).item())
            source = adata.raw if use_raw else adata
            if (
                source is None
                or gene_symbols not in source.var
                or not source.var_names.is_unique
            ):
                raise ValueError(
                    f"{context}: gene_symbols needs an unambiguous column in the ranking's raw/var source."
                )
            names = source.var.loc[list(names), gene_symbols].to_numpy()
        if not all(isinstance(name, str) for name in names):
            raise ValueError(f"{context}: gene labels must be nonmissing strings.")
        low, high = float(scores.min()), float(scores.max())
        panels.append(
            RankPanel(
                f"{group} vs. {result['params']['reference']}",
                pd.DataFrame(
                    {"_rank": np.arange(len(scores)), "_label": names, "_score": scores}
                ),
                (-0.9, count - 0.1),
                (low, high),
            )
        )
    return panels


def attribute_rank_panels(
    adata: Any,
    attr: str,
    keys: Any,
    *,
    dictionary: str | None,
    indices: Sequence[int] | None,
    labels: Any,
    n_points: int,
    log: bool,
    include_lowest: bool,
    context: str = "gsc.pl.ranking",
) -> list[RankPanel]:
    """Return sorted panels from supplied AnnData scores; never fit or modify data."""
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    count = _count(n_points, "n_points", context=context)
    if attr not in {"var", "obs", "uns", "varm", "obsm"}:
        raise ValueError(f"{context}: attr must be var, obs, uns, varm, or obsm.")
    source = getattr(adata, attr)
    if dictionary is not None:
        source = source[dictionary]
    panel_keys = [keys] if isinstance(keys, str) else list(keys)
    if not panel_keys or not all(isinstance(k, str) for k in panel_keys):
        raise ValueError(f"{context}: keys must contain score names.")
    if indices is not None:
        if not isinstance(keys, str) or dictionary is not None:
            raise ValueError(
                f"{context}: indices needs one array key without dictionary."
            )
        matrix = source[keys]
        if not isinstance(matrix, np.ndarray) or matrix.ndim != 2:
            raise TypeError(
                f"{context}: indices requires a resident two-dimensional NumPy array."
            )
        values = pd.DataFrame(matrix[:, list(indices)])
        panel_keys = [f"{keys[:-1]}{i + 1}" for i in indices]
    else:
        values = pd.DataFrame({k: source[k] for k in panel_keys})
    scores = numeric_values(values, context=context)
    if not scores.size or not np.isfinite(scores).all():
        raise ValueError(f"{context}: scores must be nonempty and finite.")
    if log:
        if (scores <= 0).any():
            raise ValueError(f"{context}: log scores must be positive.")

        # Scanpy logs the original dtype before converting plotting values.
        scores = numeric_values(np.log(values), context=context)

    # Resolve labels before choosing the highest and lowest scores.
    if labels is None:
        labels = (
            adata.var_names
            if attr in {"var", "varm"}
            else [str(i) for i in range(len(scores))]
        )
    elif isinstance(labels, str):
        labels = [f"{labels}{i + 1}" for i in range(len(scores))]
    labels = np.asarray(labels)
    if labels.shape != (len(scores),) or not all(isinstance(v, str) for v in labels):
        raise ValueError(f"{context}: labels must contain one string per score row.")
    if include_lowest and count < 2:
        raise ValueError(f"{context}: include_lowest needs n_points >= 2.")
    panels = []
    for i, title in enumerate(panel_keys):
        score = scores[:, i]
        order = np.argsort(score)[::-1]
        gap = None

        # Keep the score extremes in order, leaving two positions for omitted ranks.
        if include_lowest:
            high_indices = order[: count // 2]
            low_indices = order[-(count - count // 2) :]
            gap = (
                len(high_indices)
                if len(high_indices) + len(low_indices) < len(order)
                else None
            )
            chosen = np.concatenate([high_indices, low_indices])
        else:
            chosen = order[: count + 1]
        positions = np.arange(len(chosen))
        if gap is not None:
            positions[gap:] += 2
        selected = score[chosen]
        low, high = float(selected.min()), float(selected.max())
        table = pd.DataFrame(
            {"_rank": positions, "_label": labels[chosen], "_score": selected}
        )
        if gap is not None:
            table.loc[len(table)] = [
                gap,
                "⋮",
                (score[chosen[count // 2 - 1]] + score[chosen[count // 2]]) / 2,
            ]
            table = table.sort_values("_rank", kind="stable").reset_index(drop=True)
        panels.append(
            RankPanel(
                title.replace("_", " "),
                table,
                (-0.9, count + 0.9 + include_lowest),
                (
                    (0.95 if low > 0 else 1.05) * low,
                    (1.05 if high > 0 else 0.95) * high,
                ),
                hide_ticks=include_lowest,
            )
        )
    return panels
