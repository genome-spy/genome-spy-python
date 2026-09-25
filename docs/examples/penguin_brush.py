"""Brush-linked penguin summaries.

Select penguins in a scatter plot and count the selection by species and sex.
"""

import genome_spy as gs

META = {"category": "Interaction and exploration", "order": 33, "height": 460}

data = gs.Data(
    url="https://cdn.jsdelivr.net/npm/vega-datasets@2.9.0/data/penguins.json"
)
species = ["Chinstrap", "Adelie", "Gentoo"]
colors = gs.Scale(domain=species, range=["#BF5CCA", "#FF6C02", "#0F7574"])

# Store the selection on the parent so both views can use it.
brush = gs.param("brush")
brush_update = gs.selection_interval("brush", encodings=["x", "y"], push="outer")

points = (
    gs.Chart()
    .mark_point(filled=False, size=40, opacity=0.7)
    .encode(
        x=gs.X("Beak Length (mm):Q").scale(zero=False, padding=0.1),
        y=gs.Y("Beak Depth (mm):Q").scale(zero=False, padding=0.1),
        color=gs.when(brush_update)
        .then(gs.Color("Species:N").scale(colors).legend(orient="top-right", offset=0))
        .otherwise(gs.value("lightgrey")),
    )
    .add_params(brush_update)
    .properties(title=gs.Title(text="Palmer Penguins", style="overlay-title"))
)

# Keep every category on the axis even when its selected count is zero.
by_species = (
    gs.Chart()
    .transform_aggregate(groupby=["Species"])
    .mark_rect()
    .encode(
        x=gs.X("Species:N").scale(domain=species, padding=0.3).axis(labelAngle=0),
        color=gs.Color("Species:N").legend(None),
    )
)
by_sex = (
    gs.Chart()
    .transform_filter((gs.datum.Sex == "MALE") | (gs.datum.Sex == "FEMALE"))
    .transform_aggregate(groupby=["Sex"])
    .mark_rect()
    .encode(
        x=gs.X("Sex:N")
        .scale(domain=["MALE", "FEMALE"], padding=0.3)
        .axis(labelAngle=0),
        color=gs.value("gray"),
    )
)
summaries = (
    (by_species & by_sex)
    # Match the brush coordinates to the columns used by the scatter plot.
    .transform_filter(
        brush_update, fields={"x": "Beak Length (mm)", "y": "Beak Depth (mm)"}
    )
    .encode(y=gs.Y("count:Q"))
    .resolve_scale(x="independent", color="shared")
)
chart = (
    (points | summaries)
    .properties(data=data, padding=10, spacing=30)
    .transform_collect()
    .add_params(brush)
    .resolve_scale(color="shared", y="independent")
    .resolve_legend(color="independent")
)
