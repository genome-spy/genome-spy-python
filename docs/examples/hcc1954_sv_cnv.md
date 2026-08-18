:::{admonition} Data use and provenance
:class: note

The source data are publicly released CASTLE supplementary data on Zenodo. The
selected Wakhan source record, [17780982](https://doi.org/10.5281/zenodo.17780982),
and the compact Severus callset, [18989691](https://doi.org/10.5281/zenodo.18989691),
are licensed CC BY 4.0. The example uses Wakhan's `4.57_0.99_0.9` rank-1
solution (DNA purity 1.00, cell purity 0.99, ploidy 4.57, confidence 0.90).

Source attribution: Keskus et al., [Severus detects somatic structural
variation and complex rearrangements in cancer genomes using long-read
sequencing](https://doi.org/10.1038/s41587-025-02618-8), *Nature Biotechnology*
44, 247–257 (2026); Ahmad et al., [Wakhan: reconstruction of chromosome-scale
copy number profiles of tumor genomes with long-read sequencing](https://doi.org/10.64898/2025.12.11.25342098);
and Akdemir et al., [Disruption of chromatin folding domains by somatic genomic
rearrangements in human cancer](https://doi.org/10.1038/s41588-019-0564-y).
:::

## What to notice

Structural-variant links align with total copy-number segments normalized by
the sample's estimated ploidy. Hovering a rearrangement emphasizes its link
between the two breakpoints.

## Python implementation

The VCF pipeline normalizes paired breakends and filters duplicate link rows. A
point-selection parameter changes the hovered link's opacity and width, while
the vertically concatenated tracks share their locus scale.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/hcc1954-sv-cnv/)
for source preparation and a detailed reading guide.
