"""Internal helpers for the packaged RefSeq gene-body annotations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


def refseq_gene_bodies(assembly: Literal["hg19", "hg38"]) -> pd.DataFrame:
    """Load an assembly-wide RefSeq gene-body annotation table.

    Description:
        Loads gene bodies independently prepared from assembly-matched UCSC
        RefSeq records. Coordinates are zero-based and half-open. The number
        of contributing transcript records is intended only for label
        prioritization.

    Args:
        assembly: UCSC assembly identifier.
    Returns:
        A chart-ready table containing every packaged gene body for the
        requested assembly.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> genes = refseq_gene_bodies("hg38")
        >>> "STK3" in set(genes["symbol"])
        True
    """
    genes = load_dataset("refseq_gene_bodies", as_format="dataframe")
    return genes.loc[genes["assembly"].eq(assembly)].reset_index(drop=True)
