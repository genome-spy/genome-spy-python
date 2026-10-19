"""Export pinned complete scatter references; generated media stays outside Git."""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path


def main(output: Path | None = None) -> None:
    """Record upstream points and guides for independent native chart comparisons."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_hex
    import numpy as np
    import scanpy as sc
    from tests.integrations.scanpy.helpers import reference_paths
    from tests.integrations.scanpy.scatter_fixture import (
        make_scatter_adata,
        scatter_cases,
    )

    assert version("scanpy") == "1.11.5"
    images, metadata = reference_paths("scatter", output)
    manifest = {
        "versions": {name: version(name) for name in ("scanpy", "numpy", "matplotlib")},
        "input_sha256": sha256(
            Path(__file__).with_name("scatter_fixture.py").read_bytes()
        ).hexdigest(),
        "display_dpi": 100,
        "export_dpi": 150,
        "cases": {},
    }
    with mpl.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, options in scatter_cases().items():
            ax = sc.pl.scatter(
                make_scatter_adata(), **options, size=80, frameon=True, show=False
            )
            fig = ax.figure
            fig.canvas.draw()
            full = images / f"{name}.png"
            fig.savefig(full, dpi=150, bbox_inches="tight")
            bbox = ax.get_window_extent()
            fig.savefig(
                images / f"{name}-panel.png",
                dpi=150,
                bbox_inches=bbox.transformed(fig.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            coordinates, paints = [], []
            artists = sorted(ax.collections, key=lambda c: c.get_zorder())
            for artist in artists:
                offsets = artist.get_offsets()
                valid = ~np.ma.getmaskarray(offsets).any(axis=1)
                coordinates.extend(np.asarray(offsets)[valid].tolist())
                colors = artist.get_facecolors()
                if len(colors) == 1:
                    colors = np.repeat(colors, len(offsets), axis=0)
                paints.extend(to_hex(c, keep_alpha=True) for c in colors[valid])
            artist = artists[-1]
            manifest["cases"][name] = {
                "coordinates": coordinates,
                "colors": paints,
                "categorical": artist.get_array() is None,
                "color_domain": [artist.norm.vmin, artist.norm.vmax]
                if artist.get_array() is not None
                else None,
                "x_domain": list(ax.get_xlim()),
                "y_domain": list(ax.get_ylim()),
                "labels": [ax.get_xlabel(), ax.get_ylabel()],
                "title": ax.get_title(),
                "legend": [text.get_text() for text in ax.get_legend().texts]
                if ax.get_legend() is not None
                else None,
                "plot_size": [bbox.width, bbox.height],
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(fig)
    (metadata / "scatter.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    main()
