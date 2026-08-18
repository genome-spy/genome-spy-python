# Composition

Composition combines complete views into a larger visualization. GenomeSpy
uses three concise operators for the most common layouts:

| Operator | Composition | Result |
| --- | --- | --- |
| `a + b` | Layer | Draw `b` over `a` in the same plot area |
| `a & b` | Vertical concatenation | Place `a` above `b` |
| `a \| b` | Horizontal concatenation | Place `a` to the left of `b` |

Use `gs.concat(..., columns=n)` when the layout is an explicit wrapping grid.
Composition is hierarchical, so layers and concatenations can be nested. The
GenomeSpy documentation introduces the same model in
[view composition](https://genomespy.app/docs/grammar/composition/).

```{literalinclude} ../tutorials/composition.py
:language: python
:start-after: composition-data-start
:end-before: composition-data-end
```

## Layer complementary marks

Layer marks when they describe the same coordinate system. The first layer is
drawn first; later layers appear above it:

```{literalinclude} ../tutorials/composition.py
:language: python
:start-after: composition-layer-start
:end-before: composition-layer-end
```

```{genomespy-chart} composition:layered_chart
:height: 310
:title: Labels layered over points
```

Neither child declares data, positions, or color. Those properties belong to
the layered parent and are **inherited** by both children. The text layer adds
only the `text` encoding that it alone needs.

Place shared properties at the nearest common parent. Descendants can override
an inherited data source, encoding, transform, or view property when their
behavior differs. See
[layering views](https://genomespy.app/docs/grammar/composition/layer/) for the
layer-specific options.

## Stack aligned tracks vertically

The `&` operator gives each child its own plot area. It is particularly useful
for aligned tracks that share horizontal positions:

```{literalinclude} ../tutorials/composition.py
:language: python
:start-after: composition-vertical-start
:end-before: composition-vertical-end
```

```{genomespy-chart} composition:vertical_chart
:height: 300
:title: Two vertically concatenated tracks with one horizontal scale
```

The parent supplies the data and `x` encoding. Both tracks therefore use one
zoomable horizontal scale. Their `y` scales remain independent because signal
and quality have different units and domains.

Vertical concatenation shares `x` resolution by default because aligned tracks
are common in GenomeSpy. The explicit calls above document the intended
relationship and keep it visible when the chart becomes more complex.

## Compare panels side by side

The `|` operator keeps panels separate while arranging them horizontally:

```{literalinclude} ../tutorials/composition.py
:language: python
:start-after: composition-horizontal-start
:end-before: composition-horizontal-end
```

```{genomespy-chart} composition:horizontal_chart
:height: 300
:title: Control and treated samples in aligned panels
```

The children filter the inherited data independently. Shared `x` and `y`
scales make positions directly comparable, while independent x axes let each
panel label that shared mapping within its own column. Child sizing, spacing,
and separators are documented in
[view concatenation](https://genomespy.app/docs/grammar/composition/concat/).

## Shared, independent, and excluded resolution

A **resolution** states which child views participate in the same scale, axis,
or legend:

- `shared` creates one mapping and one domain for participating views. Zooming
  a shared positional scale updates all participants.
- `independent` creates a separate mapping for each child. Use it when fields
  have different units or unrelated domains.
- `excluded` keeps a scale shared inside its local subtree but prevents that
  resolution from being pulled into an ancestor's shared scale. It is useful
  for aligned grids containing side summaries with different units.

Configure these relationships with `resolve_scale()`, `resolve_axis()`, and
`resolve_legend()`. An axis can be shared only when its scale is shared. Legend
resolution normally follows the corresponding visual scale. The GenomeSpy
documentation describes the rules in
[scale, axis, and legend resolution](https://genomespy.app/docs/grammar/composition/#scale-axis-and-legend-resolution)
and the aligned-axis case in
[shared axes](https://genomespy.app/docs/grammar/composition/concat/#shared-axes).

Two composition features have no dedicated page in this guide:
[`multiscale`](https://genomespy.app/docs/grammar/composition/multiscale/) for
semantic zoom between detail levels, and
[importing views](https://genomespy.app/docs/grammar/import/) for reusing a view
by URL or template. Both are available through `gs.multiscale(...)` and
`gs.import_view(...)`.

## Advanced grid layouts

An UpSet-style layout combines a top summary, a left summary, and a matrix. A
two-column grid needs an empty top-left cell so the summaries align with the
matrix:

```{literalinclude} ../tutorials/composition.py
:language: python
:start-after: composition-grid-start
:end-before: composition-grid-end
```

```{genomespy-chart} composition:grid_chart
:height: 390
:title: A two-column grid with an empty top-left cell
```

The child order fills the grid row by row:

| Empty placeholder | Column summary |
| --- | --- |
| Row summary | Membership matrix |

The column summary shares its `x` index scale with the matrix but excludes its
quantitative `y` scale. The row summary does the converse. The matrix and
summaries therefore stay aligned without forcing row counts, column counts,
and matrix indices into incompatible resolutions.

The parent owns the data and shared index-scale domains. This keeps row and
column order in one place and links later zooming or panning across the matrix
and its summaries.
