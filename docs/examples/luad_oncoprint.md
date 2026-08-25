:::{admonition} Data use and provenance
:class: note

The packaged input is the TCGA LUAD example table from
[pyoncoprint](https://github.com/pnucolab/pyoncoprint/blob/31e6d6de78b64070a9c6c582ce3ef571b14e4c71/example_data/tcga.tsv),
which is MIT-licensed. TCGA data are open-access. During data loading, the
package reshapes the wide table, expands alteration labels, and orders genes and
samples by recurrence. GenomeSpy then renders the prepared alteration, clinical,
and quantitative tracks.
:::
