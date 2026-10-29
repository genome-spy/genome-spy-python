"""Native navigation, named ticks and fitted values for expression plots."""

from collections.abc import Collection, Mapping
from math import ceil
from typing import Any, Literal

import genome_spy as gs
from genome_spy.schema import OrderCondition
from genome_spy.schemapi import Undefined
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS as PT


def grid_interactions(
    marks: gs.Chart,
    highlight: bool | Literal["outline"],
    *,
    values: str | None = None,
    alpha: float = 1,
) -> gs.LayerChart:
    """Add optional native pointer feedback, owned by the grid rather than its labels."""
    if highlight == "outline":
        hovered = gs.selection_point(
            "grid_hover",
            on="mousemove",
            clear="mouseleave",
            toggle=False,
            persist=False,
            empty=False,
        )
        mark = marks._kwds["mark"]
        style = mark if isinstance(mark, dict) else {}
        marks = marks.add_params(hovered).encode(
            stroke=gs.Stroke(gs.value(style.get("stroke", "#0f172a"))).condition(
                gs.condition(hovered, "#0f172a")
            ),
            strokeWidth=gs.StrokeWidth(gs.value(style.get("strokeWidth", 0))).condition(
                gs.condition(hovered, 1.5)
            ),
            strokeOpacity=gs.StrokeOpacity(
                gs.value(
                    1
                    if style.get("strokeOpacity", Undefined) is Undefined
                    else style["strokeOpacity"]
                )
            ).condition(gs.condition(hovered, 1)),
            # Centered strokes must be drawn after adjacent tile fills.
            order=gs.Order(0).condition(
                OrderCondition(param=hovered.name, empty=False, value=1)
            ),
        )
    center = (
        with_values(marks, values, alpha=alpha)
        if values is not None
        else gs.layer(marks)
    )
    if highlight is True:
        # Container ownership keeps the ruler active between marks and in group gaps.
        return center.add_params(
            gs.ruler(
                "grid_cursor",
                encodings=["x", "y"],
                display="center",
                extent="view",
                persist=False,
                mark=gs.RulerMarkConfig(stroke="#4682b4", opacity=0.9, strokeWidth=1.5),
            )
        )
    return center


def series_focus(
    labels: Collection[str],
    field: str,
    *,
    name: str = "profile_focus",
    title: str = "Focus: ",
) -> tuple[gs.Parameter, gs.Expression]:
    """Return a native dropdown and opacity expression that emphasize one series."""
    all_series = ""
    while all_series in labels:
        all_series += "_"
    focus = gs.param(
        name,
        value=all_series,
        bind=gs.binding_select(
            options=[all_series, *labels], labels=["All", *labels], name=title
        ),
    )
    opacity = gs.expr.if_(
        (focus == all_series) | (focus == gs.datum[field]), 0.85, 0.12
    )
    return focus, opacity


def simulation_runs(
    chart: gs.Chart,
    field: str,
    length: float,
    *,
    samples: int,
    select: bool,
) -> tuple[gs.Chart, gs.Parameter | None, gs.Expression]:
    """Add run labels from sample positions and return an optional focus control.

    Points and heatmaps use the same one-based run labels and opacity rules.
    """
    position = getattr(gs.datum, field)
    chart = chart.transform_calculate(
        _run=gs.expr.format(gs.expr.floor(position / length) + 1, "d")
    )
    if not select:
        return chart, None, gs.Expression("1")

    labels = [str(i + 1) for i in range(ceil(samples / length))]
    control, opacity = series_focus(
        labels, "_run", name="simulation_run", title="Run: "
    )
    return chart, control, opacity


def profile_segments(chart: gs.Chart, groups: list[str], x: str, y: str) -> gs.Chart:
    """Pair neighboring profile values within each group, retaining missing-value gaps."""
    return chart.transform_window(
        ops=["lead", "lead"],
        fields=[x, y],
        as_=[f"_next{x}", f"_next{y}"],
        groupby=groups,
        sort={"field": x},
    ).transform_filter(
        f"isValid(datum.{y}) && isValid(datum._next{y}) && isValid(datum._next{x})"
    )


def profile_ruler() -> gs.Parameter:
    """Return a native x ruler for reading aligned profile panels."""
    return gs.ruler(
        "profile_cursor",
        encodings=["x"],
        display="line",
        extent="view",
        persist=False,
        mark=gs.RulerMarkConfig(stroke="#64748b", opacity=0.5, strokeWidth=1),
    )


def horizontal_tick_labels(ticks: Mapping[float, str], title: str | None) -> gs.Chart:
    """Return a native side track for named numeric ticks, following the shared x scale."""
    chart = (
        gs.Chart(
            [{"position": value, "label": label} for value, label in ticks.items()]
        )
        .mark_text(
            font=FONT,
            size=10 * PT,
            align="center",
            baseline="top",
            yOffset=8,
            clip="y",
            cullByVisibleRange="x",
            tooltip=None,
        )
        .encode(x=gs.X("position:Q").axis(None), y=gs.value(1), text="label:N")
        .properties(height=24)
    )
    if title:
        chart = chart.properties(
            title=gs.Title(
                text=title,
                orient="bottom",
                offset=4,
                font=FONT,
                fontSize=10 * PT,
                fontWeight="normal",
            )
        )
    return chart


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
    domain = tiles._kwds["encoding"]["color"]["scale"]["domain"]
    low, high = domain[0], domain[-1]

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

    # Value labels do not own hover state or inherit tile outlines.
    labels = tiles._copy(
        deep=False, name=Undefined, params=Undefined
    ).transform_calculate(
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
            stroke=gs.value("black"),
            strokeWidth=gs.value(0),
            strokeOpacity=gs.value(1),
            order=gs.value(0),
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
