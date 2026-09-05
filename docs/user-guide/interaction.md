# Parameters and interaction

Interaction lets a users to change and manipulate a visualization without rebuilding it from scratch. The `genome-spy-python`API follows closely to the parameter ergonomics of
[Altair](https://altair-viz.github.io/user_guide/interactions/parameters.html):
create a handle, attach it to a chart, then reuse that handle in an
encoding, expression, or filter.

In practice, GenomeSpy represents interactive state with named **parameters**. Scales,
transforms, encodings, and expressions can read those names and update when
their values change. The GenomeSpy documentation describes the complete parameter model in [parameters](https://genomespy.app/docs/grammar/parameters/).

## Zoom and pan

The simplest interaction needs no parameter at all. This chart's locus scale is
navigable as it stands:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-zoom-start
:end-before: interaction-zoom-end
```

```{genomespy-chart} interaction:zoom_chart
:height: 280
:title: A locus scale, zoomable without any configuration
```

The scale domain is the state being changed, and no explicit parameter holds it.
In a linked-track browser, put the domain on the one shared scale so every track
follows it.

## Parameters handle interaction

- A {py:func}`~genome_spy.param` is a named value, such as a cutoff.
- A {py:func}`~genome_spy.binding_range` is the input widget used to change
  that value.
- A {py:func}`~genome_spy.selection_point` stores marks a user clicks
- A {py:func}`~genome_spy.selection_interval` stores a range they drag over (brush).
- {py:meth}`~genome_spy.TopLevelSpec.add_params` puts the parameter on the
  chart that owns it.

## Bind a parameter to an input

{py:func}`~genome_spy.param` declares a value,
{py:func}`~genome_spy.binding_range` makes a slider, and
{py:meth}`~genome_spy.TopLevelSpec.add_params` attaches
the parameters to the chart:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-binding-start
:end-before: interaction-binding-end
```

```{genomespy-chart} interaction:bound_chart
:height: 310
:title: A slider controls filtering and point size
```

Parameters can be used directly in Python expressions. Here, `min_score`
controls the filter:

```python
gs.datum.score >= min_score
```

`datum` means the current data row. Moving the slider makes GenomeSpy run the
filter again in the browser.

The second parameter demonstrates a reactive expression:

```python
point_size = gs.param("pointSize", expr=60 + min_score * 100)
```

GenomeSpy recalculates `point_size` when `min_score` changes. Passing the handle
to `mark_point(size=...)` uses its current value.

The x-axis is told to always show all variant names. Moving the filter slider may hide some points, but it does not make the remaining names shift position.

The GenomeSpy documentation covers the available input widgets in
[input bindings](https://genomespy.app/docs/grammar/parameters/#using-input-bindings)
and reactive parameters in
[expressions](https://genomespy.app/docs/grammar/parameters/#expressions).

### More slider examples

- **Thresholds:** [Manhattan plot](../gallery/manhattan_plot.md),
  [HapMap volcano plot](../gallery/volcano_plot.md),
  [Airway volcano plot](../gallery/airway_volcano_plot.md), and
  [Airway MA plot](../gallery/airway_ma_plot.md) use sliders to change
  significance or effect-size cutoffs.
- **Track settings and filtering:** [BAM read alignments](../gallery/bam_read_alignments.md),
  [Sashimi plot](../gallery/sashimi_plot.md), and
  [ASCAT fitting](../gallery/ascat_fitting.md) use sliders to filter data or
  adjust a track’s layout and model settings.

## Select marks and style them conditionally

A selection parameter stores what the user picks. Use
{py:func}`~genome_spy.selection_point` for discrete marks
Use {py:func}`~genome_spy.when` to make an encoding conditional: choose one
visual value when a condition matches (`.then(...)`) and optionally another when it does not (`.otherwise(...)`). This reacts to a selection or a value parameter, for example, changing a mark’s color, opacity, size, or outline.

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-selection-start
:end-before: interaction-selection-end
```

```{genomespy-chart} interaction:selection_chart
:height: 280
:title: Click a point; Shift-click to toggle additional points
```

Selected points are opaque and outlined; other points are faint.

In the selection definition, `empty=False` makes the chart start with no
selected points:

`selected_variant = gs.selection_point("selectedVariant", empty=False)`

In the point encoding, `key=gs.Key("id")` uses each point’s `id` value to
identify it. This helps the chart keep the right point selected if its data is
updated or reordered.

See [point](https://genomespy.app/docs/grammar/parameters/#point-selection) for more configuration options.

## Select intervals with brushing

Use {py:func}`~genome_spy.selection_interval` or a **brush** for a dragged range selection. A **brush** is a translucent rectangle a user drags to choose an area. It is useful, for example, when an overview, such as a chromosome track, should control what other linked tracks show.

In code, create a named value to hold the selected brush range with {py:func}`~genome_spy.param`. Then add an interval selection with the same name using {py:func}`~genome_spy.selection_interval` to let the user drag a rectangle. Dragging updates `brush` with the chosen range. Other chart parts can reuse `brush` to zoom, filter data, or change mark styles.

In the following example, The top row is a map of the chromosomes. Drag across it to choose which part of the genome appears below. That dragged rectangle is the **brush**. It stores the selected genomic range under the name `brush`, and both detail tracks read that same range, so they move together.

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-brush-start
:end-before: interaction-brush-end
```

```{genomespy-chart} interaction:brush_chart
:height: 280
:title: Drag across the chromosome map to navigate both tracks
```

Dragging the overview updates `brush` with the selected range. Both detail
tracks use that range as their x-axis domain, so they move together. The
overview always shows the full chromosome layout; drag its brush or zoom a
detail track to change the shared view.

The brush example uses a few extra configuration objects because an overview
controls two linked detail tracks.

- {py:class}`~genome_spy.BrushConfig` controls how the dragged selection
  rectangle looks, including its fill and outline. Use it only when the default
  brush style is not enough.

- {py:class}`~genome_spy.AxisGenomeData` provides the built-in chromosome overview data for the top row.

- {py:class}`~genome_spy.SelectionDomainRef` connects each detail track’s x-axis to `brush`. Its `initial` value chooses the range shown when the chart first opens.

See GenomeSpy's documentation on
[interval selections](https://genomespy.app/docs/grammar/parameters/#interval-selection) and [domains from selection parameters](https://genomespy.app/docs/grammar/scale/#domain-from-selection-parameters)
for the underlying grammar. The [linked brush gallery example](../gallery/brush_linked_genome_tracks.md) applies the same pattern to three genome-wide association tracks.

## Add one ruler across linked tracks

A **ruler parameter** follows a coordinate and draws a guide across tracks.
{py:func}`~genome_spy.ruler` is GenomeSpy-specific, but it uses
the same create, attach, and reuse pattern as value and selection parameters.

Define one ruler at the common parent of the tracks it should span:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-ruler-start
:end-before: interaction-ruler-end
```

```{genomespy-chart} interaction:ruler_chart
:height: 240
:title: One pointer ruler spanning two linked tracks
```

In the ruler definition, `encodings=["x"]` makes the ruler follow the horizontal
position, and `extent="container"` makes one line span both tracks.
`persist=False` clears the ruler when the pointer leaves the chart.

{py:class}`~genome_spy.RulerMarkConfig` controls how that line looks, including
its color and width. Use it only when the default ruler style is not enough.

Pointer rulers follow mouse movement by default. Set `source="viewport"` when
the ruler should instead follow the centre of the visible range.

The GenomeSpy documentation covers snapping, clearing, and guide styling in
[ruler parameters](https://genomespy.app/docs/grammar/parameters/#ruler-parameters).

## Share parameters with the charts that need them

Attach a parameter to the smallest chart group that needs it.

If a slider, selection, or ruler affects only one track, add it to that track.
If it affects several tracks, add it to the chart that contains those tracks.
The tracks inside that group can then use the same parameter.

Define each shared parameter once. This keeps every affected track in sync and
avoids giving the chart several competing values with the same name.

The [ASCAT fitting](../gallery/ascat_fitting.md) example uses sliders that
control several linked tracks.
