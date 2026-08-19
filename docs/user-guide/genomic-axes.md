# Chromosomes and locus scales

A genomic position has two parts: a chromosome or other **contig**, and a
position within that contig. GenomeSpy uses an assembly's contig sizes and order
to concatenate those coordinates into one continuous visual axis.

Use `gs.Locus(chrom_field, position_field)` for this chromosome-aware encoding.
The resulting channel has the `locus` data type and automatically uses a locus
scale.

## Point features

Single nucleotide variants and other point features need one locus:

```{literalinclude} ../tutorials/genomic_coordinates.py
:language: python
:start-after: genomic-coordinates-points-start
:end-before: genomic-coordinates-points-end
```

```{genomespy-chart} genomic_coordinates:point_chart
:height: 230
:title: Four point features in an hg38 region
```

The root `assembly="hg38"` supplies chromosome sizes and order. The scale domain
focuses the initial view on a region of chromosome 17.

`GenomeAxis` options are available through `.axis(...)`. In the example,
`chromGrid=True` enables chromosome-aware grid styling and the title identifies
the coordinate channel. The remaining options are listed in
[genome axis for loci](https://genomespy.app/docs/grammar/axis/#genome-axis-for-loci).

## Genomic intervals

Features such as genes, exons, peaks, and copy-number segments cover a range.
Pair `x` with `x2` to provide the two interval boundaries:

```{literalinclude} ../tutorials/genomic_coordinates.py
:language: python
:start-after: genomic-coordinates-intervals-start
:end-before: genomic-coordinates-intervals-end
```

```{genomespy-chart} genomic_coordinates:interval_chart
:height: 220
:title: Rectangles spanning genomic start and end positions
```

The primary locus establishes the x scale and assembly. The secondary `x2`
channel supplies only the other endpoint and inherits that scale. The same
pattern works with rules, links, and arrows.

## How chromosome positions become one axis

The assembly lists contigs in their preferred order and gives each contig's
length. GenomeSpy places the first contig at the start of a continuous axis,
then places the next contig after it, and so on. `gs.Locus("chrom", "pos")`
inserts the required coordinate-linearization step automatically.

Usually, keep chromosome and position in separate fields and let GenomeSpy
linearize them. A pre-linearized field can be encoded with a regular channel of
type `L`, but it is then your responsibility to ensure that it matches the
selected assembly. The GenomeSpy documentation covers both forms in
[encoding genomic coordinates](https://genomespy.app/docs/grammar/genomic-coordinates/#encoding-genomic-coordinates).

## Coordinate counting and offsets

GenomeSpy's internal genomic intervals are **zero-based and half-open**:

- zero-based means the first base starts at position `0`;
- half-open `[start, end)` includes `start` but excludes `end`.

For example, `[100, 103)` covers three bases: 100, 101, and 102. This convention
makes interval length simply `end - start`.

Formats do not all use the same convention. VCF positions and GFF3 starts are
one-based. Pass `offset=1` to subtract one from such a position during locus
encoding:

```{literalinclude} ../tutorials/genomic_coordinates.py
:language: python
:start-after: genomic-coordinates-offset-start
:end-before: genomic-coordinates-offset-end
```

```{genomespy-chart} genomic_coordinates:offset_chart
:height: 200
:title: One-based inclusive intervals converted during encoding
```

For a one-based inclusive interval such as GFF3 `[1, 10]`, subtract one from the
start and leave the inclusive end unchanged. It then becomes the equivalent
zero-based half-open interval `[0, 10)`. That is why the example sets
`offset=1` only on `start1`.

For a one-based point such as a VCF `POS`, set `offset=1` on its single locus
channel. Do not apply an offset merely because labels should begin at one; an
offset changes data coordinates, while axis label numbering is a presentation
choice. The same convention is described in
[coordinate counting](https://genomespy.app/docs/grammar/genomic-coordinates/#coordinate-counting).

## Built-in assemblies

GenomeSpy includes `hg38`, `hg19`, `hg18`, `mm10`, `mm9`, and `dm6`; the current
list is in
[supported genomes](https://genomespy.app/docs/grammar/genomic-coordinates/#supported-genomes).
Set one as the root default when all locus scales use it:

```python
chart.properties(assembly="hg38")
```

An assembly can instead be set on a specific scale with
`.scale(assembly="hg38")`. Prefer the root property when several tracks share
the same coordinate system; it avoids repetition and keeps their relationship
clear.

## Custom assemblies

A custom assembly needs contig names, sizes, and an intentional order. Define a
reusable assembly in the root `genomes` mapping and select it by name:

```{literalinclude} ../tutorials/genomic_coordinates.py
:language: python
:start-after: genomic-coordinates-custom-start
:end-before: genomic-coordinates-custom-end
```

```{genomespy-chart} genomic_coordinates:custom_assembly_chart
:height: 210
:title: Three custom contigs shown in the declared order
```

The contig array determines the axis order: `chrA`, then `chrB`, then `plasmid`.
A custom definition may instead contain a `url` pointing to a two-column
`chrom.sizes` file. Define an assembly once under `genomes` when several scales
reuse it; a one-off inline definition can be placed in `scale.assembly`.

Contig names in the data must match the assembly. For example, `1` and `chr1`
are different names unless the data loader or preparation step normalizes them.
The accepted definition forms are described in
[custom genomes](https://genomespy.app/docs/grammar/genomic-coordinates/#custom-genomes).

## Multiple assemblies

Most charts use one root assembly. Cross-species and coordinate-comparison
views can assign a different assembly to each locus scale:

```{literalinclude} ../tutorials/genomic_coordinates.py
:language: python
:start-after: genomic-coordinates-multiple-start
:end-before: genomic-coordinates-multiple-end
```

```{genomespy-chart} genomic_coordinates:multiple_assembly_chart
:height: 320
:title: Human positions on x and mouse positions on y
```

Here, x uses human `hg38` coordinates and y uses mouse `mm10` coordinates. A
root assembly is unnecessary because every locus scale identifies its own
assembly. Keep this scale-local form for genuinely different coordinate systems;
ordinary aligned genome-browser tracks should share one root assembly.
