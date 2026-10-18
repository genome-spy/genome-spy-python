"""Freeze pinned Scanpy heatmaps; artist inspection stays in this explicit tool."""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import warnings


def main() -> None:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    import scanpy as sc

    from tests.integrations.scanpy.heatmap_fixture import (
        make_heatmap_adata,
        heatmap_cases,
    )

    assert version("scanpy") == "1.11.5"
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
            for name in ("heatmap_fixture.py", "dendrogram_fixture.py")
        },
        "cases": {},
    }
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
            figure.canvas.draw()
            image = main.images[0]
            bbox = main.get_window_extent()
            full = output / f"heatmap-{name}.png"
            figure.savefig(full, dpi=150)
            picture = Image.open(full)
            picture.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(picture.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(picture.height - bbox.y0 * 1.5),
                )
            ).save(output / f"heatmap-{name}-panel.png")
            groups = axes.get("groupby_ax")
            result["cases"][name] = {
                "plot_size": [bbox.width, bbox.height],
                "values": np.where(
                    np.ma.getmaskarray(image.get_array()), None, image.get_array().data
                ).tolist(),
                "color_domain": [image.norm.vmin, image.norm.vmax],
                "x_labels": [text.get_text() for text in main.get_xticklabels()],
                "y_labels": [text.get_text() for text in main.get_yticklabels()],
                "group_ticks": list(
                    groups.get_xticks()
                    if options.get("swap_axes")
                    else groups.get_yticks()
                )
                if groups
                else [],
                "group_labels": [
                    t.get_text()
                    for t in (
                        groups.get_xticklabels()
                        if options.get("swap_axes")
                        else groups.get_yticklabels()
                    )
                ]
                if groups
                else [],
                "tree_paths": [
                    np.column_stack([line.get_xdata(), line.get_ydata()]).tolist()
                    for line in axes["dendrogram_ax"].lines
                ]
                if "dendrogram_ax" in axes
                else [],
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(figure)
    (output / "heatmap.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
