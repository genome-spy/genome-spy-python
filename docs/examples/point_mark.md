## Inputs and adaptation

| Field | Type | Source |
| --- | --- | --- |
| `x` | Quantitative | Prepared example positions loaded in Python. |
| `sin`, `cos` | Quantitative | Derived by GenomeSpy's browser transforms. |

For your table, replace `sincos_data()` with the table supplied to `gs.Chart`;
the loader is an internal gallery fixture. Update the `x` field and axis title.
Keep the formulas only if those functions are the intended measurements;
otherwise encode your existing y/color columns and remove the formulas.

Expected here: point height follows `sin(x / 4)`, color follows `cos(x / 5)`,
and numeric x/y scales allow zoom. No statistical analysis runs in Python.
