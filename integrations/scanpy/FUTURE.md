# Remaining Scanpy coverage

This is a short handoff for work after the first integration release.
[STATUS.md](STATUS.md) owns progress and known issues; [PLAN.md](PLAN.md) owns
acceptance criteria. Keep detailed parameter contracts in
[COMPATIBILITY.md](COMPATIBILITY.md).

## Missing plot families

- Add `violin`, `stacked_violin` and `StackedViolin`, then their ranked-gene
  variants. Reuse expression access and ranking helpers. Filled shapes need
  released native support; do not carry prototype geometry into production.
- Add `rank_genes_groups_tracksplot` using the existing ranking and tracks helpers.
  Exact filled tracks remain separate from the supported per-cell bars.
- Add `spatial` when native image-backed views can support its images, coordinates
  and overlays. Keep the existing embedding helpers where their meanings match.

## Finish options on existing plots

- Close the remaining parameter and builder-method rows in STATUS. Priorities
  include storage limits, large heatmaps, graph options, normalization, typography,
  and delivery. Broader marker shapes can wait.
- Add Scanpy 1.12's group-specific dotplot colormaps. Keep unsupported forms
  explicit until implemented. Recheck Scanpy's automatic PAGA tree-layout bug.
- Review full plotting behavior, not just whether a function exists. Preserve
  source precedence, masks, categories, thresholds, supplied coordinates, cached
  results and mutation rules. Never silently rerun analysis.
- Keep Matplotlib figures, artists and global settings outside the native API.
  Full coverage means native equivalents for the agreed Scanpy plotting scope,
  with documented rendering differences; it does not mean emulating Matplotlib.

## GenomeSpy 1.3 adoption

Version 0.10.0 uses native PAGA rule outlines, linked embedding hover and
interactive legends. Multipanel legends highlight the same cells across panels.
EmbeddingSummary legends update every summary alongside its brush. Existing
gene dropdowns remain supported.
Documentation charts release their contexts when scrolled away and render again
on return. A physical-phone recheck is still useful.

Adaptive dendrograms keep index axes until Core can derive viewport heights from
categorical scales (C22). Preserve their current zoom behavior. A Figwig example
also needs a licensed, publicly hosted prepared file; keep the existing BigWig
inputs until then. Neither item needs a local substitute or a browser listener.

## Gates for extending support

Test data semantics independently, then complete charts and observed interactions.
Include sparse allocation, realistic memory use and notebook/HTML delivery.
Do not impose artificial cell, value or clustering-size caps. Improve preparation
and transport where measurements show a bottleneck.
Test supported Scanpy versions separately from the pinned reference environment.
Update the existing plan and status when a slice closes; remove obsolete working
notes after their useful findings have permanent homes. Keep generated evidence
and notebook outputs out of Git.
