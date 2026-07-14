"""Genome tracks with gene annotations.

A real browser-style locus view on hg38: GC content from GenomeSpy's BigWig
documentation example stacked above the scored RefSeq gene-annotation track
used in the GenomeSpy docs. The lower track keeps the canonical exon packing,
label scoring, and strand arrows so the annotations stay readable as the view
zooms.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "tags": ("vconcat", "bigwig", "refseq", "lazy", "real-data"),
    "order": 10,
    "height": 320,
    "max_width": 920,
}

DOMAIN = [
    {"chrom": "chr5", "pos": 177482500},
    {"chrom": "chr5", "pos": 177518000},
]

# The top track is a compact GC-content signal rendered directly from a lazy BigWig.
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
        view={"stroke": "lightgray"},
    )
)

# The lower track mirrors GenomeSpy's scored RefSeq gene view: exon blocks,
# transcript bodies, text labels, and strand arrows all share the same locus axis.
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
        x=gs.X("_start:L").axis(title="Genomic position"),
        x2=gs.X2("_end"),
        search=gs.Search("symbol"),
    )
    .properties(name="bodies", title="Gene annotations")
)

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

labels = (
    gs.Chart()
    .mark_text(size=11, yOffset=7, tooltip={"handler": "refseqgene"})
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

# Parse the hosted RefSeq table into a browser-style packed transcript layout.
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
    .transform_linearize_genomic_coordinate(
        chrom="chrom",
        pos="start",
        as_="_start",
    )
    .transform_formula(
        expr="datum._start + datum.length",
        as_="_end",
    )
    .transform_formula(
        expr="datum._start + datum.length / 2",
        as_="_centroid",
    )
    .transform_collect(sort={"field": ["_start"]})
    .transform_pileup(
        start="_start",
        end="_end",
        as_="_lane",
        preference="strand",
        preferredOrder=["-", "+"],
    )
    .transform_filter("datum._lane < 3")
)

# Stack the quantitative signal above the packed gene model and share the x domain.
chart = (
    gs.vconcat(gc_track, refseq_track, spacing=10)
    .properties(
        assembly="hg38",
        title="GC content with RefSeq gene annotations",
        description=(
            "A real hg38 browser view combining GenomeSpy's lazy BigWig GC-content "
            "track with the scored RefSeq gene-annotation track used in the "
            "GenomeSpy documentation."
        ),
        scales={"x": {"domain": DOMAIN}},
    )
    .resolve_scale(y="independent")
    .resolve_axis(y="independent")
)
