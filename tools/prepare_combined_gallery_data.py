"""Prepare the combined LAML oncoplot and Plotly p53 gallery tables.

Run with ``uv run python tools/prepare_combined_gallery_data.py`` after placing
the Plotly FASTA in tmp/alignment_viewer_p53.fasta. No network access is used.
Source revisions and input hashes are retained in each output's provenance.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import pandas as pd

from genome_spy.datasets._oncoprint import _NON_SYNONYMOUS_CLASSES

ROOT = Path(__file__).resolve().parents[1]
MAFTOOLS = ROOT / "tmp/maftools/inst/extdata"
OUTPUT = ROOT / "src/genome_spy/datasets/data"
GROUPS = {
    "TSG": ["TP53", "WT1", "PHF6"],
    "DNAm": ["DNMT3A", "DNMT3B", "TET1", "TET2", "IDH1", "IDH2"],
    "Signalling": ["FLT3", "KIT", "KRAS", "NRAS"],
    "TFs": ["RUNX1", "CEBPA"],
    "ChromMod": ["ASXL1", "EZH2", "KDM6A"],
}


def _write(name: str, data: dict) -> None:
    content = json.dumps(data, separators=(",", ":"), allow_nan=False).encode()
    (OUTPUT / f"{name}.json.gz").write_bytes(gzip.compress(content, mtime=0))


def _records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records"))


def _laml() -> dict:
    source_names = [
        "tcga_laml.maf.gz",
        "tcga_laml_annot.tsv",
        "all_lesions.conf_99.txt",
        "amp_genes.conf_99.txt",
        "del_genes.conf_99.txt",
        "LAML_sig_genes.txt.gz",
    ]
    maf = pd.read_csv(MAFTOOLS / source_names[0], sep="\t")
    clinical = pd.read_csv(MAFTOOLS / source_names[1], sep="\t")
    variants = maf[maf.Variant_Classification.isin(_NON_SYNONYMOUS_CLASSES)].copy()
    variants["sample"] = variants.Tumor_Sample_Barcode.str[:12]
    variants["gene"] = variants.Hugo_Symbol
    genes = [gene for group in GROUPS.values() for gene in group]

    # GISTIC discrete calls (1=shallow, 2=deep) apply to genes in the wide peak.
    # Join by both cytoband and boundaries, as maftools readGistic does.
    lesions = pd.read_csv(MAFTOOLS / source_names[2], sep="\t")
    cn = []
    for kind, filename in [("Amp", source_names[3]), ("Del", source_names[4])]:
        peak_genes = pd.read_csv(MAFTOOLS / filename, sep="\t", dtype=str)
        for band in peak_genes.columns[1:]:
            selected = {
                gene for gene in peak_genes[band].iloc[3:].dropna() if "|" not in gene
            }
            if not selected:
                continue
            boundary = peak_genes[band].iloc[2]
            matched = lesions[
                lesions["Unique Name"].str.startswith(kind)
                & ~lesions["Unique Name"].str.contains("CN values")
                & (lesions.Descriptor.str.strip() == band)
                & (
                    lesions["Wide Peak Limits"].str.split("(").str[0].str.strip()
                    == boundary
                )
            ]
            for _, row in matched.iterrows():
                for sample in lesions.columns[9:]:
                    if str(sample).startswith("TCGA-") and row[sample] in (1, 2):
                        cn.extend(
                            {"sample": sample[:12], "gene": gene, "class": kind}
                            for gene in sorted(selected)
                        )
    all_cn = pd.DataFrame(cn).drop_duplicates(["sample", "gene"])
    cn_frame = all_cn[all_cn.gene.isin(genes)].copy()
    selected = variants[variants.gene.isin(genes)]
    events = []
    for (sample, gene), rows in selected.groupby(["sample", "gene"]):
        events.append(
            {
                "sample": sample,
                "gene": gene,
                "class": rows.Variant_Classification.iloc[0]
                if len(rows) == 1
                else "Multi_Hit",
                "alt_c": bool((rows.Tumor_Seq_Allele2 == "C").any()),
                "feature": "Alternate allele C"
                if (rows.Tumor_Seq_Allele2 == "C").any()
                else None,
            }
        )
    events_frame = pd.DataFrame(events)
    altered = pd.concat(
        [events_frame[["sample", "gene"]], cn_frame[["sample", "gene"]]]
    ).drop_duplicates()
    frequency = altered.groupby("gene")["sample"].nunique()
    # maftools orders groups by their most frequently altered gene, then size.
    group_order = sorted(
        GROUPS,
        key=lambda g: (
            -max(frequency.get(gene, 0) for gene in GROUPS[g]),
            -len(GROUPS[g]),
            g,
        ),
    )
    genes = [
        gene
        for group in group_order
        for gene in sorted(GROUPS[group], key=lambda g: (-frequency.get(g, 0), g))
    ]
    samples = clinical.rename(columns={"Tumor_Sample_Barcode": "sample"}).copy()
    samples["sample"] = samples["sample"].str[:12]
    samples["FAB_classification"] = samples.FAB_classification.fillna("Unknown")
    group_size = samples.FAB_classification.value_counts()
    presence = set(map(tuple, altered[["sample", "gene"]].values))
    sample_order = sorted(
        samples["sample"],
        key=lambda s: (
            -group_size[
                samples.loc[samples["sample"] == s, "FAB_classification"].iloc[0]
            ],
            samples.loc[samples["sample"] == s, "FAB_classification"].iloc[0],
            tuple(-int((s, g) in presence) for g in genes),
            s,
        ),
    )
    order = {sample: i for i, sample in enumerate(sample_order)}
    for frame in (samples, events_frame, cn_frame):
        frame["sample_order"] = frame["sample"].map(order)
    # Match oncoplot's default includeColBarCN=TRUE: the "TMB" bars count
    # nonsynonymous variants AND genome-wide GISTIC gene calls, not variants/Mb.
    burden = (
        variants.groupby(["sample", "Variant_Classification"])
        .size()
        .reset_index(name="count")
        .rename(columns={"Variant_Classification": "class"})
    )
    burden = pd.concat(
        [
            burden,
            all_cn.groupby(["sample", "class"]).size().reset_index(name="count"),
        ],
        ignore_index=True,
    )
    burden["sample_order"] = burden["sample"].map(order)
    vaf = selected.groupby("gene").i_TumorVAF_WU.mean()
    mutsig = pd.read_csv(MAFTOOLS / source_names[5], sep="\t").set_index("gene")["q"]
    gene_rows = [
        {
            "gene": gene,
            "pathway": group,
            "vaf": None if pd.isna(vaf.get(gene)) else float(vaf[gene]),
            "neglog_q": -math.log10(float(mutsig[gene]))
            if gene in mutsig and mutsig[gene] > 0
            else None,
            "altered_percent": round(100 * frequency.get(gene, 0) / len(samples), 1),
        }
        for group in group_order
        for gene in genes
        if gene in GROUPS[group]
    ]
    matrix_rows = []
    pathway_events = []
    pathway_bounds = []
    for group in group_order:
        members = [row for row in gene_rows if row["pathway"] == group]
        start = len(matrix_rows)
        matrix_rows.extend(members)
        affected = sorted(set(altered.loc[altered.gene.isin(GROUPS[group]), "sample"]))
        matrix_rows.append(
            {
                "gene": group,
                "pathway": group,
                "altered_percent": 100 * len(affected) / len(samples),
            }
        )
        pathway_events.extend(
            {
                "sample": sample,
                "sample_order": order[sample],
                "gene": group,
                "class": "Pathway",
            }
            for sample in affected
        )
        pathway_bounds.append(
            {"pathway": group, "start": start, "end": len(matrix_rows) - 1}
        )
    row_order = {row["gene"]: i for i, row in enumerate(matrix_rows)}
    for row in [*matrix_rows, *gene_rows, *pathway_events]:
        row["row"] = row_order[row["gene"]]
        if "altered_percent" in row:
            row["percent_label"] = f"{row['altered_percent']:g}%"
    for frame in (events_frame, cn_frame):
        frame["row"] = frame.gene.map(row_order)
    # maftools draw_titv includes synonymous SNVs and pyrimidine-normalizes them.
    spectrum = []
    complement = str.maketrans("ACGT", "TGCA")
    for sample, rows in maf[maf.Variant_Type == "SNP"].groupby("Tumor_Sample_Barcode"):
        counts: Counter[str] = Counter()
        for row in rows.itertuples():
            ref, alt = row.Reference_Allele, row.Tumor_Seq_Allele2
            if ref in "ACGT" and alt in "ACGT" and ref != alt:
                if ref in "AG":
                    ref, alt = ref.translate(complement), alt.translate(complement)
                counts[f"{ref}>{alt}"] += 1
        spectrum.extend(
            {
                "sample": sample[:12],
                "sample_order": order[sample[:12]],
                "substitution": key,
                "percent": 100 * count / sum(counts.values()),
            }
            for key, count in sorted(counts.items())
        )
    return {
        "samples": _records(samples),
        "events": _records(events_frame),
        "copy_number": _records(cn_frame),
        "genes": gene_rows,
        "gene_order": genes,
        "matrix_rows": matrix_rows,
        "pathway_events": pathway_events,
        "pathway_bounds": pathway_bounds,
        "altered_samples": int(altered["sample"].nunique()),
        "sample_domain": [0, len(samples) - 1],
        "burden": _records(burden),
        "burden_limit": int(burden.groupby("sample")["count"].sum().max()),
        "spectrum": spectrum,
        "provenance": {
            "repository": "PoisonAlien/maftools",
            "revision": "015a4cf8c69ba89a55a3fdcea911421509e9a198",
            "sha256": {
                name: hashlib.sha256((MAFTOOLS / name).read_bytes()).hexdigest()
                for name in source_names
            },
        },
    }


def _p53() -> dict:
    source = ROOT / "tmp/alignment_viewer_p53.fasta"
    sequences = []
    for record in source.read_text().split(">")[1:]:
        header, *lines = record.splitlines()
        identifier = header.split()[0]
        sequences.append(
            {
                "identifier": identifier.split("|")[-1],
                "accession": identifier.split("|")[1],
                "header": header,
                "sequence": "".join(lines).upper(),
            }
        )
    width = max(len(row["sequence"]) for row in sequences)
    cells = [
        {
            "identifier": row["identifier"],
            "accession": row["accession"],
            "position": pos + 1,
            "residue": aa,
        }
        for row in sequences
        for pos, aa in enumerate(row["sequence"].ljust(width, "-"))
    ]
    columns = []
    for pos in range(width):
        counts = Counter(
            row["sequence"][pos] for row in sequences if pos < len(row["sequence"])
        )
        total = sum(counts.values())
        consensus = sorted(counts, key=lambda aa: (-counts[aa], aa))[0]
        columns.append(
            {
                "position": pos + 1,
                "residue": consensus,
                "identifier": "Consensus",
                "identity": counts[consensus] / len(sequences),
                "coverage": total / len(sequences),
            }
        )
    return {
        "sequences": sequences,
        "cells": cells,
        "columns": columns,
        "length": width,
        "sequence_order": [row["identifier"] for row in sequences],
        "provenance": {
            "repository": "plotly/datasets",
            "revision": "0c447c47b757ad74edecab31f0d72f849d2e67c2",
            "path": "Dash_Bio/Genetic/alignment_viewer_p53.fasta",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "processing": "Original ungapped sequences; right padding only, no sequence alignment.",
        },
    }


if __name__ == "__main__":
    _write("tcga_laml_combined_oncoplot", _laml())
    _write("p53_sequence_comparison", _p53())
