# Bundled example data

The wheel contains 17 data files under `genome_spy/datasets/data/`. This static
documentation directory contains byte-identical copies of the two Airway CSVs,
`hapmap_gwas.csv`, `oncoprint_dataset3.json`, and `pik3ca_mutations.json`.
Documentation also publishes chart-ready derivatives in generated specs and
Arrow assets.

See the [third-party notices](../../THIRD_PARTY_NOTICES.md) for attribution,
license links and modifications. The source
repository also carries these notices at its root. Dataset terms are separate
from the MIT license of the Python implementation.

| File | Origin / processing |
| --- | --- |
| `airway_scaledcounts.csv` | Bioconnector's kallisto/tximport `lengthScaledTPM` reprocessing of Himes et al., GSE52778; exact workshop copy |
| `airway_metadata.csv` | Exact Bioconnector eight-sample metadata table |
| `hapmap_gwas.csv` | manhattanly via Plotly; HapMap 3 draft release 2 coordinates, UCSC hg18 gene annotations, simulated p-values/effects and derived z-scores |
| `oncoprint_dataset3.json` | Plotly Dash Bio alteration fixture, copied without modification |
| `pik3ca_mutations.json` | Exact Plotly NeedlePlot fixture; grouped historical UniProt P42336 annotations and Pfam domains, not cancer-sample frequencies |
| `p53_sequence_comparison_aligned.fasta.gz` | 34 UniProt sequences via Plotly, aligned with MAFFT 7.526 L-INS-i |
| `tcga.tsv` | Exact pyoncoprint cBioPortal LUAD PanCancer Atlas 2018 export, including a subsequently retracted microbiome study |
| `tcga_laml.maf.gz` | maftools mutation calls, protein changes and Washington University VAF annotations |
| `tcga_laml_annot.tsv` | maftools LAML clinical and survival annotations |
| `brca.maf.gz` | maftools mutation calls for TCGA-A8-A08B |
| `tcga_laml_combined_oncoplot.json.gz` | Python-prepared joins and summaries of six maftools inputs, plus its custom pathway groups |
| `pik3ca_tcga_brca_lollipop.json` | GenomeSpy's GDC TCGA-BRCA recurrent mutation counts and UniProt P42336 domains |
| `tcga_ov_gistic_scores.tsv.gz` | Firehose OV-TP 2016-01-28 `scores.gistic`, gzip-compressed |
| `tcga_ov_gistic_lesions.tsv.gz` | Same release's `all_lesions.conf_99.txt`, gzip-compressed |
| `refseq_gene_bodies.csv.gz` | UCSC hg19/hg38 `refGene`, overlapping transcripts collapsed in Python |
| `tal1_alphagenome_reference.json.gz` | UCSC hg38 chr1 reference sequence and local interval metadata; no model output |
| `mutation_impact_reference.json` | Project-authored synthetic values |

Airway workshop contributions are CC BY-NC-SA 4.0. UniProt data are CC BY 4.0;
Pfam data are CC0. See the notices for source-specific attribution and terms.
