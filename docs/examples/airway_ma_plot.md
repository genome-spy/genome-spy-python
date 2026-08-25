:::{admonition} Data use and provenance
:class: note

Counts come from the Himes et al. airway smooth-muscle RNA-seq experiment
([GEO GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778)),
distributed through the LGPL-licensed Bioconductor
[`airway` package](https://bioconductor.org/packages/airway/). During data
loading, the package filters genes, computes paired treated-versus-control
log-count tests and Benjamini-Hochberg adjusted p-values, and selects the genes
to plot. GenomeSpy then renders the prepared table.
:::
