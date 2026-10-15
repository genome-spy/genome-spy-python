## Inputs and adaptation

| Field | Type | Meaning |
| --- | --- | --- |
| `x` | Ordered category | Column identifier. |
| `y` | Ordered category | Row identifier. |
| `z` | Quantitative | Prepared cell value. |

Replace the internal `heatmap_data()` fixture with your prepared long-form table:
one row per x/y pair. Update fields, category order, palette, domain and color
title together. Distinguish missing cells from observed zeros. Enable native axes
when row/column labels are needed; this example deliberately hides them.

Expected here: a 40-column by 20-row grid with quantitative color. Python loads
the prepared synthetic table; no browser-side calculation is declared.
