"""Tests for the packaged dataset loader."""

from __future__ import annotations

import hashlib
from importlib.resources import files
from pathlib import Path

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
from genome_spy.datasets._gistic import tcga_ov_gistic_data
from genome_spy.datasets._mutation import brca_rainfall_data, dnmt3a_lollipop_data
from genome_spy.datasets._oncoprint import laml_oncoplot_data, luad_oncoprint_data


def test_available_datasets_are_stable() -> None:
    assert available_datasets() == (
        "airway_metadata",
        "airway_scaledcounts",
        "brca_maf",
        "hapmap_gwas",
        "mutation_impact_reference",
        "pik3ca_mutations",
        "pyoncoprint_tcga",
        "tal1_alphagenome_reference",
        "tcga_laml_annotations",
        "tcga_laml_maf",
        "tcga_oncoprint",
        "tcga_ov_gistic_lesions",
        "tcga_ov_gistic_scores",
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


def test_load_mutation_impact_reference_dataset() -> None:
    data = load_dataset("mutation_impact_reference", as_format="json")

    assert isinstance(data, dict)
    assert data["assembly"] == "synthetic-v1"
    assert data["chrom"] == "chrSynthetic"
    assert len(data["rows"]) == 20
    assert data["rows"][0] == {"position": 100, "base": "A", "value": 0.25}


def test_load_tal1_alphagenome_reference_dataset() -> None:
    data = load_dataset("tal1_alphagenome_reference", as_format="json")

    assert data["provenance"]["assembly"] == "GRCh38"
    assert data["interval"] == {
        "chrom": "chr1",
        "start0": 47_173_759,
        "end0": 47_304_831,
    }
    assert len(data["sequence"]) == 131_072
    offset = data["positive_control_site"]["pos1"] - 1 - data["interval"]["start0"]
    assert data["sequence"][offset] == "C"
    assert (
        hashlib.sha256(data["sequence"].encode()).hexdigest() == data["sequence_sha256"]
    )


def test_auto_format_loads_json_as_python_object() -> None:
    data = load_dataset("tcga_oncoprint")

    assert isinstance(data, list)
    assert data
    assert "gene" in data[0]


def test_load_upstream_mutation_tables() -> None:
    luad = load_dataset("pyoncoprint_tcga", as_format="dataframe")
    laml = load_dataset("tcga_laml_maf", as_format="dataframe")
    annotations = load_dataset("tcga_laml_annotations", as_format="dataframe")
    brca = load_dataset("brca_maf", as_format="dataframe")

    assert luad.shape == (145, 509)
    assert laml.shape == (2207, 17)
    assert annotations.shape == (200, 4)
    assert brca.shape == (1913, 9)
    assert luad.columns[:2].tolist() == ["track_name", "track_type"]
    assert "Tumor_Sample_Barcode" in laml


def test_load_gistic_tables_for_the_displayed_genomic_interval() -> None:
    data = tcga_ov_gistic_data()

    assert data["scores"].shape == (9046, 8)
    assert set(data["scores"]["Chromosome"]) == {18, 19, 20}
    assert data["lesions"].shape == (22, 589)


def test_upstream_mutation_files_are_byte_exact() -> None:
    data_dir = files("genome_spy.datasets").joinpath("data")
    expected_hashes = {
        "brca.maf.gz": "61d5355e960bd480bec4f245b8f096e2333408659ced0d196e42b0e38de3d724",
        "oncoprint_dataset3.json": "e07aa6ae9cf4f5f3a9f331d9979855ccf33bc47ed1bb2f4b871939b47c2a09ef",
        "pik3ca_mutations.json": "4f36df9ad960c1429827522bbd4fce0cb47520d14a5c642abe8a55969f177aec",
        "tal1_alphagenome_reference.json.gz": "10702eaaee63d2a4f600bf23ea4fac913db720aba56d33868b0f32590fc7b77e",
        "tcga.tsv": "39a90fc1f50ebcd113c37fd03894fb41b17dca4d6014f7efcf0e3f234c957742",
        "tcga_laml.maf.gz": "d102b071a052265b6f8ad7947bad1d58d3e3036fd17d6b274f7ea09a376cd6a0",
        "tcga_laml_annot.tsv": "7033030d52868e9a0f35ffd78f45a9d7a126c2edef90cf9e74e4f5d78990a710",
        "tcga_ov_gistic_lesions.tsv.gz": "e301075b6742cb8fc4d4bc0b5c125bea5b6b8eee60b196a75d9baa7825cb46b7",
        "tcga_ov_gistic_scores.tsv.gz": "2c61eb4a5f26afa9a026994cbf116796f663f74a320382ad20b50e6a9d6f30a0",
    }

    for filename, expected_hash in expected_hashes.items():
        digest = hashlib.sha256(data_dir.joinpath(filename).read_bytes()).hexdigest()
        assert digest == expected_hash


def test_mutation_helpers_return_chart_ready_data() -> None:
    dnmt3a = dnmt3a_lollipop_data()
    rainfall = brca_rainfall_data()

    assert dnmt3a["total_samples"] == 193
    assert dnmt3a["mutated_samples"] == 47
    assert dnmt3a["mutation_rate"] == 24.35
    assert len(dnmt3a["features"]) == 22
    hotspot = dnmt3a["features"][dnmt3a["features"]["position"].eq(882)].iloc[0]
    assert hotspot["count"] == 27
    assert hotspot["is_hotspot"]

    assert rainfall["sample"] == "TCGA-A8-A08B"
    assert rainfall["reference_build"] == "hg38"
    assert len(rainfall["points"]) == 1890
    assert len(rainfall["change_points"]) == 7
    assert rainfall["y_max"] == 7.56
    assert {"chrom", "pos", "gene", "distance", "log10_distance", "con_class"} <= set(
        rainfall["points"]
    )
    assert {"chrom", "start", "end", "count", "mean_distance", "arrow_y"} <= set(
        rainfall["change_points"]
    )


def test_oncoprint_helpers_return_chart_ready_data() -> None:
    laml = laml_oncoplot_data()
    luad = luad_oncoprint_data()
    assert set(laml) == {
        "samples",
        "genes",
        "events",
        "grid",
        "sample_tmb",
        "gene_counts",
        "total_samples",
        "altered_samples",
        "tmb_limit",
        "count_limit",
        "sample_domain",
    }
    assert set(luad) == {
        "samples",
        "genes",
        "events",
        "grid",
        "sample_burden",
        "mutation_spectrum",
        "msi",
        "stage",
        "gene_counts",
        "heatmap_rows",
        "heatmap_cells",
        "sample_domain",
        "gene_order",
        "burden_limit",
        "spectrum_limit",
        "count_limit",
        "msi_limit",
    }
    coordinate_columns = {"x", "x0", "x1", "y", "y0", "y1"}
    laml_tables = (
        laml["samples"],
        laml["genes"],
        laml["events"],
        laml["grid"],
        laml["sample_tmb"],
        laml["gene_counts"],
    )
    luad_tables = (
        luad["samples"],
        luad["genes"],
        luad["sample_burden"],
        luad["mutation_spectrum"],
        luad["msi"],
        luad["stage"],
        luad["grid"],
        luad["events"],
        luad["gene_counts"],
        luad["heatmap_rows"],
        luad["heatmap_cells"],
    )

    assert laml["sample_domain"] == [-0.5, laml["total_samples"] - 0.5]
    assert laml["events"].shape == (247, 5)
    assert laml["grid"].shape == (1930, 4)
    assert all(coordinate_columns.isdisjoint(table.columns) for table in laml_tables)
    assert "count" in laml["sample_tmb"]
    assert "count" in laml["gene_counts"]
    assert laml["events"]["gene"].dtype.name == "category"
    assert luad["sample_domain"] == [
        -0.5,
        len(luad["samples"]["sample_order"].unique()) - 0.5,
    ]
    assert luad["events"].shape == (598, 5)
    assert luad["heatmap_cells"].shape == (2401, 7)
    assert all(coordinate_columns.isdisjoint(table.columns) for table in luad_tables)
    assert "count" in luad["sample_burden"]
    assert "count" in luad["mutation_spectrum"]
    assert "count" in luad["gene_counts"]
    assert "Missense Mutation (putative driver)" in set(luad["events"]["class"])
    assert (
        luad["sample_burden"].groupby("sample_order")["count"].sum().max()
        == (luad["burden_limit"])
    )
    assert (
        luad["mutation_spectrum"].groupby("sample_order")["count"].sum().max()
        == (luad["spectrum_limit"])
    )
    assert (
        luad["gene_counts"].groupby("gene", observed=True)["count"].sum().max()
        == (luad["count_limit"])
    )
    assert luad["grid"]["gene"].dtype.name == "category"


def test_laml_gene_order_breaks_sample_count_ties_alphabetically() -> None:
    genes = laml_oncoplot_data()["genes"]

    # NRAS and TP53 are altered in the same number of samples; an unstable sort
    # ordered them differently on other platforms.
    tied = genes.loc[genes["altered_samples"].eq(15), "gene"].tolist()
    assert tied == ["NRAS", "TP53"]
    assert genes["gene"].tolist() == [
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


def test_every_packaged_dataset_is_documented_or_explicitly_excluded() -> None:
    """A dataset reaches the docs only once its source and license are stated."""
    # These ship with the package but no documented example uses them, so they
    # carry no attribution in the docs.
    undocumented = {
        "mutation_impact_reference",
        "pik3ca_mutations",
        "tal1_alphagenome_reference",
        "tcga_oncoprint",
    }
    page = (Path(__file__).resolve().parents[1] / "docs" / "datasets.md").read_text(
        encoding="utf-8"
    )

    for name in available_datasets():
        if name in undocumented:
            assert f"`{name}`" not in page, f"{name} is documented but excluded"
            continue
        assert f"`{name}`" in page, f"{name} has no entry in docs/datasets.md"
