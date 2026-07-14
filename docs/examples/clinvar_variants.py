"""ClinVar variants track.

A ClinVar small-variant classification view adapted from the GenomeSpy docs,
using a lazy VCF source and categorical germline classifications over a focused
hg38 locus.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Lollipop and pathogenicity plots",
    "tags": ("vcf", "clinvar", "lazy", "variants", "layer", "real-data"),
    "order": 24,
    "height": 260,
    "max_width": 920,
}

classification_domain = [
    "Pathogenic",
    "Likely pathogenic",
    "Uncertain significance",
    "Likely benign",
    "Benign",
    "Conflicting",
]

# A faint baseline makes it easier to compare classes with sparse variant counts.
baseline = (
    gs.Chart([{}])
    .mark_rule(color="lightgray")
    .encode(y=gs.Y({"datum": "Uncertain significance"}, type="ordinal"))
    .properties(name="baseline")
)

# Split each variant into a stem and a point so pathogenicity reads like a lollipop
# track instead of a bare scatter plot.
sticks = (
    gs.Chart()
    .mark_rule(tooltip=False)
    .encode(y2=gs.Y2({"datum": "Uncertain significance"}))
    .properties(name="sticks")
)

balls = gs.Chart().mark_point(size=80, geometricZoomBound=13).properties(name="balls")

# Load ClinVar lazily from bgzip-compressed VCF and keep the locus domain focused
# on a small BRCA2 region so the categorical classes stay readable.
variants = (
    gs.layer(sticks, balls)
    .properties(
        data=gs.lazy.vcf(
            "https://data.genomespy.app/sample-data/clinvar_20241215.vcf.gz",
            addChrPrefix=True,
            windowSize=1_000_000,
        ),
        scales={
            "x": {
                "domain": [
                    {"chrom": "chr18", "pos": 31524101},
                    {"chrom": "chr18", "pos": 31525003},
                ]
            }
        },
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
    # ClinVar stores classification strings in INFO fields; normalize them into a
    # compact set of labels that works well for color and y-axis ordering.
    .transform_formula(
        expr="replace(datum.INFO['CLNSIG'], /_/g, ' ')",
        as_="Germline classification",
    )
    .transform(
        {
            "type": "regexExtract",
            "field": "Germline classification",
            "regex": "^([^/]+)",
            "as": "Germline classification",
        }
    )
    .transform_formula(
        expr="replace(datum['Germline classification'], /^Conflicting.*/g, 'Conflicting')",
        as_="Germline classification",
    )
    .transform_filter(
        "datum['Germline classification'] == 'Pathogenic' || datum['Germline classification'] == 'Likely pathogenic' || datum['Germline classification'] == 'Uncertain significance' || datum['Germline classification'] == 'Likely benign' || datum['Germline classification'] == 'Benign' || datum['Germline classification'] == 'Conflicting'"
    )
)

chart = gs.layer(baseline, variants).properties(
    assembly="hg38",
    name="clinvar",
    title=gs.title("ClinVar Variants", style="overlay"),
    description=(
        "A ClinVar germline classification track adapted from the GenomeSpy docs."
    ),
    height=gs.step(13),
    view={"fill": "#f8f8f8"},
)
