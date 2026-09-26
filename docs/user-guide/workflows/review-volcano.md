# Review treatment-responsive genes

{download}`Download the notebook <../../../notebooks/review_volcano.ipynb>`

Which dexamethasone-responsive genes deserve follow-up? **Shift-drag** to brush
several genes, or **click** one point to select its record.
Scroll to zoom; drag without Shift to pan. The gallery’s two sliders control
the absolute log2 fold-change cutoff and −log10 p cutoff. Dashed guide lines
and point colors update with them. Defaults are p ≤ 0.01 and |log2 fold change| ≥ 1.

```{genomespy-workflow} volcano
```

Select **Add to shortlist**, enter a review note, then change or clear the plot
selection. The application shortlist stays intact. Remove unwanted candidates
with **Remove**.

**Export selection CSV** contains the current selection, including rows beyond
the 20-row preview. **Export shortlist CSV** contains saved genes and notes.
Both retain original statistics and eight length-scaled sample-count columns named
by SRA run ID. The plot uses the gallery’s −log10 raw p-value axis and display cap;
exports retain the original p-values. Candidate selection is exploratory, not validation.

The tables, notes, and CSV downloads belong to the host
application, outside GenomeSpy. Interval hooks return ranges, which the host
matches against the prepared table. Point hooks return records directly.
Saved records are keyed by Ensembl ID, so adding them twice does not duplicate
or overwrite notes. Reloading the page clears this in-memory shortlist; export
it before reloading.

## Python

The notebook uses the same chart and prepared dataset. Python callbacks put
selected records into a pandas DataFrame and save a shortlist with notes.
The row-removal controls are specific to this web demo.
All statistical analysis ran during dataset preparation; GenomeSpy renders and
interacts with the prepared values in the browser.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} volcano
:code: chart
```
::::

::::{dropdown} Python hooks
```{genomespy-workflow} volcano
:code: hooks
```
::::

:::{admonition} Data use and provenance
:class: note

The data, gene subset, fold changes, p-values, plotting domains, and default
color thresholds are identical to the [gallery volcano example](../../gallery/airway_volcano_plot.md).
Packaged Bioconnector workshop counts from Himes et al. (2014), GSE52778,
were prepared with kallisto and tximport `lengthScaledTPM` (CC BY-NC-SA 4.0).
The gallery helper computes paired t-tests on log2(count+1), Benjamini–Hochberg
adjustment, and retains 12,000 genes by mean count after filtering at mean ≥10.
CSV sample columns contain the same rounded length-scaled counts used by that
analysis. `tools/prepare_airway_review.py` packages these
existing results and sample measurements without changing the analysis.
:::
