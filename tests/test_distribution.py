"""Build real archives to keep local research and generated files out of releases."""

from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import zipfile


def test_distributions_exclude_local_outputs_without_git(tmp_path):
    root = Path(__file__).resolve().parents[1]
    project = tmp_path / "tmp" / "project"
    project.mkdir(parents=True)
    for name in (
        "pyproject.toml",
        "README.md",
        "THIRD_PARTY_NOTICES.md",
        "LICENSE",
        ".gitignore",
    ):
        shutil.copyfile(root / name, project / name)
    shutil.copytree(root / "LICENSES", project / "LICENSES")

    files = {
        "src/genome_spy/__init__.py": "",
        "skills/create-genomespy-visualization/SKILL.md": "# Test skill\n",
        "tests/fixtures/expected.json": "{}",
        "tmp/scanpy-guide-data/cache.h5ad": "local data",
        "data/pbmc3k_raw.h5ad": "downloaded data",
        "plans/report.md": "local report",
        "material/reference.pdf": "local reference",
        "docs/_build/chart.html": "generated page",
        "docs/gallery/generated.md": "generated gallery",
        "docs/generated/api.md": "generated API",
        "docs/_static/specs/chart.json": "{}",
        "docs/_static/generated/chart.png": "generated image",
        "tests/fixtures/chart.png": "test image",
        "tests/fixtures/chart-performance.json": "{}",
    }
    for name, contents in files.items():
        path = project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)

    output = tmp_path / "distributions"
    result = subprocess.run(
        [
            "uv",
            "build",
            "--offline",
            "--python",
            sys.executable,
            "--out-dir",
            str(output),
        ],
        cwd=project,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    with tarfile.open(next(output.glob("*.tar.gz"))) as archive:
        names = {name.partition("/")[2] for name in archive.getnames()}
    assert {
        "src/genome_spy/__init__.py",
        "LICENSE",
        "tests/fixtures/expected.json",
    } <= names
    assert not names.intersection(
        set(files)
        - {
            "src/genome_spy/__init__.py",
            "skills/create-genomespy-visualization/SKILL.md",
            "tests/fixtures/expected.json",
        }
    )
    with zipfile.ZipFile(next(output.glob("*.whl"))) as wheel:
        assert "genome_spy/__init__.py" in wheel.namelist()
        assert not any(
            name.startswith(("tmp/", "tests/", "docs/")) for name in wheel.namelist()
        )
