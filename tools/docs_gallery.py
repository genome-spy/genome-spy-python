"""Framework-agnostic core for the documentation example gallery.

Each example under ``docs/examples/<name>.py`` is a runnable module that defines
a ``chart`` object and, optionally, a ``META`` mapping. Importing the module and
serializing ``chart`` is the single source of truth for the gallery.

This module only collects examples and provides shared paths, category metadata,
and the SVG fallback poster. The Sphinx extension (``docs/_ext/genomespy_gallery.py``)
turns collected examples into gallery pages, and ``tools/render_thumbnails.py``
renders real PNG thumbnails. Keeping this core framework-agnostic lets both reuse it.
"""

from __future__ import annotations

import html
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
EXAMPLES_DIR = DOCS_DIR / "examples"
STATIC_DIR = DOCS_DIR / "_static"
GALLERY_PAGES_DIR = DOCS_DIR / "gallery"
THUMBS_DIR = STATIC_DIR / "gallery"
SPECS_DIR = STATIC_DIR / "specs"

# Category display order and one-line blurbs. Unknown categories sort last.
CATEGORIES: dict[str, tuple[int, str]] = {
    "GWAS": (10, "Genome-wide association scans: Manhattan, QQ, and locus zoom views."),
    "RNA-seq": (
        20,
        "Expression and differential-expression views such as volcano and MA plots.",
    ),
    "Genome tracks": (
        30,
        "Coverage, peak, and gene-annotation tracks sharing a genomic axis.",
    ),
    "Populations": (
        40,
        "Ancestry and population-structure views such as admixture bars.",
    ),
    "Basics": (50, "Core grammar and Altair-style ergonomics on tabular data."),
}
UNKNOWN_CATEGORY = (100, "")


@dataclass(frozen=True, slots=True)
class Example:
    """Metadata and rendered artifacts for one gallery example."""

    name: str
    title: str
    description: str
    category: str
    tags: tuple[str, ...]
    order: int
    height: int
    source: str
    spec: dict


def _ensure_src_on_path() -> None:
    src = str(REPO_ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)


def default_bundle_url() -> str:
    """The pinned GenomeSpy JS bundle URL that examples embed and render with."""
    _ensure_src_on_path()
    from genome_spy.chart import DEFAULT_EMBED_URL

    return DEFAULT_EMBED_URL


def _load_module(path: Path) -> ModuleType:
    module_name = f"_gs_gallery_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load example module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _docstring_parts(module: ModuleType, fallback: str) -> tuple[str, str]:
    doc = (module.__doc__ or "").strip()
    if not doc:
        return fallback, ""
    title, _, rest = doc.partition("\n")
    title = title.strip().rstrip(".") or fallback
    return title, rest.strip()


def collect_example(path: Path) -> Example:
    """Import one example module and capture its chart spec and metadata."""
    _ensure_src_on_path()
    module = _load_module(path)
    if not hasattr(module, "chart"):
        raise AttributeError(f"{path.name} does not define a `chart` object")

    chart = module.chart
    if not hasattr(chart, "to_dict"):
        raise TypeError(f"{path.name}'s `chart` is not serializable")

    meta = getattr(module, "META", {}) or {}
    title, description = _docstring_parts(module, path.stem.replace("_", " ").title())

    return Example(
        name=path.stem,
        title=meta.get("title", title),
        description=meta.get("description", description),
        category=meta.get("category", "Basics"),
        tags=tuple(meta.get("tags", ())),
        order=int(meta.get("order", 100)),
        height=int(meta.get("height", 400)),
        source=path.read_text(encoding="utf-8"),
        spec=chart.to_dict(),
    )


def collect_examples() -> list[Example]:
    """Collect every example module under ``docs/examples`` in a stable order."""
    return [
        collect_example(path)
        for path in sorted(EXAMPLES_DIR.glob("*.py"))
        if not path.name.startswith("_")
    ]


def grouped_by_category(examples: list[Example]) -> list[tuple[str, list[Example]]]:
    """Group examples by category, ordered by the category registry."""
    groups: dict[str, list[Example]] = {}
    for example in examples:
        groups.setdefault(example.category, []).append(example)
    for items in groups.values():
        items.sort(key=lambda e: (e.order, e.title))
    return sorted(
        groups.items(), key=lambda kv: CATEGORIES.get(kv[0], UNKNOWN_CATEGORY)[0]
    )


def thumb_filename(example: Example) -> str:
    """Thumbnail file name, preferring a rendered PNG over the SVG fallback."""
    if (THUMBS_DIR / f"{example.name}.png").exists():
        return f"{example.name}.png"
    return f"{example.name}.svg"


def poster_svg(example: Example) -> str:
    """Static SVG poster used when no PNG screenshot has been rendered."""
    category = html.escape(example.category.upper())
    seed = sum(ord(char) for char in example.name)
    dots = "".join(
        f'<circle cx="{60 + (i * 53) % 520}" cy="{300 - (seed * (i + 3)) % 150}" '
        f'r="4" fill="#{"3e8cb6" if i % 2 else "7fbbdd"}" opacity="0.9"/>'
        for i in range(46)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="{html.escape(example.title)}">
  <rect width="640" height="360" fill="#f4f8fb"/>
  <line x1="48" y1="312" x2="600" y2="312" stroke="#d5dee6" stroke-width="1.5"/>
  <line x1="48" y1="312" x2="48" y2="70" stroke="#d5dee6" stroke-width="1.5"/>
  <g>{dots}</g>
  <line x1="48" y1="150" x2="600" y2="150" stroke="#c53b2c" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="48" y="52" fill="#3e8cb6" font-family="Lato, system-ui, sans-serif" font-size="15" letter-spacing="2" font-weight="700">{category}</text>
</svg>
"""
