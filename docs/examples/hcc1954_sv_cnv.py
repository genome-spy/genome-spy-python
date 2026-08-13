"""HCC1954 structural variants and copy number.

Somatic Severus structural-variant arcs are aligned with Wakhan total
copy-number segments for the highly rearranged HCC1954 breast-cancer cell line.
"""

import genome_spy as gs

META = {
    "category": "Copy-number plots",
    "tags": ("structural-variants", "vcf", "copy-number", "lookup"),
    "order": 35,
    "height": 420,
    "max_width": 980,
}

SV_URL = "https://data.genomespy.app/sample-data/HCC1954/severus_somatic.vcf.gz"
CN_URL = "https://data.genomespy.app/sample-data/HCC1954/copy-numbers.tsv"

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
                    "datum.INFO.SVTYPE[0] == 'BND' ? "
                    "replace(datum.ID[0], /_[12]$/, '') : datum.ID[0]"
                )
            ).title("SV ID"),
            gs.Tooltip("INFO.SVTYPE[0]").title("SV type"),
            gs.Tooltip(
                gs.expr(
                    "isValid(datum.INFO.DETAILED_TYPE) ? "
                    "datum.INFO.DETAILED_TYPE[0] : null"
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
                    "datum.SAMPLES.wakhan_haplotagged.DV[0] + ' variant, ' + "
                    "datum.SAMPLES.wakhan_haplotagged.DR[0] + ' reference'"
                )
            ).title("Read support"),
            gs.Tooltip(
                gs.expr("isValid(datum.INFO.HP) ? datum.INFO.HP[0] : null")
            ).title("Haplotype"),
            gs.Tooltip(
                gs.expr(
                    "isValid(datum.INFO.PHASESETID) ? datum.INFO.PHASESETID[0] : null"
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
        "datum.FILTER == 'PASS' && "
        "test(/^chr([1-9]|1[0-9]|2[0-2]|X|Y)$/, datum.CHROM) && "
        "test(/^(DEL|DUP|BND)$/, datum.INFO.SVTYPE[0])"
    )
    .transform_window(
        ops=["row_number"],
        as_=["_source_order"],
        description="Record VCF order so one BND mate is retained.",
    )
    .transform_formula(
        expr=("datum.INFO.SVTYPE[0] == 'BND' ? datum.INFO.MATE_ID[0] : datum.ID[0]"),
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
        "datum.INFO.SVTYPE[0] != 'BND' || datum._source_order < datum.mateOrder"
    )
    .transform_formula(expr="datum.CHROM", as_="chrom1")
    .transform_formula(expr="datum.POS", as_="breakpoint1")
    .transform_formula(
        expr=("datum.INFO.SVTYPE[0] == 'BND' ? datum.mateChrom : datum.CHROM"),
        as_="chrom2",
    )
    .transform_formula(
        expr=("datum.INFO.SVTYPE[0] == 'BND' ? datum.matePos : datum.INFO.END[0]"),
        as_="breakpoint2",
    )
    .transform_formula(expr="datum.INFO.STRANDS[0][0]", as_="strand1")
    .transform_formula(expr="datum.INFO.STRANDS[0][1]", as_="strand2")
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
