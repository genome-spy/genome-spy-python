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

# Use a fixed version of the hosted examples so their contents stay the same.
EXAMPLE_ROOT = (
    "https://raw.githubusercontent.com/genome-spy/genome-spy/"
    "d2e9bd71/examples/docs/examples/genomic-data"
)

# Load four ready-made charts from JSON files and stack them vertically.
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
        # Start all four tracks at the same region on chromosome 20.
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
    # Show one position axis for the whole browser.
    .resolve_axis(x="shared")
    .configure_legend(disable=True)
)
