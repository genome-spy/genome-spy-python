"""Native presentation options retain source values, IDs and analysis ownership."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks, points
from tests.integrations.scanpy.hvg_fixture import make_hvg_result
from tests.integrations.scanpy.paga_fixture import make_adjacency
from tests.integrations.scanpy.test_paga_compare import make_compare


def test_hvg_preview_reuses_stored_scores_and_keeps_saved_selection():
    frame = make_hvg_result()
    original = frame.copy(deep=True)
    base = gsc.pl.highly_variable_genes(frame, show=False).to_dict()
    preview = gsc.pl.highly_variable_genes(
        frame, threshold_slider=True, show=False
    ).to_dict()
    assert len(preview["datasets"]) == 2  # Gene table plus one cutoff-rule record.
    genes = next(
        rows for rows in preview["datasets"].values() if "_selected" in rows[0]
    )
    assert genes == next(iter(base["datasets"].values()))
    assert (
        len(preview["params"]) == 1 and preview["params"][0]["bind"]["input"] == "range"
    )
    pd.testing.assert_frame_equal(frame, original)


@pytest.mark.parametrize(
    "result",
    [
        lambda: make_hvg_result().assign(dispersions_norm=1),
        lambda: make_hvg_result().assign(dispersions_norm=np.nan),
    ],
)
def test_hvg_slider_requires_a_varying_stored_score(result):
    with pytest.raises(ValueError, match="varying normalized score"):
        gsc.pl.highly_variable_genes(result(), threshold_slider=True, show=False)


@pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
def test_focus_and_ruler_leave_profile_records_and_ids_unchanged(family):
    source = pd.DataFrame({"A": [1, np.nan, 3], "B": [4, 5, 6]})
    options = dict(var_names=source.columns, show=False)
    base = getattr(gsc.pl, family)(source, **options).to_dict()
    interactive = getattr(gsc.pl, family)(
        source, series_select=True, ruler=True, zoom=True, **options
    ).to_dict()
    assert interactive["datasets"] == base["datasets"]
    mark = leaf_marks(interactive)[0]
    assert mark["encoding"]["opacity"]["scale"] is None
    assert "zoomLevel" in mark["mark"]["size"]["expr"]
    assert len(interactive["params"]) == 2


@pytest.mark.parametrize("labels", [["only one"], "ABC"])
def test_adjacency_labels_must_cover_the_explicit_matrix_order(labels):
    with pytest.raises(ValueError, match="labels.*3 labels"):
        gsc.pl.paga_adjacency(make_adjacency(), labels=labels, show=False)


def test_compare_uses_small_default_cells_and_respects_explicit_sizes():
    adata = make_compare()
    before = deepcopy(adata)
    for size in [None, 25]:
        spec = gsc.pl.paga_compare(
            adata,
            size=size,
            zoom=True,
            legend_fontweight="normal",
            add_pos=False,
            show=False,
        ).to_dict()
        cells = points(spec["hconcat"][0])
        records = spec["datasets"][cells["data"]["name"]]
        assert {r["_size_0"] for r in records} == {9 if size is None else size}
        assert "zoomLevel" in cells["encoding"]["size"]["scale"]["range"][1]["expr"]
    np.testing.assert_array_equal(adata.obsm["X_umap"], before.obsm["X_umap"])
    pd.testing.assert_frame_equal(adata.obs, before.obs)


@pytest.mark.parametrize(
    "options",
    [
        {"shuffle": True, "connect": True},
        {"shuffle": True, "run_select": True},
        {"as_heatmap": True, "connect": True},
    ],
)
def test_simulation_controls_reject_modes_without_ordered_run_coordinates(options):
    from tests.integrations.scanpy.sim_fixture import make_sim

    with pytest.raises(NotImplementedError, match="gsc.pl.sim"):
        gsc.pl.sim(make_sim(), show=False, **options)


@pytest.mark.parametrize("alias", ["color", "colors"])
def test_edge_slider_rejects_degree_colors_instead_of_showing_stale_statistics(alias):
    from tests.integrations.scanpy.paga_fixture import make_paga

    with pytest.raises(NotImplementedError, match="graph-degree"):
        gsc.pl.paga(
            make_paga(), **{alias: "degree_solid"}, edge_slider=True, show=False
        )
