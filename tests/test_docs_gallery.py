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


def test_luad_oncoprint_uses_sample_index_scale_and_categorical_genes() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "luad_oncoprint.py")

    assert example.spec["viewportHeight"] == "container"
    assert example.height == 920
    center_column = example.spec["hconcat"][0]
    sample_tracks = center_column["vconcat"][0]
    matrix_panel = sample_tracks["vconcat"][4]
    matrix_layers = matrix_panel["layer"]
    assert matrix_panel["scales"]["y"]["domain"]
    assert matrix_panel["scales"]["y"]["reverse"] is True
    assert "params" not in matrix_panel
    assert "params" not in center_column
    assert sample_tracks["params"] == [
        {
            "name": "sampleRuler",
            "persist": False,
            "ruler": {"encodings": ["x"], "mark": {"opacity": 0.3}},
        }
    ]
    assert example.spec["width"] == "container"
    assert center_column["width"] == "container"
    assert sample_tracks["width"] == "container"
    assert all(panel["width"] == "container" for panel in sample_tracks["vconcat"])

    assert center_column["resolve"]["scale"]["x"] == "shared"
    assert center_column["resolve"]["scale"]["y"] == "independent"
    assert center_column["resolve"]["axis"]["y"] == "independent"
    assert sample_tracks["resolve"]["scale"]["x"] == "shared"
    assert sample_tracks["resolve"]["scale"]["y"] == "independent"
    assert sample_tracks["resolve"]["axis"]["y"] == "independent"
    assert example.spec["resolve"]["scale"] == {
        "x": "independent",
        "y": "independent",
    }
    for layer in matrix_layers:
        assert layer["encoding"]["y"]["field"] == "gene"
        assert layer["encoding"]["y"]["type"] == "nominal"
        assert "axis" not in layer["encoding"]["y"]
    assert matrix_layers[1]["encoding"]["color"]["legend"] is None
    assert center_column["scales"]["x"] == {
        "domain": [-0.5, 342.5],
        "paddingInner": 0,
        "paddingOuter": 0,
        "zoom": True,
    }
    assert sample_tracks["vconcat"][0]["encoding"]["y"]["title"] is None
    spectrum = sample_tracks["vconcat"][1]
    assert spectrum["encoding"]["y"]["title"] is None
    assert spectrum["encoding"]["y"]["scale"]["domain"] == [0, 1]
    assert sample_tracks["vconcat"][2]["encoding"]["y"]["title"] is None
    assert [panel["title"] for panel in sample_tracks["vconcat"][:4]] == [
        {"text": "TMB", "style": "track-title"},
        {"text": "Mutation spectrum", "style": "track-title"},
        {"text": "MSI", "style": "track-title"},
        {"text": "AJCC Stage", "style": "track-title"},
    ]
    sample_layers = [
        *sample_tracks["vconcat"][:4],
        *matrix_layers,
        *sample_tracks["vconcat"][5:],
    ]
    for layer in sample_layers:
        assert layer["encoding"]["x"]["field"] == "sample_order"
        assert layer["encoding"]["x"]["type"] == "index"
        assert layer["encoding"]["x"]["axis"] is None
        assert "x2" not in layer["encoding"]
    sample_labels = center_column["vconcat"][1]
    assert sample_labels["mark"]["type"] == "text"
    assert sample_labels["mark"]["angle"] == 90
    assert sample_labels["mark"]["align"] == "center"
    assert sample_labels["mark"]["baseline"] == "top"
    assert sample_labels["height"] == 80
    assert sample_labels["encoding"]["x"] == {
        "field": "sample_order",
        "type": "index",
        "band": 0,
        "axis": None,
        "title": None,
    }
    assert sample_labels["encoding"]["x2"] == {
        "field": "sample_order",
        "band": 1,
    }
    assert sample_labels["encoding"]["text"] == {
        "field": "sample",
        "type": "nominal",
    }
    for layer in [*matrix_layers[:2], *matrix_layers[3:]]:
        assert "y2" not in layer["encoding"]
    assert len(matrix_layers) == 4
    assert matrix_layers[2]["mark"] == "rect"
    assert matrix_layers[2]["encoding"]["y"]["band"] == 0.5
    assert "y2" not in matrix_layers[2]["encoding"]
    for panel in sample_tracks["vconcat"][:2]:
        expected_transform = {
            "type": "stack",
            "groupby": ["sample_order"],
            "as": ["_y0", "_y1"],
            "field": "count",
        }
        if panel is spectrum:
            expected_transform["offset"] = "normalize"
        assert panel["transform"][0] == expected_transform
    percent_panel = example.spec["hconcat"][1]["vconcat"][4]["hconcat"][0]
    assert percent_panel["encoding"]["x"] == {"value": 1}
    assert percent_panel["mark"]["clip"] == "never"
    assert percent_panel["encoding"]["y"]["scale"]["reverse"] is True
    count_layers = example.spec["hconcat"][1]["vconcat"][4]["hconcat"][1]["layer"]
    assert all(
        layer["encoding"]["y"]["scale"]["reverse"] is True for layer in count_layers
    )
    assert all(panel["data"]["values"] for panel in sample_tracks["vconcat"][5:])
    assert len(sample_tracks["vconcat"]) == 8
    assert len(center_column["vconcat"]) == 2


def test_laml_oncoprint_uses_shared_sample_index_scale() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "oncoprint.py")

    assert example.height == 660
    assert example.max_width == 760
    left_column = example.spec["hconcat"][0]
    assert all(panel["width"] == 400 for panel in left_column["vconcat"])
    sample_layers = [left_column["vconcat"][0], *left_column["vconcat"][1]["layer"]]
    assert left_column["vconcat"][1]["scales"]["y"]["domain"] == [
        "FLT3",
        "DNMT3A",
        "NPM1",
        "IDH2",
        "IDH1",
        "TET2",
        "RUNX1",
        "NRAS",
        "TP53",
        "CEBPA",
    ]
    assert left_column["vconcat"][1]["scales"]["y"]["reverse"] is True
    assert "params" not in left_column["vconcat"][1]
    assert left_column["params"] == [
        {
            "name": "sampleRuler",
            "persist": False,
            "ruler": {"encodings": ["x"], "mark": {"opacity": 0.3}},
        }
    ]

    assert left_column["resolve"]["scale"]["x"] == "shared"
    assert left_column["resolve"]["scale"]["y"] == "independent"
    assert left_column["resolve"]["axis"]["y"] == "independent"
    assert left_column["scales"]["x"] == {
        "domain": [-0.5, 192.5],
        "paddingInner": 0,
        "paddingOuter": 0,
        "zoom": True,
    }
    for layer in sample_layers:
        assert layer["encoding"]["x"]["field"] == "sample_order"
        assert layer["encoding"]["x"]["type"] == "index"
        assert "x2" not in layer["encoding"]
    assert left_column["vconcat"][0]["transform"][0] == {
        "type": "stack",
        "groupby": ["sample_order"],
        "as": ["_y0", "_y1"],
        "field": "count",
    }
    count_bars = example.spec["hconcat"][2]["vconcat"][1]["layer"][1]
    assert count_bars["transform"][0] == {
        "type": "stack",
        "groupby": ["gene"],
        "as": ["_x0", "_x1"],
        "field": "count",
    }
    percent_panel = example.spec["hconcat"][1]["vconcat"][1]
    assert percent_panel["encoding"]["x"] == {"value": 1}
    assert percent_panel["encoding"]["y"]["scale"]["reverse"] is True
    assert all(
        layer["encoding"]["y"]["scale"]["reverse"] is True
        for layer in example.spec["hconcat"][2]["vconcat"][1]["layer"]
    )
    assert [row["label"] for row in percent_panel["data"]["values"]] == [
        "27%",
        "25%",
        "17%",
        "10%",
        "9%",
        "9%",
        "8%",
        "8%",
        "8%",
        "7%",
    ]
    count_title = example.spec["hconcat"][2]["vconcat"][0]
    assert count_title["encoding"]["x"] == {"value": 0.5}


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


def test_dynseq_uses_fasta_coordinate_lookup_and_sequence_logos() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "dynseq_bqtl.py")

    assert example.spec["data"]["lazy"]["type"] == "indexedFasta"
    assert example.spec["vconcat"] == [
        {
            "params": {"allele": "ref"},
            "import": {"template": "allele-track"},
        },
        {
            "params": {"allele": "alt"},
            "import": {"template": "allele-track"},
        },
    ]

    template = example.spec["templates"]["allele-track"]
    assert template["transform"][0]["type"] == "coordinateLookup"
    assert template["transform"][0]["from"]["data"]["lazy"]["type"] == "bigwig"
    assert template["transform"][0]["key"] == ["chrom", "pos"]
    assert template["transform"][0]["values"] == ["score"]

    logo = template["layer"][1]
    assert logo["mark"]["type"] == "text"
    assert logo["mark"]["logoLetters"] is True
    assert logo["mark"]["fitToBand"] is True
    assert logo["encoding"]["text"]["field"] == "base"
    assert logo["encoding"]["y2"]["field"] == "score"
    assert logo["encoding"]["tooltip"] == [
        {"field": "base", "type": "nominal"},
        {"field": "score", "type": "quantitative"},
    ]


def test_gistic_includes_scores_thresholds_and_lesion_regions() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "tcga_ov_gistic.py")

    assert example.spec["assembly"] == "hg19"
    assert len(example.spec["vconcat"]) == 2

    score_track, lesion_track = example.spec["vconcat"]
    assert [layer["name"] for layer in score_track["layer"]] == [
        "zero-line",
        "q-value-rects",
        "q-value-thresholds",
    ]
    assert lesion_track["name"] == "gistic-all-lesions"
    assert [transform["type"] for transform in lesion_track["transform"]] == [
        "regexExtract",
        "filter",
        "regexFold",
        "regexExtract",
        "project",
    ]
    assert lesion_track["encoding"]["opacity"]["field"] == "Segment type"
    assert lesion_track["encoding"]["size"]["field"] == "Segment type"


def test_bam_example_uses_full_alignment_dataflow() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "bam_read_alignments.py")

    assert example.spec["assembly"] == "hg38"
    assert example.spec["data"]["lazy"]["type"] == "bam"
    assert example.spec["data"]["lazy"]["windowSize"] == {"expr": "windowSize"}
    assert [param["name"] for param in example.spec["params"]] == [
        "minMapq",
        "minBaseQuality",
        "windowSize",
    ]
    assert [panel["name"] for panel in example.spec["vconcat"]] == [
        "coverage",
        "read-alignments",
    ]
    assert [layer["name"] for layer in example.spec["vconcat"][0]["layer"]] == [
        "depth",
        "mismatch-summary",
        "insertion-summary",
    ]
    read_spec = example.spec["vconcat"][1]
    assert read_spec["viewportHeight"] == "container"
    assert read_spec["layer"][0]["layer"][0]["mark"]["type"] == "arrow"
    assert [transform["type"] for transform in example.spec["transform"]] == [
        "filter",
        "formula",
        "pileup",
    ]
    assert "flattenCigar" in str(example.spec)
    assert "alignmentMismatches" in str(example.spec)


def test_stacked_genome_browser_uses_shared_hg38_locus() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "stacked_genome_browser.py")

    assert example.spec["assembly"] == "hg38"
    assert example.spec["scales"]["x"]["domain"] == [
        {"chrom": "chr7", "pos": 55100000},
        {"chrom": "chr7", "pos": 55120000},
    ]
    assert example.spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }
    assert example.spec["axes"] == {
        "x": {"orient": "bottom", "title": "Genomic position"}
    }
    assert len(example.spec["vconcat"]) == 5

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


def test_ascat_segmentation_has_three_aligned_tracks() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "ascat_copy_number.py").spec

    assert spec["assembly"] == "hg18"
    assert spec["resolve"]["axis"]["x"] == "shared"
    assert [track["name"] for track in spec["vconcat"]] == [
        "copyNumberTrack",
        "logRTrack",
        "bafTrack",
    ]
    assert spec["encoding"]["x"] == {
        "chrom": "chr",
        "pos": "startpos",
        "type": "locus",
        "scale": {"type": "locus"},
    }
    assert spec["encoding"]["x2"]["offset"] == 1


def test_ascat_fitting_uses_cross_grid_and_linked_fit_parameters() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "ascat_fitting.py").spec

    assert spec["assembly"] == "hg19"
    assert [param["name"] for param in spec["params"]] == [
        "minLength",
        "selectedFit",
        "sample",
        "gamma",
        "downweightBalanced",
        "fitBothAlleles",
    ]
    sunrise = spec["vconcat"][0]
    assert [transform["type"] for transform in sunrise["transform"][:2]] == [
        "cross",
        "cross",
    ]
    assert sunrise["params"][0]["push"] == "outer"
    assert sunrise["params"][0]["ruler"]["encodings"] == ["x", "y"]
    assert len(spec["datasets"]["ascat-solutions"]) == 9
    assert [transform["type"] for transform in spec["transform"]][-1] == ("identifier")


def test_six_frame_translation_uses_lookup_windows_and_strand_template() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "six_frame_translation.py").spec

    assert spec["assembly"] == "hg38"
    assert len(spec["datasets"]["geneticCode"]) == 64
    translation = spec["vconcat"][1]
    assert [transform["type"] for transform in translation["transform"]] == [
        "formula",
        "lookup",
        "window",
        "filter",
        "formula",
    ]
    assert translation["transform"][2]["ops"] == ["lead"] * 4
    assert [view["params"]["strand"] for view in translation["layer"]] == [
        "forward",
        "reverse",
    ]
    assert "amino-acid-translation" in translation["templates"]


def test_hcc1954_uses_vcf_self_lookup_and_copy_number_track() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "hcc1954_sv_cnv.py").spec

    assert spec["assembly"] == "hg38"
    assert [track["name"] for track in spec["vconcat"]] == [
        "sv-link-layers",
        "copy-numbers",
    ]
    sv_track = spec["vconcat"][0]
    assert sv_track["data"]["format"]["type"] == "vcf"
    lookup = next(
        transform
        for transform in sv_track["transform"]
        if transform["type"] == "lookup"
    )
    assert lookup["from"] == {"source": "input"}
    assert lookup["as"] == ["mateChrom", "matePos", "mateOrder"]
    assert sv_track["layer"][0]["transform"][0]["type"] == "regexFold"
    assert spec["vconcat"][1]["encoding"]["color"]["field"] == ("relative_copy_ratio")


def test_refseq_example_preserves_nested_semantic_zoom_layers() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "refseq_scored_genes.py").spec

    assert [layer["name"] for layer in spec["layer"]] == [
        "transcripts",
        "symbols",
    ]
    assert spec["layer"][0]["opacity"]["unitsPerPixel"] == [100000, 40000]
    assert [transform["type"] for transform in spec["layer"][1]["transform"]] == [
        "measureText",
        "filterScoredLabels",
    ]
    arrows = spec["layer"][1]["layer"][1]
    assert arrows["encoding"]["dx"]["scale"] is None


def test_composed_genome_browser_imports_four_release_pinned_tracks() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "composing_genome_browser.py").spec

    assert spec["assembly"] == "hg38"
    assert spec["scales"]["x"]["domain"] == [
        {"chrom": "chr20", "pos": 10006452},
        {"chrom": "chr20", "pos": 10006533},
    ]
    assert spec["axes"]["x"] == {"orient": "top", "title": None}
    assert spec["resolve"]["axis"]["x"] == "shared"
    urls = [view["import"]["url"] for view in spec["vconcat"]]
    assert all("/d2e9bd71/" in url for url in urls)
    assert [url.rsplit("/", 1)[-1] for url in urls] == [
        "cytobands.json",
        "indexed-fasta-six-frame-translation.json",
        "bam-read-alignments.json",
        "scored-refSeq-genes.json",
    ]


def test_upset_plot_derives_and_aligns_exact_set_intersections() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "upset_mutations.py")
    spec = example.spec

    assert example.category == "Set intersections"
    assert [transform["type"] for transform in spec["transform"]] == [
        "regexFold",
        "setIntersection",
        "filter",
        "formula",
        "window",
        "collect",
        "formula",
        "window",
        "window",
    ]
    assert spec["transform"][1] == {
        "type": "setIntersection",
        "element": "Identifier",
        "set": "set",
        "membership": "membership",
    }
    assert [view["name"] for view in spec["concat"]] == [
        "empty-space",
        "intersection-sizes",
        "set-sizes",
        "combination-matrix",
    ]
    assert spec["columns"] == 2
    assert spec["scales"]["x"]["domain"] == [0.5, 20.5]
    assert spec["scales"]["y"]["domain"] == [-0.5, 4.5]
    assert spec["concat"][1]["scales"]["y"] == {
        "zero": True,
        "nice": True,
        "padding": 0.12,
        "domainMin": 0,
    }


def test_multiple_sequence_alignment_configures_shared_x_scale_once() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "multiple_sequence_alignment.py").spec

    assert spec["scales"]["x"] == {
        "domain": [190, 230],
        "zoom": {"extent": "data"},
    }
    assert spec["transform"] == [{"type": "flattenSequence"}]
    assert "scale" not in spec["vconcat"][0]["encoding"]["x"]
    assert "scale" not in spec["vconcat"][1]["encoding"]["x"]
    assert spec["vconcat"][0]["encoding"]["x"]["type"] == "index"
    assert spec["vconcat"][1]["encoding"]["x"]["type"] == "index"
    expected_base_color = {
        "field": "sequence",
        "type": "nominal",
        "scale": {
            "domain": ["A", "C", "T", "G", "N", "-"],
            "range": [
                "#4FBF45",
                "#4D96E8",
                "#E85F78",
                "#E8B322",
                "#BDBDBD",
                "#f5f5f5",
            ],
        },
        "legend": None,
    }
    assert spec["vconcat"][1]["encoding"]["color"] == expected_base_color
    assert spec["vconcat"][1]["layer"][1]["encoding"]["color"] == {"value": "black"}


def test_cytobands_suppresses_legends_to_preserve_the_ideogram() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "cytobands.py").spec

    assert all(
        layer["encoding"]["color"]["legend"] is None for layer in spec["layer"][:2]
    )


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
    assert f"manhattan_plot.png?v={build_token}" in markdown
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


def test_gallery_generation_removes_stale_build_outputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    extension = _load_gallery_extension()
    pages = tmp_path / "gallery-pages"
    specs = tmp_path / "specs"
    outdir = tmp_path / "html"
    doctreedir = tmp_path / "doctrees"
    stale_paths = [
        pages / "obsolete.md",
        specs / "obsolete.json",
        outdir / "gallery" / "obsolete.html",
        outdir / "_sources" / "gallery" / "obsolete.md.txt",
        outdir / "_static" / "specs" / "obsolete.json",
        outdir / "_static" / "gallery" / "obsolete.png",
        outdir / "_downloads" / "hash" / "obsolete.json",
        doctreedir / "gallery" / "obsolete.doctree",
    ]
    for path in stale_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("stale", encoding="utf-8")

    monkeypatch.setattr(extension.core, "GALLERY_PAGES_DIR", pages)
    monkeypatch.setattr(extension.core, "SPECS_DIR", specs)
    monkeypatch.setattr(extension.core, "collect_examples", lambda: [])
    app = type(
        "App",
        (),
        {
            "outdir": outdir,
            "doctreedir": doctreedir,
            "env": type("Env", (), {})(),
        },
    )()

    extension._generate(app)

    assert all(not path.exists() for path in stale_paths)


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
    assert f"_static/gallery/manhattan_plot.png?v={expected}" in nodes[0].astext()


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
