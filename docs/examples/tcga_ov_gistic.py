"""TCGA ovarian cancer GISTIC landscape.

Recurrent copy-number scores and their amplification and deletion peaks are
shown over a shared hg19 genomic axis.
"""

import genome_spy as gs
from genome_spy.datasets._gistic import tcga_ov_gistic_data

META = {
    "category": "Copy-number plots",
    "tags": ("gistic", "copy-number", "locus", "transforms"),
    "order": 36,
    "height": 280,
    "max_width": 980,
}

event_colors = gs.Scale(
    domain=["Amp", "Del"],
    range=["#e45756", "#4c78a8"],
)

data = tcga_ov_gistic_data()

zero_line = (
    gs.Chart([{"value": 0}])
    .mark_rule(color="black", opacity=0.3)
    .encode(y=gs.Y("value:Q").title(None))
    .properties(name="zero-line")
)

q_values = (
    gs.Chart(data["scores"])
    .transform_formula(
        expr="datum['-log10(q-value)'] * (datum.Type == 'Del' ? -1 : 1)",
        as_="-log10(q-value)",
    )
    .mark_rect(minOpacity=1)
    .encode(
        x=gs.Locus("Chromosome", "Start"),
        x2=gs.Locus("Chromosome", "End"),
        y=gs.Y("-log10(q-value):Q"),
        color=gs.Color("Type:N").scale(event_colors),
    )
    .properties(name="q-value-rects")
)

thresholds = (
    gs.Chart([{"value": 0.602}, {"value": -0.602}])
    .mark_rule(strokeDash=[3, 1], color="black", opacity=0.3)
    .encode(y=gs.Y("value:Q").title(None))
    .properties(name="q-value-thresholds")
)

score_track = gs.layer(zero_line, q_values, thresholds).properties(
    name="gistic-q-value",
    title=gs.Title(
        text="GISTIC q-values from the TCGA OV-TP cohort",
        style="overlay-title",
    ),
)

lesion_track = (
    gs.Chart(data["lesions"])
    .transform_regex_extract(
        field="Unique Name",
        regex=r"^(Amplification|Deletion) Peak[ ]+\d+$",
        as_=["Type"],
        skipInvalidInput=True,
    )
    .transform_filter("!!datum.Type")
    .transform_regex_fold(
        columnRegex=[r"^(.*) Limits$"],
        asValue=["limits"],
        asKey="Segment type",
    )
    .transform_regex_extract(
        field="limits",
        regex=r"^(chr[^:]+):(\d+)-(\d+)",
        as_=["Chrom", "Start", "End"],
    )
    .transform_project(
        fields=[
            "Segment type",
            "Chrom",
            "Start",
            "End",
            "Type",
            "Descriptor",
            "q values",
        ]
    )
    .mark_rule(minLength=2)
    .encode(
        x=gs.Locus("Chrom", "Start"),
        x2=gs.Locus("Chrom", "End"),
        y=gs.Y("Type:N")
        .scale(domain=["Amplification", "Deletion"], padding=0.2)
        .title(None),
        color=gs.Color("Type:N").scale(
            domain=["Amplification", "Deletion"],
            range=["#e45756", "#4c78a8"],
        ),
        opacity=gs.Opacity("Segment type:N").scale(
            type="ordinal",
            domain=["Wide Peak", "Peak", "Region"],
            range=[0.3, 1, 0.3],
        ),
        size=gs.Size("Segment type:N").scale(
            type="ordinal",
            domain=["Wide Peak", "Peak", "Region"],
            range=[11, 15, 2],
        ),
    )
    .properties(
        name="gistic-all-lesions",
        title=gs.Title(text="Regions and peaks", orient="none"),
        height=gs.step(20),
    )
)

chart = (
    gs.vconcat(score_track, lesion_track)
    .properties(
        assembly="hg19",
        name="gistic-track",
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr18", "pos": 14593640},
                    {"chrom": "chr20", "pos": 22538731},
                ]
            )
        ),
        description="TCGA OV-TP GISTIC2 copy-number scores and recurrent lesions.",
    )
    .resolve_axis(x="shared")
    .configure_legend(disable=True)
    .configure_view(stroke="lightgray")
)
