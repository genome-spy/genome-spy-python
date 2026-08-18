# Configuration

GenomeSpy exposes appearance and layout at several levels. Choosing the narrowest
appropriate level keeps a specification predictable:

| Level | Typical API | Scope |
| --- | --- | --- |
| Mark | `mark_point(size=...)` | Every instance of that mark |
| Encoding | `size="amount:Q"` | Varies from row to row |
| View | `.properties(...)`, `.with_view(...)` | One chart or composed subtree |
| Configuration | `.configure_*()` | Defaults within a configuration scope |
| Theme | `.properties(theme=...)` | Broad root-level visual preset |

Explicit properties win over configured defaults. A configured point size, for
example, applies only when the point mark or size encoding does not provide a
more specific value. The GenomeSpy documentation describes where a default
applies in [config scopes](https://genomespy.app/docs/grammar/config/#config-scopes)
and how competing defaults are settled in
[resolution order](https://genomespy.app/docs/grammar/config/#resolution-order).

```{literalinclude} ../tutorials/configuration.py
:language: python
:start-after: configuration-data-start
:end-before: configuration-data-end
```

## Configure one chart

This example uses all three non-data appearance levels deliberately:

```{literalinclude} ../tutorials/configuration.py
:language: python
:start-after: configuration-levels-start
:end-before: configuration-levels-end
```

```{genomespy-chart} configuration:configured_chart
:height: 300
:title: Explicit view properties with configured defaults
```

The responsibilities are separate:

- `mark_point()` sets properties specific to these points;
- `properties()` sets the title, plot size, and padding;
- `with_view()` sets the current view's background and border;
- `configure_point()` supplies defaults for point marks;
- `configure_axis()` and `configure_title()` supply guide and title defaults.

Use `configure_mark()` for defaults shared by every mark type and a specific
method such as `configure_point()`, `configure_rect()`, or `configure_text()`
when the default belongs to one geometry. Configuration methods merge into the
chart's `config` block and can be chained.

`configure_view()` differs from `with_view()`: the former supplies defaults to
views in its configuration scope, while the latter explicitly styles the
current view.

## Titles and descriptions

A string is sufficient for a simple title:

```python
chart.properties(title="Response by sample")
```

Use `gs.title()` for subtitles or placement options:

```python
chart.properties(
    title=gs.title(
        "Response by sample",
        subtitle="Six measurements",
        orient="top",
        anchor="start",
    )
)
```

`orient` chooses the side of the view and `anchor` positions the title along
that side. Use `.configure_title(...)` when several titles in a composed chart
should share typography. A view `description` is not normally drawn, but gives
the chart an accessibility-oriented textual description. Reserved and overlay
titles, subtitles, and styling are covered in
[titles](https://genomespy.app/docs/grammar/title/).

## Fixed dimensions

Numeric `width` and `height` values are plot-area sizes in logical pixels:

```python
chart.properties(width=360, height=210)
```

Fixed dimensions are useful for controlled layouts and small standalone
figures. Avoid hardcoding every child size in a large composition; repeated
fixed values make the layout difficult to adapt.

## Step sizing for discrete positions

For a nominal, ordinal, or index position, `gs.step()` reserves a fixed amount
of space for every scale value:

```{literalinclude} ../tutorials/configuration.py
:language: python
:start-after: configuration-step-start
:end-before: configuration-step-end
```

```{genomespy-chart} configuration:step_chart
:height: 260
:title: Width derived from four categorical steps
```

The four categories and `gs.step(48)` produce a plot width based on four
48-pixel steps. If another category is added, the plot grows automatically.
Step sizing is useful for matrices, alignments, categorical rows, and compact
genome-browser tracks. See
[step sizing](https://genomespy.app/docs/grammar/composition/concat/#step-sizing)
in the GenomeSpy documentation.

## Container and flexible sizing

`"container"` allows a view to use available space. Concatenated children can
combine fixed pixels with flex-like growth through `gs.SizeDef()`:

```{literalinclude} ../tutorials/configuration.py
:language: python
:start-after: configuration-flex-start
:end-before: configuration-flex-end
```

```{genomespy-chart} configuration:flex_chart
:height: 110
:title: One fixed child and one growing child
```

The left child has a fixed 120-pixel plot width. The right child has `grow=1`,
so it receives remaining horizontal space, while `minPx=180` prevents it from
becoming too narrow. `gs.SizeDef` can combine:

- `px` for an absolute component;
- `grow` for a share of remaining space;
- `minPx` and `maxPx` for constraints.

Use `viewportWidth` or `viewportHeight` when the content should retain its
calculated size but appear inside a smaller scrollable viewport. This is often
preferable to squeezing a long categorical or sequence view. The GenomeSpy
documentation covers both in
[child sizing](https://genomespy.app/docs/grammar/composition/concat/#child-sizing)
and
[scrollable viewports](https://genomespy.app/docs/grammar/composition/concat/#scrollable-viewports).

## Padding and spacing

`padding` reserves space around one view. Use a number for equal padding or
`gs.Paddings()` for individual edges:

```python
chart.properties(
    padding=gs.Paddings(top=8, right=12, bottom=4, left=12)
)
```

`spacing` is different: it controls the gaps between children of a
concatenation. Keep padding local to the view that needs breathing room and
spacing on the parent that arranges the children.

## Built-in themes

A theme supplies a coordinated set of broad defaults. Theme selection belongs
on the root specification:

```{literalinclude} ../tutorials/configuration.py
:language: python
:start-after: configuration-theme-start
:end-before: configuration-theme-end
```

```{genomespy-chart} configuration:themed_chart
:height: 290
:title: A chart using the Quartz theme
```

Available built-in themes include `genomespy`, `vegalite`, `quartz`, `dark`,
`fivethirtyeight`, and `urbaninstitute`. The default is `genomespy`. The current
list and a preview of each theme are in
[built-in themes](https://genomespy.app/docs/grammar/config/#built-in-themes).

Use a theme for the broad visual language, configuration for repeated defaults,
and explicit properties for intentional exceptions. Local explicit properties
take precedence over both configuration and theme defaults.
