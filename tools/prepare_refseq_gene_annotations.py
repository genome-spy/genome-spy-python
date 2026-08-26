"""Prepare assembly-wide RefSeq gene bodies from official UCSC tables.

Usage:
    uv run python tools/prepare_refseq_gene_annotations.py
"""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "hg19": "https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz",
    "hg38": "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz",
}
REFGENE_COLUMNS = [
    "bin",
    "accession",
    "chrom",
    "strand",
    "tx_start",
    "tx_end",
    "cds_start",
    "cds_end",
    "exon_count",
    "exon_starts",
    "exon_ends",
    "ucsc_score",
    "symbol",
    "cds_start_status",
    "cds_end_status",
    "exon_frames",
]
CANONICAL_CHROMS = [f"chr{chrom}" for chrom in range(1, 23)] + [
    "chrX",
    "chrY",
    "chrM",
]


def parse_args() -> argparse.Namespace:
    """Parse source and output paths for the preparation workflow."""
    parser = argparse.ArgumentParser(description=__doc__)
    for assembly, url in SOURCES.items():
        parser.add_argument(
            f"--{assembly}-source",
            default=url,
            help=f"Path or URL for the UCSC {assembly} refGene table.",
        )
    parser.add_argument(
        "--output",
        type=Path,
        default=(REPO_ROOT / "src/genome_spy/datasets/data/refseq_gene_bodies.csv.gz"),
        help="Combined compressed CSV to write.",
    )
    return parser.parse_args()


def iter_gene_bodies(transcripts: pd.DataFrame) -> Iterator[dict[str, object]]:
    """Yield one body for each overlapping symbol, chromosome, and strand locus."""
    group_fields = ["chrom", "strand", "symbol"]
    for (chrom, strand, symbol), group in transcripts.groupby(
        group_fields, sort=False, observed=True
    ):
        intervals = group.sort_values(["tx_start", "tx_end", "accession"])
        component_start: int | None = None
        component_end = -1
        component_count = 0
        for row in intervals.itertuples(index=False):
            start = int(row.tx_start)
            end = int(row.tx_end)
            if component_start is not None and start > component_end:
                yield gene_body_record(
                    str(chrom),
                    str(strand),
                    str(symbol),
                    component_start,
                    component_end,
                    component_count,
                )
                component_start = None
                component_end = -1
                component_count = 0
            component_start = start if component_start is None else component_start
            component_end = max(component_end, end)
            component_count += 1
        if component_start is not None:
            yield gene_body_record(
                str(chrom),
                str(strand),
                str(symbol),
                component_start,
                component_end,
                component_count,
            )


def gene_body_record(
    chrom: str,
    strand: str,
    symbol: str,
    start: int,
    end: int,
    score: int,
) -> dict[str, object]:
    """Return one zero-based, half-open gene-body record."""
    return {
        "chrom": chrom,
        "start": start,
        "end": end,
        "strand": strand,
        "symbol": symbol,
        "identifier": f"{symbol}:{chrom}:{start}-{end}:{strand}",
        "score": score,
    }


def load_gene_bodies(assembly: str, source: str) -> pd.DataFrame:
    """Load one UCSC table and collapse overlapping transcripts into loci."""
    transcripts = pd.read_csv(
        source,
        sep="\t",
        header=None,
        names=REFGENE_COLUMNS,
        dtype={"chrom": "string", "strand": "string", "symbol": "string"},
    )
    transcripts = transcripts.loc[
        transcripts["chrom"].isin(CANONICAL_CHROMS)
        & transcripts["strand"].isin(["+", "-"])
        & transcripts["symbol"].notna()
        & transcripts["symbol"].str.strip().ne("")
        & transcripts["tx_start"].ge(0)
        & transcripts["tx_end"].gt(transcripts["tx_start"])
    ].copy()
    chrom_order = {chrom: index for index, chrom in enumerate(CANONICAL_CHROMS)}
    transcripts["_chrom_order"] = transcripts["chrom"].map(chrom_order)
    transcripts = transcripts.sort_values(
        ["_chrom_order", "tx_start", "tx_end", "strand", "symbol", "accession"],
        kind="stable",
    )
    bodies = pd.DataFrame(iter_gene_bodies(transcripts))
    bodies.insert(0, "assembly", assembly)
    return bodies


def main() -> int:
    """Prepare and write deterministic hg19 and hg38 gene-body annotations."""
    args = parse_args()
    genes = pd.concat(
        [
            load_gene_bodies("hg19", args.hg19_source),
            load_gene_bodies("hg38", args.hg38_source),
        ],
        ignore_index=True,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    genes.to_csv(
        args.output,
        index=False,
        compression={"method": "gzip", "compresslevel": 9, "mtime": 0},
    )
    print(f"Wrote {len(genes):,} gene bodies to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
