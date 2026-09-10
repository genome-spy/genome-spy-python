:::{admonition} Data use and provenance
:class: note

The packaged input is the TCGA LUAD example table from
[pyoncoprint](https://github.com/pnucolab/pyoncoprint/blob/31e6d6de78b64070a9c6c582ce3ef571b14e4c71/example_data/tcga.tsv),
a cBioPortal export of TCGA LUAD. See the
<a href="../THIRD_PARTY_NOTICES.md">third-party notices</a> for
cBioPortal's default ODbL policy and this study's Broad GDAC notice. The
Dicipivirus track comes from Poore et al. (2020),
[retracted in 2024](https://doi.org/10.1038/s41586-024-07656-x), and is not a
validated biological finding. During data loading, the
package reshapes the wide table, expands alteration labels, and orders genes and
samples by recurrence. GenomeSpy then renders the prepared alteration, clinical,
and quantitative tracks.
:::
