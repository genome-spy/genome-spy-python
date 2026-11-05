"""Native legend selections shared by plot families."""

from typing import Literal

import genome_spy as gs


def legend_focus(
    name: str,
    field: str,
    *,
    channel: Literal["color", "fill", "stroke", "shape"] = "color",
    categorical: bool = True,
) -> tuple[gs.Parameter, gs.Expression]:
    """Return a legend selection and a native predicate; an empty selection keeps all rows."""
    if categorical:
        selection = gs.selection_point(name, encodings=[channel], bind="legend")
    else:
        if channel == "shape":
            raise ValueError("A numeric legend requires a color channel.")
        selection = gs.selection_interval(name, encodings=[channel], bind="legend")
    reference = gs.Expression(name)
    if categorical:
        member = gs.expr.selectionContains(reference, channel, gs.datum[field])
    else:
        bounds = gs.expr.selectionBounds(reference, channel)
        member = (gs.datum[field] >= bounds[0]) & (gs.datum[field] < bounds[1])
    match = ~gs.expr.selectionActive(reference) | member
    return selection, match
