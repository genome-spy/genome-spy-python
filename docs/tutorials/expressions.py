"""Single-source chart objects used by the Expressions guide."""

# expressions-calculate-start
import genome_spy as gs

measurements = [
    {"sample": "A", "score": 2},
    {"sample": "B", "score": 5},
    {"sample": "C", "score": 8},
]

chart = (
    gs.Chart(measurements)
    .transform_calculate(doubled=gs.datum.score * 2)
    .mark_point(filled=True, size=100)
    .encode(x="sample:N", y="doubled:Q")
)
# expressions-calculate-end


# expressions-choice-start
labeled_chart = chart.transform_calculate(
    label=gs.expr.if_(gs.datum.score >= 5, "high", "low"),
)
# expressions-choice-end


# expressions-property-start
point_size = gs.param("pointSize", value=50)
resized_chart = chart.mark_point(
    filled=True,
    size=gs.expr(point_size * 2),
).add_params(point_size)
# expressions-property-end


CHARTS = {
    "chart": chart,
    "labeled_chart": labeled_chart,
    "resized_chart": resized_chart,
}
