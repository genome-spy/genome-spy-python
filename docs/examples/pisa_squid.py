"""PISA squid plot.

Brush input and output positions to explore base-to-base effects around the
Drosophila sog enhancer, with accessibility, contribution, and motif tracks.
"""

import genome_spy as gs

META = {
    "category": "Regulatory model interpretation",
    "order": 36,
    "height": 440,
    "max_width": 980,
}
DATA = "https://data.genomespy.app/datasets/bpreveal-pisa/v3/"
tracks = gs.Data(url=DATA + "fig2cd-atac-tracks.parquet", format={"type": "parquet"})
MUTED = "#d8dbe0"

# Preserve the reference palette: each effect value is paired with its color.
EFFECT_COLOR_STOPS = (
    (-0.216404, "#053061"),
    (-0.173123, "#2166ac"),
    (-0.129843, "#4393c3"),
    (-0.086562, "#92c5de"),
    (-0.043281, "#d1e5f0"),
    (0, "#ffffff"),
    (0.043281, "#fddbc7"),
    (0.086562, "#f4a582"),
    (0.129843, "#d6604d"),
    (0.173123, "#b2182b"),
    (0.216404, "#67001f"),
)
effect_scale = gs.Scale(
    domain=[value for value, _ in EFFECT_COLOR_STOPS],
    range=[color for _, color in EFFECT_COLOR_STOPS],
    clamp=True,
)

# Each track updates a selection stored in the parent view's parameter scope.
output_brush = gs.selection_interval(
    "accessibilityRegion",
    push="outer",
    persist=False,
    encodings=["x"],
    extent="view",
    on="mousedown",
    clear="dblclick",
    zoom=False,
)
input_brush = gs.selection_interval(
    "contributionRegion",
    push="outer",
    persist=False,
    encodings=["x"],
    extent="view",
    on="mousedown",
    clear="dblclick",
    zoom=False,
)
hover = gs.selection_point(
    "pisaLinkHover",
    push="outer",
    persist=False,
    on="pointerover[event.shiftKey]",
    clear="mousemove[!event.shiftKey]",
)

accessibility = (
    gs.Chart(tracks)
    .transform_filter(gs.datum.track == "prediction")
    .mark_rect(minOpacity=1)
    .encode(
        x=gs.X("position:I").title("dm6 chrX"),
        y=gs.Y("value:Q").scale(zero=True).axis(None),
        y2=gs.datum(0),
        color=gs.when(output_brush)
        .then(gs.value("#332288"))
        .otherwise(gs.value(MUTED)),
        tooltip=[
            gs.Tooltip("position").title("Output position"),
            gs.Tooltip("value").title("Prediction").format(".4g"),
        ],
    )
    .properties(
        name="prediction",
        title=gs.Title(text="Accessibility", style="overlay-title"),
        height={"grow": 0.16},
        cursor="text",
    )
    .add_params(output_brush)
)

# A projected brush tests the input (x) or output (x2) endpoint of a link.
# The final OR makes Shift-hover isolate links when both brushes are empty.
output_endpoint = gs.SelectionPredicateOperand(param=output_brush.name).project(x="x2")
input_endpoint = gs.SelectionPredicateOperand(param=input_brush.name).project(x="x")
highlighted_link = gs.SelectionPredicateDefinition(
    or_=[
        gs.SelectionPredicateOperand(param=hover.name, empty=False),
        gs.SelectionPredicateOperand(
            and_=[
                output_endpoint,
                input_endpoint,
                gs.SelectionPredicateOperand(
                    or_=[
                        gs.SelectionPredicateOperand(param=hover.name),
                        output_endpoint.empty(False),
                        input_endpoint.empty(False),
                    ]
                ),
            ]
        ),
    ]
)
highlight = gs.when(gs.NamedSelectionPredicateRef(ref="highlightedLink"))
effect_color = (
    gs.Color("effect:Q")
    .scale(effect_scale)
    .legend(
        title="PISA (log2(fc))",
        orient="left",
        direction="vertical",
        gradientLength=84,
        gradientThickness=18,
        gradientStrokeColor="#777777",
        gradientStrokeWidth=0.5,
        values=[-0.2, 0, 0.2],
    )
)
links = (
    gs.Chart(gs.Data(url=DATA + "fig2c-atac-links.parquet", format={"type": "parquet"}))
    .transform_calculate(absEffect=gs.expr.abs(gs.datum.effect))
    .mark_link(linkShape="diagonal", orient="vertical", size=1.5, minPickingSize=2)
    .encode(
        x=gs.X("source:I").title("dm6 chrX").buildIndex(False),
        x2=gs.X2("target"),
        y=gs.datum(0, type="quantitative").scale(domain=[0, 1]).axis(None),
        y2=gs.datum(1),
        order=highlight.then(gs.value(1)).otherwise(gs.value(0)),
        color=highlight.then(effect_color).otherwise(gs.value(MUTED)),
        opacity=highlight.then(
            gs.Opacity("absEffect:Q")
            .scale(
                domain=[0, 0.216404],
                range=[0, 1],
                clamp=True,
            )
            .legend(None)
        ).otherwise(gs.value(0.1)),
        tooltip=[
            gs.Tooltip("source").title("Input position"),
            gs.Tooltip("target").title("Output position"),
            gs.Tooltip("effect").title("PISA effect (log2 fold change)").format(".4f"),
        ],
    )
    .properties(name="pisa-links", predicates={"highlightedLink": highlighted_link})
    .add_params(hover)
)

# Overlay motif intervals and labels near the bottom of the link panel.
motif_blocks = (
    gs.Chart()
    .mark_rect(minOpacity=1)
    .encode(
        color=gs.Color("motifLabel:N")
        .scale(
            domain=["M1bp", "Gaga", "Zelda"],
            range=["#bbcc33", "#44bb99", "#99ddff"],
        )
        .legend(orient="left", direction="vertical", symbolOpacity=1),
        tooltip=[
            gs.Tooltip("motifLabel").title("Motif"),
            gs.Tooltip("start").title("Start"),
            gs.Tooltip("end").title("End"),
            gs.Tooltip("strand").title("Strand"),
            gs.Tooltip("score").title("Score"),
        ],
    )
)
motif_labels = (
    gs.Chart()
    .mark_text(
        align="center",
        baseline="middle",
        paddingX=3,
        tooltip=None,
    )
    .encode(text="motifLabel", color=gs.value("black"))
)
motifs = (
    (motif_blocks + motif_labels)
    .properties(
        name="motifs",
        data=gs.Data(
            url=DATA + "fig2cd-atac-motifs.parquet",
            format={"type": "parquet"},
        ),
    )
    .transform_calculate(
        motifLabel=gs.expr.if_(
            gs.datum.name == "m1bp",
            "M1bp",
            gs.expr.if_(gs.datum.name == "gaga", "Gaga", "Zelda"),
        )
    )
    .encode(
        x=gs.X("start:I").title("dm6 chrX"),
        x2="end",
        y=gs.value(gs.expr(4 / gs.Expression("height"))),
        y2=gs.value(gs.expr(20 / gs.Expression("height"))),
    )
)

# Switch from compact bars to base-colored contribution letters as we zoom in.
bars = (
    gs.Chart()
    .mark_rect(minOpacity=1)
    .encode(
        color=gs.when(input_brush).then(gs.value("#332288")).otherwise(gs.value(MUTED)),
    )
)
logo = (
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
        text="base",
        color=gs.when(input_brush)
        .then(
            gs.Color("base:N")
            .scale(
                type="ordinal",
                domain=["A", "C", "G", "T", "N"],
                range=["#009E73", "#0072B2", "#F0E442", "#D55E00", "#BDBDBD"],
            )
            .legend(None)
        )
        .otherwise(gs.value(MUTED)),
    )
)
contribution = (
    gs.multiscale(
        bars,
        logo,
        stops={
            "channel": "x",
            "values": [0.15],
            "transition": {"type": "lerp", "halfLife": 60},
        },
    )
    .properties(
        name="importance",
        data=tracks,
        height={"grow": 0.16},
        cursor="text",
        title=gs.Title(text="Contribution score", style="overlay-title"),
    )
    .transform_filter(gs.datum.track == "importance")
    .encode(
        x=gs.X("position:I").title("dm6 chrX"),
        y=gs.datum(0, type="quantitative").scale(zero=True).axis(None),
        y2="value",
        tooltip=[
            gs.Tooltip("position").title("Input position"),
            gs.Tooltip("base").title("Base"),
            gs.Tooltip("value").title("Contribution").format(".4g"),
        ],
    )
    .add_params(input_brush)
)

chart = (
    (accessibility & (links + motifs).resolve_scale(color="independent") & contribution)
    .properties(
        spacing=0,
        padding={"top": 8, "right": 30, "bottom": 8, "left": 10},
        scales=gs.scales(x=gs.Scale(domain=[15646649, 15647250], zoom=True)),
    )
    .add_params(
        gs.param("accessibilityRegion", value=None),
        gs.param("contributionRegion", value=None),
        gs.param("pisaLinkHover", value=None),
    )
    .resolve_scale(x="shared")
    .resolve_axis(x="shared")
    .resolve_legend(color="collected")
    .configure_axis(domain=False)
    .configure_legend(
        labelFontSize=11,
        titleFontSize=11,
        layout={"left": {"anchor": "middle", "wrap": False}},
    )
    .configure_legend_track(style=None)
    .configure_title(fontSize=12, fontWeight="normal", offset=2)
    .configure_view(stroke="transparent", strokeWidth=0)
)
