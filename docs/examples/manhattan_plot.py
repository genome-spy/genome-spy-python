"""Manhattan plot.

Genome-wide association hits on a locus-aware chromosome axis. Alternating
chromosome colors separate the blocks, dashed rules mark significance
thresholds, and the strongest peaks are outlined for emphasis.
"""

import numpy as np
import pandas as pd

import genome_spy as gs
from genome_spy.datasets import load_dataset
from genome_spy.schema import GenomeAxis, Scale

META = {
    "category": "Association plots",
    "tags": ("locus", "layer", "real-data"),
    "order": 10,
    "height": 340,
}

GENOME_WIDE_P = 5e-8
SUGGESTIVE_P = 1e-5


def hapmap_gwas() -> pd.DataFrame:
    """Load the HapMap GWAS table and derive the columns the plot encodes."""
    data = load_dataset("hapmap_gwas", as_format="dataframe")
    data = data[data["P"] > 0].copy()
    # GenomeSpy's assemblies use bare chromosome names (as in its ASCAT data);
    # HapMap encodes chromosome 23 as X.
    data["chrom"] = np.where(data["CHR"] == 23, "X", data["CHR"].astype(str))
    data["neglog"] = -np.log10(data["P"])
    data["chrom_group"] = np.where(data["CHR"] % 2 == 0, "even", "odd")
    return data


data = hapmap_gwas()
top_hits = data.nsmallest(8, "P")

# Explicit y-domain so the shared scale spans the points, not the tiny
# threshold-rule datasets (which would otherwise clip the peaks).
Y_DOMAIN = [0.0, float(np.ceil(data["neglog"].max()))]

# --- Visualization -------------------------------------------------------------

chrom_colors = Scale().range(["#5b8fd6", "#8f98a3"])

axis = (
    GenomeAxis()
    .title("Genomic position")
    .chromGrid(True)
    .chromGridOpacity(0.14)
    .chromGridFillEven("#f4f6fb")
    .chromGridFillOdd("#ffffff")
    .chromLabels(True)
    .chromLabelFontSize(11)
    .chromTicks(True)
    .chromTickSize(10)
    .labelFontSize(10)
    .grid(False)
)

points = (
    gs.Chart(data)
    .mark_point(size=20, filled=True, opacity=0.82)
    .encode(
        x=gs.Locus("chrom", "BP").scale(assembly="hg38").axis(axis),
        y=gs.Y("neglog:Q").scale(reverse=False, domain=Y_DOMAIN).title("−log10 p"),
        color=gs.Color("chrom_group:N")
        .scale(chrom_colors)
        .legend(title="Chromosome group"),
    )
)

genome_wide_rule = (
    gs.Chart([{"threshold": -np.log10(GENOME_WIDE_P)}])
    .mark_rule(strokeDash=[6, 4], size=1.4, color="#c53b2c")
    .encode(
        y=gs.Y("threshold:Q").scale(reverse=False, domain=Y_DOMAIN).title("−log10 p")
    )
)

suggestive_rule = (
    gs.Chart([{"threshold": -np.log10(SUGGESTIVE_P)}])
    .mark_rule(strokeDash=[2, 4], size=1.2, color="#d48b31")
    .encode(
        y=gs.Y("threshold:Q").scale(reverse=False, domain=Y_DOMAIN).title("−log10 p")
    )
)

highlight_points = (
    gs.Chart(top_hits)
    .mark_point(size=48, filled=True, stroke="black", strokeWidth=0.5)
    .encode(
        x=gs.Locus("chrom", "BP").scale(assembly="hg38"),
        y=gs.Y("neglog:Q").scale(reverse=False, domain=Y_DOMAIN).title("−log10 p"),
        color=gs.Color("chrom_group:N").scale(chrom_colors).legend(None),
    )
)

chart = (genome_wide_rule + suggestive_rule + points + highlight_points).properties(
    title="HapMap genome-wide association scan",
    description="A GenomeSpy-native Manhattan plot with a locus-aware chromosome axis and significance rules.",
)
