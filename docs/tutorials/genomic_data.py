"""Single-source chart objects used by the indexed genomic data guide."""

import genome_spy as gs


REGION = [
    {"chrom": "chr7", "pos": 66_600_000},
    {"chrom": "chr7", "pos": 66_800_000},
]


# genomic-data-bigwig-start
bigwig_chart = (
    gs.Chart(gs.lazy.bigwig("https://data.genomespy.app/genomes/hg38/hg38.gc5Base.bw"))
    .mark_rect(color="#4c78a8", minWidth=0.5, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "start").scale(domain=REGION),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q").scale(domain=[0, 100]).axis(title="GC (%)"),
    )
    .properties(assembly="hg38", title="Lazy BigWig signal")
)
# genomic-data-bigwig-end


# genomic-data-bigbed-start
bigbed_chart = (
    gs.Chart(
        gs.lazy.bigbed(
            "https://data.genomespy.app/sample-data/encodeCcreCombined.hg38.bb"
        )
    )
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "chromStart").scale(domain=REGION),
        x2=gs.Locus("chrom", "chromEnd"),
        color=gs.Color("ucscLabel:N").legend(title="cCRE class"),
    )
    .properties(assembly="hg38", title="Lazy BigBed intervals")
)
# genomic-data-bigbed-end


CHARTS = {
    "bigwig_chart": bigwig_chart,
    "bigbed_chart": bigbed_chart,
}
