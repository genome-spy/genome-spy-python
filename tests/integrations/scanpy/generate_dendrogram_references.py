"""Explicit pinned Scanpy tree computations and complete native-chart oracles.

Run ``uv run --no-sync python -m tests.integrations.scanpy.generate_dendrogram_references``.
Upstream plotting and artist inspection occur only in this reference generator.
"""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path


def main() -> None:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    import scanpy as sc
    from tests.integrations.scanpy.dendrogram_fixture import (
        make_tree_adata,
        tree_cases,
        tree_plot_cases,
    )

    if version("scanpy") != "1.11.5":
        raise RuntimeError("Dendrogram references require Scanpy 1.11.5.")
    output = Path(__file__).with_name("fixtures")

    def serial(value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, dict):
            return {key: serial(item) for key, item in value.items()}
        return value

    result = {
        "versions": {
            p: version(p) for p in ("scanpy", "scipy", "pandas", "numpy", "matplotlib")
        },
        "display_dpi": 100,
        "export_dpi": 150,
        "font": "DejaVu Sans",
        "native_font": "Lato Regular",
        "fixture_sha256": sha256(
            Path(__file__).with_name("dendrogram_fixture.py").read_bytes()
        ).hexdigest(),
        "computations": {},
        "charts": {},
    }
    for name, options in tree_cases().items():
        options = options.copy()
        groupby = options.pop("groupby", "group")
        data = sc.tl.dendrogram(
            make_tree_adata(name), groupby, inplace=False, **options
        )
        result["computations"][name] = serial(data)
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
                main, tree = axes["mainplot_ax"], axes["group_extra_ax"]
            elif family == "dendrogram":
                main = sc.pl.dendrogram(a, "group", show=False, **options)
                tree = main
            else:
                axes = sc.pl.correlation_matrix(
                    a, "group", figsize=(7, 4), show=False, **options
                )
                main = axes[-2]
                tree = axes[0] if options.get("dendrogram") is not False else None
            figure = main.figure
            figure.canvas.draw()
            full = output / f"dendrogram-{name}.png"
            figure.savefig(full, dpi=150)
            bbox = main.get_window_extent()
            image = Image.open(full)
            image.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(image.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(image.height - bbox.y0 * 1.5),
                )
            ).save(output / f"dendrogram-{name}-panel.png")
            result["charts"][name] = {
                "family": family,
                "plot_size": [bbox.width, bbox.height],
                "x_domain": list(main.get_xlim()),
                "y_domain": list(main.get_ylim()),
                "x_labels": [t.get_text() for t in main.get_xticklabels()],
                "y_labels": [t.get_text() for t in main.get_yticklabels()],
                "tree_paths": [line.get_xydata().tolist() for line in tree.lines]
                if tree is not None
                else [],
                "tree_x_domain": list(tree.get_xlim()) if tree is not None else None,
                "tree_y_domain": list(tree.get_ylim()) if tree is not None else None,
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            if family in ("matrixplot", "correlation_matrix"):
                result["charts"][name]["values"] = (
                    main.collections[0].get_array().tolist()
                )
            plt.close(figure)
    (output / "dendrogram.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
