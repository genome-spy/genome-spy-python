"""Explicitly freeze Scanpy 1.11.5 grouped data/statistics without figure rendering.

Run ``uv run --no-sync python -m tests.integrations.scanpy.generate_grouped_references``.
Production and ordinary tests do not call Scanpy plotting or import this module.
The fixture is original project data under MIT; no upstream code is vendored.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from typing import Any
import warnings


def _frame(frame: Any) -> dict[str, Any]:
    return {
        "index": [str(value) for value in frame.index],
        "columns": list(frame.columns),
        "values": json.loads(frame.to_json(orient="values", double_precision=15)),
    }


def main() -> None:
    import scanpy as sc

    from tests.integrations.scanpy.grouped_fixture import (
        grouped_cases,
        make_grouped_adata,
    )

    if version("scanpy") != "1.11.5":
        raise RuntimeError("Grouped reference generation requires Scanpy 1.11.5.")
    result: dict[str, Any] = {
        "versions": {
            name: version(name)
            for name in ("scanpy", "anndata", "numpy", "pandas", "scipy")
        },
        "fixture_sha256": sha256(
            Path(__file__).with_name("grouped_fixture.py").read_bytes()
        ).hexdigest(),
        "cases": {},
    }
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Observation names are not unique")
        for name, options in grouped_cases().items():
            adata = make_grouped_adata()
            adata.obs.index.name = "barcode"
            if name == "multiple_groups":
                adata = adata[adata.obs["group"].notna()].copy()
            call = {"var_names": ["g1", "g2", "g3"], "groupby": "group", **options}
            plot = sc.pl.DotPlot(adata, **call)
            order = (
                plot.categories
                if plot.categories_order is None
                else plot.categories_order
            )
            result["cases"][name] = {
                "categories": [str(value) for value in order],
                "table": _frame(plot.obs_tidy),
                "means": _frame(plot.dot_color_df),
                "fractions": _frame(plot.dot_size_df),
                "feature_groups": []
                if plot.var_groups is None
                else [
                    {"label": label, "start": start, "end": end}
                    for label, (start, end) in zip(
                        plot.var_groups.labels, plot.var_groups.positions, strict=True
                    )
                ],
            }
    Path(__file__).with_name("fixtures").joinpath("grouped.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
