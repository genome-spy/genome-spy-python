# Encodings and channels

An **encoding** maps data to a visible property. The property being controlled
is called a **channel**: `x` controls horizontal position, `color` controls
color, and `size` controls mark size. The field supplies the values, while its
data type tells GenomeSpy how those values should be interpreted.

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-data-start
:end-before: encoding-channels-data-end
```

## Field and type shorthand

The compact string `"score:Q"` contains a field name (`score`) and a type code
(`Q`) separated by a colon. The shorthand and explicit forms below produce the
same encodings:

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-syntax-start
:end-before: encoding-channels-syntax-end
```

Use shorthand when a field and type are enough. Use a channel class such as
`gs.X`, `gs.Color`, or `gs.Tooltip` when adding a title, scale, axis, legend, or
another channel option. Setter methods can be chained:

```python
gs.X("score:Q").scale(zero=False).axis(grid=True).title("Score")
```

## Data types describe meaning

Choose a type from what a field means, not merely from how Python stores it:

| Code | Type | Concrete example |
| --- | --- | --- |
| `Q` | quantitative | A measured score such as `3.4` |
| `N` | nominal | An unordered sample label such as `A` or `B` |
| `O` | ordinal | An ordered stage such as low, medium, or high |
| `I` | index | A numbered sequence position with a regular slot |
| `L` | locus | A chromosome-aware genomic position |

A numeric identifier is usually nominal, not quantitative: sample `12` is not
twice sample `6`. Likewise, an ordinal field describes order but does not claim
that the distance from low to medium equals the distance from medium to high.
The selected type affects the default scale and the guide GenomeSpy creates, as
described in
[visual encoding](https://genomespy.app/docs/grammar/mark/#visual-encoding).

## Visual channels

Several encodings can describe different parts of the same row:

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-visual-start
:end-before: encoding-channels-visual-end
```

```{genomespy-chart} encoding_channels:channel_chart
:height: 310
:title: Position, color, shape, size, opacity, and tooltip encodings
```

The most common channels have distinct jobs:

| Channels | Purpose |
| --- | --- |
| `x`, `y` | Primary horizontal and vertical positions |
| `x2`, `y2` | Secondary endpoints for ranges, rectangles, links, and arrows |
| `color`, `opacity`, `size`, `shape` | Visible mark properties |
| `text` | Content drawn by a text mark |
| `tooltip` | Details shown when pointing at a mark |

Position is generally the easiest visual channel to compare accurately. Color
and shape are useful for categories; size and opacity can show quantities but
are harder to compare precisely. A tooltip adds details without replacing a
clear visible encoding. The GenomeSpy documentation lists every channel,
including the offset channels, in
[channels](https://genomespy.app/docs/grammar/mark/#channels).

## Index positions

The `I` type combines numbered positions with regular-width slots. It is useful
for bases, amino acids, matrix columns, and other ordered integer locations:

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-index-start
:end-before: encoding-channels-index-end
```

```{genomespy-chart} encoding_channels:index_chart
:height: 170
:title: Bases positioned with an index channel
```

Unlike an ordinal category, an index remains linear and can be zoomed: index and
locus scales both zoom and pan by default, with no option to set. Each integer
also has a band, allowing a rectangle to fill one indexed position. The
[index scale](https://genomespy.app/docs/grammar/scale/#index-scale) describes
that behavior in detail.

## Genomic loci

The `L` type places positions on a chromosome-aware axis. `gs.Locus()` is the
clearest form when chromosome and position are stored in separate fields:

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-locus-start
:end-before: encoding-channels-locus-end
```

```{genomespy-chart} encoding_channels:locus_chart
:height: 220
:title: Genomic intervals encoded as loci
```

The chart's `assembly="hg38"` supplies chromosome names, lengths, and order.
Without a `domain`, the scale would span the whole genome and these 31 kb of
features would collapse into one thin line, so the example opens on a 40 kb
window around them.
The genomic coordinates guide covers locus domains and coordinate conventions
in detail, as does the
[locus scale](https://genomespy.app/docs/grammar/scale/#locus-scale) in the
GenomeSpy documentation.

## Field, datum, value, and expression

Most encodings read a field, but an encoding definition can obtain its value in
four ways:

```{literalinclude} ../tutorials/encoding_channels.py
:language: python
:start-after: encoding-channels-definitions-start
:end-before: encoding-channels-definitions-end
```

```{genomespy-chart} encoding_channels:definition_chart
:height: 200
:title: Four kinds of encoding definition
```

| Definition | Meaning | Example above |
| --- | --- | --- |
| Field | Read a value from every row | `gs.X("score:Q")` |
| Datum | Use a constant in the scale's data domain | `gs.datum(0, type="quantitative")` |
| Value | Use a constant visual value without a scale | `gs.value("#4c78a8")` |
| Expression | Calculate a value while the chart runs | `gs.expr("datum.amount * datum.confidence")` |

A datum and a value are deliberately different. A quantitative datum of `0`
is mapped through the channel's scale; a positional value of `0` means the
start of the visual range and a value of `0.5` means its midpoint.

Expressions that participate in a scale need an explicit type, as the size
expression above demonstrates. GenomeSpy cannot infer whether an arbitrary
expression returns a quantity, category, index, or locus. The
[expression language](https://genomespy.app/docs/grammar/expressions/) describes
what an expression may contain.

Scales translate data values into visual values. Axes and legends explain those
translations to the reader. Their defaults and focused customization are the
subject of the next guide.
