"""Allele-specific signal (real data).

Raw ASCAT logR and B-allele frequency for tumour sample S96 across the whole
genome, streamed directly from GenomeSpy's hosted data. logR tracks total
coverage change while BAF reveals allelic imbalance; together they are the raw
signal behind the copy-number segments. Around 10,000 SNPs render smoothly —
pan and zoom into any locus.
"""

import genome_spy as gs
from genome_spy.schema import GenomeAxis

META = {
    "category": "Copy number",
    "tags": ("locus", "real-data", "multi-track"),
    "order": 20,
    "height": 380,
}

# Real per-SNP ASCAT signal for sample S96, hosted by GenomeSpy.
RAW = {
    "url": "https://data.genomespy.app/sample-data/ASCAT/raw_S96.tsv",
    "format": {"type": "tsv"},
}

axis = GenomeAxis(
    title="Genomic position",
    chromGrid=True,
    chromGridOpacity=0.12,
    chromGridFillEven="#f4f6fb",
    chromGridFillOdd="#ffffff",
    chromLabels=True,
    chromTicks=True,
    grid=False,
)

log_r = (
    gs.Chart(RAW)
    .mark_point(size=8, filled=True, opacity=0.35, color="#3e8cb6")
    .encode(
        x=gs.Locus("chr", "pos", scale={"assembly": "hg38"}),
        y=gs.Y("logR:Q").scale(reverse=False, domain=[-1.5, 1.5]).title("logR"),
    )
)

baf = (
    gs.Chart(RAW)
    .mark_point(size=8, filled=True, opacity=0.35, color="#2c6e6a")
    .encode(
        x=gs.Locus("chr", "pos", scale={"assembly": "hg38"}, axis=axis),
        y=gs.Y("baf:Q").scale(reverse=False, domain=[0, 1]).title("B-allele freq."),
    )
)

chart = gs.vconcat(log_r, baf).properties(
    title="Allele-specific raw signal (ASCAT, sample S96)",
    description="Real genome-wide logR and BAF streamed from GenomeSpy's hosted sample data.",
)
