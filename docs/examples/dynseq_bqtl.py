"""Dynseq binding-QTL tracks.

Reference and alternate SPI1 contribution tracks are stacked over the same
base-resolution locus, following the GenomeSpy dynseq example.
"""

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "tags": ("bigwig", "bqtl", "locus", "vconcat", "lazy"),
    "order": 34,
    "height": 300,
    "max_width": 980,
}

DOMAIN = [
    {"chrom": "chr22", "pos": 43720850},
    {"chrom": "chr22", "pos": 43720960},
]
REF_URL = (
    "https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/bigwigs/chip_imp_ref.bw"
)
ALT_URL = (
    "https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/bigwigs/chip_imp_alt.bw"
)


def allele_track(url: str, title: str, color: str) -> gs.Chart:
    """Build one contribution track from a dynseq BigWig."""
    return (
        gs.Chart(gs.lazy.bigwig(url, pixelsPerBin=1))
        .mark_rect(color=color, minWidth=0.5, tooltip=None)
        .encode(
            x=gs.Locus("chrom", "start"),
            x2=gs.Locus("chrom", "end"),
            y=gs.Y("score:Q").scale(zero=True).title("Contribution"),
        )
        .properties(height=120, title=title)
    )


chart = (
    gs.vconcat(
        allele_track(REF_URL, "Reference allele (C)", "#4c78a8"),
        allele_track(ALT_URL, "Alternate allele (G)", "#f58518"),
        spacing=8,
    )
    .properties(
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
        description="Reference and alternate SPI1 dynseq contribution tracks.",
    )
    .resolve_scale(y="shared")
    .resolve_axis(x="shared")
)
