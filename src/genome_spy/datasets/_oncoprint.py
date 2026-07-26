"""Prepared cohort tables used by oncoprint examples."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


@dataclass(frozen=True, slots=True)
class LuadOncoprintData:
    """Chart-ready tables and domains for the TCGA LUAD oncoprint."""

    title: str
    samples: pd.DataFrame
    genes: pd.DataFrame
    sample_burden: pd.DataFrame
    mutation_spectrum: pd.DataFrame
    msi: pd.DataFrame
    stage: pd.DataFrame
    grid: pd.DataFrame
    full_rect_events: pd.DataFrame
    half_rect_events: pd.DataFrame
    triangle_events: pd.DataFrame
    star_events: pd.DataFrame
    gene_counts: pd.DataFrame
    count_grid: pd.DataFrame
    percent_labels: pd.DataFrame
    heatmap_rows: pd.DataFrame
    heatmap_cells: pd.DataFrame
    sample_domain: list[int]
    gene_order: list[str]
    burden_limit: int
    spectrum_limit: int
    count_limit: int
    msi_limit: float


@dataclass(frozen=True, slots=True)
class LamlOncoplotData:
    """Chart-ready tables and summary values for the TCGA LAML oncoplot."""

    samples: pd.DataFrame
    genes: pd.DataFrame
    matrix: pd.DataFrame
    grid: pd.DataFrame
    sample_tmb: pd.DataFrame
    gene_counts: pd.DataFrame
    percent_labels: pd.DataFrame
    count_grid: pd.DataFrame
    total_samples: int
    altered_samples: int
    tmb_limit: int
    count_limit: int
    sample_domain: list[int]


def laml_oncoplot_data() -> LamlOncoplotData:
    """Prepare the packaged TCGA LAML oncoplot tables for visualization.

    Returns:
        A chart-ready collection of aligned tables and plotting domains.

    Raises:
        ImportError: If pandas is not installed.
    """
    import pandas as pd

    payload = cast(
        dict[str, Any], load_dataset("tcga_laml_oncoprint", as_format="json")
    )
    samples = pd.DataFrame(payload["samples"]).sort_values("sample_order")
    genes = pd.DataFrame(payload["genes"]).sort_values("gene_order")
    matrix = pd.DataFrame(payload["matrix"])
    grid = pd.DataFrame(payload["grid"])
    sample_tmb = pd.DataFrame(payload["sample_tmb"])
    gene_counts = pd.DataFrame(payload["gene_counts"])
    percent_labels = pd.DataFrame(payload["percent_labels"])

    sample_order = samples["sample"].tolist()
    gene_order = genes["gene"].tolist()
    for frame in [samples, matrix, grid, sample_tmb]:
        frame["sample"] = pd.Categorical(
            frame["sample"], categories=sample_order, ordered=True
        )
        frame["x0"] = frame["sample_order"]
        frame["x1"] = frame["sample_order"] + 1
    for frame in [genes, matrix, grid, gene_counts, percent_labels]:
        frame["gene"] = pd.Categorical(
            frame["gene"], categories=gene_order, ordered=True
        )

    genes["zero"] = 0
    percent_labels["x"] = 0
    count_limit = int(genes["altered_samples"].max())
    count_grid = genes[["gene"]].copy()
    count_grid["x0"] = 0
    count_grid["x1"] = count_limit

    return LamlOncoplotData(
        samples=samples,
        genes=genes,
        matrix=matrix,
        grid=grid,
        sample_tmb=sample_tmb,
        gene_counts=gene_counts,
        percent_labels=percent_labels,
        count_grid=count_grid,
        total_samples=int(payload["total_samples"]),
        altered_samples=int(payload["altered_samples"]),
        tmb_limit=int(samples["tmb_total"].max()),
        count_limit=count_limit,
        sample_domain=[0, len(sample_order)],
    )


def luad_oncoprint_data() -> LuadOncoprintData:
    """Prepare the packaged TCGA LUAD oncoprint tables for visualization.

    Returns:
        A chart-ready collection of aligned tables, categorical orders, and
        plotting domains.

    Raises:
        ImportError: If pandas is not installed.
    """
    import pandas as pd

    payload = cast(
        dict[str, Any], load_dataset("tcga_luad_oncoprint", as_format="json")
    )
    frames = {
        name: pd.DataFrame(payload[name])
        for name in (
            "samples",
            "genes",
            "sample_burden",
            "mutation_spectrum",
            "msi",
            "stage",
            "grid",
            "full_rect_events",
            "half_rect_events",
            "triangle_events",
            "star_events",
            "gene_counts",
            "percent_labels",
            "heatmap_rows",
            "heatmap_cells",
        )
    }
    event_frames = [
        frames["full_rect_events"],
        frames["half_rect_events"],
        frames["triangle_events"],
        frames["star_events"],
    ]
    active_orders = sorted(
        pd.concat([frame["sample_order"] for frame in event_frames])
        .drop_duplicates()
        .astype(int)
        .tolist()
    )
    order_map = {old: new for new, old in enumerate(active_orders)}

    def align_samples(frame: pd.DataFrame) -> pd.DataFrame:
        aligned = frame[frame["sample_order"].isin(order_map)].copy()
        aligned["sample_order"] = aligned["sample_order"].map(order_map)
        aligned["x0"] = aligned["sample_order"]
        aligned["x1"] = aligned["sample_order"] + 1
        return aligned

    for name in (
        "samples",
        "sample_burden",
        "mutation_spectrum",
        "msi",
        "stage",
        "grid",
        "full_rect_events",
        "half_rect_events",
        "triangle_events",
        "star_events",
        "heatmap_cells",
    ):
        frames[name] = align_samples(frames[name])

    gene_order = frames["genes"].sort_values("gene_order")["gene"].tolist()
    frames["percent_labels"]["x"] = 1
    frames["msi"]["y0"] = 0.0
    frames["stage"]["y0"] = 0.0
    frames["stage"]["y1"] = 1.0
    frames["grid"]["gene"] = frames["grid"]["gene_order"].map(
        dict(enumerate(gene_order))
    )

    for frame_name in (
        "genes",
        "grid",
        "full_rect_events",
        "half_rect_events",
        "triangle_events",
        "star_events",
        "percent_labels",
        "gene_counts",
    ):
        frames[frame_name]["gene"] = pd.Categorical(
            frames[frame_name]["gene"], categories=gene_order, ordered=True
        )

    count_limit = int(payload["max_gene_count"])
    count_grid = frames["genes"][["gene"]].copy()
    count_grid["x0"] = 0
    count_grid["x1"] = count_limit

    return LuadOncoprintData(
        title=str(payload["title"]),
        **frames,
        count_grid=count_grid,
        sample_domain=[0, len(active_orders)],
        gene_order=gene_order,
        burden_limit=int(payload["max_sample_burden"]),
        spectrum_limit=int(payload["max_mutation_spectrum"]),
        count_limit=count_limit,
        msi_limit=float(payload["msi_max"]),
    )
