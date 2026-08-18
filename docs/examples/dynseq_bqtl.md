:::{admonition} Data use and provenance
:class: note

The visualization loads the original `chip_imp_ref.bw` and `chip_imp_alt.bw`
directly from the pinned [dynseq-paper source revision](https://github.com/kundajelab/dynseq-paper/tree/febc9180d72e92302d35c549002e0d56c79c536e/SPI1_bQTL/bigwigs).
The score values and missing-value gaps are not modified. The Zenodo source
data are distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Source attribution: [dynseq tracks data, Zenodo record 6582100](https://doi.org/10.5281/zenodo.6582100);
Nair et al., [The dynseq browser track shows context-specific features at
nucleotide resolution](https://doi.org/10.1038/s41588-022-01194-w), *Nature
Genetics* 54, 1581–1583 (2022); and Tehranchi et al., [Pooled ChIP-Seq Links
Variation in Transcription Factor Binding to Complex Disease Risk](https://doi.org/10.1016/j.cell.2016.03.041),
*Cell* 165, 730–741 (2016).
:::

## What to notice

Reference and alternate SPI1 contribution scores use the same genomic scale.
At base resolution, signed sequence-logo letters show the reference bases and
make the direction and magnitude of each contribution visible.

## Python implementation

A named template defines the shared baseline, BigWig lookup, and indexed-FASTA
sequence-logo layers. Two imports instantiate it with reference and alternate
allele parameters, which select the corresponding BigWig source and title.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/dynseq-spi1-bqtl/)
for the biological context and original grammar explanation.
