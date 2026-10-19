"""Freeze Scanpy's supplied matrices; Matplotlib is used only in this test tool."""

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
    from tests.integrations.scanpy.matrix_fixture import matrix_cases

    assert version("scanpy") == "1.11.5"
    from tests.integrations.scanpy.helpers import reference_paths

    output, metadata = reference_paths("matrix", output)
    manifest = {
        "versions": {name: version(name) for name in ("scanpy", "numpy", "matplotlib")},
        "display_dpi": 100,
        "export_dpi": 150,
        "input_sha256": sha256(
            Path(__file__).with_name("matrix_fixture.py").read_bytes()
        ).hexdigest(),
        "cases": {},
    }
    with mpl.rc_context({"font.size": 10, "figure.dpi": 100, "savefig.dpi": 150}):
        for case, (values, options) in matrix_cases().items():
            fig, ax = plt.subplots(figsize=(6, 4))
            sc.pl.matrix(values, show=False, **options)
            fig.canvas.draw()
            image = ax.images[0]
            bbox = ax.get_window_extent()
            full = output / f"matrix-{case}.png"
            fig.savefig(full, dpi=150)
            picture = Image.open(full)
            picture.crop(
                (
                    round(bbox.x0 * 1.5),
                    round(picture.height - bbox.y1 * 1.5),
                    round(bbox.x1 * 1.5),
                    round(picture.height - bbox.y0 * 1.5),
                )
            ).save(output / f"matrix-{case}-panel.png")
            array = image.get_array()
            manifest["cases"][case] = {
                "values": np.where(
                    np.ma.getmaskarray(array), None, array.data
                ).tolist(),
                "color_domain": [image.norm.vmin, image.norm.vmax],
                "plot_size": [bbox.width, bbox.height],
                "xlabel": ax.get_xlabel(),
                "ylabel": ax.get_ylabel(),
                "title": ax.get_title(),
                "x_labels": [t.get_text() for t in ax.get_xticklabels()],
                "y_labels": [t.get_text() for t in ax.get_yticklabels()],
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(fig)
    (metadata / "matrix.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
