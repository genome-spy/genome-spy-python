"""Native text panels for supplied scores and stored gene rankings."""

import genome_spy as gs
from genome_spy.integrations.scanpy._data import number
from genome_spy.integrations.scanpy._ranking.data import RankPanel
from genome_spy.integrations.scanpy._style import FONT, POINTS_TO_PIXELS, native_color


def build_ranking(
    panels: list[RankPanel],
    *,
    ncols: int | None = None,
    sharey: bool,
    fontsize: float,
    color: str,
    hover: bool,
    width: float | None,
    height: float | None,
    context: str,
    headroom: float = 0,
    ylabel: str | None = None,
    bottom_labels: bool = False,
) -> gs.TopLevelSpec:
    """Return rank-label charts with supplied bounds, optional shared scores and hover."""
    width = number(300 if width is None else width, "width", context=context)
    height = number(300 if height is None else height, "height", context=context)
    fontsize = number(fontsize, "fontsize", context=context)
    if not width or not height or not fontsize:
        raise ValueError(f"{context}: width, height and fontsize must be positive.")
    color = native_color(color, "color", context=context)
    if ncols is None:
        ncols = len(panels) if len(panels) <= 5 else (len(panels) + 1) // 2
    bounds = [min(p.y_domain[0] for p in panels), max(p.y_domain[1] for p in panels)]
    charts = []
    last_row = ((len(panels) - 1) // ncols) * ncols
    for index, panel in enumerate(panels):
        domain = bounds if sharey else list(panel.y_domain)
        domain = [domain[0], domain[1] + headroom * (domain[1] - domain[0])]
        if domain[0] == domain[1]:
            delta = abs(domain[0]) * 0.05 or 0.05
            domain = [domain[0] - delta, domain[1] + delta]
        chart = (
            gs.Chart(panel.values)
            .mark_text(
                font=FONT,
                size=fontsize * POINTS_TO_PIXELS,
                color=color,
                angle=-90,
                align="left",
                baseline="middle",
                clip="never",
                tooltip={"handler": "default"} if hover else None,
            )
            .encode(
                x=gs.X("_rank:Q")
                .scale(domain=list(panel.x_domain), zero=False, nice=False)
                .axis(
                    title="ranking" if not bottom_labels or index >= last_row else None,
                    labels=not panel.hide_ticks,
                    ticks=not panel.hide_ticks,
                ),
                y=gs.Y("_score:Q")
                .scale(domain=domain, zero=False, nice=False)
                .axis(title=ylabel if index % ncols == 0 else None),
                # Rotate ASCII dots because the native atlas lacks vertical ellipsis.
                text=gs.Text(
                    {
                        "expr": "datum._label === '⋮' ? '...' : datum._label",
                        "type": "nominal",
                    }
                ),
            )
        )
        if hover:
            chart = chart.encode(
                tooltip=[
                    gs.Tooltip("_label:N", title="Label"),
                    gs.Tooltip("_score:Q", title="Score", format=".4g"),
                    gs.Tooltip("_rank:Q", title="Rank", format="d"),
                ]
            )

        # Reserve only the part of a rotated label that can extend above the plot.
        top_space = 0
        for label, score in panel.values[["_label", "_score"]].itertuples(
            index=False, name=None
        ):
            label_height = len(label) * fontsize * POINTS_TO_PIXELS
            space_above_score = (domain[1] - score) / (domain[1] - domain[0]) * height
            top_space = max(top_space, label_height - space_above_score)
        charts.append(
            chart.properties(
                width=width,
                height=height,
                title=panel.title,
                padding={"top": top_space},
            )
        )
    if len(charts) == 1:
        return charts[0]
    return gs.concat(*charts, columns=min(ncols, len(charts))).resolve_scale(
        x="independent", y="independent"
    )
