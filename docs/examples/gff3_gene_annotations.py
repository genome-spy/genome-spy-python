"""GFF3 gene annotations.

A browser-style gene-annotation track built from a GFF3 source. Layered marks
separate transcript bodies, exon structure, UTRs, and transcript labels within
one shared locus view.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "tags": ("gff3", "lazy", "genes", "layer", "real-data"),
    "order": 15,
    "height": 430,
    "max_width": 920,
}

DOMAIN = [
    {"chrom": "chr5", "pos": 177482500},
    {"chrom": "chr5", "pos": 177518000},
]

# A transparent but wide rule layer makes transcript tooltips easier to hit.
transcript_tooltip_trap = (
    gs.Chart()
    .mark_rule(color="#b0b0b0", opacity=0, size=7)
    .properties(name="gencode-tooltip-trap", title="GENCODE transcript")
)

transcript_body = (
    gs.Chart()
    .mark_rule(color="#b0b0b0", tooltip=None)
    .properties(name="gencode-transcript-body")
)

transcript_layer = gs.layer(transcript_tooltip_trap, transcript_body).properties(
    name="gencode-transcript"
)

# Flatten the nested GFF3 child features once so exons, CDS blocks, and UTRs can
# be drawn with ordinary encodings.
exon_base = (
    gs.Chart()
    .transform_flatten(fields=["_child_features"])
    .transform_flatten(fields=["_child_features"], as_=["child_feature"])
    .transform_project(
        fields=[
            "gene_name",
            "_lane",
            "child_feature.type",
            "child_feature.seq_id",
            "child_feature.start",
            "child_feature.end",
            "child_feature.attributes.exon_number",
            "child_feature.attributes.exon_id",
        ],
        as_=[
            "gene_name",
            "_lane",
            "type",
            "seq_id",
            "start",
            "end",
            "exon_number",
            "exon_id",
        ],
    )
)

exon_rects = (
    exon_base.mark_rect(
        minWidth=0.5,
        minOpacity=0.5,
        stroke="#505050",
        fill="#fafafa",
        strokeWidth=1,
    )
    .transform_filter("datum.type == 'exon'")
    .properties(title="GENCODE exon")
)

utr_cds_rects = (
    exon_base.mark_rect(
        minWidth=0.5,
        minOpacity=0,
        strokeWidth=1,
        strokeOpacity=0,
        stroke="gray",
    )
    .transform_filter(
        "datum.type != 'exon' && datum.type != 'start_codon' && datum.type != 'stop_codon'"
    )
    .encode(
        fill=gs.Fill("type:N").scale(
            domain=["five_prime_UTR", "CDS", "three_prime_UTR"],
            range=["#83bcb6", "#ffbf79", "#d6a5c9"],
        )
    )
    .properties(title="GENCODE exon")
)

utr_labels = (
    exon_base.mark_text(
        color="black",
        size=11,
        opacity=0.7,
        paddingX=2,
        paddingY=1.5,
        tooltip=None,
    )
    .transform_filter(
        "datum.type == 'three_prime_UTR' || datum.type == 'five_prime_UTR'"
    )
    .transform_formula(
        expr="datum.type == 'three_prime_UTR' ? \"3'\" : \"5'\"",
        as_="label",
    )
    .encode(text=gs.Text("label:N"))
)

exon_layer = gs.layer(exon_rects, utr_cds_rects, utr_labels).properties(
    name="gencode-exons"
)

# Transcript names are derived from attributes and annotated with strand direction.
transcript_labels = (
    gs.Chart()
    .mark_text(size=10, yOffset=12, tooltip=None, color="#505050")
    .transform_formula(
        expr="(datum.strand == '-' ? '< ' : '') + datum.transcript_name + ' - ' + datum.transcript_id + (datum.strand == '+' ? ' >' : '')",
        as_="label",
    )
    .encode(text=gs.Text("label:N"))
    .properties(name="gencode-transcript-labels")
)

# Load the lazy GFF3 source and project transcript-level records into a packed
# browser track with exon structure preserved.
chart = (
    gs.layer(transcript_layer, exon_layer, transcript_labels)
    .properties(
        title="GENCODE GFF3 gene annotations",
        description=(
            "A packed gene-annotation track showing transcript bodies, exons, "
            "UTRs, and labels within one locus view."
        ),
        assembly="hg38",
        height=gs.step(28),
        viewportHeight="container",
        data=gs.lazy.gff3(
            "https://data.genomespy.app/sample-data/gencode.v43.annotation.sorted.gff3.gz",
            windowSize=2_000_000,
            debounceDomainChange=300,
        ),
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    )
    .encode(
        x=gs.Locus("seq_id", "start", offset=1),
        x2=gs.Locus("seq_id", "end"),
        y=gs.Y("_lane", type="index")
        .scale(zoom=False, reverse=True, domain=[0, 40], padding=0.5)
        .axis(None),
    )
    .transform({"type": "flatten"})
    .transform_formula(expr="datum.attributes.gene_name", as_="gene_name")
    .transform_flatten(fields=["child_features"])
    .transform_flatten(fields=["child_features"], as_=["child_feature"])
    .transform_project(
        fields=[
            "gene_name",
            "child_feature.type",
            "child_feature.strand",
            "child_feature.seq_id",
            "child_feature.start",
            "child_feature.end",
            "child_feature.attributes.gene_type",
            "child_feature.attributes.transcript_type",
            "child_feature.attributes.gene_id",
            "child_feature.attributes.transcript_id",
            "child_feature.attributes.transcript_name",
            "child_feature.attributes.tag",
            "source",
            "child_feature.child_features",
        ],
        as_=[
            "gene_name",
            "type",
            "strand",
            "seq_id",
            "start",
            "end",
            "gene_type",
            "transcript_type",
            "gene_id",
            "transcript_id",
            "transcript_name",
            "tag",
            "source",
            "_child_features",
        ],
    )
    .transform_collect(sort=gs.compare(["seq_id", "start", "transcript_id"]))
    .transform_pileup(start="start", end="end", as_="_lane")
    .configure_view(stroke="lightgray")
)
