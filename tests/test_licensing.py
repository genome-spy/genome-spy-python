"""Keep third-party notices in the package's declared license files."""

from pathlib import Path
import hashlib
import tomllib

import pytest


@pytest.mark.parametrize(
    ("filename", "holder"),
    [
        ("ALTAIR-BSD-3-Clause.txt", "Vega-Altair Developers"),
        ("GENOMESPY-MIT.txt", "Kari Lavikka"),
        ("VEGA-LITE-BSD-3-Clause.txt", "University of Washington"),
        ("VEGA-BSD-3-Clause.txt", "University of Washington"),
        ("DATA-SOURCE-REPOSITORIES-MIT.txt", "Sahir Bhatnagar"),
        ("DATA-SOURCE-REPOSITORIES-MIT.txt", "Anand Mayakonda"),
        ("DATA-SOURCE-REPOSITORIES-MIT.txt", "Plotly Technologies Inc."),
    ],
)
def test_third_party_license_is_declared_for_distribution(filename, holder) -> None:
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    relative_path = f"LICENSES/{filename}"

    assert relative_path in project["license-files"]
    assert "THIRD_PARTY_NOTICES.md" in project["license-files"]
    text = (root / relative_path).read_text()
    assert holder in text
    assert "WARRANTIES" in text
    assert "Permission is hereby granted" in text or "Redistribution and use" in text


def test_license_metadata_includes_borrowed_materials() -> None:
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]

    assert set(project["license"].split(" AND ")) == {
        "MIT",
        "BSD-3-Clause",
        "CC-BY-4.0",
        "CC0-1.0",
        "CC-BY-NC-SA-4.0",
    }


# Keep published data identities aligned with the recorded provenance.
_AUDITED_DATA = {
    "airway_metadata.csv": "05bd7e78a0ca5b2a2f60ec715296381ca19f31a8c5a51e70c9f60583fa9fcf97",
    "airway_scaledcounts.csv": "4d34df15affa22fa5d5539874e148378ea18db1c9d731d175ef1b9f73cbc2927",
    "brca.maf.gz": "61d5355e960bd480bec4f245b8f096e2333408659ced0d196e42b0e38de3d724",
    "hapmap_gwas.csv": "20eb668da67431679afc1f9816a051f037c209b99027bcbb6c33019f006c6547",
    "mutation_impact_reference.json": "81e1d4bb5803e38228e80dbdaec8ff450ccccf9dc1c5ca1c97646dcd2688f048",
    "oncoprint_dataset3.json": "e07aa6ae9cf4f5f3a9f331d9979855ccf33bc47ed1bb2f4b871939b47c2a09ef",
    "p53_sequence_comparison_aligned.fasta.gz": "bfb9b427b31dba6d41095fca95aa6cd306f8caee9e9819254428f54407a08956",
    "pik3ca_mutations.json": "4f36df9ad960c1429827522bbd4fce0cb47520d14a5c642abe8a55969f177aec",
    "pik3ca_tcga_brca_lollipop.json": "3d13291134b4bd3af801848a8be384b08936fb99d2371b34fbe49df00e42e685",
    "refseq_gene_bodies.csv.gz": "6ecb8f12d120cc10724a816d4dc6f8ebdf5e468f725950809de5082f8db17785",
    "tal1_alphagenome_reference.json.gz": "10702eaaee63d2a4f600bf23ea4fac913db720aba56d33868b0f32590fc7b77e",
    "tcga.tsv": "39a90fc1f50ebcd113c37fd03894fb41b17dca4d6014f7efcf0e3f234c957742",
    "tcga_laml.maf.gz": "d102b071a052265b6f8ad7947bad1d58d3e3036fd17d6b274f7ea09a376cd6a0",
    "tcga_laml_annot.tsv": "7033030d52868e9a0f35ffd78f45a9d7a126c2edef90cf9e74e4f5d78990a710",
    "tcga_laml_combined_oncoplot.json.gz": "8e1cd49ea8e2f8f7b30b49d83b76aa6bd74a6a2c4d9b6cc95f04955b8916ef8a",
    "tcga_ov_gistic_lesions.tsv.gz": "ac2a6d445a4f085419987629e7fd63f77bbedfacb9e50c9f0c06b43ec50fd6e2",
    "tcga_ov_gistic_scores.tsv.gz": "6361638a2921cae4abd13956cd710035eb31f5cc0bfd554fe155f61f2a7883be",
}


def test_bundled_data_match_audited_inventory_and_have_notices() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "src/genome_spy/datasets/data"
    notices = (root / "THIRD_PARTY_NOTICES.md").read_text()

    assert {path.name for path in data.iterdir()} == _AUDITED_DATA.keys()
    for name, digest in _AUDITED_DATA.items():
        assert hashlib.sha256((data / name).read_bytes()).hexdigest() == digest, name
        assert f"`{name}`" in notices, name


def test_static_documentation_data_match_audited_package_files() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "docs/_static/data"

    for path in data.iterdir():
        if path.name == "README.md":
            continue
        assert path.name in _AUDITED_DATA, path.name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == _AUDITED_DATA[path.name]


@pytest.mark.parametrize(
    ("section", "source"),
    [
        ("## Airway data", "CC BY-NC-SA 4.0"),
        ("## Bundled TCGA example tables", "pyoncoprint"),
        ("## Bundled TCGA example tables", "Plotly"),
        ("## Bundled TCGA example tables", "maftools"),
        ("## Provider terms and scientific context", "ODbL"),
        ("## Provider terms and scientific context", "Broad GDAC"),
        ("## Provider terms and scientific context", "retracted in 2024"),
    ],
)
def test_public_notices_preserve_source_terms(section: str, source: str) -> None:
    root = Path(__file__).resolve().parents[1]
    notices = (root / "THIRD_PARTY_NOTICES.md").read_text()
    content = notices.split(section, 1)[1].split("\n## ", 1)[0]
    assert source in content


def test_every_license_text_is_declared_and_nonempty() -> None:
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]

    for path in (root / "LICENSES").iterdir():
        assert path.relative_to(root).as_posix() in project["license-files"]
        assert path.stat().st_size > 500
