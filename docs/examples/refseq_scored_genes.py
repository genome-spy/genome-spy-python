"""RefSeq genes with scored labels.

Transcript bodies and exons fade in at detailed zoom levels while a scored
label transform keeps the most useful RefSeq gene symbols visible.
"""

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "order": 15,
    "height": 110,
    "max_width": 980,
}

# Draw exon blocks along each transcript.
exons = (
    gs.Chart()
    .transform_project(fields=["_lane", "_start", "exons"])
    .transform_flatten_compressed_exons(start="_start")
    .mark_rect(minOpacity=0.2, minWidth=0.5, tooltip=None)
    .encode(x=gs.X("exonStart:L"), x2=gs.X2("exonEnd"))
    .properties(name="exons")
)

# Connect the exons with a thin line spanning the transcript.
bodies = (
    gs.Chart()
    .mark_rule(minLength=0.5, size=1, tooltip=None)
    .encode(
        x=gs.X("_start:L"),
        x2=gs.X2("_end"),
        search=gs.Search("symbol"),
    )
    .properties(name="bodies", title="Gene annotations")
)

# Reveal the gene shapes as the reader zooms in.
transcripts = (
    (exons + bodies)
    .encode(color=gs.value("#909090"))
    .properties(
        name="transcripts",
        opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
    )
)

# Label each gene and show more details on hover.
labels = (
    gs.Chart()
    .mark_text(size=11, yOffset=7, tooltip=gs.HandledTooltip(handler="refseqgene"))
    .encode(x=gs.X("_centroid:L"), text=gs.Text("symbol:N"))
    .properties(name="labels")
)

# Put a direction arrow just beside each name, leaving room for the text.
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
    (labels + arrows)
    .properties(name="symbols")
    .transform_measure_text(field="symbol", as_="_textWidth", fontSize=11)
    .transform_filter_scored_labels(
        lane="_lane",
        score="score",
        width="_textWidth",
        pos="_centroid",
        padding=5,
    )
)

# Load one RefSeq table for both the gene shapes and labels.
chart = (
    gs.layer(transcripts, symbols)
    .properties(
        assembly="hg38",
        name="refseq-track",
        title=gs.title("RefSeq Gene annotation", orient="none"),
        description=(
            "Hg38 RefSeq annotations with packed transcripts, scored labels, "
            "and strand arrows that appear at detailed zoom levels."
        ),
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
        axes=gs.axes(x=gs.GenomeAxis(title=None)),
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
        .axis(None)
    )
    # Find each transcript's start, end, and label position.
    .transform_linearize_genomic_coordinate(chrom="chrom", pos="start", as_="_start")
    .transform_formula(expr=gs.datum._start + gs.datum.length, as_="_end")
    .transform_formula(
        expr=gs.datum._start + gs.datum.length / 2,
        as_="_centroid",
    )
    # Put overlapping transcripts on separate rows, showing up to three rows.
    .transform_collect(sort=gs.compare(field=["_start"]))
    .transform_pileup(
        start="_start",
        end="_end",
        as_="_lane",
        preference="strand",
        preferredOrder=["-", "+"],
    )
    .transform_filter(gs.datum._lane < 3)
)
