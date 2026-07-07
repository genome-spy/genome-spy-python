"""Sphinx extension that builds the GenomeSpy example gallery.

On ``builder-inited`` it turns every ``docs/examples/<name>.py`` module into:

* a spec JSON under ``_static/specs/`` that the browser hydrates,
* an SVG poster under ``_static/gallery/`` when no PNG screenshot exists,
* a per-example detail page with the live interactive chart and source, and
* the gallery landing page grouped into category sections.

It also registers the ``genomespy-minigallery`` directive, which renders the
Altair-style image-tile showcase used on the site's landing page.

Example modules are the single source of truth; authors never edit the
generated pages. The generation core lives in ``tools/docs_gallery.py`` so the
thumbnail renderer can reuse it.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import Directive

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "tools"))

import docs_gallery as core  # noqa: E402


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _card_html(example: core.Example, *, link_prefix: str, thumb_prefix: str) -> str:
    thumb = f"{thumb_prefix}/{core.thumb_filename(example)}"
    href = f"{link_prefix}{example.name}.html"
    tags = "".join(
        f'<span class="gs-tag">{html.escape(t)}</span>' for t in example.tags
    )
    return (
        f'<a class="gs-card" href="{href}">'
        f'<span class="gs-card__shot" style="background-image:url({thumb})" '
        f'role="img" aria-label="{html.escape(example.title)}"></span>'
        f'<span class="gs-card__body"><span class="gs-card__title">'
        f"{html.escape(example.title)}</span>"
        f'<span class="gs-card__tags">{tags}</span></span></a>'
    )


def _gallery_index_md(examples: list[core.Example]) -> str:
    blocks = [
        "---",
        "html_theme.sidebar_secondary.remove: true",
        "---",
        "",
        "# Example gallery",
        "",
        "Each example is a real, interactive GenomeSpy visualization. Click a card "
        "to open the live chart and its Python source.",
        "",
    ]
    for category, items in core.grouped_by_category(examples):
        blurb = core.CATEGORIES.get(category, core.UNKNOWN_CATEGORY)[1]
        cards = "\n".join(
            _card_html(e, link_prefix="", thumb_prefix="../_static/gallery")
            for e in items
        )
        blocks.append(f"## {category}")
        blocks.append("")
        if blurb:
            blocks.append(blurb)
            blocks.append("")
        blocks.append("```{raw} html")
        blocks.append('<div class="gs-gallery">')
        blocks.append(cards)
        blocks.append("</div>")
        blocks.append("```")
        blocks.append("")

    # Hidden toctree keeps the orphan detail pages linked for search/next-prev.
    blocks.append("```{toctree}")
    blocks.append(":hidden:")
    blocks.append("")
    blocks.extend(e.name for e in examples)
    blocks.append("```")
    blocks.append("")
    return "\n".join(blocks)


def _detail_md(example: core.Example, bundle_url: str) -> str:
    spec_url = f"../_static/specs/{example.name}.json"
    tags = " ".join(f"`{t}`" for t in example.tags)
    embed = (
        f'<div class="gs-live-embed" data-spec="{spec_url}" '
        f'data-bundle="{html.escape(bundle_url)}" data-autoload="1"></div>'
    )
    parts = [
        "---",
        "html_theme.sidebar_secondary.remove: true",
        "---",
        "",
        f"# {example.title}",
        "",
        example.description or "",
        "",
        "```{raw} html",
        embed,
        "```",
        "",
        "*Interactive: drag to pan, scroll or pinch to zoom.*",
        "",
    ]
    if tags:
        parts += [f"**Tags:** {tags}", ""]
    parts += [
        "## Source",
        "",
        "```python",
        example.source.rstrip(),
        "```",
        "",
        f"[Download the generated GenomeSpy spec]({spec_url})",
        "",
    ]
    return "\n".join(parts)


def _generate(app: Any) -> None:
    examples = core.collect_examples()
    bundle_url = core.default_bundle_url()

    for example in examples:
        _write(
            core.SPECS_DIR / f"{example.name}.json",
            json.dumps(example.spec, indent=2),
        )
        if not (core.THUMBS_DIR / f"{example.name}.png").exists():
            _write(core.THUMBS_DIR / f"{example.name}.svg", core.poster_svg(example))
        _write(
            core.GALLERY_PAGES_DIR / f"{example.name}.md",
            _detail_md(example, bundle_url),
        )

    _write(core.GALLERY_PAGES_DIR / "index.md", _gallery_index_md(examples))
    app.env.genomespy_examples = examples  # type: ignore[attr-defined]


class GenomeSpyMiniGallery(Directive):
    """Render the Altair-style image-tile showcase for the landing page."""

    has_content = False

    def run(self) -> list[nodes.Node]:
        examples: list[core.Example] = getattr(
            self.state.document.settings.env, "genomespy_examples", []
        )
        tiles = "\n".join(
            f'<a class="preview" href="gallery/{e.name}.html" '
            f'title="{html.escape(e.title)}" '
            f'style="background-image:url(_static/gallery/{core.thumb_filename(e)})"></a>'
            for e in examples
        )
        markup = (
            f'<div id="gs-showcase"><div class="gs-showcase-track">{tiles}</div></div>'
        )
        return [nodes.raw("", markup, format="html")]


def setup(app: Any) -> dict[str, Any]:
    app.connect("builder-inited", _generate)
    app.add_directive("genomespy-minigallery", GenomeSpyMiniGallery)
    return {"parallel_read_safe": False, "parallel_write_safe": True}
