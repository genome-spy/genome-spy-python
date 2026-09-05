# Parameters and interaction

Interaction lets a reader change and manipulate a visualization without rebuilding it from scratch. This API follows closely to the parameter ergonomics of
[Altair](https://altair-viz.github.io/user_guide/interactions/parameters.html):
create a handle, attach it to a chart, then reuse that handle in an
encoding, expression, or filter.

In practice, GenomeSpy represents interactive state with named **parameters**. Scales,
transforms, encodings, and expressions can read those names and update when
their values change. The GenomeSpy documentation describes the complete parameter model in [parameters](https://genomespy.app/docs/grammar/parameters/).

## The four interaction building blocks

- A {py:func}`~genome_spy.param` is a named value, such as a cutoff.
- A {py:func}`~genome_spy.binding_range` is the input widget used to change
  that value.
- A {py:func}`~genome_spy.selection_point` stores marks a reader clicks;
  {py:func}`~genome_spy.selection_interval` stores a range they drag over.
- {py:meth}`~genome_spy.TopLevelSpec.add_params` puts the parameter on the
  chart that owns it.

A **brush** is simply an interval selection: the translucent rectangle that a
reader drags to choose a range. The selected range can then color marks, filter
rows, or set a genomic scale domain.

`gs.when(...).then(...).otherwise(...)`
uses a selection in an encoding; `then()` and `otherwise()` are methods on the
builder returned by {py:func}`~genome_spy.when`, not separate
top-level functions.

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

The explicit variant domain keeps every category on the x-axis while the filter
hides and shows points.

The GenomeSpy documentation covers the available input widgets in
[input bindings](https://genomespy.app/docs/grammar/parameters/#using-input-bindings)
and reactive parameters in
[expressions](https://genomespy.app/docs/grammar/parameters/#expressions).

Use unique, descriptive parameter names. Define a parameter at the closest
common parent of every view that needs to read it.

## Select marks and style them conditionally

A **selection parameter** stores what the reader picks. Use
{py:func}`~genome_spy.selection_point` for discrete marks or
{py:func}`~genome_spy.selection_interval` for a dragged range. The
{py:func}`~genome_spy.when` helper uses
that selection in an encoding:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-selection-start
:end-before: interaction-selection-end
```

```{genomespy-chart} interaction:selection_chart
:height: 280
:title: Click a point; Shift-click to toggle additional points
```

Selected points are opaque and outlined; other points are faint. Setting
`empty=False` means the condition matches nothing until the first click. The
GenomeSpy documentation explains this behavior in
[empty selections](https://genomespy.app/docs/grammar/conditional-encoding/#empty-selections)
and the surrounding rules in
[conditional encoding](https://genomespy.app/docs/grammar/conditional-encoding/).

`key=gs.Key("id")` gives each point a stable identity.

Use `select="point"` for discrete rows. An interval selection instead describes
a continuous brushed range. See
[point](https://genomespy.app/docs/grammar/parameters/#point-selection) and
[interval selections](https://genomespy.app/docs/grammar/parameters/#interval-selection)
for their configuration options.

## Brush an overview to navigate linked tracks

The top row is a map of the chromosomes. Drag across it to choose which part of
the genome appears below. That dragged rectangle is the **brush**. It stores
the selected genomic range under the name `brush`, and both detail tracks read
that same range, so they move together.

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-brush-start
:end-before: interaction-brush-end
```

```{genomespy-chart} interaction:brush_chart
:height: 370
:title: Drag across the chromosome map to navigate both tracks
```

`brush` stores the highlighted region. `initial` chooses the first visible
region. Both detail tracks use the brush as their x-axis range. Think of it as
using the overview to move a shared viewport: drag a different region above,
and the tracks below show that region.

The chromosome row always shows the whole genome. Drag its brush, or zoom one
of the detail tracks, and the other views follow automatically.

See GenomeSpy's documentation on
[interval selections](https://genomespy.app/docs/grammar/parameters/#interval-selection)
and
[domains from selection parameters](https://genomespy.app/docs/grammar/scale/#domain-from-selection-parameters)
for the underlying grammar. The
[linked brush gallery example](../gallery/brush_linked_genome_tracks.md) applies
the same pattern to three genome-wide association tracks.

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

`encodings=["x"]` tracks the x coordinate. `extent="container"` draws one line
across both tracks.

Pointer rulers follow mouse movement and clear on mouse leave by default. Set
`source="viewport"` when the ruler should track the center of the visible domain
instead. The GenomeSpy documentation covers snapping, clearing, and guide
styling in
[ruler parameters](https://genomespy.app/docs/grammar/parameters/#ruler-parameters).

## Keep interaction state close to its consumers

Put a parameter on the nearest chart that contains everything using it:

- define a track-local control on that track;
- define shared controls, selections, and rulers on the nearest common parent;
- let descendant transforms and encodings read the parameter by name;
- define the parameter only once at that scope.

The [ASCAT fitting](../gallery/ascat_fitting.md) example drives a whole
visualization from bound parameters.
