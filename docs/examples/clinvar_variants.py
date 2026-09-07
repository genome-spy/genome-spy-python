"""ClinVar variants track.

A categorical variant track with stems and points for germline classification.
Colors encode pathogenicity classes across a focused genomic locus.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Mutation position plots",
    "order": 24,
    "height": 145,
    "max_width": 920,
}

# Keep classifications in this order on the vertical axis.
classification_domain = [
    "Pathogenic",
    "Likely pathogenic",
    "Uncertain significance",
    "Likely benign",
    "Benign",
    "Conflicting",
]

# Draw a reference line at "Uncertain significance".
baseline = (
    gs.Chart([{}])
    .mark_rule(color="lightgray")
    .encode(y=gs.Y(gs.datum("Uncertain significance"), type="ordinal"))
    .properties(name="baseline")
)

# Connect each variant point to the reference line with a thin stem.
sticks = (
    gs.Chart()
    .mark_rule(tooltip=False)
    .encode(y2=gs.Y2(gs.datum("Uncertain significance")))
    .properties(name="sticks")
)

# Let variant points grow as the reader zooms in.
balls = gs.Chart().mark_point(size=80, geometricZoomBound=13).properties(name="balls")

# Load variants for the region being viewed, starting on chromosome 18.
variants = (
    gs.layer(sticks, balls)
    .properties(
        data=gs.lazy.vcf(
            "https://data.genomespy.app/sample-data/clinvar_20241215.vcf.gz",
            addChrPrefix=True,
            windowSize=1_000_000,
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr18", "pos": 31524101},
                    {"chrom": "chr18", "pos": 31525003},
                ]
            )
        ),
    )
    .encode(
        x=gs.Locus("CHROM", "POS", offset=1).axis(title="Genomic position", grid=False),
        y=gs.Y("Germline classification:O")
        .scale(domain=classification_domain)
        .axis(title="Classification"),
        color=gs.Color("Germline classification:O").scale(
            domain=classification_domain,
            range=[
                "firebrick",
                "orange",
                "#f0f000",
                "#00a000",
                "darkgreen",
                "gray",
            ],
        ),
    )
    # Shorten the ClinVar classifications to match the labels above.
    .transform_formula(
        expr=gs.expr.replace(
            gs.datum.INFO["CLNSIG"],
            gs.expr.regexp("_", "g"),
            " ",
        ),
        as_="Germline classification",
    )
    .transform_regex_extract(
        field="Germline classification",
        regex="^([^/]+)",
        as_="Germline classification",
    )
    .transform_formula(
        expr=gs.expr.replace(
            gs.datum["Germline classification"],
            gs.expr.regexp(r"^Conflicting.*", "g"),
            "Conflicting",
        ),
        as_="Germline classification",
    )
    .transform_filter(
        (gs.datum["Germline classification"] == "Pathogenic")
        | (gs.datum["Germline classification"] == "Likely pathogenic")
        | (gs.datum["Germline classification"] == "Uncertain significance")
        | (gs.datum["Germline classification"] == "Likely benign")
        | (gs.datum["Germline classification"] == "Benign")
        | (gs.datum["Germline classification"] == "Conflicting")
    )
)

# Combine the reference line and variants on a pale background.
chart = (
    gs.layer(baseline, variants)
    .properties(
        assembly="hg38",
        name="clinvar",
        title=gs.title("ClinVar Variants", style="overlay"),
        description="A lollipop-style ClinVar track colored by germline classification.",
        height=gs.step(13),
    )
    .configure_view(fill="#f8f8f8")
)
