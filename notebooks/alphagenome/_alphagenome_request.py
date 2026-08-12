"""Pure request and coordinate helpers for the optional AlphaGenome notebook.

The helper loads no model and reads no credentials. Its outputs are plain
Python values that the notebook can translate to a local inference backend.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


class AlphaGenomeRequestError(ValueError):
    """Raised when a proposed model request is not reproducible or valid."""


@dataclass(frozen=True, slots=True)
class Interval:
    """A zero-based, half-open genomic interval."""

    chrom: str
    start0: int
    end0: int

    def __post_init__(self) -> None:
        if not self.chrom:
            raise AlphaGenomeRequestError("Interval chromosome must not be empty.")
        if self.start0 < 0 or self.end0 <= self.start0:
            raise AlphaGenomeRequestError(
                "Interval must have non-negative start0 and end0 greater than start0."
            )


@dataclass(frozen=True, slots=True)
class Variant:
    """One normalized, one-based allele-specific variant."""

    chrom: str
    pos1: int
    ref: str
    alt: str

    def __post_init__(self) -> None:
        normalized_ref = self.ref.upper()
        normalized_alt = self.alt.upper()
        if not self.chrom or self.pos1 < 1:
            raise AlphaGenomeRequestError("Variant requires chrom and positive pos1.")
        if not normalized_ref or not normalized_alt:
            raise AlphaGenomeRequestError("Variant REF and ALT must not be empty.")
        allowed_bases = {"A", "C", "G", "T"}
        if not set(normalized_ref + normalized_alt) <= allowed_bases:
            raise AlphaGenomeRequestError(
                "Variant REF and ALT must contain only A/C/G/T."
            )
        if normalized_ref == normalized_alt:
            raise AlphaGenomeRequestError("Variant REF and ALT must differ.")
        object.__setattr__(self, "ref", normalized_ref)
        object.__setattr__(self, "alt", normalized_alt)

    @property
    def start0(self) -> int:
        """Zero-based first reference base consumed by this variant."""
        return self.pos1 - 1

    @property
    def key(self) -> str:
        """Canonical allele-specific identifier."""
        return f"{self.chrom}:{self.pos1}:{self.ref}:{self.alt}"


@dataclass(frozen=True, slots=True)
class ReferenceSlice:
    """A contiguous reference sequence over a zero-based, half-open interval."""

    interval: Interval
    sequence: str
    assembly: str
    checksum: str

    def __post_init__(self) -> None:
        normalized = self.sequence.upper()
        if len(normalized) != self.interval.end0 - self.interval.start0:
            raise AlphaGenomeRequestError(
                "Reference sequence length must equal its interval width."
            )
        if not set(normalized) <= {"A", "C", "G", "T", "N"}:
            raise AlphaGenomeRequestError(
                "Reference sequence contains an invalid base."
            )
        if not self.assembly:
            raise AlphaGenomeRequestError("Reference assembly is required.")
        expected_checksum = hashlib.sha256(normalized.encode()).hexdigest()
        if self.checksum != expected_checksum:
            raise AlphaGenomeRequestError(
                "Reference checksum does not match its sequence."
            )
        object.__setattr__(self, "sequence", normalized)


@dataclass(frozen=True, slots=True)
class PredictionRequest:
    """Pinned model inputs used for one explicit prediction submission."""

    package_version: str
    checkpoint_id: str
    organism: str
    assembly: str
    reference_checksum: str
    precision: str
    resolution: int
    interval: Interval
    display_interval: Interval
    variant: Variant
    ontology_terms: tuple[str, ...]
    output_types: tuple[str, ...]
    selectors: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.package_version
            or not self.checkpoint_id
            or not self.organism
            or not self.assembly
            or not self.reference_checksum
            or not self.precision
        ):
            raise AlphaGenomeRequestError(
                "Package version, checkpoint ID, organism, assembly, reference "
                "checksum, and precision are required."
            )
        if self.resolution <= 0:
            raise AlphaGenomeRequestError("Prediction resolution must be positive.")
        if self.precision not in {"full_float32", "mixed_precision"}:
            raise AlphaGenomeRequestError(
                f"Unsupported prediction precision: {self.precision!r}."
            )
        if not self.ontology_terms or not self.output_types or not self.selectors:
            raise AlphaGenomeRequestError(
                "At least one ontology term, output type, and selector are required."
            )
        if self.interval.chrom != self.variant.chrom:
            raise AlphaGenomeRequestError(
                "Variant chromosome must match the input interval."
            )
        if not (
            self.interval.start0
            <= self.variant.start0
            < self.variant.start0 + len(self.variant.ref)
            <= self.interval.end0
        ):
            raise AlphaGenomeRequestError(
                "Variant position must fall inside the input interval."
            )
        if (
            self.display_interval.chrom != self.interval.chrom
            or self.display_interval.start0 < self.interval.start0
            or self.display_interval.end0 > self.interval.end0
        ):
            raise AlphaGenomeRequestError(
                "Display interval must fall inside the model interval."
            )

    @property
    def request_id(self) -> str:
        """Stable cache key independent of selector ordering."""
        payload = {
            "assembly": self.assembly,
            "package_version": self.package_version,
            "interval": [self.interval.chrom, self.interval.start0, self.interval.end0],
            "checkpoint_id": self.checkpoint_id,
            "display_interval": [
                self.display_interval.chrom,
                self.display_interval.start0,
                self.display_interval.end0,
            ],
            "ontology_terms": sorted(set(self.ontology_terms)),
            "organism": self.organism,
            "output_types": sorted(set(self.output_types)),
            "precision": self.precision,
            "reference_checksum": self.reference_checksum,
            "resolution": self.resolution,
            "selectors": sorted(set(self.selectors)),
            "variant": self.variant.key,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode()).hexdigest()


def centered_interval(variant: Variant, *, width: int = 131_072) -> Interval:
    """Return the fixed-width, zero-based model context centered on a variant."""
    if width <= 0 or width % 2:
        raise AlphaGenomeRequestError(
            "Model interval width must be a positive even integer."
        )
    start0 = variant.start0 - width // 2
    if start0 < 0:
        raise AlphaGenomeRequestError(
            "Centered model interval would extend before the chromosome start."
        )
    return Interval(variant.chrom, start0, start0 + width)


def validate_reference_allele(reference: ReferenceSlice, variant: Variant) -> None:
    """Raise unless the slice's zero-based bases exactly match variant REF."""
    if reference.interval.chrom != variant.chrom:
        raise AlphaGenomeRequestError("Reference slice and variant chromosomes differ.")
    start0 = variant.start0
    end0 = start0 + len(variant.ref)
    if start0 < reference.interval.start0 or end0 > reference.interval.end0:
        raise AlphaGenomeRequestError(
            "Variant REF falls outside the packaged reference slice."
        )
    offset = start0 - reference.interval.start0
    observed = reference.sequence[offset : offset + len(variant.ref)]
    if observed != variant.ref:
        raise AlphaGenomeRequestError(
            f"Reference mismatch at {variant.key}: slice contains {observed!r}."
        )
