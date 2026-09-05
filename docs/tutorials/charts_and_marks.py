"""Single-source chart objects used by the Charts and Marks guide."""

# charts-marks-point-start
import genome_spy as gs

observations = [
    {"sample": "A", "time": 1, "value": 2.2, "amount": 18},
    {"sample": "A", "time": 2, "value": 3.1, "amount": 32},
    {"sample": "A", "time": 3, "value": 3.8, "amount": 24},
    {"sample": "B", "time": 1, "value": 1.7, "amount": 22},
    {"sample": "B", "time": 2, "value": 2.5, "amount": 15},
    {"sample": "B", "time": 3, "value": 3.3, "amount": 36},
]

point_chart = (
    gs.Chart(observations)
    .mark_point(filled=True, stroke="white", strokeWidth=1)
    .encode(
        x=gs.X("time:O").title("Time"),
        y=gs.Y("value:Q").scale(zero=False).title("Value"),
        color=gs.Color("sample:N").legend(title="Sample"),
        size=gs.Size("amount:Q").legend(title="Amount"),
    )
    .properties(
        title="Measurements by sample",
        description="Six measurements grouped by sample.",
    )
)
# charts-marks-point-end


# charts-marks-ranges-start
intervals = [
    {"feature": "A", "start": 1, "end": 4, "group": "first"},
    {"feature": "B", "start": 3, "end": 8, "group": "second"},
    {"feature": "C", "start": 7, "end": 11, "group": "first"},
]

interval_chart = (
    gs.Chart(intervals)
    .mark_rule(size=8, strokeCap="round")
    .encode(
        x=gs.X("start:Q").scale(domain=[0, 12]).title("Position"),
        x2=gs.X2("end"),
        y=gs.Y("feature:N").title("Feature"),
        color=gs.Color("group:N").legend(title="Group"),
    )
    .properties(title="Intervals have two endpoints")
)
# charts-marks-ranges-end


# charts-marks-text-start
text_chart = (
    gs.Chart(observations)
    .mark_text(size=13)
    .encode(
        x=gs.X("time:O").title("Time"),
        y=gs.Y("value:Q").scale(zero=False).title("Value"),
        text="sample:N",
        color="sample:N",
    )
    .properties(title="Text can represent a field")
)
# charts-marks-text-end


# charts-marks-relations-start
relations = [
    {"x": 1, "y": 1, "x2": 4, "y2": 3, "kind": "observed"},
    {"x": 2, "y": 4, "x2": 6, "y2": 2, "kind": "predicted"},
    {"x": 5, "y": 1, "x2": 8, "y2": 4, "kind": "observed"},
]

relation_base = gs.Chart(relations).encode(
    x=gs.X("x:Q").scale(domain=[0, 9]).title("Source x"),
    x2=gs.X2("x2"),
    y=gs.Y("y:Q").scale(domain=[0, 5]).title("Source y"),
    y2=gs.Y2("y2"),
    color=gs.Color("kind:N").legend(title="Relation"),
)

link_chart = relation_base.mark_link(linkShape="diagonal", size=2).properties(
    title="Links connect two positions"
)

arrow_chart = relation_base.mark_arrow(size=5, headWidth=3).properties(
    title="Arrows add direction"
)
# charts-marks-relations-end


CHARTS = {
    "point_chart": point_chart,
    "interval_chart": interval_chart,
    "text_chart": text_chart,
    "link_chart": link_chart,
    "arrow_chart": arrow_chart,
}
