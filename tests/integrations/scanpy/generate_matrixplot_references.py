"""Explicit frozen Scanpy matrixplot values, complete figures and registered crops.

Run ``uv run --no-sync python -m tests.integrations.scanpy.generate_matrixplot_references``.
Artist inspection is confined to this generator, never runtime preparation.
"""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import warnings


def main(output: Path | None = None) -> None:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    import scanpy as sc

    from tests.integrations.scanpy.grouped_fixture import make_grouped_adata
    from tests.integrations.scanpy.matrixplot_fixture import matrixplot_cases

    if version("scanpy") != "1.11.5":
        raise RuntimeError("Matrixplot references require Scanpy 1.11.5.")
    from tests.integrations.scanpy.helpers import reference_paths

    output, metadata = reference_paths("matrixplot", output)
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
            for name in ("grouped_fixture.py", "matrixplot_fixture.py")
        },
        "cases": {},
    }
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
            figure.canvas.draw()
            main = plot.get_axes()["mainplot_ax"]
            collection = main.collections[0]
            bbox = main.get_window_extent()
            full = output / f"matrixplot-{name}.png"
            figure.savefig(full, dpi=150)
            image = Image.open(full)
            image.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(image.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(image.height - bbox.y0 * 1.5),
                )
            ).save(output / f"matrixplot-{name}-panel.png")
            values = plot.values_df
            if plot.categories_order is not None:
                values = values.loc[plot.categories_order]
            if plot.are_axes_swapped:
                values = values.T
            result["cases"][name] = {
                "plot_size": [bbox.width, bbox.height],
                "x_domain": list(main.get_xlim()),
                "y_domain": list(main.get_ylim()),
                "values": np.where(values.isna(), None, values).tolist(),
                "x_labels": [t.get_text() for t in main.get_xticklabels()],
                "y_labels": [t.get_text() for t in main.get_yticklabels()],
                "tile_bounds": [
                    [*path.vertices.min(axis=0), *path.vertices.max(axis=0)]
                    for path in collection.get_paths()
                ],
                "colors": collection.get_facecolors().tolist(),
                "color_domain": [collection.norm.vmin, collection.norm.vmax],
                "edge_colors": collection.get_edgecolors().tolist(),
                "linewidths": collection.get_linewidths().tolist(),
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(figure)
    (metadata / "matrixplot.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
