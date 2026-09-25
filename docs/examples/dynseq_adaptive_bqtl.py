"""Adaptive dynseq binding-QTL tracks.

Reference and alternate SPI1 contribution scores switch from sequence-logo
letters to labeled bars as the reader zooms in.
"""

import genome_spy as gs

META = {
    "category": "Regulatory model interpretation",
    "order": 35,
    "height": 300,
    "max_width": 980,
    "thumbnail_stage_width": 696,
    "thumbnail_fit": False,
    "thumbnail_x_domain": [
        {"chrom": "chr22", "pos": 43720912},
        {"chrom": "chr22", "pos": 43720947},
    ],
}
# Cross-fade when bases are about 11–18 pixels wide. The stops are genomic
# units (base pairs) per screen pixel.
REPRESENTATION_TRANSITION = [0.09, 0.055]
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


def _allele_track(*, alternate: bool):
    bigwig_url = ALT_BIGWIG_URL if alternate else REF_BIGWIG_URL
    title = "Alternate allele (G)" if alternate else "Reference allele (C)"
    base_color = (
        gs.Color("base:N")
        .scale(
            domain=["A", "C", "G", "T"],
            range=["green", "blue", "orange", "red"],
        )
        .legend(None)
    )
    score_tooltip = [
        gs.Tooltip("base:N").title("Base"),
        gs.Tooltip("score:Q").title("Score"),
    ]

    # At detailed zoom, bars carry the magnitude while normal letters sit
    # inside them and disappear when a bar is too small for a legible label.
    score_bars = (
        gs.Chart()
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "pos"),
            y=gs.datum(0, type="quantitative")
            .scale(zero=True, nice=False, reverse=False)
            .axis(title="Score"),
            y2=gs.Y2("score"),
            color=base_color,
            tooltip=score_tooltip,
        )
    )
    bar_labels = (
        gs.Chart()
        .mark_text(
            font="Source Sans Pro",
            fontWeight=700,
            size=18,
            fitToBand=True,
            paddingX=2,
            paddingY=2,
            color="white",
            tooltip=None,
        )
        .encode(
            x=gs.Locus("chrom", "pos"),
            y=gs.datum(0, type="quantitative"),
            y2=gs.Y2("score"),
            text=gs.Text("base"),
        )
    )
    bar_representation = gs.layer(score_bars, bar_labels).properties(
        opacity=gs.dynamic_opacity(
            unitsPerPixel=REPRESENTATION_TRANSITION,
            values=[0, 1],
        )
    )

    # At wider genomic windows, retain the familiar sequence-logo view.
    logo_representation = (
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
            y=gs.datum(0, type="quantitative"),
            y2=gs.Y2("score"),
            text=gs.Text("base"),
            color=base_color,
            tooltip=score_tooltip,
        )
        .properties(
            opacity=gs.dynamic_opacity(
                unitsPerPixel=REPRESENTATION_TRANSITION,
                values=[1, 0],
            ),
        )
    )

    track = (
        gs.layer(
            gs.Chart([{}])
            .mark_rule()
            .encode(
                y=gs.datum(0, type="quantitative"),
                color=gs.value("gray"),
            ),
            bar_representation,
            logo_representation,
        )
        .properties(
            title=gs.Title(text=title, style="overlay-title"),
            height=120,
            data=gs.lazy.indexed_fasta(
                "https://data.genomespy.app/genomes/hg38/hg38.fa"
            ),
        )
        .transform_flatten_sequence(field="sequence", as_=["rawPos", "base"])
        .transform_formula(expr=gs.expr.upper(gs.datum.base), as_="base")
        .transform_formula(expr=gs.datum.start + gs.datum.rawPos, as_="pos")
        .transform_coordinate_lookup(
            from_={
                "data": gs.lazy.bigwig(bigwig_url, pixelsPerBin=1),
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
    )
    if alternate:
        track = track.transform_formula(
            expr=gs.expr.if_(gs.datum.pos == 43720929, "G", gs.datum.base),
            as_="base",
            description=(
                "Show the rs5764238 alternate allele while retaining the shared "
                "reference FASTA source."
            ),
        )
    return track


chart = (
    gs.vconcat(
        _allele_track(alternate=False),
        _allele_track(alternate=True),
    )
    .properties(
        assembly="hg38",
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
        description=(
            "Reference and alternate SPI1 contribution tracks that transition "
            "from sequence letters to labeled bars when zoomed in. Data source: "
            "https://github.com/kundajelab/dynseq-paper"
        ),
    )
    .resolve_scale(y="shared")
    .resolve_axis(x="shared")
    .configure_view(fill="#FAFAFA")
)
