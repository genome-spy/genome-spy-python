"""Scanpy plotting entry points; analysis continues through Scanpy itself."""

from __future__ import annotations

from collections.abc import Callable, Collection, Mapping, Sequence
from numbers import Integral
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Literal

from genome_spy.integrations.scanpy._dotplot_builder import DotPlot
from genome_spy.integrations.scanpy._matrixplot_builder import MatrixPlot
from genome_spy.integrations.scanpy._guards import (
    _check_grid_zoom,
    _check_kwargs,
    _check_point_options,
    _require_scanpy,
)

if TYPE_CHECKING:
    from anndata import AnnData
    from numpy.typing import ArrayLike
    import numpy as np
    import pandas as pd

    from genome_spy import Parameter, TopLevelSpec

__all__ = [
    "DotPlot",
    "MatrixPlot",
    "clustermap",
    "correlation_matrix",
    "dendrogram",
    "dotplot",
    "heatmap",
    "tracksplot",
    "matrix",
    "timeseries_as_heatmap",
    "timeseries",
    "timeseries_subplot",
    "sim",
    "dpt_groups_pseudotime",
    "dpt_timeseries",
    "paga",
    "paga_adjacency",
    "paga_compare",
    "paga_path",
    "matrixplot",
    "ranking",
    "rank_genes_groups",
    "rank_genes_groups_dotplot",
    "rank_genes_groups_matrixplot",
    "rank_genes_groups_heatmap",
    "umap",
    "embedding",
    "tsne",
    "diffmap",
    "draw_graph",
    "pca",
    "pca_scatter",
    "pca_loadings",
    "pca_variance_ratio",
    "pca_overview",
    "scatter",
    "highly_variable_genes",
    "filter_genes_dispersion",
    "highest_expr_genes",
    "scrublet_score_distribution",
    "embedding_density",
]

_BoundValue = float | str | Callable[[Any], float]
_Bound = _BoundValue | Sequence[_BoundValue | None] | None


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


def _embedding(
    adata: AnnData,
    basis: str,
    context: str,
    annotate_var_explained: bool,
    /,
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
    vcenter: _Bound = None,
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
    """Validate shared embedding options, then prepare and render stored coordinates."""
    if not isinstance(annotate_var_explained, bool):
        raise TypeError(f"{context}: annotate_var_explained must be boolean.")
    # Accept Scanpy defaults, but reject options we cannot render faithfully.
    unsupported = {
        "arrows": arrows is not False,
        "arrows_kwds": arrows_kwds is not None,
        "projection": projection != "2d",
        "scale_factor": scale_factor is not None,
        "legend_fontoutline": legend_fontoutline is not None,
        "legend_fontweight": legend_loc == "on data"
        and legend_fontweight not in (400, "normal", "regular"),
        "legend_loc": legend_loc not in (None, "none", "right margin", "on data"),
        "colorbar_loc": colorbar_loc not in (None, "right", "left", "top", "bottom"),
        "norm": norm is not None,
    }

    # Linked panels must share one brush over the same two coordinates.
    if selection is not None:
        from genome_spy import Parameter

        if not isinstance(selection, Parameter):
            raise TypeError(f"{context}: selection must be a GenomeSpy parameter.")
        definition = selection.param.to_dict()
        config = definition.get("select")
        if not isinstance(config, dict) or config.get("type") != "interval":
            raise NotImplementedError(
                f"{context}: selection currently supports x/y interval brushing; "
                "point selections are not supported yet."
            )
        if sorted(config.get("encodings", [])) != ["x", "y"]:
            raise NotImplementedError(
                f"{context}: selection requires encodings=['x', 'y']."
            )
        if "push" in definition or "value" in definition:
            raise NotImplementedError(
                f"{context}: selection push and initial value are not supported; "
                "the adapter owns the shared brush scope."
            )
    for name, rejected in unsupported.items():
        if rejected:
            raise NotImplementedError(
                f"{context} (Scanpy 1.11.5): {name} is not supported yet. "
                "See the Scanpy integration support table."
            )
    _check_kwargs(
        kwargs,
        {"s", "alpha", "edgecolor", "edgecolors", "linewidth", "linewidths"},
        context=context,
    )

    # Resolve alternate argument names before reading data.
    for left, right in [("edgecolor", "edgecolors"), ("linewidth", "linewidths")]:
        if left in kwargs and right in kwargs:
            raise TypeError(f"{context}: pass only one of {left} and {right}.")
    if "s" in kwargs:
        if size is not None:
            raise TypeError(f"{context}: pass only one of size and s.")
        size = kwargs["s"]
    if color_map is not None and cmap is not None:
        raise ValueError(f"{context}: cannot specify both color_map and cmap.")
    if groups is not None and mask_obs is not None:
        raise ValueError(f"{context}: groups and mask_obs are incompatible.")

    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=frameon,
        sort_order=sort_order,
        na_in_legend=na_in_legend,
        hover=hover,
        zoom=zoom,
        add_outline=False if add_outline is None else add_outline,
        edges=edges,
    )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._embedding_data import prepare_embedding
    from genome_spy.integrations.scanpy._embedding_chart import build_embedding
    from genome_spy.integrations.scanpy._style import embedding_style

    # Read existing coordinates and colors without running analysis.
    prepared = prepare_embedding(
        adata,
        basis=basis,
        annotate_var_explained=annotate_var_explained,
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
        vcenter=vcenter,
        title=title,
        obs_id=obs_id,
        colorbar_loc=colorbar_loc,
        edges=edges,
        neighbors_key=neighbors_key,
    )

    # Keep appearance separate from the selected data.
    style = embedding_style(
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
        alpha=kwargs.get("alpha", 0.7 if add_outline else None),
        edgecolor=kwargs.get("edgecolor", kwargs.get("edgecolors", "none")),
        linewidth=kwargs.get("linewidth", kwargs.get("linewidths")),
        na_color=na_color,
        add_outline=bool(add_outline),
        outline_width=outline_width,
        outline_color=outline_color,
        edges_width=edges_width if edges else 0.1,
        edges_color=edges_color if edges else "grey",
    )
    chart = build_embedding(
        prepared, style, hover=hover, zoom=zoom, selection=selection
    )
    return _finish_plot(chart, show, sc)


def scatter(
    adata: AnnData,
    x: str | None = None,
    y: str | None = None,
    *,
    color: str | Collection[str] | None = None,
    use_raw: bool | None = None,
    layers: str | Collection[str | None] | None = None,
    sort_order: bool = True,
    alpha: float | None = None,
    basis: str | None = None,
    groups: str | Collection[str] | None = None,
    components: str | Collection[str] | None = None,
    projection: Literal["2d", "3d"] = "2d",
    legend_loc: str | None = "right margin",
    legend_fontsize: float | str | None = None,
    legend_fontweight: int | str | None = None,
    legend_fontoutline: float | None = None,
    color_map: Any = None,
    palette: Any = None,
    frameon: bool | None = None,
    right_margin: float | None = None,
    left_margin: float | None = None,
    size: float | None = None,
    marker: str | Sequence[str] = ".",
    title: str | Collection[str] | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    hover: bool = True,
    zoom: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot cells or genes from supplied coordinates with Scanpy scatter semantics.

    Uses observation/variable annotations or selected expression vectors for x
    and y, or an existing X_<basis> embedding. Reuses native embedding points,
    colors, guides, hover and zoom without changing AnnData or running analysis.

    Args:
        adata: AnnData containing the requested annotations and expression.
        x: Numeric annotation or expression key for the horizontal axis.
        y: Numeric annotation or expression key for the vertical axis.
        color: Annotation/expression key, CSS color, or one per panel.
        use_raw: Use raw expression; defaults to whether raw exists.
        layers: One layer for all values, or separate x/y/color layers. Use
            None or "X" for X; other layers require use_raw=False when raw exists.
        sort_order: Retained Scanpy flag; pinned scatter always sorts numeric colors.
        alpha: Scalar point opacity.
        basis: Existing X_<basis> coordinates, taking priority over x/y.
        groups: Category names to color; other points remain light gray.
        components: One-based coordinate pair; diffusion maps skip the first column.
        projection: Only 2d is currently supported.
        legend_loc: Right margin or none; other placements currently error.
        legend_fontsize: Native category legend font size.
        legend_fontweight: Retained Scanpy option; only affects on-data labels upstream.
        legend_fontoutline: Nondefault values currently error.
        color_map: GenomeSpy continuous color scheme name.
        palette: CSS category colors or native scheme, optionally one per panel.
        frameon: Embedding frame visibility; x/y plots retain axes as in Scanpy.
        right_margin: Nondefault values currently error; native guides own layout.
        left_margin: Nondefault values currently error; use width/height for sizing.
        size: Scalar point area, defaulting to 120000 divided by the point count.
        marker: Dot or circle, optionally one per color panel.
        title: Panel titles, defaulting to annotation names with underscores replaced.
        show: Display the chart, using Scanpy autoshow when None.
        save: None/False only; save the returned native chart as HTML/JSON.
        hover: Enable native point tooltips.
        zoom: Enable x/y zoom and panning.
        width: Native panel width in pixels.
        height: Native panel height in pixels.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the pinned optional Scanpy dependency is unavailable.
        TypeError: If argument types are invalid or omitted renderer options are passed.
        ValueError: If data, layers, orientations or components are invalid.
        NotImplementedError: If an appearance or storage form is unsupported.

    Example:
        >>> chart = gsc.pl.scatter(adata, "n_counts", "n_genes", color="louvain", show=False)
    """
    context = "gsc.pl.scatter"
    unsupported = {
        "projection": projection != "2d",
        "legend_loc": legend_loc not in ("right margin", "none"),
        "legend_fontoutline": legend_fontoutline is not None,
        "right_margin": right_margin is not None,
        "left_margin": left_margin is not None,
    }
    for name, rejected in unsupported.items():
        if rejected:
            raise NotImplementedError(f"{context}: {name} is not supported yet.")
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=frameon,
        sort_order=sort_order,
        hover=hover,
        zoom=zoom,
    )
    sc = _prepare_plot(show, save, context=context)
    from dataclasses import replace
    from genome_spy.integrations.scanpy._scatter_data import prepare_scatter
    from genome_spy.integrations.scanpy._embedding_chart import build_embedding
    from genome_spy.integrations.scanpy._style import embedding_style

    prepared = prepare_scatter(
        adata,
        x=x,
        y=y,
        basis=basis,
        color=color,
        use_raw=use_raw,
        layers=layers,
        groups=groups,
        components=components,
        size=size,
        marker=marker,
        palette=palette,
        cmap=color_map,
        title=title,
    )
    show_frame = sc.settings._frameon if frameon is None else frameon
    # Scanpy retains the frame and numeric ticks for direct x/y plots.
    if basis is None or x is not None or y is not None:
        show_frame = True
    style = embedding_style(
        count=len(prepared.panels),
        width=width,
        height=height,
        frameon=show_frame,
        legend_loc=legend_loc,
        colorbar_loc="right",
        legend_fontsize=legend_fontsize,
        ncols=len(prepared.panels),
        hspace=0.25,
        wspace=None,
        alpha=alpha,
        edgecolor="none",
        linewidth=None,
        na_color="lightgrey",
    )
    style = replace(style, legend_symbol_size=300)
    return _finish_plot(
        build_embedding(prepared, style, hover=hover, zoom=zoom), show, sc
    )


def embedding_density(
    adata: AnnData,
    basis: str = "umap",
    *,
    key: str | None = None,
    groupby: str | None = None,
    group: str | Sequence[str] | None = "all",
    color_map: Any = "YlOrRd",
    bg_dotsize: int | None = 80,
    fg_dotsize: int | None = 180,
    vmax: _Bound = 1,
    vmin: _Bound = 0,
    vcenter: _Bound = None,
    norm: Any = None,
    ncols: int | None = 4,
    hspace: float | None = 0.25,
    wspace: float | None = None,
    title: str | None = None,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool = False,
    obs_id: str | None = None,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Plot stored embedding densities using the shared native point renderer.

    Reads density values and their stored component/covariate metadata. Group
    panels preserve background cells, sizes and under/over colors without KDE,
    temporary observation columns or changes to the supplied coordinates.

    Args:
        adata: AnnData containing explicitly computed embedding-density results.
        basis: Stored ``X_`` embedding; lowercase names and the fa alias match Scanpy.
        key: Stored obs density key with a matching uns key_params mapping.
        groupby: Append this suffix to the pinned default umap_density key.
        group: All stored categories by default; select a string/list, or None for ungrouped results.
        color_map: GenomeSpy continuous scheme, default YlOrRd.
        bg_dotsize: Background point area in squared points, default 80.
        fg_dotsize: Foreground point area in squared points, default 180.
        vmax: Upper color bound, default 1; accepts shared bound forms.
        vmin: Lower color bound, default 0; accepts shared bound forms.
        vcenter: Optional numeric, percentile or callable color center.
        norm: Only None; Matplotlib normalization objects are unsupported.
        ncols: Maximum panels per row, default 4.
        hspace: Vertical spacing relative to panel height, default 0.25.
        wspace: Horizontal spacing relative to width; native default 0.2.
        title: Optional common panel title; otherwise the selected group.
        show: Display once, return a chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show stable cell identity, stored density and coordinates.
        zoom: Enable shared x/y zoom across density panels.
        obs_id: Optional unique, nonmissing obs column for stable cell IDs.
        width: Plot width per panel, default 300 logical pixels.
        height: Plot height per panel, default 300 logical pixels.
        **kwargs: Supported embedding styles: frameon, sort_order, marker, alpha,
            edgecolor/edgecolors, linewidth/linewidths and colorbar_loc.
            Unsorted points must stay within one color range; native under/over
            layers otherwise change their overlap order. One marker serves all groups.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If arguments or stored data are invalid.
        ValueError: If density values, params, groups or dimensions are invalid.
        NotImplementedError: If options require unsupported normalization or rendering.

    Example:
        >>> sc.tl.embedding_density(adata, basis="umap", groupby="phase")
        >>> chart = gsc.pl.embedding_density(adata, groupby="phase", show=False)
    """
    context = "gsc.pl.embedding_density"
    _check_kwargs(
        kwargs,
        {
            "frameon",
            "sort_order",
            "marker",
            "alpha",
            "edgecolor",
            "edgecolors",
            "linewidth",
            "linewidths",
            "colorbar_loc",
        },
        context=context,
    )
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=kwargs.get("frameon"),
        sort_order=kwargs.get("sort_order", True),
        hover=hover,
        zoom=zoom,
    )
    if not isinstance(basis, str) or not basis:
        raise ValueError(f"{context}: basis must be a nonempty string.")
    for name, value in (("key", key), ("groupby", groupby), ("title", title)):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    if key is not None and groupby is not None:
        raise ValueError(f"{context}: pass key or groupby, not both.")
    if group is not None and not isinstance(group, (str, list, tuple)):
        raise TypeError(
            f"{context}: group must be a string, list/tuple of strings or None."
        )
    if norm is not None or ncols is None or hspace is None:
        raise NotImplementedError(
            f"{context}: norm requires None; ncols and hspace require numeric values."
        )
    for left, right in (("edgecolor", "edgecolors"), ("linewidth", "linewidths")):
        if left in kwargs and right in kwargs:
            raise TypeError(f"{context}: pass only one of {left} and {right}.")
    colorbar = kwargs.get("colorbar_loc", "right")
    if colorbar not in (None, "right", "left", "top", "bottom"):
        raise NotImplementedError(f"{context}: unsupported colorbar_loc.")
    from genome_spy.integrations.scanpy._data import number

    bg = number(bg_dotsize, "bg_dotsize", context=context)
    fg = number(fg_dotsize, "fg_dotsize", context=context)
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._embedding_density_data import prepare_density
    from genome_spy.integrations.scanpy._embedding_chart import build_embedding
    from genome_spy.integrations.scanpy._style import embedding_style

    basis = "draw_graph_fa" if basis.lower() == "fa" else basis.lower()
    prepared = prepare_density(
        adata,
        basis,
        key=key,
        groupby=groupby,
        group=group,
        color_map=color_map,
        bg_dotsize=bg,
        fg_dotsize=fg,
        vmin=vmin,
        vmax=vmax,
        vcenter=vcenter,
        title=title,
        marker=kwargs.get("marker", "."),
        sort_order=kwargs.get("sort_order", True),
        obs_id=obs_id,
        colorbar_loc=colorbar,
    )
    style = embedding_style(
        count=len(prepared.panels),
        width=width,
        height=height,
        frameon=sc.settings._frameon
        if kwargs.get("frameon") is None
        else kwargs["frameon"],
        legend_loc="right margin",
        colorbar_loc=colorbar,
        legend_fontsize=None,
        ncols=ncols,
        hspace=hspace,
        wspace=wspace,
        alpha=kwargs.get("alpha"),
        edgecolor=kwargs.get("edgecolor", kwargs.get("edgecolors", "none")),
        linewidth=kwargs.get("linewidth", kwargs.get("linewidths")),
        na_color="lightgray",
    )
    return _finish_plot(
        build_embedding(prepared, style, hover=hover, zoom=zoom), show, sc
    )


def scrublet_score_distribution(
    adata: AnnData,
    *,
    scale_hist_obs: str = "log",
    scale_hist_sim: str = "linear",
    figsize: tuple[float, float] = (8, 3),
    show: bool | None = True,
    save: str | bool | None = None,
    hover: bool = True,
    zoom: bool = False,
    threshold_slider: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Plot stored observed and simulated Scrublet score densities by batch.

    Reads obs.doublet_score and uns.scrublet without running Scrublet or reading
    expression. Each pair retains Scanpy's fixed bins and stored threshold.

    Args:
        adata: AnnData with previously computed Scrublet results.
        scale_hist_obs: Observed density scale, linear or log (default).
        scale_hist_sim: Simulated density scale, linear (default) or log.
        figsize: Approximate figure size per batch in inches, default (8, 3).
        show: Display once by default; False returns a native chart.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show each populated bin's boundaries, count and density.
        zoom: Enable independent score-axis zoom in each panel.
        threshold_slider: Preview a cutoff per batch and highlight bins above it.
            Bins containing the cutoff stay neutral; saved doublet calls are unchanged.
        width: Plot width per panel, default 340 logical pixels.
        height: Plot height per panel, default 210 logical pixels.
        **kwargs: Matplotlib ax/return_fig and other options are omitted.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If arguments or score storage are invalid.
        ValueError: If results, scores, thresholds or dimensions are invalid.
        NotImplementedError: If scales, unused batch categories or saving are unsupported.

    Example:
        >>> sc.pp.scrublet(counts, threshold=0.25, random_state=0)
        >>> chart = gsc.pl.scrublet_score_distribution(counts, show=False)
    """
    context = "gsc.pl.scrublet_score_distribution"
    _check_kwargs(kwargs, set(), context=context)
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=None,
        hover=hover,
        zoom=zoom,
        threshold_slider=threshold_slider,
    )
    for name, scale in (
        ("scale_hist_obs", scale_hist_obs),
        ("scale_hist_sim", scale_hist_sim),
    ):
        if not isinstance(scale, str) or scale not in {"linear", "log"}:
            raise NotImplementedError(
                f"{context}: {name} supports 'linear' and 'log' only."
            )
    from genome_spy.integrations.scanpy._data import number

    if not isinstance(figsize, (tuple, list)) or len(figsize) != 2:
        raise TypeError(
            f"{context}: figsize requires two positive dimensions in inches."
        )
    figure_width, figure_height = [
        number(v, "figsize", context=context) for v in figsize
    ]
    if figure_width * 50 <= 60 or figure_height * 100 <= 90:
        raise ValueError(
            f"{context}: figsize is too small to reserve space for axes and titles."
        )
    if tuple(figsize) != (8, 3) and (width is not None or height is not None):
        raise TypeError(
            f"{context}: nondefault figsize cannot be combined with width or height."
        )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._scrublet_data import prepare_scrublet
    from genome_spy.integrations.scanpy._scrublet_chart import build_scrublet

    bins, thresholds = prepare_scrublet(adata)
    chart = build_scrublet(
        bins,
        thresholds,
        scales=(scale_hist_obs, scale_hist_sim),
        hover=hover,
        zoom=zoom,
        threshold_slider=threshold_slider,
        width=figure_width * 50 - 60 if width is None else width,
        height=figure_height * 100 - 90 if height is None else height,
    )
    return _finish_plot(chart, show, sc)


def highest_expr_genes(
    adata: AnnData,
    n_top: int = 30,
    *,
    layer: str | None = None,
    gene_symbols: str | None = None,
    log: bool = False,
    show: bool | None = None,
    save: str | bool | None = None,
    hover: bool = True,
    zoom: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot per-cell count percentages for genes with the highest mean percentage.

    Reuses Scanpy's public total normalization on X or a layer, ignoring raw.
    Native boxes show quartiles, 1.5-IQR whiskers and individual outliers.
    Expression and metadata are never changed, including for AnnData views.

    Args:
        adata: AnnData with resident, finite, nonnegative counts.
        n_top: Number of genes ranked by mean percentage, default 30.
        layer: Count layer instead of X; raw is never selected implicitly.
        gene_symbols: Optional var column for unique, nonmissing display labels.
        log: Use a logarithmic percentage axis; summaries remain in linear units.
        show: Display once, return a chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show box summaries and outlier cell identities.
        zoom: Enable native zoom along the percentage axis.
        width: Plot width, default 387.5 logical pixels.
        height: Plot height, default Scanpy's gene-count-dependent panel height.
        **kwds: Seaborn styling and Matplotlib options are currently unsupported.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If arguments or expression storage are unsupported.
        ValueError: If counts, labels, dimensions or n_top are invalid.
        NotImplementedError: If labels are ambiguous or styling/saving is unsupported.

    Example:
        >>> chart = gsc.pl.highest_expr_genes(counts, n_top=20, show=False)
    """
    context = "gsc.pl.highest_expr_genes"
    _check_kwargs(kwds, set(), context=context)
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=None,
        log=log,
        hover=hover,
        zoom=zoom,
    )
    if isinstance(n_top, bool) or not isinstance(n_top, Integral) or n_top <= 0:
        raise ValueError(f"{context}: n_top must be a positive integer.")
    for name, value in (("layer", layer), ("gene_symbols", gene_symbols)):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._highest_expr_data import (
        prepare_highest_expression,
    )
    from genome_spy.integrations.scanpy._highest_expr_chart import (
        build_highest_expression,
    )

    boxes, outliers, limits = prepare_highest_expression(
        adata, n_top, layer, gene_symbols
    )
    chart = build_highest_expression(
        boxes,
        outliers,
        limits,
        n_top=n_top,
        log=log,
        hover=hover,
        zoom=zoom,
        width=width,
        height=height,
    )
    return _finish_plot(chart, show, sc)


def highly_variable_genes(
    adata_or_result: AnnData | pd.DataFrame | np.recarray,
    *,
    log: bool = False,
    show: bool | None = None,
    save: bool | str | None = None,
    highly_variable_genes: bool = True,
    hover: bool = True,
    zoom: bool = False,
    threshold_slider: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot stored gene means against normalized and raw dispersion or variance.

    Reads AnnData.var or supplied results without selecting genes or accessing
    expression. The two panels share native colors and keep their own axis limits.

    Args:
        adata_or_result: AnnData with stored hvg flavor, a DataFrame or record array.
        log: Use logarithmic axes, retaining Scanpy's raw-statistic limits.
        show: Display once, return a chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        highly_variable_genes: Use highly_variable; False reads legacy gene_subset.
        hover: Show gene identity and the stored plotted statistics.
        zoom: Enable native x/y zoom independently in each panel.
        threshold_slider: Add a normalized-score cutoff preview; leaves saved selection unchanged.
        width: Plot width per panel, default 300 logical pixels.
        height: Plot height per panel, default 300 logical pixels.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If result storage, flags or selected-gene values are invalid.
        ValueError: If stored fields or dimensions are missing or invalid.
        NotImplementedError: If log bounds or saving need unsupported behavior.

    Example:
        >>> chart = gsc.pl.highly_variable_genes(adata, zoom=True, show=False)
    """
    context = "gsc.pl.highly_variable_genes"
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=None,
        log=log,
        highly_variable_genes=highly_variable_genes,
        hover=hover,
        zoom=zoom,
        threshold_slider=threshold_slider,
    )
    if threshold_slider and log:
        raise NotImplementedError(
            f"{context}: threshold_slider requires linear axes (log=False)."
        )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._scatter_data import prepare_variable_genes
    from genome_spy.integrations.scanpy._hvg_chart import build_variable_genes

    table, statistic = prepare_variable_genes(adata_or_result, highly_variable_genes)
    chart = build_variable_genes(
        table,
        statistic,
        log=log,
        hover=hover,
        zoom=zoom,
        threshold_slider=threshold_slider,
        width=width,
        height=height,
    )
    return _finish_plot(chart, show, sc)


def filter_genes_dispersion(
    result: np.recarray,
    *,
    log: bool = False,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool = False,
    threshold_slider: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot legacy stored dispersions through highly_variable_genes.

    Reads gene_subset instead of highly_variable. As with other native plots,
    show=False returns a chart rather than the legacy wrapper's None.

    Args:
        result: Stored record array with means, dispersions and gene_subset.
        log: Use logarithmic axes with Scanpy's stored-statistic limits.
        show: Display once, return a chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show gene identity and stored statistics.
        zoom: Enable native x/y zoom independently in each panel.
        threshold_slider: Preview a normalized-score cutoff without changing gene_subset.
        width: Plot width per panel, default 300 logical pixels.
        height: Plot height per panel, default 300 logical pixels.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If result storage or flags are invalid.
        ValueError: If stored fields or dimensions are missing or invalid.
        NotImplementedError: If log bounds or saving need unsupported behavior.

    Example:
        >>> chart = gsc.pl.filter_genes_dispersion(result, show=False)
    """
    import warnings

    warnings.warn(
        "Use gsc.pl.highly_variable_genes instead", DeprecationWarning, stacklevel=2
    )
    return highly_variable_genes(
        result,
        log=log,
        show=show,
        save=save,
        highly_variable_genes=False,
        threshold_slider=threshold_slider,
        hover=hover,
        zoom=zoom,
        width=width,
        height=height,
    )


def _embedding_signature(
    plot: Callable[..., TopLevelSpec | None],
) -> Callable[..., TopLevelSpec | None]:
    """Expose shared keyword defaults without copying six plotting signatures."""
    from inspect import signature

    own = signature(plot)
    parameters = {
        name: parameter
        for name, parameter in signature(_embedding).parameters.items()
        if name not in {"context", "annotate_var_explained", "kwargs"}
        and (name != "basis" or name in own.parameters)
    }
    parameters.update(own.parameters)
    setattr(plot, "__signature__", own.replace(parameters=list(parameters.values())))
    return plot


@_embedding_signature
def embedding(adata: AnnData, basis: str, **kwargs: Any) -> TopLevelSpec | None:
    """Plot supplied 2D embedding coordinates with Scanpy-compatible colors.

    Reads an existing obsm basis using direct-name then ``X_`` precedence. Shared
    options cover categorical/continuous colors, component panels, masks, native
    sizing, hover, zoom and interval selection. Analysis stays in Scanpy.

    Args:
        adata: AnnData containing the supplied coordinates and requested colors.
        basis: Existing obsm name, such as umap, tsne, diffmap or pca.
        **kwargs: Shared embedding options shown in the signature. Components
            are one-based strings; dimensions are zero-based pairs. Raw/layer
            lookup, colors, defaults and native controls match pl.umap.
            marker accepts '.', 'o', 's' and 'D', once or per panel.
            colorbar_loc accepts right, left, top, bottom, or None to hide it.
            add_outline draws two background outlines with outline_width and
            outline_color; the foreground then defaults to alpha=0.7.
            vmin/vmax/vcenter also accept callables returning a finite number from each
            panel's masked colors in painting order, including missing values.
            vcenter maps to the native color scheme's midpoint; automatic limits
            expand when needed to enclose it, while explicit limits must enclose it.
            edges draws the stored undirected neighbor graph beneath points;
            edges_width uses points and edges_color requires one opaque CSS color.
            neighbors_key selects saved metadata. Edges currently require the
            first two components and a graph without self-loops.
            selection accepts a native x/y interval parameter and adds a live
            cell count without changing point appearance. With zoom=True,
            Shift-drag brushes and ordinary dragging pans.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the pinned optional Scanpy dependency is unavailable.
        TypeError: If options or source types are invalid.
        ValueError: If coordinates, colors or component requests are invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.embedding(adata, "pca", color="cell_type", show=False)
    """
    return _embedding(adata, basis, "gsc.pl.embedding", False, **kwargs)


@_embedding_signature
def umap(adata: AnnData, **kwargs: Any) -> TopLevelSpec | None:
    """Plot stored UMAP coordinates through the shared embedding renderer.

    Preserves Scanpy defaults and the existing native UMAP controls. Computes no
    embedding and does not modify AnnData; see pl.embedding for shared options.

    Args:
        adata: AnnData containing umap or X_umap coordinates.
        **kwargs: Shared embedding options shown in the signature, including
            hover, zoom, selection, obs_id, width and height.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If arguments or source types are invalid.
        ValueError: If stored coordinates or requested data are invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.umap(adata, color=["cell_type", "MS4A1"], show=False)
    """
    return _embedding(adata, "umap", "gsc.pl.umap", False, **kwargs)


@_embedding_signature
def tsne(adata: AnnData, **kwargs: Any) -> TopLevelSpec | None:
    """Plot stored t-SNE coordinates through the shared embedding renderer.

    Uses tsne or X_tsne without computing t-SNE; see pl.embedding for options.

    Args:
        adata: AnnData containing supplied t-SNE coordinates.
        **kwargs: Shared embedding colors, component choices and native controls.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If arguments or source types are invalid.
        ValueError: If coordinates or requested data are missing or invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.tsne(adata, color="cell_type", zoom=True, show=False)
    """
    return _embedding(adata, "tsne", "gsc.pl.tsne", False, **kwargs)


@_embedding_signature
def diffmap(adata: AnnData, **kwargs: Any) -> TopLevelSpec | None:
    """Plot stored diffusion coordinates through the shared embedding renderer.

    Preserves Scanpy 1.11.5's default first two columns and DC labels. Reads
    diffmap or X_diffmap without fitting diffusion components or neighbors.

    Args:
        adata: AnnData containing supplied diffusion coordinates.
        **kwargs: Shared embedding colors, component choices and native controls.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If arguments or source types are invalid.
        ValueError: If coordinates or requested data are missing or invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.diffmap(adata, components="2,3", show=False)
    """
    return _embedding(adata, "diffmap", "gsc.pl.diffmap", False, **kwargs)


@_embedding_signature
def draw_graph(
    adata: AnnData, *, layout: str | None = None, **kwargs: Any
) -> TopLevelSpec | None:
    """Plot an existing graph layout through the shared embedding renderer.

    Reads the requested X_draw_graph_<layout> coordinates. With layout=None,
    uses the saved draw_graph params; never computes a layout or neighbors.

    Args:
        adata: AnnData containing saved graph-layout coordinates.
        layout: Saved layout name; None uses the last computed layout.
        **kwargs: Shared embedding colors, component choices and native controls.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If arguments or source types are invalid.
        ValueError: If layout metadata, coordinates or requested data are invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.draw_graph(adata, layout="fa", color="cell_type", show=False)
    """
    _prepare_plot(kwargs.get("show"), kwargs.get("save"), context="gsc.pl.draw_graph")
    from anndata import AnnData

    if not isinstance(adata, AnnData):
        raise TypeError("gsc.pl.draw_graph: expected AnnData.")
    if layout is None:
        stored = adata.uns.get("draw_graph")
        params = stored.get("params") if isinstance(stored, Mapping) else None
        layout = params.get("layout") if isinstance(params, Mapping) else None
    if not isinstance(layout, str) or not layout:
        raise ValueError(
            "gsc.pl.draw_graph: supply layout or stored draw_graph params; compute the layout explicitly first."
        )
    basis = f"draw_graph_{layout}"
    if f"X_{basis}" not in adata.obsm:
        raise ValueError(
            f"gsc.pl.draw_graph: missing X_{basis}; compute the requested layout explicitly first."
        )
    return _embedding(adata, basis, "gsc.pl.draw_graph", False, **kwargs)


@_embedding_signature
def pca(
    adata: AnnData, *, annotate_var_explained: bool = False, **kwargs: Any
) -> TopLevelSpec | None:
    """Plot stored PCA coordinates, optionally labeling their explained variance.

    Reuses embedding data, chart and interaction helpers. Variance annotations
    read uns['pca']['variance_ratio']; plotting never fits PCA.

    Args:
        adata: AnnData containing pca or X_pca coordinates.
        annotate_var_explained: Add stored variance percentages to PC axis labels.
        **kwargs: Shared embedding colors, component choices and native controls.

    Returns:
        A native chart when show=False, otherwise None after display.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If arguments or source types are invalid.
        ValueError: If coordinates or required variance metadata are invalid.
        NotImplementedError: If a renderer option is unsupported.

    Example:
        >>> chart = gsc.pl.pca(adata, annotate_var_explained=True, show=False)
    """
    return _embedding(adata, "pca", "gsc.pl.pca", annotate_var_explained, **kwargs)


pca_scatter = pca


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
    colorbar_title: str | None = "Mean expression",
    size_title: str | None = "Cells expressing (%)",
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
    zoom: bool | Literal["xy"] = False,
    highlight: bool = False,
    group_gap: float = 0,
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
        colorbar_title: Color guide title, default "Mean expression"; None omits the title.
        size_title: Percentage guide title, default "Cells expressing (%)"; None omits the title.
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
        zoom: True enables y-only zoom/panning; "xy" also enables x navigation.
        highlight: Mark the row and column under the pointer with a native ruler.
        group_gap: Space between marker blocks in pixels; 0 keeps slots contiguous.
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
    _check_kwargs(kwds, {"linewidth"}, context="gsc.pl.dotplot")
    if not isinstance(dendrogram, (bool, str)) or dendrogram == "":
        raise TypeError(
            "gsc.pl.dotplot: dendrogram must be False, True, or a nonempty cache key."
        )
    if swap_axes is not None and not isinstance(swap_axes, bool):
        raise TypeError("gsc.pl.dotplot: swap_axes must be boolean or None.")
    _check_point_options(
        context="gsc.pl.dotplot",
        width=width,
        height=height,
        frameon=None,
        log=log,
        mean_only_expressed=mean_only_expressed,
        hover=hover,
        highlight=highlight,
    )
    _check_grid_zoom(zoom, context="gsc.pl.dotplot")
    sc = _prepare_plot(show, save, context="gsc.pl.dotplot")
    plot = DotPlot(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log,
        num_categories=num_categories,
        categories_order=categories_order,
        expression_cutoff=expression_cutoff,
        mean_only_expressed=mean_only_expressed,
        standard_scale=standard_scale,
        title=title,
        figsize=figsize,
        gene_symbols=gene_symbols,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
        var_group_rotation=var_group_rotation,
        layer=layer,
        dot_color_df=dot_color_df,
        vmin=vmin,
        vmax=vmax,
        vcenter=vcenter,
        norm=norm,
        hover=hover,
        zoom=zoom,
        highlight=highlight,
        group_gap=group_gap,
        width=width,
        height=height,
        cmap=cmap,
        **kwds,
    )
    plot.swap_axes(swap_axes=swap_axes).style(
        dot_max=dot_max, dot_min=dot_min, smallest_dot=smallest_dot
    ).legend(colorbar_title=colorbar_title, size_title=size_title)
    if dendrogram:
        plot.add_dendrogram(
            dendrogram_key=dendrogram if isinstance(dendrogram, str) else None
        )
    return _finish_plot(plot.to_chart(), show, sc)


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
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
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
        zoom: True enables y-only zoom/panning; "xy" also enables x navigation.
        show_values: Show plotted values to two decimals when cells have enough room.
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
    for name, value in {
        "log": log,
        "swap_axes": swap_axes,
        "hover": hover,
        "show_values": show_values,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if standard_scale not in (None, "var", "group"):
        raise ValueError(f"{context}: standard_scale must be 'var', 'group', or None.")
    _check_grid_zoom(zoom, context=context)
    sc = _prepare_plot(show, save, context=context)
    plot = MatrixPlot(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log,
        num_categories=num_categories,
        categories_order=categories_order,
        title=title,
        figsize=figsize,
        gene_symbols=gene_symbols,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
        var_group_rotation=var_group_rotation,
        layer=layer,
        standard_scale=standard_scale,
        values_df=values_df,
        vmin=vmin,
        vmax=vmax,
        vcenter=vcenter,
        norm=norm,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
        cmap=cmap,
        **kwds,
    )
    plot.swap_axes(swap_axes=swap_axes).legend(title=colorbar_title)
    if dendrogram:
        plot.add_dendrogram(
            dendrogram_key=dendrogram if isinstance(dendrogram, str) else None
        )
    return _finish_plot(plot.to_chart(), show, sc)


def tracksplot(
    adata: AnnData,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str,
    *,
    use_raw: bool | None = None,
    log: bool = False,
    dendrogram: bool | str = False,
    gene_symbols: str | None = None,
    var_group_positions: Sequence[tuple[int, int]] | None = None,
    var_group_labels: Sequence[str] | None = None,
    layer: str | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    figsize: tuple[float, float] | None = None,
    hover: bool = True,
    zoom: bool = False,
    group_gap: float = 0,
    spacing: float = 0,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot cell-level expression tracks ordered by a categorical annotation.

    Description:
        Read selected genes through Scanpy's public getter, preserving raw/layer
        precedence and cell order within groups. Each cell is one native rect,
        giving stepped profiles rather than Scanpy's fill between adjacent values.
        Optional trees reuse stored linkage or Scanpy's existing tree helper;
        plotting never fits embeddings or rankings. The preview reads at most
        250,000 cell–gene values from resident data, without changing AnnData.

    Args:
        adata: Annotated expression data.
        var_names: Gene keys or a marker dictionary; repeated genes retain tracks.
        groupby: Categorical observation column defining cell order and colors.
        use_raw: Use raw by default when available and no layer is requested.
        log: Apply log1p to values, then use logarithmic y-axes, as in Scanpy.
        dendrogram: Attach a group tree, optionally naming a stored result.
        gene_symbols: Variable annotation containing requested gene symbols.
        var_group_positions: Inclusive marker spans, covering all genes in order.
        var_group_labels: Labels defining those marker groups.
        layer: Expression layer; incompatible with explicit use_raw=True.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the returned chart's HTML/JSON export.
        figsize: Overall size in inches; cannot be combined with native dimensions.
        hover: Include cell ID, label, group, gene and plotted-value tooltips.
        zoom: Enable linked x-only zoom and panning across cells.
        group_gap: Space between cell groups in pixels; defaults to 0.
        spacing: Space between tracks, the tree and category strip in pixels.
        width: Track plotting width in pixels; defaults to 1200.
        height: Combined expression-track height in pixels; defaults to 25 per gene.
        **kwds: Forwarded styling is unsupported and fails by name.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If options or expression storage are unsupported.
        ValueError: If groups, values, sources, marker spans or dimensions are invalid.
        NotImplementedError: If marker spans do not partition the requested genes.

    Example:
        >>> chart = gsc.pl.tracksplot(
        ...     pbmc, ["CD79A", "CD3D"], "bulk_labels", zoom=True, show=False
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.tracksplot"
    _check_kwargs(kwds, set(), context=context)
    for name, value in {"log": log, "hover": hover, "zoom": zoom}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if not isinstance(dendrogram, (bool, str)) or dendrogram == "":
        raise TypeError(f"{context}: dendrogram must be False, True or a nonempty key.")
    from genome_spy.integrations.scanpy._data import number

    group_gap = number(group_gap, "group_gap", context=context)
    spacing = number(spacing, "spacing", context=context)
    sc = _prepare_plot(show, save, context=context)
    import numpy as np
    import pandas as pd
    from anndata import AnnData
    from genome_spy.integrations.scanpy._grouped_data import ordered_cell_expression
    from genome_spy.integrations.scanpy._style import _palette
    from genome_spy.integrations.scanpy._tracksplot_chart import build_tracksplot

    # Tracks require one explicit categorical column, unlike heatmap's numeric bins.
    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    if (
        not isinstance(groupby, str)
        or groupby not in adata.obs
        or not isinstance(adata.obs[groupby].dtype, pd.CategoricalDtype)
    ):
        raise ValueError(f"{context}: groupby must name a categorical observation.")
    prepared, groups, tree = ordered_cell_expression(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log,
        gene_symbols=gene_symbols,
        layer=layer,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
        dendrogram=dendrogram,
        context=context,
    )
    categories = adata.obs[groupby].cat.categories
    palette, _ = _palette(adata, groupby, categories, None)
    names = adata.obs_names.to_numpy().copy()
    ids = (
        names
        if adata.obs_names.is_unique
        else np.array([f"row-{i}" for i in range(len(adata))])
    )
    positions = prepared.observation_positions
    chart = build_tracksplot(
        prepared,
        groups,
        names[positions],
        ids[positions],
        groupby=groupby,
        categories=list(map(str, categories)),
        palette=palette,
        tree=tree,
        log=log,
        hover=hover,
        zoom=zoom,
        group_gap=group_gap,
        spacing=spacing,
        width=width,
        height=height,
        figsize=figsize,
    )
    return _finish_plot(chart, show, sc)


def heatmap(
    adata: AnnData,
    var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
    groupby: str | Sequence[str],
    *,
    use_raw: bool | None = None,
    log: bool = False,
    num_categories: int = 7,
    dendrogram: bool | str = False,
    gene_symbols: str | None = None,
    var_group_positions: Sequence[tuple[int, int]] | None = None,
    var_group_labels: Sequence[str] | None = None,
    var_group_rotation: float | None = None,
    layer: str | None = None,
    standard_scale: Literal["var", "obs"] | None = None,
    swap_axes: bool = False,
    show_gene_labels: bool | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    figsize: tuple[float, float] | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    vcenter: float | None = None,
    norm: Any = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    group_gap: float = 0,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot individual cells' expression with Scanpy-compatible ordering.

    Description:
        Read selected values using Scanpy's public getter. Apply log1p and
        optional cell/gene scaling before sorting cells by category. Render
        native tiles, category strips, marker annotations and optional stored
        dendrograms. Colors use cell values; embeddings and rankings are not rerun.
        This preview supports at most 250,000 cell–gene values and rejects
        larger requests before extraction; subset explicitly to plot more data.

    Args:
        adata: Annotated expression data.
        var_names: Gene keys or a marker dictionary; repeated genes retain slots.
        groupby: Observation annotation or annotations defining cell order.
        use_raw: Use raw by default when available and no layer is requested.
        log: Apply log1p to cell values before scaling and sorting.
        num_categories: Number of bins for a numeric grouping column.
        dendrogram: Attach a tree, optionally naming its stored result.
        gene_symbols: Variable annotation containing the requested symbols.
        var_group_positions: Inclusive gene positions for marker annotations.
        var_group_labels: Labels for those marker annotations.
        var_group_rotation: Rotation of marker labels above an ordinary heatmap.
        layer: Expression layer; incompatible with explicit use_raw=True.
        standard_scale: Scale values to 0–1 per gene ("var") or cell ("obs").
        swap_axes: Place cells on x and genes on y.
        show_gene_labels: Default to showing labels for at most 50 genes.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the returned chart's HTML/JSON export.
        figsize: Compatible overall size in inches; native dimensions use pixels.
        vmin: Lower continuous color bound.
        vmax: Upper continuous color bound.
        vcenter: Nondefault values are unsupported.
        norm: Matplotlib normalization objects are unsupported.
        hover: Include cell ID, gene, group and expression tooltips, including
            category-strip tooltips.
        zoom: True enables y-only zoom/panning; "xy" also enables x navigation.
        show_values: Show plotted values to two decimals when cells have enough room.
        group_gap: Space between cell groups and marker blocks in CSS pixels;
            defaults to 0. Set a positive width to separate groups.
        width: Native tile-area width in pixels.
        height: Native tile-area height in pixels.
        **kwds: Native cmap scheme, scalar alpha and interpolation="nearest".

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If an option, source or forwarded keyword is unsupported.
        ValueError: If values, groups, labels, bounds or plot size are invalid.
        NotImplementedError: If normalization or interpolation is unsupported.

    Example:
        >>> chart = gsc.pl.heatmap(
        ...     pbmc, ["CD79A", "CD3D"], "bulk_labels", show=False
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.heatmap"
    # Validate options before loading data or the optional scientific stack.
    _check_kwargs(kwds, {"cmap", "alpha", "interpolation"}, context=context)
    for name, value in {"vcenter": vcenter, "norm": norm}.items():
        if value is not None:
            raise NotImplementedError(f"{context}: {name} is unsupported.")
    if kwds.get("interpolation", "nearest") != "nearest":
        raise NotImplementedError(f"{context}: interpolation supports only 'nearest'.")
    for name, value in {
        "log": log,
        "swap_axes": swap_axes,
        "hover": hover,
        "show_values": show_values,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if show_gene_labels is not None and not isinstance(show_gene_labels, bool):
        raise TypeError(f"{context}: show_gene_labels must be boolean or None.")
    if not isinstance(dendrogram, (bool, str)) or dendrogram == "":
        raise TypeError(f"{context}: dendrogram must be False, True or a nonempty key.")
    if standard_scale not in (None, "var", "obs"):
        raise ValueError(f"{context}: standard_scale must be 'var', 'obs' or None.")
    _check_grid_zoom(zoom, context=context)
    from genome_spy.integrations.scanpy._data import number

    group_gap = number(group_gap, "group_gap", context=context)
    sc = _prepare_plot(show, save, context=context)
    import numpy as np
    import pandas as pd
    from genome_spy.integrations.scanpy._grouped_data import (
        ordered_cell_expression,
    )
    from genome_spy.integrations.scanpy._heatmap_chart import build_heatmap
    from genome_spy.integrations.scanpy._style import _palette

    # Reuse expression access without replacing cells with group means.
    prepared, feature_groups, tree = ordered_cell_expression(
        adata,
        var_names,
        groupby,
        use_raw=use_raw,
        log=log,
        num_categories=num_categories,
        gene_symbols=gene_symbols,
        layer=layer,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
        dendrogram=dendrogram,
        standard_scale=standard_scale,
        context=context,
    )
    categories = prepared.values.index.categories

    # Saved category colors stay tied to labels even after tree reordering.
    palette: tuple[str, ...] = ()
    palette_scheme = None
    if (
        isinstance(groupby, str)
        and groupby in adata.obs
        and isinstance(adata.obs[groupby].dtype, pd.CategoricalDtype)
    ):
        source_categories = adata.obs[groupby].cat.categories
        original, _ = _palette(adata, groupby, source_categories, None)
        lookup = dict(zip(map(str, source_categories), original, strict=True))
        palette = tuple(lookup[label] for label in prepared.intervals["label"])
    else:
        if len(categories) > 20:
            raise NotImplementedError(
                f"{context}: automatic numeric/multi-key strip colors support at most 20 groups."
            )
        palette_scheme = "category20"

    # Use original row positions to keep duplicate observation names distinct.
    names = adata.obs_names.to_numpy().copy()
    ids = (
        names
        if adata.obs_names.is_unique
        else np.array([f"row-{i}" for i in range(len(adata))])
    )
    positions = prepared.observation_positions
    chart = build_heatmap(
        prepared,
        feature_groups,
        names[positions],
        ids[positions],
        groupby=groupby if isinstance(groupby, str) else "_".join(groupby),
        palette=palette,
        palette_scheme=palette_scheme,
        tree=tree,
        swap_axes=swap_axes,
        show_gene_labels=show_gene_labels,
        rotation=var_group_rotation,
        cmap=kwds.get("cmap", "viridis"),
        vmin=vmin,
        vmax=vmax,
        alpha=kwds.get("alpha", 1),
        hover=hover,
        show_values=show_values,
        group_gap=group_gap,
        zoom=zoom,
        scaled=standard_scale is not None,
        width=width,
        height=height,
        figsize=figsize,
    )
    return _finish_plot(chart, show, sc)


def clustermap(
    adata: AnnData,
    obs_keys: str | None = None,
    *,
    use_raw: bool | None = None,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Display individual cells and genes ordered by hierarchical clustering.

    Description:
        Reproduce supported Scanpy/Seaborn clustermap computations with public
        SciPy linkage and native tiles. This plotting-only clustering does not
        write AnnData or rerun analysis. Supplied linkage is authoritative.
        The preview uses a native magma palette and a color guide on the right;
        it returns a GenomeSpy chart rather than Seaborn's ClusterGrid.

    Args:
        adata: Resident AnnData; subset cells and genes before plotting.
        obs_keys: One categorical observation column for a row color strip
            and native legend.
        use_raw: Use raw expression when present by default, matching Scanpy.
        show: Display once if true; return a chart if false; None uses Scanpy's setting.
        save: None or False; use chart.save for HTML or JSON.
        hover: Show native tile and observation-strip tooltips.
        zoom: Enable y-only zoom and pan with True, or both axes with "xy".
        show_values: Show plotted values when enough space is available in each tile.
        width: Matrix width in logical pixels, excluding trees and labels.
        height: Matrix height in logical pixels, excluding trees and labels.
        **kwds: Supported Seaborn options: method, metric, z_score,
            standard_scale, row_cluster, col_cluster, row_linkage, col_linkage,
            row_colors, col_colors, mask, figsize, dendrogram_ratio, colors_ratio,
            xticklabels, yticklabels, cmap, vmin, vmax, linewidths, linecolor,
            cbar_pos (default or None), and cbar_kws (label only).

    Returns:
        A native chart, or None after display.

    Raises:
        ImportError: The supported Scanpy dependency is unavailable.
        TypeError: Options or data have unsupported types.
        ValueError: Shapes, linkage, scaling or resource limits are invalid.
        NotImplementedError: A renderer-specific option is unsupported.

    Example:
        >>> import scanpy as sc
        >>> import genome_spy.integrations.scanpy as gsc
        >>> pbmc = sc.datasets.pbmc68k_reduced()
        >>> chart = gsc.pl.clustermap(
        ...     pbmc[:, ["CD79A", "MS4A1", "CD3D"]],
        ...     obs_keys="bulk_labels", use_raw=False, show=False,
        ... )
    """
    context = "gsc.pl.clustermap"
    data_options = {
        "method",
        "metric",
        "z_score",
        "standard_scale",
        "row_cluster",
        "col_cluster",
        "row_linkage",
        "col_linkage",
        "row_colors",
        "col_colors",
        "mask",
    }
    chart_options = {
        "cmap",
        "vmin",
        "vmax",
        "figsize",
        "dendrogram_ratio",
        "colors_ratio",
        "xticklabels",
        "yticklabels",
        "linewidths",
        "linecolor",
        "cbar_pos",
        "cbar_kws",
    }
    _check_kwargs(kwds, data_options | chart_options, context=context)
    _check_grid_zoom(zoom, context=context)
    for name, option in (("hover", hover), ("show_values", show_values)):
        if not isinstance(option, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._clustermap_data import prepare_clustermap
    from genome_spy.integrations.scanpy._clustermap_chart import build_clustermap

    data = prepare_clustermap(
        adata,
        obs_keys,
        use_raw,
        **{key: value for key, value in kwds.items() if key in data_options},
    )
    chart = build_clustermap(
        data,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
        **{key: value for key, value in kwds.items() if key in chart_options},
    )
    return _finish_plot(chart, show, sc)


def matrix(
    matrix: ArrayLike,
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xticks: Collection[str] | None = None,
    yticks: Collection[str] | None = None,
    title: str | None = None,
    colorbar_shrink: float = 0.5,
    color_map: Any = None,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Display a supplied numeric matrix in its original row and column order.

    Description:
        Reproduce Scanpy's matrix helper using native tiles and a linear color
        guide. No AnnData access, aggregation or clustering occurs. Missing and
        masked entries stay blank; color bounds follow the finite input range.
        Matplotlib axes, image objects and colormap objects are unsupported.

    Args:
        matrix: Resident 2D numeric array, nested sequence or DataFrame.
        xlabel: Label below the x axis.
        ylabel: Label beside the y axis.
        xticks: One label per column; repeated labels retain separate slots.
        yticks: One label per row; repeated labels retain separate slots.
        title: Plot title.
        colorbar_shrink: Color guide length relative to plot height.
        color_map: Native GenomeSpy scheme; None uses viridis.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the returned chart's HTML/JSON export.
        hover: Include row, column and numeric value tooltips.
        zoom: True enables y-only zoom/panning; "xy" also enables x navigation.
        show_values: Show plotted values to two decimals when cells have enough room.
        width: Native tile-area width in pixels.
        height: Native tile-area height in pixels.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If the source or label form is unsupported.
        ValueError: If shape, numeric values, tick counts or sizes are invalid.
        NotImplementedError: If image saving or a nonnative color scheme is requested.

    Example:
        >>> chart = gsc.pl.matrix(
        ...     [[0, 1], [2, 3]], xticks=["A", "B"], show=False
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.matrix"
    for name, value in {
        "hover": hover,
        "show_values": show_values,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_grid_zoom(zoom, context=context)
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._matrix_chart import build_matrix

    chart = build_matrix(
        matrix,
        xlabel=xlabel,
        ylabel=ylabel,
        xticks=xticks,
        yticks=yticks,
        title=title,
        colorbar_shrink=colorbar_shrink,
        color_map=color_map,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
    )
    return _finish_plot(chart, show, sc)


def paga_compare(
    adata: AnnData,
    basis: str | None = None,
    *,
    edges: bool = False,
    color: str | None = None,
    alpha: float | None = None,
    groups: str | Sequence[str] | None = None,
    components: str | Sequence[str] | None = None,
    projection: Literal["2d", "3d"] = "2d",
    legend_loc: str | None = "on data",
    legend_fontsize: float | str | None = None,
    legend_fontweight: int | str = "bold",
    legend_fontoutline: int | None = None,
    color_map: Any = None,
    palette: Any = None,
    frameon: bool = False,
    size: float | Sequence[float] | None = None,
    title: str | None = None,
    right_margin: float | None = None,
    left_margin: float = 0.05,
    show: bool | None = None,
    save: bool | str | None = None,
    title_graph: str | None = None,
    groups_graph: Sequence[str] | None = None,
    pos: Any = None,
    hover: bool = True,
    zoom: bool = False,
    width: float | None = None,
    height: float | None = None,
    **paga_graph_params: Any,
) -> TopLevelSpec | None:
    """Compare a stored embedding and its PAGA graph in aligned native panels.

    Description:
        Reuse the embedding and PAGA plotting entries without computing analysis.
        With the PAGA group color, omitted positions are group medians in the
        selected embedding components. Other colors use cached PAGA positions.
        Both panels share the embedding limits and optional navigation. Colors
        and point sizes stay independent; the group key sits below both views.

    Args:
        adata: AnnData with stored embedding coordinates and PAGA results.
        basis: Stored basis; None prefers draw_graph_fa, umap, tsne, draw_graph_fr.
        edges: Show the stored observation-neighbor graph in the embedding panel.
        color: One observation key or gene; None uses the stored PAGA group key.
        alpha: Embedding point opacity; None uses the shared embedding default.
        groups: Categories highlighted in the embedding; graph groups are unchanged.
        components: One one-based coordinate pair, for example "2,3".
        projection: Only the default two-dimensional projection is supported.
        legend_loc: Embedding guide location, defaulting to group-median labels.
        legend_fontsize: Shared label size in points or a supported named size.
        legend_fontweight: On-data labels require normal/400; the bold default
            remains unsupported with the bundled regular font atlas.
        legend_fontoutline: Unsupported label outlines.
        color_map: Native continuous embedding scheme; graph cmap is independent.
        palette: CSS category colors/mapping or native scheme, shared by embedding
            and graph when color is the stored PAGA grouping.
        frameon: Draw the native panel frames.
        size: Embedding point areas in square points; None uses a compact area of 9.
            Points grow gently on zoom, up to twice their initial diameter.
        title: Common title when title_graph is None; otherwise embedding title.
        right_margin: Only None; native composition places the guides.
        left_margin: Only the pinned default; native composition sets spacing.
        show: Display once, return the chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        title_graph: Graph title; None selects a common title instead.
        groups_graph: Graph node labels, overridden by labels in paga_graph_params.
        pos: Supplied graph coordinates; None uses medians or cached positions.
        hover: Enable the existing observation, node and edge tooltips.
        zoom: Enable shared native x/y zoom and pan across the two panels.
        width: Per-panel plot width in pixels, default 300.
        height: Per-panel plot height in pixels, default 300.
        **paga_graph_params: Supported paga options, including threshold and add_pos.
            The graph shows labels on hover unless show_node_labels=True or custom labels
            are supplied. Labels make room for each other and the nodes while zooming.
            edge_slider=True adds a stored-edge display filter.
            Parent rendering restrictions apply; plot=False is unsupported here.

    Returns:
        A horizontal native composition when show=False, otherwise None.

    Raises:
        ImportError: If the supported optional dependencies are unavailable.
        TypeError: If the data or requested options have invalid types.
        ValueError: If required stored results or components are invalid.
        NotImplementedError: If a parent rendering option or panel mode is unsupported.

    Example:
        >>> sc.tl.paga(adata, groups="cell_type")
        >>> chart = gsc.pl.paga_compare(
        ...     adata, basis="umap", legend_fontweight="normal", zoom=True, show=False
        ... )
    """
    context = "gsc.pl.paga_compare"
    sc = _prepare_plot(show, save, context=context)
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=frameon,
        hover=hover,
        zoom=zoom,
    )
    if right_margin is not None or left_margin != 0.05:
        raise NotImplementedError(f"{context}: custom margins are unsupported.")
    if paga_graph_params.get("plot", True) is not True:
        raise NotImplementedError(f"{context}: plot=False is unsupported.")
    for name, value in (("title", title), ("title_graph", title_graph)):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{context}: {name} must be a string or None.")
    from anndata import AnnData
    import genome_spy as gs
    import pandas as pd
    from genome_spy.integrations.scanpy._embedding_data import (
        embedding_key,
        dimensions_for,
    )
    from genome_spy.integrations.scanpy._style import _font_size, POINTS_TO_PIXELS

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: adata must be AnnData.")
    stored = adata.uns.get("paga", {})
    key = stored.get("groups") if isinstance(stored, Mapping) else None
    if not isinstance(key, str) or key not in adata.obs:
        raise ValueError(
            f"{context}: stored PAGA results are required; run sc.tl.paga explicitly."
        )
    color = key if color is None else color
    if not isinstance(color, str):
        raise NotImplementedError(
            f"{context}: color must be a single observation key or gene."
        )
    if basis is None:
        basis = next(
            (
                name
                for name in ("draw_graph_fa", "umap", "tsne", "draw_graph_fr")
                if f"X_{name}" in adata.obsm
            ),
            "umap",
        )
    coordinate_key = embedding_key(adata, basis, context=context)
    dimensions = dimensions_for(components, None, adata.obsm[coordinate_key].shape[1])
    if len(dimensions) != 1:
        raise NotImplementedError(
            f"{context}: components must select one coordinate pair."
        )
    common_title = (color if title is None else title) if title_graph is None else None
    embedding_chart = _embedding(
        adata,
        basis,
        context,
        False,
        color=color,
        edges=edges,
        alpha=alpha,
        groups=groups,
        components=components,
        projection=projection,
        legend_loc=legend_loc,
        legend_fontsize=legend_fontsize,
        legend_fontweight=legend_fontweight,
        legend_fontoutline=legend_fontoutline,
        color_map=color_map,
        palette=palette,
        frameon=frameon,
        size=9 if size is None else size,
        title="" if title_graph is None else title,
        hover=hover,
        zoom=zoom,
        width=width,
        height=height,
        show=False,
        save=False,
    )
    if pos is None:
        if color == key:
            coordinates = pd.DataFrame(
                adata.obsm[coordinate_key][:, list(dimensions[0])],
                columns=["x", "y"],
                index=adata.obs_names,
            )
            pos = (
                coordinates.groupby(adata.obs[key], observed=True)
                .median()
                .sort_index()
                .to_numpy()
            )
        else:
            pos = stored.get("pos")
            if pos is None:
                raise ValueError(
                    f"{context}: non-group colors require supplied or cached PAGA positions."
                )
    labels = paga_graph_params.pop("labels", groups_graph)
    if legend_fontsize is not None:
        paga_graph_params["fontsize"] = _font_size(legend_fontsize) / POINTS_TO_PIXELS
    if legend_fontweight is not None:
        paga_graph_params["fontweight"] = {
            400: "normal",
            700: "bold",
            "regular": "normal",
        }.get(legend_fontweight, legend_fontweight)
    paga_graph_params.setdefault("show_node_labels", labels is not None)
    graph = paga(
        adata,
        colors=color,
        palette=palette if color == key else None,
        labels=labels,
        pos=pos,
        frameon=frameon,
        title="" if title_graph is None else title_graph,
        hover=hover,
        zoom=False,
        width=300 if width is None else width,
        height=300 if height is None else height,
        show=False,
        save=False,
        **paga_graph_params,
    )
    assert embedding_chart is not None and isinstance(graph, gs.LayerChart)
    # The graph inherits the embedding limits instead of contributing its own.
    graph = graph.encode(x=gs.X("_x:Q").axis(None), y=gs.Y("_y:Q").axis(None))
    chart = (
        gs.hconcat(embedding_chart, graph)
        .resolve_scale(
            x="shared",
            y="shared",
            color="independent",
            fill="independent",
            stroke="independent",
            size="independent",
        )
        .resolve_legend(default="independent", fill="collected")
    )
    if common_title:
        chart = chart.properties(title=common_title)
    return _finish_plot(chart, show, sc)


def paga_path(
    adata: AnnData,
    nodes: Sequence[str | int],
    keys: Sequence[str],
    *,
    use_raw: bool = True,
    annotations: Sequence[str] = ("dpt_pseudotime",),
    color_map: Any = None,
    color_maps_annotations: Mapping[str, Any] = MappingProxyType(
        dict(dpt_pseudotime="Greys")
    ),
    palette_groups: Sequence[str] | None = None,
    n_avg: int = 1,
    groups_key: str | None = None,
    xlim: tuple[int | None, int | None] = (None, None),
    title: str | None = None,
    left_margin: Any = None,
    ytick_fontsize: int | None = None,
    title_fontsize: int | None = None,
    show_node_names: bool = True,
    show_yticks: bool = True,
    show_colorbar: bool = True,
    legend_fontsize: Any = None,
    legend_fontweight: Any = None,
    normalize_to_zero_one: bool = False,
    as_heatmap: bool = True,
    return_data: bool = False,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    series_select: bool = False,
    ruler: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | tuple[TopLevelSpec, pd.DataFrame] | pd.DataFrame | None:
    """Show expression along supplied PAGA groups using stored DPT pseudotime.

    Description:
        Order cells within each requested group, smooth the concatenated values,
        then optionally normalize each key. Reuse shared Scanpy data access and
        native matrix tiles with original group bands and numeric annotations.
        Analysis remains explicit; no embeddings, PAGA or DPT are recomputed.
        Heatmaps require two keys and two smoothed cells. Lines use native
        round-cap rules with minor stroke differences. Native Greys
        differs from Scanpy's white-to-black annotation palette.

    Args:
        adata: AnnData with categorical groups and stored dpt_pseudotime.
        nodes: Ordered group names or integer category indices; repeats are kept.
        keys: Gene or numeric observation keys, retaining supplied order.
        use_raw: Use raw when available, otherwise X, as in Scanpy.
        annotations: Observation tracks; heatmaps support one numeric track. Lines show no tracks.
        color_map: Native heatmap scheme; None uses viridis. Inactive for lines.
        color_maps_annotations: Native schemes by annotation key; defaults to Greys.
        palette_groups: CSS colors in full category order; None reuses saved/default colors.
        n_avg: Full-window running average across concatenated cells.
        groups_key: Group column; None reads uns['paga']['groups'].
        xlim: Slice smoothed line samples, resetting x to zero; inactive for heatmaps.
        title: Optional chart title.
        left_margin: Only None; native layout reserves label space automatically.
        ytick_fontsize: Gene and track label size in points.
        title_fontsize: Title size in points.
        show_node_names: Label the supplied groups on their color band.
        show_yticks: Show key and track names.
        show_colorbar: Show the native expression color guide.
        legend_fontsize: Line legend font size in points or a standard name; inactive for heatmaps.
        legend_fontweight: Inactive, as in Scanpy.
        normalize_to_zero_one: Normalize each smoothed profile to zero through one.
        as_heatmap: True shows tiles and tracks; False connects adjacent samples with rules.
        return_data: Return the prepared table with the chart, or after display.
        show: Use Scanpy autoshow when unset; False returns the native chart.
        save: Only None/False; use native HTML/JSON export.
        hover: Include value and annotation tooltips.
        zoom: True navigates y; "xy" navigates both axes and aligned tracks.
        series_select: Add a dropdown to emphasize one plotted key.
        ruler: Show a native cursor along the path.
        show_values: Show fitted tile values; requires as_heatmap=True.
        width: Native plot area width in pixels.
        height: Native plot area height in pixels.

    Returns:
        A chart for show=False, otherwise None. With return_data=True, return
        (chart, table) for show=False, otherwise the table after displaying.

    Raises:
        ImportError: If the optional supported Scanpy version is unavailable.
        TypeError: If option types, groups or values are unsupported.
        ValueError: If metadata, node indices, bounds or window size are invalid.
        NotImplementedError: If categorical/multiple heatmap tracks, repeated line
            keys, custom margins, image saving or nonnative heatmap colors are requested.

    Example:
        >>> chart = gsc.pl.paga_path(adata, nodes=[0, 1], keys=["CD3D", "CD79A"], show=False)
    """
    context = "gsc.pl.paga_path"
    for name, value in {
        "use_raw": use_raw,
        "show_node_names": show_node_names,
        "show_yticks": show_yticks,
        "show_colorbar": show_colorbar,
        "normalize_to_zero_one": normalize_to_zero_one,
        "as_heatmap": as_heatmap,
        "return_data": return_data,
        "hover": hover,
        "show_values": show_values,
        "series_select": series_select,
        "ruler": ruler,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_grid_zoom(zoom, context=context)
    sc = _prepare_plot(show, save, context=context)
    if not as_heatmap and show_values:
        raise NotImplementedError(f"{context}: show_values requires as_heatmap=True.")
    if left_margin is not None:
        raise NotImplementedError(
            f"{context}: left_margin is unsupported; use native layout."
        )
    if title is not None and not isinstance(title, str):
        raise TypeError(f"{context}: title must be a string or None.")
    if as_heatmap and not isinstance(color_maps_annotations, Mapping):
        raise TypeError(f"{context}: color_maps_annotations must be a mapping.")
    from genome_spy.integrations.scanpy._paga_path_data import (
        prepare_paga_path,
        running_average,
    )
    from genome_spy.integrations.scanpy._paga_path_chart import (
        build_paga_path,
        build_paga_path_lines,
    )
    from genome_spy.integrations.scanpy._style import _palette

    prepared = prepare_paga_path(
        adata,
        nodes,
        keys,
        use_raw=use_raw,
        annotations=annotations,
        n_avg=n_avg,
        groups_key=groups_key,
        normalize_to_zero_one=normalize_to_zero_one,
        as_heatmap=as_heatmap,
    )
    categories = adata.obs[prepared.group_key].cat.categories
    if palette_groups is not None and (
        isinstance(palette_groups, str) or len(palette_groups) < len(categories)
    ):
        raise ValueError(
            f"{context}: palette_groups needs CSS colors for all categories."
        )
    palette, _ = _palette(
        adata, prepared.group_key, categories, palette_groups, context=context
    )
    if as_heatmap:
        chart = build_paga_path(
            prepared,
            categories=list(map(str, categories)),
            palette=palette,
            color_map=color_map,
            color_maps_annotations=color_maps_annotations,
            title=title,
            ytick_fontsize=ytick_fontsize,
            title_fontsize=title_fontsize,
            show_node_names=show_node_names,
            show_yticks=show_yticks,
            show_colorbar=show_colorbar,
            hover=hover,
            zoom=zoom,
            show_values=show_values,
            width=width,
            height=height,
            series_select=series_select,
            ruler=ruler,
        )
    else:
        chart = build_paga_path_lines(
            prepared,
            xlim=xlim,
            categories=list(map(str, categories)),
            palette=palette,
            show_node_names=show_node_names,
            normalized=normalize_to_zero_one,
            title=title,
            title_fontsize=title_fontsize,
            legend_fontsize=legend_fontsize,
            hover=hover,
            zoom=zoom,
            width=width,
            height=height,
            series_select=series_select,
            ruler=ruler,
        )
    shown = _finish_plot(chart, show, sc)
    if not return_data:
        return shown
    frame = prepared.values.copy()
    frame["groups"] = running_average(prepared.groups, n_avg)
    if "dpt_pseudotime" in prepared.annotations:
        frame["distance"] = prepared.annotations["dpt_pseudotime"].to_numpy()
    return frame if shown is None else (shown, frame)


def paga_adjacency(
    adata: AnnData,
    *,
    adjacency: str = "connectivities",
    adjacency_tree: str = "connectivities_tree",
    as_heatmap: bool = True,
    color_map: Any = None,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    labels: Collection[str] | None = None,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Display stored PAGA adjacency as a matrix or connectivity stripplot.

    Description:
        Read top-level uns matrices, as Scanpy's legacy entry does. Reuse native
        matrix tiles, color guides and navigation without reading expression,
        computing PAGA or changing AnnData. Dots mark tree nonzero entries
        at x=row, y=column, preserving Scanpy's orientation. Stripplot mode shows
        off-diagonal connectivity in light gray and tree-selected values in blue.
        Points grow gently on zoom; heatmap dots stay inside their cells.

    Args:
        adata: AnnData containing the explicitly stored adjacency matrices.
        adjacency: Top-level uns key for the sparse numeric matrix.
        adjacency_tree: Top-level uns key for the sparse tree matrix.
        as_heatmap: True shows matrix tiles; False shows connectivity by source group.
        color_map: Native heatmap scheme; None uses viridis. Inactive for stripplots.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use native HTML/JSON export.
        hover: Include matrix-value, tree-edge or stripplot connectivity tooltips.
        zoom: True enables y navigation; "xy" enables both axes.
        show_values: Show fitted heatmap values; requires as_heatmap=True.
        labels: Explicit group labels in adjacency row/column order; None keeps indices.
        width: Native plot width in pixels.
        height: Native plot height in pixels.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional supported Scanpy version is unavailable.
        TypeError: If AnnData, keys, matrix values or native options have unsupported types.
        ValueError: If matrices are missing, mismatched, infinite or too large.
        NotImplementedError: If stripplot cell labels, image saving or a nonnative
            heatmap scheme is requested.

    Example:
        >>> adata.uns["connectivities"] = adata.uns["paga"]["connectivities"]
        >>> adata.uns["connectivities_tree"] = adata.uns["paga"]["connectivities_tree"]
        >>> chart = gsc.pl.paga_adjacency(adata, show=False)
    """
    context = "gsc.pl.paga_adjacency"
    for name, value in {
        "as_heatmap": as_heatmap,
        "hover": hover,
        "show_values": show_values,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if not as_heatmap and show_values:
        raise NotImplementedError(f"{context}: show_values requires as_heatmap=True.")
    _check_grid_zoom(zoom, context=context)
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._paga_data import adjacency_values
    from genome_spy.integrations.scanpy._paga_chart import build_paga_adjacency

    values, points = adjacency_values(adata, adjacency, adjacency_tree)
    if labels is not None:
        from genome_spy.integrations.scanpy._matrix_chart import _labels

        labels = _labels(labels, len(values), "labels", context=context)
    chart = build_paga_adjacency(
        values,
        points,
        as_heatmap=as_heatmap,
        labels=labels,
        color_map=color_map,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
    )
    return _finish_plot(chart, show, sc)


def paga(
    adata: AnnData,
    *,
    threshold: float | None = None,
    color: Any = None,
    layout: str | None = None,
    layout_kwds: Mapping[str, Any] = MappingProxyType({}),
    init_pos: Any = None,
    root: Any = 0,
    labels: Any = None,
    single_component: bool = False,
    solid_edges: str = "connectivities",
    dashed_edges: str | None = None,
    transitions: str | None = None,
    fontsize: int | None = None,
    fontweight: str = "bold",
    fontoutline: int | None = None,
    text_kwds: Mapping[str, Any] = MappingProxyType({}),
    node_size_scale: float = 1.0,
    node_size_power: float = 0.5,
    edge_width_scale: float = 1.0,
    min_edge_width: float | None = None,
    max_edge_width: float | None = None,
    arrowsize: int = 30,
    title: str | None = None,
    left_margin: float = 0.01,
    random_state: int | None = 0,
    pos: Any = None,
    normalize_to_color: bool = False,
    cmap: Any = None,
    colorbar: bool | None = None,
    cb_kwds: Mapping[str, Any] = MappingProxyType({}),
    frameon: bool | None = None,
    add_pos: bool = True,
    export_to_gexf: bool = False,
    use_raw: bool = True,
    colors: Any = None,
    groups: Any = None,
    plot: bool = True,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool = False,
    width: float | None = None,
    height: float | None = None,
    palette: Any = None,
    edge_slider: bool = False,
    show_node_labels: bool = True,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Draw stored undirected PAGA connectivity graphs with native nodes and edges.

    Description:
        Read saved PAGA matrices and groups; gene colors read only the requested
        expression column. Never rerun PAGA analysis. Supplied positions are retained;
        otherwise Scanpy's public plot=False path computes the layout on a
        metadata-only object without creating a figure. Native rules, points
        and text draw the result.

    Args:
        adata: AnnData with stored PAGA graphs and categorical observation groups.
        threshold: Drop weights below this value; None uses 0.01, zero retains zeros.
        color: Group key, numeric observation key, gene, degree_solid/degree_dashed,
            CSS color or one CSS color per node. None uses group colors.
        layout: Scanpy layout, computed only when pos is None.
        layout_kwds: Keywords passed to Scanpy's public layout computation.
        init_pos: Initial layout coordinates; unused when pos is supplied.
        root: Scanpy tree-layout root; unused when pos is supplied.
        labels: One string per node; None uses category labels.
        single_component: Show only the largest thresholded solid component;
            ties keep the first group order. Filtering requires dashed_edges=None.
        solid_edges: Stored PAGA matrix key for black solid edges.
        dashed_edges: Optional stored matrix key for gray dashed edges.
        transitions: Unsupported directed-edge mode.
        fontsize: Native label size in points; None uses 10.
        fontweight: Native 'normal' or 'bold' label weight.
        fontoutline: Unsupported label outline.
        text_kwds: Only empty; use native chart styling for supported customization.
        node_size_scale: Multiply Scanpy's node areas by this nonnegative value.
        node_size_power: Exponent of stored size divided by its median.
        edge_width_scale: Multiply default 7.5-point weight-scaled widths.
        min_edge_width: Minimum solid-edge width in points.
        max_edge_width: Maximum solid/dashed width in points.
        arrowsize: Inactive without transitions.
        title: Optional plot title.
        left_margin: Only the pinned default; width/height set native dimensions.
        random_state: Scanpy layout seed.
        pos: Two coordinates per node; file-based positions are unsupported.
        normalize_to_color: Inactive without categorical mixtures.
        cmap: Native continuous scheme, default viridis; inactive for CSS colors.
        colorbar: None or True shows a native guide for numeric node colors.
            False hides that guide. Group colors have a native categorical legend.
        cb_kwds: Only empty in this preview.
        frameon: Draw the native view frame; None uses Scanpy's frame setting.
        add_pos: Store successful positions in uns['paga']['pos'], as in Scanpy.
        export_to_gexf: Unsupported; never writes an implicit graph file.
        use_raw: Use raw gene expression when present, otherwise X; False uses X.
            Inactive for metadata and degree colors.
        colors: Legacy alias overriding color when supplied.
        groups: Deprecated alias overriding labels when supplied.
        plot: False computes/caches positions without constructing a chart.
        show: Use Scanpy autoshow when unset; False returns the native chart.
        save: Only None/False; use native HTML/JSON saving.
        hover: Show group/cell counts, numeric color values and edge weights.
        zoom: Enable native x/y wheel zoom and pan.
        width: Native plot width in pixels, default 548.
        height: Native plot height in pixels, default 384.
        palette: Native addition: CSS category colors/mapping or native scheme
            for group colors. None reuses saved colors; inactive for other colors.
        edge_slider: Add a slider that hides displayed edges below a weight cutoff.
            It does not recover edges excluded by threshold or recompute node statistics.
        show_node_labels: Show native labels that make room for nodes and each other.
            False keeps group names on hover.
        **kwargs: Unsupported keywords fail clearly, including ax/cax.

    Returns:
        A native chart for show=False; otherwise None, including plot=False.

    Raises:
        ImportError: If the optional Scanpy/PAGA dependencies are unavailable.
        TypeError: If flags, metadata or native options are unsupported.
        ValueError: If stored graphs, positions, sizes or labels are invalid.
        NotImplementedError: If a requested color, edge or styling mode is unsupported.

    Example:
        >>> sc.tl.paga(adata, groups="louvain")
        >>> chart = gsc.pl.paga(adata, zoom=True, show=False)
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.paga"
    for name, flag in {
        "edge_slider": edge_slider,
        "show_node_labels": show_node_labels,
    }.items():
        if not isinstance(flag, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    node_color = colors if colors is not None else color
    if (
        edge_slider
        and isinstance(node_color, str)
        and node_color in {"degree_solid", "degree_dashed"}
    ):
        raise NotImplementedError(
            f"{context}: edge_slider cannot update graph-degree node colors; use a fixed threshold."
        )
    _check_kwargs(kwargs, set(), context=context)
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=frameon,
        hover=hover,
        zoom=zoom,
    )
    for name, value in {
        "single_component": single_component,
        "add_pos": add_pos,
        "export_to_gexf": export_to_gexf,
        "plot": plot,
        "normalize_to_color": normalize_to_color,
        "use_raw": use_raw,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    if colorbar is not None and not isinstance(colorbar, bool):
        raise TypeError(f"{context}: colorbar must be boolean or None.")
    unsupported = {
        "transitions": transitions is not None,
        "fontoutline": fontoutline is not None,
        "text_kwds": bool(text_kwds),
        "cb_kwds": bool(cb_kwds),
        "export_to_gexf": export_to_gexf,
        "left_margin": left_margin != 0.01,
    }
    if any(unsupported.values()):
        raise NotImplementedError(
            f"{context}: unsupported option(s): {', '.join(k for k, v in unsupported.items() if v)}."
        )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._paga_data import (
        prepare_paga,
        paga_nodes,
        paga_edges,
        largest_component,
    )

    key, positions, solid, dashed = prepare_paga(
        adata,
        threshold=threshold,
        solid_edges=solid_edges,
        dashed_edges=dashed_edges,
        pos=pos,
        layout=layout,
        layout_kwds=layout_kwds,
        init_pos=init_pos,
        root=root,
        random_state=random_state,
    )
    chart = None
    if plot:
        from genome_spy.integrations.scanpy._paga_chart import build_paga
        from genome_spy.integrations.scanpy._style import native_scheme
        import pandas as pd

        cmap = native_scheme(
            "viridis" if cmap is None else cmap, "cmap", context=context
        )
        if groups is not None:
            labels = groups
            sc.logging.warning(
                "`groups` is deprecated in `pl.paga`: use `labels` instead"
            )
        indices = None
        if single_component:
            kept = largest_component(solid)
            if len(kept) < len(positions):
                if dashed is not None:
                    raise ValueError(
                        f"{context}: single_component requires dashed_edges=None on disconnected graphs."
                    )
                indices = kept
        nodes, color_data = paga_nodes(
            adata,
            key,
            positions,
            color=colors if colors is not None else color,
            labels=labels,
            node_size_scale=node_size_scale,
            node_size_power=node_size_power,
            solid=solid,
            dashed=dashed,
            use_raw=use_raw,
            indices=indices,
            palette=palette,
        )
        if indices is not None:
            solid = solid.subgraph(indices)
        solid_table = paga_edges(
            solid,
            positions,
            edge_width_scale=edge_width_scale,
            min_edge_width=min_edge_width,
            max_edge_width=max_edge_width,
        )
        dashed_table = (
            paga_edges(
                dashed,
                positions,
                edge_width_scale=edge_width_scale,
                min_edge_width=None,
                max_edge_width=max_edge_width,
            )
            if dashed is not None
            else pd.DataFrame()
        )
        chart = build_paga(
            nodes,
            solid_table,
            dashed_table,
            fontsize=fontsize,
            fontweight=fontweight,
            frameon=sc.settings._frameon if frameon is None else frameon,
            title=title,
            hover=hover,
            zoom=zoom,
            width=width,
            height=height,
            cmap=cmap,
            colorbar=colorbar is not False,
            group_key=key,
            group_labels=list(map(str, adata.obs[key].cat.categories)),
            color_title=node_color if isinstance(node_color, str) else key,
            color_data=color_data,
            edge_slider=edge_slider,
            show_node_labels=show_node_labels,
        )
    if add_pos:
        adata.uns["paga"]["pos"] = positions.copy()
    return _finish_plot(chart, show, sc) if chart is not None else None


def dpt_timeseries(
    adata: AnnData,
    *,
    color_map: Any = None,
    show: bool | None = None,
    save: bool | None = None,
    as_heatmap: bool = True,
    marker: str | Sequence[str] = ".",
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot expression in saved DPT order using the existing time-series charts.

    Description:
        Index resident dense X with stored dpt_order_indices and retain saved
        dpt_changepoints. No trajectory analysis, sorting, smoothing or scaling
        runs. Heatmap and point modes reuse their existing preparation/renderers.
        Raw and layers are unused, as in Scanpy.

    Args:
        adata: AnnData with resident dense X and stored DPT indices/boundaries.
        color_map: Native heatmap scheme; None uses viridis. Unused for points.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the native chart's HTML/JSON saving.
        as_heatmap: Draw a variable-by-ordered-observation heatmap; False uses points.
        marker: Shared native point marker; unused in heatmap mode.
        hover: Show variable, ordered sample position and value tooltips.
        zoom: True navigates heatmap y or both point axes; 'xy' navigates both.
        show_values: Fit values inside heatmap cells; points reject True.
        width: Native plot-area width; defaults to the selected time-series chart.
        height: Native plot-area height; defaults to the selected time-series chart.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If flags, AnnData or expression storage are unsupported.
        ValueError: If saved indices, profiles, boundaries or dimensions are invalid.
        NotImplementedError: If native rendering cannot preserve a plotting option.

    Example:
        >>> sc.tl.dpt(adata, n_branchings=1)
        >>> chart = gsc.pl.dpt_timeseries(adata[:, genes], zoom="xy", show=False)
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.dpt_timeseries"
    for name, value in {
        "as_heatmap": as_heatmap,
        "hover": hover,
        "show_values": show_values,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_grid_zoom(zoom, context=context)
    if show_values and not as_heatmap:
        raise NotImplementedError(f"{context}: show_values requires heatmap output.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._timeseries_data import prepare_dpt_timeseries

    values, highlights = prepare_dpt_timeseries(adata)
    if adata.n_vars > 100:
        sc.logging.warning(
            "Plotting more than 100 genes might take some while, "
            "consider selecting only highly variable genes, for example."
        )
    options = dict(
        var_names=adata.var_names,
        highlights_x=highlights,
        xlabel="dpt order",
        hover=hover,
        width=width,
        height=height,
        context=context,
    )
    if as_heatmap:
        from genome_spy.integrations.scanpy._matrix_chart import (
            build_timeseries_heatmap,
        )

        chart = build_timeseries_heatmap(
            values, color_map=color_map, zoom=zoom, show_values=show_values, **options
        )
    else:
        from genome_spy.integrations.scanpy._timeseries_chart import build_timeseries

        chart = build_timeseries(
            values,
            xlim=[0, 1.3 * adata.n_obs],
            marker=marker,
            zoom=bool(zoom),
            **options,
        )
    return _finish_plot(chart, show, sc)


def dpt_groups_pseudotime(
    adata: AnnData,
    *,
    color_map: Any = None,
    palette: Any = None,
    show: bool | None = None,
    save: bool | str | None = None,
    marker: str | Sequence[str] = ".",
    hover: bool = True,
    zoom: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Compare stored DPT groups and pseudotime in two native time-series panels.

    Description:
        Read categorical dpt_groups, dpt_order, dpt_pseudotime and stored
        dpt_changepoints without reading expression or running analysis. Preserve
        category codes and supplied order coordinates. Palette assignment follows
        Scanpy's sorted observed groups, with a native DPT group legend.
        The lower panel colors by pseudotime, with a colorbar for continuous values.
        Missing or infinite pseudotimes are omitted from the lower panel only.

    Args:
        adata: AnnData with the stored DPT observation fields and boundaries.
        color_map: Native lower-panel color scheme; None uses viridis.
        palette: CSS color sequence for observed groups; None uses Scanpy's Vega 10.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use native chart HTML/JSON saving.
        marker: Supported shared point marker; differing per-group shapes reject.
        hover: Show the existing time-series sample, order and value tooltips.
        zoom: Enable independent native x/y zoom and pan in each panel.
        width: Each panel's plot-area width in pixels, default 496.
        height: Each panel's plot-area height in pixels, default 168.

    Returns:
        A native two-panel chart for show=False, otherwise displays and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If metadata types, flags or native styles are unsupported.
        ValueError: If stored fields, order, values, palettes or dimensions are invalid.
        NotImplementedError: If native rendering cannot preserve a plotting option.

    Example:
        >>> sc.tl.dpt(adata, n_branchings=1)
        >>> chart = gsc.pl.dpt_groups_pseudotime(adata, zoom=True, show=False)
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.dpt_groups_pseudotime"
    _check_point_options(
        context=context,
        width=width,
        height=height,
        frameon=None,
        hover=hover,
        zoom=zoom,
    )
    sc = _prepare_plot(show, save, context=context)
    import genome_spy as gs
    from genome_spy.integrations.scanpy._timeseries_data import prepare_dpt_groups
    from genome_spy.integrations.scanpy._timeseries_chart import build_timeseries

    groups, order, pseudotime, highlights = prepare_dpt_groups(adata)
    options = dict(
        time=order,
        highlights_x=highlights,
        marker=marker,
        hover=hover,
        zoom=zoom,
        width=496 if width is None else width,
        height=168 if height is None else height,
        context=context,
    )
    group_chart = build_timeseries(
        groups.cat.codes.to_numpy(),
        color=groups.to_numpy(),
        var_names=[str(v) for v in sorted(groups.unique())],
        ylabel="dpt groups",
        yticks=list(range(len(groups.cat.categories)))
        if len(groups.cat.categories) < 5
        else None,
        palette=palette,
        legend_style=gs.Legend(
            title="DPT group", orient="right", direction="vertical", symbolSize=49
        ),
        **options,
    )
    time_chart = build_timeseries(
        pseudotime.to_frame(),
        color=pseudotime,
        xlabel="dpt order",
        ylabel="pseudotime",
        yticks=[0, 1],
        color_map=color_map,
        colorbar=True,
        **options,
    )
    chart = gs.vconcat(group_chart, time_chart, spacing=10).resolve_scale(
        default="independent"
    )
    return _finish_plot(chart, show, sc)


def sim(
    adata: AnnData,
    *,
    tmax_realization: int | None = None,
    as_heatmap: bool = False,
    shuffle: bool = False,
    show: bool | None = None,
    save: bool | str | None = None,
    marker: str | Sequence[str] = ".",
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    series_select: bool = False,
    ruler: bool = False,
    run_select: bool = False,
    connect: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot supplied simulation realizations with the existing time-series charts.

    Description:
        Read X and var_names without running simulation or changing AnnData.
        Realization length comes from tmax_realization, then uns['tmax_write'],
        then n_obs. It sets boundaries and one-based tick labels, never truncates
        X. Shuffle uses Scanpy's seed-1 permutation without changing global random
        state; as in Scanpy, shuffled output is always points.

    Args:
        adata: AnnData containing resident dense samples-by-variables X.
        tmax_realization: Positive observations per realization; None uses metadata.
        as_heatmap: Use the existing heatmap renderer unless shuffle is True.
        shuffle: Permute all observations deterministically before point plotting.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use native chart HTML/JSON saving.
        marker: Supported shared point marker; unused for heatmap output.
        hover: Show the existing time-series value tooltips.
        zoom: True navigates both point axes or heatmap y; 'xy' navigates both.
        show_values: Fit numeric labels inside heatmap cells; points reject True.
        series_select: Add a dropdown to emphasize one gene in points or heatmap.
        ruler: Show a native cursor for reading sample positions.
        run_select: Add a run dropdown; unavailable for shuffled samples.
        connect: Join adjacent simulation samples within each run; point output only.
            Missing values leave gaps. Never connects different runs.
        width: Native plot-area width; defaults to the selected time-series chart.
        height: Native plot-area height; defaults to the selected time-series chart.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If flags, AnnData or expression storage are unsupported.
        ValueError: If realization length, profiles, labels or dimensions are invalid.
        NotImplementedError: If a requested native style or delivery is unsupported.

    Example:
        >>> simulation = sc.datasets.krumsiek11()[:, ["Gata2", "Gata1", "Pu.1"]]
        >>> chart = gsc.pl.sim(simulation, tmax_realization=160, show=False)
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.sim"
    for name, value in {
        "as_heatmap": as_heatmap,
        "shuffle": shuffle,
        "hover": hover,
        "show_values": show_values,
        "series_select": series_select,
        "ruler": ruler,
        "run_select": run_select,
        "connect": connect,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_grid_zoom(zoom, context=context)
    if show_values and (not as_heatmap or shuffle):
        raise NotImplementedError(
            f"{context}: show_values requires unshuffled heatmap output."
        )
    if shuffle and (run_select or connect):
        raise NotImplementedError(
            f"{context}: run_select and connect require unshuffled samples."
        )
    if connect and as_heatmap:
        raise NotImplementedError(
            f"{context}: connect requires point output (as_heatmap=False)."
        )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._timeseries_data import prepare_sim

    values, highlights, ticks = prepare_sim(adata, tmax_realization, shuffle)
    realization_length = highlights[0] if highlights else adata.n_obs
    if as_heatmap and not shuffle:
        from genome_spy.integrations.scanpy._matrix_chart import (
            build_timeseries_heatmap,
        )

        chart = build_timeseries_heatmap(
            values,
            var_names=adata.var_names,
            highlights_x=highlights,
            color_map=None,
            hover=hover,
            zoom=zoom,
            show_values=show_values,
            width=width,
            height=height,
            context=context,
            xtick_labels=ticks,
            series_select=series_select,
            ruler=ruler,
            run_select=run_select,
            realization_length=realization_length,
        )
    else:
        from genome_spy.integrations.scanpy._timeseries_chart import build_timeseries

        chart = build_timeseries(
            values,
            var_names=adata.var_names,
            highlights_x=highlights,
            xlabel="index (arbitrary order)" if shuffle else "realizations",
            xlim=[0, 1.25 * adata.n_obs],
            marker=marker,
            hover=hover,
            zoom=bool(zoom),
            connect=connect,
            width=width,
            height=height,
            context=context,
            xtick_labels=None if shuffle else ticks,
            series_select=series_select,
            ruler=ruler,
            run_select=run_select,
            realization_length=realization_length,
        )
    return _finish_plot(chart, show, sc)


def timeseries(
    X: ArrayLike,
    *,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool = False,
    series_select: bool = False,
    ruler: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Plot supplied ordered profiles as points, as Scanpy's timeseries helper does.

    Description:
        Preserve supplied time coordinates, sample order and subset draw order.
        No sorting by time, line interpolation, smoothing or analysis runs.
        Multi-column inputs use palette colors; a single column requires color.
        Floating color values are continuous; other sortable values define groups.

    Args:
        X: Resident numeric vector or samples-by-variables matrix/table.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the native chart's HTML/JSON export.
        hover: Show series, source sample position, time, value and numeric color.
        zoom: Enable native wheel zoom and drag panning on both axes.
        series_select: Add a dropdown to emphasize one series without filtering samples.
        ruler: Show a native cursor for reading time positions.
        width: Native plot-area width in pixels, default 992.
        height: Native plot-area height in pixels, default 739.2.
        **kwargs: Scanpy's time=None, color=None, var_names=(), highlights_x=(),
            xlabel="", ylabel="gene expression", yticks=None, xlim=None,
            legend=True, palette=None, color_map="viridis", marker=".".
            Palette accepts CSS color sequences; color_map uses native schemes.
            Markers reuse the supported embedding shapes; different per-subset
            shapes, repeated labels and Matplotlib axes/cyclers are unsupported.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If arguments, numeric sources or vectors are unsupported.
        ValueError: If shapes, labels, colors, bounds or sizes are invalid.
        NotImplementedError: If native rendering cannot preserve an option.

    Example:
        >>> chart = gsc.pl.timeseries(
        ...     profiles, time=times, var_names=genes, zoom=True, show=False
        ... )
        >>> chart.display(inline=True)
    """
    return _timeseries_plot(
        X,
        kwargs,
        context="gsc.pl.timeseries",
        show=show,
        save=save,
        hover=hover,
        zoom=zoom,
        series_select=series_select,
        ruler=ruler,
        width=width,
        height=height,
    )


def timeseries_subplot(
    X: ArrayLike,
    *,
    time: ArrayLike | None = None,
    color: ArrayLike | None = None,
    var_names: Collection[str] = (),
    highlights_x: Collection[float] = (),
    xlabel: str | None = "",
    ylabel: str | None = "gene expression",
    yticks: Collection[float] | None = None,
    xlim: Collection[float] | None = None,
    legend: bool = True,
    palette: Any = None,
    color_map: Any = "viridis",
    marker: str | Sequence[str] = ".",
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool = False,
    series_select: bool = False,
    ruler: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Build a supplied-profile point panel for native chart composition.

    Description:
        Use the same preparation and renderer as timeseries, preserving supplied
        time, sample order and color subsets. Compose returned panels with
        genome_spy.hconcat/vconcat; no current figure or Matplotlib axes are used.

    Args:
        X: Resident numeric vector or samples-by-variables matrix/table.
        time: Supplied sample coordinates; None uses positions.
        color: Single-variable sample colors; floating first values are continuous.
        var_names: Distinct series or category labels; empty hides the legend.
        highlights_x: Finite positions for clipped dashed vertical rules.
        xlabel: Horizontal axis label.
        ylabel: Vertical axis label.
        yticks: Explicit finite ticks, expanding the vertical limits if needed.
        xlim: Explicit finite horizontal limits, including reversed limits.
        legend: Show the native series guide when var_names is supplied.
        palette: CSS color sequence for variables or single-variable categories.
        color_map: Native scheme for continuous single-variable colors.
        marker: Shared native marker, or an identical marker per subset.
        show: Use Scanpy autoshow when unset; False returns a composable chart.
        save: Only None/False; use the native chart's HTML/JSON export.
        hover: Show series, source position, time, value and numeric color.
        zoom: Enable native wheel zoom and panning on both axes.
        series_select: Add a dropdown to emphasize one series without filtering samples.
        ruler: Show a native cursor for reading time positions.
        width: Native plot-area width in pixels, default 496.
        height: Native plot-area height in pixels, default 369.6.
        **kwargs: Unsupported keywords fail clearly; ax and return_fig are omitted.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If arguments, sources or plotting options are unsupported.
        ValueError: If shapes, labels, bounds or dimensions are invalid.
        NotImplementedError: If native rendering cannot preserve an option.

    Example:
        >>> left = gsc.pl.timeseries_subplot(profiles, show=False)
        >>> right = gsc.pl.timeseries_subplot(other_profiles, show=False)
        >>> chart = gs.hconcat(left, right).resolve_scale(default="independent")
    """
    return _timeseries_plot(
        X,
        dict(
            time=time,
            color=color,
            var_names=var_names,
            highlights_x=highlights_x,
            xlabel=xlabel,
            ylabel=ylabel,
            yticks=yticks,
            xlim=xlim,
            legend=legend,
            palette=palette,
            color_map=color_map,
            marker=marker,
            **kwargs,
        ),
        context="gsc.pl.timeseries_subplot",
        show=show,
        save=save,
        hover=hover,
        zoom=zoom,
        series_select=series_select,
        ruler=ruler,
        width=496 if width is None else width,
        height=369.6 if height is None else height,
    )


def _timeseries_plot(
    X: Any,
    options: dict[str, Any],
    *,
    context: str,
    show: bool | None,
    save: bool | str | None,
    hover: bool,
    zoom: bool,
    series_select: bool,
    ruler: bool,
    width: float | None,
    height: float | None,
) -> TopLevelSpec | None:
    """Validate either time-series entry and deliver its shared native point chart."""
    for name, value in {
        "hover": hover,
        "zoom": zoom,
        "series_select": series_select,
        "ruler": ruler,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_kwargs(
        options,
        {
            "time",
            "color",
            "var_names",
            "highlights_x",
            "xlabel",
            "ylabel",
            "yticks",
            "xlim",
            "legend",
            "palette",
            "color_map",
            "marker",
        },
        context=context,
    )
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._timeseries_chart import build_timeseries

    chart = build_timeseries(
        X,
        hover=hover,
        zoom=zoom,
        series_select=series_select,
        ruler=ruler,
        width=width,
        height=height,
        context=context,
        **options,
    )
    return _finish_plot(chart, show, sc)


def timeseries_as_heatmap(
    X: ArrayLike,
    *,
    var_names: Collection[str] = (),
    highlights_x: Collection[float] = (),
    color_map: Any = None,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Display supplied ordered profiles as a variable-by-sample heatmap.

    Description:
        Reuse the matrix renderer without sorting, normalizing or computing time.
        Match Scanpy's transpose, first variable at the bottom, center-cropped
        limits and dashed highlights. Missing values stay blank. Matplotlib
        colormap objects and global figure settings are unsupported.

    Args:
        X: Resident numeric matrix with samples in rows and variables in columns.
        var_names: Variable labels; empty uses positions, 2D uses the first column.
        highlights_x: Finite sample positions for dashed vertical rules.
        color_map: Native GenomeSpy scheme; None uses viridis.
        show: Display according to Scanpy's autoshow when unset.
        save: Only None/False; use the returned chart's HTML/JSON export.
        hover: Include row (variable), column (sample position) and value tooltips.
        zoom: True enables y-only zoom/panning; "xy" also enables x navigation.
        show_values: Show values to two decimals when cells have enough room.
        width: Native tile-area width in pixels, default 372.
        height: Native tile-area height in pixels, default 616.

    Returns:
        A native chart for show=False, otherwise displays it and returns None.

    Raises:
        ImportError: If the optional Scanpy version is unavailable.
        TypeError: If the source, labels or flags are unsupported.
        ValueError: If values, shape, labels, highlights or sizes are invalid.
        NotImplementedError: If saving or a nonnative color scheme is requested.

    Example:
        >>> chart = gsc.pl.timeseries_as_heatmap(
        ...     profiles, var_names=genes, zoom="xy", show=False
        ... )
        >>> chart.display(inline=True)
    """
    context = "gsc.pl.timeseries_as_heatmap"
    for name, value in {"hover": hover, "show_values": show_values}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    _check_grid_zoom(zoom, context=context)
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._matrix_chart import build_timeseries_heatmap

    chart = build_timeseries_heatmap(
        X,
        var_names=var_names,
        highlights_x=highlights_x,
        color_map=color_map,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
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
    show_values: bool | None = None,
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
        show_correlation_numbers: Scanpy name for fitted two-decimal tile labels.
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
        show_values: Common matrix option for fitted tile labels. None follows
            show_correlation_numbers; False conflicts with that flag set True.
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
        ...     pbmc, "bulk_labels", show_values=True, show=False
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
    # Retain Scanpy's flag while allowing the same option as other matrices.
    if show_values is None:
        show_values = show_correlation_numbers
    elif not isinstance(show_values, bool):
        raise TypeError(f"{context}: show_values must be boolean or None.")
    elif show_correlation_numbers and not show_values:
        raise ValueError(
            f"{context}: show_values=False conflicts with show_correlation_numbers=True."
        )
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
        numbers=show_values,
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


def ranking(
    adata: AnnData,
    attr: Literal["var", "obs", "uns", "varm", "obsm"],
    keys: str | Sequence[str],
    *,
    dictionary: str | None = None,
    indices: Sequence[int] | None = None,
    labels: str | Sequence[str] | None = None,
    color: Any = "black",
    n_points: int = 30,
    log: bool = False,
    include_lowest: bool = False,
    show: bool | None = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot ranked labels from scores already stored in AnnData.

    Reads supplied attributes or nested dictionaries without computing analysis.
    Native text panels preserve Scanpy's score sorting and extreme-rank gap.

    Args:
        adata: AnnData containing the scores.
        attr: Attribute containing score columns or a dictionary.
        keys: Score names, or an array key when selecting indices.
        dictionary: Nested dictionary key within the attribute.
        indices: Array columns to display as separate panels.
        labels: Labels per score row, a numbered prefix, or automatic labels.
        color: Opaque native CSS text color.
        n_points: Rank count; Scanpy includes one extra label without include_lowest.
        log: Take the natural logarithm of positive scores before sorting.
        include_lowest: Show high and low scores with a gap when ranks are omitted.
        show: Display once, or return the native chart when False.
        hover: Show the label, score and zero-based rank in native tooltips.
        width: Native width per panel, default 300 logical pixels.
        height: Native height per panel, default 300 logical pixels.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        ValueError: If scores, labels, counts or dimensions are invalid.
        NotImplementedError: If the color needs Matplotlib conversion.

    Example:
        >>> chart = gsc.pl.ranking(adata, "varm", "PCs", indices=[0, 1], show=False)
    """
    context = "gsc.pl.ranking"
    for name, value in {
        "log": log,
        "include_lowest": include_lowest,
        "hover": hover,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    sc = _prepare_plot(show, False, context=context)
    from genome_spy.integrations.scanpy._ranked_data import attribute_rank_panels
    from genome_spy.integrations.scanpy._ranking_chart import build_ranking

    panels = attribute_rank_panels(
        adata,
        attr,
        keys,
        dictionary=dictionary,
        indices=indices,
        labels=labels,
        n_points=n_points,
        log=log,
        include_lowest=include_lowest,
    )
    chart = build_ranking(
        panels,
        sharey=False,
        fontsize=8,
        color=color,
        hover=hover,
        width=width,
        height=height,
        context=context,
    )
    return _finish_plot(chart, show, sc)


def pca_loadings(
    adata: AnnData,
    components: str | Sequence[int] | None = None,
    *,
    include_lowest: bool = True,
    n_points: int | None = None,
    show: bool | None = None,
    save: str | bool | None = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Rank genes by their stored principal-component loadings.

    Reads varm["PCs"] and variable names, using the same rank panels as ranking.
    Neither PCA nor expression extraction runs, and AnnData stays unchanged.
    The display adds 30% of the score range above the labels' loading values.

    Args:
        adata: AnnData with resident NumPy loadings in varm["PCs"].
        components: One-based components in display order; default first three.
        include_lowest: Show both loading extremes, with a gap for omitted ranks.
        n_points: Rank count, default min(30, adata.n_vars). Without include_lowest,
            Scanpy includes one extra label when available.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show gene name, loading score and displayed rank.
        width: Native width per panel, default 300 logical pixels.
        height: Native height per panel, default 300 logical pixels.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If AnnData, flags or loading storage are unsupported.
        ValueError: If stored loadings, components, counts or dimensions are invalid.
        NotImplementedError: If saving requests Matplotlib output.

    Example:
        >>> chart = gsc.pl.pca_loadings(adata, components="1,2", show=False)
    """
    context = "gsc.pl.pca_loadings"
    for name, value in {"include_lowest": include_lowest, "hover": hover}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    sc = _prepare_plot(show, save, context=context)
    from anndata import AnnData
    from genome_spy.integrations.scanpy._ranked_data import (
        _count,
        attribute_rank_panels,
    )
    from genome_spy.integrations.scanpy._ranking_chart import build_ranking

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    if "PCs" not in adata.varm:
        raise ValueError(
            f"{context}: missing varm['PCs']; run sc.pp.pca explicitly first."
        )
    # Loadings select individual one-based components, rather than embedding pairs.
    try:
        if components is None:
            chosen = [1, 2, 3]
        elif isinstance(components, str):
            chosen = [int(value) for value in components.split(",")]
        else:
            chosen = list(components)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{context}: components must be one-based integers."
        ) from error
    shape = adata.varm["PCs"].shape
    if (
        len(shape) != 2
        or not chosen
        or any(
            isinstance(value, bool)
            or not isinstance(value, Integral)
            or not 1 <= value <= shape[1]
            for value in chosen
        )
    ):
        raise ValueError(f"{context}: components must be available one-based integers.")
    count = _count(
        min(30, adata.n_vars) if n_points is None else n_points,
        "n_points",
        context=context,
    )
    if count > adata.n_vars:
        raise ValueError(f"{context}: n_points exceeds the {adata.n_vars} variables.")
    panels = attribute_rank_panels(
        adata,
        "varm",
        "PCs",
        dictionary=None,
        indices=[int(value) - 1 for value in chosen],
        labels=None,
        n_points=count,
        log=False,
        include_lowest=include_lowest,
        context=context,
    )
    chart = build_ranking(
        panels,
        sharey=False,
        fontsize=8,
        color="black",
        hover=hover,
        width=width,
        height=height,
        context=context,
        headroom=0.3,
    )
    return _finish_plot(chart, show, sc)


def pca_variance_ratio(
    adata: AnnData,
    n_pcs: int = 30,
    *,
    log: bool = False,
    show: bool | None = None,
    save: bool | str | None = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
) -> TopLevelSpec | None:
    """Plot ranked variance ratios from stored PCA results.

    Reads uns["pca"]["variance_ratio"] through the shared ranking helpers.
    log=True takes the natural logarithm before sorting, as Scanpy does;
    PCA and expression access never run, and stored results stay unchanged.
    The display adds 30% of the score range above the plotted values for labels.

    Args:
        adata: AnnData with a resident variance-ratio vector in uns["pca"].
        n_pcs: Positive rank count; Scanpy includes one extra PC when available.
        log: Take the natural logarithm of positive ratios before ranking.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show the original PC label, plotted score and displayed rank.
        width: Native plot width, default 300 logical pixels.
        height: Native plot height, default 300 logical pixels.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If AnnData, flags or variance-ratio storage are unsupported.
        ValueError: If ratios, log inputs, rank counts or dimensions are invalid.
        NotImplementedError: If saving requests Matplotlib output.

    Example:
        >>> chart = gsc.pl.pca_variance_ratio(adata, n_pcs=10, log=True, show=False)
    """
    context = "gsc.pl.pca_variance_ratio"
    for name, value in {"log": log, "hover": hover}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    sc = _prepare_plot(show, save, context=context)
    import numpy as np
    from anndata import AnnData
    from genome_spy.integrations.scanpy._ranked_data import (
        _count,
        attribute_rank_panels,
    )
    from genome_spy.integrations.scanpy._ranking_chart import build_ranking

    if not isinstance(adata, AnnData):
        raise TypeError(f"{context}: expected AnnData.")
    stored = adata.uns.get("pca")
    if not isinstance(stored, Mapping) or "variance_ratio" not in stored:
        raise ValueError(
            f"{context}: missing uns['pca']['variance_ratio']; run sc.pp.pca explicitly first."
        )
    ratios = stored["variance_ratio"]
    # Reject lazy vectors before table construction can materialize them.
    if (
        isinstance(ratios, (str, bytes))
        or not isinstance(ratios, (np.ndarray, Sequence))
        or getattr(ratios, "ndim", 1) != 1
    ):
        raise TypeError(
            f"{context}: variance_ratio requires a resident one-dimensional vector."
        )
    count = _count(n_pcs, "n_pcs", context=context)
    panels = attribute_rank_panels(
        adata,
        "uns",
        "variance_ratio",
        dictionary="pca",
        indices=None,
        labels="PC",
        n_points=count,
        log=log,
        include_lowest=False,
        context=context,
    )
    chart = build_ranking(
        panels,
        sharey=False,
        fontsize=8,
        color="black",
        hover=hover,
        width=width,
        height=height,
        context=context,
        headroom=0.3,
    )
    return _finish_plot(chart, show, sc)


def pca_overview(
    adata: AnnData,
    *,
    show: bool | None = None,
    save: str | bool | None = None,
    **params: Any,
) -> TopLevelSpec | None:
    """Combine stored PCA coordinates, loadings and variance ratios.

    Reuses pca, pca_loadings and pca_variance_ratio in Scanpy's display order.
    Cell positions sit above two diagnostic rows: PC1/PC2, then PC3/variance.
    Plotting never computes PCA, filters genes or modifies supplied results.

    Args:
        adata: AnnData containing the stored results required by all three plots.
        show: Display once, return the chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        **params: Supported pca options, including color, components, hover, zoom,
            width and height. These affect only the embedding section. Loadings
            use 280-pixel panels in two columns; other diagnostic defaults remain.

    Returns:
        A vertically composed native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy dependency is unavailable.
        TypeError: If options or stored result types are unsupported.
        ValueError: If required results, selected values or dimensions are invalid.
        NotImplementedError: If a parent plot's rendering option is unsupported.

    Example:
        >>> chart = gsc.pl.pca_overview(adata, color="cell_type", show=False)
    """
    context = "gsc.pl.pca_overview"
    sc = _prepare_plot(show, save, context=context)
    import genome_spy as gs

    # Build every child before displaying, so a failed diagnostic leaves no output.
    embedding_chart = pca(adata, show=False, save=False, **params)
    loadings_chart = pca_loadings(
        adata, components="1,2", width=280, show=False, save=False
    )
    third_loading = pca_loadings(
        adata, components="3", width=280, show=False, save=False
    )
    variance_chart = pca_variance_ratio(adata, show=False, save=False)
    assert embedding_chart is not None and isinstance(loadings_chart, gs.ConcatChart)
    assert third_loading is not None and variance_chart is not None
    # Keep PC3 and variance together to avoid an empty cell.
    last_row = gs.hconcat(third_loading, variance_chart, spacing=4).resolve_scale(
        x="independent", y="independent"
    )
    chart = (
        gs.vconcat(
            # This wrapper keeps the cell plot at its requested width.
            gs.hconcat(embedding_chart),
            loadings_chart.properties(spacing=4),
            last_row,
            spacing=4,
        )
        .resolve_scale(x="independent", y="independent", color="independent")
        .resolve_legend(default="independent")
    )
    return _finish_plot(chart, show, sc)


def rank_genes_groups(
    adata: AnnData,
    groups: str | Sequence[str] | None = None,
    *,
    n_genes: int = 20,
    gene_symbols: str | None = None,
    key: str | None = "rank_genes_groups",
    fontsize: int = 8,
    ncols: int = 4,
    sharey: bool = True,
    show: bool | None = None,
    save: bool | None = None,
    hover: bool = True,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot gene labels at their stored differential-expression rank and score.

    Uses existing results only; neither analysis nor expression extraction runs.
    Group titles, requested order, score bounds and shared-y behavior follow Scanpy.

    Args:
        adata: AnnData with stored rank_genes_groups results.
        groups: Ranked groups to show, in the requested order.
        n_genes: Positive number of stored ranks per group.
        gene_symbols: Annotation column in the ranking's raw or variable source.
        key: Stored result key.
        fontsize: Gene-label font size in points.
        ncols: Maximum panel columns.
        sharey: Use common score bounds across panels.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Show gene label, score and zero-based rank.
        width: Native width per panel, default 300 logical pixels.
        height: Native height per panel, default 300 logical pixels.
        **kwds: The n_panels_per_row alias for ncols; other options error.

    Returns:
        A native chart when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If forwarded options or flags are invalid.
        ValueError: If stored results, names or score values are invalid.
        NotImplementedError: If saving requests Matplotlib output.

    Example:
        >>> chart = gsc.pl.rank_genes_groups(pbmc, n_genes=5, show=False)
    """
    context = "gsc.pl.rank_genes_groups"
    _check_kwargs(kwds, {"n_panels_per_row"}, context=context)
    for name, value in {"sharey": sharey, "hover": hover}.items():
        if not isinstance(value, bool):
            raise TypeError(f"{context}: {name} must be boolean.")
    sc = _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._ranked_data import _count, gene_rank_panels
    from genome_spy.integrations.scanpy._ranking_chart import build_ranking

    columns = _count(kwds.get("n_panels_per_row", ncols), "ncols", context=context)
    panels = gene_rank_panels(
        adata, groups, key=key, n_genes=n_genes, gene_symbols=gene_symbols
    )
    chart = build_ranking(
        panels,
        ncols=columns,
        sharey=sharey,
        fontsize=fontsize,
        color="black",
        hover=hover,
        width=width,
        height=height,
        context=context,
        headroom=0.3,
        ylabel="score",
        bottom_labels=True,
    )
    return _finish_plot(chart, show, sc)


def _ranked_expression(
    plot: Callable[..., TopLevelSpec | None],
    adata: AnnData,
    groups: Any,
    *,
    n_genes: int | None,
    groupby: str | None,
    values_to_plot: str | None,
    var_names: Any,
    gene_symbols: str | None,
    min_logfoldchange: float | None,
    key: str | None,
    show: bool | None,
    save: bool | None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Select stored marker slots once, then delegate to an existing expression plot."""
    context = f"gsc.pl.rank_genes_groups_{plot.__name__}"
    if "ax" in kwds or "return_fig" in kwds:
        _check_kwargs(kwds, set(), context=context)
    if "dot_color_df" in kwds or "values_df" in kwds:
        raise TypeError(f"{context}: use the parent plot for supplied summary tables.")
    _prepare_plot(show, save, context=context)
    from genome_spy.integrations.scanpy._ranked_data import (
        _ranking_table,
        ranked_features,
        ranked_statistic,
        stored_ranking,
    )

    # One detached result serves both marker selection and statistic colors.
    ranking = None
    if values_to_plot is not None:
        result, ranking_groups = stored_ranking(adata, key, None, context=context)
        ranking = _ranking_table(
            adata,
            result,
            ranking_groups,
            key=key,
            gene_symbols=gene_symbols,
            min_logfoldchange=None,
            context=context,
        )
    markers, grouping = ranked_features(
        adata,
        groups,
        n_genes=n_genes,
        groupby=groupby,
        var_names=var_names,
        gene_symbols=gene_symbols,
        min_logfoldchange=min_logfoldchange,
        key=key,
        context=context,
        table=ranking,
    )
    # Stored colors replace means; the parent still owns expression fractions.
    if values_to_plot is not None:
        table = ranked_statistic(
            adata,
            markers,
            values_to_plot,
            key=key,
            gene_symbols=gene_symbols,
            context=context,
            table=ranking,
        )
        kwds["dot_color_df" if plot is dotplot else "values_df"] = table
        title = (
            "log fold change"
            if values_to_plot == "logfoldchanges"
            else values_to_plot.replace("_", " ").replace("pvals", "p-value")
        )
        kwds.setdefault("colorbar_title", title)
    kwds.setdefault("dendrogram", True)
    return plot(
        adata,
        markers,
        grouping,
        gene_symbols=gene_symbols,
        show=show,
        save=save,
        **kwds,
    )


def rank_genes_groups_dotplot(
    adata: AnnData,
    groups: str | Sequence[str] | None = None,
    *,
    n_genes: int | None = None,
    groupby: str | None = None,
    values_to_plot: Literal[
        "scores",
        "logfoldchanges",
        "pvals",
        "pvals_adj",
        "log10_pvals",
        "log10_pvals_adj",
    ]
    | None = None,
    var_names: Sequence[str] | Mapping[str, Sequence[str]] | None = None,
    gene_symbols: str | None = None,
    min_logfoldchange: float | None = None,
    key: str | None = None,
    show: bool | None = None,
    save: bool | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    highlight: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot stored ranked genes through the existing native dotplot.

    Selects top or tail genes with Scanpy's public getter. Colors show means or
    stored statistics; sizes always show expressing-cell fractions.

    Args:
        adata: AnnData containing stored rankings and expression.
        groups: Rank lists to select; does not filter expression groups or cells.
        n_genes: Genes per list, default 10; negative selects the stored tail.
        groupby: Expression grouping key, default the ranking's groupby.
        values_to_plot: Stored statistic for colors, or None for expression means.
            log10_pvals and log10_pvals_adj use negative base-10 logarithms.
        var_names: Explicit markers instead of n_genes, retaining repeated slots.
        gene_symbols: Variable annotation used for gene labels and lookup.
        min_logfoldchange: Strict lower stored log-fold-change threshold.
        key: Stored ranking key, default rank_genes_groups.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Enable the parent plot's native summary tooltips.
        zoom: True navigates y only; "xy" navigates both axes.
        highlight: Enable the native row/column ruler.
        width: Parent plot width in logical pixels.
        height: Parent plot height in logical pixels.
        **kwds: Existing dotplot options; dendrogram defaults True.

    Returns:
        A native dotplot when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        ValueError: If stored rankings or gene-selection options are invalid.
        TypeError: If forwarded options are unsupported.
        NotImplementedError: If renderer options are unsupported.

    Example:
        >>> chart = gsc.pl.rank_genes_groups_dotplot(pbmc, n_genes=3, show=False)
    """
    return _ranked_expression(
        dotplot,
        adata,
        groups,
        n_genes=n_genes,
        groupby=groupby,
        values_to_plot=values_to_plot,
        var_names=var_names,
        gene_symbols=gene_symbols,
        min_logfoldchange=min_logfoldchange,
        key=key,
        show=show,
        save=save,
        hover=hover,
        zoom=zoom,
        highlight=highlight,
        width=width,
        height=height,
        **kwds,
    )


def rank_genes_groups_matrixplot(
    adata: AnnData,
    groups: str | Sequence[str] | None = None,
    *,
    n_genes: int | None = None,
    groupby: str | None = None,
    values_to_plot: Literal[
        "scores",
        "logfoldchanges",
        "pvals",
        "pvals_adj",
        "log10_pvals",
        "log10_pvals_adj",
    ]
    | None = None,
    var_names: Sequence[str] | Mapping[str, Sequence[str]] | None = None,
    gene_symbols: str | None = None,
    min_logfoldchange: float | None = None,
    key: str | None = None,
    show: bool | None = None,
    save: bool | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot stored ranked genes through the existing native matrixplot.

    Reuses ranked marker selection, supplied statistic tables and parent chart
    helpers. Stored statistics bypass expression scaling, as in Scanpy.

    Args:
        adata: AnnData containing stored rankings and expression.
        groups: Rank lists to select; does not filter expression groups or cells.
        n_genes: Genes per list, default 10; negative selects the stored tail.
        groupby: Expression grouping key, default the ranking's groupby.
        values_to_plot: Stored statistic for colors, or None for expression means.
            log10_pvals and log10_pvals_adj use negative base-10 logarithms.
        var_names: Explicit markers instead of n_genes.
        gene_symbols: Variable annotation used for gene labels and lookup.
        min_logfoldchange: Strict lower stored log-fold-change threshold.
        key: Stored ranking key, default rank_genes_groups.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Enable the parent plot's native summary tooltips.
        zoom: True navigates y only; "xy" navigates both axes.
        show_values: Show fitted plotted values when tiles have room.
        width: Parent plot width in logical pixels.
        height: Parent plot height in logical pixels.
        **kwds: Existing matrixplot options; dendrogram defaults True.

    Returns:
        A native matrixplot when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        ValueError: If stored rankings or gene-selection options are invalid.
        TypeError: If forwarded options are unsupported.
        NotImplementedError: If renderer options are unsupported.

    Example:
        >>> chart = gsc.pl.rank_genes_groups_matrixplot(pbmc, n_genes=3, show=False)
    """
    return _ranked_expression(
        matrixplot,
        adata,
        groups,
        n_genes=n_genes,
        groupby=groupby,
        values_to_plot=values_to_plot,
        var_names=var_names,
        gene_symbols=gene_symbols,
        min_logfoldchange=min_logfoldchange,
        key=key,
        show=show,
        save=save,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        width=width,
        height=height,
        **kwds,
    )


def rank_genes_groups_heatmap(
    adata: AnnData,
    groups: str | Sequence[str] | None = None,
    *,
    n_genes: int | None = None,
    groupby: str | None = None,
    gene_symbols: str | None = None,
    var_names: Sequence[str] | Mapping[str, Sequence[str]] | None = None,
    min_logfoldchange: float | None = None,
    key: str | None = None,
    show: bool | None = None,
    save: bool | None = None,
    hover: bool = True,
    zoom: bool | Literal["xy"] = False,
    show_values: bool = False,
    group_gap: float = 0,
    width: float | None = None,
    height: float | None = None,
    **kwds: Any,
) -> TopLevelSpec | None:
    """Plot stored ranked genes through the existing individual-cell heatmap.

    Reuses ranked marker selection and all parent heatmap data and chart helpers.

    Args:
        adata: AnnData containing stored rankings and expression.
        groups: Rank lists to select; does not filter expression groups or cells.
        n_genes: Genes per list, default 10; negative selects the stored tail.
        groupby: Expression grouping key, default the ranking's groupby.
        gene_symbols: Variable annotation used for gene labels and lookup.
        var_names: Explicit markers instead of n_genes.
        min_logfoldchange: Strict lower stored log-fold-change threshold.
        key: Stored ranking key, default rank_genes_groups.
        show: Display once, return chart when False, or use Scanpy autoshow.
        save: None or False; use native chart.save for HTML/JSON.
        hover: Enable native cell tooltips.
        zoom: True navigates y only; "xy" navigates both axes.
        show_values: Show fitted plotted values when tiles have room.
        group_gap: Space between groups in CSS pixels; 0 keeps tiles contiguous.
        width: Parent heatmap width in logical pixels.
        height: Parent heatmap height in logical pixels.
        **kwds: Existing heatmap options; dendrogram defaults True.

    Returns:
        A native heatmap when show=False, otherwise None.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        ValueError: If stored rankings or gene-selection options are invalid.
        TypeError: If forwarded options are unsupported.
        NotImplementedError: If renderer options are unsupported.

    Example:
        >>> chart = gsc.pl.rank_genes_groups_heatmap(pbmc, n_genes=3, show=False)
    """
    return _ranked_expression(
        heatmap,
        adata,
        groups,
        n_genes=n_genes,
        groupby=groupby,
        values_to_plot=None,
        var_names=var_names,
        gene_symbols=gene_symbols,
        min_logfoldchange=min_logfoldchange,
        key=key,
        show=show,
        save=save,
        hover=hover,
        zoom=zoom,
        show_values=show_values,
        group_gap=group_gap,
        width=width,
        height=height,
        **kwds,
    )
