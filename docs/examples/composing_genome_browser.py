"""Composing a genome browser.

Cytoband, six-frame translation, BAM alignment, and RefSeq track specs are
written out with the Python API and aligned under a shared genomic scale.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 38,
    "height": 650,
    "max_width": 980,
}


def _build_cytoband_track() -> gs.Chart:
    """Build the cytoband track in this example."""
    stain_domain = [
        "gneg",
        "gpos25",
        "gpos50",
        "gpos75",
        "gpos100",
        "acen",
        "stalk",
        "gvar",
    ]

    band_layer = (
        gs.Chart()
        .mark_rect()
        .encode(
            color=gs.Color("gieStain:N")
            .scale(
                domain=stain_domain,
                range=[
                    "#f0f0f0",
                    "#e0e0e0",
                    "#d0d0d0",
                    "#c0c0c0",
                    "#a0a0a0",
                    "#cc4444",
                    "#338833",
                    "#000000",
                ],
            )
            .legend(None)
        )
        .properties(title="Cytoband")
    )

    label_layer = (
        gs.Chart()
        .mark_text(
            align="center",
            baseline="middle",
            paddingX=4,
            tooltip=None,
        )
        .encode(
            color=gs.Color("gieStain:N")
            .scale(
                domain=stain_domain,
                range=[
                    "black",
                    "black",
                    "black",
                    "black",
                    "black",
                    "black",
                    "white",
                    "white",
                ],
            )
            .legend(None),
            text=gs.Text("name:N"),
        )
    )

    separator_layer = (
        gs.Chart()
        .encode(x2=None)
        .mark_rule(color="#a0a0a0", strokeDash=[3, 3], strokeDashOffset=2)
        .transform_filter((gs.datum.chromStart == 0) & (gs.datum.chrom != "chr1"))
    )

    # The shared encoding keeps all cytoband layers on the same loci.
    return (
        gs.layer(band_layer, label_layer, separator_layer)
        .properties(
            name="ideogram-track",
            title=gs.title("Chromosome Ideogram", style="track-title"),
            data=gs.Data(
                url="https://data.genomespy.app/genomes/hg38/cytoBand.txt.gz",
                format=gs.data_format(
                    type="tsv",
                    columns=["chrom", "chromStart", "chromEnd", "name", "gieStain"],
                ),
            ),
        )
        .encode(x=gs.Locus("chrom", "chromStart"), x2=gs.Locus("chrom", "chromEnd"))
        .transform_filter(~gs.expr.test(gs.expr.regexp("_"), gs.datum.chrom))
        .resolve_scale(color="independent")
    )


def _build_six_frame_translation_track() -> gs.Chart:
    """Build the six frame translation track in this example."""
    STRAND = gs.Expression("strand")

    WIDTH = gs.Expression("width")

    COMPLEMENTS = [
        {"base": base, "complement": complement}
        for base, complement in zip("ACGTN", "TGCAN", strict=True)
    ]

    AMINO_ACIDS = {
        "TTT": "F",
        "TTC": "F",
        "TTA": "L",
        "TTG": "L",
        "TCT": "S",
        "TCC": "S",
        "TCA": "S",
        "TCG": "S",
        "TAT": "Y",
        "TAC": "Y",
        "TAA": "STOP",
        "TAG": "STOP",
        "TGT": "C",
        "TGC": "C",
        "TGA": "STOP",
        "TGG": "W",
        "CTT": "L",
        "CTC": "L",
        "CTA": "L",
        "CTG": "L",
        "CCT": "P",
        "CCC": "P",
        "CCA": "P",
        "CCG": "P",
        "CAT": "H",
        "CAC": "H",
        "CAA": "Q",
        "CAG": "Q",
        "CGT": "R",
        "CGC": "R",
        "CGA": "R",
        "CGG": "R",
        "ATT": "I",
        "ATC": "I",
        "ATA": "I",
        "ATG": "M",
        "ACT": "T",
        "ACC": "T",
        "ACA": "T",
        "ACG": "T",
        "AAT": "N",
        "AAC": "N",
        "AAA": "K",
        "AAG": "K",
        "AGT": "S",
        "AGC": "S",
        "AGA": "R",
        "AGG": "R",
        "GTT": "V",
        "GTC": "V",
        "GTA": "V",
        "GTG": "V",
        "GCT": "A",
        "GCC": "A",
        "GCA": "A",
        "GCG": "A",
        "GAT": "D",
        "GAC": "D",
        "GAA": "E",
        "GAG": "E",
        "GGT": "G",
        "GGC": "G",
        "GGA": "G",
        "GGG": "G",
    }

    GENETIC_CODE = [
        {
            "codon": codon,
            "aminoAcid": amino_acid,
            "kind": (
                "start"
                if codon == "ATG"
                else "stop"
                if amino_acid == "STOP"
                else "other"
            ),
        }
        for codon, amino_acid in AMINO_ACIDS.items()
    ]

    base_colors = gs.Scale(
        domain=["A", "C", "T", "G", "a", "c", "t", "g", "N"],
        range=[
            "#7BD56C",
            "#FF9B9B",
            "#86BBF1",
            "#FFC56C",
            "#7BD56C",
            "#FF9B9B",
            "#86BBF1",
            "#FFC56C",
            "#E0E0E0",
        ],
    )

    reference_background = (
        gs.Chart().mark_rect(tooltip=None).properties(name="reference-base-background")
    )

    reference_labels = (
        gs.Chart()
        .mark_text(
            size=13,
            fitToBand=True,
            paddingX=1.5,
            paddingY=1,
            opacity=0.7,
            flushX=False,
            tooltip=None,
        )
        .encode(color=gs.value("black"), text=gs.Text("base"))
        .properties(name="reference-base-labels")
    )

    reference = (
        (reference_background + reference_labels)
        .properties(name="reference-bases", height=20)
        .encode(
            x=gs.Locus("chrom", "pos"),
            color=gs.Color("base:N").scale(base_colors).legend(None),
        )
    )

    amino_acids = (
        gs.Chart()
        .mark_arrow(
            style="arrow-block-notch",
            stroke="#C0C0C0",
            headAngle=65,
            strokeWidth=gs.expr(
                1.0
                - gs.expr.smoothstep(
                    0.2,
                    1,
                    gs.expr.span(gs.expr.domain("x")) / WIDTH,
                )
            ),
            tooltip=None,
        )
        .encode(
            direction=gs.value(gs.expr(STRAND)),
            color=gs.Color("kind:N")
            .scale(
                domain=["start", "stop", "other", "?"],
                range=["#40B050", "#F06060", "#F8F8F8", "#E0E0E0"],
            )
            .legend(None),
        )
        .properties(name="amino-acids")
    )

    amino_acid_labels = (
        gs.Chart()
        .mark_text(size=12, paddingX=1.5, tooltip=None)
        .encode(color=gs.value("black"), text=gs.Text("aminoAcid"))
        .properties(name="amino-acid-labels")
    )

    def translation_strand(strand: str, name: str) -> gs.Chart:
        return (
            (amino_acids + amino_acid_labels)
            .properties(name=name, params=[gs.param("strand", value=strand)])
            .transform_formula(
                expr=gs.expr.if_(
                    STRAND == "reverse",
                    gs.datum.complement2 + gs.datum.complement1 + gs.datum.complement,
                    gs.datum.base + gs.datum.base1 + gs.datum.base2,
                ),
                as_="codon",
            )
            .transform_lookup(from_={"name": "geneticCode"}, key="codon", default="?")
            .transform_formula(expr=STRAND + " " + (gs.datum.pos % 3), as_="lane")
        )

    translation = (
        (
            translation_strand("forward", "forward-translation")
            + translation_strand("reverse", "reverse-translation")
        )
        .properties(
            name="translation",
            height=gs.step(17),
        )
        .with_view(stroke="#c0c0c0")
        .encode(
            y=gs.Y("lane:O")
            .scale(
                domain=[
                    "forward 2",
                    "forward 1",
                    "forward 0",
                    "reverse 0",
                    "reverse 1",
                    "reverse 2",
                ]
            )
            .axis(title=None),
            x=gs.Locus("chrom", "pos", band=0),
            x2=gs.Locus("chrom", "end", band=0),
        )
        .transform_formula(expr=gs.expr.upper(gs.datum.base), as_="base")
        .transform_lookup(
            from_={"name": "nucleotideComplements"},
            key="base",
            values=["complement"],
            default="N",
        )
        # Lead windows collect the next two bases needed to form each codon.
        .transform_window(
            sort=gs.compare("pos"),
            ops=["lead", "lead", "lead", "lead"],
            fields=["base", "base", "complement", "complement"],
            params=[1, 2, 1, 2],
            as_=["base1", "base2", "complement1", "complement2"],
        )
        .transform_filter(
            gs.expr.isValid(gs.datum.base2) & gs.expr.isValid(gs.datum.complement2)
        )
        .transform_formula(expr=gs.datum.pos + 3, as_="end")
    )

    # The indexed FASTA source loads and translates the visible sequence.
    return (
        (reference & translation)
        .properties(
            name="indexed-fasta-six-frame-translation",
            datasets={
                "nucleotideComplements": COMPLEMENTS,
                "geneticCode": GENETIC_CODE,
            },
            data=gs.lazy.indexed_fasta(
                "https://data.genomespy.app/genomes/hg38/hg38.fa"
            ),
            spacing=5,
        )
        .transform_flatten_sequence(field="sequence", as_=["rawPos", "base"])
        .transform_formula(expr=gs.datum.start + gs.datum.rawPos, as_="pos")
    )


def _build_bam_alignment_track() -> gs.Chart:
    """Build the bam alignment track in this example."""
    read_tooltips = [
        gs.Tooltip("name").title("Read"),
        gs.Tooltip("strand").title("Strand"),
        gs.Tooltip("isPaired").title("Paired"),
        gs.Tooltip("isProperPair").title("Proper pair"),
        gs.Tooltip("isDuplicate").title("Duplicate"),
        gs.Tooltip("isQcFail").title("QC fail"),
        gs.Tooltip("isSecondary").title("Secondary"),
        gs.Tooltip("isSupplementary").title("Supplementary"),
        gs.Tooltip("mapq").title("Mapping quality"),
        gs.Tooltip("cigar").title("CIGAR"),
    ]

    base_colors = gs.Scale(
        domain=["A", "C", "T", "G", "N"],
        range=["#4FBF45", "#4D96E8", "#E85F78", "#E8B322", "#BDBDBD"],
    )

    LANE_HEIGHT = gs.Expression("laneHeight")

    MIN_MAPQ = gs.Expression("minMapq")

    MIN_BASE_QUALITY = gs.Expression("minBaseQuality")

    WINDOW_SIZE = gs.Expression("windowSize")

    depth = (
        gs.Chart()
        .transform_flatten_cigar(copyFields=["chrom"])
        .transform_filter(gs.datum.cigarType == "aligned")
        .transform_collect(sort=gs.compare(["chrom", "cigarStart"]))
        .transform_coverage(
            chrom="chrom",
            start="cigarStart",
            end="cigarEnd",
            as_="coverage",
            asStart="start",
            asEnd="end",
        )
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "start", band=0),
            x2=gs.Locus("chrom", "end", band=0),
            y=gs.Y("coverage:Q").axis(tickCount=2, title="Depth"),
            color=gs.value("#d0d0d0"),
        )
        .properties(name="depth", title="Depth")
    )

    mismatch_summary = (
        gs.Chart()
        .transform_filter(gs.datum.md != None)  # noqa: E711
        .transform_alignment_mismatches(copyFields=["chrom"])
        .transform_filter(
            (gs.datum.baseQuality == None)  # noqa: E711
            | (gs.datum.baseQuality >= MIN_BASE_QUALITY)
        )
        .transform_aggregate(groupby=["chrom", "mismatchStart", "base"])
        .transform_stack(
            field="count",
            groupby=["chrom", "mismatchStart"],
            sort=gs.compare("base", order="ascending"),
            as_=["mismatchCount0", "mismatchCount1"],
        )
        .transform_formula(expr=gs.datum.mismatchStart + 1, as_="mismatchEnd")
        .mark_rect()
        .encode(
            x=gs.Locus("chrom", "mismatchStart", band=0),
            x2=gs.Locus("chrom", "mismatchEnd", band=0),
            y=gs.Y("mismatchCount0:Q"),
            y2=gs.Y2("mismatchCount1"),
            color=gs.Color("base:N").scale(base_colors).legend(None),
        )
        .properties(name="mismatch-summary", title="Mismatch support")
    )

    insertion_summary = (
        gs.Chart()
        .transform_flatten_cigar(copyFields=["chrom"])
        .transform_filter(gs.datum.cigarType == "insertion")
        .transform_aggregate(groupby=["chrom", "cigarStart"])
        .mark_rule(color="black", size=1)
        .encode(
            x=gs.Locus("chrom", "cigarStart", band=0),
            y=gs.datum(0, type="quantitative"),
            y2=gs.Y2("count"),
        )
        .properties(name="insertion-summary", title="Insertion support")
    )

    coverage = (
        (depth + mismatch_summary + insertion_summary)
        .properties(
            name="coverage",
            title=gs.Title(
                text="Depth and mismatch support",
                style="overlay-title",
                fontSize=11,
            ),
            height=40,
        )
        .resolve_scale(color="independent")
    )

    read_backbone = (
        gs.Chart()
        .mark_arrow(
            style="arrow-block",
            minStemLength=10,
            fill="#e0e0e0",
            stroke="#c4c4c4",
            strokeWidth=gs.expr(gs.expr.linearstep(3, 8, LANE_HEIGHT)),
        )
        .encode(
            x=gs.Locus("chrom", "start", band=0),
            x2=gs.Locus("chrom", "end", band=0),
            direction=gs.Direction("strand:N").scale(
                domain=["+", "-"], range=["forward", "reverse"]
            ),
            opacity=gs.Opacity("_mapqOrZero:Q")
            .scale(domain=[0, 60], range=[0.25, 1])
            .legend(
                title="Mapping quality",
                values=[0, 20, 40, 60],
            ),
            tooltip=read_tooltips,
        )
        .properties(name="read-backbone", title="Read alignment")
    )

    deletions = gs.layer(
        gs.Chart()
        .transform_filter(gs.datum.cigarType == "deletion")
        .mark_rect(color="white", minWidth=1),
        gs.Chart()
        .transform_filter(gs.datum.cigarType == "deletion")
        .mark_rule(color="#222", minLength=1),
    )

    deletions = deletions.properties(name="deletions", title="Deletion").encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        x2=gs.Locus("chrom", "cigarEnd", band=0),
    )

    skips = (
        gs.Chart()
        .transform_filter(gs.datum.cigarType == "skip")
        .mark_rule(color="#6b6b6b", strokeDash=[2, 2], minLength=1)
        .encode(
            x=gs.Locus("chrom", "cigarStart", band=0),
            x2=gs.Locus("chrom", "cigarEnd", band=0),
        )
        .properties(name="skips", title="Skipped region")
    )

    insertions = (
        gs.Chart()
        .transform_filter(gs.datum.cigarType == "insertion")
        .mark_text(
            text="I",
            color="black",
            size=gs.expr(LANE_HEIGHT * 0.90),
            font="Radley",
        )
        .encode(
            x=gs.Locus("chrom", "cigarStart", band=0),
            x2=None,
            tooltip=[
                gs.Tooltip(
                    gs.expr(
                        gs.expr.slice(
                            gs.datum._seq,
                            gs.datum.readStart,
                            gs.datum.readEnd,
                        )
                    )
                ).title("Inserted sequence")
            ],
        )
        .properties(name="insertions", title="Insertion")
    )

    soft_clips = (
        gs.Chart()
        .transform_filter(gs.datum.cigarType == "softClip")
        .mark_text(
            text="S",
            color="#555",
            size=gs.expr(LANE_HEIGHT * 0.90),
            font="Radley",
        )
        .encode(x=gs.Locus("chrom", "cigarStart", band=0), x2=None)
        .properties(name="soft-clips", title="Soft-clipped bases")
    )

    cigar_overlays = (
        gs.layer(deletions, skips, insertions, soft_clips)
        .transform_formula(expr=gs.datum.seq, as_="_seq")
        .transform_flatten_cigar(copyFields=["chrom", "_lane", "name", "cigar", "_seq"])
        .properties(name="cigar-overlays", title="CIGAR operation")
    )

    mismatch_rects = (
        gs.Chart()
        .mark_rect(minWidth=1)
        .encode(
            color=gs.Color("base:N").scale(base_colors).legend(title="Base"),
            opacity=gs.Opacity("_baseQualityForOpacity:Q")
            .scale(domain=[5, 20], range=[0.1, 1], clamp=True, nice=False)
            .legend(title="Base quality", values=[6, 10, 15, 20]),
        )
        .properties(name="mismatch-rects", title="Mismatch")
    )

    mismatch_labels = (
        gs.Chart()
        .mark_text(color="black", size=gs.expr(LANE_HEIGHT * 0.75), tooltip=None)
        .encode(text=gs.Text("base:N"))
        .properties(name="mismatch-labels", title="Mismatch base")
    )

    mismatches = (
        (mismatch_rects + mismatch_labels)
        .transform_filter(gs.datum.md != None)  # noqa: E711
        .transform_alignment_mismatches(
            copyFields=["chrom", "_lane", "name", "cigar", "mapq", "strand"]
        )
        .transform_formula(
            expr=gs.expr.if_(gs.datum.baseQuality == None, 20, gs.datum.baseQuality),  # noqa: E711
            as_="_baseQualityForOpacity",
        )
        .transform_filter(
            (gs.datum.baseQuality == None)  # noqa: E711
            | (gs.datum.baseQuality >= MIN_BASE_QUALITY)
        )
        .properties(name="mismatches", title="Mismatch")
        .encode(
            x=gs.Locus("chrom", "mismatchStart", band=0),
            x2=gs.Locus("chrom", "mismatchEnd", band=0),
        )
    )

    read_layers = (
        gs.layer(read_backbone, cigar_overlays, mismatches)
        .properties(name="read-layers", title="Read alignments")
        .encode(y=gs.Y("_lane:I").scale(padding=0.25, reverse=True, zoom=False))
        .resolve_scale(opacity="independent")
    )

    zoom_message = gs.layer(
        gs.Chart().mark_rect(fill="white", opacity=0.7),
        gs.Chart()
        .mark_text(
            text="Zoom in closer to load data.", color="#333", size=13, yOffset=20
        )
        .encode(x=gs.value(0.5), y=gs.value(1)),
        data=[{}],
        name="zoom-message",
        params=[
            gs.param(
                "zoomMessageState",
                expr=gs.expr.if_(
                    gs.expr.abs(gs.expr.span(gs.expr.domain("x"))) > WINDOW_SIZE,
                    1,
                    0,
                ),
                transition={"type": "lerp", "halfLife": 60},
            )
        ],
        opacity=gs.expr("zoomMessageState"),
    )

    read_alignments = (
        gs.layer(read_layers, zoom_message)
        .properties(
            name="read-alignments",
            title=gs.Title(text="Read alignments", orient="none"),
            height=gs.Step(step=gs.expr(LANE_HEIGHT)),
            viewportHeight="container",
            params=[
                gs.param(
                    "laneHeight",
                    value=12,
                    bind={"input": "range", "min": 1, "max": 30, "step": 1},
                    transition={"type": "lerp", "halfLife": 30, "epsilon": 0.02},
                )
            ],
        )
        .resolve_scale(color="independent", opacity="independent")
    )

    # The lazy BAM source keeps depth and reads synchronized while zooming.
    return (
        (coverage & read_alignments.properties(viewportHeight=300))
        .properties(
            data=gs.lazy.bam(
                "https://data.genomespy.app/sample-data/NIST-HG002/HG002.GRCh38.chr20_9950000_10100000.downsample33pct.bam",
                windowSize=gs.expr("windowSize"),
            ),
            params=[
                gs.param(
                    "minMapq",
                    value=0,
                    bind={
                        "input": "range",
                        "min": 0,
                        "max": 60,
                        "step": 1,
                        "debounce": 100,
                    },
                ),
                gs.param(
                    "minBaseQuality",
                    value=0,
                    bind={
                        "input": "range",
                        "min": 0,
                        "max": 40,
                        "step": 1,
                        "debounce": 100,
                    },
                ),
                gs.param("windowSize", value=15000),
            ],
            spacing=5,
            description="BAM depth, alignments, CIGAR operations, and mismatches.",
        )
        .transform_filter(
            (gs.datum.mapq == None) | (gs.datum.mapq >= MIN_MAPQ)  # noqa: E711
        )
        .transform_formula(
            expr=gs.expr.if_(gs.datum.mapq == None, 0, gs.datum.mapq),  # noqa: E711
            as_="_mapqOrZero",
        )
        .transform_pileup(start="start", end="end", as_="_lane")
        .resolve_axis(x="shared")
    )


def _build_refseq_track() -> gs.Chart:
    """Build the refseq track in this example."""
    exons = (
        gs.Chart()
        .transform_project(fields=["_lane", "_start", "exons"])
        .transform_flatten_compressed_exons(start="_start")
        .mark_rect(minOpacity=0.2, minWidth=0.5, tooltip=None)
        .encode(x=gs.X("exonStart:L"), x2=gs.X2("exonEnd"))
        .properties(name="exons")
    )

    bodies = (
        gs.Chart()
        .mark_rule(minLength=0.5, size=1, tooltip=None)
        .encode(
            x=gs.X("_start:L"),
            x2=gs.X2("_end"),
            search=gs.Search("symbol"),
        )
        .properties(name="bodies", title="Gene annotations")
    )

    transcripts = (
        (exons + bodies)
        .encode(color=gs.value("#909090"))
        .properties(
            name="transcripts",
            opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
        )
    )

    labels = (
        gs.Chart()
        .mark_text(size=11, yOffset=7, tooltip=gs.HandledTooltip(handler="refseqgene"))
        .encode(x=gs.X("_centroid:L"), text=gs.Text("symbol:N"))
        .properties(name="labels")
    )

    arrows = (
        gs.Chart()
        .mark_point(yOffset=7, size=50, tooltip=None)
        .encode(
            x=gs.X("_centroid:L"),
            dx=gs.Dx(
                gs.expr(
                    (gs.datum._textWidth / 2 + 5)
                    * gs.expr.if_(gs.datum.strand == "-", -1, 1)
                ),
                type="quantitative",
            ).scale(None),
            color=gs.value("black"),
            shape=gs.Shape("strand:N")
            .scale(domain=["-", "+"], range=["triangle-left", "triangle-right"])
            .legend(None),
        )
        .properties(
            name="arrows",
            opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1]),
        )
    )

    symbols = (
        (labels + arrows)
        .properties(name="symbols")
        .transform_measure_text(field="symbol", as_="_textWidth", fontSize=11)
        .transform_filter_scored_labels(
            lane="_lane",
            score="score",
            width="_textWidth",
            pos="_centroid",
            padding=5,
        )
    )

    # Linearized coordinates drive lane packing while loci remain genomic.
    return (
        gs.layer(transcripts, symbols)
        .properties(
            name="refseq-track",
            title=gs.title("RefSeq Gene annotation", orient="none"),
            height=gs.step(23),
            data=gs.Data(
                url="https://data.genomespy.app/genomes/hg38/refSeqGenes-hg38-release232.tsv.gz",
                format=gs.data_format(
                    parse=gs.parse(
                        symbol="string",
                        chrom="string",
                        start="integer",
                        length="integer",
                        strand="string",
                        score="integer",
                        exons="string",
                    )
                ),
            ),
        )
        .encode(
            y=gs.Y("_lane:O")
            .scale(
                type="index",
                align=0,
                paddingInner=0.4,
                paddingOuter=0.2,
                domain=[0, 3],
                reverse=True,
                zoom=False,
            )
            .axis(None)
        )
        .transform_linearize_genomic_coordinate(
            chrom="chrom", pos="start", as_="_start"
        )
        .transform_formula(expr=gs.datum._start + gs.datum.length, as_="_end")
        .transform_formula(expr=gs.datum._start + gs.datum.length / 2, as_="_centroid")
        .transform_collect(sort=gs.compare(field=["_start"]))
        .transform_pileup(
            start="_start",
            end="_end",
            as_="_lane",
            preference="strand",
            preferredOrder=["-", "+"],
        )
        .transform_filter(gs.datum._lane < 3)
    )


def _build_genome_browser() -> gs.Chart:
    """Compose the four independently authored tracks."""
    return (
        gs.vconcat(
            _build_cytoband_track().properties(
                height=30,
                axes=gs.axes(x=gs.GenomeAxis(orient="top", title=None)),
            ),
            _build_six_frame_translation_track(),
            _build_bam_alignment_track(),
            _build_refseq_track(),
        )
        .properties(
            assembly="hg38",
            description=(
                "Python-authored cytoband, six-frame translation, BAM alignment, "
                "and RefSeq tracks composed into a shared-locus genome browser."
            ),
            scales=gs.scales(
                x=gs.Scale(
                    domain=[
                        {"chrom": "chr20", "pos": 10006452},
                        {"chrom": "chr20", "pos": 10006533},
                    ]
                )
            ),
        )
        .resolve_scale(x="shared", y="independent")
        .resolve_axis(x="shared", y="independent")
        .configure_view(stroke="lightgray")
        .configure_legend(disable=True)
    )


chart = _build_genome_browser()
