"""HCC1954 structural variants and copy number.

Somatic Severus structural-variant arcs are aligned with Wakhan total
copy-number segments for the highly rearranged HCC1954 breast-cancer cell line.
"""

import genome_spy as gs

META = {
    "category": "Copy-number plots",
    "order": 35,
    "height": 420,
    "max_width": 980,
}

SV_URL = "https://data.genomespy.app/sample-data/HCC1954/severus_somatic.vcf.gz"
CN_URL = "https://data.genomespy.app/sample-data/HCC1954/copy-numbers.tsv"

# Fold each link's two endpoints into rows so both receive a breakpoint marker.
endpoint_markers = (
    gs.Chart()
    .transform_regex_fold(
        columnRegex=["^chrom(1|2)$", "^breakpoint(1|2)$", "^strand(1|2)$"],
        asValue=["chrom", "pos", "strand"],
        asKey="endpoint",
        description="Fold both link endpoints into rows for breakpoint markers.",
    )
    .mark_rule(tooltip=None, y=0, yOffset=-0.5, opacity=0.5)
    .encode(
        x=gs.Locus("chrom", "pos", band=0),
        x2=gs.Locus("chrom", "pos", band=0),
        size=gs.Size("SAMPLES.wakhan_haplotagged.VAF[0]:Q")
        .scale(range=[0.5, 2.5], type="pow")
        .legend(None),
    )
)

sv_links = (
    gs.Chart()
    .mark_link(arcFadingDistance=gs.expr("[height - 20, height + 20]"), segments=200)
    .encode(
        x=gs.Locus("chrom1", "breakpoint1", band=0),
        x2=gs.Locus("chrom2", "breakpoint2", band=0),
        size=(
            gs.Size("SAMPLES.wakhan_haplotagged.VAF[0]:Q")
            .scale(range=[0.1, 2.5], type="pow")
            .legend(title="Variant allele frequency", orient="top")
            .condition([gs.condition("svHover", 3, empty=False)])
        ),
        opacity=gs.Opacity(gs.value(0.5)).condition(
            [gs.condition("svHover", 1, empty=False)]
        ),
        tooltip=[
            gs.Tooltip(
                gs.expr(
                    gs.expr.if_(
                        gs.datum.INFO.SVTYPE[0] == "BND",
                        gs.expr.replace(
                            gs.datum.ID[0],
                            gs.expr.regexp(r"_[12]$"),
                            "",
                        ),
                        gs.datum.ID[0],
                    )
                )
            ).title("SV ID"),
            gs.Tooltip("INFO.SVTYPE[0]").title("SV type"),
            gs.Tooltip(
                gs.expr(
                    gs.expr.if_(
                        gs.expr.isValid(gs.datum.INFO.DETAILED_TYPE),
                        gs.datum.INFO.DETAILED_TYPE[0],
                        None,
                    )
                )
            ).title("Detailed type"),
            gs.Tooltip("SAMPLES.wakhan_haplotagged.VAF[0]")
            .title("Variant allele frequency")
            .format(".3f"),
            gs.Tooltip("SAMPLES.wakhan_haplotagged.hVAF")
            .title("Haplotype VAF")
            .format(".3f"),
            gs.Tooltip("SAMPLES.wakhan_haplotagged.GT[0]").title("Genotype"),
            gs.Tooltip(
                gs.expr(
                    gs.datum.SAMPLES.wakhan_haplotagged.DV[0]
                    + " variant, "
                    + gs.datum.SAMPLES.wakhan_haplotagged.DR[0]
                    + " reference"
                )
            ).title("Read support"),
            gs.Tooltip(
                gs.expr(
                    gs.expr.if_(
                        gs.expr.isValid(gs.datum.INFO.HP),
                        gs.datum.INFO.HP[0],
                        None,
                    )
                )
            ).title("Haplotype"),
            gs.Tooltip(
                gs.expr(
                    gs.expr.if_(
                        gs.expr.isValid(gs.datum.INFO.PHASESETID),
                        gs.datum.INFO.PHASESETID[0],
                        None,
                    )
                )
            ).title("Phase set"),
            gs.Tooltip("INFO.MAPQ[0]").title("Mapping quality"),
        ],
    )
    .properties(
        title=gs.title(
            "Severus somatic structural variants loaded directly from VCF",
            orient="none",
        ),
        params=[
            gs.param(
                "svHover",
                select={"type": "point", "on": "mouseover"},
                persist=False,
            )
        ],
    )
)

sv_track = (
    (endpoint_markers + sv_links)
    .properties(
        name="sv-link-layers",
        data=gs.Data(url=SV_URL, format=gs.data_format(type="vcf")),
    )
    .encode(
        color=gs.Color("INFO.SVTYPE[0]:N")
        .scale(
            domain=["DEL", "DUP", "BND"],
            range=["#2563eb", "#dc2626", "#808080"],
        )
        .legend(title="Severus SV type", orient="top")
    )
    .transform_filter(
        (gs.datum.FILTER == "PASS")
        & gs.expr.test(
            gs.expr.regexp(r"^chr([1-9]|1[0-9]|2[0-2]|X|Y)$"),
            gs.datum.CHROM,
        )
        & gs.expr.test(
            gs.expr.regexp(r"^(DEL|DUP|BND)$"),
            gs.datum.INFO.SVTYPE[0],
        )
    )
    .transform_window(
        ops=["row_number"],
        as_=["_source_order"],
        description="Record VCF order so one BND mate is retained.",
    )
    # BND records describe each link twice. Look up the mate and keep the first
    # record so the arc is drawn only once.
    .transform_formula(
        expr=gs.expr.if_(
            gs.datum.INFO.SVTYPE[0] == "BND",
            gs.datum.INFO.MATE_ID[0],
            gs.datum.ID[0],
        ),
        as_="_lookup_mate_id",
    )
    .transform_lookup(
        from_={"source": "input"},
        fields="_lookup_mate_id",
        key="ID[0]",
        values=["CHROM", "POS", "_source_order"],
        as_=["mateChrom", "matePos", "mateOrder"],
    )
    .transform_filter(
        (gs.datum.INFO.SVTYPE[0] != "BND")
        | (gs.datum._source_order < gs.datum.mateOrder)
    )
    .transform_formula(expr=gs.datum.CHROM, as_="chrom1")
    .transform_formula(expr=gs.datum.POS, as_="breakpoint1")
    .transform_formula(
        expr=gs.expr.if_(
            gs.datum.INFO.SVTYPE[0] == "BND",
            gs.datum.mateChrom,
            gs.datum.CHROM,
        ),
        as_="chrom2",
    )
    .transform_formula(
        expr=gs.expr.if_(
            gs.datum.INFO.SVTYPE[0] == "BND",
            gs.datum.matePos,
            gs.datum.INFO.END[0],
        ),
        as_="breakpoint2",
    )
    .transform_formula(expr=gs.datum.INFO.STRANDS[0][0], as_="strand1")
    .transform_formula(expr=gs.datum.INFO.STRANDS[0][1], as_="strand2")
    .transform_identifier()
)

copy_numbers = (
    gs.Chart(gs.Data(url=CN_URL))
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        color=gs.Color("relative_copy_ratio:Q")
        .scale(
            domain=[0, 1, 3, 8],
            range=["#1060f8", "#f6f6f6", "#ff4000", "#801800"],
        )
        .legend(title="Total CN / ploidy", values=[0, 1, 3, 8]),
    )
    .properties(
        name="copy-numbers",
        title=gs.title(
            "Wakhan total copy number relative to ploidy (4.57)", orient="none"
        ),
        height=32,
    )
)

# A shared locus scale keeps the SV endpoints aligned with their copy-number
# segments while panning and zooming.
chart = (
    (sv_track & copy_numbers)
    .properties(
        assembly="hg38",
        description=(
            "Paired Severus somatic SV arcs and Wakhan ploidy-relative "
            "copy-number segments for HCC1954."
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr21", "pos": 4708647},
                    {"chrom": "chr22", "pos": 43863053},
                ]
            )
        ),
        spacing=2,
    )
    .resolve_scale(x="shared")
    .resolve_axis(x="shared")
)
