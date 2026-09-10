Use the sliders to choose the minimum absolute fold change and p-value evidence
for calling a gene changed. The fold-change guides move, and genes passing both
cutoffs are recolored immediately. The p-value cutoff has no line because an MA
plot has no p-value axis.

:::{admonition} Data use and provenance
:class: note

Counts come from the Himes et al. airway smooth-muscle RNA-seq experiment
([GEO GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778)),
reprocessed with kallisto and tximport `lengthScaledTPM` for Stephen Turner's
[Bioconnector workshops](https://github.com/bioconnector/workshops/blob/d0c4d0cca5f21dc2c6e12912dc09d5e279e706ce/data/airway_scaledcounts.csv).
The exact workshop CSVs are bundled; the workshop declares CC BY-NC-SA 4.0,
with attribution and license details in the
<a href="../THIRD_PARTY_NOTICES.md">third-party notices</a>. During data
loading, the package filters genes, computes paired treated-versus-control
log-count tests and Benjamini-Hochberg adjusted p-values, and selects the genes
to plot. GenomeSpy then renders the prepared table and applies the interactive
classification in the browser.
:::
