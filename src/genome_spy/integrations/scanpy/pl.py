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

__all__ = ["dotplot", "matrixplot", "umap"]

_Bound = float | str | Sequence[float | str | None] | None


def _require_scanpy(context: str = "gsc.pl.umap") -> Any:
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
        "save": save is not None and save is not False,
    }
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
    for name in ("ax", "return_fig"):
        if name in kwargs:
            raise TypeError(
                f"gsc.pl.umap: {name} is omitted from the native API. "
                "Use show=False and the returned GenomeSpy chart."
            )
    for name, rejected in unsupported.items():
        if rejected:
            raise NotImplementedError(
                f"gsc.pl.umap (Scanpy 1.11.5): {name} is not supported yet. "
                "See the Scanpy integration support table."
            )
    aliases = {"s", "alpha", "edgecolor", "edgecolors", "linewidth", "linewidths"}
    unknown = kwargs.keys() - aliases
    if unknown:
        raise TypeError(
            f"gsc.pl.umap: unknown option(s): {', '.join(sorted(unknown))}."
        )
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
    for name, nullable in {"show": show, "frameon": frameon}.items():
        if nullable is not None and not isinstance(nullable, bool):
            raise TypeError(f"gsc.pl.umap: {name} must be boolean or None.")
    sc = _require_scanpy()
    if sc.settings.autosave and save is None:
        raise NotImplementedError(
            "gsc.pl.umap: automatic image saving is not supported yet; "
            "use save=False and chart.save('umap.html', inline=True)."
        )
    from genome_spy.integrations.scanpy._umap_data import prepare_umap
    from genome_spy.integrations.scanpy._umap_chart import build_umap
    from genome_spy.integrations.scanpy._umap_style import umap_style

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
    should_show = sc.settings.autoshow if show is None else show
    if should_show:
        chart.display()
        return None
    return chart


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
        dendrogram: Only False is supported until tree attachment is implemented.
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
    for name in ("ax", "return_fig"):
        if name in kwds:
            raise TypeError(
                f"gsc.pl.dotplot: {name} is omitted; use show=False and the native chart."
            )
    unknown = kwds.keys() - {"linewidth"}
    if unknown:
        raise TypeError(
            f"gsc.pl.dotplot: unsupported option(s): {', '.join(sorted(unknown))}."
        )
    for name, rejected in {
        "dendrogram": dendrogram is not False,
        "save": save is not None and save is not False,
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
    for name, nullable in {"show": show, "swap_axes": swap_axes}.items():
        if nullable is not None and not isinstance(nullable, bool):
            raise TypeError(f"gsc.pl.dotplot: {name} must be boolean or None.")
    if standard_scale not in (None, "var", "group"):
        raise ValueError(
            "gsc.pl.dotplot: standard_scale must be 'var', 'group', or None."
        )
    sc = _require_scanpy("gsc.pl.dotplot")
    if sc.settings.autosave and save is None:
        raise NotImplementedError(
            "gsc.pl.dotplot: automatic image saving is unsupported; use save=False."
        )
    from genome_spy.integrations.scanpy._grouped_data import (
        dotplot_statistics,
        grouped_expression,
    )
    from genome_spy.integrations.scanpy._dotplot_chart import build_dotplot

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
    colors, fractions = dotplot_statistics(
        prepared.values,
        expression_cutoff=expression_cutoff,
        mean_only_expressed=mean_only_expressed,
        standard_scale=standard_scale,
        dot_color_df=dot_color_df,
        swap_axes=bool(swap_axes),
    )
    chart = build_dotplot(
        colors,
        fractions,
        prepared.feature_groups,
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
        value_title=("Color value" if dot_color_df is not None else "Mean expression")
        + (" (scaled)" if standard_scale is not None else ""),
        linewidth=kwds.get("linewidth", 0.2),
        rotation=var_group_rotation,
        width=width,
        height=height,
        figsize=figsize,
    )
    if sc.settings.autoshow if show is None else show:
        chart.display()
        return None
    return chart


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
        dendrogram: Only False until tree attachment in M04.
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
    for name in ("ax", "return_fig"):
        if name in kwds:
            raise TypeError(
                f"{context}: {name} is omitted; use show=False and the native chart."
            )
    unknown = kwds.keys() - {"edgecolor", "linewidth"}
    if unknown:
        raise TypeError(
            f"{context}: unsupported option(s): {', '.join(sorted(unknown))}. "
            "Use scalar edgecolor and linewidth for tile edges."
        )
    for name, rejected in {
        "dendrogram": dendrogram is not False,
        "save": save is not None and save is not False,
        "vcenter": vcenter is not None,
        "norm": norm is not None,
    }.items():
        if rejected:
            raise NotImplementedError(f"{context}: {name} is not supported yet.")
    for name, value in {"log": log, "swap_axes": swap_axes, "hover": hover}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if show is not None and not isinstance(show, bool):
        raise TypeError(f"{context}: show must be boolean or None.")
    if standard_scale not in (None, "var", "group"):
        raise ValueError(f"{context}: standard_scale must be 'var', 'group', or None.")
    sc = _require_scanpy(context)
    if sc.settings.autosave and save is None:
        raise NotImplementedError(
            f"{context}: automatic image saving is unsupported; use save=False."
        )
    from genome_spy.integrations.scanpy._grouped_data import (
        grouped_expression,
        matrixplot_statistics,
    )
    from genome_spy.integrations.scanpy._matrixplot_chart import build_matrixplot

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
    colors = matrixplot_statistics(
        prepared.values,
        standard_scale=standard_scale,
        values_df=values_df,
        categories_order=categories_order,
        swap_axes=swap_axes,
    )
    chart = build_matrixplot(
        colors,
        prepared.feature_groups,
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
        value_title="Value"
        if values_df is not None
        else "Mean expression" + (" (scaled)" if standard_scale is not None else ""),
        width=width,
        height=height,
        figsize=figsize,
    )
    if sc.settings.autoshow if show is None else show:
        chart.display()
        return None
    return chart
