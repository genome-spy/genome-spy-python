# Expressions

An **expression** is a small calculation, such as doubling a score or checking
whether it is above a cutoff. You write it in Python; GenomeSpy works out the
answer in the browser.

## Calculate from a row

`gs.datum.score` reads the current row's `score`. Here, each score is doubled
and stored in a new field:

```{literalinclude} ../tutorials/expressions.py
:language: python
:start-after: expressions-calculate-start
:end-before: expressions-calculate-end
```

```{genomespy-chart} expressions:chart
:height: 240
:title: Each score multiplied by two
```

Use brackets for field names with spaces or dots: `gs.datum["Sample score"]`.
See [Transforms](transforms.md) for more ways to calculate and filter rows.

(expression-tests)=

## Compare and combine

Compare values with `>`, `>=`, `<`, `<=`, `==`, or `!=`. This test means
“the score is at least 5 and below 10”:

```python
(gs.datum.score >= 5) & (gs.datum.score < 10)
```

Use `&` for “and,” `|` for “or,” and `~` for “not,” with parentheses around
each comparison. Python's `and`, `or`, and `not` do not work here.

Functions live under `gs.expr`. For example, `gs.expr.sqrt(gs.datum.score)`
calculates a square root.

(expression-choices)=

## Choose between two values

`gs.expr.if_()` takes a test, the answer when it is true, and the answer when
it is false:

```{literalinclude} ../tutorials/expressions.py
:language: python
:start-after: expressions-choice-start
:end-before: expressions-choice-end
```

A score of 5 or more gets the label `"high"`; other scores get `"low"`.
Use `None` for a missing result. Use `gs.expr.if_()` instead of Python's
`a if test else b` inside expressions.

For styling selected marks, see {ref}`Conditional encodings <conditional-encodings>`.

## Write an expression as a string

You can also write the calculation using JavaScript-style syntax. These two
forms mean the same thing:

```python
chart.transform_calculate(doubled=gs.datum.score * 2)
chart.transform_calculate(doubled="datum.score * 2")
```

The [GenomeSpy expression reference](https://genomespy.app/docs/grammar/expressions/)
lists the available operators and functions.

For expressions in channels, see {ref}`Encodings <encoding-definitions>`.
To calculate a mark property from a parameter, see
{ref}`Parameters and interaction <parameter-expressions>`.
