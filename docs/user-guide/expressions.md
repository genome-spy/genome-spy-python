# Expressions

An **expression** is a small calculation, such as doubling a score or checking
whether it is above a cutoff. You write it in Python; GenomeSpy works out the
answer in the browser.

## Calculate from a row

`gs.datum.score` reads the current row's `score`. This expression doubles it:

```{literalinclude} ../tutorials/expressions.py
:language: python
:start-after: expressions-row-start
:end-before: expressions-row-end
```

Use brackets for field names with spaces or dots: `gs.datum["Sample score"]`.

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
double_score = gs.datum.score * 2
double_score = "datum.score * 2"
```

The [GenomeSpy expression reference](https://genomespy.app/docs/grammar/expressions/)
lists the available operators and functions.

For expressions in channels, see {ref}`Encodings <encoding-definitions>`.
To calculate a mark property from a parameter, see
{ref}`Parameters and interaction <parameter-expressions>`.

## Use expressions with transforms

`transform_calculate()` stores an expression's answer in a field.
`transform_filter()` keeps rows that pass a test:

```{literalinclude} ../tutorials/expressions.py
:language: python
:start-after: expressions-transforms-start
:end-before: expressions-transforms-end
```

```{genomespy-chart} expressions:chart
:height: 240
:title: Double each score, then keep values of at least 10
```

This stores `double_score` and `score_label` as `doubled` and `label`, then
keeps rows where `doubled` is at least 10. See [Transforms](transforms.md)
for more ways to change rows.
