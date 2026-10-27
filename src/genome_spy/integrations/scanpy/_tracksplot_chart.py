"""Native per-cell expression tracks with shared cell positions and side guides."""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.integrations.scanpy._data import coordinate_domain, number
from genome_spy.integrations.scanpy._dendrogram_chart import tree_track
from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
from genome_spy.integrations.scanpy._grouped_data import FeatureGroup, HeatmapData
from genome_spy.integrations.scanpy._grouped_chart import _category_strip
from genome_spy.integrations.scanpy._style import FONT


def build_tracksplot(
    prepared: HeatmapData,
    feature_groups: tuple[FeatureGroup, ...],
    observation_names: np.ndarray,
    observation_ids: np.ndarray,
    *,
    groupby: str,
    categories: list[str],
    palette: tuple[str, ...],
    tree: DendrogramData | None,
    log: bool,
    hover: bool,
    zoom: bool,
    width: float | None,
    height: float | None,
    figsize: tuple[float, float] | None,
) -> gs.TopLevelSpec:
    """Return one rect per cell and gene, with independent expression scales.

    Share cell slots across tracks, the category strip and optional group tree.
    """
    context = "gsc.pl.tracksplot"
    values = prepared.values
    cells, genes = values.shape
    if figsize is not None:
        if width is not None or height is not None:
            raise TypeError(
                f"{context}: figsize cannot be combined with width or height."
            )
        if len(figsize) != 2:
            raise ValueError(f"{context}: figsize needs width and height in inches.")
        width = number(figsize[0], "figsize width", context=context) * 100
        height = number(figsize[1], "figsize height", context=context) * 100 - (
            (100 if tree else 0) + 24
        )
    width = number(1200 if width is None else width, "width", context=context)
    height = number(genes * 25 if height is None else height, "height", context=context)
    if not width or not height:
        raise ValueError(f"{context}: width and height must be positive.")
    if feature_groups and [
        slot for group in feature_groups for slot in range(group.start, group.end + 1)
    ] != list(range(genes)):
        raise NotImplementedError(
            f"{context}: marker spans must cover every gene once, in order."
        )

    # Send cell metadata once; each track reads one selected expression column.
    numeric = values.to_numpy(dtype=float, na_value=np.nan)
    table = pd.DataFrame(numeric, columns=[f"_value_{i}" for i in range(genes)]).assign(
        _cell=np.arange(cells),
        _group=np.asarray(values.index.astype(str)),
        _obs_id=observation_ids,
        _obs_label=observation_names,
    )
    color = (
        gs.Color("_group:N").scale(domain=categories, range=list(palette)).legend(None)
    )
    group_colors = dict(zip(categories, palette, strict=True))
    boundaries = (
        gs.Chart(
            [{"_boundary": int(stop)} for stop in prepared.intervals["stop"].iloc[:-1]]
        )
        .mark_rule(
            color="#777777", size=0.5, strokeDash=[3, 3], clip=True, tooltip=None
        )
        .encode(
            x=gs.X("_boundary:I", band=0).axis(None),
            y=gs.value(0),
            y2=gs.value(1),
        )
    )
    tracks: list[gs.TopLevelSpec] = []
    for slot, name in enumerate(values.columns):
        field = f"_value_{slot}"
        finite = numeric[:, slot][np.isfinite(numeric[:, slot])]
        if log:
            positive = finite[finite > 0]
            domain = coordinate_domain(
                positive if positive.size else np.array([1.0, 10.0]), 0.05, log=True
            )
        else:
            domain = coordinate_domain(np.append(finite, 0), 0.05)
        # Scanpy masks nonpositive log values; their baseline is the viewport bottom.
        bars = (
            gs.Chart()
            .transform_filter(
                f"isValid(datum.{field})" + (f" && datum.{field} > 0" if log else "")
            )
            .mark_rect(
                minWidth=0,
                minHeight=0,
                minOpacity=1,
                clip=True,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                x=gs.X("_cell:I").axis(None),
                y=gs.Y(f"{field}:Q")
                .scale(
                    type="log" if log else "linear",
                    domain=list(domain),
                    nice=False,
                    zero=False,
                    zoom=False,
                )
                .axis(
                    title=None,
                    orient="right",
                    values=[int(domain[1]) if not log or domain[1] >= 1 else domain[1]],
                    labelBaseline="top",
                    grid=False,
                    domain=False,
                    labelFontSize=10,
                ),
                y2=gs.value(0) if log else gs.Y2(datum=0),
                color=color,
            )
        )
        if hover:
            bars = bars.encode(
                tooltip=[
                    gs.Tooltip("_obs_id:N", title="Cell ID"),
                    gs.Tooltip("_obs_label:N", title="Cell"),
                    gs.Tooltip("_group:N", title="Group"),
                    gs.Tooltip(
                        f"{field}:Q",
                        title=f"{name} expression" + (" (log1p)" if log else ""),
                        format=".4g",
                    ),
                ]
            )
        baseline = (
            gs.Chart([{}])
            .mark_rule(color="#999999", size=0.5, tooltip=None)
            .encode(y=gs.value(0) if log else gs.Y(datum=0, type="quantitative"))
        )
        track: gs.LayerChart | gs.SurroundChart = gs.layer(
            bars, baseline, boundaries
        ).properties(width=width, height=height / genes)
        if feature_groups:
            block = next(
                i
                for i, group in enumerate(feature_groups)
                if group.start <= slot <= group.end
            )
            marker = (
                gs.Chart([{}])
                .mark_rect(
                    color=group_colors[
                        prepared.intervals["label"].iloc[min(block, len(palette) - 1)]
                    ],
                    tooltip=None,
                )
                .properties(width=10)
            )
            track = gs.surround(
                track, surround=gs.SurroundSides(right=[marker]), spacing=4
            )
        tracks.append(
            track.properties(
                title=gs.Title(
                    text=str(name),
                    orient="left",
                    angle=0,
                    align="right",
                    font=FONT,
                    fontSize=11,
                    fontWeight="normal",
                    offset=8,
                )
            )
        )

    strip_color = (
        gs.Color("label:N")
        .scale(domain=categories, range=list(palette))
        .legend(title=groupby, orient="bottom", columns=2)
    )
    strip = _category_strip(
        list(values.index.astype(str)),
        gs.X("slot:I").axis(None),
        strip_color,
        horizontal=True,
        title=groupby,
        hover=hover,
    )
    if tree is not None:
        tracks.insert(
            0,
            tree_track(
                tree, prepared.intervals["center"].tolist(), horizontal=True, size=100
            ).properties(width=width),
        )
    return (
        gs.vconcat(*tracks, strip, spacing=0)
        .properties(
            data=table,
            width=width,
            scales=gs.scales(
                x=gs.Scale(
                    type="index",
                    domain=[0, cells - 1],
                    paddingOuter=0,
                    zoom=zoom,
                )
            ),
        )
        .resolve_scale(x="shared", y="independent", color="shared")
        .resolve_axis(x="independent", y="independent")
        .resolve_legend(default="collected")
        .configure_view(stroke="transparent", strokeWidth=0)
        .configure_axis(labelFont=FONT)
        .configure_legend(labelFont=FONT, layout={"anchor": "middle"})
    )
