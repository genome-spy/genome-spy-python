"""Stacked genome browser tracks.

Several lazy hg38 resources share one zoomable genomic axis: signal tracks,
regulatory intervals, sequence, and RefSeq gene annotations.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "tags": ("vconcat", "bigwig", "bigbed", "fasta", "refseq", "lazy"),
    "order": 12,
    "height": 640,
    "max_width": 980,
}

DOMAIN = [
    {"chrom": "chr7", "pos": 55100000},
    {"chrom": "chr7", "pos": 55120000},
]


gc_track = (
    gs.Chart(gs.lazy.bigwig("https://data.genomespy.app/genomes/hg38/hg38.gc5Base.bw"))
    .mark_rect(color="#6c8ebf", minWidth=0.5, minOpacity=1, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q")
        .scale(domain=[0, 100])
        .axis(title="GC (%)", grid=True, gridDash=[2, 2]),
    )
    .properties(
        name="gc-content", title=gs.title("GC content", orient="left"), height=80
    )
)


conservation_track = (
    gs.Chart(
        gs.lazy.bigwig(
            "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/phyloP100way/"
            "hg38.phyloP100way.bw"
        )
    )
    .mark_rect(color="#c77c8a", opacity=0.75, minWidth=0.5, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q")
        .scale(domain=[-5, 5])
        .axis(title="phyloP", grid=True, gridDash=[2, 2]),
    )
    .properties(
        name="phylop-100way",
        title=gs.title("100-way conservation", orient="left"),
        height=80,
    )
)


ccre_track = (
    gs.Chart(
        gs.lazy.bigbed(
            "https://data.genomespy.app/sample-data/encodeCcreCombined.hg38.bb"
        )
    )
    .mark_rect(minWidth=0.5, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "chromStart"),
        x2=gs.Locus("chrom", "chromEnd"),
        color=gs.Color("ucscLabel:N").scale(
            domain=["prom", "enhP", "enhD", "K4m3", "CTCF"],
            range=["#e45756", "#f2a541", "#f6cf65", "#d99ac5", "#4f9fc4"],
        ),
    )
    .properties(name="ccre", title=gs.title("ENCODE cCRE", orient="left"), height=42)
)


sequence_rects = gs.Chart().mark_rect(tooltip=None)
sequence_labels = (
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
    .encode(color=gs.value("black"), text=gs.Text("base:N"))
)

sequence_track = (
    (sequence_rects + sequence_labels)
    .properties(
        name="sequence",
        title=gs.title("Reference sequence", orient="left"),
        height=52,
        data=gs.lazy.indexed_fasta(
            "https://data.genomespy.app/genomes/hg38/hg38.fa", windowSize=30_000
        ),
        opacity=gs.dynamic_opacity(unitsPerPixel=[100, 10], values=[0, 1]),
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


exons = (
    gs.Chart()
    .mark_rect(minOpacity=0.2, minWidth=0.5, tooltip=None)
    .encode(x=gs.X("exonStart:L"), x2=gs.X2("exonEnd"))
    .transform_project(fields=["_lane", "_start", "exons"])
    .transform_flatten_compressed_exons(start="_start")
    .properties(name="exons")
)

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

transcripts = (
    (exons + bodies)
    .properties(
        name="transcripts",
        opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
    )
    .encode(color=gs.value("#909090"))
)

labels = (
    gs.Chart()
    .mark_text(size=11, yOffset=7, tooltip=gs.HandledTooltip(handler="refseqgene"))
    .encode(x=gs.X("_centroid:L"), text=gs.Text("symbol:N"))
    .properties(name="labels")
)

arrows = (
    gs.Chart()
    .mark_point(yOffset=7, size=50, tooltip=None)
    .encode(
        x=gs.X("_centroid:L"),
        dx=gs.Dx(
            gs.expr("(datum._textWidth / 2 + 5) * (datum.strand == '-' ? -1 : 1)"),
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

refseq_track = (
    (transcripts + symbols)
    .properties(
        name="refseq-track",
        title=gs.title("RefSeq genes", orient="left"),
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
    .transform_linearize_genomic_coordinate(chrom="chrom", pos="start", as_="_start")
    .transform_formula(expr="datum._start + datum.length", as_="_end")
    .transform_formula(expr="datum._start + datum.length / 2", as_="_centroid")
    .transform_collect(sort=gs.compare(["_start"]))
    .transform_pileup(
        start="_start",
        end="_end",
        as_="_lane",
        preference="strand",
        preferredOrder=["-", "+"],
    )
    .transform_filter("datum._lane < 3")
)


chart = (
    (gc_track & conservation_track & ccre_track & sequence_track & refseq_track)
    .properties(
        assembly="hg38",
        title="Stacked hg38 genome browser tracks",
        description=(
            "Lazy signal, regulatory, sequence, and RefSeq tracks aligned to "
            "one zoomable genomic axis."
        ),
        axes={"x": gs.GenomeAxis(orient="bottom", title="Genomic position")},
        spacing=8,
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
)
