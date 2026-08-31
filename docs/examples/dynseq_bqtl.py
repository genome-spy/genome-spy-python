"""Dynseq binding-QTL tracks.

Sequence-logo tracks compare reference and alternate SPI1 contribution scores
over the same base-resolution locus.
"""

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 34,
    "height": 300,
    "max_width": 980,
}
ALLELE = gs.Expression("allele")
REF_BIGWIG_URL = (
    "https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/"
    "bigwigs/chip_imp_ref.bw"
)
ALT_BIGWIG_URL = (
    "https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/"
    "bigwigs/chip_imp_alt.bw"
)

allele_track = (
    gs.layer(
        gs.Chart(
            [{}],
        )
        .mark_rule()
        .encode(
            y=gs.datum(0, type="quantitative"),
            color=gs.value("gray"),
        )
        .properties(name="baseline"),
        gs.Chart()
        .mark_text(
            font="Source Sans Pro",
            fontWeight=700,
            size=100,
            squeeze=True,
            fitToBand=True,
            paddingX=0,
            paddingY=0,
            logoLetters=True,
        )
        .encode(
            x=gs.Locus("chrom", "pos"),
            y=gs.datum(0, type="quantitative")
            .scale(zero=True, nice=False, reverse=False)
            .axis(title="Score"),
            y2=gs.Y2("score"),
            text=gs.Text("base"),
            color=gs.Color("base:N")
            .scale(
                domain=["A", "C", "G", "T"],
                range=["green", "blue", "orange", "red"],
            )
            .legend(None),
            tooltip=[
                gs.Tooltip("base:N"),
                gs.Tooltip("score:Q"),
            ],
        )
        .properties(name="dynseq"),
    )
    .properties(
        params=[gs.param("allele", value="ref")],
        title=gs.Title(
            text=gs.expr(
                gs.expr.if_(
                    ALLELE == "ref",
                    "Reference allele (C)",
                    "Alternate allele (G)",
                )
            ),
            style="overlay-title",
        ),
        height=120,
    )
    .transform_coordinate_lookup(
        from_={
            "data": gs.lazy.bigwig(
                gs.expr(gs.expr.if_(ALLELE == "ref", REF_BIGWIG_URL, ALT_BIGWIG_URL)),
                pixelsPerBin=1,
            ),
            "transform": [
                {
                    "type": "formula",
                    "expr": gs.datum.start,
                    "as": "pos",
                }
            ],
        },
        key=["chrom", "pos"],
        values=["score"],
    )
    .transform_filter(gs.expr.isValid(gs.datum.score))
    .transform_formula(
        expr=gs.expr.if_(
            (ALLELE == "alt") & (gs.datum.pos == 43720929),
            "G",
            gs.datum.base,
        ),
        as_="base",
        description=(
            "Show the rs5764238 alternate allele while retaining the shared "
            "reference FASTA source."
        ),
    )
)

chart = (
    gs.vconcat(
        gs.import_view(template="allele-track", params={"allele": "ref"}),
        gs.import_view(template="allele-track", params={"allele": "alt"}),
    )
    .properties(
        assembly="hg38",
        data=gs.lazy.indexed_fasta("https://data.genomespy.app/genomes/hg38/hg38.fa"),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr22", "pos": 43720850},
                    {"chrom": "chr22", "pos": 43720960},
                ],
                zoom={
                    "extent": [
                        {"chrom": "chr22", "pos": 43719872},
                        {"chrom": "chr22", "pos": 43721985},
                    ]
                },
            )
        ),
        templates={"allele-track": allele_track},
        description=(
            "Reference and alternate SPI1 contribution logos for rs5764238. "
            "Data source: https://github.com/kundajelab/dynseq-paper"
        ),
    )
    .transform_flatten_sequence(field="sequence", as_=["rawPos", "base"])
    .transform_formula(expr=gs.expr.upper(gs.datum.base), as_="base")
    .transform_formula(expr=gs.datum.start + gs.datum.rawPos, as_="pos")
    .resolve_scale(y="shared")
    .resolve_axis(x="shared")
    .configure_view(fill="#FAFAFA")
)
