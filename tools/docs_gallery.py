"""Framework-agnostic core for the documentation example gallery.

Each example under ``docs/examples/<name>.py`` is a runnable module that defines
a ``chart`` object and, optionally, a ``META`` mapping. Importing the module and
serializing ``chart`` is the single source of truth for the gallery.

This module only collects examples and provides shared paths and category
metadata. The Sphinx extension (``docs/_ext/genomespy_gallery.py``) turns
collected examples into gallery pages, and ``tools/render_thumbnails.py``
renders the checked-in PNG thumbnails. Keeping this core framework-agnostic
lets both reuse it.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
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
    "Association plots": (
        10,
        "Genome-wide association views such as Manhattan and QQ plots.",
    ),
    "Volcano and MA plots": (
        20,
        "Differential-effect views such as volcano and MA plots.",
    ),
    "Genome browser tracks": (
        30,
        "Shared-locus browser views with signal tracks or read-level detail.",
    ),
    "Reference annotation tracks": (
        40,
        "Reference tracks such as cytobands, sequence, gene models, and annotations.",
    ),
    "Mutation position plots": (
        50,
        "Mutation-position views such as lollipop, rainfall, and variant tracks.",
    ),
    "Oncoprints and cohort summaries": (
        60,
        "Cohort-level alteration matrices and related summaries.",
    ),
    "Set intersections": (
        65,
        "Set-membership combinations and intersection-size summaries.",
    ),
    "Copy-number plots": (
        70,
        "Genome-wide copy-number and allele-specific signal views.",
    ),
    "Basics": (90, "Core chart types and grammar building blocks."),
}
UNKNOWN_CATEGORY = (100, "")


@dataclass(frozen=True, slots=True)
class DataPreview:
    """Small, serializable table preview captured from an example module."""

    title: str
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


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
    max_width: int | None
    source: str
    spec: dict
    previews: tuple[DataPreview, ...] = ()


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
    summary = rest.strip().split("\n\n", 1)[0].strip()
    return title, summary


def _data_previews(module: ModuleType) -> tuple[DataPreview, ...]:
    configured = getattr(module, "DATA_PREVIEW", None)
    if configured is None:
        return ()
    if hasattr(configured, "head"):
        configured = {"Data preview": configured}
    if not isinstance(configured, dict):
        raise TypeError(
            "DATA_PREVIEW must be a DataFrame or mapping of names to DataFrames"
        )

    previews: list[DataPreview] = []
    for title, frame in configured.items():
        if not hasattr(frame, "head") or not hasattr(frame, "itertuples"):
            raise TypeError(f"DATA_PREVIEW[{title!r}] must be a DataFrame-like object")
        head = frame.head(5)
        columns = tuple(str(column) for column in head.columns)
        rows = tuple(
            tuple(str(value) for value in row)
            for row in head.itertuples(index=False, name=None)
        )
        previews.append(DataPreview(str(title), columns, rows))
    return tuple(previews)


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
        max_width=(
            int(meta["max_width"]) if meta.get("max_width") is not None else None
        ),
        source=path.read_text(encoding="utf-8"),
        spec=chart.to_dict(),
        previews=_data_previews(module),
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


def build_token(examples: list[Example]) -> str:
    """Return a short content-derived token for cache-busting gallery links."""
    digest = hashlib.sha256()
    for example in examples:
        digest.update(example.name.encode("utf-8"))
        digest.update(example.title.encode("utf-8"))
        digest.update(example.source.encode("utf-8"))
        digest.update(json.dumps(example.spec, sort_keys=True).encode("utf-8"))
    return digest.hexdigest()[:12]


def thumb_filename(example: Example) -> str:
    """Return the checked-in PNG thumbnail name for an example."""
    png_name = f"{example.name}.png"
    if not (THUMBS_DIR / png_name).exists():
        raise FileNotFoundError(
            f"Missing PNG thumbnail for docs example {example.name!r}. "
            "Add the manually reviewed thumbnail before building the docs."
        )
    return png_name
