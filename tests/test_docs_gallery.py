"""Every documentation gallery example must import and serialize to a valid spec.

Building a chart's dict runs it through the generated schema validation path, so
this test doubles as a schema check for the authored examples.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "docs" / "examples"


def _load_gallery():
    path = REPO_ROOT / "tools" / "docs_gallery.py"
    spec = importlib.util.spec_from_file_location("_gs_docs_gallery", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _example_paths() -> list[Path]:
    return [p for p in sorted(EXAMPLES_DIR.glob("*.py")) if not p.name.startswith("_")]


def test_gallery_has_examples() -> None:
    assert _example_paths(), "no gallery examples found under docs/examples/"


@pytest.mark.parametrize("path", _example_paths(), ids=lambda p: p.stem)
def test_example_builds_valid_spec(path: Path) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(path)

    assert example.title
    assert isinstance(example.spec, dict)
    assert example.spec, "serialized spec is empty"
    assert (
        "$schema" in example.spec or "mark" in example.spec or "layer" in example.spec
    )
