"""Pure interaction helpers for the AlphaGenome Marimo example."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

BASES = ("A", "C", "G", "T")


def allele_click_submission(
    clicked: Mapping[str, Any],
    click_revision: int,
    variants: Sequence[Mapping[str, Any]],
) -> dict[str, Any] | None:
    """Apply one allele-grid click to the designed sequence."""
    if (
        clicked.get("interaction_kind") != "allele_choice"
        or clicked.get("pos1") != clicked.get("pos0", -2) + 1
        or clicked.get("reference") not in BASES
        or clicked.get("allele") not in BASES
    ):
        return None

    key = (str(clicked["chrom"]), int(clicked["pos0"]))
    by_position = {
        (str(variant["chrom"]), int(variant["pos0"])): dict(variant)
        for variant in variants
    }
    if clicked["allele"] == clicked["reference"]:
        by_position.pop(key, None)
    else:
        by_position[key] = {
            "chrom": key[0],
            "pos0": key[1],
            "pos1": int(clicked["pos1"]),
            "reference": str(clicked["reference"]),
            "alternate": str(clicked["allele"]),
        }

    updated = tuple(by_position[key] for key in sorted(by_position))
    if updated == tuple(variants):
        return None
    return {"click_revision": click_revision, "variants": updated}


def prediction_input_key(
    variants: Sequence[Mapping[str, Any]],
    checkpoint: str,
    device: str,
    precision: str,
) -> tuple[Any, ...]:
    """Return the inputs that determine whether a displayed result is current."""
    variant_key = tuple(
        (
            variant["chrom"],
            variant["pos1"],
            variant["reference"],
            variant["alternate"],
        )
        for variant in variants
    )
    return (
        variant_key,
        checkpoint.strip() or "pinned-checkpoint",
        device,
        precision,
    )


def prediction_display_state(
    prediction: Mapping[str, Any], pending_input_key: tuple[Any, ...]
) -> tuple[str, str]:
    """Return a user-facing status while retaining stale successful output."""
    if (
        prediction["status"] == "succeeded"
        and prediction["frame"] is not None
        and prediction["input_key"] != pending_input_key
    ):
        return "stale", "The previous model result remains visible."
    return str(prediction["status"]), str(prediction["message"])


def should_run_submission(
    submission: Mapping[str, Any] | None, prediction: Mapping[str, Any]
) -> bool:
    """Return whether an edit revision still needs one prediction attempt."""
    return (
        submission is not None
        and bool(submission["variants"])
        and submission["click_revision"] != prediction["click_revision"]
    )
