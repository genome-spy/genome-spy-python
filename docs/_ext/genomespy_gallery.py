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

import ast
import html
import importlib.util
import json
import re
import sys
from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import Directive, directives

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "tools"))

import docs_gallery as core  # noqa: E402


_TUTORIALS_DIR = _REPO_ROOT / "docs" / "tutorials"
_TUTORIAL_TARGET = re.compile(
    r"(?P<module>[A-Za-z_][A-Za-z0-9_]*):(?P<attribute>[A-Za-z_][A-Za-z0-9_]*)"
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_arrow_assets(buffers: dict[str, bytes]) -> set[str]:
    """Write content-addressed Arrow assets and return their identifiers."""
    identifiers = set(buffers)
    for identifier, payload in buffers.items():
        if sha256(payload).hexdigest() != identifier:
            raise ValueError("Arrow asset identifier does not match its payload.")
        path = core.ARROW_DIR / f"{identifier}.arrow"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    return identifiers


def _rewrite_arrow_urls(spec: dict[str, Any], identifiers: set[str]) -> dict[str, Any]:
    """Replace private Arrow tokens with paths that work from gallery pages."""
    rewritten = deepcopy(spec)

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        if not isinstance(value, dict):
            return
        url = value.get("url")
        if isinstance(url, str) and url.startswith("arrow://"):
            identifier = url.removeprefix("arrow://")
            if identifier not in identifiers:
                raise ValueError(
                    f"Gallery spec references missing Arrow payload {identifier!r}."
                )
            # GenomeSpy derives ``_static/specs/`` from the URL passed to
            # ``embed``. That base is resolved from ``gallery/<example>.html``,
            # so the asset needs three parent segments to reach ``/_static``.
            value["url"] = f"../../../_static/generated/arrow/{identifier}.arrow"
        for child in value.values():
            visit(child)

    visit(rewritten)
    return rewritten


def _remove_stale_arrow_assets(referenced: set[str]) -> None:
    """Delete only generated Arrow assets no longer referenced by examples."""
    if not core.ARROW_DIR.is_dir():
        return
    for path in core.ARROW_DIR.glob("*.arrow"):
        if path.stem not in referenced:
            path.unlink()


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
        "# Example gallery",
        "",
        "Each card opens the live chart and the Python code that produced it. "
        "The [user guide](../user-guide/index.md) teaches the grammar they use.",
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

    # The sidebar is built from toctrees, so every generated detail page must be
    # listed here. They are hidden because the cards above already link them;
    # a visible toctree would repeat the whole gallery as a plain list.
    for category, items in core.grouped_by_category(examples):
        blocks.append("```{toctree}")
        blocks.append(":hidden:")
        blocks.append(":maxdepth: 1")
        blocks.append(f":caption: {category}")
        blocks.append("")
        blocks.extend(e.name for e in items)
        blocks.append("```")
        blocks.append("")
    return "\n".join(blocks)


def _load_tutorial_chart(target: str) -> Any:
    """Load one named chart from a docs-only tutorial module."""
    match = _TUTORIAL_TARGET.fullmatch(target)
    if match is None:
        raise ValueError("Tutorial chart target must use the form 'module:chart_name'.")

    module_name = match.group("module")
    path = _TUTORIALS_DIR / f"{module_name}.py"
    if not path.is_file():
        raise ValueError(f"Tutorial module does not exist: {path}")

    import_name = f"_genomespy_tutorial_{module_name}"
    module_spec = importlib.util.spec_from_file_location(import_name, path)
    if module_spec is None or module_spec.loader is None:
        raise ValueError(f"Cannot import tutorial module: {path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    attribute = match.group("attribute")
    try:
        chart = getattr(module, attribute)
    except AttributeError as exc:
        raise ValueError(
            f"Tutorial module {module_name!r} has no chart {attribute!r}."
        ) from exc
    if not callable(getattr(chart, "to_dict", None)):
        raise ValueError(f"Tutorial target {target!r} is not a chart.")
    return chart


def _tutorial_embed_html(
    target: str,
    spec: dict[str, Any],
    *,
    bundle_url: str,
    height: int,
    title: str,
    identity: str,
    controls: tuple[str, ...] = (),
    control_definitions: dict[str, dict[str, str]] | None = None,
    control_module_urls: dict[str, str] | None = None,
) -> str:
    """Return a direct, wrapper-free GenomeSpy embed for a prose page."""
    token = sha256(f"{target}:{identity}".encode()).hexdigest()[:12]
    container_id = f"gs-tutorial-{token}"
    controls_script = ""
    if controls:
        definitions = control_definitions or {}
        module_urls = control_module_urls or {}
        controls_script = (
            "if (c && api) {\n"
            "  try {\n"
            f"    const controlNames = {json.dumps(controls)};\n"
            f"    const controlDefinitions = {json.dumps(definitions)};\n"
            f"    const moduleUrls = {json.dumps(module_urls)};\n"
            "    const controlsModule = await import(moduleUrls.core);\n"
            "    const modules = { core: controlsModule };\n"
            "    const mounted = [];\n"
            "    for (const name of controlNames) {\n"
            "      const definition = controlDefinitions[name];\n"
            "      if (!modules[definition.module]) {\n"
            "        modules[definition.module] = await import(moduleUrls[definition.module]);\n"
            "      }\n"
            "      mounted.push(modules[definition.module][definition.export]());\n"
            "    }\n"
            "    controlsModule.attachControls(c, api, { controls: mounted });\n"
            "  } catch (error) {\n"
            "    console.error('GenomeSpy controls failed to load', error);\n"
            "  }\n"
            "}\n"
        )
    return (
        f'<div id="{container_id}" class="gs-doc-embed" '
        f'style="height:{height}px" role="img" '
        f'aria-label="{html.escape(title)}"></div>\n'
        '<script type="module">\n'
        f"import {{ embed }} from {json.dumps(bundle_url)};\n"
        f"const c = document.getElementById({json.dumps(container_id)});\n"
        f"const spec = {json.dumps(spec, separators=(',', ':'))};\n"
        "const api = c ? await embed(c, spec, { bare: true }) : null;\n"
        f"{controls_script}"
        "</script>"
    )


def _source_without_gallery_meta(source: str) -> str:
    """Remove the internal gallery layout metadata from displayed source."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    lines = source.splitlines(keepends=True)
    meta_spans = [
        (node.lineno - 1, node.end_lineno)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "META"
            for target in node.targets
        )
        and node.end_lineno is not None
    ]
    for start, end in reversed(meta_spans):
        del lines[start:end]
    return "".join(lines).lstrip()


def _detail_md(example: core.Example, bundle_url: str) -> str:
    spec_token = core.build_token([example])
    spec_url = f"../_static/specs/{example.name}.json?v={spec_token}"
    host_id = f"gs-embed-{example.name}"
    spec_toggle_id = f"gs-spec-toggle-{example.name}"
    spec_wrapper_id = f"gs-spec-wrapper-{example.name}"
    spec_output_id = f"gs-spec-output-{example.name}"
    spec_copy_id = f"gs-spec-copy-{example.name}"
    spec_copy_message_id = f"gs-spec-copy-message-{example.name}"
    host_style = f"height:{example.height}px"
    if example.max_width is not None:
        host_style += f";max-width:{example.max_width}px"
    chart = (
        f'<div id="{host_id}" class="gs-doc-embed" style="{host_style}" '
        f'role="img" aria-label="{html.escape(example.title)}"></div>\n'
    )
    specification_controls = (
        '<div class="gs-embed-actions">\n'
        f'<button id="{spec_toggle_id}" class="gs-embed-action" type="button" '
        f'aria-controls="{spec_wrapper_id}" aria-expanded="false">'
        "Show specification</button>\n"
        "</div>\n"
        f'<div id="{spec_wrapper_id}" class="gs-embed-spec-wrapper" hidden>\n'
        f'<button id="{spec_copy_id}" class="gs-embed-copy" type="button" '
        'aria-label="Copy specification" title="Copy specification">'
        '<svg aria-hidden="true" viewBox="0 0 24 24">'
        '<path d="M8 7V5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/>'
        '<rect x="3" y="8" width="13" height="13" rx="2"/>'
        "</svg></button>\n"
        f'<span id="{spec_copy_message_id}" class="gs-embed-copy-message" '
        'role="status" aria-live="polite"></span>\n'
        f'<pre class="gs-embed-spec"><code id="{spec_output_id}"></code></pre>\n'
        "</div>\n"
        '<script type="module">\n'
        f"import {{ embed }} from '{bundle_url}';\n"
        f"const c = document.getElementById('{host_id}');\n"
        f"const spec = '{spec_url}';\n"
        f"const specToggle = document.getElementById('{spec_toggle_id}');\n"
        f"const specWrapper = document.getElementById('{spec_wrapper_id}');\n"
        f"const specOutput = document.getElementById('{spec_output_id}');\n"
        f"const specCopy = document.getElementById('{spec_copy_id}');\n"
        f"const specCopyMessage = document.getElementById('{spec_copy_message_id}');\n"
        "let loadedSpec;\n"
        "const loadSpec = async () => {\n"
        "  if (!loadedSpec) {\n"
        "    loadedSpec = fetch(spec).then((response) => {\n"
        "      if (!response.ok) throw new Error(`HTTP ${response.status}`);\n"
        "      return response.json();\n"
        "    });\n"
        "  }\n"
        "  return loadedSpec;\n"
        "};\n"
        "const copyText = async (text) => {\n"
        "  if (navigator.clipboard && window.isSecureContext) {\n"
        "    try {\n"
        "      await navigator.clipboard.writeText(text);\n"
        "      return;\n"
        "    } catch {}\n"
        "  }\n"
        "  const textarea = document.createElement('textarea');\n"
        "  textarea.value = text;\n"
        "  textarea.setAttribute('readonly', '');\n"
        "  textarea.style.cssText = 'position:fixed;opacity:0';\n"
        "  document.body.appendChild(textarea);\n"
        "  textarea.select();\n"
        "  const copied = document.execCommand('copy');\n"
        "  textarea.remove();\n"
        "  if (!copied) throw new Error('Clipboard access was denied');\n"
        "};\n"
        "if (specCopy) {\n"
        "  specCopy.addEventListener('click', async () => {\n"
        "    try {\n"
        "      const text = JSON.stringify(await loadSpec(), null, 2);\n"
        "      await copyText(text);\n"
        "      specCopy.dataset.copied = 'true';\n"
        "      specCopy.setAttribute('aria-label', 'Specification copied');\n"
        "      specCopy.title = 'Copied';\n"
        "      if (specCopyMessage) specCopyMessage.textContent = 'Copied to clipboard';\n"
        "      window.setTimeout(() => {\n"
        "        delete specCopy.dataset.copied;\n"
        "        specCopy.setAttribute('aria-label', 'Copy specification');\n"
        "        specCopy.title = 'Copy specification';\n"
        "        if (specCopyMessage) specCopyMessage.textContent = '';\n"
        "      }, 1600);\n"
        "    } catch (error) {\n"
        "      specCopy.setAttribute('aria-label', `Unable to copy specification: ${error}`);\n"
        "      specCopy.title = 'Unable to copy specification';\n"
        "      if (specCopyMessage) specCopyMessage.textContent = 'Unable to copy';\n"
        "    }\n"
        "  });\n"
        "}\n"
        "if (specToggle && specWrapper && specOutput) {\n"
        "  specToggle.addEventListener('click', async () => {\n"
        "    const show = specWrapper.hidden;\n"
        "    specWrapper.hidden = !show;\n"
        "    specToggle.textContent = show ? 'Hide specification' : "
        "'Show specification';\n"
        "    specToggle.setAttribute('aria-expanded', String(show));\n"
        "    if (show && !specOutput.dataset.loaded) {\n"
        "      specOutput.textContent = 'Loading specification…';\n"
        "      try {\n"
        "        specOutput.textContent = JSON.stringify(await loadSpec(), null, 2);\n"
        "        specOutput.dataset.loaded = 'true';\n"
        "      } catch (error) {\n"
        "        specOutput.textContent = `Unable to load specification: ${error}`;\n"
        "      }\n"
        "    }\n"
        "  });\n"
        "}\n"
        "if (c) await embed(c, spec, { bare: true });\n"
        "</script>"
    )
    parts = [
        f"# {example.title}",
        "",
        example.description or "",
        "",
        "```{raw} html",
        chart,
        "```",
        "",
    ]
    if example.prose:
        parts += [example.prose, ""]
    parts += [
        "## Code",
        "",
        "```python",
        _source_without_gallery_meta(example.source).rstrip(),
        "```",
        "",
        "```{raw} html",
        specification_controls,
        "```",
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

    examples: list[core.Example] = []
    referenced_arrow_assets: set[str] = set()
    bundle_url = core.default_bundle_url()

    for example, buffers in core.iter_prepared_examples():
        referenced_arrow_assets.update(_write_arrow_assets(buffers))
        example = replace(
            example,
            spec=_rewrite_arrow_urls(example.spec, set(buffers)),
        )
        examples.append(example)
        _write(
            core.SPECS_DIR / f"{example.name}.json",
            json.dumps(example.spec, indent=2),
        )
        _write(
            core.GALLERY_PAGES_DIR / f"{example.name}.md",
            _detail_md(example, bundle_url),
        )

    _write(core.GALLERY_PAGES_DIR / "index.md", _gallery_index_md(examples))
    _remove_stale_arrow_assets(referenced_arrow_assets)
    if hasattr(app, "env"):
        app.env.genomespy_examples = examples  # type: ignore[attr-defined]


def _generate_on_config(app: Any, _config: Any) -> None:
    _generate(app)


def _refresh_landing_page(_app: Any, env: Any, docnames: list[str]) -> None:
    """Re-read the mini-gallery directive after the example inventory changes."""
    env.genomespy_examples = core.collect_examples()
    if "index" in env.found_docs and "index" not in docnames:
        docnames.append("index")


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


class GenomeSpyChart(Directive):
    """Render a named chart from ``docs/tutorials`` in a prose page."""

    required_arguments = 1
    has_content = False
    option_spec = {
        "height": directives.nonnegative_int,
        "title": directives.unchanged_required,
        "controls": directives.unchanged_required,
    }

    def run(self) -> list[nodes.Node]:
        target = self.arguments[0]
        try:
            chart = _load_tutorial_chart(target)
            spec = chart.to_dict()
        except Exception as exc:
            raise self.error(
                f"Cannot render GenomeSpy chart {target!r}: {exc}"
            ) from exc

        env = self.state.document.settings.env
        identity = f"{env.docname}:{self.lineno}"
        controls: tuple[str, ...] = ()
        if value := self.options.get("controls"):
            from genome_spy._embed import normalize_controls

            controls = normalize_controls(
                tuple(name.strip() for name in value.split(",") if name.strip())
            )
        control_definitions, control_module_urls = core.default_control_config()
        markup = _tutorial_embed_html(
            target,
            spec,
            bundle_url=core.default_bundle_url(),
            height=self.options.get("height", 280),
            title=self.options.get("title", target),
            identity=identity,
            controls=controls,
            control_definitions=control_definitions,
            control_module_urls=control_module_urls,
        )
        return [nodes.raw("", markup, format="html")]


def setup(app: Any) -> dict[str, Any]:
    app.connect("config-inited", _generate_on_config)
    app.connect("env-before-read-docs", _refresh_landing_page)
    app.add_directive("genomespy-minigallery", GenomeSpyMiniGallery)
    app.add_directive("genomespy-chart", GenomeSpyChart)
    return {"parallel_read_safe": False, "parallel_write_safe": True}
