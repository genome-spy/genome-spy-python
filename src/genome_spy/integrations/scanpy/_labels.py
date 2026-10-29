"""Shared native label placement for embeddings and group graphs."""

from typing import Literal

import genome_spy as gs

from genome_spy.integrations.scanpy._style import FONT


def displaced_labels(
    source: gs.Chart,
    *,
    key: str,
    text: str,
    x: str,
    y: str,
    size: float,
    font: str = FONT,
    fontweight: Literal["normal", "bold"] = "normal",
    anchor_size: float | str = 6,
) -> gs.Chart:
    """Return centered labels from source fields, avoiding labels and anchor boxes.

    Native text measurement and offsets keep placement aligned while zooming.
    """
    return (
        source.transform_measure_text(
            field=text,
            fontSize=size,
            font=font,
            fontWeight=fontweight,
            as_="_label_width",
        )
        .transform_collect()
        .transform_filter(
            gs.expr.inrange(gs.datum[x], gs.expr.domain("x"))
            & gs.expr.inrange(gs.datum[y], gs.expr.domain("y"))
        )
        .transform_displace2d(
            key=key,
            x=x,
            y=y,
            width="_label_width",
            height=size * 1.2,
            anchorWidth=anchor_size,
            anchorHeight=anchor_size,
            as_=["_label_dx", "_label_dy"],
        )
        .mark_text(
            size=size,
            font=font,
            fontWeight=fontweight,
            align="center",
            baseline="middle",
            clip=True,
            tooltip=None,
        )
        .encode(
            text=gs.Text(field=text, type="nominal"),
            xOffset=gs.XOffset("_label_dx:Q").scale(None),
            yOffset=gs.YOffset("_label_dy:Q").scale(None),
        )
    )
