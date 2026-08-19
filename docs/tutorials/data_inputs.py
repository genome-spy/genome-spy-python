"""Single-source chart objects used by the Data user-guide page."""

# data-inputs-records-start
import genome_spy as gs

measurements = [
    {"sample": "A", "time": 0, "value": 2.1},
    {"sample": "A", "time": 1, "value": 3.4},
    {"sample": "A", "time": 2, "value": 4.0},
    {"sample": "B", "time": 0, "value": 1.8},
    {"sample": "B", "time": 1, "value": 2.7},
    {"sample": "B", "time": 2, "value": 3.6},
]
# data-inputs-records-end


# data-inputs-inline-chart-start
inline_chart = (
    gs.Chart(measurements)
    .mark_point(size=90)
    .encode(
        x=gs.X("time:O").title("Time"),
        y=gs.Y("value:Q").scale(zero=False).title("Value"),
        color=gs.Color("sample:N").legend(title="Sample"),
    )
)
# data-inputs-inline-chart-end


# data-inputs-url-start
url_chart = (
    gs.Chart(
        gs.Data(
            url="https://example.org/measurements.csv",
            format=gs.data_format(type="csv"),
        )
    )
    .mark_point()
    .encode(x="time:O", y="value:Q", color="sample:N")
)
# data-inputs-url-end


# data-inputs-inheritance-start
points = (
    gs.Chart()
    .mark_point(size=90)
    .encode(
        x="time:O",
        y=gs.Y("value:Q").scale(zero=False),
        color="sample:N",
    )
)
labels = (
    gs.Chart()
    .mark_text(dy=-12)
    .encode(
        x="time:O",
        y="value:Q",
        text="value",
        color="sample:N",
    )
)

inherited_chart = (points + labels).properties(
    data=measurements,
    title="Measurements over time",
)
# data-inputs-inheritance-end


CHARTS = {
    "inline_chart": inline_chart,
    "url_chart": url_chart,
    "inherited_chart": inherited_chart,
}
