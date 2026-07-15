# Genomic axes and loci

GenomeSpy's defining feature is the genomic coordinate system. Use `Locus(...)`
to place a field on a chromosome-aware axis and configure the chromosome grid
and labels through `GenomeAxis`.

```python
import genome_spy as gs
from genome_spy.schema import GenomeAxis

axis = GenomeAxis().chromGrid(True).chromLabels(True).chromTicks(True)

gs.Chart(variants).mark_point().encode(
    x=gs.Locus("chrom", "pos").scale(assembly="hg38").axis(axis),
    y=gs.Y("neglog:Q"),
)
```

The `scale={"assembly": "hg38"}` option lays out chromosomes using a known
genome assembly. A secondary `x2` locus channel draws intervals (for example
genes or peaks).

For interval-style tracks, pair `x=gs.Locus(...)` with `x2=gs.Locus(...)`:

```python
gs.Chart(features).mark_rect().encode(
    x=gs.Locus("chrom", "start"),
    x2=gs.Locus("chrom", "end"),
    y="score:Q",
)
```

Use ordinary `X`, `Y`, `Color`, and other channel classes alongside locus
channels when you need browser-style views that mix genomic position with
annotations, coverage, or categorical tracks.
