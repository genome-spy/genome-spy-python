"""Static genomic context for the TAL1 AlphaGenome example."""

from __future__ import annotations

from typing import Any

_REFSEQ_SOURCE = "UCSC NCBI RefSeq, hg38 (data release 2025-08-13)"
_ENSEMBL_SOURCE = "Ensembl GRCh38 release 116 (accessed 2026-08-13)"
_TRANSCRIPTS = (
    {
        "gene": "TAL1",
        "biotype": "protein_coding",
        "transcript": "NM_003189.5",
        "source": _REFSEQ_SOURCE,
        "strand": "-",
        "start0": 47_216_289,
        "end0": 47_232_335,
        "exons": (
            (47_216_289, 47_220_174),
            (47_224_003, 47_224_098),
            (47_225_442, 47_225_889),
            (47_229_195, 47_229_351),
            (47_229_653, 47_229_771),
            (47_232_166, 47_232_335),
        ),
    },
    {
        "gene": "ENSG00000226252 (lncRNA)",
        "biotype": "lncRNA",
        "transcript": "ENST00000422216.1",
        "source": _ENSEMBL_SOURCE,
        "strand": "+",
        "start0": 47_225_797,
        "end0": 47_230_750,
        "exons": (
            (47_225_797, 47_226_244),
            (47_227_163, 47_230_750),
        ),
    },
)


def gene_annotation_rows(display_start: int, display_end: int) -> list[dict[str, Any]]:
    """Return representative transcript and exon rows for the display."""
    rows: list[dict[str, Any]] = []
    for lane, transcript in enumerate(_TRANSCRIPTS):
        visible_start = max(display_start, transcript["start0"])
        visible_end = min(display_end, transcript["end0"])
        if visible_start >= visible_end:
            continue
        common = {
            "gene": transcript["gene"],
            "biotype": transcript["biotype"],
            "transcript": transcript["transcript"],
            "strand": transcript["strand"],
            "lane": lane,
            "source": transcript["source"],
        }
        rows.append(
            {
                **common,
                "feature": "transcript",
                "start0": transcript["start0"],
                "end0": transcript["end0"],
                "label_pos0": (visible_start + visible_end) // 2,
            }
        )
        rows.extend(
            {
                **common,
                "feature": "exon",
                "start0": exon_start,
                "end0": exon_end,
                "label_pos0": None,
            }
            for exon_start, exon_end in transcript["exons"]
            if exon_start < display_end and exon_end > display_start
        )
    return rows


def sequence_composition_rows(
    sequence: str, start0: int, *, bin_size: int = 128
) -> list[dict[str, Any]]:
    """Summarize GC fraction so the sequence track is useful when zoomed out."""
    if bin_size < 1:
        raise ValueError("Sequence composition bin size must be positive.")
    rows = []
    for offset in range(0, len(sequence), bin_size):
        chunk = sequence[offset : offset + bin_size].upper()
        rows.append(
            {
                "start0": start0 + offset,
                "end0": start0 + offset + len(chunk),
                "gc_fraction": sum(base in {"G", "C"} for base in chunk) / len(chunk),
                "bin_size": len(chunk),
            }
        )
    return rows
