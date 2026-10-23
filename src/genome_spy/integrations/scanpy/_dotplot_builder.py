"""A mutable Scanpy-style builder backed by the shared native dotplot renderer."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, Self

from genome_spy.integrations.scanpy._grouped_builder import _GroupedPlot
from genome_spy.integrations.scanpy._guards import (
    _check_grid_zoom,
    _check_kwargs,
    _check_point_options,
    _require_scanpy,
)
from genome_spy.schemapi import Undefined, UndefinedType

if TYPE_CHECKING:
    from anndata import AnnData
    import pandas as pd

    from genome_spy import TopLevelSpec


class DotPlot(_GroupedPlot):
    """Build a grouped dotplot with Scanpy-style method chains.

    Read selected expression once at construction. Methods mutate this builder
    and return self; each to_chart call returns a detached native chart. Use that
    chart's composition, display and HTML/JSON saving APIs.

    Args:
        adata: AnnData containing expression and grouping annotations.
        var_names: Feature keys, repeated slots, or labeled feature groups.
        groupby: Observation key or categorical grouping keys.
        use_raw: Use raw when available; layer overrides the automatic choice.
        log: Apply log1p before calculating summaries.
        num_categories: Number of bins for numeric grouping annotations.
        categories_order: Complete order of grouping categories.
        title: Plot title.
        figsize: Native layout budget in inches at 100 logical pixels/inch.
        gene_symbols: Variable annotation column for symbol lookup.
        var_group_positions: Inclusive feature-slot bracket endpoints.
        var_group_labels: Bracket labels; mappings already supply these.
        var_group_rotation: Bracket label rotation in degrees.
        layer: Expression layer instead of the automatic raw/X source.
        expression_cutoff: Strict lower threshold for expressing cells.
        mean_only_expressed: Average only expressed values, with empty means zero.
        standard_scale: Scale means per variable or group, following Scanpy.
        dot_color_df: Authoritative labeled color values.
        dot_size_df: Authoritative labeled fractions between zero and one.
        vmin: Numeric lower color bound.
        vmax: Numeric upper color bound.
        vcenter: Reserved; nondefault values error.
        norm: Reserved; Matplotlib normalization objects error.
        hover: Show gene, group, displayed value and expressing percentage.
        zoom: True enables y navigation; "xy" also enables x navigation.
        highlight: Mark the hovered row and column with a native ruler.
        width: Plot-area width in logical pixels.
        height: Plot-area height in logical pixels.
        **kwds: Only cmap and scalar linewidth are supported.

    Returns:
        A mutable dotplot builder; construction does not display a chart.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If inputs or forwarded options have invalid types.
        ValueError: If groups, labels, fractions or dimensions are invalid.
        NotImplementedError: If a requested renderer option is unsupported.

    Example:
        >>> plot = gsc.pl.DotPlot(pbmc, markers, "louvain")
        >>> chart = plot.add_dendrogram().swap_axes().to_chart()
        >>> chart.save("markers.html", inline=True)
    """

    def __init__(
        self,
        adata: AnnData,
        var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
        groupby: str | Sequence[str],
        *,
        use_raw: bool | None = None,
        log: bool = False,
        num_categories: int = 7,
        categories_order: Sequence[str] | None = None,
        title: str | None = None,
        figsize: tuple[float, float] | None = None,
        gene_symbols: str | None = None,
        var_group_positions: Sequence[tuple[int, int]] | None = None,
        var_group_labels: Sequence[str] | None = None,
        var_group_rotation: float | None = None,
        layer: str | None = None,
        expression_cutoff: float = 0.0,
        mean_only_expressed: bool = False,
        standard_scale: Literal["var", "group"] | None = None,
        dot_color_df: pd.DataFrame | None = None,
        dot_size_df: pd.DataFrame | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        vcenter: float | None = None,
        norm: Any = None,
        hover: bool = True,
        zoom: bool | Literal["xy"] = False,
        highlight: bool = False,
        width: float | None = None,
        height: float | None = None,
        **kwds: Any,
    ) -> None:
        context = "gsc.pl.DotPlot"
        _check_kwargs(kwds, {"cmap", "linewidth"}, context=context)
        for name, value in {"vcenter": vcenter, "norm": norm}.items():
            if value is not None:
                raise NotImplementedError(f"{context}: {name} is not supported yet.")
        _check_point_options(
            context=context,
            width=width,
            height=height,
            frameon=None,
            log=log,
            mean_only_expressed=mean_only_expressed,
            hover=hover,
            highlight=highlight,
        )
        if standard_scale not in (None, "var", "group"):
            raise ValueError(
                f"{context}: standard_scale must be 'var', 'group', or None."
            )
        _check_grid_zoom(zoom, context=context)
        _require_scanpy(context)

        from genome_spy.integrations.scanpy._grouped_data import (
            dotplot_summaries,
            grouped_expression,
        )

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
        self._colors, self._fractions = dotplot_summaries(
            prepared.values,
            expression_cutoff=expression_cutoff,
            mean_only_expressed=mean_only_expressed,
            standard_scale=standard_scale,
            dot_color_df=dot_color_df,
            dot_size_df=dot_size_df,
        )
        super().__init__(
            adata,
            groupby,
            self._colors,
            prepared.feature_groups,
            prepared.counts,
            context=context,
        )
        self._standard_scale = standard_scale
        self._value_title = (
            "Color value" if dot_color_df is not None else "Mean expression"
        )
        if standard_scale is not None:
            self._value_title += " (scaled)"
        self._options: dict[str, Any] = {
            "title": title,
            "figsize": figsize,
            "rotation": var_group_rotation,
            "vmin": vmin,
            "vmax": vmax,
            "hover": hover,
            "zoom": zoom,
            "highlight": highlight,
            "width": width,
            "height": height,
            "cmap": kwds.get("cmap", "Reds"),
            "linewidth": kwds.get("linewidth", 0.2),
        }

    def style(
        self,
        *,
        cmap: Any = Undefined,
        color_on: Literal["dot", "square"] | UndefinedType = Undefined,
        dot_max: float | None | UndefinedType = Undefined,
        dot_min: float | None | UndefinedType = Undefined,
        smallest_dot: float | UndefinedType = Undefined,
        largest_dot: float | UndefinedType = Undefined,
        dot_edge_color: str | None | UndefinedType = Undefined,
        dot_edge_lw: float | None | UndefinedType = Undefined,
        size_exponent: float | UndefinedType = Undefined,
        grid: bool | UndefinedType = Undefined,
        x_padding: float | UndefinedType = Undefined,
        y_padding: float | UndefinedType = Undefined,
    ) -> Self:
        """Update only supplied styles; omitted settings retain their current values.

        Args:
            cmap: Native GenomeSpy color scheme; None selects viridis.
            color_on: Only dot coloring is currently supported.
            dot_max: Upper fraction limit; None restores the observed maximum.
            dot_min: Lower fraction limit; None restores zero.
            smallest_dot: Minimum dot area in points squared.
            largest_dot: Maximum dot area in points squared.
            dot_edge_color: Opaque CSS edge color; None removes the edge.
            dot_edge_lw: Edge width in points; None removes the edge.
            size_exponent: Positive exponent of the clipped expression fraction.
            grid: Show native grid lines at the dot centers.
            x_padding: Horizontal padding in slot units, at least 0.5.
            y_padding: Vertical padding in slot units, at least 0.5.

        Returns:
            This builder; scalar styles are validated by the shared renderer.

        Raises:
            NotImplementedError: If color_on requests square backgrounds.
            ValueError: If color_on is invalid.

        Example:
            >>> chart = plot.style(dot_edge_color="black", largest_dot=160).to_chart()
        """
        if color_on is not Undefined and color_on != "dot":
            if color_on == "square":
                raise NotImplementedError(
                    "gsc.pl.DotPlot: color_on='square' is not supported yet."
                )
            raise ValueError("gsc.pl.DotPlot: color_on must be 'dot' or 'square'.")
        self._options.update(
            {
                key: value
                for key, value in {
                    "cmap": cmap,
                    "dot_max": dot_max,
                    "dot_min": dot_min,
                    "smallest_dot": smallest_dot,
                    "largest_dot": largest_dot,
                    "edge_color": dot_edge_color,
                    "linewidth": dot_edge_lw,
                    "size_exponent": size_exponent,
                    "grid": grid,
                    "x_padding": x_padding,
                    "y_padding": y_padding,
                }.items()
                if value is not Undefined
            }
        )
        return self

    def legend(
        self,
        *,
        show: bool | None = True,
        show_size_legend: bool | None = True,
        show_colorbar: bool | None = True,
        size_title: str | None = "Fraction of cells\nin group (%)",
        colorbar_title: str | None = "Mean expression\nin group",
        width: float | None = 1.5,
    ) -> Self:
        """Configure native size/color guides without changing either data scale.

        Args:
            show: False or None hides both guides.
            show_size_legend: Show the percentage guide when show is True.
            show_colorbar: Show the color guide when show is True.
            size_title: Percentage guide title; None removes its title.
            colorbar_title: Color guide title; None removes its title.
            width: Native gradient width and figsize guide allowance in inches.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If visibility flags are not boolean or None.
            ValueError: If a visible guide's width is not positive and finite.

        Example:
            >>> chart = plot.legend(show_size_legend=False).to_chart()
        """
        for flag in (show, show_size_legend, show_colorbar):
            self._check_show(flag)
        if not show:
            self._options.update(
                show_size_legend=False, show_colorbar=False, legend_width=0
            )
        else:
            self._options.update(
                show_size_legend=bool(show_size_legend),
                show_colorbar=bool(show_colorbar),
                size_title=size_title,
                colorbar_title=colorbar_title,
                legend_width=self._track_size(width),
            )
        return self

    def to_chart(self) -> TopLevelSpec:
        """Render the current settings as a detached, composable native chart.

        Returns:
            A fresh GenomeSpy chart; later chains do not change this snapshot.

        Raises:
            ValueError: If the current style or layout options are invalid.
            NotImplementedError: If a style needs an unsupported renderer form.

        Example:
            >>> combined = plot.to_chart() | another_chart
        """
        from genome_spy.integrations.scanpy._dotplot_chart import build_dotplot
        from genome_spy.integrations.scanpy._grouped_data import scale_values

        colors, groups, slots = self._displayed()
        fractions = self._fractions.loc[self._order].iloc[:, slots]
        if self._swapped:
            colors, fractions = colors.T, fractions.T
        colors = scale_values(colors, self._standard_scale)
        return build_dotplot(
            colors,
            fractions,
            groups,
            swap_axes=self._swapped,
            value_title=self._value_title,
            tree=self._tree if self._extra == "dendrogram" else None,
            tree_size=self._extra_size,
            totals=self._totals(),
            **self._options,
        )

    def show(self, *, return_axes: bool | None = None) -> None:
        """Display one native chart using the notebook widget.

        Args:
            return_axes: Only None/False; use to_chart for a composable result.

        Returns:
            None, preventing a duplicate notebook output.

        Raises:
            TypeError: If return_axes requests Matplotlib axes.

        Example:
            >>> plot.style(cmap="viridis").show()
        """
        if return_axes is not None and return_axes is not False:
            raise TypeError(
                "gsc.pl.DotPlot: return_axes is omitted; use to_chart() for the native chart."
            )
        self.to_chart().display()
