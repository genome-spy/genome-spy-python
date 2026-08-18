"""Single-source chart objects used by the Transforms guide."""

# transforms-data-start
import genome_spy as gs


measurements = [
    {"sample": "C1", "group": "control", "response": 0.42, "quality": 0.92},
    {"sample": "C2", "group": "control", "response": 0.55, "quality": 0.64},
    {"sample": "C3", "group": "control", "response": 0.61, "quality": 0.81},
    {"sample": "T1", "group": "treated", "response": 0.48, "quality": 0.58},
    {"sample": "T2", "group": "treated", "response": 0.72, "quality": 0.88},
    {"sample": "T3", "group": "treated", "response": 0.84, "quality": 0.95},
]
# transforms-data-end


# transforms-filter-start
filtered_chart = (
    gs.Chart(measurements)
    .transform_filter("datum.quality >= 0.7")
    .mark_point(filled=True, size=100)
    .encode(
        x=gs.X("response:Q").scale(domain=[0, 1]).title("Response"),
        y=gs.Y("sample:N").title("Passing sample"),
        color=gs.Color("group:N").legend(title="Group"),
        tooltip=["sample:N", "quality:Q"],
    )
    .properties(title="Keep rows with sufficient quality")
)
# transforms-filter-end


# transforms-formula-start
formula_chart = (
    gs.Chart(measurements)
    .transform_formula(
        expr="datum.response * 100",
        as_="responsePercent",
    )
    .mark_point(filled=True, size=100)
    .encode(
        x=gs.X("sample:N").title("Sample"),
        y=gs.Y("responsePercent:Q").scale(domain=[0, 100]).title("Response (%)"),
        color=gs.Color("group:N").legend(title="Group"),
    )
    .properties(title="Derive a percentage field")
)
# transforms-formula-end


# transforms-aggregate-start
aggregate_chart = (
    gs.Chart(measurements)
    .transform_formula(
        expr="datum.response * 100",
        as_="responsePercent",
    )
    .transform_aggregate(
        groupby=["group"],
        fields=["responsePercent"],
        ops=["mean"],
        as_=["meanResponse"],
    )
    .mark_point(filled=True, size=140)
    .encode(
        x=gs.X("group:N").title("Group"),
        y=gs.Y("meanResponse:Q").scale(domain=[0, 100]).title("Mean response (%)"),
        color=gs.Color("group:N").legend(None),
        tooltip=[gs.Tooltip("group:N"), gs.Tooltip("meanResponse:Q").format(".1f")],
    )
    .properties(title="One summarized row per group")
)
# transforms-aggregate-end


CHARTS = {
    "filtered_chart": filtered_chart,
    "formula_chart": formula_chart,
    "aggregate_chart": aggregate_chart,
}
