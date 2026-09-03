"""Single-source chart objects used by the interaction guide."""

import genome_spy as gs
from genome_spy.schema import (
    AxisGenomeData,
    BrushConfig,
    IntervalSelectionConfig,
    SelectionDomainRef,
)


VARIANTS = [
    {
        "id": "v1",
        "chrom": "chr17",
        "pos": 43_044_295,
        "score": 0.42,
        "depth": 38,
        "impact": "moderate",
    },
    {
        "id": "v2",
        "chrom": "chr17",
        "pos": 43_057_481,
        "score": 0.91,
        "depth": 72,
        "impact": "high",
    },
    {
        "id": "v3",
        "chrom": "chr17",
        "pos": 43_070_977,
        "score": 0.27,
        "depth": 51,
        "impact": "low",
    },
    {
        "id": "v4",
        "chrom": "chr17",
        "pos": 43_082_144,
        "score": 0.73,
        "depth": 64,
        "impact": "high",
    },
]

REGION = [
    {"chrom": "chr17", "pos": 43_040_000},
    {"chrom": "chr17", "pos": 43_090_000},
]

VARIANT_DOMAIN = ["v1", "v2", "v3", "v4"]
MIN_SCORE = gs.Expression("minScore")
DETAIL_REGION = [
    {"chrom": "chr6", "pos": 20_000_000},
    {"chrom": "chr11", "pos": 40_000_000},
]
BRUSH_VARIANTS = [
    {"id": "g1", "chrom": "chr1", "pos": 45_000_000, "score": 0.42, "depth": 38},
    {"id": "g2", "chrom": "chr7", "pos": 35_000_000, "score": 0.91, "depth": 72},
    {"id": "g3", "chrom": "chr9", "pos": 60_000_000, "score": 0.27, "depth": 51},
    {"id": "g4", "chrom": "chr11", "pos": 20_000_000, "score": 0.73, "depth": 64},
    {"id": "g5", "chrom": "chr17", "pos": 43_000_000, "score": 0.58, "depth": 46},
    {"id": "g6", "chrom": "chr20", "pos": 30_000_000, "score": 0.36, "depth": 57},
]


# interaction-zoom-start
zoom_chart = (
    gs.Chart(VARIANTS)
    .mark_point(filled=True, size=110)
    .encode(
        x=gs.Locus("chrom", "pos").scale(domain=REGION).axis(title="Genomic position"),
        y=gs.Y("score:Q").scale(domain=[0, 1]).title("Score"),
        color=gs.Color("impact:N"),
        tooltip=["id:N", "score:Q", "impact:N"],
    )
    .properties(assembly="hg38", title="Zoomable locus scale")
)
# interaction-zoom-end


# interaction-binding-start
bound_chart = (
    gs.Chart(VARIANTS)
    .transform_filter(gs.datum.score >= MIN_SCORE)
    .mark_point(
        filled=True,
        color="#4c78a8",
        size=gs.expr("pointSize"),
    )
    .encode(
        x=gs.X("id:N").scale(domain=VARIANT_DOMAIN).title("Variant"),
        y=gs.Y("score:Q").scale(domain=[0, 1]).title("Score"),
    )
    .properties(
        title="Filter with a bound parameter",
        params=[
            gs.param(
                "minScore",
                value=0.4,
                bind={
                    "input": "range",
                    "min": 0,
                    "max": 1,
                    "step": 0.05,
                    "name": "Minimum score: ",
                },
            ),
            gs.param("pointSize", expr="60 + minScore * 100"),
        ],
    )
)
# interaction-binding-end


# interaction-selection-start
selection_chart = (
    gs.Chart(VARIANTS)
    .mark_point(filled=True, size=140, stroke="black")
    .encode(
        x=gs.Locus("chrom", "pos").scale(domain=REGION),
        y=gs.Y("score:Q").scale(domain=[0, 1]),
        color=gs.Color("impact:N"),
        key=gs.Key("id"),
        opacity=gs.Opacity(gs.value(0.25)).condition(
            gs.condition("selectedVariant", 1)
        ),
        strokeWidth=gs.StrokeWidth(gs.value(0)).condition(
            gs.condition("selectedVariant", 2, empty=False)
        ),
        tooltip=["id:N", "impact:N", "score:Q"],
    )
    .properties(
        assembly="hg38",
        title="Click a variant to select it",
        params=[gs.param("selectedVariant", select="point")],
    )
)
# interaction-selection-end


# interaction-brush-start
chromosome_rects = (
    gs.Chart()
    .mark_rect(tooltip=None)
    .encode(
        fill=gs.Fill("odd:N")
        .scale(domain=[True, False], range=["#e8e8e8", "white"])
        .legend(None)
    )
)

chromosome_labels = (
    gs.Chart()
    .mark_text(paddingX=3, paddingY=5, tooltip=None)
    .encode(text=gs.Text("name:N"))
)

overview_track = (
    gs.layer(chromosome_rects, chromosome_labels)
    .encode(
        x=gs.X("continuousStart:L").scale(zoom=False).axis(None),
        x2=gs.X2("continuousEnd"),
    )
    .properties(
        data=gs.Data(lazy=AxisGenomeData(type="axisGenome", channel="x")),
        height=26,
        params=[
            gs.param(
                "brush",
                select=IntervalSelectionConfig(
                    type="interval",
                    encodings=["x"],
                    mark=BrushConfig(
                        clip=False,
                        fill="#4c78a8",
                        fillOpacity=0.18,
                        stroke="#4c78a8",
                        measure="outside",
                        zindex=11,
                    ),
                ),
                push="outer",
                persist=False,
            )
        ],
    )
)

# The overview needs its own x scale while the detail tracks share another.
overview = gs.vconcat(overview_track).resolve_scale(x="excluded")

brush_score_track = (
    gs.Chart()
    .mark_point(filled=True, size=100, color="#4c78a8")
    .encode(
        x=gs.Locus("chrom", "pos"),
        y=gs.Y("score:Q").scale(domain=[0, 1]).title(None),
        tooltip=["id:N", "score:Q"],
    )
    .properties(height=80, title=gs.title("Score", orient="left"))
)

brush_depth_track = (
    gs.Chart()
    .mark_point(filled=True, size=100, color="#f58518", shape="square")
    .encode(
        x=gs.Locus("chrom", "pos"),
        y=gs.Y("depth:Q").scale(domain=[0, 80]).title(None),
        tooltip=["id:N", "depth:Q"],
    )
    .properties(height=80, title=gs.title("Depth", orient="left"))
)

brush_details = (
    gs.vconcat(brush_score_track, brush_depth_track)
    .properties(
        scales=gs.scales(
            x=gs.Scale(domain=SelectionDomainRef(param="brush", initial=DETAIL_REGION))
        ),
        axes=gs.axes(x=gs.GenomeAxis(title="Genomic position")),
        spacing=8,
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
)

brush_chart = gs.vconcat(overview, brush_details).properties(
    data=BRUSH_VARIANTS,
    assembly="hg38",
    padding=gs.Paddings(top=20),
    params=[gs.param("brush")],
    spacing=8,
)
# interaction-brush-end


# interaction-ruler-start
score_track = (
    gs.Chart()
    .mark_point(filled=True, size=90, color="#4c78a8")
    .encode(y=gs.Y("score:Q").scale(domain=[0, 1]).title("Score"))
    .properties(height=90, title=gs.title("Score", orient="left"))
)

depth_track = (
    gs.Chart()
    .mark_point(filled=True, size=90, color="#f58518")
    .encode(y=gs.Y("depth:Q").scale(domain=[0, 80]).title("Depth"))
    .properties(height=90, title=gs.title("Read depth", orient="left"))
)

ruler_chart = (
    (score_track & depth_track)
    .properties(
        data=VARIANTS,
        assembly="hg38",
        scales=gs.scales(x=gs.Scale(domain=REGION)),
        axes=gs.axes(x=gs.GenomeAxis(title="Genomic position")),
        params=[
            gs.param(
                "cursor",
                persist=False,
                ruler={
                    "encodings": ["x"],
                    "extent": "container",
                    "display": "line",
                    "mark": {"stroke": "#d62728", "strokeWidth": 1},
                },
            )
        ],
        spacing=8,
    )
    .encode(x=gs.Locus("chrom", "pos"))
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
)
# interaction-ruler-end


CHARTS = {
    "zoom_chart": zoom_chart,
    "bound_chart": bound_chart,
    "selection_chart": selection_chart,
    "brush_chart": brush_chart,
    "ruler_chart": ruler_chart,
}
