"""Set intersections with an UpSet plot.

Aligned bars and a membership matrix show exact mutation intersections among
five genes in the UpSetR glioblastoma cohort, with linked row highlighting.
"""

import genome_spy as gs
from genome_spy.schema import RulerMarkConfig

META = {
    "category": "Set intersections",
    "order": 10,
    "height": 390,
    "max_width": 650,
}
SET_CURSOR = gs.param("setCursor")
SET_CURSOR_UPDATE = gs.ruler(
    "setCursor",
    push="outer",
    persist=False,
    encodings=["y"],
    on="mousemove",
    mark=RulerMarkConfig(
        stroke="#555",
        strokeDash=[3, 3],
        opacity=0.7,
    ),
)
SET_CURSOR_Y = SET_CURSOR.values.y
CURSOR = ~gs.expr.isValid(SET_CURSOR_Y) | (gs.datum.profileContainsHoveredSet == 1)

intersection_bars = (
    gs.Chart()
    .mark_rect(color="#3b3b3b")
    .encode(
        x=gs.X("profileNumber:I").axis(None),
        y=gs.Y("profileSize:Q").axis(title="Intersection Size", grid=True, tickCount=5),
    )
    .properties(name="intersection-bars")
)

intersection_labels = (
    gs.Chart()
    .mark_text(size=11, fontWeight="bold", baseline="bottom", dy=-5)
    .encode(
        x=gs.X("profileNumber:I"),
        y=gs.Y("profileSize:Q"),
        text=gs.Text("profileSize:Q"),
        color=gs.value("#333"),
    )
    .properties(name="intersection-labels")
)

# Set-intersection output repeats each profile once per set. One representative
# row is enough for each intersection bar.
intersection_sizes = (
    gs.layer(intersection_bars, intersection_labels)
    .properties(
        name="intersection-sizes",
        width=gs.step(20),
        height=210,
        scales={
            "y": {
                "zero": True,
                "nice": True,
                "padding": 0.12,
                "domainMin": 0,
            }
        },
    )
    .resolve_scale(y="excluded")
    .encode(
        opacity=gs.Opacity(gs.expr(CURSOR), type="nominal")
        .scale(type="ordinal", domain=[False, True], range=[0.14, 1])
        .legend(None)
    )
    .transform_filter(gs.datum.setIndex == 0)
)

set_bars = (
    gs.Chart()
    .mark_rect(color="#6f6f6f")
    .encode(
        x=gs.X("setSize:Q").axis(title="Set Size", orient="bottom", grid=False),
        y=gs.Y("setIndex:I").axis(None),
    )
    .properties(name="set-bars")
)

set_labels = (
    gs.Chart()
    .mark_text(size=11, fontWeight="bold", align="left", dx=5)
    .encode(
        x=gs.X("setSize:Q"),
        y=gs.Y("setIndex:I"),
        text=gs.Text("setSize:Q"),
        color=gs.value("white"),
    )
    .properties(name="set-labels")
)

# Likewise, one profile column is enough when calculating and drawing set sizes.
set_sizes = (
    gs.layer(set_bars, set_labels)
    .properties(
        name="set-sizes",
        width=150,
        height=gs.step(20),
        scales={
            "x": {
                "zero": True,
                "nice": True,
                "reverse": True,
                "padding": 0.08,
                "domain": [0, 100],
            }
        },
    )
    .add_params(SET_CURSOR_UPDATE)
    .resolve_scale(x="excluded")
    .transform_filter(gs.datum.profileNumber == 1)
)

set_names = (
    gs.Chart()
    .transform_filter(gs.datum.profileNumber == 1)
    .mark_text(align="right", dx=-3, clip="never")
    .encode(
        x=gs.value(0),
        y=gs.Y("setIndex:I"),
        text=gs.Text("set"),
        color=gs.value("#555"),
    )
    .properties(name="set-names")
)

row_backgrounds = (
    gs.Chart()
    .transform_filter((gs.datum.setIndex % 2 == 0) & (gs.datum.profileNumber == 1))
    .mark_rect()
    .encode(x=None, y=gs.Y("setIndex:I"), color=gs.value("#f1f1f1"))
    .properties(name="row-backgrounds")
)

background_points = (
    gs.Chart()
    .mark_point(
        filled=True,
        size=95,
        strokeWidth=0,
        opacity=gs.expr(gs.expr.if_(gs.expr.isValid(SET_CURSOR_Y), 0.2, 1)),
    )
    .encode(
        x=gs.X("profileNumber:I"),
        y=gs.Y("setIndex:I"),
        color=gs.value("#d1d1d1"),
    )
    .properties(name="background-points")
)

connectors = (
    gs.Chart()
    .transform_filter(gs.datum.member)
    .transform_aggregate(
        groupby=["profileNumber", "profileContainsHoveredSet"],
        fields=["setIndex", "setIndex"],
        ops=["min", "max"],
        as_=["firstSetIndex", "lastSetIndex"],
    )
    .mark_rule(size=2.5, strokeCap="round")
    .encode(
        x=gs.X("profileNumber:I"),
        y=gs.Y("firstSetIndex:I"),
        y2=gs.Y2("lastSetIndex"),
    )
    .properties(name="connectors")
)

members = (
    gs.Chart()
    .transform_filter(gs.datum.member)
    .mark_point(filled=True, size=115, strokeWidth=0)
    .encode(
        x=gs.X("profileNumber:I").axis(None),
        y=gs.Y("setIndex:I").axis(None),
        tooltip=[
            gs.Tooltip("profileSize:Q").title("Intersection size"),
            gs.Tooltip("profileDegree").title("Degree"),
            gs.Tooltip("profileKey").title("Profile"),
        ],
    )
    .properties(name="members")
)

# The matrix layers share setCursor so hovering a row fades unrelated profiles
# in both the matrix and the bars above it.
matrix = (
    gs.layer(
        set_names,
        row_backgrounds,
        background_points,
        connectors,
        members,
    )
    .properties(
        name="combination-matrix",
        width=gs.step(20),
        height=gs.step(20),
        padding=gs.Paddings(left=45),
    )
    .add_params(SET_CURSOR_UPDATE)
    .encode(
        color=gs.Color(gs.expr(CURSOR), type="nominal")
        .scale(type="ordinal", domain=[False, True], range=["#ddd", "#3b3b3b"])
        .legend(None)
    )
)

# Fold the five gene columns into rows before calculating exact intersections.
# The remaining transforms derive set sizes, hover membership, and bar order.
chart = (
    gs.concat(
        gs.Chart([]).mark_point().properties(name="empty-space", width=0, height=0),
        intersection_sizes,
        set_sizes,
        matrix,
        columns=2,
    )
    .properties(
        name="upsetr-mutations",
        description=(
            "Exact mutation intersections among PTEN, TP53, EGFR, PIK3R1, "
            "and RB1 with linked hover highlighting."
        ),
        data=gs.Data(
            url=(
                "https://raw.githubusercontent.com/hms-dbmi/UpSetR/"
                "master/inst/extdata/mutations.csv"
            ),
            format=gs.data_format(type="csv"),
        ),
        spacing=3,
        scales={
            "x": {
                "domain": [0.5, 20.5],
                "paddingInner": 0.22,
                "paddingOuter": 0.12,
            },
            "y": {
                "domain": [-0.5, 4.5],
                "paddingInner": 0.16,
                "paddingOuter": 0.08,
            },
        },
    )
    .add_params(SET_CURSOR)
    .resolve_scale(x="shared", y="shared")
    .transform_regex_fold(
        columnRegex="^(PTEN|TP53|EGFR|PIK3R1|RB1)$",
        asKey="set",
        asValue="membership",
    )
    .transform_set_intersection(
        element="Identifier",
        set="set",
        membership="membership",
    )
    .transform_filter(gs.datum.profileDegree > 0)
    .transform_formula(
        expr=gs.expr.if_(gs.datum.member, gs.datum.profileSize, 0),
        as_="memberSize",
    )
    .transform_window(
        groupby=["set"],
        frame=[None, None],
        ops=["sum"],
        fields=["memberSize"],
        as_=["setSize"],
    )
    .transform_collect()
    .transform_formula(
        expr=gs.expr.if_(
            gs.expr.isValid(SET_CURSOR_Y)
            & (gs.expr.round(SET_CURSOR_Y) == gs.datum.setIndex)
            & gs.datum.member,
            1,
            0,
        ),
        as_="hoveredSetMember",
    )
    .transform_window(
        groupby=["profileKey"],
        frame=[None, None],
        ops=["max"],
        fields=["hoveredSetMember"],
        as_=["profileContainsHoveredSet"],
    )
    .transform_window(
        sort=gs.compare(
            ["profileSize", "profileKey"],
            order=["descending", "ascending"],
        ),
        ops=["dense_rank"],
        fields=[None],
        as_=["profileNumber"],
    )
    .configure_axis(
        domainColor="#999",
        gridColor="#e6e6e6",
        labelColor="#555",
        titleColor="#333",
        titleFontWeight="normal",
    )
    .configure_scale(zoom=False)
    .configure_mark(tooltip=False)
)
