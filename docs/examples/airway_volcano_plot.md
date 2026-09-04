The sliders control the minimum absolute fold change and p-value evidence.
Genes that pass both cutoffs become red or blue, and the guide lines move to
show the active boundaries.

:::{admonition} Data use and provenance
:class: note

Counts come from the Himes et al. airway smooth-muscle RNA-seq experiment
([GEO GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778)),
distributed through the LGPL-licensed Bioconductor
[`airway` package](https://bioconductor.org/packages/airway/). During data
loading, the package filters genes, computes paired treated-versus-control
log-count tests and Benjamini-Hochberg adjusted p-values, and selects the genes
to plot. GenomeSpy then renders the prepared table and applies the interactive
classification in the browser.
:::
