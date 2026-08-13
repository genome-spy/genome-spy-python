"""Pure interaction helpers for the AlphaGenome Marimo example."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

BASES = ("A", "C", "G", "T")


def alternate_options(reference: str) -> tuple[str, ...]:
    """Return valid single-base alternates in a stable order."""
    return tuple(base for base in BASES if base != reference)


def sequence_click_submission(
    clicked: Mapping[str, Any], click_revision: int, alternate: str
) -> dict[str, Any] | None:
    """Build a prediction submission from a valid sequence-base click."""
    if (
        clicked.get("interaction_kind") != "sequence_base"
        or clicked.get("pos1") != clicked.get("pos0", -2) + 1
        or clicked.get("base") not in BASES
    ):
        return None
    selection = {
        "chrom": clicked["chrom"],
        "pos0": clicked["pos0"],
        "pos1": clicked["pos1"],
        "base": clicked["base"],
    }
    reconciled_alternate = alternate
    if reconciled_alternate == selection["base"]:
        reconciled_alternate = alternate_options(selection["base"])[0]
    return {
        "click_revision": click_revision,
        "selection": selection,
        "alternate": reconciled_alternate,
    }


def prediction_input_key(
    selection: Mapping[str, Any],
    alternate: str,
    checkpoint: str,
    device: str,
    precision: str,
) -> tuple[Any, ...]:
    """Return the inputs that determine whether a displayed result is current."""
    return (
        selection["chrom"],
        selection["pos1"],
        selection["base"],
        alternate,
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
        return "stale", "Inputs changed; the previous model result remains visible."
    return str(prediction["status"]), str(prediction["message"])


def should_run_submission(
    submission: Mapping[str, Any] | None, prediction: Mapping[str, Any]
) -> bool:
    """Return whether a click revision still needs one prediction attempt."""
    return (
        submission is not None
        and submission["click_revision"] != prediction["click_revision"]
    )
