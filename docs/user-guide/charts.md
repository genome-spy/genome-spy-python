# Charts and marks

A `Chart` combines data, one geometric shape called a **mark**, and encodings
that control where and how those marks are drawn. A chart with one mark type is
also called a *unit view*.

For most marks, GenomeSpy draws one mark for every data row. Six rows therefore
produce six points in this example:


```{literalinclude} ../tutorials/charts_and_marks.py
:language: python
:start-after: charts-marks-point-start
:end-before: charts-marks-point-end
```

```{genomespy-chart} charts_and_marks:point_chart
:height: 320
:title: A point for each observation
```

The call to `mark_point()` chooses the geometry. The calls inside `encode()`
connect data fields to visual channels such as position, color, and size.

## Static properties and data-driven encodings

The location of a property determines whether it is constant or varies with
the data:

| Level | Example above | Effect |
| --- | --- | --- |
| Mark | `filled=True`, `stroke="white"` | Applies to every point |
| Encoding | `color="sample:N"`, `size="amount:Q"` | Reads a value from each row |
| View | `title=...`, `description=...` | Describes the chart area as a whole |

Put a visual value directly in the mark method when every instance should look
the same. Put it in `encode()` when the value should represent a field.
`properties()` is for view-level settings such as `width`, `height`, `title`,
and the accessibility-oriented `description`. The GenomeSpy documentation lists
the properties shared by all marks in
[marks](https://genomespy.app/docs/grammar/mark/#properties).

## Choose a mark for the visual task

Different marks emphasize different aspects of the data:

| Mark method | Useful for | GenomeSpy reference |
| --- | --- | --- |
| `mark_point()`  | Individual observations and distributions | [Point](https://genomespy.app/docs/grammar/mark/point/) |
| `mark_rect()` | Bands, intervals, and heatmaps | [Rect](https://genomespy.app/docs/grammar/mark/rect/) |
| `mark_rule()` | Ranges, boundaries, and reference lines | [Rule](https://genomespy.app/docs/grammar/mark/rule/) |
| `mark_tick()` | Compact positions along one axis | [Tick](https://genomespy.app/docs/grammar/mark/tick/) |
| `mark_text()` | Labels or values shown as text | [Text](https://genomespy.app/docs/grammar/mark/text/) |
| `mark_link()` | Connections between two positions | [Link](https://genomespy.app/docs/grammar/mark/link/) |
| `mark_arrow()` | Directed connections or events | [Arrow](https://genomespy.app/docs/grammar/mark/arrow/) |

Marks can often express related tasks, so choose the one that makes the intended reading
most direct. Each reference page lists the properties that mark supports.

The [point mark](../gallery/point_mark.md) and
[rect heatmap](../gallery/rect_heatmap.md) examples show two of them in full.

## Ranged marks use secondary positions

A point needs one position on each axis. An interval needs a start and an end.
The secondary channels `x2` and `y2` supply that second endpoint:

```{literalinclude} ../tutorials/charts_and_marks.py
:language: python
:start-after: charts-marks-ranges-start
:end-before: charts-marks-ranges-end
```

```{genomespy-chart} charts_and_marks:interval_chart
:height: 250
:title: Rules spanning start and end positions
```

Here, each rule begins at `start` and ends at `end`. A rectangle can likewise
use `x` with `x2`, `y` with `y2`, or both pairs to fill an area. A tick is a
compact rule centered on a single encoded position. Which marks support a second
endpoint is documented in
[secondary channels](https://genomespy.app/docs/grammar/mark/#secondary-channels).

## Text is also a mark

Text becomes data-driven through the `text` encoding. The mark's `size=13` is
constant, while each rendered label comes from the `sample` field:

```{literalinclude} ../tutorials/charts_and_marks.py
:language: python
:start-after: charts-marks-text-start
:end-before: charts-marks-text-end
```

```{genomespy-chart} charts_and_marks:text_chart
:height: 260
:title: Field values rendered as text
```

Text marks work well for short labels. Dense labels can overlap, so points or
rectangles are usually better for large datasets.

## Links and arrows connect rows

Links and arrows also use primary and secondary positions, but they connect
the endpoints instead of showing a range along one axis:

```{literalinclude} ../tutorials/charts_and_marks.py
:language: python
:start-after: charts-marks-relations-start
:end-before: charts-marks-relations-end
```

```{genomespy-chart} charts_and_marks:link_chart
:height: 280
:title: Curved links between positions
```

```{genomespy-chart} charts_and_marks:arrow_chart
:height: 280
:title: Directed arrows between positions
```

Use a link when the relationship has no direction. Use an arrow when the
source-to-target direction matters. Both examples reuse the same encoded base;
only their marks and view properties differ.

Mark methods return new chart objects, so a base can be reused safely as shown
above. Repeated defaults across many charts can instead be set with GenomeSpy
configuration, which is covered later in the user guide.
