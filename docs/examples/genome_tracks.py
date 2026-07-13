"""Genome tracks with gene annotations.

A browser-style locus view: three epigenomic signal tracks (H3K27ac, H3K4me3,
and ATAC) stacked over a shared genomic window, with a gene-annotation track
below. Signals are drawn as coverage ``rect`` bars and genes as labelled blocks,
all sharing one linear position axis via vertical concatenation.

The data is synthetic (a made-up locus with Gaussian peaks); it illustrates the
multi-track composition pattern rather than a specific region.
"""

import numpy as np
import pandas as pd

import genome_spy as gs

META = {
    "category": "Genome tracks",
    "tags": ("vconcat", "coverage", "genes"),
    "order": 10,
    "height": 470,
}

WINDOW = 4000
BIN = 25
ASSAYS = {
    "H3K27ac": (("#e15759", [700, 2600, 3200])),
    "H3K4me3": (("#4e79a7", [720, 1800])),
    "ATAC": (("#59a14f", [700, 1810, 2600, 3200])),
}
GENES = [
    {"name": "AURKA", "start": 640, "end": 900, "strand": "+"},
    {"name": "CSDE1", "start": 1750, "end": 1980, "strand": "-"},
    {"name": "MYCN", "start": 2540, "end": 2760, "strand": "+"},
    {"name": "DDX1", "start": 3140, "end": 3460, "strand": "+"},
]


def coverage(peaks: list[int], seed: int) -> pd.DataFrame:
    """Binned coverage over the window: a sum of Gaussian peaks plus noise."""
    rng = np.random.default_rng(seed)
    starts = np.arange(0, WINDOW, BIN)
    centers = starts + BIN / 2
    value = np.full(centers.shape, 0.15)
    for peak in peaks:
        value += np.exp(-0.5 * ((centers - peak) / 90) ** 2) * rng.uniform(0.8, 1.2)
    value += rng.uniform(0, 0.05, value.shape)
    return pd.DataFrame({"start": starts, "end": starts + BIN, "value": value})


# --- Visualization -------------------------------------------------------------


def signal_track(assay: str, color: str, peaks: list[int], seed: int) -> gs.Chart:
    return (
        gs.Chart(coverage(peaks, seed))
        .mark_rect(color=color)
        .encode(
            x=gs.X("start:Q").scale(domain=[0, WINDOW], zoom=True).title(None),
            x2=gs.X2("end"),
            y=gs.Y("value:Q").scale(reverse=False, zero=True).title(assay),
        )
    )


tracks = [
    signal_track(assay, color, peaks, seed)
    for seed, (assay, (color, peaks)) in enumerate(ASSAYS.items())
]

gene_bodies = (
    gs.Chart(GENES)
    .mark_rect(cornerRadius=2, color="#8f98a3")
    .encode(
        x=gs.X("start:Q").scale(domain=[0, WINDOW], zoom=True).title("Position (bp)"),
        x2=gs.X2("end"),
    )
)

gene_labels = (
    gs.Chart(GENES)
    .mark_text(align="left", dy=-9, size=11)
    .encode(
        x=gs.X("start:Q").scale(domain=[0, WINDOW], zoom=True),
        text=gs.Text("name:N"),
    )
)

gene_track = gene_bodies + gene_labels

chart = gs.vconcat(*tracks, gene_track).properties(
    title="Epigenomic signal and gene annotations at a locus",
    description="Stacked coverage tracks over a shared genomic window with a gene track.",
)
