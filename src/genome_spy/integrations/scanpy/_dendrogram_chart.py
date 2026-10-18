"""Native rules render Python tree geometry; GenomeSpy performs no clustering."""

from typing import Literal

import genome_spy as gs
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._style import (
    FONT as _FONT,
    POINTS_TO_PIXELS as _PT,
    GROUPED_FONT_SIZE as _TICK,
)

Orientation = Literal["top", "bottom", "left", "right"]


def tree_records(tree: DendrogramData) -> list[dict[str, float]]:
    return [
        {
            "leaf": float(leaves[i] / 10),
            "leaf2": float(leaves[i + 1] / 10),
            "distance": float(distances[i]),
            "distance2": float(distances[i + 1]),
        }
        for leaves, distances in zip(tree.icoord, tree.dcoord, strict=True)
        for i in range(3)
    ]


def distance_domain(tree: DendrogramData) -> list[float]:
    high = float(tree.dcoord.max())
    return [-0.05 * high, 1.05 * high] if high else [-0.055, 0.055]


def tree_overlay(
    tree: DendrogramData,
    *,
    orientation: Orientation,
    padding: float = 0,
    reverse: bool = False,
    size: float = 80,
) -> gs.LayerChart:
    """Place branches beside the same fixed index slots used by summary marks."""
    n = len(tree.order)
    maximum = float(tree.dcoord.max()) or 1
    leaf = f"(datum.leaf + {padding}) / {n + 2 * padding}"
    leaf2 = leaf.replace("datum.leaf", "datum.leaf2")
    distance = f"datum.distance / {maximum} * {size}"
    distance2 = distance.replace("datum.distance", "datum.distance2")
    rules = gs.Chart(tree_records(tree)).mark_rule(
        color="#555555", size=1.5 * _PT, clip="never", tooltip=None
    )
    if orientation in ("right", "left"):
        side = "-" if orientation == "left" else "1 +"
        xpos = f"{side} ({distance}) / width"
        x2pos = f"{side} ({distance2}) / width"
        ypos = f"1 - ({leaf})" if reverse else leaf
        y2pos = f"1 - ({leaf2})" if reverse else leaf2
    else:
        side = "1 +" if orientation == "top" else "-"
        xpos, x2pos = leaf, leaf2
        ypos = f"{side} ({distance}) / height"
        y2pos = f"{side} ({distance2}) / height"
    rules = rules.transform_calculate(
        _tree_x=xpos,
        _tree_x2=x2pos,
        _tree_y=ypos,
        _tree_y2=y2pos,
    ).encode(
        x=gs.X("_tree_x:Q").scale(None).axis(None),
        x2="_tree_x2:Q",
        y=gs.Y("_tree_y:Q").scale(None).axis(None),
        y2="_tree_y2:Q",
    )
    return (
        gs.layer(rules)
        .resolve_scale(x="excluded", y="excluded")
        .resolve_axis(x="excluded", y="excluded")
    )


def build_dendrogram(
    tree: DendrogramData,
    *,
    orientation: Orientation,
    remove_labels: bool,
    width: float | None,
    height: float | None,
) -> gs.TopLevelSpec:
    context = "gsc.pl.dendrogram"
    width = number(300 if width is None else width, "width", context=context)
    height = number(300 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    n = len(tree.order)
    margin = (n - 1) * 0.05
    domain = [0.5 - margin, n - 0.5 + margin]
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
    rules = gs.Chart(tree_records(tree)).mark_rule(
        color="#555555", size=1.5 * _PT, tooltip=None
    )
    if horizontal:
        rules = rules.encode(x=leaf, x2="leaf2:Q", y=distance, y2="distance2:Q")
    else:
        rules = rules.encode(y=leaf, y2="leaf2:Q", x=distance, x2="distance2:Q")
    layers = [rules]
    padding = {"left": 10.0, "right": 10.0, "top": 10.0, "bottom": 10.0}
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
