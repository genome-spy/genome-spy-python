"""Documentation tutorials must stay executable and single-sourced."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType

import pytest

pytestmark = pytest.mark.docs

REPO_ROOT = Path(__file__).resolve().parents[1]
TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "getting_started.py"
GETTING_STARTED_PATH = REPO_ROOT / "docs" / "getting-started.md"
DATA_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "data_inputs.py"
DATA_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "data.md"
MARKS_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "charts_and_marks.py"
MARKS_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "charts.md"
ENCODING_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "encoding_channels.py"
ENCODING_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "encodings.md"
GUIDES_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "scales_and_guides.py"
GUIDES_PATH = REPO_ROOT / "docs" / "user-guide" / "scales-axes-legends.md"
TRANSFORMS_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "transforms.py"
TRANSFORMS_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "transforms.md"
COMPOSITION_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "composition.py"
COMPOSITION_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "composition.md"
CONFIGURATION_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "configuration.py"
CONFIGURATION_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "configuration.md"
GENOMIC_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "genomic_coordinates.py"
GENOMIC_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "genomic-axes.md"
GENOMIC_DATA_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "genomic_data.py"
GENOMIC_DATA_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "genomic-data.md"
BROWSER_LAYOUT_TUTORIAL_PATH = (
    REPO_ROOT / "docs" / "tutorials" / "genome_browser_layouts.py"
)
BROWSER_LAYOUT_GUIDE_PATH = (
    REPO_ROOT / "docs" / "user-guide" / "genome-browser-layouts.md"
)
ANNOTATIONS_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "annotations.py"
ANNOTATIONS_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "annotations.md"
INTERACTION_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "interaction.py"
INTERACTION_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "interaction.md"
NOTEBOOKS_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "notebooks.py"
NOTEBOOKS_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "notebooks.md"
SERIALIZATION_TUTORIAL_PATH = REPO_ROOT / "docs" / "tutorials" / "serialization.py"
SERIALIZATION_GUIDE_PATH = REPO_ROOT / "docs" / "user-guide" / "serialization.md"
GALLERY_EXTENSION_PATH = REPO_ROOT / "docs" / "_ext" / "genomespy_gallery.py"
TUTORIALS_DIR = REPO_ROOT / "docs" / "tutorials"


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_tutorial_sizes_are_owned_by_the_embedder() -> None:
    sizing_demonstrations = {"configuration:configured_chart"}
    blocks: list[tuple[str, str]] = []
    pattern = re.compile(
        r"^```\{genomespy-chart\}\s+(\S+)\n((?::[^\n]+\n)*)", re.MULTILINE
    )
    for path in sorted((REPO_ROOT / "docs").rglob("*.md")):
        if "_build" in path.parts:
            continue
        blocks.extend(pattern.findall(path.read_text(encoding="utf-8")))

    assert blocks
    for target, options in blocks:
        assert re.search(r"^:height:\s*\d+", options, re.MULTILINE), target
        module_name, attribute = target.split(":")
        tutorial = _load_module(
            f"_sizing_{module_name}", TUTORIALS_DIR / f"{module_name}.py"
        )
        spec = getattr(tutorial, attribute).to_dict()
        if target not in sizing_demonstrations:
            assert not isinstance(spec.get("width"), (int, float)), target
            assert not isinstance(spec.get("height"), (int, float)), target


def test_getting_started_charts_serialize_and_validate() -> None:
    tutorial = _load_module("_getting_started_tutorial", TUTORIAL_PATH)

    assert tutorial.CHARTS
    for chart in tutorial.CHARTS.values():
        spec = chart.to_dict()
        assert spec["$schema"].endswith("/dist/schema.json")
        assert "mark" in spec

    genomic_spec = tutorial.CHARTS["genomic_track"].to_dict()
    assert genomic_spec["assembly"] == "hg38"
    assert genomic_spec["encoding"]["x"]["type"] == "locus"
    # Without a domain the whole assembly is visible and the features vanish.
    assert genomic_spec["encoding"]["x"]["scale"] == {
        "domain": [
            {"chrom": "chr17", "pos": 43_040_000},
            {"chrom": "chr17", "pos": 43_080_000},
        ]
    }
    assert genomic_spec["encoding"]["x2"] == {"chrom": "chrom", "pos": "end"}


def test_getting_started_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_getting_started_tutorial_targets", TUTORIAL_PATH)
    source = GETTING_STARTED_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} getting_started:([A-Za-z0-9_]+)", source)

    assert targets == ["encoded_points", "measurement_chart", "genomic_track"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_data_guide_charts_serialize_with_expected_data_ownership() -> None:
    tutorial = _load_module("_data_inputs_tutorial", DATA_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    inline_spec = tutorial.inline_chart.to_dict()
    assert inline_spec["data"]["values"] == tutorial.measurements

    url_spec = tutorial.url_chart.to_dict()
    assert url_spec["data"] == {
        "url": "https://example.org/measurements.csv",
        "format": {"type": "csv"},
    }

    inherited_spec = tutorial.inherited_chart.to_dict()
    assert inherited_spec["data"]["values"] == tutorial.measurements
    assert all("data" not in layer for layer in inherited_spec["layer"])
    # The title reserves the space the dy=-12 labels need above the top point.
    assert inherited_spec["title"] == "Measurements over time"
    assert "padding" not in inherited_spec["layer"][0]["encoding"]["y"]["scale"]


def test_data_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_data_inputs_tutorial_targets", DATA_TUTORIAL_PATH)
    source = DATA_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} data_inputs:([A-Za-z0-9_]+)", source)

    assert targets == ["inline_chart", "inherited_chart"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_charts_and_marks_guide_examples_serialize() -> None:
    tutorial = _load_module("_charts_and_marks_tutorial", MARKS_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    point_spec = tutorial.point_chart.to_dict()
    assert point_spec["mark"] == {
        "type": "point",
        "filled": True,
        "stroke": "white",
        "strokeWidth": 1,
    }
    assert point_spec["encoding"]["size"]["field"] == "amount"
    assert "height" not in point_spec
    assert point_spec["description"] == "Six measurements grouped by sample."

    interval_spec = tutorial.interval_chart.to_dict()
    assert interval_spec["mark"]["type"] == "rule"
    assert interval_spec["encoding"]["x2"] == {"field": "end"}

    assert tutorial.text_chart.to_dict()["mark"]["type"] == "text"
    assert tutorial.link_chart.to_dict()["mark"]["type"] == "link"
    assert tutorial.arrow_chart.to_dict()["mark"]["type"] == "arrow"


def test_charts_and_marks_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_charts_and_marks_tutorial_targets", MARKS_TUTORIAL_PATH)
    source = MARKS_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(
        r"\{genomespy-chart\} charts_and_marks:([A-Za-z0-9_]+)", source
    )

    assert targets == [
        "point_chart",
        "interval_chart",
        "text_chart",
        "link_chart",
        "arrow_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_encoding_guide_examples_serialize_with_expected_definitions() -> None:
    tutorial = _load_module("_encoding_channels_tutorial", ENCODING_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    assert (
        tutorial.shorthand_chart.to_dict()["encoding"]
        == tutorial.explicit_chart.to_dict()["encoding"]
    )

    channel_spec = tutorial.channel_chart.to_dict()
    assert channel_spec["encoding"]["x"]["type"] == "quantitative"
    assert channel_spec["encoding"]["y"]["type"] == "ordinal"
    assert channel_spec["encoding"]["color"]["type"] == "nominal"
    assert channel_spec["encoding"]["tooltip"][2]["format"] == ".0%"

    assert tutorial.index_chart.to_dict()["encoding"]["x"]["type"] == "index"

    locus_spec = tutorial.locus_chart.to_dict()
    assert locus_spec["assembly"] == "hg38"
    # An explicit domain keeps the features visible; the whole-genome default
    # would render them as one thin line.
    assert locus_spec["encoding"]["x"] == {
        "chrom": "chrom",
        "pos": "start",
        "type": "locus",
        "scale": {
            "domain": [
                {"chrom": "chr17", "pos": 43_040_000},
                {"chrom": "chr17", "pos": 43_080_000},
            ]
        },
    }
    assert locus_spec["encoding"]["x2"] == {
        "chrom": "chrom",
        "pos": "end",
    }

    # A constant datum and a calculated expression give a scale no domain to
    # derive, so both need an explicit one or the marks never resolve.
    definition_spec = tutorial.definition_chart.to_dict()["encoding"]
    assert definition_spec["y"] == {
        "datum": 0,
        "type": "quantitative",
        "scale": {"domain": [-1, 1]},
    }
    assert definition_spec["color"] == {"value": "#4c78a8"}
    assert definition_spec["size"] == {
        "expr": "(datum.amount * datum.confidence)",
        "type": "quantitative",
        "scale": {"domain": [0, 35]},
        "legend": None,
    }


def test_encoding_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module(
        "_encoding_channels_tutorial_targets", ENCODING_TUTORIAL_PATH
    )
    source = ENCODING_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(
        r"\{genomespy-chart\} encoding_channels:([A-Za-z0-9_]+)", source
    )

    assert targets == [
        "channel_chart",
        "index_chart",
        "locus_chart",
        "definition_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_scales_and_guides_examples_serialize_expected_options() -> None:
    tutorial = _load_module("_scales_and_guides_tutorial", GUIDES_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    automatic_spec = tutorial.automatic_chart.to_dict()
    assert all(
        "scale" not in automatic_spec["encoding"][channel]
        for channel in ("x", "y", "color")
    )
    assert "axis" not in automatic_spec["encoding"]["x"]
    assert "legend" not in automatic_spec["encoding"]["color"]

    customized_spec = tutorial.customized_chart.to_dict()["encoding"]
    assert customized_spec["x"]["scale"] == {
        "domain": [0.5, 3.5],
        "zoom": True,
    }
    assert customized_spec["y"]["axis"] == {"grid": True, "tickCount": 4}
    assert customized_spec["color"]["scale"] == {
        "domain": ["control", "treated"],
        "range": ["#4c78a8", "#e45756"],
    }
    assert customized_spec["color"]["legend"] == {
        "title": "Sample group",
        "orient": "top",
        "direction": "horizontal",
    }

    minimal_spec = tutorial.minimal_chart.to_dict()["encoding"]
    assert minimal_spec["x"]["axis"] is None
    assert minimal_spec["color"]["legend"] is None
    assert "scale" not in minimal_spec["color"]


def test_scales_and_guides_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_scales_and_guides_targets", GUIDES_TUTORIAL_PATH)
    source = GUIDES_PATH.read_text(encoding="utf-8")
    targets = re.findall(
        r"\{genomespy-chart\} scales_and_guides:([A-Za-z0-9_]+)", source
    )

    assert targets == ["automatic_chart", "customized_chart", "minimal_chart"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_transform_guide_examples_serialize_in_pipeline_order() -> None:
    tutorial = _load_module("_transforms_tutorial", TRANSFORMS_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    filtered_spec = tutorial.filtered_chart.to_dict()
    assert filtered_spec["transform"] == [
        {"type": "filter", "expr": "(datum.quality >= 0.7)"}
    ]
    assert len(filtered_spec["data"]["values"]) == 6

    formula_spec = tutorial.formula_chart.to_dict()
    assert formula_spec["transform"] == [
        {
            "type": "formula",
            "expr": "(datum.response * 100)",
            "as": "responsePercent",
        }
    ]
    assert formula_spec["encoding"]["y"]["field"] == "responsePercent"

    aggregate_spec = tutorial.aggregate_chart.to_dict()
    assert aggregate_spec["transform"] == [
        {
            "type": "formula",
            "expr": "(datum.response * 100)",
            "as": "responsePercent",
        },
        {
            "type": "aggregate",
            "groupby": ["group"],
            "fields": ["responsePercent"],
            "ops": ["mean"],
            "as": ["meanResponse"],
        },
    ]
    assert aggregate_spec["encoding"]["y"]["field"] == "meanResponse"


def test_transform_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_transforms_tutorial_targets", TRANSFORMS_TUTORIAL_PATH)
    source = TRANSFORMS_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} transforms:([A-Za-z0-9_]+)", source)

    assert targets == ["filtered_chart", "formula_chart", "aggregate_chart"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_composition_guide_examples_serialize_inherited_properties() -> None:
    tutorial = _load_module("_composition_tutorial", COMPOSITION_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    layered_spec = tutorial.layered_chart.to_dict()
    assert "data" in layered_spec
    assert {"x", "y", "color"} <= layered_spec["encoding"].keys()
    assert all("data" not in child for child in layered_spec["layer"])
    assert all("x" not in child.get("encoding", {}) for child in layered_spec["layer"])
    assert layered_spec["layer"][1]["encoding"]["text"]["field"] == "label"

    vertical_spec = tutorial.vertical_chart.to_dict()
    assert "data" in vertical_spec
    assert vertical_spec["spacing"] == 20
    assert vertical_spec["encoding"]["x"]["scale"]["zoom"] is True
    assert all(
        child["view"] == {"stroke": "lightgray"} for child in vertical_spec["vconcat"]
    )
    assert all("data" not in child for child in vertical_spec["vconcat"])
    assert vertical_spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }

    horizontal_spec = tutorial.horizontal_chart.to_dict()
    assert len(horizontal_spec["hconcat"]) == 2
    assert horizontal_spec["spacing"] == 20
    assert all(
        child["view"] == {"stroke": "lightgray"} for child in horizontal_spec["hconcat"]
    )
    assert horizontal_spec["resolve"]["scale"] == {"x": "shared", "y": "shared"}


def test_composition_grid_uses_placeholder_and_excluded_summaries() -> None:
    tutorial = _load_module("_composition_grid_tutorial", COMPOSITION_TUTORIAL_PATH)
    spec = tutorial.grid_chart.to_dict()

    assert spec["columns"] == 2
    assert len(spec["concat"]) == 4
    assert spec["concat"][0]["data"] == {"values": []}
    assert spec["concat"][1]["resolve"]["scale"] == {"y": "excluded"}
    assert spec["concat"][2]["resolve"]["scale"] == {"x": "excluded"}
    assert spec["resolve"]["scale"] == {"x": "shared", "y": "shared"}
    assert spec["scales"]["x"]["domain"] == [-0.5, 2.5]
    assert spec["scales"]["y"]["domain"] == [-0.5, 2.5]
    assert "data" in spec


def test_composition_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_composition_tutorial_targets", COMPOSITION_TUTORIAL_PATH)
    source = COMPOSITION_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} composition:([A-Za-z0-9_]+)", source)

    assert targets == [
        "layered_chart",
        "vertical_chart",
        "horizontal_chart",
        "grid_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_configuration_guide_examples_serialize_expected_scopes() -> None:
    tutorial = _load_module("_configuration_tutorial", CONFIGURATION_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    configured_spec = tutorial.configured_chart.to_dict()
    assert configured_spec["mark"] == {
        "type": "point",
        "filled": True,
        "stroke": "white",
        "strokeWidth": 1,
    }
    assert configured_spec["width"] == 360
    assert configured_spec["height"] == 210
    assert configured_spec["padding"] == {
        "top": 8,
        "right": 12,
        "bottom": 4,
        "left": 12,
    }
    assert configured_spec["view"] == {
        "fill": "#fafafa",
        "stroke": "#d3d3d3",
        "strokeWidth": 1,
    }
    assert configured_spec["config"] == {
        "point": {"size": 110, "opacity": 0.85},
        "axis": {"grid": True, "gridColor": "#e5e5e5"},
        "title": {"anchor": "start", "fontSize": 16, "subtitleFontSize": 11},
    }
    assert configured_spec["title"]["subtitle"] == (
        "Explicit properties override configured defaults"
    )

    assert tutorial.step_chart.to_dict()["width"] == {"step": 48}

    flex_spec = tutorial.flex_chart.to_dict()
    assert flex_spec["width"] == "container"
    assert flex_spec["hconcat"][0]["width"] == 120
    assert flex_spec["hconcat"][1]["width"] == {"grow": 1, "minPx": 180}

    assert tutorial.themed_chart.to_dict()["theme"] == "quartz"


def test_configuration_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module(
        "_configuration_tutorial_targets", CONFIGURATION_TUTORIAL_PATH
    )
    source = CONFIGURATION_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} configuration:([A-Za-z0-9_]+)", source)

    assert targets == [
        "configured_chart",
        "step_chart",
        "flex_chart",
        "themed_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_genomic_coordinate_examples_serialize_locus_semantics() -> None:
    tutorial = _load_module("_genomic_coordinates_tutorial", GENOMIC_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    point_spec = tutorial.point_chart.to_dict()
    assert point_spec["assembly"] == "hg38"
    assert point_spec["encoding"]["x"]["type"] == "locus"
    assert point_spec["encoding"]["x"]["chrom"] == "chrom"
    assert point_spec["encoding"]["x"]["pos"] == "pos"
    assert point_spec["encoding"]["x"]["scale"] == {"domain": tutorial.BRCA1_DOMAIN}

    interval_spec = tutorial.interval_chart.to_dict()
    assert interval_spec["encoding"]["x2"] == {"chrom": "chrom", "pos": "end"}

    offset_spec = tutorial.offset_chart.to_dict()
    assert offset_spec["encoding"]["x"]["offset"] == 1
    assert "offset" not in offset_spec["encoding"]["x2"]


def test_genomic_coordinate_examples_serialize_assembly_scope() -> None:
    tutorial = _load_module("_genomic_assemblies_tutorial", GENOMIC_TUTORIAL_PATH)

    custom_spec = tutorial.custom_assembly_chart.to_dict()
    assert custom_spec["assembly"] == "toy"
    assert custom_spec["genomes"] == {"toy": tutorial.toy_genome}
    assert [contig["name"] for contig in custom_spec["genomes"]["toy"]["contigs"]] == [
        "chrA",
        "chrB",
        "plasmid",
    ]

    multiple_spec = tutorial.multiple_assembly_chart.to_dict()
    assert "assembly" not in multiple_spec
    for channel, assembly in (("x", "hg38"), ("y", "mm10")):
        scale = multiple_spec["encoding"][channel]["scale"]
        assert scale["assembly"] == assembly
        assert scale["type"] == "locus"
        # A chrom/pos domain is linearized without consulting the scale's own
        # assembly, so it throws "No genomes have been configured!" here.
        assert "domain" not in scale


def test_genomic_coordinate_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_genomic_coordinates_targets", GENOMIC_TUTORIAL_PATH)
    source = GENOMIC_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(
        r"\{genomespy-chart\} genomic_coordinates:([A-Za-z0-9_]+)", source
    )

    assert targets == [
        "point_chart",
        "interval_chart",
        "offset_chart",
        "custom_assembly_chart",
        "multiple_assembly_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_genomic_data_examples_serialize_lazy_sources() -> None:
    tutorial = _load_module("_genomic_data_tutorial", GENOMIC_DATA_TUTORIAL_PATH)

    for chart in tutorial.CHARTS.values():
        assert chart.to_dict()["$schema"].endswith("/dist/schema.json")

    bigwig_spec = tutorial.bigwig_chart.to_dict()
    assert bigwig_spec["data"]["lazy"]["type"] == "bigwig"
    assert bigwig_spec["encoding"]["x"]["type"] == "locus"
    assert bigwig_spec["encoding"]["x"]["scale"] == {"domain": tutorial.REGION}

    bigbed_spec = tutorial.bigbed_chart.to_dict()
    assert bigbed_spec["data"]["lazy"]["type"] == "bigbed"
    assert bigbed_spec["encoding"]["x2"] == {
        "chrom": "chrom",
        "pos": "chromEnd",
    }


def test_genomic_data_guide_embeds_only_representative_tracks() -> None:
    tutorial = _load_module("_genomic_data_targets", GENOMIC_DATA_TUTORIAL_PATH)
    source = GENOMIC_DATA_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} genomic_data:([A-Za-z0-9_]+)", source)

    assert targets == ["bigwig_chart", "bigbed_chart"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_genome_browser_tracks_keep_local_data_and_y_encodings() -> None:
    tutorial = _load_module(
        "_genome_browser_layout_tracks", BROWSER_LAYOUT_TUTORIAL_PATH
    )

    signal_spec = tutorial.signal_track.to_dict()
    assert signal_spec["data"]["lazy"]["type"] == "bigwig"
    assert signal_spec["encoding"]["y"]["type"] == "quantitative"
    assert "scale" not in signal_spec["encoding"]["x"]

    annotation_spec = tutorial.annotation_track.to_dict()
    assert annotation_spec["data"]["lazy"]["type"] == "bigbed"
    assert annotation_spec["encoding"]["y"]["type"] == "nominal"
    assert all("data" not in child for child in annotation_spec["layer"])
    assert annotation_spec["layer"][1]["opacity"] == {
        "unitsPerPixel": [500, 100],
        "values": [0, 1],
    }


def test_genome_browser_parent_owns_shared_genomic_resolution() -> None:
    tutorial = _load_module("_genome_browser_layout", BROWSER_LAYOUT_TUTORIAL_PATH)
    spec = tutorial.browser.to_dict()

    assert spec["assembly"] == "hg38"
    assert spec["scales"]["x"] == {"domain": tutorial.REGION}
    assert spec["axes"]["x"] == {
        "orient": "bottom",
        "title": "Genomic position",
        "chromGrid": True,
    }
    assert spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }
    assert len(spec["vconcat"]) == 2
    assert spec["spacing"] == 8
    assert tutorial.scrollable_annotations.to_dict()["viewportHeight"] == 120


def test_genome_browser_guide_embeds_only_completed_browser() -> None:
    tutorial = _load_module(
        "_genome_browser_layout_targets", BROWSER_LAYOUT_TUTORIAL_PATH
    )
    source = BROWSER_LAYOUT_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(
        r"\{genomespy-chart\} genome_browser_layouts:([A-Za-z0-9_]+)", source
    )

    assert targets == ["browser"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_annotation_layers_keep_targets_and_labels_separate() -> None:
    tutorial = _load_module("_annotations", ANNOTATIONS_TUTORIAL_PATH)
    spec = tutorial.point_annotation_chart.to_dict()

    assert [layer["mark"]["type"] for layer in spec["layer"]] == [
        "point",
        "rule",
        "text",
    ]
    assert spec["layer"][0]["encoding"]["tooltip"] == [
        {"field": "gene", "type": "nominal", "title": "Gene"},
        {"field": "effect", "type": "quantitative", "title": "Effect"},
        {
            "field": "significance",
            "type": "quantitative",
            "title": "Significance",
        },
    ]
    assert spec["layer"][1]["mark"]["tooltip"] is None
    assert spec["layer"][1]["encoding"] == {
        "x": {"field": "effect", "type": "quantitative", "title": "Effect"},
        "xOffset": {
            "field": "label_x_offset",
            "type": "quantitative",
            "scale": None,
        },
        "x2": {"field": "effect"},
        "y": {
            "field": "significance",
            "type": "quantitative",
            "title": "Significance",
        },
        "yOffset": {
            "field": "label_y_offset",
            "type": "quantitative",
            "scale": None,
        },
        "y2": {"field": "significance"},
    }
    assert spec["layer"][2]["mark"]["tooltip"] is None
    assert spec["layer"][2]["encoding"]["x"] == {
        "field": "effect",
        "type": "quantitative",
        "title": "Effect",
    }
    assert spec["layer"][2]["encoding"]["xOffset"] == {
        "field": "label_x_offset",
        "type": "quantitative",
        "scale": None,
    }
    assert spec["layer"][2]["encoding"]["y"] == {
        "field": "significance",
        "type": "quantitative",
        "title": "Significance",
    }
    assert spec["layer"][2]["encoding"]["yOffset"] == {
        "field": "label_y_offset",
        "type": "quantitative",
        "scale": None,
    }
    assert spec["layer"][2]["encoding"]["text"] == {
        "field": "gene",
        "type": "nominal",
    }


def test_gene_annotation_track_prioritizes_overlapping_labels() -> None:
    tutorial = _load_module("_gene_annotations", ANNOTATIONS_TUTORIAL_PATH)
    spec = tutorial.gene_annotation_track.to_dict()
    body, labels = spec["layer"]

    assert body["mark"]["type"] == "arrow"
    assert body["mark"]["style"] == "arrow-block"
    assert body["opacity"] == {
        "unitsPerPixel": [100000, 40000],
        "values": [0, 1],
    }
    assert body["encoding"]["direction"]["field"] == "strand"
    assert labels["transform"][-1] == {
        "type": "filterScoredLabels",
        "pos": "linear_start",
        "pos2": "linear_end",
        "asMidpoint": "label_position",
        "score": "score",
        "width": "label_width",
        "lane": "lane",
        "padding": 5,
    }
    assert [transform["type"] for transform in spec["transform"]] == [
        "linearizeGenomicCoordinate",
        "collect",
        "pileup",
        "filter",
    ]
    assert "offset" not in spec["transform"][0]
    assert "offset" not in body["encoding"]["x"]
    assert len(tutorial.genes) == 29_599
    assert {"CPQ", "TSPYL5", "MTDH", "MATN2"} <= set(tutorial.genes["symbol"])


def test_annotations_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_annotation_targets", ANNOTATIONS_TUTORIAL_PATH)
    source = ANNOTATIONS_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} annotations:([A-Za-z0-9_]+)", source)

    assert targets == ["point_annotation_chart", "gene_annotation_track"]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_interaction_zoom_and_bound_parameters_serialize() -> None:
    tutorial = _load_module("_interaction_parameters", INTERACTION_TUTORIAL_PATH)

    zoom_spec = tutorial.zoom_chart.to_dict()
    # Locus scales zoom by default, so the example sets no zoom option.
    assert zoom_spec["encoding"]["x"]["scale"] == {"domain": tutorial.REGION}

    bound_spec = tutorial.bound_chart.to_dict()
    assert bound_spec["transform"] == [
        {"type": "filter", "expr": "(datum.score >= minScore)"}
    ]
    assert bound_spec["mark"]["size"] == {"expr": "pointSize"}
    assert bound_spec["encoding"]["x"]["scale"] == {"domain": tutorial.VARIANT_DOMAIN}
    assert bound_spec["params"] == [
        {
            "name": "minScore",
            "value": 0.4,
            "bind": {
                "input": "range",
                "min": 0,
                "max": 1,
                "step": 0.05,
                "name": "Minimum score: ",
            },
        },
        {"name": "pointSize", "expr": "60 + minScore * 100"},
    ]


def test_interaction_selection_uses_key_and_conditional_encodings() -> None:
    tutorial = _load_module("_interaction_selection", INTERACTION_TUTORIAL_PATH)
    spec = tutorial.selection_chart.to_dict()

    assert spec["params"] == [{"name": "selectedVariant", "select": "point"}]
    assert spec["encoding"]["key"] == {"field": "id"}
    assert spec["encoding"]["opacity"] == {
        "value": 0.25,
        "condition": {"param": "selectedVariant", "empty": True, "value": 1},
    }
    assert spec["encoding"]["strokeWidth"]["condition"] == {
        "param": "selectedVariant",
        "empty": False,
        "value": 2,
    }


def test_interaction_ruler_is_declared_once_on_shared_parent() -> None:
    tutorial = _load_module("_interaction_ruler", INTERACTION_TUTORIAL_PATH)
    spec = tutorial.ruler_chart.to_dict()

    assert spec["params"] == [
        {
            "name": "cursor",
            "persist": False,
            "ruler": {
                "encodings": ["x"],
                "extent": "container",
                "display": "line",
                "mark": {"stroke": "#d62728", "strokeWidth": 1},
            },
        }
    ]
    assert all("params" not in child for child in spec["vconcat"])
    assert spec["encoding"]["x"]["type"] == "locus"
    assert spec["resolve"] == {
        "scale": {"x": "shared", "y": "independent"},
        "axis": {"x": "shared", "y": "independent"},
    }


def test_interaction_guide_embeds_only_named_tutorial_charts() -> None:
    tutorial = _load_module("_interaction_targets", INTERACTION_TUTORIAL_PATH)
    source = INTERACTION_GUIDE_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\{genomespy-chart\} interaction:([A-Za-z0-9_]+)", source)

    assert targets == [
        "zoom_chart",
        "bound_chart",
        "selection_chart",
        "ruler_chart",
    ]
    assert set(targets) <= tutorial.CHARTS.keys()


def test_notebook_tutorial_declares_one_stable_named_dataset() -> None:
    tutorial = _load_module("_notebook_tutorial", NOTEBOOKS_TUTORIAL_PATH)
    spec = tutorial.chart.to_dict()

    assert spec["data"] == {"name": "measurements"}
    assert spec["datasets"] == {"measurements": tutorial.initial_rows}
    assert tutorial.view.dataset_names == ("measurements",)
    assert tutorial.view.spec["data"] == {"name": "measurements"}


def test_notebook_tutorial_updates_without_rewriting_widget_spec() -> None:
    tutorial = _load_module("_notebook_updates", NOTEBOOKS_TUTORIAL_PATH)
    original_spec = tutorial.view.spec.copy()

    tutorial.view.set_dataset(
        "measurements",
        [{"sample": "D", "value": 2.5, "group": "treated"}],
        format="records",
    )

    assert tutorial.view.spec == original_spec
    assert tutorial.view.dataset_names == ("measurements",)


def test_notebook_guide_uses_executable_tutorial_sections() -> None:
    source = NOTEBOOKS_GUIDE_PATH.read_text(encoding="utf-8")

    for marker in (
        "notebooks-chart-start",
        "notebooks-implicit-display-start",
        "notebooks-widget-start",
        "notebooks-record-update-start",
    ):
        assert f":start-after: {marker}" in source

    assert "{genomespy-chart}" not in source


def test_serialization_tutorial_produces_dict_and_json() -> None:
    tutorial = _load_module("_serialization_tutorial", SERIALIZATION_TUTORIAL_PATH)

    assert tutorial.spec["$schema"].endswith("/dist/schema.json")
    assert tutorial.mark_definition == {
        "type": "point",
        "filled": True,
        "size": 120,
    }
    assert tutorial.x_definition == {
        "field": "sample",
        "type": "nominal",
        "title": "Sample",
    }
    assert tutorial.json_spec.startswith("{")


def test_serialization_tutorial_saves_supported_formats(tmp_path: Path) -> None:
    tutorial = _load_module("_serialization_save", SERIALIZATION_TUTORIAL_PATH)
    json_path, html_path = tutorial.save_examples(tmp_path)

    assert json_path.read_text(encoding="utf-8").endswith("\n")
    assert json_path.read_text(encoding="utf-8").startswith("{")
    html = html_path.read_text(encoding="utf-8")
    assert "import(moduleUrl)" in html
    assert "Serializable measurements" in html


def test_serialization_guide_uses_executable_tutorial_sections() -> None:
    source = SERIALIZATION_GUIDE_PATH.read_text(encoding="utf-8")

    for marker in (
        "serialization-dict-start",
        "serialization-json-start",
        "serialization-save-start",
    ):
        assert f":start-after: {marker}" in source

    assert "{genomespy-chart}" not in source


def test_tutorial_directive_uses_direct_static_bundle_embed() -> None:
    extension = _load_module(
        "_getting_started_gallery_extension", GALLERY_EXTENSION_PATH
    )
    chart = extension._load_tutorial_chart("getting_started:genomic_track")
    markup = extension._tutorial_embed_html(
        "getting_started:genomic_track",
        chart.to_dict(),
        bundle_url="https://example.test/bundle.js",
        height=190,
        title="Genomic track",
        identity="getting-started:1",
    )

    assert 'import { embed } from "https://example.test/bundle.js"' in markup
    assert "await embed(c, spec, { bare: true })" in markup
    assert "height:190px" in markup
    assert "iframe" not in markup
    assert "ResizeObserver" not in markup
    assert "attachShadow" not in markup


def test_tutorial_chart_target_rejects_paths() -> None:
    extension = _load_module(
        "_invalid_tutorial_target_extension", GALLERY_EXTENSION_PATH
    )

    with pytest.raises(ValueError, match="module:chart_name"):
        extension._load_tutorial_chart("../getting_started:genomic_track")
