"""Static genomic context for the TAL1 AlphaGenome example."""

from __future__ import annotations

from typing import Any

_REFSEQ_SOURCE = "UCSC NCBI RefSeq, hg38 (data release 2025-08-13)"
_TRANSCRIPTS = (
    {
        "gene": "TAL1",
        "transcript": "NM_003189.5",
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
        "gene": "STIL",
        "transcript": "NM_003035.2",
        "strand": "-",
        "start0": 47_250_138,
        "end0": 47_314_147,
        "exons": (
            (47_250_138, 47_251_922),
            (47_260_288, 47_260_539),
            (47_262_902, 47_263_113),
            (47_269_634, 47_269_866),
            (47_272_075, 47_272_241),
            (47_280_240, 47_281_209),
            (47_282_344, 47_282_459),
            (47_287_550, 47_287_660),
            (47_289_434, 47_289_585),
            (47_293_457, 47_293_544),
            (47_295_764, 47_295_848),
            (47_299_904, 47_300_152),
            (47_301_560, 47_301_748),
            (47_302_233, 47_302_346),
            (47_304_888, 47_304_996),
            (47_310_275, 47_310_362),
            (47_314_035, 47_314_147),
        ),
    },
)


def gene_annotation_rows(display_start: int, display_end: int) -> list[dict[str, Any]]:
    """Return representative RefSeq transcript and exon rows for the display."""
    rows: list[dict[str, Any]] = []
    for lane, transcript in enumerate(_TRANSCRIPTS):
        visible_start = max(display_start, transcript["start0"])
        visible_end = min(display_end, transcript["end0"])
        if visible_start >= visible_end:
            continue
        common = {
            "gene": transcript["gene"],
            "transcript": transcript["transcript"],
            "strand": transcript["strand"],
            "lane": lane,
            "source": _REFSEQ_SOURCE,
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
