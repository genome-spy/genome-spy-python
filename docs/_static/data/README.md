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

## `oncoprint_dataset3.json`

- **What it is:** sample alteration records (`sample`, `gene`, `alteration`,
  `type`) used by the OncoPrint example.
- **Source:** byte-exact copy of
  [`plotly/datasets/Dash_Bio/Chromosomal/oncoprint_dataset3.json`](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/oncoprint_dataset3.json),
  first added as a Dash Bio sample input in
  [commit `20088fe`](https://github.com/plotly/datasets/commit/20088fe2168789d0d5f5ba9820df9bd46f73231f).
- **SHA-256:** `e07aa6ae9cf4f5f3a9f331d9979855ccf33bc47ed1bb2f4b871939b47c2a09ef`.
- **Provenance note:** Plotly documents this as input in cBioPortal format, but
  the repository does not identify a deeper cBioPortal or TCGA source for this
  particular sample file.
- **License:** MIT (`plotly/datasets`, © Plotly Technologies Inc.).

## `tcga.tsv`

- **What it is:** the wide TCGA LUAD table used by pyoncoprint's example
  notebook, containing alteration, mutation-spectrum, MSI, stage, expression,
  methylation, and microbiome tracks for 507 samples.
- **Source:** the byte-exact
  `example_data/tcga.tsv` file from
  [`pnucolab/pyoncoprint`](https://github.com/pnucolab/pyoncoprint), commit
  `31e6d6de78b64070a9c6c582ce3ef571b14e4c71`.
- **SHA-256:** `39a90fc1f50ebcd113c37fd03894fb41b17dca4d6014f7efcf0e3f234c957742`.
- **License:** MIT (`pyoncoprint`). TCGA data is open-access.

## `tcga_laml.maf.gz` / `tcga_laml_annot.tsv`

- **What they are:** the exact TCGA LAML mutation and clinical-annotation files
  used by `maftools::oncoplot()` and `maftools::lollipopPlot()` examples.
- **Source:** byte-exact files from `inst/extdata/` in the
  [`maftools`](https://github.com/PoisonAlien/maftools) package and used by its
  examples, commit `015a4cf8c69ba89a55a3fdcea911421509e9a198`.
- **SHA-256:** `d102b071a052265b6f8ad7947bad1d58d3e3036fd17d6b274f7ea09a376cd6a0`
  and `7033030d52868e9a0f35ffd78f45a9d7a126c2edef90cf9e74e4f5d78990a710`.
- **Preparation:** for the oncoplot, silent/non-coding calls are excluded; the
  top 10 genes are
  ordered by number of altered samples to match the canonical LAML oncoplot
  ordering; samples were ordered by the presence pattern across those genes to
  cluster co-occurring mutations; sample-gene pairs with multiple hits were
  collapsed into a `Multi_Hit` display class for the matrix.
- **License:** MIT (`maftools`, © Anand Mayakonda). TCGA data is open-access.

The DNMT3A lollipop is prepared from the same MAF at load time. Amino-acid
positions are parsed from `Protein_Change`, mutations are aggregated by site,
and the small protein-domain model is maintained in Python visualization
metadata.

## `brca.maf.gz`

- **What it is:** the exact single-sample TCGA BRCA MAF used by maftools'
  rainfall-plot example.
- **Source:** byte-exact `inst/extdata/brca.maf.gz` from
  [`maftools`](https://github.com/PoisonAlien/maftools), commit
  `015a4cf8c69ba89a55a3fdcea911421509e9a198`.
- **SHA-256:** `61d5355e960bd480bec4f245b8f096e2333408659ced0d196e42b0e38de3d724`.
- **Preparation:** inter-event distances, pyrimidine-oriented substitution
  classes, and six-mutation kataegis windows are computed at load time.
- **License:** MIT (`maftools`, © Anand Mayakonda). TCGA data is open-access.

## `pik3ca_mutations.json`

- **What it is:** structured mutation and protein-domain input for the NeedlePlot
  example.
- **Source:** byte-exact copy of
  [`plotly/datasets/Dash_Bio/Genetic/needle_PIK3CA.json`](https://github.com/plotly/datasets/blob/master/Dash_Bio/Genetic/needle_PIK3CA.json),
  added in [commit `1f6923b`](https://github.com/plotly/datasets/commit/1f6923b9c30c19ed825d3dad96754d0cb0f76708).
- **SHA-256:** `4f36df9ad960c1429827522bbd4fce0cb47520d14a5c642abe8a55969f177aec`.
- **Provenance note:** the Plotly file is the documented Dash Bio sample input;
  its repository history does not identify a deeper biological source.
- **License:** MIT (`plotly/datasets`, © Plotly Technologies Inc.).

## `mutation_impact_reference.json`

- **What it is:** a small deterministic synthetic reference window used by the
  mutation-impact notebook.
- **Source:** authored in this repository from the notebook's original
  hard-coded values; it is not downloaded from an external data package.
- **License:** project source code/data.

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
