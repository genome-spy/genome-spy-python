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

# Real ASCAT copy-number calls for sample S96, hosted by GenomeSpy.
SEGMENTS = {
    "url": "https://data.genomespy.app/sample-data/ASCAT/segments_S96.tsv",
    "format": {"type": "tsv"},
}

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

diploid_baseline = (
    gs.Chart([{"cn": 2}])
    .mark_rule(strokeDash=[4, 4], size=1, color="#8f98a3")
    .encode(y=gs.Y("cn:Q").scale(reverse=False))
)

segments = (
    gs.Chart(SEGMENTS)
    .transform_formula(expr="datum.nMajor + datum.nMinor", as_="totalCN")
    .transform_formula(expr="datum.nMinor == 0 ? 'LOH' : 'retained'", as_="zygosity")
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

chart = (diploid_baseline + segments).properties(
    title="Allele-specific copy number (ASCAT, sample S96)",
    description="A whole-genome copy-number profile with total copy number and LOH status.",
)
