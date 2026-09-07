"""Genome tracks with gene annotations.

A browser-style locus view with a quantitative signal track stacked above a
gene-annotation track. The lower panel combines transcript bodies, exons,
labels, and strand cues so the annotations stay readable while zooming.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 10,
    "height": 250,
    "max_width": 920,
}

DOMAIN = [
    {"chrom": "chr5", "pos": 177500000},
    {"chrom": "chr5", "pos": 179500000},
]

# Show GC content, loading just the region being viewed.
gc_track = (
    gs.Chart(
        data=gs.lazy.bigwig("https://data.genomespy.app/genomes/hg38/hg38.gc5Base.bw")
    )
    .mark_rect(color="#6c8ebf", minWidth=0.5, minOpacity=1, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q")
        .scale(domain=[0, 100], reverse=False)
        .axis(title="GC (%)", grid=True, gridDash=[2, 2]),
    )
    .properties(
        name="gc-content",
        title=gs.title("GC content", orient="left"),
        height=96,
    )
    .configure_view(stroke="lightgray")
)

# Draw exon blocks for the gene track below.
exons = (
    gs.Chart()
    .mark_rect(minOpacity=0.2, minWidth=0.5, tooltip=None)
    .encode(x=gs.X("exonStart:L"), x2=gs.X2("exonEnd"))
    .transform_project(fields=["_lane", "_start", "exons"])
    .transform_flatten_compressed_exons(start="_start")
    .properties(name="exons")
)

# Connect the exons with a thin line spanning each transcript.
bodies = (
    gs.Chart()
    .mark_rule(minLength=0.5, size=1, tooltip=None)
    .encode(
        x=gs.X("_start:L").axis(title="Genomic position"),
        x2=gs.X2("_end"),
        search=gs.Search("symbol"),
    )
    .properties(name="bodies", title="Gene annotations")
)

# Reveal the gene shapes as the reader zooms in.
transcripts = (
    gs.layer(exons, bodies)
    .properties(
        name="transcripts",
        opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
    )
    .encode(
        color=gs.value("#909090"),
    )
)

# Label genes and show more details on hover.
labels = (
    gs.Chart()
    .mark_text(size=11, yOffset=7, tooltip=gs.HandledTooltip(handler="refseqgene"))
    .encode(x=gs.X("_centroid:L"), text=gs.Text("symbol:N"))
    .properties(name="labels")
)

# Put a reading-direction arrow just beside each gene name.
arrows = (
    gs.Chart()
    .mark_point(yOffset=7, size=50, tooltip=None)
    .encode(
        x=gs.X("_centroid:L"),
        dx=gs.Dx(
            gs.expr(
                (gs.datum._textWidth / 2 + 5)
                * gs.expr.if_(gs.datum.strand == "-", -1, 1)
            ),
            type="quantitative",
        ).scale(None),
        color=gs.value("black"),
        shape=gs.Shape("strand:N")
        .scale(domain=["-", "+"], range=["triangle-left", "triangle-right"])
        .legend(None),
    )
    .properties(
        name="arrows",
        opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
    )
)

# Hide overlapping names, using the supplied scores to choose which to keep.
symbols = (
    gs.layer(labels, arrows)
    .properties(
        name="symbols",
    )
    .transform_measure_text(
        field="symbol",
        as_="_textWidth",
        fontSize=11,
    )
    .transform_filter_scored_labels(
        lane="_lane",
        score="score",
        width="_textWidth",
        pos="_centroid",
        padding=5,
    )
)

# Load one RefSeq table for the gene shapes and labels.
refseq_track = (
    gs.layer(transcripts, symbols)
    .properties(
        name="refseq-track",
        title=gs.title("RefSeq gene annotation", orient="left"),
        height=gs.step(23),
        data=gs.Data(
            url="https://data.genomespy.app/genomes/hg38/refSeqGenes-hg38-release232.tsv.gz",
            format=gs.data_format(
                parse=gs.parse(
                    symbol="string",
                    chrom="string",
                    start="integer",
                    length="integer",
                    strand="string",
                    score="integer",
                    exons="string",
                )
            ),
        ),
    )
    .encode(
        y=gs.Y("_lane:O")
        .scale(
            type="index",
            align=0,
            paddingInner=0.4,
            paddingOuter=0.2,
            domain=[0, 3],
            reverse=True,
            zoom=False,
        )
        .axis(None),
    )
    # Find each transcript's start, end, and label position.
    .transform_linearize_genomic_coordinate(
        chrom="chrom",
        pos="start",
        as_="_start",
    )
    .transform_formula(
        expr=gs.datum._start + gs.datum.length,
        as_="_end",
    )
    .transform_formula(
        expr=gs.datum._start + gs.datum.length / 2,
        as_="_centroid",
    )
    # Put overlapping transcripts on separate rows, showing up to three rows.
    .transform_collect(sort=gs.compare(["_start"]))
    .transform_pileup(
        start="_start",
        end="_end",
        as_="_lane",
        preference="strand",
        preferredOrder=["-", "+"],
    )
    .transform_filter(gs.datum._lane < 3)
)

# Put GC content above the genes so both tracks move together when zooming.
chart = (
    gs.vconcat(gc_track, refseq_track, spacing=10)
    .properties(
        assembly="hg38",
        title="GC content with RefSeq gene annotations",
        description=(
            "A genome browser view combining a GC-content signal track with "
            "stacked RefSeq gene annotations."
        ),
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    )
    .resolve_scale(y="independent")
    .resolve_axis(y="independent")
)
