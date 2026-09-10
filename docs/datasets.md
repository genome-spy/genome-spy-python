# Example datasets

The combined LAML oncoplot uses `load_dataset("tcga_laml_combined_oncoplot")`;
the p53 sequence comparison loads aligned FASTA text with
`load_dataset("p53_sequence_comparison", as_format="text")`. Their
sources and processing are described in the
[combined oncoplot](gallery/combined_laml_oncoplot.md) and
[p53 comparison](gallery/p53_sequence_comparison.md) gallery pages.

The package ships the tables that the [gallery](gallery/index.md) examples use,
so you can try the API on real data without downloading anything.

Data retain their own terms, independently of the source packages' software
licenses. See the
<a href="THIRD_PARTY_NOTICES.md">third-party notices</a> for file-level status, attribution,
and terms.

```python
from genome_spy.datasets import available_datasets, load_dataset

available_datasets()
counts = load_dataset("airway_scaledcounts")
```

`load_dataset()` returns a pandas DataFrame for tabular files and parsed JSON
for JSON files. Pass `as_format="text"` to get the raw file contents instead.

| Dataset | Contents |
| --- | --- |
| `airway_metadata` | Sample table for the airway RNA-seq experiment |
| `airway_scaledcounts` | Rounded, length-scaled gene counts for the same eight samples |
| `hapmap_gwas` | HapMap coordinates with simulated p-values and effect sizes |
| `brca_maf` | Somatic mutation calls for one TCGA breast-tumor sample |
| `pik3ca_mutations` | Historical UniProt feature counts and Pfam protein domains |
| `tcga_oncoprint` | Plotly Dash Bio alteration fixture |
| `mutation_impact_reference` | Project-authored synthetic reference window |
| `tal1_alphagenome_reference` | UCSC hg38 reference sequence with interval metadata |
| `pik3ca_tcga_brca_lollipop` | Prepared recurrent PIK3CA mutations and protein domains |
| `tcga_laml_maf` | Somatic mutation calls for TCGA acute myeloid leukemia |
| `tcga_laml_annotations` | Clinical annotations for those leukemia samples |
| `tcga_laml_combined_oncoplot` | Prepared mutation, copy-number, clinical, pathway, VAF, and MutSig tables |
| `p53_sequence_comparison` | 34 p53 protein sequences aligned with MAFFT L-INS-i, compressed FASTA |
| `pyoncoprint_tcga` | Alteration matrix for TCGA lung adenocarcinoma samples |
| `tcga_ov_gistic_scores` | GISTIC2 copy-number scores for TCGA ovarian tumors |
| `tcga_ov_gistic_lesions` | GISTIC2 peak regions for the same cohort |
| `refseq_gene_bodies` | Assembly-wide hg19 and hg38 RefSeq gene bodies |

:::{admonition} Data use and provenance
:class: note

- `airway_metadata` and `airway_scaledcounts` describe the airway smooth muscle
  RNA-seq experiment of Himes et al., *PLoS One* 2014
  ([GEO GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778)),
  independently reprocessed by Stephen Turner for the
  [Bioconnector workshops](https://github.com/bioconnector/workshops/blob/0785f9ffbab87f451f35d52bf48f2fa228e8327a/_dev/airway_kallisto/airway_kallisto_tximport.R)
  with kallisto and tximport `lengthScaledTPM`. The bundled CSVs exactly match
  those workshop files; the workshop declares CC BY-NC-SA 4.0.
- `hapmap_gwas` is the `HapMap` example table from the
  [manhattanly](https://cran.r-project.org/package=manhattanly) R package.
  HapMap supplied the build-36 map coordinates and rs identifiers; UCSC hg18
  supplied gene annotations. The association statistics are simulated or
  derived from simulated p-values. The table contains no individual genotypes.
- `brca_maf`, `tcga_laml_maf`, and `tcga_laml_annotations` are the example
  files bundled with [maftools](https://bioconductor.org/packages/maftools/)
  and contain TCGA mutation calls or clinical annotations.
- `pik3ca_tcga_brca_lollipop` contains the chart-ready named datasets from
  GenomeSpy's official TCGA-BRCA PIK3CA lollipop example. Mutation counts come
  from GDC masked somatic MAFs and protein domains from UniProt P42336; see the
  gallery example for full provenance.
- `pyoncoprint_tcga` is the example alteration table from
  [pyoncoprint](https://github.com/pnucolab/pyoncoprint) as a cBioPortal TCGA LUAD export. See the
  [cBioPortal data policy](https://docs.cbioportal.org/user-guide/faq/) and the
  study-specific notice linked in our third-party notices. Its microbiome
  track comes from a study retracted in 2024 and is not a validated finding.
- `tcga_ov_gistic_scores` and `tcga_ov_gistic_lesions` are the complete
  `scores.gistic` and `all_lesions.conf_99.txt` tables used by the official
  GenomeSpy example. They are open-access TCGA OV-TP GISTIC2 output produced
  by the Broad Institute TCGA Genome Data Analysis Center, Firehose run
  2016-01-28
  ([source archive](https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/OV-TP/20160128/gdac.broadinstitute.org_OV-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz)).
- `refseq_gene_bodies` is independently prepared from the official hg19 and
  hg38 UCSC `refGene` tables. Overlapping transcripts are collapsed by symbol,
  chromosome, and strand; transcript counts prioritize colliding labels. See
  UCSC's [conditions for use](https://genome.ucsc.edu/license/).

Results shown with the TCGA-derived tables are in whole or part based upon data
generated by the
[TCGA Research Network](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing).
:::
