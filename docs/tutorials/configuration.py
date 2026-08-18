"""Single-source chart objects used by the Configuration guide."""

# configuration-data-start
import genome_spy as gs


measurements = [
    {"sample": "A", "time": 1, "value": 2.1},
    {"sample": "A", "time": 2, "value": 2.8},
    {"sample": "A", "time": 3, "value": 3.2},
    {"sample": "B", "time": 1, "value": 2.4},
    {"sample": "B", "time": 2, "value": 3.5},
    {"sample": "B", "time": 3, "value": 4.3},
]
# configuration-data-end


# configuration-levels-start
configured_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, stroke="white", strokeWidth=1)
    .encode(
        x=gs.X("time:Q").title("Time"),
        y=gs.Y("value:Q").scale(zero=False).title("Response"),
        color=gs.Color("sample:N").legend(title="Sample"),
    )
    .properties(
        width=360,
        height=210,
        padding=gs.Paddings(top=8, right=12, bottom=4, left=12),
        title=gs.title(
            "Configured measurements",
            subtitle="Explicit properties override configured defaults",
        ),
    )
    .with_view(fill="#fafafa", stroke="#d3d3d3", strokeWidth=1)
    .configure_point(size=110, opacity=0.85)
    .configure_axis(grid=True, gridColor="#e5e5e5")
    .configure_title(anchor="start", fontSize=16, subtitleFontSize=11)
)
# configuration-levels-end


# configuration-step-start
categories = [
    {"category": "A", "value": 3},
    {"category": "B", "value": 5},
    {"category": "C", "value": 2},
    {"category": "D", "value": 4},
]

step_chart = (
    gs.Chart(categories)
    .mark_rect(color="#4c78a8")
    .encode(
        x=gs.X("category:N").title("Category"),
        y=gs.Y("value:Q").title("Value"),
    )
    .properties(width=gs.step(48), height=150, title="48 pixels per category")
)
# configuration-step-end


# configuration-flex-start
fixed_panel = (
    gs.Chart([{}])
    .mark_text(size=13)
    .encode(x=gs.value(0.5), y=gs.value(0.5), text=gs.value("Fixed: 120 px"))
    .properties(width=120, height=80)
    .with_view(fill="#eef3f8", stroke="#9eb4c8")
)
growing_panel = (
    gs.Chart([{}])
    .mark_text(size=13)
    .encode(x=gs.value(0.5), y=gs.value(0.5), text=gs.value("Flexible: grow=1"))
    .properties(width=gs.SizeDef(grow=1, minPx=180), height=80)
    .with_view(fill="#f8f1ea", stroke="#cfaa83")
)

flex_chart = (fixed_panel | growing_panel).properties(
    width="container", spacing=8, title="Fixed and flexible child widths"
)
# configuration-flex-end


# configuration-theme-start
themed_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, size=100)
    .encode(x="time:Q", y="value:Q", color="sample:N")
    .properties(height=190, title="The Quartz built-in theme", theme="quartz")
)
# configuration-theme-end


CHARTS = {
    "configured_chart": configured_chart,
    "step_chart": step_chart,
    "flex_chart": flex_chart,
    "themed_chart": themed_chart,
}
