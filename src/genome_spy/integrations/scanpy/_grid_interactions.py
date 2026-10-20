"""Native navigation and value labels for the expression grids."""

from typing import Any, Literal

import genome_spy as gs
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._style import FONT


def zoom_axes(
    x: Any, y: Any, *, enabled: bool | Literal["xy"], name: str
) -> tuple[Any, Any]:
    """Enable y navigation by default, or both named index axes for 'xy'."""
    if not enabled:
        return x, y
    return x.scale(zoom=enabled == "xy", name=f"{name}-x"), y.scale(
        zoom=True, name=f"{name}-y"
    )


def slot_position(axis: str, value: str) -> str:
    """Project a slot expression from the top or left through the live index scale."""
    return f"grid_{axis}_origin + ({value}) * grid_{axis}_step"


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


def visible_slots(
    chart: gs.Chart, axis: str, start: str, stop: str | None = None
) -> gs.Chart:
    """Hide outside labels or incomplete brackets using their slot expressions."""
    position = slot_position(axis, start)
    predicate = f"inrange({position}, [0, 1])"
    if stop is not None:
        predicate = f"({position}) >= 0 && ({slot_position(axis, stop)}) <= 1"
    return chart.transform_filter(predicate)


def with_navigation(chart: gs.LayerChart, *, enabled: bool) -> gs.LayerChart:
    """Expose live x/y origins and band widths to the grid's outside annotations."""
    if not enabled:
        return chart
    # Read scales at their owner; outside annotations have excluded scales.
    return chart.add_params(
        gs.param("grid_x_origin", expr="scale('x', 0)"),
        gs.param("grid_y_origin", expr="1 - scale('y', 0)"),
        gs.param("grid_x_step", expr="bandwidth('x')"),
        gs.param("grid_y_step", expr="bandwidth('y')"),
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
