"""Export pinned Scanpy clustermaps; figures and PNGs stay outside Git."""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path


def main(output: Path | None = None) -> None:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    import scanpy as sc

    from tests.integrations.scanpy.clustermap_fixture import (
        make_cluster_adata,
        clustermap_cases,
    )
    from tests.integrations.scanpy.helpers import reference_paths

    assert version("scanpy") == "1.11.5"
    output, metadata = reference_paths("clustermap", output)
    manifest = {
        "versions": {
            name: version(name)
            for name in ("scanpy", "seaborn", "numpy", "scipy", "matplotlib")
        },
        "display_dpi": 100,
        "export_dpi": 150,
        "input_sha256": sha256(
            Path(__file__).with_name("clustermap_fixture.py").read_bytes()
        ).hexdigest(),
        "cases": {},
    }
    with mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}):
        for case, options in clustermap_cases().items():
            grid = sc.pl.clustermap(
                make_cluster_adata(), show=False, cmap="viridis", **options
            )
            grid.fig.canvas.draw()
            bbox = grid.ax_heatmap.get_window_extent()
            full = output / f"clustermap-{case}.png"
            grid.fig.savefig(full, dpi=150)
            picture = Image.open(full)
            picture.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(picture.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(picture.height - bbox.y0 * 1.5),
                )
            ).save(output / f"clustermap-{case}-panel.png")
            trees = {}
            for axis in ("row", "col"):
                tree = getattr(grid, "dendrogram_" + axis)
                trees[axis + "_order"] = (
                    tree.reordered_ind
                    if tree
                    else list(range(grid.data2d.shape[0 if axis == "row" else 1]))
                )
                trees[axis + "_tree"] = (
                    {key: tree.dendrogram[key] for key in ("icoord", "dcoord")}
                    if tree
                    else None
                )
            manifest["cases"][case] = {
                **trees,
                "values": grid.data2d.to_numpy().tolist(),
                "mask": np.ma.getmaskarray(grid.ax_heatmap.collections[0].get_array())
                .reshape(grid.data2d.shape)
                .tolist(),
                "plot_size": [bbox.width, bbox.height],
                "color_domain": [
                    grid.ax_heatmap.collections[0].norm.vmin,
                    grid.ax_heatmap.collections[0].norm.vmax,
                ],
                "x_labels": [
                    tick.get_text() for tick in grid.ax_heatmap.get_xticklabels()
                ],
                "y_labels": [
                    tick.get_text() for tick in grid.ax_heatmap.get_yticklabels()
                ],
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(grid.fig)
    (metadata / "clustermap.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
