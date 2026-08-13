"""Dynseq binding-QTL tracks.

Sequence-logo tracks compare reference and alternate SPI1 contribution scores
over the same base-resolution locus.
"""

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "tags": ("bigwig", "fasta", "bqtl", "sequence-logo", "template"),
    "order": 34,
    "height": 300,
    "max_width": 980,
}

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
                "allele === 'ref' ? 'Reference allele (C)' : 'Alternate allele (G)'"
            ),
            style="overlay-title",
        ),
        height=120,
    )
    .transform_coordinate_lookup(
        from_={
            "data": gs.lazy.bigwig(
                gs.expr(
                    "allele === 'ref' ? "
                    "'https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
                    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/"
                    "bigwigs/chip_imp_ref.bw' : "
                    "'https://raw.githubusercontent.com/kundajelab/dynseq-paper/"
                    "febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/"
                    "bigwigs/chip_imp_alt.bw'"
                ),
                pixelsPerBin=1,
            ),
            "transform": [
                {
                    "type": "formula",
                    "expr": "datum.start",
                    "as": "pos",
                }
            ],
        },
        key=["chrom", "pos"],
        values=["score"],
    )
    .transform_filter("isValid(datum.score)")
    .transform_formula(
        expr="allele === 'alt' && datum.pos === 43720929 ? 'G' : datum.base",
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
    .transform_formula(expr="upper(datum.base)", as_="base")
    .transform_formula(expr="datum.start + datum.rawPos", as_="pos")
    .resolve_scale(y="shared")
    .resolve_axis(x="shared")
    .configure_view(fill="#FAFAFA")
)
