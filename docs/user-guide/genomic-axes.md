# Genomic axes and loci

GenomeSpy's defining feature is the genomic coordinate system. Use `Locus(...)`
to place a field on a chromosome-aware axis and configure the chromosome grid
and labels through `GenomeAxis`.

```python
import genome_spy as gs
from genome_spy.schema import GenomeAxis

axis = GenomeAxis(chromGrid=True, chromLabels=True, chromTicks=True)

gs.Chart(variants).mark_point().encode(
    x=gs.Locus("chrom", "pos", scale={"assembly": "hg38"}, axis=axis),
    y=gs.Y("neglog:Q"),
)
```

The `scale={"assembly": "hg38"}` option lays out chromosomes using a known
genome assembly. A secondary `x2` locus channel draws intervals (for example
genes or peaks).

:::{admonition} Work in progress
:class: note
This guide page is a scaffold. Expand it with assembly options, interval
tracks, and the peak/gene locus example.
:::
