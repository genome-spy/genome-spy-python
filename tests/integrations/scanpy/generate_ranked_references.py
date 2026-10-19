"""Freeze upstream ranking panels; rendered artist inspection stays in this tool."""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path


def main(output: Path | None = None) -> None:
    """Write reference images outside Git and deliberate numeric/guide metadata."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc
    from PIL import Image
    from tests.integrations.scanpy.helpers import reference_paths
    from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases

    assert version("scanpy") == "1.11.5"
    images, metadata = reference_paths("ranked", output)
    manifest = {
        "versions": {name: version(name) for name in ("scanpy", "numpy", "matplotlib")},
        "display_dpi": 100,
        "export_dpi": 150,
        "input_sha256": sha256(
            Path(__file__).with_name("ranked_fixture.py").read_bytes()
        ).hexdigest(),
        "cases": {},
        "statistics": {},
    }
    with mpl.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, (family, args, options) in ranked_cases().items():
            getattr(sc.pl, family)(make_ranked_adata(), *args, show=False, **options)
            figure = plt.gcf()
            figure.canvas.draw()
            full = images / f"ranked-{name}.png"
            figure.savefig(full, dpi=150)
            image = Image.open(full)
            panels = []
            for i, ax in enumerate(figure.axes):
                bbox = ax.get_window_extent()
                image.crop(
                    (
                        round(bbox.x0 * 1.5),
                        round(image.height - bbox.y1 * 1.5),
                        round(bbox.x1 * 1.5),
                        round(image.height - bbox.y0 * 1.5),
                    )
                ).save(images / f"ranked-{name}-panel-{i}.png")
                panels.append(
                    {
                        "labels": [
                            {
                                "text": text.get_text(),
                                "position": list(map(float, text.get_position())),
                                "fontsize": text.get_fontsize(),
                                "rotation": text.get_rotation(),
                            }
                            for text in ax.texts
                        ],
                        "x_domain": list(ax.get_xlim()),
                        "y_domain": list(ax.get_ylim()),
                        "plot_size": [bbox.width, bbox.height],
                        "xlabel": ax.get_xlabel(),
                        "ylabel": ax.get_ylabel(),
                        "title": ax.get_title(),
                    }
                )
            manifest["cases"][name] = {
                "panels": panels,
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(figure)
        # Reference the complete ranked wrappers, including their native metric titles.
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
            figure.canvas.draw()
            axes = plot.get_axes()
            main = axes["mainplot_ax"]
            bbox = main.get_window_extent()
            full = images / f"ranked-statistic-{family}.png"
            figure.savefig(full, dpi=150)
            image = Image.open(full)
            image.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(image.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(image.height - bbox.y0 * 1.5),
                )
            ).save(images / f"ranked-statistic-{family}-panel.png")
            colorbar = axes["color_legend_ax"].collections[-1]
            manifest["statistics"][family] = {
                "metric": metric,
                "plot_size": [bbox.width, bbox.height],
                "x_domain": list(main.get_xlim()),
                "y_domain": list(main.get_ylim()),
                "x_labels": [t.get_text() for t in main.get_xticklabels()],
                "y_labels": [t.get_text() for t in main.get_yticklabels()],
                "color_domain": [colorbar.norm.vmin, colorbar.norm.vmax],
                "legend_title": plot.color_legend_title,
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(figure)
    (metadata / "ranked.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
