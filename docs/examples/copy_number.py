"""Copy-number profile.

Allele-specific copy-number segments drawn across the genome on a locus axis.
Segment height shows total copy number, while color highlights loss of
heterozygosity.
"""

import genome_spy as gs
from genome_spy.schema import GenomeAxis, Scale

META = {
    "category": "Copy-number plots",
    "order": 10,
    "height": 300,
}

# Use the hosted ASCAT segment estimates for sample S96.
SEGMENTS = {
    "url": "https://data.genomespy.app/sample-data/ASCAT/segments_S96.tsv",
    "format": {"type": "tsv"},
}

# Label chromosomes and separate them with alternating backgrounds.
axis = (
    GenomeAxis()
    .title("Genomic position")
    .chromGrid(True)
    .chromGridOpacity(0.12)
    .chromGridFillEven("#f4f6fb")
    .chromGridFillOdd("#ffffff")
    .chromLabels(True)
    .chromLabelFontSize(11)
    .chromTicks(True)
    .grid(False)
)

# Mark two copies as a reference line.
diploid_baseline = (
    gs.Chart([{"cn": 2}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(y=gs.Y("cn:Q").scale(reverse=False))
)

# Add both allele counts and highlight segments where the minor count is zero.
segments = (
    gs.Chart(SEGMENTS)
    .transform_formula(expr=gs.datum.nMajor + gs.datum.nMinor, as_="totalCN")
    .transform_formula(
        expr=gs.expr.if_(gs.datum.nMinor == 0, "LOH", "retained"),
        as_="zygosity",
    )
    .mark_rect()
    .encode(
        x=gs.Locus("chr", "startpos").scale(assembly="hg38").axis(axis),
        x2=gs.Locus("chr", "endpos"),
        y=gs.Y("totalCN:Q").scale(reverse=False, zero=True).title("Total copy number"),
        color=gs.Color("zygosity:N")
        .scale(Scale().domain(["retained", "LOH"]).range(["#5b8fd6", "#c53b2c"]))
        .legend(title="Heterozygosity"),
    )
)

# Combine the copy-number segments and the reference line.
chart = (diploid_baseline + segments).properties(
    title="Allele-specific copy number (ASCAT, sample S96)",
    description="A whole-genome copy-number profile with total copy number and LOH status.",
)
