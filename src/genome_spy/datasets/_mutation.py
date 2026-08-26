"""Wrangle packaged MAFs for position-based gallery examples."""

from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, TypedDict

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


_COMPLEMENTARY_SUBSTITUTIONS = {
    "A>G": "T>C",
    "T>C": "T>C",
    "C>T": "C>T",
    "G>A": "C>T",
    "A>T": "T>A",
    "T>A": "T>A",
    "A>C": "T>G",
    "T>G": "T>G",
    "C>A": "C>A",
    "G>T": "C>A",
    "C>G": "C>G",
    "G>C": "C>G",
}

_DNMT3A_DOMAINS = (
    {"name": "Dnmt3b_related", "start": 290, "end": 377, "color": "#e78973"},
    {"name": "ADDz_Dnmt3a", "start": 476, "end": 612, "color": "#8094ee"},
    {"name": "AdoMet_MTases", "start": 634, "end": 905, "color": "#f7c57a"},
)


class Dnmt3aLollipopData(TypedDict):
    """Chart tables and metadata returned for the DNMT3A lollipop."""

    gene: str
    transcript: str
    protein_length: int
    total_samples: int
    mutated_samples: int
    mutation_rate: float
    features: pd.DataFrame
    domains: pd.DataFrame
    backbone: pd.DataFrame


class BrcaRainfallData(TypedDict):
    """Chart tables and metadata returned for the BRCA rainfall plot."""

    sample: str
    reference_build: str
    points: pd.DataFrame
    change_points: pd.DataFrame
    y_max: float


def dnmt3a_lollipop_data() -> Dnmt3aLollipopData:
    """Prepare DNMT3A mutation positions from the packaged TCGA LAML MAF.

    Description:
        Loads the MAF's ``Hugo_Symbol``, ``Protein_Change``,
        ``Variant_Classification``, and ``Tumor_Sample_Barcode`` columns.
        DNMT3A protein changes are parsed to amino-acid positions and grouped
        into one feature per position. Domains and the protein backbone are
        small display annotations maintained here because they are not in the
        upstream MAF.

    Returns:
        A mapping containing mutation features, domain/backbone tables, and
        sample-rate metadata.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> dnmt3a_lollipop_data()["features"].head()
    """
    import pandas as pd

    maf = load_dataset("tcga_laml_maf", as_format="dataframe")
    gene_variants = maf.loc[maf["Hugo_Symbol"].eq("DNMT3A")].copy()
    gene_variants["label"] = gene_variants["Protein_Change"].str.removeprefix("p.")
    gene_variants["position"] = gene_variants["label"].map(_protein_position)
    parsed = gene_variants.dropna(subset=["position"]).copy()
    parsed["position"] = parsed["position"].astype(int)

    # Count calls and choose the most frequent class at each position. Sorting
    # class names descending preserves the previous deterministic tie-break.
    features = parsed.groupby("position", as_index=False).agg(
        count=("label", "size"),
        labels=("label", lambda values: sorted(values.dropna().unique())),
    )
    dominant_class = (
        parsed.groupby(["position", "Variant_Classification"], as_index=False)
        .size()
        .sort_values(
            ["position", "size", "Variant_Classification"],
            ascending=[True, False, False],
            kind="stable",
        )
        .drop_duplicates("position")
        .rename(columns={"Variant_Classification": "class"})[["position", "class"]]
    )
    features = features.merge(dominant_class, on="position", validate="one_to_one")
    features["label"] = features["labels"].map(" / ".join)
    features["is_hotspot"] = features["position"].eq(882)

    total_samples = int(maf["Tumor_Sample_Barcode"].nunique())
    mutated_samples = int(parsed["Tumor_Sample_Barcode"].nunique())
    return {
        "gene": "DNMT3A",
        "transcript": "NM_022552",
        "protein_length": 912,
        "total_samples": total_samples,
        "mutated_samples": mutated_samples,
        "mutation_rate": round(mutated_samples / total_samples * 100, 2),
        "features": features,
        "domains": pd.DataFrame(_DNMT3A_DOMAINS),
        "backbone": pd.DataFrame([{"start": 1, "end": 912, "color": "#a8b5b6"}]),
    }


def brca_rainfall_data() -> BrcaRainfallData:
    """Prepare a BRCA rainfall plot from the packaged maftools MAF.

    Description:
        Loads the sample, variant-type, chromosome, position, allele, and gene
        columns. The sample with the most calls is selected, SNPs are ordered
        within chromosomes, substitutions are converted to pyrimidine
        orientation, and inter-event distances are calculated. The kataegis
        detector follows maftools' six-mutation moving-window rule.

    Returns:
        A mapping containing rainfall points, detected clusters, and display
        metadata.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> brca_rainfall_data()["points"].head()
    """
    import pandas as pd

    maf = load_dataset("brca_maf", as_format="dataframe")
    sample_counts = (
        maf.groupby("Tumor_Sample_Barcode").size().sort_values(ascending=False)
    )
    sample = str(sample_counts.index[0])
    snps = maf.loc[
        maf["Tumor_Sample_Barcode"].eq(sample) & maf["Variant_Type"].eq("SNP")
    ].copy()
    chromosome_order = sorted(snps["Chromosome"].unique(), key=_chromosome_key)
    snps["Chromosome"] = pd.Categorical(
        snps["Chromosome"], categories=chromosome_order, ordered=True
    )
    snps = snps.sort_values(["Chromosome", "Start_Position"], kind="stable")
    snps["distance"] = snps.groupby("Chromosome", observed=True)[
        "Start_Position"
    ].diff()
    substitution = snps["Reference_Allele"] + ">" + snps["Tumor_Seq_Allele2"]
    snps["con_class"] = substitution.map(_COMPLEMENTARY_SUBSTITUTIONS)
    snps["log10_distance"] = snps["distance"].map(
        lambda distance: (
            round(math.log10(distance + 1), 4) if pd.notna(distance) else math.nan
        )
    )

    points = (
        snps.dropna(subset=["distance", "con_class"])
        .rename(
            columns={
                "Chromosome": "chrom",
                "Start_Position": "pos",
                "Hugo_Symbol": "gene",
            }
        )[["chrom", "pos", "gene", "distance", "log10_distance", "con_class"]]
        .copy()
    )
    points["chrom"] = "chr" + points["chrom"].astype(str).str.removeprefix("chr")
    points["distance"] = points["distance"].astype(int)

    return {
        "sample": sample,
        # The trimmed maftools example omits NCBI_Build, but its coordinates
        # and Hugo symbols match hg19 (for example, chr8:124090377 TBC1D31).
        "reference_build": "hg19",
        "points": points.reset_index(drop=True),
        "change_points": _detect_kataegis(points),
        "y_max": round(float(points["log10_distance"].max()) + 0.2, 2),
    }


def _protein_position(label: object) -> int | None:
    if not isinstance(label, str):
        return None
    match = re.search(r"\d+", label)
    return int(match.group()) if match else None


def _chromosome_key(chromosome: object) -> tuple[int, str]:
    value = str(chromosome).removeprefix("chr")
    if value.isdigit():
        return int(value), ""
    return {"X": 23, "Y": 24, "MT": 25}.get(value, 26), value


def _detect_kataegis(points: pd.DataFrame) -> pd.DataFrame:
    import pandas as pd

    records: list[dict[str, object]] = []
    for chromosome, chromosome_points in points.groupby(
        "chrom", observed=True, sort=False
    ):
        chromosome_points = chromosome_points.reset_index(drop=True)
        start_index = 0
        end_index = 6
        while end_index <= len(chromosome_points):
            # maftools starts a cluster when six consecutive mutations average
            # at most 1,000 bp apart, then extends that cluster greedily.
            queue = chromosome_points.iloc[start_index:end_index]
            if len(queue) < 6:
                break
            if queue["distance"].mean() > 1000:
                start_index += 1
                end_index += 1
                continue

            while end_index <= len(chromosome_points):
                queue = chromosome_points.iloc[start_index:end_index]
                if queue["distance"].mean() > 1000:
                    break
                end_index += 1

            cluster = chromosome_points.iloc[start_index : end_index - 1]
            records.append(
                {
                    "chrom": str(chromosome),
                    "start": int(cluster["pos"].min()),
                    "end": int(cluster["pos"].max()),
                    "count": len(cluster),
                    "mean_distance": round(float(cluster["distance"].mean()), 2),
                    "arrow_y": round(
                        max(float(cluster["log10_distance"].min()) - 0.25, 0.1),
                        4,
                    ),
                }
            )
            start_index = end_index
            end_index += 6

    return pd.DataFrame(records)
