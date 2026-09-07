"""P53 sequence comparison with an overview brush.

Explore the p53 FASTA used by Dash Bio, with residue tiles, a consensus row,
column identity, and sequence coverage. The source is ungapped, not an MSA.
"""

import genome_spy as gs
from genome_spy.datasets import load_dataset

META = {
    "category": "Reference annotation tracks",
    "order": 29,
    "height": 980,
    "max_width": 1000,
}

# Load prepared sequence rows and per-position summaries.
data = load_dataset("p53_sequence_comparison")
# Use consistent amino-acid colors; grey fills the ends of shorter sequences.
residue_colors = gs.Scale(
    domain=list("ACDEFGHIKLMNPQRSTVWY-"),
    range=[
        "#80a0f0",
        "#f08080",
        "#c048c0",
        "#c048c0",
        "#80a0f0",
        "#f09048",
        "#15a4a4",
        "#80a0f0",
        "#f01505",
        "#80a0f0",
        "#80a0f0",
        "#00c000",
        "#ffff00",
        "#00c000",
        "#f01505",
        "#00c000",
        "#00c000",
        "#80a0f0",
        "#80a0f0",
        "#15a4a4",
        "#eeeeee",
    ],
)
color = gs.Color("residue:N").scale(residue_colors).legend(None)
# Share the range chosen by dragging across the overview.
brush = gs.param("p53Window")
selection = gs.selection_interval(
    "p53Window", encodings=["x"], push="outer", mark=gs.BrushConfig(fillOpacity=0.12)
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
    )
    .properties(height=100)
    .add_params(selection)
)
# Leave room above the overview for the selected range's label.
overview_group = (
    gs.vconcat(overview)
    .resolve_scale(x="excluded")
    .properties(padding=gs.Paddings(top=24))
)

# Show the fraction of all 34 sequences matching the most common amino acid.
identity = (
    gs.Chart(data["columns"])
    .mark_rect(color="#4c78a8")
    .encode(
        x=gs.X("position:I").axis(None),
        y=gs.Y("identity:Q").scale(domain=[0, 1]).axis(tickCount=3).title("Identity"),
        tooltip=["position:Q", "identity:Q", "residue:N"],
    )
    .properties(height=55)
)
# Show the fraction of sequences that reach each position.
coverage = (
    identity.mark_rect(color="#929ca5")
    .encode(
        y=gs.Y("coverage:Q").scale(domain=[0, 1]).axis(tickCount=3).title("Coverage"),
        tooltip=["position:Q", "coverage:Q"],
    )
    .properties(height=35)
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
        color=color,
        tooltip=["identifier:N", "accession:N", "position:Q", "residue:N"],
    )
)
# Add letters when there is enough room to read them.
letters = tiles.mark_text(size=11, fitToBand=True, tooltip=None).encode(
    text="residue:N", color=gs.value("#202020")
)
sequences = (tiles + letters).properties(height=gs.step(17))

# Add a summary row showing the most common amino acid at each position.
consensus_tiles = (
    gs.Chart(data["columns"])
    .mark_rect()
    .encode(
        x=gs.X("position:I")
        .axis(tickMinStep=1)
        .title("Sequence position (not aligned)"),
        y=gs.Y("identifier:N").title(None),
        color=color,
        tooltip=["position:Q", "residue:N", "identity:Q"],
    )
)
consensus_letters = consensus_tiles.mark_text(
    size=11, fitToBand=True, tooltip=None
).encode(text="residue:N", color=gs.value("#202020"))
consensus = (consensus_tiles + consensus_letters).properties(height=20)

# Make all detail tracks follow the selected range, starting at the first 50 positions.
details = (
    gs.vconcat(identity, coverage, sequences, consensus, spacing=6)
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
)
# Place the full overview above the linked detail tracks.
chart = (
    (overview_group & details)
    .add_params(brush)
    .properties(
        width=780,
        spacing=18,
        title="P53 sequences: overview and residue detail",
        description="34 original, unaligned p53 sequences from the Dash Bio example. Drag the overview or zoom below to compare positions; grey cells pad shorter sequences.",
    )
    .resolve_scale(x="independent", y="independent")
)
