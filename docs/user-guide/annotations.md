# Add annotations

Annotations are additional layers whose rows identify selected observations or
genomic intervals. Keeping them as data makes the association explicit and
lets the same labels update with the chart's scales and zoom state.

## Label selected points

Give each annotation both the coordinates of its target and a separate pair of
label coordinates. A rule connects the two positions and a text mark draws the
label:

```{literalinclude} ../tutorials/annotations.py
:language: python
:start-after: annotations-points-start
:end-before: annotations-points-end
```

```{genomespy-chart} annotations:point_annotation_chart
:height: 300
:title: Point annotations with leader lines
```

The annotation table contains only deliberately labelled rows. This is usually
clearer than drawing a text mark for every observation. Prepare the selection
and label coordinates with the chart-ready data when they depend on analysis
or require manual placement; use GenomeSpy transforms when the choice should
respond to browser-side filtering or interaction.

Leader lines are optional when a label can sit directly above its point. When
several labels are close together, move their label coordinates rather than
moving the points, and keep the number of callouts small. The
[airway volcano plot](../gallery/airway_volcano_plot.md) and
[airway MA plot](../gallery/airway_ma_plot.md) apply this pattern to selected
genes.

## Add a gene annotation track

A gene track is an interval track, not a special annotation mode. Each row
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

### Pack overlapping bodies into lanes

`transform_linearize_genomic_coordinate()` converts chromosome and position
pairs into one continuous coordinate system. `transform_collect()` establishes
a deterministic interval order, and `transform_pileup()` assigns overlapping
gene bodies to lanes. Its strand preference keeps the two reading directions
visually stable where space permits. The final filter limits the compact track
to three lanes.

The arrow-block mark communicates strand while still behaving like an interval
from `x` to `x2`. For unstranded annotations, use a rectangle or rule instead.
The same structure works for regulatory elements, peaks, and other named
intervals; only the mark and tooltip fields need to change.

### Keep labels readable

`transform_measure_text()` measures each symbol in pixels.
`transform_filter_scored_labels()` then retains a non-overlapping subset,
preferring larger scores. A score is a label-layout priority only; it should
not be presented as evidence of biological importance. The filter runs in
GenomeSpy, so the visible labels are reconsidered after zooming.

Use a score that has a clear layout meaning. This example uses the number of
contributing RefSeq transcripts. MutGlyph uses a GeneRIF-derived popularity
score instead. A manually curated priority is also reasonable when it is
documented and used only to resolve collisions.

The packaged table contains all canonical chromosomes for both hg19 and hg38,
not only the region that is initially visible. The explicit x-scale domain is
therefore an initial viewport: panning elsewhere continues to reveal the
assembly-matched annotation bodies. Embedding a complete assembly increases
the serialized specification size, but avoids a track that goes empty as soon
as the user leaves a curated example interval.

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

The
[RefSeq genes with scored labels](../gallery/refseq_scored_genes.md) example
shows the full pattern with transcript bodies and semantic zoom. The approach
also follows the generic interval-track design used by
[MutGlyph gene annotations](https://genomespy.app/MutGlyph/articles/gene-annotations.html).
