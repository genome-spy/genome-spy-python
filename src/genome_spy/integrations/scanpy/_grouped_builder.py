"""Group ordering and decoration state shared by DotPlot and MatrixPlot."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal, Self

if TYPE_CHECKING:
    from anndata import AnnData
    import pandas as pd

    from genome_spy.integrations.scanpy._dendrogram_data import DendrogramData
    from genome_spy.integrations.scanpy._grouped_data import FeatureGroup


class _GroupedPlot:
    """Keep the shared group layout over detached expression summaries."""

    def __init__(
        self,
        adata: AnnData,
        groupby: str | Sequence[str],
        colors: pd.DataFrame,
        feature_groups: tuple[FeatureGroup, ...],
        counts: pd.Series,
        *,
        context: str,
    ) -> None:
        self._context = context
        self._adata = adata
        self._groupby = [groupby] if isinstance(groupby, str) else list(groupby)
        self._colors = colors
        self._feature_groups = feature_groups
        self._counts = counts
        self._order = list(colors.index)
        self._tree: DendrogramData | None = None
        self._extra: Literal["dendrogram", "totals"] | None = None
        self._extra_size = 80.0
        self._total_colors: list[str] = []
        self._swapped = False

    def swap_axes(self, *, swap_axes: bool | None = True) -> Self:
        """Place groups on x and features on y, or restore the original orientation.

        Args:
            swap_axes: True transposes the plot; False or None restores it.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If swap_axes is not boolean or None.

        Example:
            >>> chart = plot.swap_axes().to_chart()
        """
        if swap_axes is not None and not isinstance(swap_axes, bool):
            raise TypeError(f"{self._context}: swap_axes must be boolean or None.")
        self._swapped = bool(swap_axes)
        return self

    def add_dendrogram(
        self,
        *,
        show: bool | None = True,
        dendrogram_key: str | None = None,
        size: float | None = 0.8,
    ) -> Self:
        """Attach the shared group tree, replacing totals while retaining its order.

        Args:
            show: False or None hides the group decoration, preserving ordering.
            dendrogram_key: Stored Scanpy tree key, or the default grouping key.
            size: Tree track size in inches at 100 logical pixels/inch.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If flags or the tree key have invalid types.
            ValueError: If the tree or size is invalid.

        Example:
            >>> chart = plot.add_dendrogram().swap_axes().to_chart()
        """
        from genome_spy.integrations.scanpy._dendrogram_data import attached_dendrogram

        self._check_show(show)
        if not show:
            self._extra = None
            return self
        size_pixels = self._track_size(size)
        if dendrogram_key is not None and (
            not isinstance(dendrogram_key, str) or not dendrogram_key
        ):
            raise TypeError(
                f"{self._context}: dendrogram_key must be a nonempty string or None."
            )
        tree = attached_dendrogram(
            self._adata, self._groupby, dendrogram_key or True, len(self._colors)
        )
        if tree is not None:
            self._tree = tree
            self._order = list(tree.order)
            self._extra = "dendrogram"
            self._extra_size = size_pixels
        return self

    def add_totals(
        self,
        *,
        show: bool | None = True,
        sort: Literal["ascending", "descending"] | None = None,
        size: float | None = 0.8,
        color: str | Sequence[str] | None = None,
    ) -> Self:
        """Show group counts with native bars, replacing the dendrogram track.

        Args:
            show: False or None hides the decoration while preserving ordering.
            sort: Sort groups by cell count, or retain their current order.
            size: Track size in inches at 100 logical pixels/inch.
            color: One CSS color or one per displayed group; default salmon.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If show or color has an invalid type.
            ValueError: If sort, size or the number of colors is invalid.
            NotImplementedError: If colors are not opaque CSS colors.

        Example:
            >>> chart = plot.add_totals(sort="descending", color="salmon").to_chart()
        """
        from genome_spy.integrations.scanpy._style import native_color

        self._check_show(show)
        if not show:
            self._extra = None
            return self
        size_pixels = self._track_size(size)
        if sort not in (None, "ascending", "descending"):
            raise ValueError(
                f"{self._context}: sort must be 'ascending', 'descending', or None."
            )
        color = "salmon" if color is None else color
        if isinstance(color, str):
            colors = [color] * len(self._counts)
        elif isinstance(color, Sequence):
            colors = list(color)
        else:
            raise TypeError(f"{self._context}: color requires a CSS color or sequence.")
        if len(colors) != len(self._counts):
            raise ValueError(f"{self._context}: totals need one color per group.")
        colors = [native_color(c, "color", context=self._context) for c in colors]
        if sort is not None:
            self._order = list(
                self._counts.sort_values(ascending=sort == "ascending").index
            )
        self._total_colors = colors
        self._extra = "totals"
        self._extra_size = size_pixels
        return self

    def _displayed(self) -> tuple[pd.DataFrame, tuple[FeatureGroup, ...], list[int]]:
        from genome_spy.integrations.scanpy._dendrogram_data import reorder_grouped

        colors, groups = self._colors, self._feature_groups
        slots = list(range(colors.shape[1]))
        if self._tree is not None:
            colors, groups, slots = reorder_grouped(
                self._tree, colors, groups, swapped=False
            )
        return colors.loc[self._order], groups, slots

    def _totals(self) -> pd.DataFrame | None:
        import pandas as pd

        if self._extra != "totals":
            return None
        return pd.DataFrame(
            {"count": self._counts.loc[self._order], "color": self._total_colors}
        )

    def _check_show(self, show: bool | None) -> None:
        if show is not None and not isinstance(show, bool):
            raise TypeError(f"{self._context}: show flags must be boolean or None.")

    def _track_size(self, size: float | None) -> float:
        from genome_spy.integrations.scanpy._data import number

        value = number(size, "size/width", context=self._context)
        if value == 0:
            raise ValueError(
                f"{self._context}: size/width must be positive; use show=False to hide it."
            )
        return value * 100
