"""Prepared HapMap tables used by association-plot examples."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


def hapmap_manhattan_data(
    *, genome_wide_p: float = 5e-8, suggestive_p: float = 1e-5
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float | list[float]]]:
    """Build the chart-ready HapMap Manhattan-plot tables."""
    data = load_dataset("hapmap_gwas", as_format="dataframe")
    data = data[data["P"] > 0].copy()
    data["chrom"] = np.where(
        data["CHR"] == 23,
        "chrX",
        "chr" + data["CHR"].astype(str),
    )
    data["neglog"] = -np.log10(data["P"])
    data["chrom_group"] = np.where(data["CHR"] % 2 == 0, "even", "odd")
    top_hits = data.nsmallest(8, "P")
    y_domain = [0.0, float(np.ceil(data["neglog"].max()))]
    return (
        data,
        top_hits,
        {
            "y_domain": y_domain,
            "genome_wide_y": float(-np.log10(genome_wide_p)),
            "suggestive_y": float(-np.log10(suggestive_p)),
        },
    )


def hapmap_volcano_data(
    *, effect_cutoff: float = 0.5, pvalue_cutoff: float = 1e-5
) -> tuple[pd.DataFrame, dict[str, float | list[float]]]:
    """Build the chart-ready HapMap volcano-plot table and domains."""
    data = load_dataset("hapmap_gwas", as_format="dataframe")
    data = data[data["P"] > 0].copy()
    data["neglog"] = -np.log10(data["P"])
    passes = (data["P"] < pvalue_cutoff) & (data["EFFECTSIZE"].abs() >= effect_cutoff)
    data["association"] = np.where(
        passes & (data["EFFECTSIZE"] > 0),
        "risk",
        np.where(passes & (data["EFFECTSIZE"] < 0), "protective", "n.s."),
    )
    x_extent = float(np.ceil(data["EFFECTSIZE"].abs().max() * 10) / 10)
    return data, {
        "x_domain": [-x_extent, x_extent],
        "y_domain": [0.0, float(np.ceil(data["neglog"].max()))],
        "effect_cutoff": effect_cutoff,
        "neglog_pvalue_cutoff": float(-np.log10(pvalue_cutoff)),
    }


def hapmap_qq_data(
    *, bins: int = 45
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    """Build the chart-ready HapMap QQ and deviation tables."""
    import pandas as pd

    pvals = np.sort(
        load_dataset("hapmap_gwas", as_format="dataframe")
        .query("P > 0")["P"]
        .to_numpy()
    )
    ranks = np.arange(1, len(pvals) + 1)
    data = pd.DataFrame(
        {
            "expected": -np.log10((ranks - 0.5) / len(pvals)),
            "observed": -np.log10(pvals),
        }
    )
    data["delta"] = data["observed"] - data["expected"]
    data["pattern"] = np.where(
        data["delta"] > 0.45, "Tail enrichment", "Null-like bulk"
    )

    edges = np.linspace(0.0, float(data["expected"].max()), bins + 1)
    deviation = (
        data.assign(
            bin=pd.cut(
                data["expected"],
                bins=edges,
                include_lowest=True,
                duplicates="drop",
            )
        )
        .groupby("bin", observed=True, as_index=False)
        .agg(delta_mean=("delta", "mean"))
    )
    intervals = deviation["bin"]
    deviation["x0"] = intervals.map(lambda interval: float(interval.left))
    deviation["x1"] = intervals.map(lambda interval: float(interval.right))
    deviation["zero"] = 0.0
    deviation["direction"] = np.where(
        deviation["delta_mean"] >= 0,
        "Observed > expected",
        "Observed < expected",
    )
    deviation = deviation[["x0", "x1", "zero", "delta_mean", "direction"]]
    limit = float(max(data["expected"].max(), data["observed"].max())) * 1.02
    delta_limit = float(max(abs(deviation["delta_mean"]).max(), 0.25)) * 1.1
    return (
        data,
        deviation,
        {
            "limit": limit,
            "delta_limit": delta_limit,
            "annotation_x": round(limit * 0.54, 2),
            "tail_y": round(limit * 0.93, 2),
        },
    )
