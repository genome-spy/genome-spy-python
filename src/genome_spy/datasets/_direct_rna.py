"""Load the prepared RNF7 nanopore direct-RNA example tables."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, cast

from genome_spy.datasets import _load_table_bundle

if TYPE_CHECKING:
    import pandas as pd


class Rnf7Metadata(TypedDict):
    """Metadata attached to the prepared RNF7 transcript window."""

    gene: str
    geneId: str
    transcriptId: str
    displayStart: int
    displayEnd: int
    readCounts: dict[str, int]


class Rnf7DirectRnaData(TypedDict):
    """Chart-ready tables for the RNF7 direct-RNA example."""

    metadata: Rnf7Metadata
    coverage: pd.DataFrame
    reads: pd.DataFrame
    events: pd.DataFrame
    sequence: pd.DataFrame
    sites: pd.DataFrame
    exons: pd.DataFrame


def rnf7_direct_rna_data() -> Rnf7DirectRnaData:
    """Load prepared RNF7 direct-RNA coverage, reads, exons, and m6A calls.

    Description:
        The tables cover transcript positions 0–919 of ENST00000273480.3 in
        matched HEK293T wild-type and METTL3-knockout demo alignments. Site
        probabilities are published m6Anet calls; coverage, reference bases,
        display-only read spans, and alignment events were derived in the
        dataset recipe. Alignment events are reference disagreements, not
        modification calls. The condition-level probabilities were not
        recomputed from those selected alignments.

    Args:
        None.

    Returns:
        Metadata and six pandas DataFrames ready for the gallery chart.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> data = rnf7_direct_rna_data()
        >>> data["metadata"]["gene"]
        'RNF7'
    """

    return cast(
        Rnf7DirectRnaData,
        _load_table_bundle(
            "rnf7_direct_rna",
            ("coverage", "reads", "events", "sequence", "sites", "exons"),
        ),
    )
