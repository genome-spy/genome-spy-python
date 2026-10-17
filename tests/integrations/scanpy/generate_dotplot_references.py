"""Explicit Scanpy dotplot exports; ordinary tests read the frozen evidence.

Run ``uv run --no-sync python -m tests.integrations.scanpy.generate_dotplot_references``.
Artist inspection is restricted to this generator, never production preparation.
"""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import warnings


def main() -> None:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    import scanpy as sc

    from tests.integrations.scanpy.dotplot_fixture import dotplot_cases
    from tests.integrations.scanpy.grouped_fixture import make_grouped_adata

    if version("scanpy") != "1.11.5":
        raise RuntimeError("Dotplot references require Scanpy 1.11.5.")
    output = Path(__file__).with_name("fixtures")
    result = {
        "versions": {
            name: version(name) for name in ("scanpy", "numpy", "pandas", "matplotlib")
        },
        "display_dpi": 100,
        "export_dpi": 150,
        "font": "DejaVu Sans",
        "native_font": "Lato Regular",
        "input_sha256": {
            name: sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ("grouped_fixture.py", "dotplot_fixture.py")
        },
        "cases": {},
    }
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
            figure.canvas.draw()
            axes = plot.get_axes()
            main = axes["mainplot_ax"]
            collection = main.collections[0]
            bbox = main.get_window_extent()
            full = output / f"dotplot-{name}.png"
            figure.savefig(full, dpi=150)
            image = Image.open(full)
            image.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(image.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(image.height - bbox.y0 * 1.5),
                )
            ).save(output / f"dotplot-{name}-panel.png")
            result["cases"][name] = {
                "plot_size": [bbox.width, bbox.height],
                "x_domain": list(main.get_xlim()),
                "y_domain": list(main.get_ylim()),
                "positions": collection.get_offsets().tolist(),
                "sizes": collection.get_sizes().tolist(),
                "colors": collection.get_facecolors().tolist(),
                "x_labels": [t.get_text() for t in main.get_xticklabels()],
                "y_labels": [t.get_text() for t in main.get_yticklabels()],
                "size_labels": [
                    t.get_text() for t in axes["size_legend_ax"].get_xticklabels()
                ],
                "dot_min": plot.dot_min,
                "dot_max": plot.dot_max,
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(figure)
    (output / "dotplot.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
