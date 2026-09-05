# Build linked genome tracks

A genome browser is a set of aligned tracks that describe the same genomic
region. The tracks share one horizontal locus scale, so a zoom or pan applies
to all of them, but each track keeps the vertical scale appropriate for its own
measurements.

This page builds a two-track browser from a quantitative BigWig signal and
categorical BigBed annotations.

## Define one track at a time

The first track maps BigWig intervals to x and GC content to y:

```{literalinclude} ../tutorials/genome_browser_layouts.py
:language: python
:start-after: genome-browser-signal-start
:end-before: genome-browser-signal-end
```

This track deliberately does not set `assembly`, an x domain, or x-axis
options. Those properties describe the relationship between tracks and will
belong to their common parent.

The annotation track layers interval rectangles and labels over one inherited
BigBed source:

```{literalinclude} ../tutorials/genome_browser_layouts.py
:language: python
:start-after: genome-browser-annotations-start
:end-before: genome-browser-annotations-end
```

The layered parent owns the data, locus encodings, category lane, and color.
Both child marks inherit those properties. Only the text child adds a `text`
encoding and zoom-dependent opacity.

`height=gs.step(18)` gives each categorical lane an 18-pixel step. This is more
robust than guessing one fixed height before knowing how many categories are
visible.

## Concatenate and link the tracks

Use `&` to place the signal above the annotations. The concatenated parent owns
the shared genomic context:

```{literalinclude} ../tutorials/genome_browser_layouts.py
:language: python
:start-after: genome-browser-compose-start
:end-before: genome-browser-compose-end
```

```{genomespy-chart} genome_browser_layouts:browser
:height: 260
:title: Two tracks sharing one zoomable genomic axis
```

Try zooming or panning in either track. Both tracks move because they
participate in the same x scale resolution.

## What is shared, and what remains separate?

The parent makes the intended resolutions explicit:

- `resolve_scale(x="shared")` creates one locus domain for both tracks. It also
  lets the parent-level `scales.x` refer to exactly one scale.
- `resolve_axis(x="shared")` draws one genome axis for that shared mapping.
- `resolve_scale(y="independent")` keeps GC percentages separate from the cCRE
  category lanes.
- `resolve_axis(y="independent")` lets each track describe its own y mapping.

An axis represents a scale, so sharing an x axis while keeping x scales
independent would not make sense. Conversely, independent y scales are needed
even when one track hides its y axis with `.axis(None)`. The GenomeSpy
documentation covers these choices in
[scale, axis, and legend resolution](https://genomespy.app/docs/grammar/composition/#scale-axis-and-legend-resolution).

Place the shared `assembly`, x scale, and x axis at the closest parent that
contains all linked tracks. Repeating the domain inside every child creates
more places to update and can accidentally produce separate scale resolutions.

## Titles, heights, and spacing

Track-local properties stay on each track:

- a title names the measurement or annotation source;
- `height` controls the track's plot area;
- y-axis settings describe that track's units;
- mark and encoding choices describe that track's rows.

The concatenated parent owns `spacing`, because spacing describes the gaps
between its children. In this example, structured titles use `orient="left"`
to label the tracks consistently without consuming a separate header row.

Fixed heights work well for continuous signal tracks. Use {py:func}`~genome_spy.step` for
categorical or packed lanes whose content height depends on a row count.

## Scroll a tall track

When the content height should remain large enough for readable lanes, constrain
only its visible viewport:

```{literalinclude} ../tutorials/genome_browser_layouts.py
:language: python
:start-after: genome-browser-scrolling-start
:end-before: genome-browser-scrolling-end
```

`height` remains the content height, while `viewportHeight` limits the space
occupied on screen and adds scrolling when necessary. Avoid replacing a
lane-based content height with a small fixed height; that compresses marks
instead of making them scrollable. See
[scrollable viewports](https://genomespy.app/docs/grammar/composition/concat/#scrollable-viewports).

## Reveal detail with semantic zoom

**Semantic zoom** changes what a view shows as the genomic scale changes. It is
different from ordinary geometric zoom, which only enlarges the same marks.

The annotation labels use:

```python
gs.dynamic_opacity(
    unitsPerPixel=[500, 100],
    values=[0, 1],
)
```

`unitsPerPixel` measures how many genomic units fit in one screen pixel. As the
view moves from 500 toward 100 bases per pixel, the labels fade from invisible
to visible. The interval rectangles remain present at every zoom level, so the
user retains context while details appear.

Use semantic zoom when labels, sequence bases, read mismatches, or other dense
details become meaningful only at close range. Keep a simpler overview layer
visible rather than making the entire track disappear.

The GenomeSpy documentation describes this technique in
[zoom-driven layer opacity](https://genomespy.app/docs/grammar/composition/layer/#zoom-driven-layer-opacity).
Two related mechanisms are
[`multiscale`](https://genomespy.app/docs/grammar/composition/multiscale/), which
switches between whole detail levels, and
[score-based semantic zoom](https://genomespy.app/docs/grammar/mark/point/#semantic-zoom)
for thinning dense point marks.

The [stacked genome browser gallery example](../gallery/stacked_genome_browser.md)
extends this pattern with multiple BigWig signals, sequence, and transcript
annotations. The [composed genome browser](../gallery/composing_genome_browser.md)
shows how independently authored imported views can use a parent-owned locus
scale and axis. The
[linked brush example](../gallery/brush_linked_genome_tracks.md) adds an
always-visible overview whose interval selection navigates several detail
tracks.
