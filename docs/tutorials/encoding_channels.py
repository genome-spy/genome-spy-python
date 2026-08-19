"""Single-source chart objects used by the Encodings and Channels guide."""

# encoding-channels-data-start
import genome_spy as gs


measurements = [
    {"sample": "A", "stage": "low", "score": 2.1, "amount": 18, "confidence": 0.55},
    {"sample": "A", "stage": "medium", "score": 3.4, "amount": 32, "confidence": 0.82},
    {"sample": "A", "stage": "high", "score": 4.2, "amount": 24, "confidence": 0.74},
    {"sample": "B", "stage": "low", "score": 1.7, "amount": 22, "confidence": 0.61},
    {"sample": "B", "stage": "medium", "score": 2.8, "amount": 15, "confidence": 0.48},
    {"sample": "B", "stage": "high", "score": 3.6, "amount": 36, "confidence": 0.91},
]
# encoding-channels-data-end


# encoding-channels-syntax-start
shorthand_chart = (
    gs.Chart(measurements)
    .mark_point()
    .encode(
        x="score:Q",
        y="stage:O",
        color="sample:N",
    )
)

explicit_chart = (
    gs.Chart(measurements)
    .mark_point()
    .encode(
        x=gs.X("score", type="quantitative"),
        y=gs.Y("stage", type="ordinal"),
        color=gs.Color("sample", type="nominal"),
    )
)
# encoding-channels-syntax-end


# encoding-channels-visual-start
channel_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True, stroke="white", strokeWidth=1)
    .encode(
        x=gs.X("score:Q").scale(zero=False).title("Score"),
        y=gs.Y("stage:O").title("Stage"),
        color=gs.Color("sample:N").legend(title="Sample"),
        shape="sample:N",
        size=gs.Size("amount:Q").legend(title="Amount"),
        opacity=gs.Opacity("confidence:Q").scale(range=[0.35, 1]),
        tooltip=[
            gs.Tooltip("sample:N").title("Sample"),
            gs.Tooltip("score:Q").title("Score"),
            gs.Tooltip("confidence:Q").format(".0%").title("Confidence"),
        ],
    )
    .properties(title="Several channels can describe each row")
)
# encoding-channels-visual-end


# encoding-channels-index-start
sequence = [
    {"position": 0, "base": "A"},
    {"position": 1, "base": "C"},
    {"position": 2, "base": "G"},
    {"position": 3, "base": "T"},
    {"position": 4, "base": "G"},
    {"position": 5, "base": "A"},
]

index_chart = (
    gs.Chart(sequence)
    .mark_text(size=22)
    .encode(
        x=gs.X("position:I").title("Zero-based index"),
        y=gs.value(0.5),
        text="base:N",
        color=gs.Color("base:N").legend(None),
    )
    .properties(title="Index values occupy regular slots")
)
# encoding-channels-index-end


# encoding-channels-locus-start
features = [
    {"chrom": "chr17", "start": 43_044_000, "end": 43_050_000, "kind": "A"},
    {"chrom": "chr17", "start": 43_057_000, "end": 43_061_000, "kind": "B"},
    {"chrom": "chr17", "start": 43_068_000, "end": 43_075_000, "kind": "A"},
]

locus_chart = (
    gs.Chart(features)
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start").scale(
            domain=[
                {"chrom": "chr17", "pos": 43_040_000},
                {"chrom": "chr17", "pos": 43_080_000},
            ]
        ),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("kind:N").title("Feature kind"),
        color=gs.Color("kind:N").legend(None),
    )
    .properties(assembly="hg38", title="Locus values follow the genome")
)
# encoding-channels-locus-end


# encoding-channels-definitions-start
definition_chart = (
    gs.Chart(measurements)
    .mark_point(filled=True)
    .encode(
        x=gs.X("score:Q").scale(zero=False),
        y=gs.datum(0, type="quantitative"),
        color=gs.value("#4c78a8"),
        size=gs.Size(
            gs.expr("datum.amount * datum.confidence"),
            type="quantitative",
        ).legend(None),
    )
    .properties(title="Field, datum, value, and expression definitions")
)
# encoding-channels-definitions-end


CHARTS = {
    "shorthand_chart": shorthand_chart,
    "explicit_chart": explicit_chart,
    "channel_chart": channel_chart,
    "index_chart": index_chart,
    "locus_chart": locus_chart,
    "definition_chart": definition_chart,
}
