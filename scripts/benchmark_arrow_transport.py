"""Compare Arrow IPC and JSON row payload sizes and encoding time."""

from __future__ import annotations

import json
import statistics
import time
from collections.abc import Callable

import genome_spy as gs
import polars as pl


def _frame(row_count: int) -> pl.DataFrame:
    """Build a deterministic genomics-shaped signal table."""
    return pl.DataFrame(
        {
            "position": range(row_count),
            "value": [(index % 97) / 97 for index in range(row_count)],
            "label": [f"bin-{index % 8}" for index in range(row_count)],
        }
    )


def _timed(callable_: Callable[[], bytes], repetitions: int = 5) -> tuple[int, float]:
    """Return the encoded byte count and median elapsed milliseconds."""
    samples: list[float] = []
    payload_size = 0
    for _ in range(repetitions):
        started = time.perf_counter()
        payload = callable_()
        samples.append((time.perf_counter() - started) * 1_000)
        payload_size = len(payload)
    return payload_size, statistics.median(samples)


def main() -> None:
    """Print a compact Arrow-versus-JSON transport comparison."""
    print("rows\tarrow_bytes\tjson_bytes\tarrow_ms\tjson_ms")
    for row_count in (8, 1_000, 10_000):
        frame = _frame(row_count)
        arrow_bytes, arrow_ms = _timed(lambda: gs.to_arrow_ipc(frame))
        json_bytes, json_ms = _timed(
            lambda: json.dumps(frame.to_dicts(), separators=(",", ":")).encode()
        )
        print(
            f"{row_count}\t{arrow_bytes}\t{json_bytes}\t{arrow_ms:.3f}\t{json_ms:.3f}"
        )


if __name__ == "__main__":
    main()
