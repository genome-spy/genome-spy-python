"""Build pinned GenomeSpy browser modules for offline rendering.

Run with uv run python tools/vendor_javascript.py. Requires npm and network
access only when regenerating the checked-in assets.
"""

from __future__ import annotations

import json
import subprocess
import tarfile
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Bundle the repository's pinned Core, controls, and Inspector as ESM."""
    with (ROOT / "pyproject.toml").open("rb") as file:
        version = tomllib.load(file)["tool"]["genome-spy"]["core-version"]
    with tempfile.TemporaryDirectory(prefix="genome-spy-javascript-") as tmp:
        work = Path(tmp)
        for name in ("core", "inspector"):
            destination = work / name
            destination.mkdir()
            result = subprocess.run(
                [
                    "npm",
                    "pack",
                    f"@genome-spy/{name}@{version}",
                    "--json",
                    "--pack-destination",
                    str(destination),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            archive_path = destination / json.loads(result.stdout)[0]["filename"]
            with tarfile.open(archive_path, "r:gz") as archive:
                archive.extractall(destination, filter="data")

        font_license = (
            work / "core/package/dist/src/rendering/webgl/fonts/OFL.txt"
        ).read_text(encoding="utf-8")
        (ROOT / "LICENSES/LATO-OFL-1.1.txt").write_text(font_license, encoding="utf-8")
        for output, entry in (
            ("genome-spy", "core/package/dist/bundle/index.es.js"),
            ("controls", "core/package/dist/src/controls.js"),
            ("inspector", "inspector/package/dist/index.es.js"),
        ):
            banner = f"// Vendored from GenomeSpy {version}."
            if output == "genome-spy":
                banner += "\n/*!\n" + font_license + "\n*/"
            subprocess.run(
                [
                    "npm",
                    "exec",
                    "--yes",
                    "--package=esbuild@0.25.9",
                    "--",
                    "esbuild",
                    str(work / entry),
                    "--bundle",
                    "--format=esm",
                    "--platform=browser",
                    "--minify",
                    "--legal-comments=inline",
                    f"--banner:js={banner}",
                    f"--outfile={ROOT / 'src/genome_spy/static' / (output + '.js')}",
                ],
                check=True,
            )


if __name__ == "__main__":
    main()
