"""Native GenomeSpy chart construction from prepared observation snapshots."""

from __future__ import annotations

from typing import Literal

import genome_spy as gs
from matplotlib import colors
from matplotlib.ticker import MaxNLocator

from genome_spy.scanpy._prepare import PreparedUMAP, coordinate_domain


def build_umap(
    prepared: PreparedUMAP,
    *,
    hover: bool,
    zoom: bool,
    selection: gs.Parameter | None = None,
) -> gs.TopLevelSpec:
    style = prepared.style
    table = prepared.table
    if selection is not None:
        if len({panel.dimensions for panel in prepared.panels}) != 1:
            raise NotImplementedError(
                "gsc.pl.umap: linked brushing requires the same dimensions in all panels."
            )
        if any(
            table[f"_opacity_{i}"].nunique() != 1 for i in range(len(prepared.panels))
        ):
            raise NotImplementedError(
                "gsc.pl.umap: brushing with per-entry transparency is not supported; "
                "set scalar alpha explicitly."
            )
    charts = []
    for i, panel in enumerate(prepared.panels):
        x_field, y_field = [f"_coord_{d}" for d in panel.dimensions]
        x_domain = coordinate_domain(table[x_field].to_numpy(), style["xmargin"])
        y_domain = coordinate_domain(table[y_field].to_numpy(), style["ymargin"])
        axis = dict(
            ticks=False,
            labels=False,
            domain=False,
            titleFontSize=style["axis_fontsize"],
            titleFont=style["font"],
        )
        x = gs.X(f"{x_field}:Q").scale(
            domain=list(x_domain), zero=False, nice=False, zoom=zoom
        )
        y = gs.Y(f"{y_field}:Q").scale(
            domain=list(y_domain), zero=False, nice=False, zoom=zoom
        )
        if zoom:
            x = x.scale(name=f"umap-x-{panel.dimensions[0]}")
            y = y.scale(name=f"umap-y-{panel.dimensions[1]}")
        x = (
            x.axis(title=f"UMAP{panel.dimensions[0] + 1}", **axis)
            if style["frameon"]
            else x.axis(None)
        )
        y = (
            y.axis(title=f"UMAP{panel.dimensions[1] + 1}", **axis)
            if style["frameon"]
            else y.axis(None)
        )
        legend = None
        if (
            panel.categorical
            and panel.key is not None
            and style["legend_loc"] == "right margin"
        ):
            legend = gs.Legend(
                title=None,
                orient="right",
                values=list(panel.legend_values),
                columns=1
                if len(panel.legend_values) <= 14
                else 2
                if len(panel.legend_values) <= 30
                else 3,
                symbolSize=36 * (style["dpi"] / 72) ** 2,
                symbolOpacity=style["alpha"],
                labelLimit=1000,
            )
        if not panel.categorical and style["colorbar_loc"] is not None:
            # Public locator arithmetic, with the same vertical tick-space
            # budget as Matplotlib; no figure/axis is constructed.
            bins = max(1, min(9, int(panel.height / (2 * style["tick_fontsize"]))))
            ticks = MaxNLocator(nbins=bins, steps=[1, 2, 2.5, 5, 10]).tick_values(
                *panel.domain
            )
            legend = gs.Legend(
                title=None,
                orient="right",
                gradientLength=panel.height,
                gradientThickness=panel.height / 30,
                gradientOpacity=style["alpha"],
                gradientStrokeColor=style["frame_color"],
                gradientStrokeWidth=style["frame_width"],
                values=[
                    float(tick)
                    for tick in ticks
                    if panel.domain[0] <= tick <= panel.domain[1]
                ],
            )
        color = (
            gs.Color(f"_color_{i}:N" if panel.categorical else f"_color_{i}:Q")
            .scale(
                type="ordinal" if panel.categorical else "quantize",
                domain=list(panel.domain),
                range=[colors.to_hex(paint) for paint in panel.palette],
                nice=False,
            )
            .legend(legend)
        )
        # Explicit fills preserve Matplotlib's LUT arithmetic (including float32
        # bin boundaries). The numeric color channel supplies its native guide.
        paints = list(dict.fromkeys(table[f"_paint_{i}"].tolist()))
        maximum_size = max(1.0, float(table[f"_size_{i}"].max()))
        chart = (
            gs.Chart(table)
            .transform_collect(sort={"field": f"_order_{i}", "order": "ascending"})
            .mark_point(
                filled=True,
                opacity=style["alpha"],
                fillOpacity=1,
                stroke=style["stroke"],
                strokeOpacity=style["stroke_opacity"],
                strokeWidth=style["stroke_width"],
                inwardStroke=False,
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                x=x,
                y=y,
                key=gs.Key("_obs_id"),
                fill=gs.Fill(f"_paint_{i}:N")
                .scale(
                    type="ordinal",
                    domain=paints,
                    range=[colors.to_hex(paint) for paint in paints],
                )
                .legend(None),
                fillOpacity=gs.FillOpacity(f"_opacity_{i}:Q")
                .scale(domain=[0, 1], range=[0, 1], nice=False)
                .legend(None),
                size=gs.Size(f"_size_{i}:Q")
                .scale(
                    domain=[0, maximum_size],
                    range=[0, maximum_size],
                    nice=False,
                    zero=True,
                )
                .legend(None),
            )
            .properties(width=panel.width, height=panel.height)
        )
        if hover:
            chart = chart.encode(
                tooltip=[
                    gs.Tooltip("_obs_id:N", title="Observation ID"),
                    gs.Tooltip("_obs_label:N", title="Observation"),
                    gs.Tooltip(
                        f"_value_{i}:N" if panel.categorical else f"_value_{i}:Q",
                        title=f"{panel.key or 'Color'} ({panel.source})",
                    ),
                    gs.Tooltip(f"{x_field}:Q", title=f"UMAP{panel.dimensions[0] + 1}"),
                    gs.Tooltip(f"{y_field}:Q", title=f"UMAP{panel.dimensions[1] + 1}"),
                ]
            )
        if selection is not None:
            opacity = float(table[f"_opacity_{i}"].iloc[0])
            chart = chart.encode(
                fillOpacity=gs.when(selection)
                .then(gs.value(opacity))
                .otherwise(gs.value(opacity * 0.2)),
                strokeOpacity=gs.when(selection)
                .then(gs.value(style["stroke_opacity"]))
                .otherwise(gs.value(style["stroke_opacity"] * 0.2)),
            )
        layers: list[gs.TopLevelSpec] = [chart]
        if legend is not None:
            # The point renderer drops an unused color channel when fill is
            # explicit. A zero-size, clipped native mark owns the numeric or
            # categorical guide without changing the plotted lookup-table fill.
            # It shares the observation table; it adds no prepared data/artist.
            guide = (
                gs.Chart(table)
                .transform_filter(f"datum._order_{i} === 0")
                .mark_point(size=0, filled=True, tooltip=None)
                .encode(x=gs.value(-10000), y=gs.value(-10000), color=color)
                .properties(width=panel.width, height=panel.height)
            )
            layers.append(guide)
        if panel.labels:
            labels = (
                gs.Chart(list(panel.labels))
                .mark_text(
                    size=style["legend_fontsize"],
                    font=style["font"],
                    fontWeight=style["legend_fontweight"],
                )
                .encode(x=x.field("x"), y=y.field("y"), text="label:N")
            )
            layers.append(labels)
        result = (gs.layer(*layers) if len(layers) > 1 else chart).properties(
            width=panel.width, height=panel.height
        )
        if selection is not None and i == 0:
            # A single panel owns the native interval controller. Declaring the
            # selection on each nested container makes ownership ambiguous.
            result = result.add_params(
                selection.copy(name=selection.name, push="outer")
            ).properties(name=f"umap-brush-{selection.name}")
        if panel.title:
            result = result.properties(
                title=gs.title(
                    panel.title, fontSize=style["title_fontsize"], font=style["font"]
                )
            )
        result = result.configure_view(
            stroke=style["frame_color"] if style["frameon"] else "transparent",
            strokeWidth=style["frame_width"] if style["frameon"] else 0,
        )
        result = result.configure_legend(
            labelFont=style["font"],
            labelFontSize=style["legend_fontsize"]
            if panel.categorical
            else style["tick_fontsize"],
            rowPadding=style["legend_labelspacing"] * style["legend_fontsize"],
            labelOffset=style["legend_handletextpad"] * style["legend_fontsize"],
            layout={"anchor": "middle", "wrap": False},
        )
        charts.append(result)
    if len(charts) == 1:
        return (
            gs.layer(charts[0]).add_params(gs.param(selection.name, value=None))
            if selection is not None
            else charts[0]
        )
    # Independent guides preserve the initial Scanpy layout. Dataset consolidation
    # shares the table even though each panel has a separate draw permutation.
    position_resolution: Literal["shared", "independent"] = (
        "shared"
        if zoom and len({p.dimensions for p in prepared.panels}) == 1
        else "independent"
    )
    resolutions: dict[str, Literal["shared", "independent"]] = dict(
        x=position_resolution,
        y=position_resolution,
        color="independent",
        fill="independent",
        size="independent",
        fillOpacity="independent",
    )
    rows = [
        gs.hconcat(*charts[start : start + style["ncols"]], spacing=style["wspace"])
        .resolve_scale(**resolutions)
        .resolve_legend(default="independent")
        for start in range(0, len(charts), style["ncols"])
    ]
    combined = (
        gs.vconcat(*rows, spacing=style["hspace"])
        .resolve_scale(**resolutions)
        .resolve_legend(default="independent")
    )
    return (
        combined.add_params(gs.param(selection.name, value=None))
        if selection is not None
        else combined
    )
