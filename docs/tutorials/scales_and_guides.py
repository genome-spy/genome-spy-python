"""Single-source chart objects used by the Scales and Guides guide."""

# scales-guides-automatic-start
import genome_spy as gs

measurements = [
    {"sample": "control", "time": 1, "value": 2.1},
    {"sample": "control", "time": 2, "value": 2.8},
    {"sample": "control", "time": 3, "value": 3.2},
    {"sample": "treated", "time": 1, "value": 2.4},
    {"sample": "treated", "time": 2, "value": 3.5},
    {"sample": "treated", "time": 3, "value": 4.3},
]

automatic_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, size=90)
    .encode(
        x="time:Q",
        y="value:Q",
        color="sample:N",
    )
    .properties(title="Automatic scales and guides")
)
# scales-guides-automatic-end


# scales-guides-custom-start
customized_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, size=90)
    .encode(
        x=gs.X("time:Q")
        .scale(domain=[0.5, 3.5], zoom=True)
        .axis(tickMinStep=1, grid=False)
        .title("Time point"),
        y=gs.Y("value:Q")
        .scale(domain=[1.5, 4.5], zero=False)
        .axis(grid=True, tickCount=4)
        .title("Response"),
        color=gs.Color("sample:N")
        .scale(
            domain=["control", "treated"],
            range=["#4c78a8", "#e45756"],
        )
        .legend(title="Sample group", orient="top", direction="horizontal"),
    )
    .properties(title="Selected scale and guide options")
)
# scales-guides-custom-end


# scales-guides-hidden-start
minimal_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, size=90)
    .encode(
        x=gs.X("time:Q").axis(None),
        y=gs.Y("value:Q").scale(zero=False).title("Response"),
        color=gs.Color("sample:N").legend(None),
    )
    .properties(title="Guides can be removed independently")
)
# scales-guides-hidden-end


CHARTS = {
    "automatic_chart": automatic_chart,
    "customized_chart": customized_chart,
    "minimal_chart": minimal_chart,
}
