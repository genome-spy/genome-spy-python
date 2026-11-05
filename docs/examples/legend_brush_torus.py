"""Brush a million-point torus.

Move the colorbar brush to highlight different bands around a doughnut-shaped surface.
"""

import genome_spy as gs

META = {"category": "Interaction and exploration", "order": 34, "height": 560}

background = "#101622"
band = gs.selection_interval(
    "wave_band",
    encodings=["color"],
    bind="legend",
    value={"color": [0.4625, 0.5375]},
)
selected = gs.when(gs.NamedSelectionPredicateRef(ref="selected"))

chart = (
    # Generate the points in GenomeSpy rather than sending a million Python rows.
    gs.Chart(gs.Data(sequence=gs.SequenceParams(start=0, stop=1_000_000, as_="i")))
    .transform_calculate(
        u=2 * gs.expr.PI * ((gs.datum.i * 0.6180339887498949) % 1),
        v=2 * gs.expr.PI * ((gs.datum.i * 0.7548776662466927) % 1),
    )
    .transform_calculate(
        x=(2 + 0.7 * gs.expr.cos(gs.datum.v))
        * (0.94 * gs.expr.cos(gs.datum.u) + 0.34 * gs.expr.sin(gs.datum.u)),
        y=(2 + 0.7 * gs.expr.cos(gs.datum.v))
        * (-0.2 * gs.expr.cos(gs.datum.u) + 0.55 * gs.expr.sin(gs.datum.u))
        + 0.574 * gs.expr.sin(gs.datum.v),
        wave=0.5 + 0.5 * gs.expr.sin(3 * gs.datum.u + 2 * gs.datum.v),
    )
    .add_params(band)
    .mark_point(
        filled=True,
        size=gs.expr(gs.expr.min(gs.expr.zoomLevel() ** 2, 200)),
        strokeWidth=0,
        tooltip=None,
    )
    .encode(
        x=gs.X("x:Q").scale(domain=[-3, 3], zoom=True).axis(None),
        y=gs.Y("y:Q").scale(domain=[-2.1, 2.1], zoom=True).axis(None),
        color=gs.Color("wave:Q", title="Wave value", format=".2f").scale(
            domain=[0, 0.5, 1], range=["#5ba7ff", "#67e7bf", "#fad668"]
        ),
        opacity=selected.then(gs.value(0.4)).otherwise(gs.value(0.01)),
        # Paint the highlighted bands last so faint points cannot cover them.
        order=selected.then(gs.value(1)).otherwise(gs.value(0)),
    )
    .properties(
        width="container",
        height="container",
        theme="dark",
        background=background,
        predicates={"selected": gs.SelectionPredicateOperand(param=band.name)},
        title=gs.Title(
            text="Braided torus",
            subtitle="1,000,000 points. Drag the colorbar brush.",
            anchor="start",
            fontSize=24,
            subtitleFontSize=13,
        ),
    )
    .configure_view(fill=background, strokeOpacity=0)
    .configure_legend(orient="right")
    .configure_style(
        {"gradient-selection-brush": gs.StyleConfig(shadowColor=background)}
    )
)
