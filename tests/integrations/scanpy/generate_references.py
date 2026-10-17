"""Generate the explicit Scanpy 1.11.5 API and synthetic rendering oracles.

Run ``uv run --group scanpy-test python -m tests.integrations.scanpy.generate_references``.
No datasets are downloaded and no analysis is run. Artists are inspected only
here, never by the production adapter. The synthetic fixture is original project
test data, covered by the project's MIT license. API metadata describes the
public Scanpy contract; no upstream implementation is vendored.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import version
import inspect
import json
from pathlib import Path
import re
from typing import Any
import warnings


def api_contract(sc: Any) -> dict[str, Any]:
    """Record public callable identities, parameters, kinds, and defaults."""
    entries = {}
    for name, obj in sorted(vars(sc.pl).items()):
        if (
            name.startswith("_")
            or not callable(obj)
            or not getattr(obj, "__module__", "").startswith("scanpy")
        ):
            continue
        signature = inspect.signature(obj)
        entries[name] = {
            "kind": "class" if inspect.isclass(obj) else "function",
            "target": f"{obj.__module__}.{obj.__qualname__}",
            "parameters": [
                {
                    "name": p.name,
                    "kind": p.kind.name,
                    "default": None
                    if p.default is inspect.Parameter.empty
                    else re.sub(r"0x[0-9a-f]+", "<address>", repr(p.default)),
                }
                for p in signature.parameters.values()
            ],
        }
    return {"scanpy": version("scanpy"), "namespace": "scanpy.pl", "entries": entries}


def main() -> None:
    """Freeze independent reference observations and complete figures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).with_name("fixtures")
    )
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import scanpy as sc
    from matplotlib.colors import to_hex
    from matplotlib.markers import MarkerStyle

    from tests.integrations.scanpy.fixture_data import make_adata, reference_cases

    if version("scanpy") != "1.11.5":
        raise RuntimeError("Reference generation requires Scanpy 1.11.5.")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "api.json").write_text(json.dumps(api_contract(sc), indent=2) + "\n")
    sizes = np.arange(8, dtype=float) * 7 + 25
    report: dict[str, Any] = {
        "versions": {
            p: version(p)
            for p in ["scanpy", "anndata", "numpy", "pandas", "scipy", "matplotlib"]
        },
        "cases": {},
    }
    with plt.rc_context(
        {"figure.figsize": (3, 3), "figure.dpi": 100, "savefig.dpi": 150}
    ):
        for name, options in reference_cases().items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                adata = make_adata()
                axes = sc.pl.umap(adata, **options, size=sizes, show=False)
            axes = axes if isinstance(axes, list) else [axes]
            fig = axes[0].figure
            fig.canvas.draw()
            fig.savefig(args.output / f"{name}.png", dpi=150, bbox_inches="tight")
            panels = []
            keys = options["color"]
            keys = [keys] if isinstance(keys, str) else keys
            for i, (ax, key) in enumerate(zip(axes, keys, strict=True)):
                artist = next(c for c in ax.collections if len(c.get_offsets()) == 8)
                values = (
                    adata.obs[key].to_numpy()
                    if key in adata.obs
                    else np.asarray(adata.raw[:, key].X).ravel()
                )
                categorical = key in adata.obs and isinstance(
                    adata.obs[key].dtype, pd.CategoricalDtype
                )
                order = (
                    np.argsort(~pd.isna(values), kind="stable")
                    if categorical
                    else np.argsort(-values, kind="stable")[::-1]
                )
                # Verify source-position preparation against rendered offsets;
                # coordinates and duplicate labels never serve as identity joins.
                np.testing.assert_array_equal(
                    artist.get_offsets(), adata.obsm["X_umap"][order, :2]
                )
                box = ax.get_window_extent()
                fig.savefig(
                    args.output / f"{name}-panel-{i}.png",
                    dpi=150,
                    bbox_inches=box.transformed(fig.dpi_scale_trans.inverted()),
                    pad_inches=0,
                )
                panels.append(
                    {
                        "order": order.tolist(),
                        "sizes": artist.get_sizes().tolist(),
                        "coordinates": np.asarray(artist.get_offsets()).tolist(),
                        "colors": [
                            to_hex(c, keep_alpha=True) for c in artist.get_facecolors()
                        ],
                        "x_domain": list(ax.get_xlim()),
                        "y_domain": list(ax.get_ylim()),
                        "plot_size": [box.width, box.height],
                        "title": ax.get_title(),
                        "frameon": bool(ax.axison),
                        "labels": [ax.get_xlabel(), ax.get_ylabel()],
                        "legend": [t.get_text() for t in ax.get_legend().texts]
                        if ax.get_legend() is not None
                        else None,
                        "color_domain": [artist.norm.vmin, artist.norm.vmax]
                        if artist.get_array() is not None
                        else None,
                    }
                )
            report["cases"][name] = {
                "options": options,
                "panels": panels,
                "figure_dpi": 100,
                "export_dpi": 150,
            }
            plt.close(fig)
        for marker, token, linewidth in [
            (".", "dot", 0),
            ("o", "circle", 0),
            (".", "dot-stroke", 2),
        ]:
            a = make_adata()[:1].copy()
            a.obsm["X_umap"] = np.array([[0.0, 0.0]])
            ax = sc.pl.umap(
                a,
                size=144,
                marker=marker,
                frameon=False,
                na_color="black",
                show=False,
                edgecolor="black" if linewidth else "none",
                linewidths=linewidth,
            )
            fig = ax.figure
            fig.canvas.draw()
            box = ax.get_window_extent()
            fig.savefig(
                args.output / f"footprint-{token}.png",
                dpi=150,
                bbox_inches=box.transformed(fig.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            path = MarkerStyle(marker)
            path_width = (
                path.get_path().transformed(path.get_transform()).get_extents().width
            )
            report[f"footprint_{token}"] = {
                "marker": marker,
                "size": 144,
                "path_width": path_width,
                "linewidth": linewidth,
                "diameter_at_export": (12 * path_width + linewidth) * 150 / 72,
                "plot_size_at_display": [box.width, box.height],
                "export_dpi": 150,
                "display_dpi": 100,
            }
            plt.close(fig)
    report["assets"] = {
        p.name: sha256(p.read_bytes()).hexdigest()
        for p in sorted(args.output.glob("*.png"))
    }
    report["fixture_sha256"] = sha256(
        Path(__file__).with_name("fixture_data.py").read_bytes()
    ).hexdigest()
    (args.output / "umap.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    main()
