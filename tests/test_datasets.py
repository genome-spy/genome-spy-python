"""Tests for the packaged dataset loader."""

from __future__ import annotations

import pytest

from genome_spy.datasets import DatasetNotFoundError, available_datasets, load_dataset
from genome_spy.datasets._airway import (
    airway_differential_expression,
    airway_paired_logcounts,
)
from genome_spy.datasets._hapmap import (
    hapmap_manhattan_data,
    hapmap_qq_data,
    hapmap_volcano_data,
)
from genome_spy.datasets._oncoprint import laml_oncoplot_data, luad_oncoprint_data


def test_available_datasets_are_stable() -> None:
    assert available_datasets() == (
        "airway_metadata",
        "airway_scaledcounts",
        "dnmt3a_lollipop",
        "hapmap_gwas",
        "pik3ca_mutations",
        "tcga_brca_rainfall",
        "tcga_laml_oncoprint",
        "tcga_luad_oncoprint",
        "tcga_oncoprint",
    )


def test_load_tabular_dataset_as_dataframe() -> None:
    data = load_dataset("hapmap_gwas", as_format="dataframe")

    assert list(data.columns[:4]) == ["CHR", "BP", "P", "SNP"]
    assert not data.empty


def test_load_json_dataset() -> None:
    data = load_dataset("pik3ca_mutations", as_format="json")

    assert isinstance(data, dict)
    assert "domains" in data
    assert isinstance(data["domains"], list)


def test_load_dnmt3a_lollipop_dataset() -> None:
    data = load_dataset("dnmt3a_lollipop", as_format="json")

    assert isinstance(data, dict)
    assert data["gene"] == "DNMT3A"
    assert data["transcript"] == "NM_022552"
    assert data["protein_length"] == 912
    assert data["total_samples"] == 193
    assert data["mutated_samples"] == 47
    assert data["mutation_rate"] == 24.35
    assert len(data["features"]) == 22
    assert any(
        feature["position"] == 882 and feature["count"] == 27
        for feature in data["features"]
    )


def test_auto_format_loads_json_as_python_object() -> None:
    data = load_dataset("tcga_oncoprint")

    assert isinstance(data, list)
    assert data
    assert "gene" in data[0]


def test_load_curated_laml_oncoprint_dataset() -> None:
    data = load_dataset("tcga_laml_oncoprint", as_format="json")

    assert isinstance(data, dict)
    assert data["cohort"] == "TCGA LAML"
    assert data["total_samples"] == 193
    assert data["altered_samples"] == 141
    assert len(data["genes"]) == 10
    assert len(data["samples"]) == 193
    assert len(data["matrix"]) == 247
    assert {"sample", "gene", "class"} <= set(data["matrix"][0])


def test_load_curated_brca_rainfall_dataset() -> None:
    data = load_dataset("tcga_brca_rainfall", as_format="json")

    assert isinstance(data, dict)
    assert data["sample"] == "TCGA-A8-A08B"
    assert data["reference_build"] == "hg38"
    assert len(data["points"]) == 1890
    assert len(data["change_points"]) == 7
    assert {"chrom", "pos", "gene", "distance", "log10_distance", "con_class"} <= set(
        data["points"][0]
    )
    assert {"chrom", "start", "end", "count", "mean_distance", "arrow_y"} <= set(
        data["change_points"][0]
    )


def test_load_curated_luad_oncoprint_dataset() -> None:
    data = load_dataset("tcga_luad_oncoprint", as_format="json")

    assert isinstance(data, dict)
    assert data["cohort"] == "TCGA LUAD"
    assert data["sample_count"] == 507
    assert data["gene_count"] == 26
    assert len(data["samples"]) == 507
    assert len(data["genes"]) == 26
    assert len(data["sample_burden"]) > 0
    assert len(data["mutation_spectrum"]) > 0
    assert len(data["heatmap_cells"]) == 3549
    assert {"sample", "sample_order"} <= set(data["samples"][0])
    assert {"gene", "gene_order", "altered_samples"} <= set(data["genes"][0])


def test_oncoprint_helpers_return_chart_ready_data() -> None:
    laml = laml_oncoplot_data()
    luad = luad_oncoprint_data()

    assert laml.sample_domain == [0, laml.total_samples]
    assert laml.count_grid["x1"].eq(laml.count_limit).all()
    assert laml.matrix["gene"].dtype.name == "category"
    assert luad.sample_domain[1] == len(luad.samples["sample_order"].unique())
    assert luad.count_grid["x1"].eq(luad.count_limit).all()
    assert luad.grid["gene"].dtype.name == "category"


def test_airway_paired_logcounts_uses_packaged_data() -> None:
    base_mean, treated, control = airway_paired_logcounts()

    assert len(base_mean) == len(treated) == len(control)
    assert not treated.empty
    assert list(treated.columns) == list(control.columns)
    assert treated.index.equals(control.index)
    assert treated.index.equals(base_mean.index)


def test_airway_differential_expression_is_chart_ready() -> None:
    data, domains = airway_differential_expression(max_genes=200)

    assert not data.empty
    assert {
        "ensgene",
        "log2fc",
        "pvalue",
        "padj",
        "neglog10_pvalue",
        "neglog10_pvalue_plot",
        "direction",
    } <= set(data.columns)
    assert set(data["direction"]) <= {"up in dex", "down in dex", "n.s."}
    assert set(domains) == {"ma_x", "ma_y", "volcano_x", "volcano_y", "pvalue_cutoff"}


def test_hapmap_prepared_association_tables_are_chart_ready() -> None:
    manhattan, top_hits, manhattan_domains = hapmap_manhattan_data()
    qq, deviation, qq_domains = hapmap_qq_data()
    volcano, volcano_domains = hapmap_volcano_data()

    assert {"chrom", "neglog", "chrom_group"} <= set(manhattan.columns)
    assert set(manhattan["chrom"].unique()) <= {
        *(f"chr{number}" for number in range(1, 23)),
        "chrX",
    }
    assert len(top_hits) == 8
    assert {"y_domain", "genome_wide_y", "suggestive_y"} <= set(manhattan_domains)
    assert {"expected", "observed", "pattern"} <= set(qq.columns)
    assert {"x0", "x1", "zero", "delta_mean", "direction"} <= set(deviation.columns)
    assert {"limit", "delta_limit", "annotation_x", "tail_y"} <= set(qq_domains)
    assert {"neglog", "association"} <= set(volcano.columns)
    assert set(volcano["association"]) <= {"protective", "n.s.", "risk"}
    assert {"x_domain", "y_domain", "effect_cutoff", "neglog_pvalue_cutoff"} <= set(
        volcano_domains
    )


def test_unknown_dataset_raises_contextual_error() -> None:
    with pytest.raises(DatasetNotFoundError, match="Unknown dataset"):
        load_dataset("not_a_dataset")
