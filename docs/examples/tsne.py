"""Zoomable t-SNE scatter plot.

Explore a dense embedding with sample colors and points that grow on zoom.
"""

import genome_spy as gs

META = {"category": "Interaction and exploration", "order": 80, "height": 540}

# Read the upstream Parquet file directly, without copying it into the spec.
data = gs.Data(
    url="https://genomespy.app/examples/tSNE/tsne.parquet",
    format=gs.DataFormat(type="parquet"),
)

# These are live GenomeSpy view values, not Python-side measurements.
zoom = gs.Expression("zoomLevel")
width = gs.Expression("width")
height = gs.Expression("height")

points = (
    gs.Chart()
    .mark_point(
        size=gs.expr(
            gs.expr.min(0.1 * zoom * gs.expr.sqrt(zoom), 200)
            * (width * height / (500 * 500))
        )
    )
    .encode(color=gs.Color("sample:N"), opacity=gs.value(0.7))
)

# Keep the original example's playful notes at their plotted positions.
notes = (
    gs.Chart(
        gs.Data(
            values=[
                {"x": -1.565, "y": 7.41, "text": "Ouch, that's sharp!"},
                {"x": 5.6, "y": -3.7, "text": "What's this pink mass?"},
                {"x": -4.8, "y": -7.1, "text": "An artistic appendage."},
            ]
        )
    )
    .mark_text(dy=12, align="center", size=17, font="Indie Flower", angle=5)
    .encode(text=gs.Text("text:N"))
)

# Both layers use the same zoomable coordinates.
chart = (
    (points + notes)
    # Let the plot fit the gallery container, including its axes and legend.
    .properties(data=data, title="Zoomable t-SNE scatter plot")
    .encode(
        x=gs.X("x:Q").scale(domain=[-10, 10], zoom=True),
        y=gs.Y("y:Q").scale(domain=[-10, 10], zoom=True),
    )
)
