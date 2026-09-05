# Label points and genomic intervals

Labels and leader lines make the important parts of a chart easier to find.
In this tutorial we combine ordinary text, rule, and interval marks with your main visualization to showcase how datapoints or intervals can be annotated.

## Label selected points

Give each label annotation the coordinates of its target and a pair of pixel offsets
for the label endpoint. A rule connects the offset endpoint to the point, and a
text mark draws the label:

```{literalinclude} ../tutorials/annotations.py
:language: python
:start-after: annotations-points-start
:end-before: annotations-points-end
```

```{genomespy-chart} annotations:point_annotation_chart
:height: 300
:title: Point annotations with leader lines
```

The label table contains only the points you want to call out. This is usually
clearer than labelling every observation. Pixel offsets keep label spacing
steady while readers zoom.

Leader lines are optional when a label can sit directly above its point. When
several labels are close together, adjust their offsets rather than moving the
points, and keep the number of callouts small. The
[airway volcano plot](../gallery/airway_volcano_plot.md) and
[airway MA plot](../gallery/airway_ma_plot.md) apply this pattern to selected
genes.

## Add a gene context track

A gene track is simply an interval track. Each row
needs a chromosome, start and end coordinates, and a label. Strand and a
label-priority score are useful additions. The coordinates must use the same
assembly and counting convention as the tracks they accompany.

The example below uses the full packaged hg19 RefSeq gene-body resource and
opens around three mutation clusters from the rainfall gallery. Each gene is
represented by one body for each overlapping symbol, chromosome, and strand
locus. The label score counts contributing RefSeq transcripts:

```{literalinclude} ../tutorials/annotations.py
:language: python
:start-after: annotations-genes-start
:end-before: annotations-genes-end
```

```{genomespy-chart} annotations:gene_annotation_track
:height: 170
:title: Real RefSeq genes with packed, scored labels
```

### Arrange overlapping genes

Nearby genes can overlap, so
{py:meth}`~genome_spy.TopLevelSpec.transform_linearize_genomic_coordinate`
first places their coordinates on one shared axis.
{py:meth}`~genome_spy.TopLevelSpec.transform_collect` puts them in a predictable
order, and {py:meth}`~genome_spy.TopLevelSpec.transform_pileup` assigns
overlapping genes to separate lanes. The final filter shows up to three lanes
to keep the track compact.

Arrow-shaped gene bodies show their direction. For intervals without a
direction, use a rectangle or rule instead.

### Keep labels readable

{py:meth}`~genome_spy.TopLevelSpec.transform_measure_text` measures each gene
name. {py:meth}`~genome_spy.TopLevelSpec.transform_filter_scored_labels` then
shows only labels that fit without overlapping. When there is not enough room
for every label, genes with a higher `score` are preferred.

Here, `score` is only a layout preference: it helps choose which names to show.
It is not a measure of biological importance. Labels are checked again as the
reader zooms, so more names can appear when there is room.

### Align the track with another visualization

Place the completed annotation track below a signal track with `&`, then put
the assembly, locus domain, genome axis, and shared x resolution on their
common parent. Keep y scales independent because the primary measurement and
the packed gene lanes have unrelated units.

The [rainfall plot](../gallery/rainfall_plot.md) aligns hg19 genes with mutation
distances around a cluster-rich region. The
[TCGA OV GISTIC landscape](../gallery/tcga_ov_gistic.md) uses the same track
dataflow with hg19 genes around the 19p13.3 deletion peak. In both charts,
zooming either view updates the primary plot and gene context together.

The [RefSeq genes with scored labels](../gallery/refseq_scored_genes.md) example
shows the full pattern with transcript bodies and semantic zoom.
