# Third-party notices

The project's original code is MIT-licensed. Third-party code and data retain
their own terms; the project license does not relicense those materials.

## GenomeSpy schema and examples

The bundled `src/genome_spy/schema/genome-spy-schema.json`, generated schema
bindings and descriptions, and adapted official visualization examples come
from [GenomeSpy](https://github.com/genome-spy/genome-spy), copyright
2018–2026 Kari Lavikka, under MIT. The full license is in
`LICENSES/GENOMESPY-MIT.txt`.

GenomeSpy's schema types include material adapted from Vega-Lite (axis, scale,
data, title, channel, and selection definitions) and Vega (input bindings).
Their notices also apply to the corresponding bundled schema and generated
descriptions: University of Washington Interactive Data Lab. All rights
reserved. The BSD-3-Clause terms and upstream copyright
notices are in `LICENSES/VEGA-LITE-BSD-3-Clause.txt` and
`LICENSES/VEGA-BSD-3-Clause.txt`. Expression API generation also reads
GenomeSpy and Vega expression documentation.

## Bundled reference and example data

- **`p53_sequence_comparison_aligned.fasta.gz`:** 34 UniProt
  Consortium p53 sequences, obtained through
  [Plotly's FASTA](https://github.com/plotly/datasets/blob/0c447c47b757ad74edecab31f0d72f849d2e67c2/Dash_Bio/Genetic/alignment_viewer_p53.fasta).
  The accession and sequence version are retained in each header, including
  P02340 sequence version 3. GenomeSpy Python aligned the sequences with MAFFT
  7.526 L-INS-i and gzip-compressed the result. UniProt's copyrightable data
  are [CC BY 4.0](https://www.uniprot.org/help/license/); retain attribution,
  the license link, and this modification notice. UniProt provides no warranty
  of correctness and does not grant patent or other third-party rights.
- **`pik3ca_mutations.json`:** Plotly's NeedlePlot PIK3CA fixture,
  copied without modification. Its 173 feature rows match UniProt P42336
  entry version 193 (also 197, 201 and 203), grouped by feature type and
  coordinates; values count annotations, not tumor samples. The separate
  domain track comes from Pfam through the
  [demo's parser](https://github.com/plotly/dash-bio/blob/master/dash_bio/utils/mutation_data_parser.py).
  Credit the UniProt Consortium (CC BY 4.0), Pfam/InterPro at EMBL-EBI
  ([CC0 1.0](https://www.ebi.ac.uk/interpro/about/license/)), and Plotly for
  selecting and reformatting this historical teaching fixture.
- **`hapmap_gwas.csv`:** byte-identical to Sahir Bhatnagar's
  [manhattanly table](https://github.com/sahirbhatnagar/manhattanly/blob/f959be07f7c1df747ed5fe0169d72a97a49b343a/data-raw/HapMap.csv),
  via Plotly. Coordinates and rs identifiers are from the HapMap 3 draft
  release 2 PLINK map (2009-01, build 36); the
  [HapMap project released its data into the public domain](https://www.genome.gov/11511175/about-the-international-hapmap-project-fact-sheet).
  Gene names/distances are UCSC hg18 annotations, not HapMap observations.
  P-values and effect sizes are simulated; z-scores are calculated from those
  p-values. Retain the manhattanly/Plotly MIT contribution notices and credit
  HapMap and UCSC. No individual genotypes are in this file.
- **`refseq_gene_bodies.csv.gz`:** independently prepared from
  UCSC hg19/hg38 `refGene` downloads dated 2026-08-26; overlapping transcripts
  are collapsed and counted. Credit UCSC and NCBI RefSeq. The
  [UCSC data terms](https://genome.ucsc.edu/license/) permit public and
  commercial use of these reference tables.
- **`tal1_alphagenome_reference.json.gz`:** UCSC hg38/GRCh38
  chr1:47173759–47304831 (zero-based, half-open), retrieved 2026-08-10 and
  packaged with project-authored interval metadata. Credit UCSC and the Genome
  Reference Consortium under the same UCSC data terms. This is reference
  sequence, not AlphaGenome code, weights, or predictions.
- **`mutation_impact_reference.json`:** project-authored synthetic
  teaching data, under the project's MIT license.
- **`pik3ca_tcga_brca_lollipop.json`:** named datasets copied from
  [GenomeSpy's documented example](https://github.com/genome-spy/genome-spy/blob/3b55caf5111ab769da222a93990ca38480495f9e/docs/examples/genomic-data/pik3ca-tcga-brca-lollipop.md).
  Open-access GDC TCGA-BRCA masked somatic calls were aggregated into distinct
  tumor counts for recurrent canonical-transcript mutations, omitting
  singletons. Credit the TCGA Research Network and retain the no-reidentification
  requirement. Protein length and selected domains are from UniProt P42336,
  CC BY 4.0; credit the UniProt Consortium and GenomeSpy's selection/reformatting.
- **`tcga_ov_gistic_scores.tsv.gz`, `tcga_ov_gistic_lesions.tsv.gz`:**
  [GenomeSpy's documented open-access Broad/TCGA outputs](https://genomespy.app/docs/examples/genomic-data/tcga-ov-gistic/),
  byte-identical after decompression to Firehose OV-TP CopyNumber GISTIC2
  Level 4, run 2016-01-28, GISTIC2.0.22, hg19. Only compression changed.
  Credit the TCGA Research Network and Broad Institute TCGA Genome Data
  Analysis Center (2016), retain the source archive citation and respect
  TCGA responsible-use and no-reidentification requirements.

The full CC BY 4.0 and CC0 texts are in `LICENSES/CC-BY-4.0.txt` and
`LICENSES/CC0-1.0.txt`. The source-repository MIT notices in
`LICENSES/DATA-SOURCE-REPOSITORIES-MIT.txt` accompany the corresponding
selection, formatting and example contributions.

## Bundled TCGA example tables

| Files | Source and processing |
| --- | --- |
| `tcga.tsv` | Pyoncoprint revision `31e6d6de78b64070a9c6c582ce3ef571b14e4c71`, a cBioPortal LUAD PanCancer Atlas 2018 tabular export. See the provider notices below. |
| `oncoprint_dataset3.json` | Plotly Dash Bio alteration fixture at revision `20088fe2168789d0d5f5ba9820df9bd46f73231f`, copied without modification. |
| `tcga_laml.maf.gz`, `tcga_laml_annot.tsv`, `brca.maf.gz` | Maftools files at `015a4cf8c69ba89a55a3fdcea911421509e9a198`, copied without modification. LAML includes mutation/VAF and clinical annotations; BRCA contains one sample, TCGA-A8-A08B. |
| `tcga_laml_combined_oncoplot.json.gz` | Python-prepared tables derived from six maftools inputs at that revision. Custom pathway groups come from its vignette; GISTIC and MutSig inputs match Firehose LAML-TB 2016-01-28. Processing joins clinical data and derives alteration, recurrence, VAF and MutSig summaries. |

Credit TCGA and the contributing studies, Plotly, pyoncoprint and maftools
(Anand Mayakonda), as applicable.

## Airway data

**`airway_scaledcounts.csv`, `airway_metadata.csv`:** exact Bioconnector
workshop copies. Counts were prepared with kallisto and rounded tximport
`lengthScaledTPM` values from the Himes et al. experiment.

Airway source attribution: Stephen Turner and the UVA Bioconnector workshop
contributors, [scaled counts](https://github.com/bioconnector/workshops/blob/d0c4d0cca5f21dc2c6e12912dc09d5e279e706ce/data/airway_scaledcounts.csv)
and [metadata](https://github.com/bioconnector/workshops/blob/b563237b8feb18857d048b74975de6e753667fad/data/airway_metadata.csv),
from Himes et al., *PLoS One* 2014,
[doi:10.1371/journal.pone.0099625](https://doi.org/10.1371/journal.pone.0099625),
GEO GSE52778. The workshop's [CC BY-NC-SA 4.0 license](https://github.com/bioconnector/workshops/blob/b563237b8feb18857d048b74975de6e753667fad/LICENSE)
is retained in `LICENSES/CC-BY-NC-SA-4.0.txt` for its contributions. It requires
attribution, noncommercial use, modification notices, and share-alike for
adaptations.

## Provider terms and scientific context

The LUAD export includes Dicipivirus microbiome values from Poore et al. (2020),
[retracted in 2024](https://doi.org/10.1038/s41586-024-07656-x).
cBioPortal [removed the profile](https://github.com/cBioPortal/datahub/commit/18edd66a52b4d1b10a697e8d2fee79e1b1452b73)
on 2024-07-08. These values must not be presented as validated biological
findings. Credit TCGA, cBioPortal, the contributing studies and pyoncoprint.

cBioPortal's [data policy](https://docs.cbioportal.org/user-guide/faq/) specifies
ODbL unless otherwise noted; the historical LUAD
[study notice](https://github.com/cBioPortal/datahub/blob/2ba97208ff41206df19e860cee5e44236c3cc93b/public/luad_tcga_pan_can_atlas_2018/LICENSE)
refers to Broad GDAC terms. Preserve the applicable provider notices. ODbL's
requirements include attribution, database notices, and share-alike and
machine-readable availability for qualifying derivative databases.

Results using TCGA-derived data are in whole or part based upon data generated
by the [TCGA Research Network](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing).
GDC's
[analysis policy](https://gdc.cancer.gov/analyze-data/data-analysis-policies)
prohibits attempts to reidentify participants, including for open data.

## Code adapted from Vega-Altair

Parts of this project are adapted from
[Vega-Altair](https://github.com/vega/altair), copyright 2015–2025 the
Vega-Altair Developers, under the BSD-3-Clause license. The complete license
is in [`LICENSES/ALTAIR-BSD-3-Clause.txt`](LICENSES/ALTAIR-BSD-3-Clause.txt).

The adapted areas are:

- `src/genome_spy/schemapi.py`, a reduced schema-wrapper runtime based on
  `altair/utils/schemapi.py`;
- `src/genome_spy/_expressions.py`, expression authoring primitives adapted
  from `altair/expr/core.py`;
- `tools/schemapi/codegen.py`, whose schema-wrapper generation architecture is
  adapted from Altair's `tools/schemapi/` package and
  `tools/generate_schema_wrapper.py`;
- the multifeature penguins and cars strip-plot cases in `tests/test_chart.py`,
  adapted from Altair's example suite and mark documentation.

Each adapted source location identifies its corresponding upstream source.

## Design references

Altair also informed the separation between generated schema bindings and the
handwritten chart API, composition operators, channel shorthand, and API
reference organization. Those areas use project-specific implementations and
are acknowledged as design references rather than adapted Altair code.

MutGlyph informed the generic scored gene-annotation track used by the
rainfall and GISTIC examples. The implementation and UCSC-derived data are
maintained independently in this repository.
