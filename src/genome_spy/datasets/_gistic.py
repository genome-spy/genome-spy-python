"""Load the complete packaged TCGA OV GISTIC2 example results."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


class TcgaOvGisticData(TypedDict):
    """Chart tables returned for the TCGA OV GISTIC landscape."""

    scores: pd.DataFrame
    lesions: pd.DataFrame


def tcga_ov_gistic_data() -> TcgaOvGisticData:
    """Load the TCGA OV GISTIC2 data displayed by the gallery example.

    Description:
        The tables are the complete ``scores.gistic`` and
        ``all_lesions.conf_99.txt`` files used by GenomeSpy's TCGA OV example.
        They originate from the TCGA OV-TP GISTIC2 Level 4 archive published by
        the Broad GDAC Firehose on 2016-01-28 and use hg19 coordinates. The
        copies are retained locally so rendering does not depend on
        GenomeSpy's external data host.

    Returns:
        Score and lesion tables for the displayed genomic interval.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> tcga_ov_gistic_data()["scores"].head()
    """
    return {
        "scores": load_dataset("tcga_ov_gistic_scores", as_format="dataframe"),
        "lesions": load_dataset("tcga_ov_gistic_lesions", as_format="dataframe"),
    }
