"""Generate Python wrappers from a version-pinned GenomeSpy npm package.

This module follows Altair's maintainer-time generation workflow: fetch the
version-pinned upstream JavaScript package, write generated Python/schema
artifacts into the package tree, and commit those artifacts. It is not a direct
copy of Altair's generator; it is a GenomeSpy-specific implementation shaped to
grow toward the same generated-schema plus handwritten-API architecture.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tarfile
import tempfile
import tomllib
from pathlib import Path
from typing import Any, cast

try:
    from schemapi.codegen import SchemaWrapperGenerator
except ModuleNotFoundError:
    from tools.schemapi.codegen import SchemaWrapperGenerator

DEFAULT_OUTPUT_DIR = Path("src/genome_spy/schema")
DEFAULT_SPEC_REFERENCE_DIR = Path(".cache/genome-spy-python/genomespy-core-spec")
PACKAGE_NAME = "@genome-spy/core"
SCHEMA_FILENAME = "genome-spy-schema.json"


def configured_core_version(pyproject_path: Path = Path("pyproject.toml")) -> str:
    """Read the configured GenomeSpy core npm package version."""
    with pyproject_path.open("rb") as file:
        pyproject = tomllib.load(file)
    version = pyproject.get("tool", {}).get("genome-spy", {}).get("core-version")
    if not isinstance(version, str) or not version:
        raise ValueError("Missing [tool.genome-spy].core-version in pyproject.toml.")
    return version


def fetch_npm_package(version: str, destination: Path) -> Path:
    """Fetch ``@genome-spy/core`` from npm and unpack it into ``destination``."""
    destination.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                "npm",
                "pack",
                f"{PACKAGE_NAME}@{version}",
                "--pack-destination",
                str(destination),
                "--silent",
            ],
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "The schema generator requires npm to be installed and available on "
            "PATH because it fetches @genome-spy/core from the npm registry."
        ) from error
    tarballs = sorted(destination.glob("genome-spy-core-*.tgz"))
    if not tarballs:
        raise FileNotFoundError(f"npm pack did not create a {PACKAGE_NAME} tarball.")

    package_dir = destination / "package"
    with tarfile.open(tarballs[-1], "r:gz") as archive:
        archive.extractall(destination, filter="data")
    if not package_dir.exists():
        raise FileNotFoundError("Packed npm archive did not contain a package/ root.")
    return package_dir


def package_version(package_dir: Path) -> str:
    """Read the version from an unpacked npm package."""
    metadata = json.loads((package_dir / "package.json").read_text(encoding="utf-8"))
    version = metadata.get("version")
    if not isinstance(version, str):
        raise TypeError("GenomeSpy npm package.json must contain a string version.")
    return version


def load_schema(path: Path) -> dict[str, Any]:
    """Load a GenomeSpy JSON Schema file."""
    with path.open(encoding="utf-8") as file:
        schema = json.load(file)
    if not isinstance(schema, dict):
        raise TypeError("GenomeSpy schema must be a JSON object.")
    return cast(dict[str, Any], schema)


def copy_spec_references(package_dir: Path, output_dir: Path, version: str) -> None:
    """Copy compact TypeScript spec references into a local cache."""
    spec_dir = package_dir / "src" / "spec"
    if not spec_dir.exists():
        spec_dir = package_dir / "dist" / "src" / "spec"
    if not spec_dir.exists():
        raise FileNotFoundError(f"GenomeSpy package has no spec directory: {spec_dir}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(spec_dir.glob("*.d.ts")):
        shutil.copyfile(source, output_dir / source.name)
    (output_dir / "VERSION").write_text(version + "\n", encoding="utf-8")
    (output_dir / "README.md").write_text(
        (
            "# GenomeSpy Core Type References\n\n"
            f"Copied from `{PACKAGE_NAME}@{version}` during schema generation.\n"
            "These files are a local coding-agent cache for the compact schema "
            "source types. The npm package remains the source of truth.\n"
        ),
        encoding="utf-8",
    )


def write_schema_package(
    package_dir: Path,
    output_dir: Path,
    *,
    spec_reference_dir: Path | None,
) -> None:
    """Write generated GenomeSpy schema wrapper modules from an npm package."""
    schema_path = package_dir / "dist" / "schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"GenomeSpy package has no schema: {schema_path}")

    version = package_version(package_dir)
    schema = load_schema(schema_path)
    generator = SchemaWrapperGenerator(schema, schema_version=version)
    core_module = generator.generate_core_module()
    init_module = generator.generate_init_module(core_module.exports)
    mark_mixins_module = generator.generate_mark_mixins_module()
    channels_module = generator.generate_channels_module()

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_text = schema_path.read_text(encoding="utf-8").rstrip() + "\n"
    (output_dir / SCHEMA_FILENAME).write_text(schema_text, encoding="utf-8")
    (output_dir / "core.py").write_text(core_module.source, encoding="utf-8")
    (output_dir / "__init__.py").write_text(init_module.source, encoding="utf-8")
    (output_dir / "mixins.py").write_text(mark_mixins_module.source, encoding="utf-8")
    (output_dir / "channels.py").write_text(channels_module.source, encoding="utf-8")

    if spec_reference_dir is not None:
        copy_spec_references(package_dir, spec_reference_dir, version)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--core-version",
        default=configured_core_version(),
        help="Version of @genome-spy/core to fetch from npm.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where generated schema package files are written.",
    )
    parser.add_argument(
        "--spec-reference-dir",
        default=str(DEFAULT_SPEC_REFERENCE_DIR),
        help=(
            "Local cache directory where compact TypeScript spec reference files "
            "are copied. Use an empty string to skip copying references."
        ),
    )
    args = parser.parse_args()

    spec_reference_dir = (
        Path(args.spec_reference_dir) if args.spec_reference_dir else None
    )

    with tempfile.TemporaryDirectory(prefix="genome-spy-core-") as tmpdir:
        package_dir = fetch_npm_package(args.core_version, Path(tmpdir))
        write_schema_package(
            package_dir,
            args.output_dir,
            spec_reference_dir=spec_reference_dir,
        )

    print(
        f"Wrote generated GenomeSpy schema package from "
        f"{PACKAGE_NAME}@{args.core_version} to {args.output_dir}."
    )


if __name__ == "__main__":
    main()
