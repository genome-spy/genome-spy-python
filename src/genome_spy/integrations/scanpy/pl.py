"""Scanpy plotting entry points; analysis continues through Scanpy itself."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version
from math import isfinite
from numbers import Real
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from anndata import AnnData
    import pandas as pd

    from genome_spy import Parameter, TopLevelSpec

__all__ = ["correlation_matrix", "dendrogram", "dotplot", "matrixplot", "umap"]

_Bound = float | str | Sequence[float | str | None] | None


def _require_scanpy(context: str = "gsc.pl.umap") -> Any:
    """Return the supported Scanpy module, or raise an error naming the plotting call.

    Delay the optional import until a plot is requested to keep base imports light.
    """
    try:
        installed = version("scanpy")
    except PackageNotFoundError as error:
        raise ImportError(
            f"{context} requires genome-spy-python[scanpy] (Scanpy 1.11.5)."
        ) from error
    if installed != "1.11.5":
        raise ImportError(
            f"{context} supports Scanpy 1.11.5; found {installed}. "
            "Install genome-spy-python[scanpy]."
        )
    import scanpy

    return scanpy


def _check_kwargs(
    options: Mapping[str, Any], allowed: set[str], *, context: str
) -> None:
    """Check forwarded options against allowed names; raise a contextual error if invalid.

    Reject Matplotlib-only options explicitly rather than silently dropping them.
    """
    for name in ("ax", "return_fig"):
        if name in options:
            raise TypeError(
                f"{context}: {name} is omitted; use show=False and the native chart."
            )
    unknown = options.keys() - allowed
    if unknown:
        raise TypeError(
            f"{context}: unsupported option(s): {', '.join(sorted(unknown))}."
        )


def _prepare_plot(show: bool | None, save: str | bool | None, *, context: str) -> Any:
    """Check show/save and return Scanpy, rejecting automatic image saving early."""
    if show is not None and not isinstance(show, bool):
        raise TypeError(f"{context}: show must be boolean or None.")
    if save is not None and save is not False:
        raise NotImplementedError(
            f"{context}: save supports only None/False; use native chart.save for HTML/JSON."
        )
    sc = _require_scanpy(context)
    if sc.settings.autosave and save is None:
        raise NotImplementedError(
            f"{context}: automatic image saving is unsupported; use save=False."
        )
    return sc


def _finish_plot(
    chart: TopLevelSpec, show: bool | None, sc: Any
) -> TopLevelSpec | None:
    """Use show or Scanpy's setting to display the chart or return it.

    Displaying returns None so a notebook does not produce a second chart output.
    """
    should_show = sc.settings.autoshow if show is None else show
    if should_show:
        chart.display()
        return None
    return chart


def umap(
    adata: AnnData,
    *,
    color: str | Sequence[str] | None = None,
    mask_obs: Any = None,
    gene_symbols: str | None = None,
    use_raw: bool | None = None,
    sort_order: bool = True,
    edges: bool = False,
    edges_width: float = 0.1,
    edges_color: Any = "grey",
    neighbors_key: str | None = None,
    arrows: bool = False,
    arrows_kwds: Mapping[str, Any] | None = None,
    groups: str | Sequence[str] | None = None,
    components: str | Sequence[str] | None = None,
    dimensions: tuple[int, int] | Sequence[tuple[int, int]] | None = None,
    layer: str | None = None,
    projection: Literal["2d", "3d"] = "2d",
    scale_factor: float | None = None,
    color_map: Any = None,
    cmap: Any = None,
    palette: Any = None,
    na_color: Any = "lightgray",
    na_in_legend: bool = True,
    size: float | Sequence[float] | None = None,
    frameon: bool | None = None,
    legend_fontsize: float | str | None = None,
    legend_fontweight: int | str = "bold",
    legend_loc: str | None = "right margin",
    legend_fontoutline: int | None = None,
    colorbar_loc: str | None = "right",
    vmax: _Bound = None,
    vmin: _Bound = None,
    vcenter: Any = None,
    norm: Any = None,
    add_outline: bool | None = False,
    outline_width: tuple[float, float] = (0.3, 0.05),
    outline_color: tuple[str, str] = ("black", "white"),
    ncols: int = 4,
    hspace: float = 0.25,
    wspace: float | None = None,
    title: str | Sequence[str] | None = None,
    show: bool | None = None,
    save: bool | str | None = None,
    marker: str | Sequence[str] = ".",
    hover: bool = True,
    zoom: bool = False,
    selection: Parameter | None = None,
    obs_id: str | None = None,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Plot existing UMAP coordinates with Scanpy-compatible color semantics.

    Description:
        Supports Scanpy 1.11.5 categorical and continuous 2D UMAP, including
        multiple panels, selected raw/layer genes, palettes, masks, per-cell
        sizes, color sorting, and percentile bounds. Data preparation happens
        in Python without modifying AnnData or computing an embedding. The
        result is a native GenomeSpy chart, displayed through anywidget.
        Matplotlib object parameters ``ax`` and ``return_fig`` are omitted.
        See the Scanpy integration guide for the complete support table.

    Args:
        adata: AnnData with existing ``umap`` or ``X_umap`` coordinates.
        color: Observation or gene keys, one per panel; None uses na_color.
        mask_obs: Boolean observation mask or observation-column key. Masks
            affect coloring, retaining all coordinates.
        gene_symbols: Variable column used to resolve gene symbols.
        use_raw: Use raw when present by default, unless a layer is selected.
        sort_order: Draw larger continuous values last, following Scanpy ties.
        edges: Graph edges; currently only False is supported.
        edges_width: Reserved upstream edge width.
        edges_color: Reserved upstream edge color.
        neighbors_key: Reserved upstream graph key.
        arrows: Graph arrows; currently only False is supported.
        arrows_kwds: Reserved upstream arrow options.
        groups: Categorical groups to color; other observations remain visible.
        components: One-based component pairs, or "all".
        dimensions: Zero-based component pairs; mutually exclusive with components.
        layer: Expression layer, mutually exclusive with use_raw=True.
        projection: Currently only "2d" is supported.
        scale_factor: Reserved upstream spatial scaling option.
        color_map: Alias for cmap, mutually exclusive with it.
        cmap: GenomeSpy color scheme name; defaults to "viridis".
        palette: Native scheme name, CSS color sequence, or category-to-color mapping.
        na_color: Color for missing or masked values.
        na_in_legend: Include a missing-category legend entry.
        size: Marker area in points squared, scalar or one value per observation.
        frameon: Show axes and frame; defaults to Scanpy's frame setting.
        legend_fontsize: Legend/annotation font size in points or relative name.
        legend_fontweight: Weight of on-data category labels; currently normal
            (400) only, as other weights require an unbundled font atlas.
        legend_loc: "right margin", "on data", "none", or None.
        legend_fontoutline: Label halos are not yet supported.
        colorbar_loc: Currently "right" or None.
        vmax: Numeric or percentile upper color bound, optionally per panel.
        vmin: Numeric or percentile lower color bound, optionally per panel.
        vcenter: Custom centers are not yet supported.
        norm: Custom normalization is not yet supported.
        add_outline: Cluster outlines are not yet supported.
        outline_width: Reserved upstream outline widths.
        outline_color: Reserved upstream outline colors.
        ncols: Maximum number of panel columns.
        hspace: Relative vertical panel spacing.
        wspace: Relative horizontal panel spacing.
        title: Panel titles, defaulting to color keys.
        show: Display and return None when True; return a chart when False.
            None uses Scanpy settings.autoshow.
        save: Image saving is not yet supported; use native HTML/JSON save.
        marker: Dot (".") or circle ("o"), optionally per panel.
        hover: Enable record/value tooltips without changing initial appearance.
        zoom: Enable coordinate navigation, shared across panels.
        selection: Native ``gs.selection_interval(..., encodings=["x", "y"])``.
            Brush in the first panel to highlight matching coordinates in all
            panels and show a native selected-cell count. Requires the same
            dimension pair in every panel.
            Point selections are not yet supported.
        obs_id: Unique nonmissing observation-column key, defaulting to obs_names
            or distinct snapshot-local row keys when names repeat.
        width: GenomeSpy plot-area width per panel in logical pixels. None
            uses 300 pixels. Axes and guides add space.
        height: GenomeSpy plot-area height per panel in logical pixels. None
            uses 300 pixels. Does not resize markers/fonts.
        **kwargs: Supported scatter aliases: s, alpha, edgecolor/edgecolors,
            linewidth/linewidths. Other options fail before data extraction.

    Returns:
        A native chart/composition when show=False, otherwise None.

    Raises:
        ImportError: If the optional dependency/version is unavailable.
        TypeError: If an argument or source type is invalid.
        ValueError: If requested data, sizes, masks, or bounds are invalid.
        NotImplementedError: If a recognized plotting option is unsupported.

    Example:
        >>> import genome_spy.integrations.scanpy as gsc
        >>> chart = gsc.pl.umap(adata, color=["cell_type", "MS4A1"], show=False)
        >>> chart.save("umap.html", inline=True)
    """
    # Accept Scanpy defaults, but reject options we cannot render faithfully.
    unsupported = {
        "edges": edges is not False,
        "edges_width": edges_width != 0.1,
        "edges_color": not isinstance(edges_color, str) or edges_color != "grey",
        "neighbors_key": neighbors_key is not None,
        "arrows": arrows is not False,
        "arrows_kwds": arrows_kwds is not None,
        "projection": projection != "2d",
        "scale_factor": scale_factor is not None,
        "legend_fontoutline": legend_fontoutline is not None,
        "legend_fontweight": legend_loc == "on data"
        and legend_fontweight not in (400, "normal", "regular"),
        "legend_loc": legend_loc not in (None, "none", "right margin", "on data"),
        "colorbar_loc": colorbar_loc not in (None, "right"),
        "vcenter": vcenter is not None,
        "norm": norm is not None,
        "add_outline": add_outline not in (False, None),
        "outline_width": outline_width != (0.3, 0.05),
        "outline_color": outline_color != ("black", "white"),
    }

    # Linked panels must share one brush over the same two coordinates.
    if selection is not None:
        from genome_spy import Parameter

        if not isinstance(selection, Parameter):
            raise TypeError("gsc.pl.umap: selection must be a GenomeSpy parameter.")
        definition = selection.param.to_dict()
        config = definition.get("select")
        if not isinstance(config, dict) or config.get("type") != "interval":
            raise NotImplementedError(
                "gsc.pl.umap: selection currently supports x/y interval brushing; "
                "point selections are not supported yet."
            )
        if sorted(config.get("encodings", [])) != ["x", "y"]:
            raise NotImplementedError(
                "gsc.pl.umap: selection requires encodings=['x', 'y']."
            )
        if "push" in definition or "value" in definition:
            raise NotImplementedError(
                "gsc.pl.umap: selection push and initial value are not supported; "
                "the adapter owns the shared brush scope."
            )
    for name, rejected in unsupported.items():
        if rejected:
            raise NotImplementedError(
                f"gsc.pl.umap (Scanpy 1.11.5): {name} is not supported yet. "
                "See the Scanpy integration support table."
            )
    _check_kwargs(
        kwargs,
        {"s", "alpha", "edgecolor", "edgecolors", "linewidth", "linewidths"},
        context="gsc.pl.umap",
    )

    # Resolve alternate argument names before reading data.
    for left, right in [("edgecolor", "edgecolors"), ("linewidth", "linewidths")]:
        if left in kwargs and right in kwargs:
            raise TypeError(f"gsc.pl.umap: pass only one of {left} and {right}.")
    if "s" in kwargs:
        if size is not None:
            raise TypeError("gsc.pl.umap: pass only one of size and s.")
        size = kwargs["s"]
    if color_map is not None and cmap is not None:
        raise ValueError("gsc.pl.umap: cannot specify both color_map and cmap.")
    if groups is not None and mask_obs is not None:
        raise ValueError("gsc.pl.umap: groups and mask_obs are incompatible.")

    # Check basic options before loading the optional Scanpy dependency.
    for name, dimension in {"width": width, "height": height}.items():
        if dimension is not None and (
            isinstance(dimension, bool)
            or not isinstance(dimension, Real)
            or not isfinite(dimension)
            or dimension <= 0
        ):
            raise ValueError(
                f"gsc.pl.umap: {name} must be a positive finite number or None."
            )
    for name, option in {
        "sort_order": sort_order,
        "na_in_legend": na_in_legend,
        "hover": hover,
        "zoom": zoom,
    }.items():
        if not isinstance(option, bool):
            raise TypeError(f"gsc.pl.umap: {name} must be boolean.")
    if frameon is not None and not isinstance(frameon, bool):
        raise TypeError("gsc.pl.umap: frameon must be boolean or None.")
    sc = _prepare_plot(show, save, context="gsc.pl.umap")
    from genome_spy.integrations.scanpy._umap_data import prepare_umap
    from genome_spy.integrations.scanpy._umap_chart import build_umap
    from genome_spy.integrations.scanpy._style import umap_style

    # Read existing coordinates and colors without running analysis.
    prepared = prepare_umap(
        adata,
        color=color,
        mask_obs=mask_obs,
        gene_symbols=gene_symbols,
        use_raw=use_raw,
        layer=layer,
        groups=groups,
        components=components,
        dimensions=dimensions,
        size=size,
        marker=marker,
        palette=palette,
        cmap=cmap if color_map is None else color_map,
        na_color=na_color,
        na_in_legend=na_in_legend,
        sort_order=sort_order,
        vmin=vmin,
        vmax=vmax,
        title=title,
        obs_id=obs_id,
        colorbar_loc=colorbar_loc,
    )

    # Keep appearance separate from the selected data.
    style = umap_style(
        count=len(prepared.panels),
        width=width,
        height=height,
        frameon=sc.settings._frameon if frameon is None else frameon,
        legend_loc=legend_loc,
        colorbar_loc=colorbar_loc,
        legend_fontsize=legend_fontsize,
        ncols=ncols,
        hspace=hspace,
        wspace=wspace,
        alpha=kwargs.get("alpha"),
        edgecolor=kwargs.get("edgecolor", kwargs.get("edgecolors", "none")),
        linewidth=kwargs.get("linewidth", kwargs.get("linewidths")),
        na_color=na_color,
    )
    chart = build_umap(prepared, style, hover=hover, zoom=zoom, selection=selection)
    return _finish_plot(chart, show, sc)


def dotplot(
    adata: AnnData,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str | Sequence[str],
    *,
    use_raw: bool | None = None,
    log: bool = False,
    num_categories: int = 7,
    categories_order: Sequence[str] | None = None,
    expression_cutoff: float = 0.0,
    mean_only_expressed: bool = False,
    standard_scale: Literal["var", "group"] | None = None,
    title: str | None = None,
    colorbar_title: str | None = "Mean expression\nin group",
    size_title: str | None = "Fraction of cells\nin group (%)",
    figsize: tuple[float, float] | None = None,
    dendrogram: bool | str = False,
    gene_symbols: str | None = None,
    var_group_positions: Sequence[tuple[int, int]] | None = None,
    var_group_labels: Sequence[str] | None = None,
    var_group_rotation: float | None = None,
    layer: str | None = None,
    swap_axes: bool | None = False,
    dot_color_df: pd.DataFrame | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    vcenter: float | None = None,
    norm: Any = None,
    cmap: Any = "Reds",
    dot_max: float | None = None,
    dot_min: float | None = None,
    smallest_dot: float = 0.0,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot grouped mean expression and the fraction of expressing cells.

    Reads selected values through Scanpy's public getter and computes detached
    summaries in Python. GenomeSpy renders the dots, labels, brackets and guides.
    No analysis, AnnData mutation, or Matplotlib rendering occurs.

    Args:
        adata: AnnData containing expression and grouping annotations.
        var_names: Feature keys, repeated slots, or labeled feature groups.
        groupby: Observation key or categorical grouping keys.
        use_raw: Use raw by default when available; layer overrides that default.
        log: Apply log1p before calculating means and expression fractions.
        num_categories: Number of bins for numeric grouping annotations.
        categories_order: Complete order of the grouping categories.
        expression_cutoff: Strict lower threshold for an expressed value.
        mean_only_expressed: Average only expressed values, with empty means zero.
        standard_scale: Min–max scale means per variable or group.
        title: Plot title.
        colorbar_title: Color guide title; None removes its title.
        size_title: Percentage guide title; None removes its title.
        figsize: Native layout budget in inches at 100 logical pixels/inch.
            Width includes a fixed 150-pixel guide allowance; height sizes the
            plot area. Labels and renderer padding add space. Cannot be combined
            with width or height. No Matplotlib settings are consulted.
        dendrogram: Attach a stored Scanpy tree or compute one through Scanpy.
            True uses the default cache key; a string selects another key.
        gene_symbols: Variable annotation column for symbol lookup.
        var_group_positions: Inclusive feature-slot bracket endpoints.
        var_group_labels: Bracket labels; mappings already supply these.
        var_group_rotation: Bracket label rotation in degrees.
        layer: Expression layer instead of the automatic raw/X source.
        swap_axes: Place groups on x and features on y.
        dot_color_df: Authoritative labeled colors; scaling follows Scanpy 1.11.5.
        show: Display once, return the chart when False, or use Scanpy autoshow.
        save: Only inactive None/False; use the returned chart's HTML/JSON saving.
        vmin: Numeric lower color bound.
        vmax: Numeric upper color bound.
        vcenter: Reserved; nondefault values error.
        norm: Reserved; Matplotlib normalization objects error.
        cmap: GenomeSpy scheme name; the default Reds selects native reds.
        dot_max: Upper clipped fraction, or the observed maximum rounded up to 0.1.
        dot_min: Lower clipped fraction, default zero.
        smallest_dot: Minimum dot area in points squared; maximum is 200.
        hover: Show gene, group, displayed color value and expressing percentage.
        width: Native plot-area width in logical pixels, default 37 per column.
        height: Native plot-area height in logical pixels, default 35 per row.
        **kwds: Only scalar linewidth is supported; other scatter options error.

    Returns:
        A detached native chart when show=False, otherwise None.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If input types or forwarded options are invalid.
        ValueError: If groups, supplied labels, bounds or sizes are invalid.
        NotImplementedError: If a rendering option is unsupported.

    Example:
        >>> chart = gsc.pl.dotplot(pbmc, ["CD79A", "CD3D"], "louvain", show=False)
        >>> chart.save("markers.html", inline=True)
    """
    # Reject unsupported options before reading AnnData.
    _check_kwargs(kwds, {"linewidth"}, context="gsc.pl.dotplot")
    if not isinstance(dendrogram, (bool, str)) or dendrogram == "":
        raise TypeError(
            "gsc.pl.dotplot: dendrogram must be False, True, or a nonempty cache key."
        )
    for name, rejected in {
        "vcenter": vcenter is not None,
        "norm": norm is not None,
    }.items():
        if rejected:
            raise NotImplementedError(f"gsc.pl.dotplot: {name} is not supported yet.")
    for name, value in {
        "log": log,
        "mean_only_expressed": mean_only_expressed,
        "hover": hover,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"gsc.pl.dotplot: {name} must be boolean.")
    if swap_axes is not None and not isinstance(swap_axes, bool):
        raise TypeError("gsc.pl.dotplot: swap_axes must be boolean or None.")
    if standard_scale not in (None, "var", "group"):
        raise ValueError(
            "gsc.pl.dotplot: standard_scale must be 'var', 'group', or None."
        )
    sc = _prepare_plot(show, save, context="gsc.pl.dotplot")
    from genome_spy.integrations.scanpy._dendrogram_data import (
        attached_dendrogram,
        reorder_grouped,
    )
    from genome_spy.integrations.scanpy._grouped_data import (
        dotplot_statistics,
        grouped_expression,
    )
    from genome_spy.integrations.scanpy._dotplot_chart import build_dotplot

    # Read only the requested genes and group labels.
    prepared = grouped_expression(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log,
        num_categories=num_categories,
        categories_order=categories_order,
        gene_symbols=gene_symbols,
        layer=layer,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
    )

    # Dot color and area use different summaries of the same cells.
    colors, fractions = dotplot_statistics(
        prepared.values,
        expression_cutoff=expression_cutoff,
        mean_only_expressed=mean_only_expressed,
        standard_scale=standard_scale,
        dot_color_df=dot_color_df,
        swap_axes=bool(swap_axes),
    )

    # Keep colors, sizes and marker brackets in the tree's leaf order.
    feature_groups = prepared.feature_groups
    count = colors.shape[1] if swap_axes else colors.shape[0]
    tree = attached_dendrogram(adata, groupby, dendrogram, count)
    if tree is not None:
        colors, feature_groups, slots = reorder_grouped(
            tree, colors, feature_groups, swapped=bool(swap_axes)
        )
        fractions = (
            fractions.loc[:, list(tree.order)].iloc[slots, :]
            if swap_axes
            else fractions.loc[list(tree.order)].iloc[:, slots]
        )

    # Describe the displayed values accurately when means are replaced or scaled.
    value_title = "Color value" if dot_color_df is not None else "Mean expression"
    if standard_scale is not None:
        value_title += " (scaled)"
    chart = build_dotplot(
        colors,
        fractions,
        feature_groups,
        swap_axes=bool(swap_axes),
        title=title,
        colorbar_title=colorbar_title,
        size_title=size_title,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        dot_min=dot_min,
        dot_max=dot_max,
        smallest_dot=smallest_dot,
        hover=hover,
        value_title=value_title,
        linewidth=kwds.get("linewidth", 0.2),
        rotation=var_group_rotation,
        width=width,
        height=height,
        figsize=figsize,
        tree=tree,
    )
    return _finish_plot(chart, show, sc)


def matrixplot(
    adata: AnnData,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str | Sequence[str],
    *,
    use_raw: bool | None = None,
    log: bool = False,
    num_categories: int = 7,
    categories_order: Sequence[str] | None = None,
    figsize: tuple[float, float] | None = None,
    dendrogram: bool | str = False,
    title: str | None = None,
    cmap: Any = "viridis",
    colorbar_title: str | None = "Mean expression\nin group",
    gene_symbols: str | None = None,
    var_group_positions: Sequence[tuple[int, int]] | None = None,
    var_group_labels: Sequence[str] | None = None,
    var_group_rotation: float | None = None,
    layer: str | None = None,
    standard_scale: Literal["var", "group"] | None = None,
    values_df: pd.DataFrame | None = None,
    swap_axes: bool = False,
    show: bool | None = None,
    save: str | bool | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    vcenter: float | None = None,
    norm: Any = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot group mean expression as native GenomeSpy tiles.

    Selected-data access, means and scaling run in Python, without modifying
    AnnData or invoking analysis. Chart construction shares dotplot's native
    slots, labels and brackets. Supplied values bypass aggregation and scaling.

    Args:
        adata: AnnData with expression and grouping annotations.
        var_names: Feature keys, repeated slots, or labeled feature groups.
        groupby: Observation key or categorical grouping keys.
        use_raw: Use raw by default when available; layer overrides that default.
        log: Apply log1p before computing means; ignored for supplied values_df.
        num_categories: Number of bins for numeric grouping annotations.
        categories_order: Complete category order, also applied to values_df rows.
        figsize: Native layout budget in inches at 100 logical pixels/inch.
            Width includes a 150-pixel guide allowance; height sizes the plot
            area. Labels and padding add space. Conflicts with width/height.
        dendrogram: True or a cache key attaches a Python-computed group tree.
        title: Plot title.
        cmap: GenomeSpy color scheme name; None uses viridis.
        colorbar_title: Color guide title; None removes its title.
        gene_symbols: Variable annotation column for symbol lookup.
        var_group_positions: Inclusive feature-slot bracket endpoints.
        var_group_labels: Bracket labels; mappings supply these directly.
        var_group_rotation: Bracket label rotation in degrees.
        layer: Expression layer instead of the automatic raw/X source.
        standard_scale: Min–max scale computed means per variable or group,
            once before swapping axes. Constant ranges become zero.
            Supplied values_df is never scaled.
        values_df: Authoritative numeric table with exactly the plotted labels
            and feature multiplicities. Retains its row/column order unless
            categories_order reorders rows. Duplicate group labels error.
        swap_axes: Place groups on x and features on y.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: Only inactive None/False; use native chart HTML/JSON saving.
        vmin: Finite numeric lower color bound.
        vmax: Finite numeric upper color bound.
        vcenter: Reserved; nondefault values error.
        norm: Reserved; Matplotlib normalization objects error.
        hover: Show gene, group and displayed mean or supplied value.
        width: Plot-area logical pixels, default 37 per feature column.
        height: Plot-area logical pixels, default 35 per group row.
        **kwds: Scalar edgecolor and linewidth. Defaults are gray edges at 0.1
            points; edgecolor="none" removes edges. Plural aliases and all
            other pcolor options error.

    Returns:
        A detached native chart when show=False, otherwise None.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If input types or forwarded options are invalid.
        ValueError: If groups, table labels, bounds or dimensions are invalid.
        NotImplementedError: If a rendering option is unsupported.

    Example:
        >>> chart = gsc.pl.matrixplot(
        ...     pbmc, ["CD79A", "CD3D"], "bulk_labels",
        ...     standard_scale="var", show=False,
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.matrixplot"
    # Reject unsupported options before reading AnnData.
    _check_kwargs(kwds, {"edgecolor", "linewidth"}, context="gsc.pl.matrixplot")
    if not isinstance(dendrogram, (bool, str)) or dendrogram == "":
        raise TypeError(
            "gsc.pl.matrixplot: dendrogram must be False, True, or a nonempty cache key."
        )
    for name, rejected in {
        "vcenter": vcenter is not None,
        "norm": norm is not None,
    }.items():
        if rejected:
            raise NotImplementedError(f"{context}: {name} is not supported yet.")
    for name, value in {"log": log, "swap_axes": swap_axes, "hover": hover}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if standard_scale not in (None, "var", "group"):
        raise ValueError(f"{context}: standard_scale must be 'var', 'group', or None.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._dendrogram_data import (
        attached_dendrogram,
        reorder_grouped,
    )
    from genome_spy.integrations.scanpy._grouped_data import (
        grouped_expression,
        matrixplot_statistics,
    )
    from genome_spy.integrations.scanpy._matrixplot_chart import build_matrixplot

    # Supplied means replace expression values, so do not log-transform them.
    prepared = grouped_expression(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log if values_df is None else False,
        num_categories=num_categories,
        categories_order=categories_order,
        gene_symbols=gene_symbols,
        layer=layer,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
    )

    # Compute means once, or keep the user's supplied summary table.
    colors = matrixplot_statistics(
        prepared.values,
        standard_scale=standard_scale,
        values_df=values_df,
        categories_order=categories_order,
        swap_axes=swap_axes,
    )

    # Move the group rows and matching marker brackets together.
    feature_groups = prepared.feature_groups
    count = colors.shape[1] if swap_axes else colors.shape[0]
    tree = attached_dendrogram(adata, groupby, dendrogram, count)
    if tree is not None:
        colors, feature_groups, _ = reorder_grouped(
            tree, colors, feature_groups, swapped=bool(swap_axes)
        )

    # Supplied values keep their meaning even when standard_scale is requested.
    value_title = "Value" if values_df is not None else "Mean expression"
    if values_df is None and standard_scale is not None:
        value_title += " (scaled)"
    chart = build_matrixplot(
        colors,
        feature_groups,
        swap_axes=swap_axes,
        title=title,
        colorbar_title=colorbar_title,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        edgecolor=kwds.get("edgecolor", "gray"),
        linewidth=kwds.get("linewidth", 0.1),
        rotation=var_group_rotation,
        hover=hover,
        value_title=value_title,
        width=width,
        height=height,
        figsize=figsize,
        tree=tree,
    )
    return _finish_plot(chart, show, sc)


def dendrogram(
    adata: AnnData,
    groupby: str,
    *,
    dendrogram_key: str | None = None,
    orientation: Literal["top", "bottom", "left", "right"] = "top",
    remove_labels: bool = False,
    show: bool | None = None,
    save: str | bool | None = None,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Render group linkage computed in Python with native GenomeSpy rules.

    Read the geometry and order stored by sc.tl.dendrogram. Missing trees delegate
    to that public computation with inplace=False, using resident dense X for
    small matrices or existing dense X_pca otherwise. Plotting never fits PCA,
    writes a cache or recomputes an existing result. Recompute explicitly in
    Scanpy after changing the data or grouping.

    Args:
        adata: AnnData with categorical groups and an existing representation.
        groupby: Categorical observation key; categorical key sequences also work.
        dendrogram_key: Stored uns key, default dendrogram_<groupby>.
            Missing keys compute through Scanpy without writing to AnnData.
        orientation: Top, bottom, left or right tree orientation.
        remove_labels: Hide leaf labels while preserving leaf geometry.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: Only inactive None/False; use native chart HTML/JSON saving.
        width: Native plot-area width in logical pixels, default 300.
        height: Native plot-area height in logical pixels, default 300.

    Returns:
        A detached native chart when show=False, otherwise None.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If options or representation storage are unsupported.
        ValueError: If groups, profiles, cache or dimensions are invalid.
        NotImplementedError: If image saving is requested.

    Example:
        >>> chart = gsc.pl.dendrogram(pbmc, "bulk_labels", show=False)
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.dendrogram"
    if orientation not in ("top", "bottom", "left", "right"):
        raise ValueError(f"{context}: orientation must be top, bottom, left or right.")
    if not isinstance(remove_labels, bool):
        raise TypeError(f"{context}: remove_labels must be boolean.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._dendrogram_data import prepare_dendrogram
    from genome_spy.integrations.scanpy._dendrogram_chart import build_dendrogram

    # Reuse a stored tree; only a missing result is computed by Scanpy.
    tree = prepare_dendrogram(adata, groupby, dendrogram_key)
    chart = build_dendrogram(
        tree,
        orientation=orientation,
        remove_labels=remove_labels,
        width=width,
        height=height,
    )
    return _finish_plot(chart, show, sc)


def correlation_matrix(
    adata: AnnData,
    groupby: str,
    *,
    show_correlation_numbers: bool = False,
    dendrogram: bool | str | None = None,
    figsize: tuple[float, float] | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    vcenter: float | None = None,
    norm: Any = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot Python-computed group correlations with an optional aligned tree.

    Reuses Scanpy's stored dendrogram correlations and returns native tiles, labels,
    numbers and rules. Correlations come from the tree's representation, not the
    selected markers of a dotplot or matrixplot. No embedding, PCA, gene ranking
    or cache writes run. Missing trees delegate to sc.tl.dendrogram with a guard
    against hidden PCA; existing results are never recomputed.

    Args:
        adata: AnnData with categorical groups and an existing representation.
        groupby: Categorical observation key.
        show_correlation_numbers: Label each tile with two decimal places.
        dendrogram: None/True attaches a left tree and orders both axes by leaves.
            A string selects its cache key. False retains category order without
            drawing the tree; correlations still use the tree computation.
        figsize: Native budget in inches at 100 logical pixels/inch, subtracting
            180 pixels for an attached tree and 20 for the color guide. Labels
            and padding add space. Conflicts with width/height.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: Only inactive None/False; use native chart HTML/JSON saving.
        vmin: Numeric lower color bound; defaults to -1 if both bounds are absent.
        vmax: Numeric upper color bound; defaults to 1 if both bounds are absent.
        vcenter: Reserved; nondefault values error.
        norm: Reserved; Matplotlib normalization objects error.
        hover: Show the row group, column group and exact correlation.
        width: Tile plot-area width, default 60 logical pixels per group.
        height: Tile plot-area height, default 60 logical pixels per group.
        **kwds: Native cmap, scalar edgecolors and linewidth. Default colors
            use reversed native redblue for negative-blue/positive-red values.
            Edges are black at 0.01 points, hidden above 30 groups.

    Returns:
        A detached native chart when show=False, otherwise None.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If options or representation storage are unsupported.
        ValueError: If groups, profiles, cache or dimensions are invalid.
        NotImplementedError: If a rendering option is unsupported.

    Example:
        >>> chart = gsc.pl.correlation_matrix(
        ...     pbmc, "bulk_labels", show_correlation_numbers=True, show=False
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.correlation_matrix"
    # Reject unsupported options before reading AnnData.
    _check_kwargs(
        kwds, {"cmap", "edgecolors", "linewidth"}, context="gsc.pl.correlation_matrix"
    )
    for name, rejected in {
        "vcenter": vcenter is not None,
        "norm": norm is not None,
    }.items():
        if rejected:
            raise NotImplementedError(f"{context}: {name} is not supported yet.")
    for name, value in {
        "show_correlation_numbers": show_correlation_numbers,
        "hover": hover,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if dendrogram is not None and (
        not isinstance(dendrogram, (bool, str)) or dendrogram == ""
    ):
        raise TypeError(
            f"{context}: dendrogram must be None, False, True or a nonempty cache key."
        )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._dendrogram_data import prepare_dendrogram
    from genome_spy.integrations.scanpy._correlation_chart import (
        build_correlation_matrix,
    )

    # The Scanpy tree result also supplies the correlations, even without branches.
    tree = prepare_dendrogram(
        adata, groupby, dendrogram if isinstance(dendrogram, str) else None
    )
    chart = build_correlation_matrix(
        tree,
        dendrogram=dendrogram is not False,
        numbers=show_correlation_numbers,
        cmap=kwds.get("cmap"),
        edgecolors=kwds.get("edgecolors"),
        linewidth=kwds.get("linewidth", 0.01),
        vmin=vmin,
        vmax=vmax,
        hover=hover,
        width=width,
        height=height,
        figsize=figsize,
    )
    return _finish_plot(chart, show, sc)
