"""Sphinx extension that builds the GenomeSpy example gallery.

On ``builder-inited`` it turns every ``docs/examples/<name>.py`` module into:

* a spec JSON under ``_static/specs/`` that the browser hydrates,
* a checked-in PNG thumbnail under ``_static/gallery/``,
* a per-example detail page with the live interactive chart and source, and
* the gallery landing page grouped into category sections.

It also registers the ``genomespy-minigallery`` directive, which renders the
image-tile showcase used on the site's landing page.

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


def _card_html(
    example: core.Example, *, link_prefix: str, thumb_prefix: str, build_token: str
) -> str:
    thumb = f"{thumb_prefix}/{core.thumb_filename(example)}?v={build_token}"
    href = f"{link_prefix}{example.name}.html?v={build_token}"
    return (
        f'<a class="gs-card" href="{href}">'
        f'<span class="gs-card__shot" style="background-image:url({thumb})" '
        f'role="img" aria-label="{html.escape(example.title)}"></span>'
        f'<span class="gs-card__body"><span class="gs-card__title">'
        f"{html.escape(example.title)}</span></span></a>"
    )


def _gallery_index_md(examples: list[core.Example]) -> str:
    token = core.build_token(examples)
    blocks = [
        "---",
        "html_theme.sidebar_secondary.remove: true",
        "---",
        "",
        "# Example gallery",
        "",
        "Each card opens the live chart and the Python code that produced it.",
        "",
    ]
    for category, items in core.grouped_by_category(examples):
        blurb = core.CATEGORIES.get(category, core.UNKNOWN_CATEGORY)[1]
        cards = "\n".join(
            _card_html(
                e,
                link_prefix="",
                thumb_prefix="../_static/gallery",
                build_token=token,
            )
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

    # Keep generated detail pages in visible navigation. PyData's sidebar is
    # built from toctrees, so every generated example must be listed here.
    blocks.append("## Browse by Category")
    blocks.append("")
    for category, items in core.grouped_by_category(examples):
        blocks.append("```{toctree}")
        blocks.append(":maxdepth: 1")
        blocks.append(f":caption: {category}")
        blocks.append("")
        blocks.extend(e.name for e in items)
        blocks.append("```")
        blocks.append("")
    return "\n".join(blocks)


def _preview_html(example: core.Example) -> str:
    sections = []
    for preview in example.previews:
        header = "".join(
            f"<th>{html.escape(column)}</th>" for column in preview.columns
        )
        rows = "".join(
            "<tr>"
            + "".join(f"<td>{html.escape(value)}</td>" for value in row)
            + "</tr>"
            for row in preview.rows
        )
        sections.append(
            f'<figure class="gs-data-preview"><figcaption>{html.escape(preview.title)}'
            f'</figcaption><div class="gs-data-preview__scroll"><table><thead><tr>{header}'
            f"</tr></thead><tbody>{rows}</tbody></table></div></figure>"
        )
    return '<div class="gs-data-previews">' + "".join(sections) + "</div>"


def _detail_md(example: core.Example, bundle_url: str) -> str:
    spec_token = core.build_token([example])
    spec_url = f"../_static/specs/{example.name}.json?v={spec_token}"
    download_url = f"../_static/specs/{example.name}.json"
    # GenomeSpy's own docs use an inline custom element backed by shadow DOM
    # instead of an iframe. Follow that pattern here so the chart feels like a
    # native part of the page while still isolating embed styles from Sphinx.
    host_id = f"gs-embed-{example.name}"
    host_style = f"height:{example.height}px"
    if example.max_width is not None:
        host_style += f";max-width:{example.max_width}px"
    embed = (
        f'<div id="{host_id}" class="gs-doc-embed" style="{host_style}" '
        f'role="img" aria-label="{html.escape(example.title)}"></div>\n'
        '<script type="module">\n'
        f"import {{ embed }} from '{bundle_url}';\n"
        f"const host = document.getElementById('{host_id}');\n"
        "if (host && !host.shadowRoot) {\n"
        "  const shadow = host.attachShadow({ mode: 'open' });\n"
        "  shadow.innerHTML = `"
        "<style>"
        ":host{display:block}"
        "#shell{position:relative;width:100%;height:100%;overflow:hidden}"
        "#c{position:absolute;inset:0;overflow:hidden;opacity:0;transition:opacity .2s ease}"
        "#c canvas{display:block}"
        "#load{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;"
        "color:#8a97a8;font:14px/1.4 Lato,system-ui,sans-serif}"
        "</style>"
        "<div id='shell'><div id='load'>Loading chart...</div><div id='c'></div></div>`;\n"
        "  const c = shadow.getElementById('c');\n"
        "  const load = shadow.getElementById('load');\n"
        f"  const spec = await fetch('{spec_url}').then((r) => r.json());\n"
        "  await embed(c, spec, { bare: true });\n"
        "  let last = '', stable = 0;\n"
        "  const reveal = () => { c.style.opacity = '1'; if (load) load.remove(); };\n"
        "  const iv = setInterval(() => {\n"
        "    const cv = c.querySelector('canvas'); if (!cv) return;\n"
        "    const r = cv.getBoundingClientRect();\n"
        "    const size = `${Math.round(r.width)}x${Math.round(r.height)}`;\n"
        "    if (size === last && r.width > 0 && r.height > 0) {\n"
        "      if (++stable >= 3) { clearInterval(iv); reveal(); }\n"
        "    } else { stable = 0; last = size; }\n"
        "  }, 160);\n"
        "  setTimeout(() => { clearInterval(iv); reveal(); }, 4000);\n"
        "}\n"
        "</script>"
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
    ]
    if example.previews:
        parts += [
            "## Data preview",
            "",
            "```{raw} html",
            _preview_html(example),
            "```",
            "",
        ]
    parts += [
        "## Code",
        "",
        "```python",
        example.source.rstrip(),
        "```",
        "",
        f"[Download the generated GenomeSpy spec]({download_url})",
        "",
    ]
    return "\n".join(parts)


def _remove_stale_build_outputs(app: Any, stale_names: set[str]) -> None:
    outdir_value = getattr(app, "outdir", None)
    doctreedir_value = getattr(app, "doctreedir", None)
    if outdir_value is None:
        return

    outdir = Path(outdir_value)
    for name in stale_names:
        candidates = [
            outdir / "gallery" / f"{name}.html",
            outdir / "gallery" / name / "index.html",
            outdir / "_sources" / "gallery" / f"{name}.md.txt",
            outdir / "_static" / "specs" / f"{name}.json",
            outdir / "_static" / "gallery" / f"{name}.png",
            outdir / "_static" / "gallery" / f"{name}.svg",
        ]
        if doctreedir_value is not None:
            candidates.append(Path(doctreedir_value) / "gallery" / f"{name}.doctree")
        for path in candidates:
            if path.is_file():
                path.unlink()
        downloads = outdir / "_downloads"
        if downloads.is_dir():
            for path in downloads.glob(f"**/{name}.json"):
                path.unlink()


def _generate(app: Any) -> None:
    active_names = {
        path.stem
        for path in core.EXAMPLES_DIR.glob("*.py")
        if not path.name.startswith("_")
    }
    stale_names = {
        path.stem
        for path in core.GALLERY_PAGES_DIR.glob("*.md")
        if path.stem != "index" and path.stem not in active_names
    }
    stale_names.update(
        path.stem
        for path in core.SPECS_DIR.glob("*.json")
        if path.stem not in active_names
    )
    outdir_value = getattr(app, "outdir", None)
    if outdir_value is not None:
        stale_names.update(
            path.stem
            for path in (Path(outdir_value) / "gallery").glob("*.html")
            if path.stem != "index" and path.stem not in active_names
        )

    for path in core.GALLERY_PAGES_DIR.glob("*.md"):
        if path.stem != "index" and path.stem not in active_names:
            path.unlink()
    for path in core.SPECS_DIR.glob("*.json"):
        if path.stem not in active_names:
            path.unlink()
    _remove_stale_build_outputs(app, stale_names)

    examples = core.collect_examples()
    bundle_url = core.default_bundle_url()

    for example in examples:
        _write(
            core.SPECS_DIR / f"{example.name}.json",
            json.dumps(example.spec, indent=2),
        )
        _write(
            core.GALLERY_PAGES_DIR / f"{example.name}.md",
            _detail_md(example, bundle_url),
        )

    _write(core.GALLERY_PAGES_DIR / "index.md", _gallery_index_md(examples))
    if hasattr(app, "env"):
        app.env.genomespy_examples = examples  # type: ignore[attr-defined]


def _generate_on_config(app: Any, _config: Any) -> None:
    _generate(app)


class GenomeSpyMiniGallery(Directive):
    """Render the image-tile showcase for the landing page."""

    has_content = False

    def run(self) -> list[nodes.Node]:
        examples: list[core.Example] = getattr(
            self.state.document.settings.env, "genomespy_examples", []
        )
        if not examples:
            examples = core.collect_examples()
        token = core.build_token(examples)
        tiles = "\n".join(
            f'<a class="preview" href="gallery/{e.name}.html?v={token}" '
            f'title="{html.escape(e.title)}" '
            f'style="background-image:url(_static/gallery/{core.thumb_filename(e)}?v={token})"></a>'
            for e in examples
        )
        markup = (
            f'<div id="gs-showcase"><div class="gs-showcase-track">{tiles}</div></div>'
        )
        return [nodes.raw("", markup, format="html")]


def setup(app: Any) -> dict[str, Any]:
    app.connect("config-inited", _generate_on_config)
    app.add_directive("genomespy-minigallery", GenomeSpyMiniGallery)
    return {"parallel_read_safe": False, "parallel_write_safe": True}
