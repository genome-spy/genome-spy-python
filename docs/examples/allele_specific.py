"""Allele-specific signal (real data).

Raw ASCAT logR and B-allele frequency for tumour sample S96 across the whole
genome, streamed directly from GenomeSpy's hosted data. logR tracks total
coverage change while BAF reveals allelic imbalance; together they are the raw
signal behind the copy-number segments. Around 10,000 SNPs render smoothly —
pan and zoom into any locus.
"""

import pandas as pd

import genome_spy as gs
from genome_spy.schema import GenomeAxis, Scale

META = {
    "category": "Copy-number plots",
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

signal_colors = Scale(
    domain=["logR", "B-allele freq."],
    range=["#3e8cb6", "#2c6e6a"],
)

legend_data = pd.DataFrame(
    {"signal": ["logR", "B-allele freq."], "x": [0, 1], "y": [0, 0]}
)

legend_points = (
    gs.Chart(legend_data)
    .mark_point(size=90, filled=True, opacity=0.9)
    .encode(
        x=gs.X("x:Q").axis(None).title(None),
        y=gs.Y("y:Q").axis(None).title(None).scale(reverse=False),
        color=gs.Color("signal:N").scale(signal_colors).legend(title="Signal"),
    )
)

legend_labels = (
    gs.Chart(legend_data)
    .mark_text(align="left", dx=10, size=11)
    .encode(
        x=gs.X("x:Q").axis(None).title(None),
        y=gs.Y("y:Q").axis(None).title(None).scale(reverse=False),
        text=gs.Text("signal:N"),
    )
)

legend = (legend_points + legend_labels).properties(title="Signal key")

log_r = (
    gs.Chart(RAW)
    .transform_formula(expr="'logR'", as_="signal")
    .mark_point(size=8, filled=True, opacity=0.35)
    .encode(
        x=gs.Locus("chr", "pos", scale={"assembly": "hg38"}),
        y=gs.Y("logR:Q").scale(reverse=False, domain=[-1.5, 1.5]).title("logR"),
        color=gs.Color("signal:N").scale(signal_colors).legend(None),
    )
)

baf = (
    gs.Chart(RAW)
    .transform_formula(expr="'B-allele freq.'", as_="signal")
    .mark_point(size=8, filled=True, opacity=0.35)
    .encode(
        x=gs.Locus("chr", "pos", scale={"assembly": "hg38"}, axis=axis),
        y=gs.Y("baf:Q").scale(reverse=False, domain=[0, 1]).title("B-allele freq."),
        color=gs.Color("signal:N").scale(signal_colors).legend(None),
    )
)

chart = (
    gs.vconcat(legend, log_r, baf)
    .resolve_scale(x="independent")
    .properties(
        title="Allele-specific raw signal (ASCAT, sample S96)",
        description="Real genome-wide logR and BAF streamed from GenomeSpy's hosted sample data.",
    )
)
