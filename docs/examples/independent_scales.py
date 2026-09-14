"""Layered charts with independent scales.

Overlay probe measurements and segment means with separate vertical axes.
"""

import genome_spy as gs

META = {"category": "Basics", "order": 28, "height": 360}

# Keep the upstream tables remote, rather than embedding them in the spec.
probes = gs.Data(url="https://genomespy.app/docs/data/cnv_chr19_raw.tsv")
segments = gs.Data(url="https://genomespy.app/docs/data/cnv_chr19_segs.tsv")
zoom = gs.Expression("zoomLevel")

points = (
    gs.Chart(probes)
    .mark_point(size=gs.expr(gs.expr.min(2 * gs.expr.pow(zoom, 1.5), 200)))
    .encode(x=gs.X("Position:I"), y=gs.Y("logR:Q"), opacity=gs.value(0.15))
)
means = (
    gs.Chart(segments)
    .mark_rule(size=3, minLength=3, color="black")
    .encode(x=gs.X("startpos:I"), x2=gs.X2("endpos"), y=gs.Y("segMean:Q"))
)

# Align positions horizontally, but give each measurement its own y scale.
chart = (points + means).resolve_scale(y="independent").resolve_axis(y="independent")
