# Interactive workflows

Try these demos in your browser, or use the results in Python with a notebook.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Annotate genomic intervals
:link: annotate-intervals
:link-type: doc

Brush a region, name it, and add it to a separate annotation track. Export BED.
:::

:::{grid-item-card} Select genes for follow-up
:link: select-genes
:link-type: doc

Brush a volcano plot and export the selected genes.
:::

:::{grid-item-card} Pick individual genes
:link: pick-genes
:link-type: doc

Click or Shift-click points to collect selected gene records.
:::

:::{grid-item-card} Edit a sequence
:link: edit-sequence
:link-type: doc

Choose nucleotides in a letter grid and compare edits with the reference.
:::
::::

The web demos need no Python kernel. Each page also includes a notebook
for Jupyter or VS Code.

New to using selections in Python? Start with
[Use chart interactions in Python](../embed-api.md), which includes a small
notebook example and an optional web app.

```{toctree}
:hidden:

annotate-intervals
select-genes
pick-genes
edit-sequence
```
