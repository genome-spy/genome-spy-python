"""Export complete pinned Scanpy embedding references outside Git."""

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path


def main(output: Path | None = None) -> None:
    """Freeze labels, guides and ordered points; artist access stays in this generator."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import to_hex
    import scanpy as sc
    from tests.integrations.scanpy.embedding_fixture import (
        embedding_cases,
        make_embedding_adata,
    )
    from tests.integrations.scanpy.helpers import reference_paths

    assert version("scanpy") == "1.11.5"
    images, metadata = reference_paths("embedding", output)
    manifest = {
        "versions": {name: version(name) for name in ("scanpy", "numpy", "matplotlib")},
        "input_sha256": sha256(
            Path(__file__).with_name("embedding_fixture.py").read_bytes()
        ).hexdigest(),
        "display_dpi": 100,
        "export_dpi": 150,
        "cases": {},
    }
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
            artist = next(c for c in ax.collections if len(c.get_offsets()) == 8)
            manifest["cases"][name] = {
                "coordinates": np.asarray(artist.get_offsets()).tolist(),
                "sizes": artist.get_sizes().tolist(),
                "colors": [to_hex(c, keep_alpha=True) for c in artist.get_facecolors()],
                "color_domain": [artist.norm.vmin, artist.norm.vmax]
                if artist.get_array() is not None
                else None,
                "x_domain": list(ax.get_xlim()),
                "y_domain": list(ax.get_ylim()),
                "labels": [ax.get_xlabel(), ax.get_ylabel()],
                "title": ax.get_title(),
                "legend": [t.get_text() for t in ax.get_legend().texts]
                if ax.get_legend() is not None
                else None,
                "plot_size": [bbox.width, bbox.height],
                "full_sha256": sha256(full.read_bytes()).hexdigest(),
            }
            plt.close(fig)
    (metadata / "embedding.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    main()
