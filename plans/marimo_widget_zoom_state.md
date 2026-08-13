# Preserve GenomeSpy Zoom During AlphaGenome Updates

## Problem

After the first selected allele completes inference, the TAL1 GenomeSpy view
returns to its initial eight-base domain. This makes the user zoom back into
the sequence designer before every first edit of a session.

## Cause

The chart widget is currently included in a reactive `mo.vstack(...)` cell.
That cell depends on design and prediction state, so Marimo re-mounts the
anywidget whenever either state changes. GenomeSpy then initializes from the
spec's fixed opening domain. The live `view.set_dataset(...)` calls themselves
do not recreate GenomeSpy and should retain the current domain.

## Deferred Implementation

1. Keep the `view = chart.widget(...)` and `chart_widget = mo.ui.anywidget(view)`
   construction in its state-independent cell.
2. Add a standalone output cell whose only dependency is `chart_widget`.
3. Remove `chart_widget` from the state-dependent status `mo.vstack(...)` cell;
   that cell should render only setup, design summary, status, and the model
   warning.
4. Browser-test: zoom away from the opening domain, make the first edit, wait
   for inference, and confirm that the displayed genomic domain is unchanged.

## Acceptance Criteria

- A prediction refresh updates named `edits`, `selected_site`, and
  `predictions` datasets without re-embedding GenomeSpy.
- Pan and zoom survive first, cached, and subsequent predictions.
- Click events continue to reach Marimo and selected-site guides still update.
