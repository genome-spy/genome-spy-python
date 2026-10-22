"""Native navigation and value labels for the expression grids."""

from collections.abc import Collection
from typing import Any, Literal

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS as PT


def vertical_highlights(
    positions: Collection[float], low: float, high: float
) -> gs.Chart:
    """Return clipped native dashed rules over the supplied vertical data range."""
    return (
        gs.Chart([{"position": value} for value in positions])
        .mark_rule(
            color="black",
            size=1.5 * PT,
            # Native dash lengths use whole pixels.
            strokeDash=[round(value * 1.5 * PT) for value in (3.7, 1.6)],
            clip=True,
            tooltip=None,
        )
        .encode(
            x="position:Q", y=gs.Y(datum=low, type="quantitative"), y2=gs.Y2(datum=high)
        )
    )


def zoom_axes(
    x: Any, y: Any, *, enabled: bool | Literal["xy"], name: str | None
) -> tuple[Any, Any]:
    """Enable y navigation or both axes, naming scales only when requested."""
    if not enabled:
        return x, y
    return x.scale(
        zoom=enabled == "xy", name=f"{name}-x" if name is not None else Undefined
    ), y.scale(zoom=True, name=f"{name}-y" if name is not None else Undefined)


def index_offset(axis: str, field: str) -> Any:
    """Turn a fractional slot field into a live within-band pixel offset.

    Keep integer anchors on the index scale so grouping gaps remain aligned.
    """
    extent = "width" if axis == "x" else "height"
    sign = "" if axis == "x" else "-"
    return (gs.XOffset if axis == "x" else gs.YOffset)(f"{field}:Q").scale(
        domain=[0, 1],
        range=[0, gs.expr(f"{sign}{extent} * bandstep('{axis}', {extent})")],
    )


def with_values(tiles: gs.Chart, field: str, *, alpha: float = 1) -> gs.LayerChart:
    """Reuse tile records and positions for values that fit inside visible cells.

    Choose text contrast from GenomeSpy's rendered RGB colors over white.
    """
    # Both marks inherit one source and filter; color lookup runs at the tile scale's owner.
    data, transforms = tiles._kwds["data"], tiles._kwds["transform"]
    tiles = tiles._copy(deep=False, data=Undefined, transform=Undefined)
    low, high = tiles._kwds["encoding"]["color"]["scale"]["domain"]
    # shortcut: sample the native palette in 256 bins, until Core exposes color contrast.
    palette = (
        "["
        + ",".join(
            f"scale('color', {low + (high - low) * i / 255})" for i in range(256)
        )
        + "]"
    )
    fraction = f"(datum.{field} - {low}) / {high - low}"
    index = f"clamp(round({fraction} * 255), 0, 255)"
    labels = tiles.transform_calculate(
        _rgb=rf"split(replace(grid_palette[{index}], /rgb\(|\)/g, ''), ',')"
    )
    # Composite the tile opacity before measuring its relative luminance.
    labels = labels.transform_calculate(
        **{
            f"_{channel}": f"parseFloat(datum._rgb[{i}]) / 255 * {alpha} + {1 - alpha}"
            for i, channel in enumerate("rgb")
        }
    )
    luminance = " + ".join(
        f"{weight} * (datum._{channel} <= 0.04045 ? datum._{channel} / 12.92 : "
        f"pow((datum._{channel} + 0.055) / 1.055, 2.4))"
        for channel, weight in zip("rgb", (0.2126, 0.7152, 0.0722), strict=True)
    )
    labels = (
        labels.transform_calculate(_luminance=luminance)
        .mark_text(
            font=FONT,
            size=12,
            align="center",
            baseline="middle",
            fitToBand=True,
            paddingX=4,
            paddingY=3,
            tooltip=None,
        )
        .encode(
            text=gs.Text(f"{field}:Q", format=".2f"),
            tooltip=None,
            color=gs.Color(
                gs.expr("datum._luminance > 0.179 ? 'black' : 'white'"), type="nominal"
            )
            .scale(type="ordinal", domain=["white", "black"], range=["white", "black"])
            .legend(None),
        )
    )

    return (
        gs.layer(tiles, gs.layer(labels).resolve_scale(color="excluded"))
        .properties(data=data, transform=transforms)
        .add_params(gs.param("grid_palette", expr=palette))
    )
