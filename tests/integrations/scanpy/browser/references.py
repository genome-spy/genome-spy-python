"""Temporary Scanpy images for complete-chart comparisons, using the pinned stack.

Display at 100 DPI and export at 150 DPI. Crops never fit or rescale the marks.
Numeric expectations stay in small deliberate fixtures; no image/report is tracked.
"""

import warnings
from pathlib import Path


def _save_panel(axis, path, *, crop=True):
    """Export a registered plot area, preserving the original pixel-rounding rules."""
    from io import BytesIO

    from PIL import Image

    figure = axis.figure
    figure.canvas.draw()
    box = axis.get_window_extent()
    if not crop:
        figure.savefig(
            path,
            dpi=150,
            bbox_inches=box.transformed(figure.dpi_scale_trans.inverted()),
            pad_inches=0,
        )
        return
    output = BytesIO()
    figure.savefig(output, dpi=150)
    image = Image.open(output)
    image.crop(
        (
            round(box.x0 * 1.5),
            round(image.height - box.y1 * 1.5),
            round(box.x1 * 1.5),
            round(image.height - box.y0 * 1.5),
        )
    ).save(path)


def _clustermap(output: Path) -> None:
    """Render clustermap comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import (
        clustermap_cases,
        make_cluster_adata,
    )

    with mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}):
        for case, options in clustermap_cases().items():
            grid = sc.pl.clustermap(
                make_cluster_adata(), show=False, cmap="viridis", **options
            )
            _save_panel(grid.ax_heatmap, output / f"clustermap-{case}-panel.png")
            plt.close(grid.fig)


def _dendrogram(output: Path) -> None:
    """Render dendrogram comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import (
        make_tree_adata,
        tree_plot_cases,
    )

    with mpl.rc_context(
        {
            "font.size": 10,
            "figure.dpi": 100,
            "savefig.dpi": 150,
            "figure.figsize": (6, 4),
        }
    ):
        for name, (family, options) in tree_plot_cases().items():
            a = make_tree_adata()
            sc.tl.dendrogram(a, "group")
            if family in ("dotplot", "matrixplot"):
                plot = getattr(sc.pl, family)(
                    a,
                    groupby="group",
                    figsize=(7, 4),
                    title="Grouped markers",
                    return_fig=True,
                    **options,
                )
                plot.make_figure()
                axes = plot.get_axes()
                main = axes["mainplot_ax"]
            elif family == "dendrogram":
                main = sc.pl.dendrogram(a, "group", show=False, **options)
            else:
                axes = sc.pl.correlation_matrix(
                    a, "group", figsize=(7, 4), show=False, **options
                )
                main = axes[-2]
            figure = main.figure
            _save_panel(main, output / f"dendrogram-{name}-panel.png")
            plt.close(figure)


def _dotplot(output: Path) -> None:
    """Render dotplot comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import (
        dotplot_cases,
        make_grouped_adata,
    )

    with (
        mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}),
        warnings.catch_warnings(),
    ):
        warnings.filterwarnings("ignore", message="Observation names are not unique")
        for name, options in dotplot_cases().items():
            options = options.copy()
            var_names = options.pop("var_names", ["g1", "g2", "g3"])
            plot = sc.pl.dotplot(
                make_grouped_adata(),
                var_names,
                "group",
                use_raw=False,
                figsize=(7, 4),
                title="Grouped markers",
                return_fig=True,
                **options,
            )
            plot.make_figure()
            figure = plot.fig
            axes = plot.get_axes()
            main = axes["mainplot_ax"]
            _save_panel(main, output / f"dotplot-{name}-panel.png")
            plt.close(figure)


def _embedding(output: Path) -> None:
    """Render embedding comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import scanpy as sc

    from tests.integrations.scanpy.embedding_fixtures import (
        embedding_cases,
        make_embedding_adata,
    )

    with mpl.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, (family, options) in embedding_cases().items():
            ax = getattr(sc.pl, family)(
                make_embedding_adata(),
                size=np.arange(8) * 7 + 25,
                frameon=True,
                show=False,
                **options,
            )
            fig = ax.figure
            _save_panel(ax, output / f"{name}-panel.png", crop=False)
            plt.close(fig)


def _heatmap(output: Path) -> None:
    """Render heatmap comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import (
        heatmap_cases,
        make_heatmap_adata,
    )

    with (
        mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}),
        warnings.catch_warnings(),
    ):
        warnings.filterwarnings("ignore", message="Observation names are not unique")
        for name, options in heatmap_cases().items():
            options = options.copy()
            names = options.pop("var_names", ["g1", "g2", "g3"])
            groupby = options.pop("groupby", "group")
            adata = make_heatmap_adata(name)
            if options.get("dendrogram"):
                sc.tl.dendrogram(adata, groupby)
            axes = sc.pl.heatmap(
                adata,
                names,
                groupby,
                show=False,
                figsize=(7, 4),
                cmap="viridis",
                **options,
            )
            main = axes["heatmap_ax"]
            figure = main.figure
            _save_panel(main, output / f"heatmap-{name}-panel.png")
            plt.close(figure)


def _matrix(output: Path) -> None:
    """Render matrix comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import matrix_cases

    with mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}):
        for case, (values, options) in matrix_cases().items():
            fig, ax = plt.subplots(figsize=(6, 4))
            sc.pl.matrix(values, show=False, **options)
            _save_panel(ax, output / f"matrix-{case}-panel.png")
            plt.close(fig)


def _matrixplot(output: Path) -> None:
    """Render matrixplot comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.expression_fixtures import (
        make_grouped_adata,
        matrixplot_cases,
    )

    with (
        mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}),
        warnings.catch_warnings(),
    ):
        warnings.filterwarnings("ignore", message="Observation names are not unique")
        for name, options in matrixplot_cases().items():
            options = options.copy()
            names = options.pop("var_names", ["g1", "g2", "g3"])
            plot = sc.pl.matrixplot(
                make_grouped_adata(),
                names,
                "group",
                use_raw=False,
                figsize=(7, 4),
                title="Grouped markers",
                return_fig=True,
                **options,
            )
            plot.make_figure()
            figure = plot.fig
            main = plot.get_axes()["mainplot_ax"]
            _save_panel(main, output / f"matrixplot-{name}-panel.png")
            plt.close(figure)


def _ranked(output: Path) -> None:
    """Render ranked comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases

    with mpl.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, (family, args, options) in ranked_cases().items():
            getattr(sc.pl, family)(make_ranked_adata(), *args, show=False, **options)
            figure = plt.gcf()
            for i, ax in enumerate(figure.axes):
                _save_panel(ax, output / f"ranked-{name}-panel-{i}.png")
            plt.close(figure)
        for family, metric in [
            ("dotplot", "scores"),
            ("matrixplot", "log10_pvals_adj"),
        ]:
            plot = getattr(sc.pl, f"rank_genes_groups_{family}")(
                make_ranked_adata(),
                groups=["A", "C"],
                n_genes=2,
                values_to_plot=metric,
                dendrogram=False,
                return_fig=True,
                figsize=(7, 4),
                cmap="viridis",
            )
            plot.make_figure()
            figure = plot.fig
            axes = plot.get_axes()
            main = axes["mainplot_ax"]
            _save_panel(main, output / f"ranked-statistic-{family}-panel.png")
            plt.close(figure)


def _umap(output: Path) -> None:
    """Render umap comparison images in the temporary reference directory."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import scanpy as sc

    from tests.integrations.scanpy.embedding_fixtures import make_adata, reference_cases

    sizes = np.arange(8, dtype=float) * 7 + 25
    with plt.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, options in reference_cases().items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                adata = make_adata()
                axes = sc.pl.umap(adata, **options, size=sizes, show=False)
            axes = axes if isinstance(axes, list) else [axes]
            fig = axes[0].figure
            fig.canvas.draw()
            fig.savefig(output / f"{name}.png", dpi=150, bbox_inches="tight")
            for i, ax in enumerate(axes):
                _save_panel(ax, output / f"{name}-panel-{i}.png", crop=False)
            plt.close(fig)
        for marker, token, linewidth in [
            (".", "dot", 0),
            ("o", "circle", 0),
            (".", "dot-stroke", 2),
            ("s", "square", 0),
            ("s", "square-stroke", 2),
            ("D", "diamond", 0),
            ("D", "diamond-stroke", 2),
        ]:
            a = make_adata()[:1].copy()
            a.obsm["X_umap"] = np.array([[0.0, 0.0]])
            ax = sc.pl.umap(
                a,
                size=144,
                marker=marker,
                frameon=False,
                na_color="black",
                show=False,
                edgecolor="black" if linewidth else "none",
                linewidths=linewidth,
            )
            fig = ax.figure
            _save_panel(ax, output / f"footprint-{token}.png", crop=False)
            plt.close(fig)


def _scatter(output: Path) -> None:
    """Render scatter comparison images in the temporary reference directory."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    from tests.integrations.scanpy.embedding_fixtures import (
        make_scatter_adata,
        scatter_cases,
    )

    with mpl.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, options in scatter_cases().items():
            ax = sc.pl.scatter(
                make_scatter_adata(), **options, size=80, frameon=True, show=False
            )
            fig = ax.figure
            _save_panel(ax, output / f"{name}-panel.png", crop=False)
            plt.close(fig)


def render_images(family, output):
    """Render the requested family's reference images without updating test fixtures."""
    renderers = {
        "clustermap": _clustermap,
        "dendrogram": _dendrogram,
        "dotplot": _dotplot,
        "embedding": _embedding,
        "heatmap": _heatmap,
        "matrix": _matrix,
        "matrixplot": _matrixplot,
        "ranked": _ranked,
        "umap": _umap,
        "scatter": _scatter,
    }
    output.mkdir(parents=True, exist_ok=True)
    renderers[family](output)
