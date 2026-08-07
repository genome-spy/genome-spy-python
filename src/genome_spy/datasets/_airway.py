"""Internal helpers for the packaged airway RNA-seq examples."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


def airway_paired_logcounts(
    *, min_base_mean: float = 10.0
) -> tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    """Load packaged airway counts as paired treated/control log-counts.

    Description:
        Reads the scaled-count table and sample metadata, filters genes by
        mean count, transforms counts with ``log2(count + 1)``, and pivots the
        eight samples into matching treated and control matrices by cell type.

    Args:
        min_base_mean: Minimum mean count required to retain a gene.

    Returns:
        The retained base means, treated log-count matrix, and control
        log-count matrix. All three share the same gene index.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> base_mean, treated, control = airway_paired_logcounts()
        >>> treated.shape == control.shape
        True
    """
    counts = load_dataset("airway_scaledcounts", as_format="dataframe").set_index(
        "ensgene"
    )
    metadata = load_dataset("airway_metadata", as_format="dataframe").set_index("id")

    sample_ids = metadata.index.to_list()
    count_matrix = counts.loc[:, sample_ids].copy()
    base_mean = count_matrix.mean(axis=1)
    count_matrix = count_matrix.loc[base_mean >= min_base_mean]
    base_mean = base_mean.loc[count_matrix.index]

    long_counts = (
        np.log2(count_matrix + 1.0)
        .reset_index()
        .melt(id_vars="ensgene", var_name="id", value_name="log_count")
        .merge(
            metadata.loc[:, ["celltype", "dex"]].reset_index(),
            on="id",
            how="left",
            validate="many_to_one",
        )
    )
    paired = long_counts.pivot(
        index="ensgene",
        columns=["celltype", "dex"],
        values="log_count",
    )

    celltype_order = metadata["celltype"].drop_duplicates().to_list()
    control = paired.xs("control", axis=1, level="dex").loc[:, celltype_order]
    treated = paired.xs("treated", axis=1, level="dex").loc[:, celltype_order]
    return base_mean.loc[paired.index], treated, control


def airway_differential_expression(
    *,
    min_base_mean: float = 10.0,
    max_genes: int = 12_000,
    log2fc_cutoff: float = 1.0,
    pvalue_cutoff: float = 0.01,
    padj_alpha: float = 0.1,
) -> tuple[pd.DataFrame, dict[str, list[float]]]:
    """Build the chart-ready airway differential-expression table.

    Description:
        Uses the paired treated/control log-count matrices from
        :func:`airway_paired_logcounts`, computes paired t-tests and Benjamini-
        Hochberg adjusted p-values, then adds the transformed fields and
        significance classification shared by the MA and volcano examples.

    Args:
        min_base_mean: Minimum mean count required before testing.
        max_genes: Keep at most this many genes by base mean for plotting.
        log2fc_cutoff: Absolute fold-change threshold for significance labels.
        pvalue_cutoff: Raw p-value threshold for significance labels.
        padj_alpha: FDR level passed to the multiple-testing correction.

    Returns:
        A chart-ready result table and plotting domains.

    Raises:
        ImportError: If pandas, SciPy, or statsmodels is not installed.

    Example:
        >>> data, domains = airway_differential_expression(max_genes=200)
        >>> {"log2fc", "pvalue", "padj"} <= set(data)
        True
    """
    import pandas as pd
    from scipy.stats import ttest_rel
    from statsmodels.stats.multitest import fdrcorrection

    base_mean, treated, control = airway_paired_logcounts(min_base_mean=min_base_mean)
    log2fc = treated.subtract(control).mean(axis=1)
    test = ttest_rel(treated.to_numpy(), control.to_numpy(), axis=1, nan_policy="omit")
    pvalue = np.asarray(test.pvalue, dtype=float)
    pvalue = np.where(
        ~np.isfinite(pvalue) & np.isclose(log2fc.to_numpy(), 0.0), 1.0, pvalue
    )
    pvalue = np.where(~np.isfinite(pvalue), 0.0, pvalue)
    _rejected, padj = fdrcorrection(pvalue, alpha=padj_alpha)

    data = pd.DataFrame(
        {
            "ensgene": treated.index,
            "base_mean": base_mean.loc[treated.index].to_numpy(),
            "log2fc": log2fc.to_numpy(),
            "pvalue": pvalue,
            "padj": padj,
        }
    )
    data["neglog10_pvalue"] = -np.log10(np.clip(data["pvalue"], 1e-300, 1.0))
    data["neglog10_padj"] = -np.log10(np.clip(data["padj"], 1e-300, 1.0))
    data["log10_base_mean"] = np.log10(data["base_mean"])
    passes = (data["pvalue"] < pvalue_cutoff) & (data["log2fc"].abs() >= log2fc_cutoff)
    data["direction"] = np.where(
        passes & (data["log2fc"] > 0),
        "up in dex",
        np.where(passes & (data["log2fc"] < 0), "down in dex", "n.s."),
    )
    data = data.nlargest(max_genes, "base_mean").sort_values("log10_base_mean")

    log2fc_extent = float(np.ceil(data["log2fc"].abs().max() * 2) / 2)
    volcano_y_max = float(np.ceil(data["neglog10_pvalue"].quantile(0.995) / 5) * 5)
    data["neglog10_pvalue_plot"] = np.minimum(data["neglog10_pvalue"], volcano_y_max)
    volcano_x_extent = float(np.ceil(data["log2fc"].abs().max() * 2) / 2)
    domains = {
        "ma_x": [
            float(np.floor(data["log10_base_mean"].min() * 2) / 2),
            float(np.ceil(data["log10_base_mean"].max() * 2) / 2),
        ],
        "ma_y": [-log2fc_extent, log2fc_extent],
        "volcano_x": [-volcano_x_extent, volcano_x_extent],
        "volcano_y": [0.0, volcano_y_max],
        "pvalue_cutoff": [-float(np.log10(pvalue_cutoff))],
    }
    return data, domains
