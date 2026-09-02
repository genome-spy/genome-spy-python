"""Composing a genome browser.

Independent cytoband, six-frame translation, BAM alignment, and RefSeq views
are imported by URL and aligned under a parent-owned genomic scale and axis.
"""

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 38,
    "height": 650,
    "max_width": 980,
}

# Pin imported views to the same upstream release as the wrapper's schema and
# browser bundle. Absolute URLs also make imports work in docs, notebooks, and
# the standalone thumbnail renderer without depending on a deployment base URL.
EXAMPLE_ROOT = (
    "https://raw.githubusercontent.com/genome-spy/genome-spy/"
    "d2e9bd71/examples/docs/examples/genomic-data"
)

chart = (
    gs.vconcat(
        gs.import_view(url=f"{EXAMPLE_ROOT}/cytobands.json"),
        gs.import_view(url=f"{EXAMPLE_ROOT}/indexed-fasta-six-frame-translation.json"),
        gs.import_view(url=f"{EXAMPLE_ROOT}/bam-read-alignments.json"),
        gs.import_view(url=f"{EXAMPLE_ROOT}/scored-refSeq-genes.json"),
    )
    .properties(
        assembly="hg38",
        description=(
            "Imported cytoband, six-frame translation, BAM alignment, and "
            "RefSeq views composed into a shared-locus genome browser."
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr20", "pos": 10006452},
                    {"chrom": "chr20", "pos": 10006533},
                ]
            )
        ),
        axes=gs.axes(x=gs.GenomeAxis(orient="top", title=None)),
    )
    .resolve_axis(x="shared")
    .configure_legend(disable=True)
)
