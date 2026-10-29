"""Prepare the notebooks' analysis inputs explicitly, outside the Sphinx build."""

from __future__ import annotations

import argparse
from contextlib import chdir
import json
import logging
from pathlib import Path
import sys
from time import perf_counter
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/_ext"))

from genomespy_notebook import (  # noqa: E402
    _file_digest,
    _preparation_current,
    _preparation_digest,
    _prepared_paths,
)

log = logging.getLogger(__name__)


def main() -> None:
    """Run analysis cells once and cache their AnnData outputs with source hashes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "guides", nargs="*", help="Guide names; default: all prepared guides"
    )
    args = parser.parse_args()
    folder = ROOT / "integrations/scanpy/guides"
    paths = (
        [folder / f"{name}.ipynb" for name in args.guides]
        if args.guides
        else sorted(folder.glob("*.ipynb"))
    )
    if any(path.resolve().parent != folder for path in paths):
        parser.error(
            "Guide names must refer to notebooks in integrations/scanpy/guides."
        )
    import scanpy as sc

    sc.settings.datasetdir = ROOT / "tmp/scanpy-datasets"
    downloads = ROOT / "tmp/scanpy-guide-data/downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    with chdir(downloads):
        for path in paths:
            notebook = json.loads(path.read_text())
            prepared = _prepared_paths(notebook, ROOT)
            if not prepared:
                continue
            if _preparation_current(notebook, ROOT):
                log.info("%s: prepared inputs are current", path.stem)
                continue
            started = perf_counter()
            namespace: dict[str, Any] = {"__name__": "__genomespy_preparation__"}
            for index, cell in enumerate(notebook["cells"]):
                metadata = cell.get("metadata", {})
                if (
                    cell["cell_type"] != "code"
                    or metadata.get("genomespy", {}).get("chart")
                    or "jupyter-only" in metadata.get("tags", [])
                ):
                    continue
                log.info("%s: preparing cell %d", path.stem, index + 1)
                exec(
                    compile(
                        "".join(cell["source"]), f"{path}:cell {index + 1}", "exec"
                    ),
                    namespace,
                )
            signature = _preparation_digest(notebook)
            for name, target in prepared.items():
                target.parent.mkdir(parents=True, exist_ok=True)
                temporary = target.with_suffix(".partial.h5ad")
                namespace[name].write_h5ad(temporary, compression="gzip")
                temporary.replace(target)
                target.with_suffix(".sha256").write_text(
                    f"{signature}\n{_file_digest(target)}\n"
                )
                log.info(
                    "%s: %s; %.1f MB cached",
                    name,
                    namespace[name].shape,
                    target.stat().st_size / 1e6,
                )
            log.info("%s: prepared in %.1fs", path.stem, perf_counter() - started)


if __name__ == "__main__":
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.INFO)
    main()
