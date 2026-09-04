"""Lollipop plot.

Mutation counts aggregated by amino-acid position are aligned above a protein
domain track. Color encodes the dominant mutation class at each site.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._mutation import dnmt3a_lollipop_data
from genome_spy.schema import Axis, Legend, Scale

META = {
    "category": "Mutation position plots",
    "order": 10,
    "height": 360,
    "max_width": 760,
}

CLASS_ORDER = [
    "Frame_Shift_Del",
    "Nonsense_Mutation",
    "Missense_Mutation",
    "Splice_Site",
]
CLASS_COLORS = (
    Scale().domain(CLASS_ORDER).range(["#5f9ed1", "#e15759", "#66b55f", "#f28e2b"])
)
DOMAIN_COLORS = (
    Scale()
    .domain(["Dnmt3b_related", "ADDz_Dnmt3a", "AdoMet_MTases"])
    .range(["#e78973", "#8094ee", "#f7c57a"])
)


def build_chart() -> gs.Chart:
    """Build the DNMT3A mutation and protein-domain visualization."""
    data = dnmt3a_lollipop_data()
    features = data["features"]
    domains = data["domains"]
    max_count = int(features["count"].max())
    x_domain = [0, data["protein_length"]]

    mutation_legend = (
        Legend()
        .title("Mutation class")
        .orient("top-left")
        .direction("horizontal")
        .columns(2)
        .symbolSize(72)
    )

    # Stems and heads inherit one prepared mutation table. Their y encodings
    # differ, while the parent owns their common amino-acid position encoding.
    # The offset carries stems through the shared-axis overhang so they meet
    # the protein schematic in the next track.
    stems = (
        gs.Chart()
        .mark_rule(color="#c0c0c0", size=1, y2Offset=32)
        .encode(
            y=gs.Y(gs.datum(0), type="quantitative")
            .scale(reverse=False, domain=[0, max_count + 4])
            .axis(title="Mutation count", values=[1, max_count], grid=False),
            y2=gs.Y2("count"),
        )
    )
    heads = (
        gs.Chart()
        .mark_point(size=88, filled=True, opacity=0.9)
        .encode(
            y=gs.Y("count:Q").scale(reverse=False, domain=[0, max_count + 4]),
            color=gs.Color("class:N").scale(CLASS_COLORS).legend(mutation_legend),
        )
    )
    # The canonical R882 hotspot is labeled without adding a display-only
    # column to the prepared mutation table.
    hotspot_label = (
        gs.Chart()
        .transform_filter(gs.datum.is_hotspot)
        .mark_text(text="R882", dy=-12, size=11, color="#111111")
        .encode(y=gs.Y("count:Q").scale(reverse=False, domain=[0, max_count + 4]))
    )
    mutation_track = (
        gs.layer(stems, heads, hotspot_label)
        .properties(data=features, height=230)
        .encode(x=gs.X("position:Q"))
    )

    # Fixed mark-space y coordinates give the protein its own compact track;
    # no artificial negative count values are needed.
    backbone = (
        gs.Chart(data["backbone"])
        .mark_rect(y=0.36, y2=0.64, color="#a8b5b6", stroke="#111111", strokeWidth=1)
        .encode(x=gs.X("start:Q"), x2=gs.X2("end"))
    )
    domain_blocks = (
        gs.Chart(domains)
        .mark_rect(
            y=0.18,
            y2=0.82,
            cornerRadius=2,
            stroke="#111111",
            strokeWidth=1,
        )
        .encode(
            x=gs.X("start:Q"),
            x2=gs.X2("end"),
            color=gs.Color("name:N").scale(DOMAIN_COLORS).legend(None),
        )
    )
    # GenomeSpy derives label centers while rendering, keeping presentation
    # geometry in the declarative dataflow instead of pandas code.
    domain_labels = (
        gs.Chart(domains)
        .transform_formula(expr=(gs.datum.start + gs.datum.end) / 2, as_="center")
        .mark_text(y=0.5, size=8, color="#111111")
        .encode(x=gs.X("center:Q"), text=gs.Text("name:N"))
    )
    protein_track = gs.layer(backbone, domain_blocks, domain_labels).properties(
        height=55
    )

    # The parent scale aligns true protein coordinates across both tracks.
    return (
        (mutation_track & protein_track)
        .properties(
            title=(
                f"{data['gene']} : "
                f"[Somatic Mutation Rate: {data['mutation_rate']:.2f}%]"
            ),
            description=(
                "A DNMT3A lollipop plot derived from the maftools TCGA LAML "
                "example, with per-position mutation counts, protein domains, "
                "and the labeled R882 hotspot."
            ),
            scales=gs.scales(x=gs.Scale(domain=x_domain, zoom=True)),
            axes=gs.axes(x=Axis(title="Amino-acid position")),
            spacing=4,
        )
        .resolve_scale(x="shared", y="independent")
        .resolve_axis(x="shared", y="independent")
    )


chart = build_chart()
