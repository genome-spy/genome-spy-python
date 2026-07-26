"""Indexed FASTA sequence track.

A base-resolution sequence view for a small genomic window. Each position is
drawn as both a colored tile and a base label on the locus axis.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "tags": ("fasta", "sequence", "lazy", "layer", "real-data"),
    "order": 22,
    "height": 180,
    "max_width": 920,
}

# Draw each base twice: once as a colored tile and once as a fitted text label.
base_rects = gs.Chart().mark_rect()
base_labels = (
    gs.Chart()
    .mark_text(
        size=13,
        fitToBand=True,
        paddingX=1.5,
        paddingY=1,
        opacity=0.7,
        flushX=False,
        tooltip=None,
    )
    .encode(
        color=gs.value("black"),
        text=gs.Text("base:N"),
    )
)

# Flatten the fetched sequence string into per-base rows, then compute absolute
# genomic positions for the locus axis.
chart = (
    gs.layer(base_rects, base_labels)
    .properties(
        assembly="hg38",
        title="Indexed FASTA sequence track",
        description=(
            "A base-level reference sequence track adapted from the GenomeSpy "
            "docs, using a lazy indexed FASTA source."
        ),
        data=gs.lazy.indexed_fasta("https://data.genomespy.app/genomes/hg38/hg38.fa"),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr7", "pos": 20003500},
                    {"chrom": "chr7", "pos": 20003540},
                ]
            )
        ),
    )
    .encode(
        x=gs.Locus("chrom", "pos"),
        color=gs.Color("base:N").scale(
            domain=["A", "C", "T", "G", "a", "c", "t", "g", "N"],
            range=[
                "#7BD56C",
                "#FF9B9B",
                "#86BBF1",
                "#FFC56C",
                "#7BD56C",
                "#FF9B9B",
                "#86BBF1",
                "#FFC56C",
                "#E0E0E0",
            ],
        ),
    )
    .transform_flatten_sequence(field="sequence", as_=["rawPos", "base"])
    .transform_formula(expr="datum.rawPos + datum.start", as_="pos")
)
