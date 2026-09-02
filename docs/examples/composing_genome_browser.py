"""Composing a genome browser.

Independent cytoband, six-frame translation, BAM alignment, and RefSeq tracks
are built with the Python API and aligned under a parent-owned genomic scale.
"""

import genome_spy as gs
from docs.examples.bam_read_alignments import build_bam_alignment_track
from docs.examples.cytobands import build_cytoband_track
from docs.examples.refseq_scored_genes import build_refseq_track
from docs.examples.six_frame_translation import build_six_frame_translation_track

META = {
    "category": "Genome browser tracks",
    "order": 38,
    "height": 650,
    "max_width": 980,
}

# Each builder owns its track dataflow. The parent owns the assembly and shared
# locus domain; the first track supplies the single top axis for that scale.
chart = (
    gs.vconcat(
        build_cytoband_track().properties(
            height=30,
            axes=gs.axes(x=gs.GenomeAxis(orient="top", title=None)),
        ),
        build_six_frame_translation_track(),
        build_bam_alignment_track(viewport_height=300),
        build_refseq_track(),
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
