:::{admonition} Data use and provenance
:class: note

The visualization uses a mirrored copy of the ClinVar GRCh38 VCF release from
NCBI's [ClinVar FTP downloads](https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/).
ClinVar asks that redistributed data be attributed to ClinVar as the data
source.
:::

## What to notice

Each variant has a point at its classification row and a rule connecting it to
the uncertain-significance baseline. Position locates the variant; vertical
position and color encode its normalized germline classification.

## Python implementation

A lazy tabix-indexed VCF source loads the visible records. Formula,
regular-expression, and filter transforms normalize `CLNSIG`, and three layers
draw the baseline, stems, and points.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/clinvar-variants/)
for the original classification discussion.
