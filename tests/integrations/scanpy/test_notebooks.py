"""Run the independent plotting workflows on Scanpy's packaged PBMC data."""

import json
from pathlib import Path

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.helpers import points, units, leaf_marks

sc = pytest.importorskip("scanpy")
NOTEBOOKS = Path(__file__).resolve().parents[3] / "integrations/scanpy/notebooks"


def run_notebook(path, namespace):
    notebook = json.loads(path.read_text())
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    return notebook


def test_umap_workflow_preserves_embedding_and_retrieves_selected_cells(monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    original = sc.datasets.pbmc68k_reduced()
    tsne, analyses = sc.tl.tsne, []
    density, density_calls = sc.tl.embedding_density, []

    def prepare_tsne(*args, **kwargs):
        analyses.append(kwargs)
        return tsne(*args, **kwargs)

    def prepare_density(*args, **kwargs):
        density_calls.append(kwargs)
        return density(*args, **kwargs)

    monkeypatch.setattr(sc.tl, "tsne", prepare_tsne)
    monkeypatch.setattr(sc.tl, "embedding_density", prepare_density)
    monkeypatch.setattr(sc.pp, "pca", lambda *a, **k: pytest.fail("Ran PCA"))
    monkeypatch.setattr(sc.tl, "pca", lambda *a, **k: pytest.fail("Ran PCA"))
    monkeypatch.setattr(
        sc.pp, "neighbors", lambda *a, **k: pytest.fail("Recomputed neighbors")
    )
    namespace = {}
    path = NOTEBOOKS / "scanpy_umap.ipynb"
    try:
        notebook = run_notebook(path, namespace)
        pbmc = namespace["pbmc"]
        assert pbmc.shape == original.shape == (700, 765)
        assert pbmc.obs_names.equals(original.obs_names)
        np.testing.assert_array_equal(pbmc.obsm["X_umap"], original.obsm["X_umap"])
        np.testing.assert_array_equal(pbmc.obsm["X_pca"], original.obsm["X_pca"])
        np.testing.assert_array_equal(pbmc.varm["PCs"], original.varm["PCs"])
        np.testing.assert_array_equal(
            pbmc.uns["pca"]["variance_ratio"], original.uns["pca"]["variance_ratio"]
        )
        assert analyses == [{"use_rep": "X_pca", "random_state": 0, "n_jobs": 1}]
        assert density_calls == [{"basis": "umap", "groupby": "phase"}]
        assert namespace["density_chart"] in charts
        density_spec = namespace["density_chart"].to_dict()
        assert len(units(density_spec)) == len(pbmc.obs["phase"].cat.categories)
        rows = next(iter(density_spec["datasets"].values()))
        np.testing.assert_array_equal(
            [r["_value_0"] for r in rows], pbmc.obs["umap_density_phase"]
        )
        assert namespace["pca_chart"] in charts and namespace["tsne_chart"] in charts
        marker_chart = namespace["marker_chart"]
        assert marker_chart in charts
        marker_spec = marker_chart.to_dict()
        assert marker_spec["datasets"] == charts[0].to_dict()["datasets"]
        for panel, shape in zip(units(marker_spec), ["square", "diamond"], strict=True):
            assert all(
                mark["encoding"]["shape"] == {"value": shape}
                for mark in leaf_marks(panel)
            )
        edge_chart = namespace["edges_chart"]
        assert edge_chart in charts
        edge_spec = edge_chart.to_dict()
        assert len(edge_spec["datasets"]) == 2
        assert sorted(len(rows) for rows in edge_spec["datasets"].values()) == [
            700,
            4996,
        ]
        for panel in units(edge_spec):
            assert leaf_marks(panel)[0]["mark"]["type"] == "rule"
        np.testing.assert_array_equal(
            pbmc.obsp["connectivities"].data, original.obsp["connectivities"].data
        )
        centered = namespace["centered_chart"]
        assert centered in charts
        score = pbmc.obs["B_cell_score"]
        for panel, domain in zip(
            units(centered.to_dict()),
            [[score.min(), score.max()], [score.min(), 0, score.max()]],
            strict=True,
        ):
            np.testing.assert_allclose(
                points(panel)["encoding"]["color"]["scale"]["domain"], domain
            )
        bounds_chart = namespace["bounds_chart"]
        assert bounds_chart in charts
        for panel, gene in zip(
            units(bounds_chart.to_dict()), ["CD79A", "MS4A1"], strict=True
        ):
            values = original.raw[:, gene].X.toarray().ravel()
            np.testing.assert_allclose(
                points(panel)["encoding"]["color"]["scale"]["domain"],
                [np.nanmin(values), np.nanpercentile(values, 99)],
            )
        outlined = namespace["outline_chart"]
        assert outlined in charts
        outline_spec = outlined.to_dict()
        assert len(outline_spec["datasets"]) == 1
        for panel in units(outline_spec):
            marks = leaf_marks(panel)
            assert len(marks) == 3
            assert [mark["mark"]["fillOpacity"] for mark in marks] == [1, 1, 0.7]
        loadings = namespace["loadings_chart"]
        assert loadings in charts
        variance = namespace["variance_chart"]
        assert variance in charts
        assert (
            variance.to_dict()
            == gsc.pl.ranking(
                pbmc,
                "uns",
                "variance_ratio",
                dictionary="pca",
                labels="PC",
                n_points=10,
                log=True,
                width=360,
                height=240,
                show=False,
            ).to_dict()
        )
        assert (
            sum(len(table) for table in variance.to_dict()["datasets"].values()) == 11
        )
        overview = namespace["overview_chart"]
        assert overview in charts
        overview_spec = overview.to_dict()
        assert len(overview_spec["vconcat"]) == 3
        assert len(units(overview_spec["vconcat"][1])) == 3
        assert overview_spec["vconcat"][2]["hconcat"][0]["encoding"]["x"]["scale"][
            "domain"
        ] == [
            -0.9,
            30.9,
        ]
        for panel in units(overview_spec["vconcat"][0]):
            assert all(
                points(panel)["encoding"][axis]["scale"]["zoom"] is True
                for axis in ("x", "y")
            )
        assert namespace["pca_genes"].shape == (700, 309)
        assert (
            loadings.to_dict()
            == gsc.pl.ranking(
                namespace["pca_genes"],
                "varm",
                "PCs",
                indices=[0, 1],
                n_points=20,
                include_lowest=True,
                width=280,
                height=280,
                show=False,
            ).to_dict()
        )
        assert namespace["scatter_chart"] in charts
        scatter = namespace["scatter_chart"].to_dict()
        assert scatter["resolve"]["legend"] == {"default": "collected"}
        assert scatter["resolve"]["scale"]["color"] == "independent"
        legend = scatter["config"]["legend"]
        assert (
            legend["orient"],
            legend["direction"],
            legend["columns"],
            legend["symbolSize"],
        ) == ("bottom", "horizontal", 6, 64)
        assert legend["tickCount"] == 3
        assert namespace["gene_scatter_chart"] in charts
        gene_rows = next(
            iter(namespace["gene_scatter_chart"].to_dict()["datasets"].values())
        )
        assert len(gene_rows) == pbmc.n_vars
        assert [r["_obs_label"] for r in gene_rows] == list(pbmc.var_names)
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in gene_rows], pbmc.var["means"]
        )
        assert pbmc.obsm["X_tsne"].shape == (700, 2)
        assert charts
        for chart in charts:
            if chart is loadings or chart is variance or chart is overview:
                continue
            spec = chart.to_dict()
            assert spec["datasets"]
            for panel in units(spec):
                for channel in ("x", "y"):
                    assert points(panel)["encoding"][channel]["scale"]["zoom"] is True
        view, brush = namespace["view"], namespace["brush"]
        assert view.parameter_names == [brush.name]
        assert brush.param.to_dict()["select"] == {
            "type": "interval",
            "encodings": ["x", "y"],
        }
        for panel in units(view.spec["vconcat"][0]):
            for channel in ("x", "y"):
                assert points(panel)["encoding"][channel]["scale"]["zoom"] is True
        xy = original.obsm["X_umap"]
        lower, upper = np.quantile(xy, [0.25, 0.75], axis=0)
        view.parameter_values = {
            brush.name: {
                "type": "interval",
                "intervals": {
                    "x": [lower[0], upper[0]],
                    "y": [lower[1], upper[1]],
                },
            }
        }
        retrieval = next(
            c
            for c in notebook["cells"]
            if "mask = gsc.selection_mask" in "".join(c["source"])
        )
        exec(compile("".join(retrieval["source"]), str(path), "exec"), namespace)
        expected = (
            (xy[:, 0] >= lower[0])
            & (xy[:, 0] < upper[0])
            & (xy[:, 1] >= lower[1])
            & (xy[:, 1] < upper[1])
        )
        assert 0 < expected.sum() < pbmc.n_obs
        assert namespace["selected_adata"].obs_names.equals(pbmc.obs_names[expected])
        assert namespace["selected_ids"].equals(pbmc.obs_names[expected])
        assert (
            gsc.selection_mask(pbmc, view.parameter_values[brush.name]).tolist()
            == expected.tolist()
        )
    finally:
        if "view" in namespace:
            namespace["view"].close()


def test_expression_workflow_runs_independently_with_summary_hover(monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    namespace = {}
    dpt_calls = []
    for name, owner in [("neighbors", sc.pp), ("diffmap", sc.tl), ("dpt", sc.tl)]:
        original = getattr(owner, name)

        def analysis(*args, _name=name, _original=original, **kwargs):
            dpt_calls.append((_name, kwargs))
            return _original(*args, **kwargs)

        monkeypatch.setattr(owner, name, analysis)
    ranking, calls = sc.tl.rank_genes_groups, []

    def prepare_ranking(*args, **kwargs):
        calls.append(kwargs)
        assert kwargs["key_added"] == "rank_stats"
        return ranking(*args, **kwargs)

    monkeypatch.setattr(sc.tl, "rank_genes_groups", prepare_ranking)
    scrublet, scrublet_calls = sc.pp.scrublet, []
    select_genes = sc.pp.highly_variable_genes

    def prepare_doublets(*args, **kwargs):
        scrublet_calls.append(kwargs)
        # Gene selection belongs to the explicit Scanpy analysis, never the plotting calls.
        with monkeypatch.context() as analysis:
            analysis.setattr(sc.pp, "highly_variable_genes", select_genes)
            return scrublet(*args, **kwargs)

    monkeypatch.setattr(sc.pp, "scrublet", prepare_doublets)
    monkeypatch.setattr(
        sc.pp,
        "highly_variable_genes",
        lambda *a, **k: pytest.fail("Reran gene selection"),
    )
    run_notebook(NOTEBOOKS / "scanpy_expression.ipynb", namespace)
    assert charts == [
        namespace["dotplot"],
        namespace["matrixplot"],
        namespace["heatmap"],
        namespace["matrix"],
        namespace["correlations"],
        namespace["clustermap"],
        namespace["rank_scores"],
        namespace["ranked_dotplot"],
        namespace["ranked_matrixplot"],
        namespace["ranked_heatmap"],
        namespace["statistic_dotplot"],
        namespace["statistic_matrixplot"],
        namespace["variable_genes"],
        namespace["highest_expression"],
        namespace["scrublet_scores"],
        namespace["timeseries_heatmap"],
        namespace["time_series"],
        namespace["time_series_subplots"],
        namespace["simulation_points"],
        namespace["simulation_heatmap"],
        namespace["dpt_groups_chart"],
        namespace["dpt_expression"],
    ]
    assert dpt_calls == [
        ("neighbors", {"n_neighbors": 10, "use_rep": "X", "random_state": 0}),
        ("diffmap", {"random_state": 0}),
        ("dpt", {"n_dcs": 10, "n_branchings": 1}),
    ]
    dpt_spec = namespace["dpt_groups_chart"].to_dict()
    simulation = namespace["simulation"]
    dpt_cells = namespace["dpt_cells"]
    assert dpt_cells.is_view and dpt_cells.n_obs == 320
    np.testing.assert_array_equal(
        dpt_cells.obs["dpt_order"], simulation.obs["dpt_order"].iloc[::2]
    )
    for i, field in enumerate(["dpt_groups", "dpt_pseudotime"]):
        point = next(
            m
            for m in leaf_marks(dpt_spec["vconcat"][i])
            if m["mark"]["type"] == "point"
        )
        rows = dpt_spec["datasets"][point["data"]["name"]]
        positions = [r["_sample"] for r in rows]
        expected = dpt_cells.obs[field].cat.codes if i == 0 else dpt_cells.obs[field]
        np.testing.assert_allclose(
            [r["_value"] for r in rows], expected.to_numpy()[positions]
        )
        np.testing.assert_array_equal(
            [r["_time"] for r in rows],
            dpt_cells.obs["dpt_order"].to_numpy()[positions],
        )
        assert len(rows) == dpt_cells.n_obs
    dpt_profiles = namespace["dpt_profiles"]
    assert dpt_profiles.is_view and dpt_profiles.n_obs == simulation.n_obs
    expected = dpt_profiles.X[simulation.obs["dpt_order_indices"].to_numpy()].T
    expression_spec = namespace["dpt_expression"].to_dict()
    (rows,) = [
        rows for rows in expression_spec["datasets"].values() if "_value" in rows[0]
    ]
    np.testing.assert_array_equal(
        np.array([r["_value"] for r in rows]).reshape(expected.shape), expected
    )
    profiles = namespace["profiles"]
    simulation = namespace["simulation"]
    assert simulation.shape == (640, 11)
    sim_profiles = namespace["sim_profiles"]
    assert sim_profiles.var_names.tolist() == [
        "Gata2",
        "Gata1",
        "Cebpa",
        "Pu.1",
        "Gfi1",
    ]
    for name, heatmap in [("simulation_points", False), ("simulation_heatmap", True)]:
        spec = namespace[name].to_dict()
        assert any(
            m.get("mark", {}).get("type") == ("rect" if heatmap else "point")
            for m in leaf_marks(spec)
        )
        tables = [rows for rows in spec["datasets"].values() if "_value" in rows[0]]
        assert len(tables) == 1
        rows = tables[0]
        np.testing.assert_allclose(
            np.array([r["_value"] for r in rows]).reshape(5, 640), sim_profiles.X.T
        )
        rule = next(
            m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "rule"
        )
        assert [r["position"] for r in spec["datasets"][rule["data"]["name"]]] == [
            160,
            320,
            480,
        ]
        ticks = spec["surround"]["bottom"][0]
        assert spec["datasets"][ticks["data"]["name"]] == [
            {"position": x, "label": str(i + 1)}
            for i, x in enumerate([0, 160, 320, 480])
        ]
    expected_order = namespace["pbmc"].obs["S_score"].sort_values(kind="stable").index
    assert profiles.index.equals(expected_order)
    assert list(profiles.columns) == namespace["marker_names"]
    series = namespace["timeseries_heatmap"].to_dict()
    records = next(rows for rows in series["datasets"].values() if "_value" in rows[0])
    np.testing.assert_allclose(
        np.array([row["_value"] for row in records]).reshape(10, 700),
        sc.get.obs_df(namespace["pbmc"], keys=namespace["marker_names"], use_raw=True)
        .loc[expected_order]
        .to_numpy()
        .T,
    )
    assert series["scales"]["x"]["domain"] == [0, 699]
    assert series["scales"]["y"]["domain"] == [0, 9]
    assert series["scales"]["x"]["zoom"] is True
    assert series["scales"]["y"]["zoom"] is True
    points_spec = namespace["time_series"].to_dict()
    records = next(
        rows for rows in points_spec["datasets"].values() if "_sample" in rows[0]
    )
    assert len(records) == 2100
    assert list(dict.fromkeys(r["_series"] for r in records)) == [
        "CD79A",
        "CD3D",
        "GNLY",
    ]
    np.testing.assert_allclose(
        np.array([r["_value"] for r in records]).reshape(3, 700),
        profiles[["CD79A", "CD3D", "GNLY"]].to_numpy().T,
    )
    np.testing.assert_allclose(
        [r["_time"] for r in records[:700]],
        namespace["pbmc"].obs.loc[expected_order, "S_score"],
    )
    assert len({r["_id"] for r in records}) == len(records)
    panels = namespace["time_series_subplots"].to_dict()
    assert len(panels["hconcat"]) == 2
    assert panels["resolve"]["scale"]["default"] == "independent"
    assert panels["resolve"]["legend"]["default"] == "independent"
    for chart in (namespace["phase_panel"], namespace["score_panel"]):
        spec = chart.to_dict()
        rows = next(iter(spec["datasets"].values()))
        assert len(rows) == 700 and len({r["_id"] for r in rows}) == 700
        sample = [r["_sample"] for r in rows]
        np.testing.assert_allclose(
            [r["_value"] for r in rows], profiles["GNLY"].to_numpy()[sample]
        )
        np.testing.assert_allclose(
            [r["_time"] for r in rows],
            namespace["pbmc"].obs.loc[expected_order, "S_score"].to_numpy()[sample],
        )
    phase_rows = next(iter(namespace["phase_panel"].to_dict()["datasets"].values()))
    assert list(dict.fromkeys(r["_series"] for r in phase_rows)) == ["G1", "G2M", "S"]
    score_rows = next(iter(namespace["score_panel"].to_dict()["datasets"].values()))
    np.testing.assert_allclose(
        [r["_color"] for r in score_rows],
        namespace["pbmc"].obs.loc[expected_order, "G2M_score"],
    )
    assert scrublet_calls == [
        {
            "threshold": 0.25,
            "random_state": 0,
            "use_approx_neighbors": False,
            "verbose": False,
        }
    ]
    doublets = namespace["doublet_data"]
    assert doublets.shape == (2700, 32738)
    assert len(doublets.uns["scrublet"]["doublet_scores_sim"]) == 5400
    scrublet_spec = namespace["scrublet_scores"].to_dict()
    bins = next(
        rows for rows in scrublet_spec["datasets"].values() if "density" in rows[0]
    )
    assert len(bins) == 98
    assert sum(row["count"] for row in bins if row["panel"] == 0) == 2700
    assert sum(row["count"] for row in bins if row["panel"] == 1) == 5400
    counts = namespace["counts"]
    assert counts.shape == (2700, 32738) and counts.X.min() == 0
    assert counts.X.max() == 419 and not counts.uns
    highest = namespace["highest_expression"].to_dict()
    boxes = next(rows for rows in highest["datasets"].values() if "q1" in rows[0])
    assert len(boxes) == 20 and boxes[0]["gene"] == "MALAT1"
    assert highest["layer"][0]["encoding"]["x"]["scale"]["zoom"] is True
    qc = namespace["variable_genes"].to_dict()
    genes = next(iter(qc["datasets"].values()))
    assert len(genes) == 765 and sum(g["_selected"] for g in genes) == 309
    assert [g["_obs_label"] for g in genes] == list(namespace["pbmc"].var_names)
    assert all(
        p["encoding"][axis]["scale"]["zoom"] for p in units(qc) for axis in ("x", "y")
    )
    assert len(calls) == 1 and calls[0]["n_genes"] == 765
    assert namespace["pbmc"].shape == (700, 765)
    order = namespace["pbmc"].uns["dendrogram_bulk_labels"]["categories_ordered"]
    for chart in charts[:3]:
        chart_spec = chart.to_dict()
        values = next(
            rows for rows in chart_spec["datasets"].values() if "_group" in rows[0]
        )
        assert list(dict.fromkeys(row["_group"] for row in values)) == list(order)
        tree = next(
            mark
            for mark in leaf_marks(chart_spec)
            if mark.get("mark", {}).get("color") == "#555555"
        )
        assert tree["mark"]["type"] == "link"
        assert tree["mark"]["linkShape"] == "orthogonal"
        assert len(chart_spec["datasets"][tree["data"]["name"]]) == 2 * (len(order) - 1)
    spec = charts[0].to_dict()
    dot = points(spec)
    assert len(spec["datasets"][dot["data"]["name"]]) == 100
    assert dot["encoding"]["color"]["scale"]["scheme"] == "reds"
    assert dot["encoding"]["x"]["type"] == dot["encoding"]["y"]["type"] == "index"
    assert [item["title"] for item in dot["encoding"]["tooltip"]] == [
        "Gene",
        "Group",
        "Mean expression",
        "Expressing cells (%)",
    ]
    spec = charts[1].to_dict()
    tiles = points(spec)
    records = spec["datasets"][spec["spec"]["data"]["name"]]
    assert tiles["mark"]["type"] == "rect"
    assert len(records) == 100
    assert tiles["encoding"]["color"]["scale"]["scheme"] == "blues"
    assert tiles["encoding"]["color"]["scale"]["domain"] == [0, 1]
    assert [item["title"] for item in tiles["encoding"]["tooltip"]] == [
        "Gene",
        "Group",
        "Mean expression (scaled)",
    ]
    for gene in namespace["marker_genes"].values():
        for name in gene:
            values = [row["_mean"] for row in records if row["_gene"] == name]
            assert min(values) == 0 and max(values) == 1
    spec = charts[2].to_dict()
    tiles = points(spec)
    cells = next(rows for rows in spec["datasets"].values() if "_obs_id" in rows[0])
    assert spec["scales"]["x"]["zoom"] is False
    assert spec["scales"]["y"]["zoom"] is True
    assert len(spec["scales"]["y"]["gapPositions"]) == len(order) - 1
    assert len(cells) == 700 * 10
    assert len({row["_obs_id"] for row in cells}) == 700
    assert tiles["encoding"]["color"]["scale"]["domain"] == [0, 1]
    assert tiles["encoding"]["tooltip"][-1]["title"] == "Expression (scaled)"
    assert all(
        sum(row["_obs_id"] == name for row in cells) == 10
        for name in namespace["pbmc"].obs_names
    )
    spec = charts[3].to_dict()
    records = spec["datasets"][spec["spec"]["data"]["name"]]
    np.testing.assert_array_equal(
        np.array([row["_value"] for row in records]).reshape(10, 10),
        namespace["pbmc"].uns["dendrogram_bulk_labels"]["correlation_matrix"],
    )
    assert [row["_column"] for row in records[:10]] == namespace["group_labels"]

    rulers = [p for p in charts[0].to_dict()["spec"]["params"] if "ruler" in p]
    assert len(rulers) == 1
    assert rulers[0]["ruler"]["encodings"] == ["x", "y"]
    assert rulers[0]["ruler"]["display"] == "center"
    for chart in (
        namespace[name] for name in ("matrixplot", "heatmap", "matrix", "clustermap")
    ):
        spec = chart.to_dict()
        grid = spec["spec"] if "surround" in spec else spec["layer"][0]
        text = grid["layer"][1]["layer"][0]
        assert text["mark"]["fitToBand"] is True
        assert all(
            (
                spec["scales"][axis]
                if "surround" in spec
                else grid["layer"][0]["encoding"][axis]["scale"]
            )["zoom"]
            is (axis == "y")
            for axis in ("x", "y")
        )
    clustered = namespace["clustermap"].to_dict()
    tiles = points(clustered)
    cells = clustered["datasets"][clustered["spec"]["data"]["name"]]
    assert len(cells) == 700 * 10
    assert {row["_row"] for row in cells} == set(namespace["pbmc"].obs_names)
    assert {row["_column"] for row in cells} == set(namespace["marker_names"])
    annotation = next(
        mark["encoding"]["color"]
        for mark in leaf_marks(clustered)
        if mark.get("encoding", {}).get("color", {}).get("legend", {}) is not None
        and mark.get("encoding", {}).get("color", {}).get("legend", {}).get("title")
        == "bulk_labels"
    )
    assert annotation["scale"]["domain"] == namespace["group_labels"]
    assert annotation["scale"]["range"] == list(
        namespace["pbmc"].uns["bulk_labels_colors"]
    )
    branches = [
        mark for mark in leaf_marks(clustered) if mark["mark"].get("color") == "#555555"
    ]
    assert [len(clustered["datasets"][mark["data"]["name"]]) for mark in branches] == [
        2 * 699,
        2 * 9,
    ]
    assert clustered["scales"]["y"]["gapPositions"] == []
    assert clustered["scales"]["x"]["gapPositions"] == []

    scores = namespace["rank_scores"].to_dict()
    assert len(units(scores)) == 2
    assert sum(len(rows) for rows in scores["datasets"].values()) == 10
    expected_genes = [
        gene
        for group in namespace["ranked_groups"]
        for gene in namespace["pbmc"].uns[namespace["rank_key"]]["names"][group][:3]
    ]
    for chart in charts[7:10]:
        spec = chart.to_dict()
        records = next(
            rows
            for rows in spec["datasets"].values()
            if "_gene" in rows[0] and "_group" in rows[0]
        )
        assert {r["_gene"] for r in records} == set(expected_genes)
        assert {r["_group"] for r in records} == set(namespace["group_labels"])
    heatmap_rows = next(
        rows
        for rows in namespace["ranked_heatmap"].to_dict()["datasets"].values()
        if "_obs_id" in rows[0]
    )
    assert len(heatmap_rows) == 700 * 6
    stored = namespace["pbmc"].uns["rank_stats"]
    for chart, metric in [
        (namespace["statistic_dotplot"], "logfoldchanges"),
        (namespace["statistic_matrixplot"], "pvals_adj"),
    ]:
        spec = chart.to_dict()
        rows = next(rows for rows in spec["datasets"].values() if "_mean" in rows[0])
        assert {r["_group"] for r in rows} == set(namespace["group_labels"])
        for row in rows:
            group, gene = row["_group"], row["_gene"]
            value = stored[metric][group][list(stored["names"][group]).index(gene)]
            assert row["_mean"] == pytest.approx(
                -np.log10(value) if metric == "pvals_adj" else value
            )
