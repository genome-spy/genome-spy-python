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
  GEO accession). Not yet used by a gallery example.
- **Origin:** Himes et al. 2014, GEO accession
  [GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778);
  distributed as the Bioconductor
  [`airway`](https://bioconductor.org/packages/release/data/experiment/html/airway.html)
  experiment-data package, a standard RNA-seq teaching dataset.
- **License:** GEO/Bioconductor experiment data; treat as open for research and
  teaching use. Re-verify the exact package license before shipping a derived
  figure at release time — this file was added by the maintainer directly and
  its license has not yet been independently re-confirmed in this session.
