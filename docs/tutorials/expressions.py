"""Single-source chart objects used by the Expressions guide."""

# expressions-row-start
import genome_spy as gs

double_score = gs.datum.score * 2
# expressions-row-end


# expressions-choice-start
score_label = gs.expr.if_(gs.datum.score >= 5, "high", "low")
# expressions-choice-end


# expressions-transforms-start
measurements = [
    {"sample": "A", "score": 2},
    {"sample": "B", "score": 5},
    {"sample": "C", "score": 8},
]

chart = (
    gs.Chart(measurements)
    .transform_calculate(doubled=double_score, label=score_label)
    .transform_filter(gs.datum.doubled >= 10)
    .mark_point(filled=True, size=100)
    .encode(x="sample:N", y="doubled:Q", tooltip=["score:Q", "label:N"])
)
# expressions-transforms-end


CHARTS = {
    "chart": chart,
}
