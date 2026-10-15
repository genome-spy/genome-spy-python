## Inputs and adaptation

Input: numeric `x` positions, loaded in Python by an internal gallery fixture.
Each panel derives its own `value` in GenomeSpy: `sin(x / 4)` above and
`cos(x / 5)` below.

Replace `sincos_data()` with your table. If it already contains measurements,
remove the formula transforms and encode those fields on y. Update titles,
units and domains. Keep `&` or `gs.vconcat` for stacked panels; explicitly choose
shared/independent scales when adapting the intended navigation and value ranges.

Expected here: two vertically stacked point views from the same 31 input
positions, with a red lower series. The formulas execute in the browser,
not in Python.
