"""PISA interaction matrix.

Explore the signed effect of each input base on each ATAC-seq output position
around the Drosophila sog enhancer, with synchronized marginal tracks.
"""

import genome_spy as gs

META = {
    "category": "Regulatory model interpretation",
    "order": 37,
    "height": 500,
    "max_width": 980,
}
DATA = "https://data.genomespy.app/datasets/bpreveal-pisa/v3/"
tracks = gs.Data(url=DATA + "fig2cd-atac-tracks.parquet", format={"type": "parquet"})
INPUT_DOMAIN = [15646649, 15647250]
OUTPUT_DOMAIN = [15646499, 15647400]

# Label visibility depends on the rendered cell size in both dimensions.
label_x_span = gs.param("labelVisibilityXSpan", expr="width / 15")
label_y_span = gs.param("labelVisibilityYSpan", expr="height / 8")
x_tile_size = gs.param("labelXBinSize", value=10)
y_tile_size = gs.param("labelYBinSize", value=15)
show_labels = gs.param(
    "showCellLabels",
    expr=(
        (gs.expr.abs(gs.expr.span(gs.expr.domain("x"))) <= label_x_span)
        & (gs.expr.abs(gs.expr.span(gs.expr.domain("y"))) <= label_y_span)
    ),
)
ruler_opacity = gs.param(
    "rulerOpacity",
    expr=gs.expr.if_(show_labels, 0, 0.3),
    transition={"type": "lerp", "halfLife": 100, "epsilon": 0.01},
)
cursor = gs.ruler(
    "matrixCursor",
    persist=False,
    encodings=["x", "y"],
    extent="view",
    mark=gs.RulerMarkConfig(opacity=ruler_opacity, strokeDash=[3, 3]),
)

cells = (
    gs.Chart()
    .mark_rect(buildIndex=False, tooltip=None)
    .encode(
        x=gs.X("input:I").axis(None),
        y=gs.Y("output:I").axis(title=None, tickCount=4, grid=False),
        color=gs.Color("effect:Q")
        .scale(
            domain=[
                -0.14427,
                -0.138499,
                -0.115416,
                -0.086562,
                -0.057708,
                -0.028854,
                0,
                0.028854,
                0.057708,
                0.086562,
                0.115416,
                0.138499,
                0.14427,
            ],
            range=[
                "#18f894",
                "#053061",
                "#2166ac",
                "#4393c3",
                "#92c5de",
                "#d1e5f0",
                "#ffffff",
                "#fddbc7",
                "#f4a582",
                "#d6604d",
                "#b2182b",
                "#67001f",
                "#f81894",
            ],
            clamp=True,
        )
        .legend(
            title="PISA (log2(fc))",
            orient="left",
            direction="vertical",
            gradientLength=110,
            gradientThickness=18,
            gradientStrokeColor="#777777",
            gradientStrokeWidth=0.5,
            values=[-0.1, -0.05, 0, 0.05, 0.1],
        ),
    )
)

# One row anchors the dashed reference where input and output positions agree.
diagonal = (
    gs.Chart(tracks)
    .transform_filter(
        (gs.datum.track == "importance") & (gs.datum.position == INPUT_DOMAIN[0])
    )
    .mark_rule(
        color="#333333", opacity=0.35, size=0.75, strokeDash=[3, 3], tooltip=None
    )
    .encode(
        x=gs.datum(INPUT_DOMAIN[0], type="index"),
        x2=gs.datum(INPUT_DOMAIN[1]),
        y=gs.datum(INPUT_DOMAIN[0], type="index"),
        y2=gs.datum(INPUT_DOMAIN[1]),
    )
    .properties(name="same-position-diagonal")
)

# Stable tile bounds prevent materializing a text mark for every matrix cell.
tile_bounds = [
    gs.param(
        "labelXStart",
        expr="showCellLabels ? floor(min(domain('x')[0], domain('x')[1]) / labelXBinSize) * labelXBinSize : null",
    ),
    gs.param(
        "labelXEnd",
        expr="showCellLabels ? ceil(max(domain('x')[0], domain('x')[1]) / labelXBinSize) * labelXBinSize : null",
    ),
    gs.param(
        "labelYStart",
        expr="showCellLabels ? floor(min(domain('y')[0], domain('y')[1]) / labelYBinSize) * labelYBinSize : null",
    ),
    gs.param(
        "labelYEnd",
        expr="showCellLabels ? ceil(max(domain('y')[0], domain('y')[1]) / labelYBinSize) * labelYBinSize : null",
    ),
]
labels = (
    gs.Chart()
    .add_params(*tile_bounds)
    .transform_collect()
    .transform_filter(
        "showCellLabels && datum.input >= labelXStart && datum.input < labelXEnd && datum.output >= labelYStart && datum.output < labelYEnd"
    )
    .mark_text(
        size=10,
        opacity=0.85,
        fitToBand=True,
        paddingX=2.5,
        paddingY=2.5,
        buildIndex=False,
        tooltip=None,
    )
    .encode(
        x=gs.X("input:I").axis(None),
        y="output:I",
        text=gs.Text("effect").format(".2f"),
        color=gs.Color("effect:Q")
        .scale(
            type="threshold",
            domain=[-0.138499, -0.06, 0.06, 0.138499],
            range=["#222222", "#ffffff", "#222222", "#ffffff", "#222222"],
        )
        .legend(None),
    )
    .properties(name="cell-labels")
)

# Motif annotations keep a fixed height near the bottom of the matrix.
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
        motifLabel="datum.name == 'm1bp' ? 'M1bp' : datum.name == 'gaga' ? 'Gaga' : 'Zelda'"
    )
    .encode(
        x=gs.X("start:I").axis(None),
        x2="end",
        y=gs.value(gs.expr("4 / height")),
        y2=gs.value(gs.expr("20 / height")),
    )
)
matrix = (
    (cells + diagonal + labels + motifs)
    .properties(
        name="pisa-matrix",
        view=gs.view(stroke="gray"),
        data=gs.Data(
            url=DATA + "fig2d-atac-matrix.parquet",
            format={"type": "parquet"},
        ),
    )
    .add_params(
        cursor,
        label_x_span,
        label_y_span,
        x_tile_size,
        y_tile_size,
        show_labels,
        ruler_opacity,
    )
    .resolve_scale(color="independent")
)

# The right margin shares genomic y with the matrix, but has its own value x.
accessibility = (
    gs.Chart(tracks)
    .transform_filter(gs.datum.track == "prediction")
    .mark_rect(color="#332288", minOpacity=1)
    .encode(
        x=gs.X("value:Q").scale(type="linear", zero=True).axis(None),
        x2=gs.datum(0),
        y=gs.Y("position:I").axis(None),
        tooltip=[
            gs.Tooltip("position").title("Output position"),
            gs.Tooltip("value").title("Accessibility").format(".4g"),
        ],
    )
    .properties(
        name="accessibility",
        width=60,
        title=gs.Title(
            text="Accessibility",
            style="overlay-title",
            orient="right",
            anchor="start",
            angle=90,
            dx=5,
        ),
    )
    .properties(resolve={"scale": {"x": "excluded"}})
)

# The bottom margin shares genomic x; zooming changes bars into sequence letters.
bars = gs.Chart().mark_rect(color="#332288", minOpacity=1)
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
        color=gs.Color("base:N")
        .scale(
            type="ordinal",
            domain=["A", "C", "G", "T", "N"],
            range=["#009E73", "#0072B2", "#F0E442", "#D55E00", "#BDBDBD"],
        )
        .legend(None),
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
        width={"grow": 1},
        height=60,
        title=gs.Title(text="Contribution score", style="overlay-title", dx=5),
    )
    .transform_filter(gs.datum.track == "importance")
    .encode(
        x=gs.X("position:I").title("dm6 chrX"),
        y=gs.datum(0, type="quantitative").scale(type="linear", zero=True).axis(None),
        y2="value",
        tooltip=[
            gs.Tooltip("position").title("Input position"),
            gs.Tooltip("base").title("Base"),
            gs.Tooltip("value").title("Contribution").format(".4g"),
        ],
    )
    .resolve_scale(y="excluded")
)

# A three-cell grid aligns both margins with the matrix without a dummy panel.
chart = (
    gs.concat(matrix, accessibility, contribution, columns=2, spacing=2)
    .properties(
        scales=gs.scales(
            x=gs.Scale(type="index", domain=INPUT_DOMAIN),
            y=gs.Scale(type="index", domain=OUTPUT_DOMAIN, reverse=True),
        )
    )
    .resolve_scale(x="shared", y="shared", color="independent")
    .resolve_axis(x="independent", y="independent")
    .resolve_legend(color="collected")
    .configure_axis(domain=False, grid=False, labelFontSize=10, titleFontSize=10)
    .configure_legend(layout={"left": {"anchor": "middle", "wrap": False}})
    .configure_legend_track(style=None)
    .configure_title(fontSize=12, fontWeight="normal", offset=2)
)
