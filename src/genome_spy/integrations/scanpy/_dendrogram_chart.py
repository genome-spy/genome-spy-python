"""Native marks render Python tree geometry; GenomeSpy performs no clustering."""

from typing import Literal

import numpy as np

import genome_spy as gs
from genome_spy.integrations.scanpy._dendrogram_data import TreeData
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._grid_interactions import index_offset
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
)

Orientation = Literal["top", "bottom", "left", "right"]


def tree_records(
    tree: TreeData, leaf_positions: list[float] | None = None
) -> list[dict[str, float]]:
    """Return parent-to-child endpoint rows from stored tree coordinates."""
    # Start at each parent so native elbows retain its stored merge height.
    records = [
        {
            "leaf": float((leaves[1] + leaves[2]) / 20),
            "leaf2": float(leaves[child] / 10),
            "distance": float(distances[1]),
            "distance2": float(distances[child]),
        }
        for leaves, distances in zip(tree.icoord, tree.dcoord, strict=True)
        for child in (0, 3)
    ]
    if leaf_positions is not None:
        if len(leaf_positions) != len(tree.order):
            raise ValueError("Tree leaf positions must match the number of groups.")
        slots = np.arange(len(tree.order)) + 0.5
        positions = np.asarray(leaf_positions)
        for record in records:
            for field in ("leaf", "leaf2"):
                record[field] = float(np.interp(record[field], slots, positions))
    return records


def _tree_links(
    chart: gs.Chart,
    *,
    horizontal: bool,
    linewidth: float = 1.5,
) -> gs.Chart:
    """Apply the shared native tree mark to endpoint rows, keeping hover disabled."""
    return chart.mark_link(
        linkShape="orthogonal",
        orient="vertical" if horizontal else "horizontal",
        color="#555555",
        size=linewidth * _PT,
        clip=True,
        tooltip=None,
    )


def tree_track(
    tree: TreeData,
    leaf_positions: list[float],
    *,
    horizontal: bool,
    size: float,
    reverse: bool = False,
    linewidth: float = 1.5,
) -> gs.Chart:
    """Return an in-bounds side tree using stored branches and final slot centers.

    Integer anchors and fractional offsets share the matrix's gapped index scale.
    Fit visible heights; zero-only trees keep a nonzero range with zero at the edge.
    """
    records = tree_records(tree, leaf_positions)
    for record in records:
        for field in ("leaf", "leaf2"):
            record[f"{field}_offset"] = record[field] % 1
            record[field] = float(np.floor(record[field]))
    axis = "x" if horizontal else "y"
    leaf = (gs.X if horizontal else gs.Y)("leaf:I", band=0.5).axis(None)
    # Fit visible branches, retaining zero at the matrix edge and 5% root headroom.
    distance = (
        (gs.Y if horizontal else gs.X)("distance:Q")
        .scale(
            domain=gs.ViewportDomainRef(source="viewport", mode="contain")
            if tree.dcoord.max()
            else [0, distance_domain(tree)[1]],
            domainMin=0,
            padding=1 / 22,
            nice=False,
            zero=True,
            zoom=False,
            reverse=reverse,
        )
        .axis(None)
    )
    chart = _tree_links(gs.Chart(records), horizontal=horizontal, linewidth=linewidth)
    if horizontal:
        return chart.encode(
            x=leaf,
            x2=gs.X2("leaf2:I", band=0.5),
            y=distance,
            y2="distance2:Q",
            xOffset=index_offset(axis, "leaf_offset"),
            x2Offset=gs.X2Offset(field="leaf2_offset"),
        ).properties(height=size)
    return chart.encode(
        y=leaf,
        y2=gs.Y2("leaf2:I", band=0.5),
        x=distance,
        x2="distance2:Q",
        yOffset=index_offset(axis, "leaf_offset"),
        y2Offset=gs.Y2Offset(field="leaf2_offset"),
    ).properties(width=size)


def distance_domain(tree: TreeData) -> list[float]:
    """Return padded distance limits from tree heights, including a zero-height tree."""
    high = float(tree.dcoord.max())
    return [-0.05 * high, 1.05 * high] if high else [-0.055, 0.055]


def build_dendrogram(
    tree: TreeData,
    *,
    orientation: Orientation,
    remove_labels: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    """Return a standalone chart from prepared tree data, orientation and size.

    Draw stored branches and optional labels without computing linkage.
    """
    context = "gsc.pl.dendrogram"
    width = number(300 if width is None else width, "width", context=context)
    height = number(300 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    n = len(tree.order)
    margin = (n - 1) * 0.05
    domain = [0.5 - margin, n - 0.5 + margin]
    # The orientation decides which axis holds the leaves and which holds distance.
    horizontal = orientation in ("top", "bottom")
    leaf = (
        (gs.X if horizontal else gs.Y)("leaf:Q")
        .scale(domain=domain, nice=False, zero=False, zoom=False)
        .axis(None)
    )
    distance = (
        (gs.Y if horizontal else gs.X)("distance:Q")
        .scale(
            domain=distance_domain(tree),
            reverse=orientation in ("left", "bottom"),
            nice=False,
            zero=False,
            zoom=False,
        )
        .axis(None)
    )
    links = _tree_links(gs.Chart(tree_records(tree)), horizontal=horizontal)
    if horizontal:
        links = links.encode(x=leaf, x2="leaf2:Q", y=distance, y2="distance2:Q")
    else:
        links = links.encode(y=leaf, y2="leaf2:Q", x=distance, x2="distance2:Q")
    layers = [links]
    padding = {"left": 10.0, "right": 10.0, "top": 10.0, "bottom": 10.0}
    # Put labels on the leaf side and reserve room for their full length.
    if not remove_labels:
        labels = gs.Chart(
            [
                {"leaf": i + 0.5, "label": str(label)}
                for i, label in enumerate(tree.order)
            ]
        )
        if horizontal:
            top = orientation == "bottom"
            labels = labels.mark_text(
                font=_FONT,
                size=_TICK,
                angle=-90,
                align="left" if top else "right",
                baseline="middle",
                yOffset=-8 if top else 8,
                clip="never",
                tooltip=None,
            ).encode(x=leaf, y=gs.value(1 if top else 0), text="label:N")
            side = "top" if top else "bottom"
        else:
            right = orientation == "left"
            labels = labels.mark_text(
                font=_FONT,
                size=_TICK,
                align="left" if right else "right",
                baseline="middle",
                xOffset=8 if right else -8,
                clip="never",
                tooltip=None,
            ).encode(y=leaf, x=gs.value(1 if right else 0), text="label:N")
            side = "right" if right else "left"
        padding[side] = max(len(str(label)) for label in tree.order) * _TICK * 0.65 + 12
        layers.append(labels)
    return (
        gs.layer(*layers)
        .properties(width=width, height=height, padding=gs.Paddings(**padding))
        .configure_view(stroke="transparent", strokeWidth=0)
    )
