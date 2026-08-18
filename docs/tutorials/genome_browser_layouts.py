"""Single-source chart objects used by the linked genome tracks guide."""

import genome_spy as gs


REGION = [
    {"chrom": "chr7", "pos": 66_600_000},
    {"chrom": "chr7", "pos": 66_800_000},
]


# genome-browser-signal-start
signal_track = (
    gs.Chart(gs.lazy.bigwig("https://data.genomespy.app/genomes/hg38/hg38.gc5Base.bw"))
    .mark_rect(color="#4c78a8", minWidth=0.5, tooltip=None)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q").scale(domain=[0, 100]).axis(title="GC (%)"),
    )
    .properties(
        name="gc-content",
        height=90,
        title=gs.title("GC content", orient="left"),
    )
)
# genome-browser-signal-end


# genome-browser-annotations-start
intervals = gs.Chart().mark_rect(minWidth=0.5, tooltip=None)

interval_labels = (
    gs.Chart()
    .mark_text(fitToBand=True, color="black", size=10, tooltip=None)
    .encode(text=gs.Text("ucscLabel:N"))
    .properties(
        opacity=gs.dynamic_opacity(
            unitsPerPixel=[500, 100],
            values=[0, 1],
        )
    )
)

annotation_track = (
    (intervals + interval_labels)
    .properties(
        name="ccre-annotations",
        data=gs.lazy.bigbed(
            "https://data.genomespy.app/sample-data/encodeCcreCombined.hg38.bb"
        ),
        height=gs.step(18),
        title=gs.title("Candidate regulatory elements", orient="left"),
    )
    .encode(
        x=gs.Locus("chrom", "chromStart"),
        x2=gs.Locus("chrom", "chromEnd"),
        y=gs.Y("ucscLabel:N").axis(None),
        color=gs.Color("ucscLabel:N").legend(title="cCRE class"),
    )
)
# genome-browser-annotations-end


# genome-browser-compose-start
browser = (
    (signal_track & annotation_track)
    .properties(
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=REGION, zoom=True)),
        axes=gs.axes(
            x=gs.GenomeAxis(
                orient="bottom",
                title="Genomic position",
                chromGrid=True,
            )
        ),
        spacing=8,
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
    .configure_view(stroke="lightgray")
)
# genome-browser-compose-end


# genome-browser-scrolling-start
scrollable_annotations = annotation_track.properties(viewportHeight=120)
# genome-browser-scrolling-end


CHARTS = {"browser": browser}
