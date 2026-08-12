from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture
def request_helpers() -> ModuleType:
    path = Path("notebooks/alphagenome/_alphagenome_request.py")
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load AlphaGenome request helpers from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


def test_reference_validation_uses_one_based_variant_position(
    request_helpers: ModuleType,
) -> None:
    interval = request_helpers.Interval("chr1", 100, 106)
    reference = request_helpers.ReferenceSlice(
        interval=interval,
        sequence="ACGTAC",
        assembly="GRCh38",
        checksum=hashlib.sha256(b"ACGTAC").hexdigest(),
    )
    request_helpers.validate_reference_allele(
        reference, request_helpers.Variant("chr1", 103, "G", "A")
    )

    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="mismatch"):
        request_helpers.validate_reference_allele(
            reference, request_helpers.Variant("chr1", 102, "G", "A")
        )

    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="checksum"):
        request_helpers.ReferenceSlice(
            interval=interval,
            sequence="ACGTAC",
            assembly="GRCh38",
            checksum="not-a-sha256",
        )


def test_request_key_is_stable_when_selector_order_changes(
    request_helpers: ModuleType,
) -> None:
    variant = request_helpers.Variant("chr1", 1_000_001, "c", "t")
    interval = request_helpers.centered_interval(variant)
    first = request_helpers.PredictionRequest(
        package_version="0.3.1",
        checkpoint_id="gtca/alphagenome_pytorch:model_all_folds.safetensors",
        organism="HOMO_SAPIENS",
        assembly="GRCh38",
        reference_checksum="reference-sha256",
        precision="mixed_precision",
        resolution=128,
        interval=interval,
        display_interval=interval,
        variant=variant,
        ontology_terms=("CL:0001059", "UBERON:0000178"),
        output_types=("RNA_SEQ", "DNASE"),
        selectors=("rna", "dnase"),
    )
    second = request_helpers.PredictionRequest(
        package_version="0.3.1",
        checkpoint_id="gtca/alphagenome_pytorch:model_all_folds.safetensors",
        organism="HOMO_SAPIENS",
        assembly="GRCh38",
        reference_checksum="reference-sha256",
        precision="mixed_precision",
        resolution=128,
        interval=interval,
        display_interval=interval,
        variant=variant,
        ontology_terms=("UBERON:0000178", "CL:0001059"),
        output_types=("DNASE", "RNA_SEQ"),
        selectors=("dnase", "rna"),
    )

    assert interval == request_helpers.Interval("chr1", 934_464, 1_065_536)
    assert variant.key == "chr1:1000001:C:T"
    assert first.request_id == second.request_id

    changed_reference = request_helpers.PredictionRequest(
        package_version=first.package_version,
        checkpoint_id=first.checkpoint_id,
        organism=first.organism,
        assembly=first.assembly,
        reference_checksum="different-reference-sha256",
        precision=first.precision,
        resolution=first.resolution,
        interval=first.interval,
        display_interval=first.display_interval,
        variant=first.variant,
        ontology_terms=first.ontology_terms,
        output_types=first.output_types,
        selectors=first.selectors,
    )
    assert changed_reference.request_id != first.request_id

    changed_fields = (
        replace(first, precision="full_float32"),
        replace(first, resolution=1),
        replace(
            first,
            display_interval=request_helpers.Interval(
                first.interval.chrom,
                first.interval.start0,
                first.interval.start0 + 1024,
            ),
        ),
        replace(first, selectors=("different-track",)),
    )
    assert all(request.request_id != first.request_id for request in changed_fields)


def test_request_rejects_variant_outside_model_interval(
    request_helpers: ModuleType,
) -> None:
    variant = request_helpers.Variant("chr1", 101, "A", "T")
    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="inside"):
        request_helpers.PredictionRequest(
            package_version="0.3.1",
            checkpoint_id="checkpoint",
            organism="HOMO_SAPIENS",
            assembly="GRCh38",
            reference_checksum="reference-sha256",
            precision="full_float32",
            resolution=128,
            interval=request_helpers.Interval("chr1", 200, 400),
            display_interval=request_helpers.Interval("chr1", 200, 400),
            variant=variant,
            ontology_terms=("CL:0001059",),
            output_types=("RNA_SEQ",),
            selectors=("rna",),
        )


def test_request_rejects_invalid_precision_and_display_interval(
    request_helpers: ModuleType,
) -> None:
    variant = request_helpers.Variant("chr1", 201, "A", "T")
    interval = request_helpers.Interval("chr1", 200, 400)
    common = {
        "package_version": "0.3.1",
        "checkpoint_id": "checkpoint",
        "organism": "HOMO_SAPIENS",
        "assembly": "GRCh38",
        "reference_checksum": "reference-sha256",
        "resolution": 128,
        "interval": interval,
        "variant": variant,
        "ontology_terms": ("CL:0001059",),
        "output_types": ("RNA_SEQ",),
        "selectors": ("rna",),
    }

    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="precision"):
        request_helpers.PredictionRequest(
            **common,
            precision="automatic",
            display_interval=interval,
        )
    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="Display"):
        request_helpers.PredictionRequest(
            **common,
            precision="full_float32",
            display_interval=request_helpers.Interval("chr1", 100, 300),
        )


def test_request_rejects_unchanged_alleles_and_reference_span_overflow(
    request_helpers: ModuleType,
) -> None:
    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="must differ"):
        request_helpers.Variant("chr1", 101, "A", "A")

    with pytest.raises(request_helpers.AlphaGenomeRequestError, match="inside"):
        request_helpers.PredictionRequest(
            package_version="0.3.1",
            checkpoint_id="checkpoint",
            organism="HOMO_SAPIENS",
            assembly="GRCh38",
            reference_checksum="reference-sha256",
            precision="full_float32",
            resolution=128,
            interval=request_helpers.Interval("chr1", 100, 102),
            display_interval=request_helpers.Interval("chr1", 100, 102),
            variant=request_helpers.Variant("chr1", 102, "AC", "T"),
            ontology_terms=("CL:0001059",),
            output_types=("RNA_SEQ",),
            selectors=("rna",),
        )
