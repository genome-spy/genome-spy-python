"""Agent publication is plain Markdown, indexed, and executable."""

from pathlib import Path
import json
import re
import shutil
import inspect
from urllib.parse import urlsplit

import pytest

from tools.agent_docs import publish_agent_docs

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://genomespy.app/genome-spy-python/"
pytestmark = pytest.mark.docs


def test_all_indexed_pages_and_links_exist_with_correct_subpath(tmp_path: Path) -> None:
    outputs = publish_agent_docs(ROOT, tmp_path, BASE)
    index = (tmp_path / "llms.txt").read_text()
    urls = re.findall(r"\]\(([^)]+)\)", index)
    guides = list((ROOT / "docs/user-guide").rglob("*.md"))
    examples = list((ROOT / "docs/examples").glob("*.py"))
    assert len(urls) == 14 + len(guides) + len(examples)
    assert len(outputs) == len(urls) + 1
    assert "> Build:" not in index
    for url in urls:
        assert url.startswith(BASE)
        page = tmp_path / url.removeprefix(BASE)
        text = page.read_text()
        assert "> Build:" not in text
        assert "```{" not in text
        for href in re.findall(r"\]\(([^)]+)\)", text):
            if href.startswith(BASE) and urlsplit(href).path.endswith(".md"):
                assert (
                    tmp_path / urlsplit(href).path.removeprefix("/genome-spy-python/")
                ).is_file()
    api = (tmp_path / "agents/api-output.md").read_text()
    import genome_spy as gs

    assert f"Chart.save{inspect.signature(gs.Chart.save)}" in api
    assert "Chart.mark_point" in (tmp_path / "agents/api-chart.md").read_text()
    assert "focused subset" in api
    skill = (tmp_path / "agents/skill.md").read_text()
    assert BASE + "agents/grouped-charts.md" in skill
    assert "references/grouped-charts.md)" not in skill


def test_canonical_reference_edits_flow_into_published_pages(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    shutil.copy(ROOT / "pyproject.toml", root)
    (root / "docs/agents").mkdir(parents=True)
    source = root / "instructions.md"
    source.write_text("# Instructions\n\nFirst revision.\n")
    manifest = [
        {
            "path": "instructions.md",
            "source": "instructions.md",
            "title": "Instructions",
            "section": "Guidance",
            "description": "Read these.",
        }
    ]
    (root / "docs/agents/manifest.json").write_text(json.dumps(manifest))
    out = tmp_path / "out"
    publish_agent_docs(root, out, BASE)
    source.write_text("# Instructions\n\nChanged at canonical source.\n")
    publish_agent_docs(root, out, BASE)
    assert (
        "Changed at canonical source." in (out / "agents/instructions.md").read_text()
    )
    source.write_text("# Instructions\n\n[Missing](missing.md)\n")
    with pytest.raises(ValueError, match="Unpublished local link"):
        publish_agent_docs(root, out, BASE)
    assert (
        "Changed at canonical source." in (out / "agents/instructions.md").read_text()
    )


@pytest.mark.parametrize(
    "relative_path",
    [
        "docs/agents/quickstart.md",
        "docs/agents/data.md",
        "docs/agents/encodings.md",
        "docs/agents/scales-axes-legends.md",
        "docs/agents/rendering.md",
        "skills/create-genomespy-visualization/references/table-chart.md",
        "skills/create-genomespy-visualization/references/grouped-charts.md",
    ],
)
def test_authored_python_examples_execute_and_validate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, relative_path: str
) -> None:
    import genome_spy as gs

    monkeypatch.chdir(tmp_path)
    (tmp_path / "measurements.csv").write_text(
        "id,depth,score,group\na,2,0.5,control\n"
    )
    text = (ROOT / relative_path).read_text()
    namespace = {"__name__": "__agent_example__"}
    blocks = list(re.finditer(r"```python\n(.*?)```", text, re.DOTALL))
    assert blocks
    previous_end = 0
    authored_chart = False
    for block in blocks:
        introduction = text[previous_end : block.start()]
        if not re.search(r"\bContinues\b", introduction):
            namespace = {"__name__": "__agent_example__"}
        exec(compile(block[1], relative_path, "exec"), namespace)
        charts = [
            value for value in namespace.values() if isinstance(value, gs.TopLevelSpec)
        ]
        for chart in charts:
            chart.to_dict()
        authored_chart |= bool(charts)
        previous_end = block.end()
    assert authored_chart, f"No chart was authored by {relative_path}"
    if relative_path == "docs/agents/rendering.md":
        assert (tmp_path / "chart.html").is_file()


def test_sphinx_html_build_includes_plain_agent_outputs(tmp_path: Path) -> None:
    from sphinx.application import Sphinx
    import io

    source = tmp_path / "source"
    source.mkdir()
    (source / "index.rst").write_text(
        "Agent publication test\n======================\n"
    )
    (source / "conf.py").write_text(
        f"import sys\nsys.path.insert(0, {str(ROOT / 'docs/_ext')!r})\n"
        f"extensions = ['genomespy_agents']\nhtml_baseurl = {BASE!r}\n"
    )
    output = tmp_path / "html"
    warnings = io.StringIO()
    app = Sphinx(
        str(source),
        str(source),
        str(output),
        str(tmp_path / "doctrees"),
        "html",
        status=io.StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    app.build()
    assert app.statuscode == 0, warnings.getvalue()
    assert (output / "index.html").is_file()
    assert (output / "llms.txt").is_file()
    assert (output / "agents/api-output.md").read_text().startswith("# Python API")
    assert not (output / "agents/api-output.html").exists()


def test_sphinx_hook_skips_failed_and_non_html_builds(tmp_path: Path) -> None:
    from docs._ext.genomespy_agents import _publish
    from types import SimpleNamespace

    app = SimpleNamespace(
        builder=SimpleNamespace(format="html"),
        outdir=str(tmp_path),
        config=SimpleNamespace(html_baseurl=BASE),
    )
    _publish(app, RuntimeError("Build failed"))
    assert not (tmp_path / "llms.txt").exists()
    app.builder.format = "latex"
    _publish(app, None)
    assert not (tmp_path / "llms.txt").exists()


def test_gallery_and_guides_reuse_maintained_code_and_categories(
    tmp_path: Path,
) -> None:
    publish_agent_docs(ROOT, tmp_path, BASE)
    index = (tmp_path / "llms.txt").read_text()
    assert "## Gallery: Single-cell expression" in index
    assert "## Gallery: Basic charts and composition" in index
    assert BASE + "user-guide/genomic-data.md" in index
    catalog = (tmp_path / "agents/gallery.md").read_text()
    assert BASE + "gallery/point_mark.md" in catalog
    example = (tmp_path / "gallery/point_mark.md").read_text()
    source = (ROOT / "docs/examples/point_mark.py").read_text()
    assert source.split("META =", 1)[0].strip() in example
    assert "<script" not in example and "gs-doc-embed" not in example
    guide = (tmp_path / "user-guide/data.md").read_text()
    assert "gs.Chart(measurements)" in guide
    assert "literalinclude" not in guide and "{py:class}" not in guide
    assert BASE + "user-guide/notebooks.md" in guide
    workflow = (tmp_path / "user-guide/workflows/pick-genes.md").read_text()
    assert "```python" in workflow and "snapshot" in workflow
    assert "{genomespy-workflow}" not in workflow


def test_tutorial_edits_flow_into_markdown_without_modifying_code(
    tmp_path: Path,
) -> None:
    from tools.agent_markdown import _plain_markdown

    tutorial = tmp_path / "example.py"
    tutorial.write_text('# begin\nchart = "[literal](missing.md)"\n# end\n')
    text = "# Guide\n\n```{literalinclude} example.py\n:language: python\n:start-after: begin\n:end-before: end\n```\n"
    assert 'chart = "[literal](missing.md)"' in _plain_markdown(
        text, tmp_path / "guide.md", tmp_path
    )
    tutorial.write_text('# begin\nchart = "updated"\n# end\n')
    assert 'chart = "updated"' in _plain_markdown(text, tmp_path / "guide.md", tmp_path)
    tutorial.write_text('chart = "missing markers"\n')
    with pytest.raises(ValueError, match="Missing start-after marker"):
        _plain_markdown(text, tmp_path / "guide.md", tmp_path)


def test_fresh_checkout_publishes_examples_without_generated_gallery(
    tmp_path: Path,
) -> None:
    root = tmp_path / "source"
    (root / "docs/agents").mkdir(parents=True)
    (root / "docs/agents/manifest.json").write_text("[]")
    examples = root / "docs/examples"
    examples.mkdir()
    example = examples / "points.py"
    example.write_text(
        '"""Working points.\n\nA small point chart.\n"""\nMETA = {"category": "Basic charts and composition"}\nchart = "original"\n'
    )
    prose = examples / "points.md"
    prose.write_text("Reuse this encoding pattern.\n")
    output = tmp_path / "html"
    publish_agent_docs(root, output, BASE)
    exported = output / "gallery/points.md"
    assert "Reuse this encoding pattern." in exported.read_text()
    assert 'chart = "original"' in exported.read_text()
    assert "META =" not in exported.read_text()
    assert not (root / "docs/gallery").exists()
    example.write_text(example.read_text().replace("original", "improved"))
    prose.write_text("Improved maintained explanation.\n")
    publish_agent_docs(root, output, BASE)
    assert 'chart = "improved"' in exported.read_text()
    assert "Improved maintained explanation." in exported.read_text()
