"""Wrangle the packaged MAF and pyoncoprint tables for oncoprints.

The source files are deliberately kept in their upstream tabular form.  The
functions below only add the ordering, aggregation, and display fields that the
GenomeSpy examples need.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

import numpy as np

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd


_NON_SYNONYMOUS_CLASSES = (
    "Frame_Shift_Del",
    "Frame_Shift_Ins",
    "Splice_Site",
    "Translation_Start_Site",
    "Nonsense_Mutation",
    "Nonstop_Mutation",
    "In_Frame_Del",
    "In_Frame_Ins",
    "Missense_Mutation",
)

_LUAD_REPLACEMENTS = {
    "amp_rec": "Amplification",
    "homdel_rec": "Deep Deletion",
    "splice": "Splice Mutation (putative driver)",
    "splice_rec": "Splice Mutation (putative passenger)",
    "sv": "Structural Variant (putative driver)",
    "sv_rec": "Structural Variant (putative passenger)",
}

_LUAD_MUTATION_CLASSES = (
    "Amplification",
    "Deep Deletion",
    "Splice Mutation (putative driver)",
    "Splice Mutation (putative passenger)",
    "Structural Variant (putative driver)",
    "Structural Variant (putative passenger)",
    "Inframe Mutation (putative driver)",
    "Missense Mutation (putative driver)",
    "Missense Mutation (putative passenger)",
    "Truncating mutation (putative driver)",
    "Truncating mutation (putative passenger)",
)

_LUAD_HEATMAP_GROUPS = (
    "mRNA expression z-scores relative to diploid samples (RNA Seq V2 RSEM)",
    "Methylation (HM27 and HM450 merge)",
    "Microbiome Signatures (log RNA Seq CPM)",
)
_LUAD_HEATMAP_GROUP_ORDER = dict(zip(_LUAD_HEATMAP_GROUPS, range(3), strict=True))


class LamlOncoplotData(TypedDict):
    """Chart tables and limits returned for the LAML oncoplot."""

    samples: pd.DataFrame
    genes: pd.DataFrame
    events: pd.DataFrame
    grid: pd.DataFrame
    sample_tmb: pd.DataFrame
    gene_counts: pd.DataFrame
    total_samples: int
    altered_samples: int
    tmb_limit: int
    count_limit: int
    sample_domain: list[float]


class LuadOncoprintData(TypedDict):
    """Chart tables and limits returned for the LUAD oncoprint."""

    samples: pd.DataFrame
    genes: pd.DataFrame
    events: pd.DataFrame
    grid: pd.DataFrame
    sample_burden: pd.DataFrame
    mutation_spectrum: pd.DataFrame
    msi: pd.DataFrame
    stage: pd.DataFrame
    gene_counts: pd.DataFrame
    heatmap_rows: pd.DataFrame
    heatmap_cells: pd.DataFrame
    sample_domain: list[float]
    gene_order: list[str]
    burden_limit: int
    spectrum_limit: int
    count_limit: int
    msi_limit: float


def laml_oncoplot_data() -> LamlOncoplotData:
    """Prepare the TCGA LAML MAF for the oncoplot example.

    Description:
        Loads the 2,207-row TCGA LAML MAF and keeps the nine nonsynonymous
        ``Variant_Classification`` values used by the canonical maftools plot.
        The ten genes with the most altered samples are selected, samples are
        sorted by their gene-presence pattern, and repeated calls for one
        sample/gene pair are displayed as ``Multi_Hit``.  The returned tables
        are the mutation matrix, sample burden, gene counts, and their drawing
        grid; ``genes`` also contains the percentage label used by the chart.

    Returns:
        A mapping of chart table names to DataFrames and scalar display limits.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> data = laml_oncoplot_data()
        >>> data["events"].head()
    """
    import pandas as pd

    maf = load_dataset("tcga_laml_maf", as_format="dataframe")
    annotations = load_dataset("tcga_laml_annotations", as_format="dataframe")

    # The maftools oncoplot excludes silent and non-coding calls.
    variants = maf.loc[
        maf["Variant_Classification"].isin(_NON_SYNONYMOUS_CLASSES)
    ].copy()
    # A stable sort keeps the alphabetical groupby order among genes with the
    # same sample count, so the top-ten selection is reproducible.
    altered_by_gene = (
        variants.groupby("Hugo_Symbol")["Tumor_Sample_Barcode"]
        .nunique()
        .sort_values(ascending=False, kind="stable")
    )
    gene_order = altered_by_gene.head(10).index.tolist()
    top_variants = variants[variants["Hugo_Symbol"].isin(gene_order)].copy()

    # Sort samples by the presence pattern of the selected genes, then append
    # samples with no selected-gene calls in their original MAF order.
    presence = (
        top_variants.assign(_present=1)
        .pivot_table(
            index="Tumor_Sample_Barcode",
            columns="Hugo_Symbol",
            values="_present",
            aggfunc="max",
            fill_value=0,
        )
        .reindex(columns=gene_order)
    )
    sample_order = presence.sort_values(
        gene_order,
        ascending=[False] * len(gene_order),
        kind="stable",
    ).index.tolist()
    all_samples = maf["Tumor_Sample_Barcode"].drop_duplicates().tolist()
    sample_order.extend(sample for sample in all_samples if sample not in sample_order)
    sample_positions = {sample: index for index, sample in enumerate(sample_order)}
    gene_positions = {gene: index for index, gene in enumerate(gene_order)}

    # Aggregate repeated calls without a row-wise Python loop.
    events = (
        top_variants.groupby(["Tumor_Sample_Barcode", "Hugo_Symbol"], sort=False)
        .agg(
            hit_count=("Variant_Classification", "size"),
            first_class=("Variant_Classification", "first"),
        )
        .reset_index()
        .rename(
            columns={
                "Tumor_Sample_Barcode": "sample",
                "Hugo_Symbol": "gene",
            }
        )
    )
    events["class"] = events["first_class"].where(
        events["hit_count"].eq(1), "Multi_Hit"
    )
    events = events.drop(columns=["hit_count", "first_class"])
    events["sample_order"] = events["sample"].map(sample_positions)
    events["gene_order"] = events["gene"].map(gene_positions)

    annotation_lookup = annotations.set_index("Tumor_Sample_Barcode")
    sample_top_gene_counts = events.groupby("sample")["gene"].nunique()
    tmb_totals = variants.groupby("Tumor_Sample_Barcode").size()
    samples = pd.DataFrame({"sample": sample_order})
    samples["sample_order"] = range(len(samples))
    samples["fab_classification"] = (
        samples["sample"].map(annotation_lookup["FAB_classification"]).fillna("NA")
    )
    samples["altered_genes"] = (
        samples["sample"].map(sample_top_gene_counts).fillna(0).astype(int)
    )
    samples["tmb_total"] = samples["sample"].map(tmb_totals).fillna(0).astype(int)

    mutation_events = top_variants.groupby("Hugo_Symbol").size()
    genes = pd.DataFrame({"gene": gene_order})
    genes["gene_order"] = genes["gene"].map(gene_positions)
    genes["altered_samples"] = genes["gene"].map(altered_by_gene).astype(int)
    genes["mutation_events"] = genes["gene"].map(mutation_events).astype(int)
    genes["percent_altered"] = (
        (genes["altered_samples"] / len(sample_order) * 100).round().astype(int)
    )
    genes["label"] = genes["percent_altered"].map(lambda value: f"{value}%")

    grid = _sample_gene_grid(sample_order, gene_order, sample_positions, gene_positions)
    sample_tmb = (
        variants.groupby(["Tumor_Sample_Barcode", "Variant_Classification"], sort=False)
        .size()
        .reset_index(name="count")
        .rename(
            columns={
                "Tumor_Sample_Barcode": "sample",
                "Variant_Classification": "class",
            }
        )
    )
    sample_tmb["sample_order"] = sample_tmb["sample"].map(sample_positions)
    gene_counts = (
        events.groupby(["gene", "gene_order", "class"], sort=False)
        .size()
        .reset_index(name="count")
    )

    sample_categories = pd.CategoricalDtype(sample_order, ordered=True)
    gene_categories = pd.CategoricalDtype(gene_order, ordered=True)
    for frame in (samples, events, grid, sample_tmb):
        frame["sample"] = frame["sample"].astype(sample_categories)
    for frame in (genes, events, grid, gene_counts):
        frame["gene"] = frame["gene"].astype(gene_categories)

    count_limit = int(genes["altered_samples"].max())
    return {
        "samples": samples,
        "genes": genes,
        "events": events,
        "grid": grid,
        "sample_tmb": sample_tmb,
        "gene_counts": gene_counts,
        "total_samples": len(samples),
        "altered_samples": int(samples["altered_genes"].gt(0).sum()),
        "tmb_limit": int(samples["tmb_total"].max()),
        "count_limit": count_limit,
        "sample_domain": [-0.5, len(sample_order) - 0.5],
    }


def luad_oncoprint_data() -> LuadOncoprintData:
    """Prepare the pyoncoprint TCGA LUAD table for visualization.

    Description:
        Loads the wide ``tcga.tsv`` example table (145 tracks and 507 sample
        columns). Recurrence tracks are melted and combined by gene/sample,
        abbreviations are expanded to the display classes used by the example,
        genes and samples are ranked by recurrence, and the clinical and
        heatmap tracks are reshaped into long chart tables. The returned event
        table contains every mutation class; the example filters it into the
        rectangle and star layers at render time.

    Returns:
        A mapping of chart table names to DataFrames and scalar display limits.

    Raises:
        ImportError: If pandas is not installed.

    Example:
        >>> data = luad_oncoprint_data()
        >>> data["events"].head()
    """
    import pandas as pd

    source = load_dataset("pyoncoprint_tcga", as_format="dataframe")
    sample_columns = source.columns[2:].tolist()
    recurrence_rows = source.loc[
        source["track_type"].isin(
            ["MUTATIONS", "CNA", "STRUCTURAL_VARIANT", "PROTEIN", "MRNA"]
        )
    ].copy()
    recurrence_rows.loc[:, sample_columns] = recurrence_rows[sample_columns].replace(
        _LUAD_REPLACEMENTS
    )

    # Melt the source's repeated gene rows, then retain source order while
    # joining multiple alteration tracks into one cell per gene/sample.
    recurrence_long = recurrence_rows.melt(
        id_vars=["track_name", "track_type"],
        value_vars=sample_columns,
        var_name="sample",
        value_name="class",
    ).dropna(subset=["class"])
    recurrence_long["class"] = recurrence_long["class"].astype(str)
    recurrence_long = recurrence_long[recurrence_long["class"].ne("")].copy()
    recurrence = (
        recurrence_long.groupby(["track_name", "sample"], sort=False)["class"]
        .agg(",".join)
        .unstack(fill_value="")
        .reindex(columns=sample_columns, fill_value="")
    )

    # Gene ranking counts each distinct alteration class once per gene/sample.
    score_rows = (
        recurrence.rename_axis("gene")
        .reset_index()
        .melt(id_vars="gene", var_name="sample", value_name="classes")
    )
    score_rows["class"] = score_rows["classes"].str.split(",")
    score_rows = score_rows.explode("class")
    score_rows = score_rows[score_rows["class"].ne("")].drop_duplicates(
        ["gene", "sample", "class"]
    )
    gene_scores = (
        score_rows.groupby("gene").size().reindex(recurrence.index, fill_value=0)
    )
    # Negate instead of reversing so that ties keep their input order.
    gene_order = gene_scores.index[
        np.argsort(-gene_scores.to_numpy(), kind="stable")
    ].tolist()
    recurrence = recurrence.reindex(gene_order)

    mutation_weights = {
        mutation_class: weight
        for weight, mutation_class in enumerate(
            reversed(_LUAD_MUTATION_CLASSES), start=1
        )
    }
    weighted_events = score_rows[
        score_rows["class"].isin(_LUAD_MUTATION_CLASSES)
    ].copy()
    weighted_events["weight"] = weighted_events["class"].map(mutation_weights)
    weighted = (
        weighted_events.pivot_table(
            index="gene",
            columns="sample",
            values="weight",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(index=gene_order[::-1], columns=sample_columns, fill_value=0)
        .to_numpy()
    )
    # np.lexsort uses the final row as the primary key; reversing the gene
    # order makes the highest-ranked gene the primary sample-sorting key.
    sorted_sample_indices = np.lexsort(weighted)[::-1]
    sorted_samples = np.asarray(sample_columns)[sorted_sample_indices].tolist()

    events = weighted_events[["gene", "sample", "class"]].copy()
    old_sample_positions = {
        sample: index for index, sample in enumerate(sorted_samples)
    }
    events["old_sample_order"] = events["sample"].map(old_sample_positions)
    events["gene_order"] = events["gene"].map(
        {gene: index for index, gene in enumerate(gene_order)}
    )
    active_old_orders = sorted(events["old_sample_order"].unique())
    active_samples = [sorted_samples[index] for index in active_old_orders]
    old_to_new = {old: new for new, old in enumerate(active_old_orders)}
    sample_positions = {sample: index for index, sample in enumerate(active_samples)}
    events = events[events["sample"].isin(active_samples)].copy()
    events["sample_order"] = events["old_sample_order"].map(old_to_new)
    events = events.drop(columns="old_sample_order")

    sample_burden = (
        events.groupby(["sample", "sample_order", "class"], sort=False)
        .size()
        .reset_index(name="count")
    )
    gene_counts = (
        events.groupby(["gene", "gene_order", "class"], sort=False)
        .size()
        .reset_index(name="count")
    )
    altered_by_gene = events.groupby("gene")["sample"].nunique()

    samples = pd.DataFrame(
        {"sample": active_samples, "sample_order": range(len(active_samples))}
    )
    genes = pd.DataFrame(
        {
            "gene": gene_order,
            "gene_order": range(len(gene_order)),
            "altered_samples": [
                int(altered_by_gene.get(gene, 0)) for gene in gene_order
            ],
        }
    )
    genes["label"] = genes["altered_samples"].map(
        lambda count: f"{round(count / len(sample_columns) * 100)}%"
    )
    grid = _sample_gene_grid(
        active_samples,
        gene_order,
        sample_positions,
        {gene: index for index, gene in enumerate(gene_order)},
    )

    clinical = source[source["track_type"].eq("CLINICAL")].copy()
    spectrum_source = clinical[
        clinical["track_name"].str.startswith("Mutation spectrum")
    ].copy()
    spectrum_source["class"] = spectrum_source["track_name"].str.extract(r"\(([^)]+)\)")
    mutation_spectrum = (
        spectrum_source.drop(columns=["track_name", "track_type"])
        .set_index("class")
        .T.rename_axis("sample")
        .reset_index()
        .melt(id_vars="sample", var_name="class", value_name="count")
        .dropna(subset=["count"])
    )
    mutation_spectrum["count"] = mutation_spectrum["count"].astype(int)
    mutation_spectrum = mutation_spectrum[
        mutation_spectrum["sample"].isin(active_samples)
        & mutation_spectrum["count"].gt(0)
    ].copy()
    mutation_spectrum["sample_order"] = mutation_spectrum["sample"].map(
        sample_positions
    )
    mutation_spectrum = mutation_spectrum.sort_values(
        ["sample_order", "class"], kind="stable"
    )

    clinical_tracks = clinical.set_index("track_name")

    def clinical_track(name: str, value_name: str) -> pd.DataFrame:
        row = clinical_tracks.loc[name, sample_columns]
        frame = row.rename(value_name).rename_axis("sample").reset_index()
        frame = frame[frame["sample"].isin(active_samples)].copy()
        frame["sample_order"] = frame["sample"].map(sample_positions)
        return frame.sort_values("sample_order")

    msi = clinical_track("MSI MANTIS Score", "value")
    msi["value"] = msi["value"].fillna(0).astype(float)
    stage = clinical_track(
        "American Joint Committee on Cancer Tumor Stage Code", "stage"
    )

    heatmap_source = source[source["track_type"].str.startswith("HEATMAP")].copy()
    heatmap_source["group"] = np.select(
        [
            heatmap_source["track_type"].eq("HEATMAP MRNA_EXPRESSION Z-SCORE"),
            heatmap_source["track_name"].eq("Dicipivirus"),
        ],
        [_LUAD_HEATMAP_GROUPS[0], _LUAD_HEATMAP_GROUPS[2]],
        default=_LUAD_HEATMAP_GROUPS[1],
    )
    heatmap_source["group_order"] = heatmap_source["group"].map(
        _LUAD_HEATMAP_GROUP_ORDER
    )
    heatmap_source["track_order"] = heatmap_source.groupby(
        "group", sort=False
    ).cumcount()
    heatmap_rows = heatmap_source[
        ["group", "group_order", "track_name", "track_order"]
    ].rename(columns={"track_name": "track"})
    heatmap_cells = (
        heatmap_source.melt(
            id_vars=["group", "group_order", "track_name", "track_order"],
            value_vars=sample_columns,
            var_name="sample",
            value_name="value",
        )
        .loc[lambda frame: frame["sample"].isin(active_samples)]
        .assign(value=lambda frame: pd.to_numeric(frame["value"], errors="coerce"))
        .rename(columns={"track_name": "track"})
    )
    heatmap_cells["sample_order"] = heatmap_cells["sample"].map(sample_positions)
    heatmap_cells = heatmap_cells[
        [
            "group",
            "group_order",
            "track",
            "track_order",
            "sample",
            "sample_order",
            "value",
        ]
    ]

    gene_categories = pd.CategoricalDtype(gene_order, ordered=True)
    for frame in (genes, events, grid, gene_counts):
        frame["gene"] = frame["gene"].astype(gene_categories)

    burden_limit = int(sample_burden.groupby("sample_order")["count"].sum().max())
    spectrum_limit = int(mutation_spectrum.groupby("sample_order")["count"].sum().max())
    count_limit = int(gene_counts.groupby("gene", observed=True)["count"].sum().max())
    return {
        "samples": samples,
        "genes": genes,
        "events": events,
        "grid": grid,
        "sample_burden": sample_burden,
        "mutation_spectrum": mutation_spectrum,
        "msi": msi,
        "stage": stage,
        "gene_counts": gene_counts,
        "heatmap_rows": heatmap_rows,
        "heatmap_cells": heatmap_cells,
        "sample_domain": [-0.5, len(active_samples) - 0.5],
        "gene_order": gene_order,
        "burden_limit": burden_limit,
        "spectrum_limit": spectrum_limit,
        "count_limit": count_limit,
        "msi_limit": float(msi["value"].max()),
    }


def _sample_gene_grid(
    samples: list[str],
    genes: list[str],
    sample_positions: dict[str, int],
    gene_positions: dict[str, int],
) -> pd.DataFrame:
    import pandas as pd

    grid = pd.MultiIndex.from_product(
        [samples, genes], names=["sample", "gene"]
    ).to_frame(index=False)
    grid["sample_order"] = grid["sample"].map(sample_positions)
    grid["gene_order"] = grid["gene"].map(gene_positions)
    return grid
