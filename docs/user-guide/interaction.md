# Parameters and interaction

Interaction lets a reader change a visualization without rebuilding its Python
object. GenomeSpy represents interactive state with named **parameters**.
Scales, transforms, encodings, and expressions can read those names and update
when their values change.

Start with the interaction already built into a scale. Add a parameter only
when the chart needs another named piece of state. The GenomeSpy documentation
describes the complete parameter model in
[parameters](https://genomespy.app/docs/grammar/parameters/).

## Enable zoom and pan

Set `zoom=True` on a positional scale to enable interactive navigation:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-zoom-start
:end-before: interaction-zoom-end
```

```{genomespy-chart} interaction:zoom_chart
:height: 280
:title: A locus scale with zooming and panning enabled
```

The scale domain is the state being changed. No explicit parameter is needed.
In a linked-track browser, put the zoom option on the one shared scale so every
track follows the same domain.

## Bind a parameter to an input

`gs.param(name, value=..., bind=...)` declares a named value and an HTML input
that changes it. This slider controls a filter threshold:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-binding-start
:end-before: interaction-binding-end
```

```{genomespy-chart} interaction:bound_chart
:height: 310
:title: A slider controls filtering and point size
```

The parameter name `minScore` becomes available to expressions in the same view
and its descendants. The filter expression reads it directly:

```python
"datum.score >= minScore"
```

`datum` means the current data row. Moving the slider re-evaluates the filter in
the browser; Python does not receive the value or rebuild the chart.

The second parameter demonstrates a reactive expression:

```python
gs.param("pointSize", expr="60 + minScore * 100")
```

Because `pointSize` depends on `minScore`, GenomeSpy recalculates it whenever the
slider changes. `gs.expr("pointSize")` then supplies the current result to the
mark's size. Expressions use GenomeSpy's JavaScript-like expression language,
not Python syntax.

The GenomeSpy documentation covers the available input widgets in
[input bindings](https://genomespy.app/docs/grammar/parameters/#using-input-bindings)
and reactive parameters in
[expressions](https://genomespy.app/docs/grammar/parameters/#expressions).

Use unique, descriptive parameter names. Define a parameter at the closest
common parent of every view that needs to read it.

## Select marks and style them conditionally

A **selection parameter** stores data items or intervals chosen through pointer
gestures. A point selection can drive conditional encodings:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-selection-start
:end-before: interaction-selection-end
```

```{genomespy-chart} interaction:selection_chart
:height: 280
:title: Click a point; Shift-click to toggle additional points
```

The base opacity is `0.25`. Its condition changes opacity to `1` when a row is
in `selectedVariant`. An empty point selection matches every row by default, so
all points begin fully visible.

The stroke condition uses `empty=False`. It therefore applies only to actual
selected rows and does not outline every point before the first click. The
GenomeSpy documentation explains this behavior in
[empty selections](https://genomespy.app/docs/grammar/conditional-encoding/#empty-selections)
and the surrounding rules in
[conditional encoding](https://genomespy.app/docs/grammar/conditional-encoding/).

`key=gs.Key("id")` gives each row a stable identity. A key should be unique and
remain unchanged when data updates. It prevents a selection from depending on
the accidental order of rows.

Use `select="point"` for discrete rows. An interval selection instead describes
a continuous brushed range:

```python
gs.param(
    "brush",
    select={"type": "interval", "encodings": ["x"]},
)
```

Interval selections can filter rows or supply another scale's domain for an
overview-and-detail layout. When an x scale is already zoomable, GenomeSpy uses
Shift-drag to start the brush by default so brushing does not conflict with
panning. See
[point](https://genomespy.app/docs/grammar/parameters/#point-selection) and
[interval selections](https://genomespy.app/docs/grammar/parameters/#interval-selection)
for their configuration options, and
[domain from selection parameters](https://genomespy.app/docs/grammar/scale/#domain-from-selection-parameters)
for the overview-and-detail pattern.

## Add one ruler across linked tracks

A **ruler parameter** follows a domain coordinate and draws a cursor guide. It
is not a selection: it tracks a coordinate rather than a set of rows.

Define one ruler at the common parent of the tracks it should span:

```{literalinclude} ../tutorials/interaction.py
:language: python
:start-after: interaction-ruler-start
:end-before: interaction-ruler-end
```

```{genomespy-chart} interaction:ruler_chart
:height: 360
:title: One pointer ruler spanning two linked tracks
```

`encodings=["x"]` says which domain coordinate to track. The parent has one
shared x scale and both descendants inherit an x locus encoding, so the ruler
has one unambiguous target. `extent="container"` draws one line across the
aligned vertical container instead of a separate guide inside each track.

Pointer rulers follow mouse movement and clear on mouse leave by default. Set
`source="viewport"` when the ruler should track the center of the visible domain
instead. The GenomeSpy documentation covers snapping, clearing, and guide
styling in
[ruler parameters](https://genomespy.app/docs/grammar/parameters/#ruler-parameters).

## Keep interaction state close to its consumers

Parameter scope follows the view hierarchy:

- define a track-local control on that track;
- define shared controls, selections, and rulers on the nearest common parent;
- let descendant transforms and encodings read the parameter by name;
- define the parameter only once at that scope.

This placement mirrors data and scale ownership. It reduces repeated
definitions and makes it clear which views participate in an interaction.
