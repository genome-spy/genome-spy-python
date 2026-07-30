"""TCGA ovarian cancer GISTIC landscape.

Recurrent copy-number amplifications and deletions are shown as signed
GISTIC q-values over a shared hg19 genomic axis.
"""

import genome_spy as gs

META = {
    "category": "Copy-number plots",
    "tags": ("gistic", "copy-number", "locus", "lazy"),
    "order": 36,
    "height": 360,
    "max_width": 980,
}

DOMAIN = [
    {"chrom": "chr18", "pos": 14593640},
    {"chrom": "chr20", "pos": 22538731},
]
SCORES_URL = "https://data.genomespy.app/sample-data/TCGA-OV-GISTIC/scores.gistic"

scores = (
    gs.Chart(
        gs.Data(
            url=SCORES_URL,
            format={"type": "tsv"},
        )
    )
    .transform_formula(
        expr="datum['-log10(q-value)'] * (datum.Type == 'Del' ? -1 : 1)",
        as_="signed_q",
    )
    .mark_rect(minOpacity=1)
    .encode(
        x=gs.Locus("Chromosome", "Start"),
        x2=gs.Locus("Chromosome", "End"),
        y=gs.Y("signed_q:Q").title("Signed -log10(q-value)"),
        color=gs.Color("Type:N")
        .scale(
            domain=["Amp", "Del"],
            range=["#e45756", "#4c78a8"],
        )
        .legend(None),
    )
    .properties(height=230, title="GISTIC q-values")
)

chart = scores.properties(
    assembly="hg19",
    name="gistic-track",
    scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    description="TCGA ovarian cancer GISTIC copy-number landscape.",
)
