"""Single-source chart objects used by the Getting Started tutorial."""

import genome_spy as gs


# getting-started-data-start
measurements = [
    {"day": 1, "value": 4.2, "group": "A"},
    {"day": 1, "value": 3.4, "group": "B"},
    {"day": 2, "value": 5.1, "group": "A"},
    {"day": 2, "value": 4.6, "group": "B"},
    {"day": 3, "value": 5.8, "group": "A"},
    {"day": 3, "value": 5.2, "group": "B"},
]
# getting-started-data-end


# getting-started-mark-start
points = gs.Chart(measurements).mark_point(size=100)
# getting-started-mark-end


# getting-started-x-start
positioned_points = points.encode(x=gs.X("day:O"))
# getting-started-x-end


# getting-started-encodings-start
encoded_points = positioned_points.encode(
    y=gs.Y("value:Q"),
    color=gs.Color("group:N"),
)
# getting-started-encodings-end


# getting-started-guides-start
measurement_chart = encoded_points.encode(
    x=gs.X("day:O").title("Day"),
    y=gs.Y("value:Q").scale(zero=False).title("Measured value"),
    color=gs.Color("group:N").legend(title="Group"),
)
# getting-started-guides-end


# getting-started-genomic-data-start
features = [
    {"chrom": "chr17", "start": 43_044_000, "end": 43_050_000, "kind": "A"},
    {"chrom": "chr17", "start": 43_057_000, "end": 43_061_000, "kind": "B"},
    {"chrom": "chr17", "start": 43_068_000, "end": 43_075_000, "kind": "A"},
]
# getting-started-genomic-data-end


# getting-started-genomic-chart-start
genomic_track = (
    gs.Chart(features)
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start").scale(zoom=True),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("kind:N").title("Feature kind"),
        color=gs.Color("kind:N").legend(None),
    )
    .properties(assembly="hg38", height=120)
)
# getting-started-genomic-chart-end


CHARTS = {
    "points": points,
    "positioned_points": positioned_points,
    "encoded_points": encoded_points,
    "measurement_chart": measurement_chart,
    "genomic_track": genomic_track,
}
