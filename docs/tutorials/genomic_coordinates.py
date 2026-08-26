"""Single-source chart objects used by the Genomic Coordinates guide."""

import genome_spy as gs

BRCA1_DOMAIN = [
    {"chrom": "chr17", "pos": 43_040_000},
    {"chrom": "chr17", "pos": 43_090_000},
]


# genomic-coordinates-points-start
variants = [
    {"chrom": "chr17", "pos": 43_044_295, "impact": "moderate"},
    {"chrom": "chr17", "pos": 43_057_481, "impact": "high"},
    {"chrom": "chr17", "pos": 43_070_977, "impact": "low"},
    {"chrom": "chr17", "pos": 43_082_144, "impact": "high"},
]

point_chart = (
    gs.Chart(variants)
    .mark_point(filled=True, size=110)
    .encode(
        x=gs.Locus("chrom", "pos").axis(title="Genomic position", chromGrid=True),
        y=gs.Y("impact:N").title("Impact"),
        color=gs.Color("impact:N").legend(None),
    )
    .properties(
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=BRCA1_DOMAIN)),
        title="Point variants on chr17",
    )
)
# genomic-coordinates-points-end


# genomic-coordinates-intervals-start
features = [
    {"chrom": "chr17", "start": 43_044_000, "end": 43_050_000, "kind": "enhancer"},
    {"chrom": "chr17", "start": 43_057_000, "end": 43_061_000, "kind": "exon"},
    {"chrom": "chr17", "start": 43_068_000, "end": 43_075_000, "kind": "enhancer"},
]

interval_chart = (
    gs.Chart(features)
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("kind:N").title("Feature kind"),
        color=gs.Color("kind:N").legend(None),
    )
    .properties(
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=BRCA1_DOMAIN)),
        title="Half-open genomic intervals",
    )
)
# genomic-coordinates-intervals-end


# genomic-coordinates-offset-start
gff_features = [
    {"seqid": "chr17", "start1": 43_044_001, "end1": 43_050_000, "name": "A"},
    {"seqid": "chr17", "start1": 43_057_001, "end1": 43_061_000, "name": "B"},
]

offset_chart = (
    gs.Chart(gff_features)
    .mark_rect(color="#4c78a8")
    .encode(
        x=gs.Locus("seqid", "start1", offset=1),
        x2=gs.Locus("seqid", "end1"),
        y=gs.Y("name:N").title("Feature"),
    )
    .properties(
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=BRCA1_DOMAIN)),
        title="One-based inclusive input",
    )
)
# genomic-coordinates-offset-end


# genomic-coordinates-custom-start
toy_genome = {
    "contigs": [
        {"name": "chrA", "size": 1_000},
        {"name": "chrB", "size": 600},
        {"name": "plasmid", "size": 250},
    ]
}
toy_features = [
    {"chrom": "chrA", "start": 100, "end": 300, "label": "alpha"},
    {"chrom": "chrB", "start": 50, "end": 220, "label": "beta"},
    {"chrom": "plasmid", "start": 20, "end": 180, "label": "gamma"},
]

custom_assembly_chart = (
    gs.Chart(toy_features)
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("label:N").axis(None),
        color=gs.Color("label:N").legend(None),
    )
    .properties(
        genomes={"toy": toy_genome},
        assembly="toy",
        title="A custom three-contig assembly",
    )
)
# genomic-coordinates-custom-end


# genomic-coordinates-multiple-start
# Orthologous gene starts from the UCSC hg38 and mm10 RefSeq annotations.
homologs = [
    {
        "gene": "BRCA1",
        "hsChrom": "chr17",
        "hsPos": 43_044_295,
        "mmChrom": "chr11",
        "mmPos": 101_488_764,
    },
    {
        "gene": "TP53",
        "hsChrom": "chr17",
        "hsPos": 7_668_421,
        "mmChrom": "chr11",
        "mmPos": 69_580_359,
    },
    {
        "gene": "MYC",
        "hsChrom": "chr8",
        "hsPos": 127_736_231,
        "mmChrom": "chr15",
        "mmPos": 61_985_341,
    },
]

multiple_assembly_chart = (
    gs.Chart(homologs)
    .mark_point(filled=True, size=120)
    .encode(
        # A chrom/pos domain is linearized without the scale's assembly, so it
        # only resolves under a root assembly. These scales carry their own.
        x=gs.Locus("hsChrom", "hsPos")
        .scale(type="locus", assembly="hg38")
        .axis(title="Human hg38", chromGrid=True),
        y=gs.Locus("mmChrom", "mmPos")
        .scale(type="locus", assembly="mm10")
        .axis(title="Mouse mm10", chromGrid=True),
        color=gs.Color("gene:N").legend(title="Gene"),
        tooltip="gene:N",
    )
    .properties(title="Orthologous genes in two assemblies")
)
# genomic-coordinates-multiple-end


CHARTS = {
    "point_chart": point_chart,
    "interval_chart": interval_chart,
    "offset_chart": offset_chart,
    "custom_assembly_chart": custom_assembly_chart,
    "multiple_assembly_chart": multiple_assembly_chart,
}
