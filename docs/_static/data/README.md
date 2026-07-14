# Vendored gallery datasets

Third-party data bundled for the documentation gallery. Each entry lists its
source and license.

## `hapmap_gwas.csv`

- **What it is:** a subset of HapMap SNPs (real chromosome, position, rs-ID, and
  nearest-gene annotations) with **simulated** GWAS association statistics
  (`P`, `ZSCORE`, `EFFECTSIZE`). Used by the Manhattan, volcano, and QQ examples.
- **Immediate source:** [`plotly/datasets`](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/manhattan_data.csv)
  (`Dash_Bio/Chromosomal/manhattan_data.csv`), as used by Plotly's Dash Bio
  Manhattan and volcano examples.
- **Upstream origin:** the `HapMap` dataset from the
  [`manhattanly`](https://github.com/cran/manhattanly) R package by
  Sahir Bhatnagar, documented as "Subset of HapMap data with simulated GWAS
  results."
- **License:** MIT. Both `plotly/datasets` (© Plotly Technologies Inc.) and
  `manhattanly` (© Sahir Bhatnagar) are MIT-licensed, which permits
  redistribution with attribution. This notice satisfies that attribution
  requirement.
- **Note:** the genomic coordinates and gene names are real HapMap data; the
  association p-values and effect sizes are simulated, so results are for
  visualization demonstration only, not real biological findings.

## `tcga_oncoprint.json`

- **What it is:** real somatic alterations (sample, gene, alteration, type) in
  BRCA1/BRCA2 across a set of TCGA tumour samples. Used by the oncoprint example.
- **Source:** [`plotly/datasets`](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/oncoprint_dataset3.json)
  (`Dash_Bio/Chromosomal/oncoprint_dataset3.json`), from Plotly's Dash Bio
  OncoPrint example; upstream cBioPortal / TCGA.
- **License:** MIT (`plotly/datasets`, © Plotly Technologies Inc.). TCGA data is
  open-access.

## `tcga_laml_oncoprint.json`

- **What it is:** a curated TCGA LAML oncoplot payload modeled after
  `maftools::oncoplot(maf = laml, top = 10)`, with all 193 samples, the top 10
  recurrently altered genes, stacked per-sample mutation-burden segments, a
  collapsed mutation matrix, percentage labels, and right-side per-gene sample
  counts. Used by the flagship oncoprint example.
- **Source:** derived from `maftools` extdata files
  `tcga_laml.maf.gz` and `tcga_laml_annot.tsv`, distributed in the
  [`maftools`](https://github.com/PoisonAlien/maftools) package and used by its
  oncoplot examples.
- **Derivation:** silent/non-coding calls were excluded; the top 10 genes were
  ordered by number of altered samples to match the canonical LAML oncoplot
  ordering; samples were ordered by the presence pattern across those genes to
  cluster co-occurring mutations; sample-gene pairs with multiple hits were
  collapsed into a `Multi_Hit` display class for the matrix.
- **License:** MIT (`maftools`, © Anand Mayakonda). TCGA data is open-access.

## `dnmt3a_lollipop.json`

- **What it is:** a curated DNMT3A lollipop payload derived from the TCGA LAML
  MAF used in `maftools::lollipopPlot()`, with amino-acid positions, per-site
  mutation counts, dominant mutation classes, the R882 hotspot label, and a
  small set of DNMT3A domain annotations for the gallery example.
- **Source:** derived from `maftools` extdata file `tcga_laml.maf.gz`,
  distributed in the [`maftools`](https://github.com/PoisonAlien/maftools)
  package and used by its lollipop examples.
- **Derivation:** amino-acid positions were parsed from the `Protein_Change`
  column for DNMT3A calls; per-position counts were aggregated across samples;
  the displayed mutation class per site is the most frequent class at that
  position; the reported mutation rate is the fraction of LAML samples with a
  parsed DNMT3A protein change in the bundled MAF.
- **License:** MIT (`maftools`, © Anand Mayakonda). TCGA data is open-access.

## `pik3ca_mutations.json`

- **What it is:** real UniProt sequence features and functional domains of the
  PIK3CA protein (positions, feature types, domain coordinates). Used by the
  lollipop example.
- **Source:** [`plotly/datasets`](https://github.com/plotly/datasets/blob/master/Dash_Bio/Genetic/needle_PIK3CA.json)
  (`Dash_Bio/Genetic/needle_PIK3CA.json`), from Plotly's Dash Bio NeedlePlot
  example; upstream UniProt.
- **License:** MIT (`plotly/datasets`, © Plotly Technologies Inc.). UniProt data
  is available under CC-BY 4.0.

## `airway_scaledcounts.csv` / `airway_metadata.csv`

- **What it is:** real bulk RNA-seq gene counts for the classic `airway`
  teaching dataset (airway smooth muscle cells, dexamethasone-treated vs.
  control, 4 cell lines) plus per-sample metadata (treatment, cell line,
  GEO accession). Used by the airway differential-expression gallery example.
- **Origin:** Himes et al. 2014, GEO accession
  [GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778);
  distributed as the Bioconductor
  [`airway`](https://bioconductor.org/packages/release/data/experiment/html/airway.html)
  experiment-data package, a standard RNA-seq teaching dataset.
- **License:** GEO/Bioconductor experiment data; treat as open for research and
  teaching use. Re-verify the exact package license before shipping a derived
  figure at release time — this file was added by the maintainer directly and
  its license has not yet been independently re-confirmed in this session.
