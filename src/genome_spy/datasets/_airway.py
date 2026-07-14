"""Internal helpers for the packaged airway RNA-seq examples."""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING

import numpy as np

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


def airway_paired_logcounts(
    *, min_base_mean: float = 10.0
) -> tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    """Load the airway dataset as paired treated/control log-count matrices."""
    if importlib.util.find_spec("pandas") is None:
        raise ImportError(
            "The airway RNA-seq examples require pandas. Install the dev/docs "
            "dependencies to build these examples."
        )

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
