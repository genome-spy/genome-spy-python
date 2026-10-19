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
    (metadata / "ranked.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
