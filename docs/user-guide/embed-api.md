# Use chart selections in Python

Brush a chart to get selected regions or genes in Python. You can save those
results or send new annotations back to the chart.

Start with an [interactive workflow](workflows/index.md):

- [Annotate genomic intervals](workflows/annotate-intervals.md): name regions,
  add them to a separate track, and export BED.
- [Select genes for follow-up](workflows/select-genes.md): brush a volcano plot,
  inspect the selected genes, and export a CSV.

## How it works

Each notebook connects the chart to Python in a background task. Let the cell
finish, then interact with the chart. The connection keeps listening while you
work.

The annotation notebook stores records in `annotations`. The gene-selection
notebook updates a pandas table called `selected_genes`:

```python
# Run after brushing in the gene-selection notebook.
selected_genes[["ensgene", "log2fc", "padj"]]
```

These values stay in memory until you export them. Rerun an inspection cell to
refresh its output; the tables beside the charts update automatically.

:::{note}
The web demos run in your browser. To update Python values, use a running
kernel in Jupyter or VS Code and wait for the notebook's connection message.
:::

## If it does not connect

Restart the kernel and run all cells. Keep the background-task setup from the
example: waiting for a browser reply directly in a cell can block that reply
in VS Code.

The embed API is experimental. See [advanced integration](embed-integration.md)
for supported operations, custom hosts, and connection details.
