"""Indexed FASTA six-frame translation.

The visible hg38 reference sequence is translated in all three reading frames
on both strands and kept aligned with a base-level reference track.
"""

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "order": 18,
    "height": 170,
    "max_width": 980,
}
# Choose the reading direction for each translation track.
strand = gs.param("strand", value="forward")
WIDTH = gs.Expression("width")

# Match each DNA base to its partner on the opposite strand.
COMPLEMENTS = [
    {"base": base, "complement": complement}
    for base, complement in zip("ACGTN", "TGCAN", strict=True)
]

# Translate each three-letter codon using the standard genetic code.
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
# Give start and stop codons their own colors.
GENETIC_CODE = [
    {
        "codon": codon,
        "aminoAcid": amino_acid,
        "kind": (
            "start" if codon == "ATG" else "stop" if amino_acid == "STOP" else "other"
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

# Draw the reference DNA as colored tiles with letters on top.
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

# Draw one arrow per codon, pointing in its reading direction.
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
        direction=gs.value(strand),
        color=gs.Color("kind:N")
        .scale(
            domain=["start", "stop", "other", "?"],
            range=["#40B050", "#F06060", "#F8F8F8", "#E0E0E0"],
        )
        .legend(None),
    )
    .properties(name="amino-acids")
)

# Label each codon with its translated amino acid.
amino_acid_labels = (
    gs.Chart()
    .mark_text(size=12, paddingX=1.5, tooltip=None)
    .encode(color=gs.value("black"), text=gs.Text("aminoAcid"))
    .properties(name="amino-acid-labels")
)

# Build one translation track that works in either reading direction.
translation_template = (
    (amino_acids + amino_acid_labels)
    .add_params(strand)
    .transform_formula(
        expr=gs.expr.if_(
            strand == "reverse",
            gs.datum.complement2 + gs.datum.complement1 + gs.datum.complement,
            gs.datum.base + gs.datum.base1 + gs.datum.base2,
        ),
        as_="codon",
    )
    .transform_lookup(from_={"name": "geneticCode"}, key="codon", default="?")
    .transform_formula(expr=strand + " " + (gs.datum.pos % 3), as_="lane")
)

# Reuse the track for both strands, with three reading frames on each.
translation = (
    (
        gs.import_view(
            template="amino-acid-translation",
            name="forward-translation",
            params={"strand": "forward"},
        )
        + gs.import_view(
            template="amino-acid-translation",
            name="reverse-translation",
            params={"strand": "reverse"},
        )
    )
    .properties(
        name="translation",
        height=gs.step(17),
        templates={"amino-acid-translation": translation_template},
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
    # Gather the next two bases to form each three-letter codon.
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

# Load the visible DNA and put its six translations directly below it.
chart = (
    (reference & translation)
    .properties(
        assembly="hg38",
        name="indexed-fasta-six-frame-translation",
        description=(
            "The visible hg38 reference is translated in three forward and "
            "three reverse reading frames."
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr7", "pos": 20395929},
                    {"chrom": "chr7", "pos": 20395976},
                ]
            )
        ),
        datasets={
            "nucleotideComplements": COMPLEMENTS,
            "geneticCode": GENETIC_CODE,
        },
        data=gs.lazy.indexed_fasta("https://data.genomespy.app/genomes/hg38/hg38.fa"),
        spacing=5,
    )
    # Give each base its own row and genomic position.
    .transform_flatten_sequence(field="sequence", as_=["rawPos", "base"])
    .transform_formula(expr=gs.datum.start + gs.datum.rawPos, as_="pos")
    .resolve_axis(x="shared")
)
