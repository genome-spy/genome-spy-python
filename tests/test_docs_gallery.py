"""Every documentation gallery example must import and serialize to a valid spec.

Building a chart's dict runs it through the generated schema validation path, so
this test doubles as a schema check for the authored examples.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from hashlib import sha256
from pathlib import Path
from urllib.parse import urljoin

import pytest

pytestmark = pytest.mark.docs

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


def test_gallery_root_pixel_sizes_are_owned_by_the_embedder() -> None:
    gallery = _load_gallery()

    for example in gallery.collect_examples():
        assert not isinstance(example.spec.get("width"), (int, float)), example.name
        assert not isinstance(example.spec.get("height"), (int, float)), example.name


def test_pik3ca_lollipop_uses_reactive_collision_displacement() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "pik3ca_tcga_brca_lollipop.py")

    assert example.spec["datasets"]["mutations"][-1]["mutation"] == "G1049R"
    assert example.spec["scales"]["x"] == {"domainMin": 1, "nice": False}
    mutation_view = example.spec["vconcat"][0]
    assert mutation_view["transform"][1] == {
        "type": "displace1d",
        "pos": "position",
        "length": 18,
        "as": "xDisplacement",
        "positionFactor": {"expr": "pixelsPerResidue"},
        "extent": {
            "expr": "[0.5, proteinLength + 0.5 - 25 / max(1, pixelsPerResidue)]"
        },
    }
    assert mutation_view["encoding"]["xOffset"] == {
        "field": "xDisplacement",
        "type": "quantitative",
        "scale": None,
    }
    assert mutation_view["vconcat"][2]["layer"][1]["encoding"]["xOffset"] == {
        "value": 0
    }
    assert mutation_view["vconcat"][2]["layer"][0]["mark"]["x2Offset"] == 0


def test_dnmt3a_needle_plot_uses_separate_mutation_and_protein_tracks() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "needle_plot.py").spec

    assert len(spec["vconcat"]) == 2
    assert spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }
    mutation_track, protein_track = spec["vconcat"]
    assert set(mutation_track["data"]["values"][0]).isdisjoint(
        {"base", "label_y", "label_text"}
    )
    assert protein_track["layer"][2]["transform"] == [
        {
            "type": "formula",
            "expr": "((datum.start + datum.end) / 2)",
            "as": "center",
        }
    ]


def test_hcc_structural_variant_channels_use_typed_conditions() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "hcc1954_sv_cnv.py")

    links = example.spec["vconcat"][0]["layer"][1]
    assert links["encoding"]["size"]["condition"] == [
        {"empty": False, "param": "svHover", "value": 3}
    ]
    assert links["encoding"]["opacity"] == {
        "condition": [{"empty": False, "param": "svHover", "value": 1}],
        "value": 0.5,
    }
    assert links["encoding"]["tooltip"][0] == {
        "expr": (
            "if((datum.INFO.SVTYPE[0] === 'BND'),"
            "replace(datum.ID[0],regexp('_[12]$'),''),datum.ID[0])"
        ),
        "title": "SV ID",
    }


def test_composed_examples_use_fluent_shared_encodings() -> None:
    gallery = _load_gallery()
    dynseq = gallery.collect_example(EXAMPLES_DIR / "dynseq_bqtl.py")
    refseq = gallery.collect_example(EXAMPLES_DIR / "refseq_scored_genes.py")

    baseline = dynseq.spec["templates"]["allele-track"]["layer"][0]
    assert baseline["encoding"] == {
        "color": {"value": "gray"},
        "y": {"datum": 0, "type": "quantitative"},
    }
    transcripts = refseq.spec["layer"][0]
    assert transcripts["encoding"] == {"color": {"value": "#909090"}}


def test_link_example_encodes_dome_heights() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "link_mark.py")

    assert [row["y"] for row in example.spec["data"]["values"]] == [
        2,
        4,
        6,
        8,
        10,
    ]
    assert example.spec["encoding"]["y"] == {
        "field": "y",
        "type": "quantitative",
        "scale": {"domain": [0, 12]},
        "title": "Height",
    }


def test_sequence_examples_use_typed_sort_and_data_format_helpers() -> None:
    gallery = _load_gallery()
    alignment = gallery.collect_example(EXAMPLES_DIR / "multiple_sequence_alignment.py")
    logo = gallery.collect_example(EXAMPLES_DIR / "sequence_logo.py")

    assert alignment.spec["vconcat"][0]["transform"][2]["sort"] == {
        "field": "count",
        "order": "ascending",
    }
    assert alignment.spec["data"]["format"] == {"type": "fasta"}
    assert logo.spec["transform"][0]["sort"] == {
        "field": "count",
        "order": "ascending",
    }


def test_examples_use_typed_axis_and_view_configuration() -> None:
    gallery = _load_gallery()
    composing = gallery.collect_example(EXAMPLES_DIR / "composing_genome_browser.py")
    refseq = gallery.collect_example(EXAMPLES_DIR / "refseq_scored_genes.py")
    stacked = gallery.collect_example(EXAMPLES_DIR / "stacked_genome_browser.py")
    viewport = gallery.collect_example(EXAMPLES_DIR / "scrollable_viewport.py")

    assert composing.spec["vconcat"][0]["axes"] == {
        "x": {"orient": "top", "title": None}
    }
    assert refseq.spec["axes"] == {"x": {"title": None}}
    assert stacked.spec["axes"] == {
        "x": {"orient": "bottom", "title": "Genomic position"}
    }
    assert viewport.spec["view"] == {"stroke": "lightgray"}


def test_examples_use_typed_layout_definitions() -> None:
    gallery = _load_gallery()
    ascat = gallery.collect_example(EXAMPLES_DIR / "ascat_fitting.py")
    lollipop = gallery.collect_example(EXAMPLES_DIR / "pik3ca_tcga_brca_lollipop.py")
    upset = gallery.collect_example(EXAMPLES_DIR / "upset_mutations.py")

    def values_for_key(spec: object, key: str) -> list[object]:
        if isinstance(spec, list):
            return [value for item in spec for value in values_for_key(item, key)]
        if not isinstance(spec, dict):
            return []
        return [
            *([spec[key]] if key in spec else []),
            *(value for item in spec.values() for value in values_for_key(item, key)),
        ]

    assert {"grow": 2} in values_for_key(ascat.spec, "height")
    assert {"top": -5} in values_for_key(lollipop.spec, "padding")
    assert {"left": 45} in values_for_key(upset.spec, "padding")


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
    assert example.height == 720
    center_column, summary_column = example.spec["concat"]
    sample_tracks = center_column["vconcat"][0]
    matrix_panel = sample_tracks["vconcat"][4]
    placeholder, matrix_summary = summary_column["concat"]
    percent_panel, gene_count_panel = matrix_summary["concat"]
    assert example.spec["spacing"] == 2
    assert matrix_summary["spacing"] == 2
    assert percent_panel["width"] == 32
    matrix_layers = matrix_panel["layer"]
    assert matrix_panel["scales"]["y"]["domain"]
    assert matrix_panel["scales"]["y"]["reverse"] is True
    assert matrix_summary["resolve"]["scale"]["y"] == "shared"
    assert sample_tracks["params"] == [
        {
            "name": "sampleRuler",
            "persist": False,
            "ruler": {
                "encodings": ["x"],
                "extent": "container",
                "snap": False,
                "mark": {"opacity": 0.3},
            },
        }
    ]
    assert example.spec["width"] == "container"
    assert sample_tracks["width"] == "container"
    assert all(
        panel["width"] == "container"
        for panel in [
            *sample_tracks["vconcat"][:4],
            matrix_panel,
            *sample_tracks["vconcat"][5:],
        ]
    )

    assert sample_tracks["resolve"]["scale"]["x"] == "shared"
    assert sample_tracks["resolve"]["scale"]["y"] == "independent"
    assert sample_tracks["resolve"]["axis"]["y"] == "independent"
    assert example.spec["resolve"]["scale"] == {"x": "shared", "y": "independent"}
    for layer in matrix_layers:
        assert layer["encoding"]["y"]["field"] == "gene"
        assert layer["encoding"]["y"]["type"] == "nominal"
        assert "axis" not in layer["encoding"]["y"]
    assert matrix_layers[1]["encoding"]["color"]["legend"] is None
    assert sample_tracks["scales"]["x"] == {
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
    assert percent_panel["encoding"]["x"] == {"value": 1}
    assert percent_panel["mark"]["clip"] == "never"
    assert "scale" not in percent_panel["encoding"]["y"]
    count_layers = gene_count_panel["layer"]
    assert all("scale" not in layer["encoding"]["y"] for layer in count_layers)
    assert all(panel["data"]["values"] for panel in sample_tracks["vconcat"][5:])
    assert len(sample_tracks["vconcat"]) == 8
    assert placeholder["name"] == "summary-placeholder"
    assert placeholder["height"] == 162
    assert "hconcat" not in example.spec


def test_laml_oncoprint_uses_shared_sample_index_scale() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "oncoprint.py")

    assert example.height == 530
    assert example.max_width == 760
    sample_column, percent_column, counts_column = example.spec["concat"]
    tmb, matrix_panel = sample_column["concat"]
    _, percent_panel = percent_column["concat"]
    count_title, counts_panel = counts_column["concat"]
    assert tmb["width"] == matrix_panel["width"] == 400
    gene_scale = {
        "domain": [
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
        ],
        "reverse": True,
        "padding": 0.08,
    }
    assert matrix_panel["scales"]["y"] == gene_scale
    assert percent_panel["scales"]["y"] == gene_scale
    assert counts_panel["scales"]["y"] == gene_scale
    assert matrix_panel["params"] == [
        {
            "name": "sampleRuler",
            "persist": False,
            "ruler": {
                "encodings": ["x"],
                "snap": False,
                "mark": {"opacity": 0.3},
            },
        }
    ]
    assert tmb["encoding"]["color"]["legend"] is None
    assert matrix_panel["layer"][1]["encoding"]["color"]["legend"]["columns"] == 3

    assert example.spec["resolve"]["scale"] == {
        "x": "independent",
        "y": "independent",
    }
    assert sample_column["resolve"]["scale"] == {
        "x": "shared",
        "y": "independent",
    }
    assert sample_column["scales"]["x"] == {
        "domain": [-0.5, 192.5],
        "paddingInner": 0,
        "paddingOuter": 0,
        "zoom": True,
    }
    assert "scales" not in example.spec
    assert "resolve" not in counts_panel
    for layer in [tmb, *matrix_panel["layer"]]:
        assert layer["encoding"]["x"]["field"] == "sample_order"
        assert layer["encoding"]["x"]["type"] == "index"
        assert "x2" not in layer["encoding"]
    assert tmb["transform"][0] == {
        "type": "stack",
        "groupby": ["sample_order"],
        "as": ["_y0", "_y1"],
        "field": "count",
    }
    count_bars = counts_panel["layer"][1]
    assert count_bars["transform"][0] == {
        "type": "stack",
        "groupby": ["gene"],
        "as": ["_x0", "_x1"],
        "field": "count",
    }
    assert percent_panel["encoding"]["x"] == {"value": 1}
    assert "scale" not in percent_panel["encoding"]["y"]
    assert all("scale" not in layer["encoding"]["y"] for layer in counts_panel["layer"])
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
    assert count_title["encoding"]["x"] == {"value": 0.5}


def test_oncoprint_examples_include_data_provenance() -> None:
    gallery = _load_gallery()
    laml = gallery.collect_example(EXAMPLES_DIR / "oncoprint.py")
    luad = gallery.collect_example(EXAMPLES_DIR / "luad_oncoprint.py")

    for example in (laml, luad):
        prose = " ".join(example.prose.split())
        assert ":::{admonition} Data use and provenance" in prose
        assert "TCGA data are open-access" in prose
        assert "During data loading" in prose
        assert "GenomeSpy then renders" in prose
    assert "maftools" in laml.prose
    assert "pyoncoprint" in luad.prose


@pytest.mark.parametrize(
    ("filename", "source"),
    [
        ("manhattan_plot.py", "HapMap"),
        ("volcano_plot.py", "HapMap"),
        ("airway_ma_plot.py", "GSE52778"),
        ("airway_volcano_plot.py", "GSE52778"),
    ],
)
def test_association_and_expression_plots_include_data_provenance(
    filename: str, source: str
) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / filename)
    prose = " ".join(example.prose.split())

    assert ":::{admonition} Data use and provenance" in prose
    assert source in prose
    assert "During data loading" in prose
    assert "GenomeSpy then renders" in prose


@pytest.mark.parametrize(
    ("filename", "initial_size"),
    [
        ("volcano_plot.py", 16),
        ("airway_ma_plot.py", 14),
        ("airway_volcano_plot.py", 14),
    ],
)
def test_ma_and_volcano_points_grow_gently_when_zoomed(
    filename: str, initial_size: int
) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / filename)
    points = next(
        layer for layer in example.spec["layer"] if layer["mark"]["type"] == "point"
    )

    assert points["mark"]["size"] == {
        "expr": f"min(({initial_size} * pow(zoomLevel,0.75)),64)"
    }


def test_gallery_examples_do_not_render_data_previews() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()

    for example in gallery.collect_examples():
        markdown = extension._detail_md(example, "https://example.test/bundle.js")
        assert "## Data preview" not in markdown
        assert "gs-data-preview" not in markdown


def test_gallery_code_snippets_hide_internal_layout_metadata() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "airway_ma_plot.py")

    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert "META = {" not in markdown
    assert "LOG2FC_CUTOFF = 1.0" in markdown


@pytest.mark.parametrize(
    ("filename", "prefix", "label_field"),
    [
        ("airway_volcano_plot.py", "volcano", "volcano_label"),
        ("airway_ma_plot.py", "ma", "ma_label"),
    ],
)
def test_airway_expression_plots_include_gene_callouts(
    filename: str, prefix: str, label_field: str
) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / filename)
    layers = example.spec["layer"]
    names = [layer.get("name") for layer in layers]
    line = next(
        layer for layer in layers if layer.get("name") == f"{prefix}-callout-lines"
    )
    halos = [
        layer
        for layer in layers
        if layer.get("name", "").startswith(f"{prefix}-label-halo-")
    ]
    labels = [
        layer
        for layer in layers
        if layer.get("name") in {f"{prefix}-label-left", f"{prefix}-label-right"}
    ]

    assert line["mark"]["type"] == "rule"
    assert line["transform"] == [{"type": "filter", "expr": f"datum.{label_field}"}]
    assert len(halos) == 8
    assert len(labels) == 2
    assert all(layer["mark"]["type"] == "text" for layer in halos + labels)
    assert all(
        layer["encoding"]["text"]["field"] == label_field for layer in halos + labels
    )
    assert names.index(f"{prefix}-callout-lines") < min(
        names.index(layer["name"]) for layer in halos
    )
    assert max(names.index(layer["name"]) for layer in halos) < min(
        names.index(layer["name"]) for layer in labels
    )


@pytest.mark.parametrize(
    ("filename", "prefix", "x_field", "y_field"),
    [
        (
            "airway_volcano_plot.py",
            "volcano",
            "log2fc",
            "neglog10_pvalue_plot",
        ),
        ("airway_ma_plot.py", "ma", "log10_base_mean", "log2fc"),
    ],
)
def test_airway_callouts_use_pixel_offsets(
    filename: str, prefix: str, x_field: str, y_field: str
) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / filename)
    rule = next(
        layer
        for layer in example.spec["layer"]
        if layer.get("name") == f"{prefix}-callout-lines"
    )
    labels = [
        layer
        for layer in example.spec["layer"]
        if layer.get("name") in {f"{prefix}-label-left", f"{prefix}-label-right"}
    ]

    assert rule["mark"]["type"] == "rule"
    assert rule["mark"]["tooltip"] is None
    assert "x2Offset" not in rule["mark"]
    assert "y2Offset" not in rule["mark"]
    assert rule["transform"] == [{"type": "filter", "expr": f"datum.{prefix}_label"}]
    assert rule["encoding"]["x2"] == {"field": x_field}
    assert rule["encoding"]["y2"] == {"field": y_field}
    assert rule["encoding"]["xOffset"] == {
        "field": f"{prefix}_x_offset",
        "type": "quantitative",
        "scale": None,
    }
    assert rule["encoding"]["yOffset"] == {
        "field": f"{prefix}_y_offset",
        "type": "quantitative",
        "scale": None,
    }

    for label in labels:
        assert label["encoding"]["x"]["field"] == x_field
        assert label["encoding"]["y"]["field"] == y_field
        assert label["encoding"]["xOffset"] == {
            "field": f"{prefix}_x_offset",
            "type": "quantitative",
            "scale": None,
        }
        assert label["encoding"]["yOffset"] == {
            "field": f"{prefix}_y_offset",
            "type": "quantitative",
            "scale": None,
        }


@pytest.mark.parametrize("prefix", ["volcano", "ma"])
def test_airway_callout_labels_have_white_halos(prefix: str) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / f"airway_{prefix}_plot.py")
    layers = example.spec["layer"]
    expected_offsets = {(-1.25, -1.25), (1.25, -1.25), (-1.25, 1.25), (1.25, 1.25)}

    for side, base_dx in (("left", -4), ("right", 4)):
        label = next(
            layer for layer in layers if layer.get("name") == f"{prefix}-label-{side}"
        )
        halos = [
            layer
            for layer in layers
            if layer.get("name", "").startswith(f"{prefix}-label-halo-{side}-")
        ]

        assert label["mark"]["type"] == "text"
        assert label["mark"]["color"] == "#20262d"
        assert label["mark"]["align"] == ("right" if side == "left" else "left")
        assert label["mark"]["baseline"] == "middle"
        assert label["mark"]["tooltip"] is None
        assert {
            (halo["mark"]["dx"] - base_dx, halo["mark"]["dy"]) for halo in halos
        } == expected_offsets
        assert all(halo["mark"]["color"] == "white" for halo in halos)


@pytest.mark.parametrize("filename", ["airway_volcano_plot.py", "airway_ma_plot.py"])
def test_airway_point_tooltips_exclude_plotting_helpers(filename: str) -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / filename)
    points = next(
        layer for layer in example.spec["layer"] if layer["mark"]["type"] == "point"
    )

    assert [field["field"] for field in points["encoding"]["tooltip"]] == [
        "ensgene",
        "base_mean",
        "log2fc",
        "pvalue",
        "padj",
        "neglog10_pvalue",
        "neglog10_padj",
        "direction",
    ]


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
    assert len(example.spec["vconcat"]) == 3

    score_track, lesion_track, gene_track = example.spec["vconcat"]
    assert [layer["name"] for layer in score_track["layer"]] == [
        "zero-line",
        "q-value-rects",
        "q-value-thresholds",
    ]
    assert len(score_track["layer"][1]["data"]["values"]) == 90_240
    assert lesion_track["name"] == "gistic-all-lesions"
    assert len(lesion_track["data"]["values"]) == 146
    assert [transform["type"] for transform in lesion_track["transform"]] == [
        "regexExtract",
        "filter",
        "regexFold",
        "regexExtract",
        "project",
    ]
    assert lesion_track["encoding"]["opacity"]["field"] == "Segment type"
    assert lesion_track["encoding"]["size"]["field"] == "Segment type"
    assert gene_track["name"] == "refseq-genes"
    assert gene_track["layer"][0]["opacity"]["unitsPerPixel"] == [100000, 40000]
    assert [transform["type"] for transform in gene_track["transform"]] == [
        "linearizeGenomicCoordinate",
        "collect",
        "pileup",
        "filter",
    ]
    assert gene_track["layer"][1]["transform"][-1]["type"] == "filterScoredLabels"
    assert gene_track["layer"][1]["mark"]["clip"] == "x"
    assert "offset" not in gene_track["transform"][0]
    assert len(gene_track["data"]["values"]) == 29_599
    assert example.spec["resolve"]["scale"] == {"x": "shared", "y": "independent"}
    assert "https://data.genomespy.app" not in str(example.spec)


def test_rainfall_includes_shared_refseq_annotation_track() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "rainfall_plot.py")

    assert example.spec["assembly"] == "hg19"
    assert [view["name"] for view in example.spec["vconcat"]] == [
        "rainfall-track",
        "refseq-genes",
    ]
    assert example.spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }
    gene_track = example.spec["vconcat"][1]
    assert gene_track["title"]["offset"] == 8
    assert gene_track["layer"][0]["mark"]["style"] == "arrow-block"
    assert gene_track["layer"][0]["opacity"]["unitsPerPixel"] == [100000, 40000]
    assert gene_track["layer"][1]["transform"][-1]["type"] == "filterScoredLabels"
    assert gene_track["layer"][1]["mark"]["clip"] == "x"
    assert "offset" not in gene_track["transform"][0]
    assert len(gene_track["data"]["values"]) == 29_599
    assert "offset" not in gene_track["layer"][0]["encoding"]["x"]
    rainfall_layers = example.spec["vconcat"][0]["layer"]
    assert all(layer["encoding"]["x"]["offset"] == 1 for layer in rainfall_layers)


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
    zoom_message = read_spec["layer"][1]
    assert zoom_message["name"] == "zoom-message"
    assert zoom_message["data"] == {"values": [{}]}
    assert all("data" not in layer for layer in zoom_message["layer"])
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
        "scale": {"x": "shared", "y": "independent", "color": "independent"},
        "axis": {"x": "shared", "y": "independent"},
        "legend": {"color": "collected"},
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
    assert [track["title"] for track in tracks] == [
        {"text": "GC (%)", "style": "track-title"},
        {"text": "phyloP", "style": "track-title"},
        {"text": "cCRE", "style": "track-title"},
        {"text": "Sequence", "style": "track-title"},
        {"text": "Genes", "style": "track-title"},
    ]
    assert tracks[0]["encoding"]["y"]["axis"]["title"] is None
    assert tracks[1]["encoding"]["y"]["axis"]["title"] is None
    assert [track["data"]["lazy"]["type"] for track in tracks[:4]] == [
        "bigwig",
        "bigwig",
        "bigbed",
        "indexedFasta",
    ]
    assert tracks[2]["data"]["lazy"]["windowSize"] == 30_000
    assert tracks[3]["data"]["lazy"]["windowSize"] == 30_000
    assert "y" not in tracks[2]["encoding"]
    assert "y" not in tracks[3]["encoding"]
    assert tracks[4]["data"]["url"].endswith("refSeqGenes-hg38-release232.tsv.gz")
    assert tracks[4]["transform"][-1] == {
        "type": "filter",
        "expr": "(datum._lane < 3)",
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


def test_composed_genome_browser_builds_four_python_tracks() -> None:
    gallery = _load_gallery()
    spec = gallery.collect_example(EXAMPLES_DIR / "composing_genome_browser.py").spec

    assert spec["assembly"] == "hg38"
    assert spec["scales"]["x"]["domain"] == [
        {"chrom": "chr20", "pos": 10006452},
        {"chrom": "chr20", "pos": 10006533},
    ]
    assert spec["vconcat"][0]["axes"]["x"] == {"orient": "top", "title": None}
    assert spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }
    assert '"import"' not in str(spec)
    assert [view.get("name") for view in spec["vconcat"]] == [
        "ideogram-track",
        "indexed-fasta-six-frame-translation",
        None,
        "refseq-track",
    ]
    cytobands, translation, bam, refseq = spec["vconcat"]
    assert cytobands["data"]["url"].endswith("cytoBand.txt.gz")
    assert translation["data"]["lazy"]["type"] == "indexedFasta"
    assert bam["data"]["lazy"]["type"] == "bam"
    assert bam["vconcat"][1]["viewportHeight"] == 300
    assert refseq["data"]["url"].endswith("refSeqGenes-hg38-release232.tsv.gz")


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
    point_data = example.spec["layer"][2]["data"]["values"]
    assert {row["chrom"] for row in point_data} <= {
        *(f"chr{number}" for number in range(1, 23)),
        "chrX",
    }


def test_gallery_index_lists_every_example_in_hidden_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Toctrees feed the sidebar; the cards above are the visible listing."""
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

    assert markdown.count(":hidden:") == len(gallery.grouped_by_category(examples))
    assert "## Browse by Category" not in markdown
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
    assert "[user guide](../user-guide/index.md)" in markdown
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
            prose=example.prose,
            category=example.category,
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
    monkeypatch.setattr(extension.core, "iter_prepared_examples", lambda: iter(()))
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


def test_gallery_arrow_assets_are_rewritten_deduplicated_and_cleaned(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    extension = _load_gallery_extension()
    monkeypatch.setattr(extension.core, "ARROW_DIR", tmp_path / "arrow")
    payload = b"ARROW1-test"
    identifier = sha256(payload).hexdigest()

    assert extension._write_arrow_assets({identifier: payload}) == {identifier}
    (extension.core.ARROW_DIR / f"{identifier}.arrow").write_bytes(b"truncated")
    assert extension._write_arrow_assets({identifier: payload}) == {identifier}
    assert (extension.core.ARROW_DIR / f"{identifier}.arrow").read_bytes() == payload

    rewritten = extension._rewrite_arrow_urls(
        {"layer": [{"data": {"url": f"arrow://{identifier}"}}]}, {identifier}
    )
    assert rewritten["layer"][0]["data"]["url"] == (
        f"../../../_static/generated/arrow/{identifier}.arrow"
    )
    assert urljoin(
        "https://docs.example.test/gallery/oncoprint.html",
        "_static/specs/" + rewritten["layer"][0]["data"]["url"],
    ) == (f"https://docs.example.test/_static/generated/arrow/{identifier}.arrow")

    stale = extension.core.ARROW_DIR / f"{'b' * 64}.arrow"
    stale.write_bytes(b"stale")
    extension._remove_stale_arrow_assets({identifier})

    assert (extension.core.ARROW_DIR / f"{identifier}.arrow").exists()
    assert not stale.exists()


def test_gallery_generation_writes_prepared_arrow_assets(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    payload = b"ARROW1-test"
    identifier = sha256(payload).hexdigest()
    example = gallery.Example(
        name="arrow_example",
        title="Arrow example",
        description="",
        prose="",
        category="Basics",
        order=1,
        height=200,
        max_width=None,
        source="chart = None",
        spec={
            "mark": "point",
            "data": {"url": f"arrow://{identifier}", "format": {"type": "arrow"}},
        },
    )

    monkeypatch.setattr(extension.core, "GALLERY_PAGES_DIR", tmp_path / "gallery")
    monkeypatch.setattr(extension.core, "SPECS_DIR", tmp_path / "specs")
    monkeypatch.setattr(extension.core, "ARROW_DIR", tmp_path / "arrow")
    monkeypatch.setattr(
        extension.core,
        "iter_prepared_examples",
        lambda: iter([(example, {identifier: payload})]),
    )
    monkeypatch.setattr(extension.core, "thumb_filename", lambda _: "thumb.png")

    extension._generate(type("App", (), {"env": type("Env", (), {})()})())

    spec = (extension.core.SPECS_DIR / "arrow_example.json").read_text(encoding="utf-8")
    assert f"../../../_static/generated/arrow/{identifier}.arrow" in spec
    assert (extension.core.ARROW_DIR / f"{identifier}.arrow").read_bytes() == payload


def test_gallery_detail_embed_uses_direct_container_sizing() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "airway_volcano_plot.py")
    expected = gallery.build_token([example])
    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert 'class="gs-doc-embed"' in markdown
    assert "import { embed } from 'https://example.test/bundle.js';" in markdown
    assert "await embed(c, spec, { bare: true });" in markdown
    assert f"airway_volcano_plot.json?v={expected}" in markdown
    assert "const spec = '../_static/specs/airway_volcano_plot.json" in markdown
    assert "Show specification</button>" in markdown
    assert "Hide specification" in markdown
    assert "loadedSpec = fetch(spec).then((response) =>" in markdown
    assert "JSON.stringify(await loadSpec(), null, 2)" in markdown
    assert "await copyText(text)" in markdown
    assert "navigator.clipboard && window.isSecureContext" in markdown
    assert "document.execCommand('copy')" in markdown
    assert "Copied to clipboard" in markdown
    assert 'class="gs-embed-copy"' in markdown
    assert 'class="gs-embed-copy-message"' in markdown
    assert 'aria-label="Copy specification"' in markdown
    assert 'class="gs-embed-spec-wrapper" hidden' in markdown
    assert "Playground" not in markdown
    assert markdown.index("```python") < markdown.index("Show specification</button>")
    assert "View the generated render spec" not in markdown
    assert "references assets hosted with these docs" not in markdown
    assert "Download the generated GenomeSpy spec" not in markdown
    assert "Loading chart" not in markdown
    assert "attachShadow" not in markdown
    assert "setInterval" not in markdown
    assert "style.opacity" not in markdown


def test_gallery_detail_includes_optional_companion_prose() -> None:
    gallery = _load_gallery()
    extension = _load_gallery_extension()
    example = gallery.collect_example(EXAMPLES_DIR / "bam_read_alignments.py")
    markdown = extension._detail_md(example, "https://example.test/bundle.js")

    assert ":::{admonition} Data use and provenance" in markdown
    assert "## Data use and provenance" not in markdown
    assert "not for clinical" in markdown
    assert "interpretation, diagnostic decisions" in markdown
    assert "## What to notice" in markdown
    assert "## Python implementation" in markdown
    assert "official GenomeSpy example" in markdown
    assert markdown.index(":::{admonition} Data use and provenance") < markdown.index(
        "## Code"
    )


def test_gallery_build_token_changes_with_companion_prose() -> None:
    gallery = _load_gallery()
    example = gallery.collect_example(EXAMPLES_DIR / "bam_read_alignments.py")
    mutated = gallery.Example(
        name=example.name,
        title=example.title,
        description=example.description,
        prose=example.prose + "\nChanged prose.",
        category=example.category,
        order=example.order,
        height=example.height,
        max_width=example.max_width,
        source=example.source,
        spec=example.spec,
    )

    assert gallery.build_token([mutated]) != gallery.build_token([example])


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


def test_stylesheet_gives_the_tooltip_an_explicit_text_color() -> None:
    """GenomeSpy paints the tooltip background but inherits its text color."""
    css = (REPO_ROOT / "docs" / "_static" / "genomespy.css").read_text(encoding="utf-8")

    rule = re.search(r"\.gs-tooltip \{([^}]*)\}", css)
    assert rule is not None, "no tooltip rule in the documentation stylesheet"
    assert re.search(r"color:\s*#", rule.group(1))


def test_stylesheet_makes_the_specification_panel_scrollable() -> None:
    css = (REPO_ROOT / "docs" / "_static" / "genomespy.css").read_text(encoding="utf-8")

    rule = re.search(r"\.gs-embed-spec \{([^}]*)\}", css)
    assert rule is not None, "no specification panel rule in the stylesheet"
    declarations = rule.group(1)
    assert "max-height:" in declarations
    assert "overflow-x: auto" in declarations
    assert "overflow-y: auto" in declarations
    assert "white-space: pre" in declarations

    copy_rule = re.search(r"\.gs-embed-copy \{([^}]*)\}", css)
    assert copy_rule is not None, "no specification copy-button rule"
    assert "position: absolute" in copy_rule.group(1)
    assert "right:" in copy_rule.group(1)
