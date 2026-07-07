"""Manhattan plot.

A GenomeSpy-native genome-wide association scan. Variants are placed on a
locus-aware chromosome axis, alternating chromosome colors separate the blocks,
and dashed rules mark the genome-wide and suggestive significance thresholds.
Pan and zoom the plot to inspect individual peaks.
"""

import math

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.schema import GenomeAxis, Scale

META = {
    "category": "GWAS",
    "tags": ("locus", "layer", "thresholds"),
    "order": 10,
}

GENOME_WIDE_P = 5e-8
SUGGESTIVE_P = 1e-5


def synthetic_gwas(seed: int = 7) -> pd.DataFrame:
    """Deterministic synthetic GWAS summary statistics for chromosomes 1–22.

    Returns one row per variant with ``chrom``/``pos`` coordinates, a ``neglog``
    column (−log10 p), and an odd/even ``chrom_group`` used to color blocks. A
    handful of variants are boosted into genome-wide significance so the plot has
    clear peaks.
    """
    rng = np.random.default_rng(seed)
    chrom_sizes = {chrom: int(900 - chrom * 25) for chrom in range(1, 23)}

    frames = [
        pd.DataFrame(
            {
                "chrom": f"chr{chrom}",
                "chrom_index": chrom,
                "pos": np.sort(rng.integers(1, 250_000_000, size)),
                "pval": rng.uniform(0, 1, size),
            }
        )
        for chrom, size in chrom_sizes.items()
    ]
    data = pd.concat(frames, ignore_index=True)

    hits = rng.choice(len(data), 12, replace=False)
    data.loc[hits, "pval"] = 10 ** (-rng.uniform(8, 30, 12))
    data["neglog"] = -np.log10(data["pval"].clip(lower=1e-300))
    data["chrom_group"] = np.where(data["chrom_index"] % 2 == 0, "even", "odd")
    return data


data = synthetic_gwas()
top_hits = data.nsmallest(5, "pval")

# --- Visualization -------------------------------------------------------------

chrom_colors = Scale(range=["#5b8fd6", "#8f98a3"])

axis = GenomeAxis(
    title="Genomic position",
    chromGrid=True,
    chromGridOpacity=0.14,
    chromGridFillEven="#f4f6fb",
    chromGridFillOdd="#ffffff",
    chromLabels=True,
    chromLabelFontSize=11,
    chromTicks=True,
    chromTickSize=10,
    labelFontSize=10,
    grid=False,
)

points = (
    gs.Chart(data)
    .mark_point(size=20, filled=True, opacity=0.82)
    .encode(
        x=gs.Locus("chrom", "pos", scale={"assembly": "hg38"}, axis=axis),
        y=gs.Y("neglog:Q").scale(reverse=False, zero=True).title("−log10 p"),
        color=gs.Color("chrom_group:N")
        .scale(chrom_colors)
        .legend(title="Chromosome group"),
    )
)

genome_wide_rule = (
    gs.Chart([{"threshold": -math.log10(GENOME_WIDE_P)}])
    .mark_rule(strokeDash=[6, 4], size=1.4, color="#c53b2c")
    .encode(y=gs.Y("threshold:Q").scale(reverse=False))
)

suggestive_rule = (
    gs.Chart([{"threshold": -math.log10(SUGGESTIVE_P)}])
    .mark_rule(strokeDash=[2, 4], size=1.2, color="#d48b31")
    .encode(y=gs.Y("threshold:Q").scale(reverse=False))
)

highlight_points = (
    gs.Chart(top_hits)
    .mark_point(size=48, filled=True, stroke="black", strokeWidth=0.5)
    .encode(
        x=gs.Locus("chrom", "pos", scale={"assembly": "hg38"}),
        y=gs.Y("neglog:Q").scale(reverse=False),
        color=gs.Color("chrom_group:N").scale(chrom_colors).legend(None),
    )
)

chart = (genome_wide_rule + suggestive_rule + points + highlight_points).properties(
    width=500,
    height=280,
    title="Synthetic height GWAS across the genome",
    description="A GenomeSpy-native Manhattan plot with a locus-aware chromosome axis and significance rules.",
)
