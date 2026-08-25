:::{admonition} Data use and provenance
:class: note

The packaged mutation and annotation inputs are the TCGA LAML example files
distributed with [maftools](https://github.com/PoisonAlien/maftools/tree/015a4cf8c69ba89a55a3fdcea911421509e9a198/inst/extdata),
which is MIT-licensed. TCGA data are open-access. During data loading, the
package excludes silent and non-coding calls, selects the ten most recurrently
altered genes, orders samples by alteration pattern, and collapses repeated
sample-gene calls to `Multi_Hit`. GenomeSpy then renders the prepared tables.
:::
