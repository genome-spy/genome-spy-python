## What to notice

Each column is a patient and each gene row shows their alterations. Of the 200
patients, 159 have an alteration in a displayed gene. Outlines group related
genes; a dark cell in the summary row means at least one gene in that group is
altered. Grey dots flag variants with alternate allele C.

The surrounding tracks add context:

- Top bars show alteration counts, including copy-number changes—not mutations
  per megabase, despite the maftools **TMB** label.
- Left bars show mean variant allele frequency; right bars show −log10 MutSig
  q-values. Percentages show how many of the 200 patients are affected.
- Lower tracks show FAB classification, follow-up time, and SNV substitution types.

Hover for gene and patient details. Zoom horizontally to explore individual
patients; the tracks stay aligned and the grey dots grow for easier viewing.

:::{admonition} Data use and provenance
:class: note

Adapted from maftools'
[Combining everything example](https://bioconductor.org/packages/devel/bioc/vignettes/maftools/inst/doc/oncoplots.html#08_Combining_everything)
using its prepared [TCGA LAML data](https://github.com/PoisonAlien/maftools/tree/015a4cf8c69ba89a55a3fdcea911421509e9a198/inst/extdata).
`load_data()` loads prepared tables with joined
clinical and alteration data, sorted patients, and calculated summaries for
18 genes and five pathways. Substitution fractions include synonymous SNVs.
Empty matrix cells mean no recorded alteration, not confirmed wild type;
missing measurements remain blank.
:::
