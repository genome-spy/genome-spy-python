"""Interactive ASCAT purity/ploidy fitting.

A parameterized sunrise plot evaluates integer-copy-number fits while linked
tracks show how the selected purity, ploidy, and LogR decompaction affect the
rounded allele-specific solution.
"""

import genome_spy as gs

META = {
    "category": "Copy-number plots",
    "order": 24,
    "height": 900,
    "max_width": 980,
}

SAMPLES = ["S17", "S36", "S54", "S64", "S77", "S84", "S96", "S97", "S100"]
ASCAT_SOLUTIONS = [
    {"sample": "S17", "rho": 0.25, "psi": 3.15},
    {"sample": "S36", "rho": 0.25, "psi": 1.9},
    {"sample": "S54", "rho": 1, "psi": 2.15},
    {"sample": "S64", "rho": 1, "psi": 2.15},
    {"sample": "S77", "rho": 0.53, "psi": 1.85},
    {"sample": "S84", "rho": 0.24, "psi": 1.9},
    {"sample": "S96", "rho": 0.55, "psi": 2.75},
    {"sample": "S97", "rho": 0.41, "psi": 1.7},
    {"sample": "S100", "rho": 0.65, "psi": 3.4},
]

SEGMENT_URL = {
    "expr": (
        "'https://data.genomespy.app/sample-data/ASCAT/"
        "ascat_fit_segments_' + sample + '.tsv.gz'"
    )
}
RAW_URL = {
    "expr": (
        "'https://data.genomespy.app/sample-data/ASCAT/ascat_raw_' + sample + '.tsv.gz'"
    )
}

sunrise_rects = (
    gs.Chart()
    .mark_rect(tooltip=None)
    .encode(
        x=gs.X("psiStart:Q")
        .scale(domain=[1, 6])
        .axis(title="Tumor ploidy (psi)", format=".1f"),
        x2=gs.X2("psiEnd"),
        y=gs.Y("rhoStart:Q")
        .scale(domain=[0.1, 1.05])
        .axis(title="Tumor purity (rho)", format=".2f"),
        y2=gs.Y2("rhoEnd"),
        color=gs.Color("meanRoundingError:Q").scale(
            scheme="redblue", type="log", reverse=True
        ),
    )
    .properties(name="sunrise-rects")
)

published_solution = (
    gs.Chart(gs.Data(name="ascat-solutions"))
    .transform_filter("datum.sample === sample")
    .mark_point(shape="x", angle=0, size=180, strokeWidth=2, color="#00d000")
    .encode(
        x=gs.X("psi:Q"),
        y=gs.Y("rho:Q"),
        tooltip=[
            gs.Tooltip("sample").title("ASCAT-selected solution"),
            gs.Tooltip("rho").title("Tumor purity (rho)"),
            gs.Tooltip("psi").title("Tumor ploidy (psi)"),
        ],
    )
    .properties(title="ascat-solution")
)

sunrise = (
    (sunrise_rects + published_solution)
    .properties(
        name="sunrise-plot",
        title=gs.Title(
            text=gs.expr("'Purity/ploidy integer-fit distance - ' + sample"),
            style="overlay-title",
        ),
        height=240,
        params=[
            gs.param(
                "selectedFit",
                push="outer",
                value={"x": 2.75, "y": 0.56},
                ruler={
                    "encodings": ["x", "y"],
                    "on": "mousedown",
                    "clear": False,
                    "snap": False,
                    "mark": {"strokeDash": [5, 3]},
                },
            )
        ],
        data={
            "sequence": {
                "start": 0.1,
                "stop": 1.051,
                "step": 0.01,
                "as": "rhoCandidate",
            }
        },
    )
    .resolve_scale(x="excluded")
    .resolve_axis(x="excluded")
    .transform_cross(
        from_={
            "data": {
                "sequence": {
                    "start": 1,
                    "stop": 6.001,
                    "step": 0.05,
                    "as": "psiCandidate",
                }
            }
        }
    )
    .transform_cross(
        from_={
            "data": {"url": SEGMENT_URL},
            "transform": [
                {"type": "filter", "expr": "datum.chr !== 'X'"},
                {
                    "type": "project",
                    "fields": ["logRMean", "bafMean", "nProbes"],
                },
                {
                    "type": "formula",
                    "expr": (
                        "datum.nProbes * (downweightBalanced && "
                        "datum.bafMean === 0.5 ? 0.05 : 1)"
                    ),
                    "as": "fitWeight",
                },
            ],
        }
    )
)

for field, expression in [
    (
        "bRawCandidate",
        "(datum.rhoCandidate - 1 + pow(2, datum.logRMean / gamma) * "
        "datum.bafMean * (2 * (1 - datum.rhoCandidate) + "
        "datum.rhoCandidate * datum.psiCandidate)) / datum.rhoCandidate",
    ),
    (
        "aRawCandidate",
        "(datum.rhoCandidate - 1 + pow(2, datum.logRMean / gamma) * "
        "(1 - datum.bafMean) * (2 * (1 - datum.rhoCandidate) + "
        "datum.rhoCandidate * datum.psiCandidate)) / datum.rhoCandidate",
    ),
    ("nMinorCandidate", "max(0, round(datum.bRawCandidate))"),
    ("nMajorCandidate", "max(0, round(datum.aRawCandidate))"),
    (
        "errorSquaredWeighted",
        "(pow(datum.bRawCandidate - datum.nMinorCandidate, 2) + "
        "(fitBothAlleles ? pow(datum.aRawCandidate - datum.nMajorCandidate, 2) "
        ": 0)) * datum.fitWeight",
    ),
]:
    sunrise = sunrise.transform_formula(expr=expression, as_=field)

sunrise = sunrise.transform_aggregate(
    groupby=["rhoCandidate", "psiCandidate"],
    fields=["fitWeight", "errorSquaredWeighted"],
    ops=["sum", "sum"],
    as_=["totalWeight", "distanceSum"],
)

for field, expression in [
    (
        "meanRoundingError",
        "datum.distanceSum / (datum.totalWeight * (fitBothAlleles ? 2 : 1))",
    ),
    ("rhoStart", "max(0.1, datum.rhoCandidate - 0.005)"),
    ("rhoEnd", "min(1.05, datum.rhoCandidate + 0.005)"),
    ("psiStart", "max(1, datum.psiCandidate - 0.025)"),
    ("psiEnd", "min(6, datum.psiCandidate + 0.025)"),
]:
    sunrise = sunrise.transform_formula(expr=expression, as_=field)

fit_bar = (
    gs.Chart()
    .mark_rect(color="#a0e7e5", tooltip=None)
    .encode(
        x=gs.X("goodnessOfFit:Q").scale(domain=[0, 100], clamp=True).axis(None),
        x2=gs.datum(0),
    )
    .properties(name="bar")
)
fit_text = (
    gs.Chart()
    .mark_text(size=12, tooltip=None)
    .encode(
        x=gs.value(0.5),
        x2=None,
        text=gs.Text(
            gs.expr(
                "'rho ' + (round(selectedFit.values.y * 1000) / 1000) + "
                "' | psi ' + (round(selectedFit.values.x * 1000) / 1000) + "
                "' | gamma ' + gamma + ' | score ' + "
                "(round(datum.goodnessOfFit * 100) / 100)"
            )
        ),
    )
    .properties(name="text")
)
selected_fit = (
    (fit_bar + fit_text)
    .properties(
        name="selectedGoodnessOfFit",
        title=gs.title("Selected fit", orient="none"),
        height=24,
    )
    .resolve_scale(x="excluded")
    .resolve_axis(x="excluded")
    .transform_filter("datum.chr !== 'X'")
    .transform_project(fields=["bafMean", "aError", "bError", "nProbes"])
    .transform_formula(
        expr=(
            "datum.nProbes * (downweightBalanced && datum.bafMean === 0.5 ? 0.05 : 1)"
        ),
        as_="fitWeight",
    )
    .transform_formula(
        expr=(
            "(datum.bError * datum.bError + (fitBothAlleles ? "
            "datum.aError * datum.aError : 0)) * datum.fitWeight"
        ),
        as_="errorSquaredWeighted",
    )
    .transform_aggregate(
        fields=["fitWeight", "errorSquaredWeighted"],
        ops=["sum", "sum"],
        as_=["totalWeight", "distanceSum"],
    )
    .transform_formula(
        expr=(
            "100 - datum.distanceSum / (datum.totalWeight * "
            "(fitBothAlleles ? 2 : 1) * 0.25) * 100"
        ),
        as_="goodnessOfFit",
    )
)

minor_error = (
    gs.Chart()
    .mark_rect(
        minWidth=gs.expr("minLength"),
        fillOpacity=0.15,
        strokeOpacity=1,
        strokeWidth=1,
        fill="gray",
        stroke="#88d27a",
    )
    .encode(
        y=gs.Y("bRaw:Q"),
        y2=gs.Y2("nMinor"),
        strokeOpacity=gs.StrokeOpacity("bError:Q").scale(
            type="pow", base=2, domain=[0, 0.5], range=[0, 0.8]
        ),
    )
)
major_error = (
    gs.Chart()
    .mark_rect(
        minWidth=gs.expr("minLength"),
        fillOpacity=0.15,
        strokeOpacity=1,
        strokeWidth=1,
        fill="gray",
        stroke="#f06850",
    )
    .encode(
        y=gs.Y("aRaw:Q"),
        y2=gs.Y2("nMajor"),
        strokeOpacity=gs.StrokeOpacity("aError:Q").scale(
            type="pow", base=2, domain=[0, 0.5], range=[0, 0.8]
        ),
    )
)
minor_rounded = (
    gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"), yOffset=-3)
    .encode(
        y=gs.Y("nMinor:Q")
        .scale(domain=[0, 6], padding=0.04, clamp=True)
        .axis(tickMinStep=1),
        size=gs.value(5),
        color=gs.value("#88d27a"),
    )
)
major_rounded = (
    gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"), yOffset=3)
    .encode(
        y=gs.Y("nMajor:Q").scale(domain=[0, 6]),
        size=gs.value(5),
        color=gs.Color("nMajor:Q").scale(
            domain=[0, 6, 16], range=["#f06850", "#f06850", "#5F0F0F"]
        ),
    )
)
rounded_copy_number = (
    minor_error + major_error + minor_rounded + major_rounded
).properties(
    name="roundedAndDifference",
    title=gs.title(
        "Copy numbers rounded to integers + difference to raw values",
        style="overlay",
    ),
    height=gs.SizeDef(grow=2),
)
selected_solution = (selected_fit & rounded_copy_number).resolve_axis(x="shared")


def raw_probe_track(field: str) -> gs.Chart:
    """Build one dynamically sized raw ASCAT probe layer."""
    chart = (
        gs.Chart(gs.Data(url=RAW_URL))
        .mark_point(
            size=gs.expr("min(pow(zoomLevel, 2) * width * height / 10000, 100)"),
            color="#aab",
            opacity=0.3,
        )
        .encode(x=gs.Locus("chr", "pos"), y=gs.Y(f"{field}:Q").title(None))
        .properties(title="Single probe")
    )
    return chart.transform_filter("datum.baf !== null") if field == "baf" else chart


logr_track = (
    raw_probe_track("logR")
    + gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"))
    .encode(
        y=gs.Y("logRMean:Q").title("LogR"), size=gs.value(3), color=gs.value("black")
    )
    + gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"))
    .encode(
        y=gs.Y("logRMean_ASCAT:Q").title(None),
        size=gs.value(2),
        color=gs.value("#f06850"),
    )
).properties(
    name="logRTrack",
    title=gs.title("Observed and fitted LogR", style="overlay-title"),
)

baf_track = (
    raw_probe_track("baf")
    + gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"))
    .encode(
        y=gs.Y("bafMean:Q").scale(domain=[0, 1]).title("BAF"),
        size=gs.value(3),
        color=gs.value("black"),
    )
    + gs.Chart()
    .mark_rule(minLength=3)
    .encode(
        y=gs.Y(gs.expr("1 - datum.bafMean"), type="quantitative").title(None),
        size=gs.value(3),
        color=gs.value("black"),
    )
    + gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"))
    .encode(
        y=gs.Y("bafMean_ASCAT:Q").title(None),
        size=gs.value(2),
        color=gs.value("#88d27a"),
    )
    + gs.Chart()
    .mark_rule(minLength=gs.expr("minLength"))
    .encode(
        y=gs.Y(gs.expr("1 - datum.bafMean_ASCAT"), type="quantitative").title(None),
        size=gs.value(2),
        color=gs.value("#f06850"),
    )
).properties(
    name="bafTrack",
    title=gs.title("Observed and fitted B-allele frequency", style="overlay-title"),
)

chart = (
    (sunrise & selected_solution & logr_track & baf_track)
    .properties(
        assembly="hg19",
        datasets={"ascat-solutions": ASCAT_SOLUTIONS},
        params=[
            gs.param("minLength", value=1),
            gs.param("selectedFit"),
            gs.param(
                "sample",
                value="S96",
                bind={"input": "select", "options": SAMPLES, "name": "Sample"},
            ),
            gs.param(
                "gamma",
                value=0.55,
                bind={
                    "input": "range",
                    "min": 0.2,
                    "max": 1.2,
                    "step": 0.05,
                    "name": "LogR decompaction (gamma)",
                    "debounce": 100,
                },
            ),
            gs.param(
                "downweightBalanced",
                value=True,
                bind={"input": "checkbox", "name": "Downweight balanced segments"},
            ),
            gs.param(
                "fitBothAlleles",
                value=False,
                bind={"input": "checkbox", "name": "Include both alleles in fit"},
            ),
        ],
        data=gs.Data(url=SEGMENT_URL),
        background="#fafafa",
        description=(
            "Interactive ASCAT-like purity/ploidy fitting with linked rounded "
            "copy-number, LogR, and BAF tracks."
        ),
    )
    .encode(
        x=gs.Locus("chr", "startpos").scale(type="locus").axis(title=None),
        x2=gs.Locus("chr", "endpos", offset=1),
    )
    .transform_collect()
)

for field, expression in [
    (
        "aRaw",
        "(selectedFit.values.y - 1 + pow(2, datum.logRMean / gamma) * "
        "(1 - datum.bafMean) * (2 * (1 - selectedFit.values.y) + "
        "selectedFit.values.y * selectedFit.values.x)) / selectedFit.values.y",
    ),
    (
        "bRaw",
        "(selectedFit.values.y - 1 + pow(2, datum.logRMean / gamma) * "
        "datum.bafMean * (2 * (1 - selectedFit.values.y) + "
        "selectedFit.values.y * selectedFit.values.x)) / selectedFit.values.y",
    ),
    ("nMajor", "max(0, round(datum.aRaw))"),
    ("nMinor", "max(0, round(datum.bRaw))"),
    ("aError", "abs(datum.aRaw - datum.nMajor)"),
    ("bError", "abs(datum.bRaw - datum.nMinor)"),
    (
        "logRMean_ASCAT",
        "gamma * log((2 * (1 - selectedFit.values.y) + selectedFit.values.y * "
        "(datum.nMajor + datum.nMinor)) / (2 * (1 - selectedFit.values.y) + "
        "selectedFit.values.y * selectedFit.values.x)) / LN2",
    ),
    (
        "bafMean_ASCAT",
        "(1 - selectedFit.values.y + selectedFit.values.y * datum.nMinor) / "
        "(2 - 2 * selectedFit.values.y + selectedFit.values.y * "
        "(datum.nMajor + datum.nMinor))",
    ),
]:
    chart = chart.transform_formula(expr=expression, as_=field)

chart = (
    chart.transform_identifier()
    .resolve_axis(x="shared")
    .configure_axis_x(grid=False, chromGrid=True, orient="bottom")
    .configure_axis_y(grid=True, gridColor="#f8f8f8")
    .configure_legend(disable=True)
    .configure_view(
        fill="white",
        stroke="#c8c8c8",
        shadowBlur=8,
        shadowColor="black",
        shadowOpacity=0.1,
    )
)
