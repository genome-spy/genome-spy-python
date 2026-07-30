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


def _load_gallery_extension():
    path = REPO_ROOT / "docs" / "_ext" / "genomespy_gallery.py"
    spec = importlib.util.spec_from_file_location("_gs_gallery_ext", path)
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


def test_luad_oncoprint_uses_sample_intervals_and_categorical_genes() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "luad_oncoprint.py")

    assert example.spec["viewportHeight"] == "container"
    center_column = example.spec["hconcat"][0]
    matrix_layers = center_column["vconcat"][4]["layer"]

    assert center_column["resolve"]["scale"]["x"] == "shared"
    assert center_column["resolve"]["scale"]["y"] == "independent"
    assert center_column["resolve"]["axis"]["y"] == "independent"
    assert example.spec["resolve"]["scale"] == {
        "x": "independent",
        "y": "independent",
    }
    for layer in matrix_layers:
        assert layer["encoding"]["y"]["field"] == "gene"
        assert layer["encoding"]["y"]["type"] == "nominal"
        assert "axis" not in layer["encoding"]["y"]
    assert matrix_layers[1]["encoding"]["color"]["legend"] is None
    assert center_column["vconcat"][0]["encoding"]["x"]["scale"]["domain"] == [
        0,
        343,
    ]
    assert center_column["vconcat"][0]["encoding"]["y"]["title"] == "TMB"
    assert center_column["vconcat"][1]["encoding"]["y"]["title"] == (
        "Mutation spectrum"
    )
    assert center_column["vconcat"][2]["encoding"]["y"]["title"] == "MSI"
    for layer in matrix_layers[:3]:
        assert layer["encoding"]["x"]["field"] == "x0"
        assert layer["encoding"]["x2"]["field"] == "x1"
        assert "y2" not in layer["encoding"]
    assert all(panel["data"]["values"] for panel in center_column["vconcat"][5:])
    assert len(center_column["vconcat"]) == 8


def test_gallery_data_preview_is_rendered_for_opt_in_example() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "luad_oncoprint.py")

    assert [preview.title for preview in example.previews] == [
        "Samples",
        "Mutation matrix",
    ]
    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert "## Data preview" in markdown
    assert '<figure class="gs-data-preview"><figcaption>Samples' in markdown
    assert "<th>sample</th>" in markdown
    assert "<th>class</th>" in markdown
    assert "<table><thead>" in markdown


def test_sashimi_plot_uses_direct_data_urls() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "sashimi_plot.py")

    bigwig_url = example.spec["layer"][0]["data"]["lazy"]["url"]
    bed_url = example.spec["layer"][1]["data"]["url"]

    assert "//splice_junction" not in bigwig_url
    assert bigwig_url.endswith(".bigWig")
    assert bed_url.endswith(".SJ.out.bed")
    assert "encoding" not in example.spec["layer"][1]


def test_stacked_genome_browser_uses_shared_hg38_locus() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "stacked_genome_browser.py")

    assert example.spec["assembly"] == "hg38"
    assert example.spec["scales"]["x"]["domain"] == [
        {"chrom": "chr7", "pos": 55100000},
        {"chrom": "chr7", "pos": 55120000},
    ]
    assert example.spec["resolve"] == {
        "scale": {"y": "independent"},
        "axis": {"y": "independent"},
    }

    tracks = example.spec["vconcat"]
    assert [track["name"] for track in tracks] == [
        "gc-content",
        "phylop-100way",
        "ccre",
        "sequence",
        "refseq-track",
    ]
    assert [track["data"]["lazy"]["type"] for track in tracks[:4]] == [
        "bigwig",
        "bigwig",
        "bigbed",
        "indexedFasta",
    ]
    assert tracks[3]["data"]["lazy"]["windowSize"] == 30_000
    assert "y" not in tracks[2]["encoding"]
    assert "y" not in tracks[3]["encoding"]
    assert tracks[4]["data"]["url"].endswith("refSeqGenes-hg38-release232.tsv.gz")
    assert tracks[4]["transform"][-1] == {
        "type": "filter",
        "expr": "datum._lane < 3",
    }


def test_manhattan_plot_uses_canonical_hg18_points() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "manhattan_plot.py")

    assert example.spec["assembly"] == "hg18"
    assert "genomes" not in example.spec
    assert "vconcat" not in example.spec
    assert example.spec["height"] == 360
    point_data = example.spec["layer"][2]["data"]["values"]
    assert {row["chrom"] for row in point_data} <= {
        *(f"chr{number}" for number in range(1, 23)),
        "chrX",
    }


def test_gallery_index_keeps_examples_in_visible_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    examples = gallery.collect_examples()
    monkeypatch.setattr(
        extension.core,
        "thumb_filename",
        lambda example: f"{example.name}.png",
    )
    markdown = extension._gallery_index_md(examples)
    build_token = gallery.build_token(examples)

    assert ":hidden:" not in markdown
    assert ":caption: Volcano and MA plots" in markdown
    assert "airway_ma_plot" in markdown
    assert "airway_volcano_plot" in markdown
    assert ":caption: Association plots" in markdown
    assert ":caption: Genome browser tracks" in markdown
    assert f"manhattan_plot.html?v={build_token}" in markdown
    assert "Each card opens the live chart and the Python code that produced it." in (
        markdown
    )
    assert 'class="gs-card__tags"' not in markdown
    for example in examples:
        assert f"\n{example.name}\n" in markdown


def test_gallery_build_token_changes_with_example_content() -> None:
    gallery = _load_gallery()
    examples = gallery.collect_examples()
    original = gallery.build_token(examples)
    mutated = [
        gallery.Example(
            name=example.name,
            title=example.title,
            description=example.description,
            category=example.category,
            tags=example.tags,
            order=example.order,
            height=example.height,
            max_width=example.max_width,
            source=example.source + "\n# cache bust",
            spec=example.spec,
        )
        if example.name == examples[0].name
        else example
        for example in examples
    ]

    assert gallery.build_token(mutated) != original


def test_gallery_requires_png_thumbnails(tmp_path: Path) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "manhattan_plot.py")

    gallery.THUMBS_DIR = tmp_path

    with pytest.raises(FileNotFoundError, match="Missing PNG thumbnail"):
        gallery.thumb_filename(example)


def test_gallery_generation_runs_during_sphinx_config_phase() -> None:
    extension = _load_gallery_extension()
    app = FakeSphinxApp()

    extension.setup(app)
    events = [args[0] for args in app.events]

    assert "config-inited" in events
    assert "builder-inited" not in events


def test_gallery_detail_embed_uses_shadow_dom_and_stable_reveal() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "airway_volcano_plot.py")
    expected = gallery.build_token([example])
    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert 'class="gs-doc-embed"' in markdown
    assert "attachShadow({ mode: 'open' })" in markdown
    assert "import { embed } from 'https://example.test/bundle.js';" in markdown
    assert "await embed(c, spec, { bare: true });" in markdown
    assert f"airway_volcano_plot.json?v={expected}" in markdown
    assert (
        "#shell{position:relative;width:100%;height:100%;overflow:hidden}" in markdown
    )
    assert (
        "#c{position:absolute;inset:0;overflow:hidden;opacity:0;transition:opacity .2s ease}"
        in markdown
    )
    assert "Math.round(r.width)}x${Math.round(r.height)" in markdown
    assert "stable >= 3" in markdown


def test_gallery_example_can_cap_embed_width() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "manhattan_plot.py")
    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert 'class="gs-doc-embed" style="height:500px;max-width:980px"' in markdown


def test_minigallery_links_include_cache_busting_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    examples = gallery.collect_examples()
    expected = gallery.build_token(examples)
    monkeypatch.setattr(
        extension.core,
        "thumb_filename",
        lambda example: f"{example.name}.png",
    )
    directive = extension.GenomeSpyMiniGallery(
        "genomespy-minigallery",
        [],
        {},
        [],
        0,
        0,
        "",
        FakeState(examples),
        FakeStateMachine(),
    )

    nodes = directive.run()

    assert len(nodes) == 1
    assert f"gallery/manhattan_plot.html?v={expected}" in nodes[0].astext()


class FakeSphinxApp:
    def __init__(self) -> None:
        self.events: list[tuple[str, object]] = []
        self.directives: list[tuple[str, object]] = []

    def connect(self, name: str, callback: object) -> None:
        self.events.append((name, callback))

    def add_directive(self, name: str, directive: object) -> None:
        self.directives.append((name, directive))


class FakeState:
    def __init__(self, examples: list[object]) -> None:
        self.document = FakeDocument(examples)


class FakeDocument:
    def __init__(self, examples: list[object]) -> None:
        self.settings = FakeSettings(examples)


class FakeSettings:
    def __init__(self, examples: list[object]) -> None:
        self.env = FakeEnv(examples)


class FakeEnv:
    def __init__(self, examples: list[object]) -> None:
        self.genomespy_examples = examples


class FakeStateMachine:
    def __init__(self) -> None:
        self.reporter = object()
