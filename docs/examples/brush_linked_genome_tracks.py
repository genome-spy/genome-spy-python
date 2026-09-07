"""Brush-linked genome tracks.

A whole-genome overview brush controls three synchronized association tracks.
The overview keeps its own scale while the detail views share a selection-driven
locus domain.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._hapmap import hapmap_manhattan_data
from genome_spy.schema import BrushConfig, SelectionDomainRef

META = {
    "category": "Association plots",
    "order": 12,
    "height": 500,
    "max_width": 980,
}

INITIAL_REGION = [
    {"chrom": "chr5", "pos": 0},
    {"chrom": "chr5", "pos": 180_857_866},
]

# Load association results and the axis limits for the example.
data, _, domains = hapmap_manhattan_data()
# Store the selected range so all three detail tracks can use it.
brush = gs.param("brush")
# Let the reader drag a rectangle across the overview to choose that range.
brush_update = gs.selection_interval(
    "brush",
    encodings=["x"],
    mark=BrushConfig(
        clip=False,
        fill="#4c78a8",
        fillOpacity=0.2,
        stroke="#315f8c",
        strokeWidth=1.2,
        measure="outside",
    ),
    push="outer",
    persist=False,
)


# Keep the whole genome visible above the zoomed-in tracks.
overview_track = (
    gs.Chart()
    .mark_point(filled=True, size=13, opacity=0.68, color="#7f8c8d")
    .encode(
        x=gs.Locus("chrom", "BP")
        .scale(assembly="hg18", zoom=False)
        .axis(title=None, chromTicks=True, chromLabels=True),
        y=gs.Y("neglog:Q")
        .scale(domain=domains["y_domain"])
        .axis(title="Overview", grid=False, labels=False, ticks=False),
        tooltip=["SNP:N", "chrom:N", "BP:Q", "P:Q"],
    )
    .properties(height=105)
    .add_params(brush_update)
)
# Leave room above the overview for the selected range's length label.
overview = (
    gs.vconcat(overview_track)
    .properties(padding=gs.Paddings(top=24))
    .resolve_scale(x="excluded")
)


# Show association strength within the selected range, starting on chromosome 5.
association_track = (
    gs.Chart()
    .mark_point(filled=True, size=24, opacity=0.78, color="#4c78a8")
    .encode(
        x=gs.Locus("chrom", "BP")
        .scale(domain=SelectionDomainRef(param=brush.name, initial=INITIAL_REGION))
        .axis(None),
        y=gs.Y("neglog:Q").scale(domain=domains["y_domain"]).title("−log10 p"),
        tooltip=["SNP:N", "GENE:N", "P:Q"],
    )
    .properties(
        name="association-strength",
        height=95,
    )
)

# Show effect sizes for the same range.
effect_track = (
    gs.Chart()
    .mark_point(filled=True, size=24, opacity=0.78, color="#f58518")
    .encode(
        x=gs.Locus("chrom", "BP")
        .scale(domain=SelectionDomainRef(param=brush.name, initial=INITIAL_REGION))
        .axis(None),
        y=gs.Y("EFFECTSIZE:Q").scale(domain=[-3, 3]).title("Effect size"),
        tooltip=["SNP:N", "GENE:N", "EFFECTSIZE:Q"],
    )
    .properties(
        name="effect-size",
        height=95,
    )
)

# Add Z-scores as the third view of the selected range.
zscore_track = (
    gs.Chart()
    .mark_point(filled=True, size=24, opacity=0.78, color="#54a24b")
    .encode(
        x=gs.Locus("chrom", "BP").scale(
            domain=SelectionDomainRef(param=brush.name, initial=INITIAL_REGION)
        ),
        y=gs.Y("ZSCORE:Q").scale(domain=[0, 7]).title("Z-score"),
        tooltip=["SNP:N", "GENE:N", "ZSCORE:Q"],
    )
    .properties(
        name="z-score",
        height=95,
    )
)


# Stack the overview and detail tracks, and give them the same selection.
chart = (
    gs.vconcat(overview, association_track, effect_track, zscore_track)
    .properties(
        data=data,
        assembly="hg18",
        title="Brush-linked HapMap association tracks",
        description=(
            "A whole-genome interval selection controls three synchronized "
            "association detail tracks."
        ),
        spacing=8,
    )
    .add_params(brush)
    .resolve_scale(x="independent", y="independent")
    .resolve_axis(x="independent", y="independent")
)
