"""The generated API reference index must stay in step with the public API."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import genome_spy as gs
import pytest

pytestmark = pytest.mark.docs

REPO_ROOT = Path(__file__).resolve().parent.parent
API_PAGE = REPO_ROOT / "docs" / "api.md"
TEMPLATES_DIR = REPO_ROOT / "docs" / "_templates" / "autosummary"


def _load_generator():
    path = REPO_ROOT / "tools" / "generate_api_docs.py"
    spec = importlib.util.spec_from_file_location("_gs_api_docs", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _listed_names() -> list[str]:
    page = API_PAGE.read_text(encoding="utf-8")
    entries = re.findall(r"^   ([A-Za-z_][A-Za-z_0-9]*)$", page, re.M)
    return entries


def test_api_page_is_up_to_date() -> None:
    generator = _load_generator()

    assert API_PAGE.read_text(encoding="utf-8") == generator.render_api_page(), (
        "docs/api.md is stale; run `uv run python tools/generate_api_docs.py`."
    )


def test_every_public_export_is_documented_once() -> None:
    listed = _listed_names()
    exported = {name for name in gs.__all__ if not name.startswith("__")}

    for name in exported:
        if name in listed:
            assert listed.count(name) == 1, f"{name} is in more than one API section"
            continue
        # Exported instances, such as ``gs.lazy``, are documented through their
        # class page instead of getting one of their own.
        class_name = type(getattr(gs, name)).__name__
        assert class_name in listed, f"{name} is not documented in docs/api.md"


def test_case_colliding_names_use_separate_stub_directories() -> None:
    """``Locus`` and ``locus`` must not share one autosummary output directory."""
    page = API_PAGE.read_text(encoding="utf-8")
    blocks = page.split(":toctree: generated/")[1:]
    groups = {block.split("/", 1)[0]: block for block in blocks}

    assert re.search(r"^   Locus$", groups["channels"], re.M)
    assert re.search(r"^   locus$", groups["functions"], re.M)


def test_custom_templates_are_referenced_with_the_autosummary_prefix() -> None:
    """Sphinx silently falls back to its base template for unresolved names."""
    page = API_PAGE.read_text(encoding="utf-8")
    referenced = set(re.findall(r":template: (\S+)", page))

    assert referenced, "no custom autosummary template is referenced"
    for template in referenced:
        assert template.startswith("autosummary/"), template
        assert (TEMPLATES_DIR.parent / template).is_file(), template


def test_class_template_lists_methods_before_their_descriptions() -> None:
    """The rubric must sit *inside* the ``autoclass`` body.

    Indentation is what puts the summary table above the generated member
    descriptions; dedenting it would move the table below them while leaving
    the file's ordering unchanged.
    """
    template = (TEMPLATES_DIR / "class.rst").read_text(encoding="utf-8")

    assert ":members:" in template
    assert ":inherited-members:" in template
    assert "\n   .. rubric:: Methods" in template
    assert "\n   .. autosummary::" in template
