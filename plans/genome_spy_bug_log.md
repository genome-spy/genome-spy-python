# GenomeSpy Bug Log

This document records GenomeSpy bugs and behavior gaps that should become
upstream issues once they have a minimal reproduction and a proposed fix.

## GS-001 - Tooltip coordinates are wrong in transformed embeds

**Status:** Needs upstream issue

**Observed in:** The documentation gallery's wide LUAD oncoprint embed.

**Symptoms:**

- Hovering a gene-matrix cell reports the wrong gene. For example, a cell in
  the `KRAS` row can report `MAPK8`.
- The upper tracks do not respond to hover in the expected area.
- The apparent tooltip hit area starts lower than the visible chart and the
  offset increases through the plot.

**Reproduction context:**

- Embed a wide GenomeSpy chart in a narrower documentation column.
- Apply a CSS transform such as `transform: scale(...)` to the chart container
  to fit it to the available width.
- Hover matrix cells and tracks after the chart has been scaled.

**Suspected cause:**

The browser displays the canvas using transformed coordinates, while GenomeSpy
hit-testing and tooltip placement use the canvas's unscaled coordinate system.
The pointer position is therefore interpreted with the wrong scale and offset.
The progressive vertical offset explains why the error is more noticeable in
lower rows and why upper tracks can appear non-interactive.

**Impact:**

Interactive tooltips can identify the wrong datum, which is especially serious
for genomic plots where row and sample identity are the primary interpretation.

**Potential fix direction:**

Make pointer-coordinate conversion transform-aware by deriving the scale and
offset from the rendered canvas bounding rectangle, or expose an embed-safe
scaling mechanism that updates GenomeSpy's interaction coordinate system. A
documentation-side workaround is to avoid CSS transforms and use natural-size
rendering with scrolling, but that is less suitable for narrow responsive
layouts.

**Validation notes:**

The issue was reproduced after restoring transform-based fitting. Natural-size
rendering avoids the visual scaling mismatch but does not provide the desired
compact layout. Browser `zoom` was also attempted and caused broader rendering
regressions, so it is not currently the preferred workaround.
