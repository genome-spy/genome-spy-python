"""P53 sequence comparison with an overview brush.

Explore the p53 FASTA used by Dash Bio, with residue tiles, a consensus logo,
position agreement, sequence coverage, and a linked overview.
"""

import genome_spy as gs
from genome_spy.datasets import load_dataset

META = {
    "category": "Reference annotation tracks",
    "order": 29,
    "height": 870,
    "max_width": 1000,
}

# Load prepared sequence rows and per-position summaries.
data = load_dataset("p53_sequence_comparison")
# Use soft amino-acid colors; grey fills the ends of shorter sequences.
residue_colors = gs.Scale(
    domain=list("ACDEFGHIKLMNPQRSTVWY-"),
    range=[
        "#b8c9e6",
        "#f3aaaa",
        "#d7a5d7",
        "#d7a5d7",
        "#b8c9e6",
        "#f2bf86",
        "#8fcfcf",
        "#b8c9e6",
        "#f39b91",
        "#b8c9e6",
        "#b8c9e6",
        "#9bdc91",
        "#f4e88a",
        "#9bdc91",
        "#f39b91",
        "#9bdc91",
        "#9bdc91",
        "#b8c9e6",
        "#b8c9e6",
        "#8fcfcf",
        "#f1f1f1",
    ],
)
color = gs.Color("residue:N").scale(residue_colors).legend(None)
legend_color = (
    gs.Color("residue:N").scale(residue_colors).legend(title="Amino acid", columns=11)
)
# Share the range chosen by dragging across the overview.
brush = gs.param("p53Window")
selection = gs.selection_interval(
    "p53Window",
    encodings=["x"],
    push="outer",
    mark=gs.BrushConfig(
        clip=False,
        fill="#4c78a8",
        fillOpacity=0.28,
        stroke="#244f78",
        strokeOpacity=0.9,
        strokeWidth=1.5,
        shadowBlur=3,
        shadowColor="#244f78",
        shadowOpacity=0.35,
        zindex=11,
    ),
)
# Follow one sequence position through all detail tracks.
detail_ruler = gs.ruler(
    "positionRuler",
    persist=False,
    encodings=["x"],
    extent="container",
    snap=False,
    mark=gs.RulerMarkConfig(stroke="#30343b", strokeWidth=1, opacity=0.4),
)

# Keep all positions visible here; drag to choose the range shown below.
overview = (
    gs.Chart(data["cells"])
    .mark_rect()
    .encode(
        x=gs.X("position:I")
        .scale(domain=[1, data["length"] + 1], zoom=False)
        .title("Sequence position"),
        y=gs.Y("identifier:N")
        .scale(domain=data["sequence_order"], reverse=True)
        .axis(None),
        color=color,
        tooltip=["identifier:N", "accession:N", "position:Q", "residue:N"],
    )
    .properties(height=100)
    .add_params(selection)
)
# Leave room above the overview for the selected range's label.
overview_group = (
    gs.vconcat(overview)
    .resolve_scale(x="excluded")
    .properties(padding=gs.Paddings(top=6))
)

# Show the fraction matching the most common amino acid at each position.
conservation = (
    gs.Chart(data["columns"])
    .mark_rect()
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("identity:Q").scale(domain=[0, 1]).axis(tickCount=3, title=None),
        color=gs.Color("identity:Q")
        .scale(domain=[0, 1], scheme="viridis")
        .legend(title="Conservation", gradientLength=140, tickCount=3),
        tooltip=["position:Q", "identity:Q", "residue:N"],
    )
    .properties(height=60, title=gs.title("Conservation", style="track-title"))
)
# Show the fraction of sequences without a gap at each position.
gap_free = (
    gs.Chart(data["columns"])
    .mark_rect(color="#b4bbc2")
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("coverage:Q").scale(domain=[0, 1]).axis(tickCount=3, title=None),
        tooltip=["position:Q", "coverage:Q"],
    )
    .properties(
        height=30,
        padding=gs.Paddings(bottom=8),
        title=gs.title("Gap-free", style="track-title"),
    )
)

# Show the most common amino acid as a compact consensus row.
consensus_tiles = (
    gs.Chart(data["columns"])
    .mark_rect()
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("identifier:N").title(None),
        color=color,
        tooltip=["position:Q", "residue:N", "identity:Q"],
    )
)
consensus_letters = consensus_tiles.mark_text(size=11, fitToBand=True).encode(
    text="residue:N", color=gs.value("#202020")
)
consensus = (consensus_tiles + consensus_letters).properties(height=15)

# Summarize the residue mixture at each position as a sequence logo.
consensus_logo = (
    gs.Chart(data["cells"])
    .transform_filter(gs.datum.residue != "-")
    .transform_aggregate(groupby=["position", "residue"])
    .transform_stack(
        field="count",
        groupby=["position"],
        offset="normalize",
        as_=["_y0", "_y1"],
        sort=gs.compare("count", order="ascending"),
    )
    .mark_text(
        font="Source Sans Pro",
        fontWeight=700,
        size=90,
        squeeze=True,
        fitToBand=True,
        logoLetters=True,
        paddingX=0,
        paddingY=0,
    )
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("_y0:Q").scale(domain=[0, 1]).title("Share"),
        y2=gs.Y2("_y1"),
        text=gs.Text("residue:N"),
        color=color,
        tooltip=["position:Q", "residue:N", "count:Q"],
    )
    .properties(height=70)
)

# Draw one colored tile per amino acid, with sequence details on hover.
tiles = (
    gs.Chart(data["cells"])
    .mark_rect()
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("identifier:N")
        .scale(domain=data["sequence_order"], reverse=True)
        .title(None),
        color=legend_color,
        tooltip=["identifier:N", "accession:N", "position:Q", "residue:N"],
    )
)
# Add letters when there is enough room to read them.
letters = tiles.mark_text(size=11, fitToBand=True).encode(
    text="residue:N", color=gs.value("#202020")
)
sequences = (tiles + letters).properties(height=gs.step(15), viewportHeight=380)

# Make all detail tracks follow the selected range, starting at the first 50 positions.
details = (
    gs.vconcat(
        gap_free,
        conservation,
        consensus,
        consensus_logo,
        sequences,
        spacing=6,
    )
    .properties(
        scales=gs.scales(
            x=gs.Scale(
                domain=gs.SelectionDomainRef(param="p53Window", initial=[1, 51]),
                zoom=True,
                paddingInner=0,
                paddingOuter=0,
            )
        )
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="independent", y="independent")
    .add_params(detail_ruler)
)
# Place the full overview below the linked detail tracks.
chart = (
    gs.vconcat(details, overview_group, spacing=2)
    .add_params(brush)
    .properties(
        width="container",
        title="P53 sequences: overview and residue detail",
        description="34 original, ungapped p53 sequences from the Dash Bio example. Drag the overview or zoom the detail tracks to compare positions; grey cells pad shorter sequences.",
    )
    .resolve_scale(x="independent", y="independent")
    .resolve_legend(color="collected")
    .configure_legend(
        orient="bottom",
        direction="horizontal",
        titleOrient="top",
        labelFontSize=10,
        symbolSize=60,
        spacing=20,
        layout={"anchor": "middle"},
    )
)
