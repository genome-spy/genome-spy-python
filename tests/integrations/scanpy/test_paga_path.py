"""Paga path behavior and regressions."""

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._paga.path_data import prepare_paga_path
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.paga_fixtures import make_path, path_cases

pytest.importorskip("scanpy")


class TestPagaPath:
    """PAGA path data and defaults against Scanpy's public plotting entry."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", path_cases())
    def test_values_tracks_labels_and_return_data_match_public_scanpy(
        self, case, monkeypatch
    ):
        storage = "csr"
        import matplotlib.pyplot as plt
        import scanpy as sc

        options = path_cases()[case].copy()
        nodes, keys = (
            options.pop("nodes", ["beta", "alpha"]),
            options.pop("keys", ["g1", "g2"]),
        )
        a = make_path(storage, "missing" if case.startswith("missing") else case)
        plt.close("all")
        ax = sc.pl.paga_path(a, nodes, keys, show=False, **options)
        image = np.asarray(ax.images[0].get_array()).copy()
        tracks = [
            np.asarray(axis.images[0].get_array()).ravel()
            for axis in plt.gcf().axes
            if axis is not ax and axis.images
        ]
        labels = (
            [t.get_text() for t in plt.gcf().axes[-len(tracks)].texts] if tracks else []
        )
        expected = pd.DataFrame(image.T, columns=keys)
        window = options.get("n_avg", 1)
        expected["groups"] = np.convolve(
            tracks[0], np.ones(window) / window, mode="valid"
        )
        if "dpt_pseudotime" in options.get("annotations", ("dpt_pseudotime",)):
            expected["distance"] = tracks[1]
        plt.close("all")
        before_obs, before_x = (a.obs.copy(deep=True), a.X.copy())
        for owner, name in [(sc.pl, "paga_path"), (sc.tl, "paga"), (sc.tl, "dpt")]:
            monkeypatch.setattr(
                owner,
                name,
                lambda *a, **k: pytest.fail("Ran upstream plotting/analysis"),
            )
        chart, frame = gsc.pl.paga_path(
            a, nodes, keys, return_data=True, show=False, **options
        )
        pd.testing.assert_frame_equal(frame, expected)
        spec = chart.to_dict()
        tiles = next(
            (
                mark
                for mark in leaf_marks(spec)
                if mark.get("name") == "paga-path-values"
            )
        )
        table = spec["datasets"][tiles["data"]["name"]]
        np.testing.assert_equal(
            np.array(
                [np.nan if row["_value"] is None else row["_value"] for row in table]
            ).reshape(image.shape),
            image,
        )
        prepared = prepare_paga_path(
            a,
            nodes,
            keys,
            use_raw=options.get("use_raw", True),
            annotations=options.get("annotations", ("dpt_pseudotime",)),
            n_avg=options.get("n_avg", 1),
            groups_key=None,
            normalize_to_zero_one=options.get("normalize_to_zero_one", False),
        )
        np.testing.assert_equal(prepared.groups, tracks[0])
        if len(tracks) > 1:
            np.testing.assert_equal(
                prepared.annotations.to_numpy().T.ravel(), tracks[1]
            )
        actual_labels = [
            row["_label"]
            for data in spec["datasets"].values()
            for row in data
            if "_label" in row
        ]
        assert actual_labels == labels
        pd.testing.assert_frame_equal(a.obs, before_obs)
        np.testing.assert_equal(
            a.X.toarray() if hasattr(a.X, "toarray") else a.X,
            before_x.toarray() if hasattr(before_x, "toarray") else before_x,
        )

    @pytest.mark.parametrize(
        "options,error,match",
        [
            (
                {"as_heatmap": False, "show_values": True},
                NotImplementedError,
                "show_values",
            ),
            ({"left_margin": 0.2}, NotImplementedError, "left_margin"),
            ({"n_avg": 0}, ValueError, "n_avg"),
            ({"n_avg": 5}, ValueError, "n_avg"),
            ({"nodes": ["unknown"]}, ValueError, "existing group"),
            ({"nodes": [-1, 3]}, ValueError, "existing group"),
            ({"nodes": [4, 2]}, ValueError, "existing group"),
            ({"nodes": [True, 3]}, TypeError, "all group names"),
            ({"nodes": [2, "alpha"]}, TypeError, "all group names"),
            ({"nodes": ["unused"]}, ValueError, "no cells"),
            ({"keys": ["g1"]}, NotImplementedError, "two keys"),
            (
                {"annotations": ("score", "dpt_pseudotime")},
                NotImplementedError,
                "multiple annotation",
            ),
            ({"annotations": ("cluster",)}, NotImplementedError, "categorical"),
            ({"color_map": "invented"}, NotImplementedError, "color_map"),
            ({"zoom": "x"}, TypeError, "zoom"),
        ],
    )
    def test_unsupported_and_invalid_cases_fail_clearly(self, options, error, match):
        options = {"nodes": ["beta", "alpha"], "keys": ["g1", "g2"], **options}
        with pytest.raises(error, match=match):
            gsc.pl.paga_path(make_path(), show=False, **options)

    @pytest.mark.reference
    @pytest.mark.parametrize("options", [{"n_avg": 2}, {"annotations": ()}])
    def test_returned_table_matches_working_public_return_data_cases(self, options):
        import matplotlib.pyplot as plt
        import scanpy as sc

        a = make_path()
        try:
            _, expected = sc.pl.paga_path(
                a,
                ["beta", "alpha"],
                ["g1", "g2"],
                return_data=True,
                show=False,
                **options,
            )
            _, actual = gsc.pl.paga_path(
                a,
                ["beta", "alpha"],
                ["g1", "g2"],
                return_data=True,
                show=False,
                **options,
            )
            pd.testing.assert_frame_equal(actual, expected)
        finally:
            plt.close("all")

    @pytest.mark.reference
    @pytest.mark.xfail(
        strict=True,
        raises=AttributeError,
        reason="Scanpy 1.11.5 calls .T on its unsmoothed pseudotime list; C16",
    )
    def test_c16_public_unsmoothed_return_data_detects_an_upstream_fix(self):
        import matplotlib.pyplot as plt
        import scanpy as sc

        try:
            try:
                _, frame = sc.pl.paga_path(
                    make_path(),
                    ["beta", "alpha"],
                    ["g1", "g2"],
                    return_data=True,
                    show=False,
                )
            except AttributeError as error:
                assert str(error) == "'list' object has no attribute 'T'"
                raise
            assert list(frame.columns) == ["g1", "g2", "groups", "distance"]
            np.testing.assert_allclose(frame["distance"], [0.1, 0.7, 0.2, 0.4])
        finally:
            plt.close("all")

    def test_selected_sparse_genes_only_are_densified_without_mutation(
        self, monkeypatch
    ):
        from scipy import sparse

        a = make_path("csr")
        before_uns = repr(a.uns)
        original = sparse.csr_matrix.toarray

        def selected(matrix, *args, **kwargs):
            assert matrix.shape[1] == 2, "Densified unrequested genes"
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        gsc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], show=False)
        assert repr(a.uns) == before_uns

    @pytest.mark.parametrize("use_raw", [False, True], ids=["X", "raw"])
    @pytest.mark.parametrize("as_heatmap", [True, False], ids=["heatmap", "lines"])
    def test_dense_path_reads_selected_columns_before_reordering_rows(
        self, use_raw, as_heatmap
    ):
        copied_widths = []

        class SelectedColumnsOnly(np.ndarray):
            def __getitem__(self, index):
                result = super().__getitem__(index)
                if (
                    isinstance(result, np.ndarray)
                    and result.ndim == 2
                    and (not np.shares_memory(self, result))
                ):
                    copied_widths.append(result.shape[1])
                    assert result.shape[1] == 2, "Copied unrequested genes"
                return result

        a = make_path(case="raw_fallback")
        original = a.X.copy()
        a.X = original.view(SelectedColumnsOnly)
        if use_raw:
            a.raw = a
            a.X = original * 3
        _, frame = gsc.pl.paga_path(
            a,
            ["beta", "alpha", "beta"],
            ["g2", "g1"],
            use_raw=use_raw,
            as_heatmap=as_heatmap,
            return_data=True,
            show=False,
        )
        assert copied_widths and set(copied_widths) == {2}
        np.testing.assert_array_equal(
            frame[["g2", "g1"]], original[[3, 0, 4, 1, 3, 0]][:, [1, 0]]
        )

    @pytest.mark.parametrize("use_raw", [False, True], ids=["X", "raw"])
    def test_expression_validation_only_checks_cells_in_the_path(self, use_raw):
        a = make_path()
        matrix = a.raw.X if use_raw else a.X
        matrix[2, 0] = np.inf
        prepared = prepare_paga_path(
            a,
            ["beta", "alpha"],
            ["g1", "score"],
            use_raw=use_raw,
            annotations=(),
            n_avg=1,
            groups_key=None,
            normalize_to_zero_one=False,
        )
        factor = 1 if use_raw else 3
        np.testing.assert_array_equal(
            prepared.values,
            [[8 * factor, 5], [2 * factor, 10], [3 * factor, 0], [6 * factor, 20]],
        )
        matrix[3, 0] = np.inf
        with pytest.raises(ValueError, match="finite or missing"):
            prepare_paga_path(
                a,
                ["beta", "alpha"],
                ["g1", "score"],
                use_raw=use_raw,
                annotations=(),
                n_avg=1,
                groups_key=None,
                normalize_to_zero_one=False,
            )

    def test_large_path_reads_only_selected_gene_columns(self, monkeypatch):
        from anndata import AnnData
        from scipy import sparse

        a = AnnData(
            sparse.csr_matrix((100000, 20000)),
            obs=pd.DataFrame(
                {
                    "cluster": pd.Categorical(["a"] * 100000),
                    "dpt_pseudotime": np.arange(100000),
                },
                index=[str(i) for i in range(100000)],
            ),
            var=pd.DataFrame(index=[f"g{i}" for i in range(20000)]),
            uns={"paga": {"groups": "cluster"}},
        )
        original, shapes = (sparse.csr_matrix.toarray, [])

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape == (100000, 3), "Densified unrequested genes"
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        prepared = prepare_paga_path(
            a,
            ["a"],
            ["g1", "g2", "g3"],
            use_raw=False,
            annotations=(),
            n_avg=1,
            groups_key=None,
            normalize_to_zero_one=False,
        )
        assert shapes == [(100000, 3)]
        assert prepared.values.shape == (100000, 3)

    def test_return_data_after_display_and_disabled_hover(self, monkeypatch):
        import genome_spy as gs

        shown = []
        monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: shown.append(self))
        frame = gsc.pl.paga_path(
            make_path(),
            ["beta", "alpha"],
            ["g1", "g2"],
            show=True,
            return_data=True,
            hover=False,
        )
        assert isinstance(frame, pd.DataFrame) and len(shown) == 1
        assert all(
            (
                mark["mark"].get("tooltip") is None
                for mark in leaf_marks(shown[0].to_dict())
            )
        )

    def test_numeric_observation_keys_do_not_read_expression(self, monkeypatch):
        from anndata import AnnData

        a = make_path()
        monkeypatch.setattr(
            AnnData, "X", property(lambda self: pytest.fail("Read expression"))
        )
        chart, frame = gsc.pl.paga_path(
            a,
            ["beta", "alpha"],
            ["score", "dpt_pseudotime"],
            use_raw=False,
            return_data=True,
            show=False,
        )
        np.testing.assert_equal(frame["score"].to_numpy(), [5, 10, 0, 20])
        assert chart.to_dict()["scales"]["x"]["domain"] == [-0.5, 3.5]

    def test_backed_expression_rejects_before_reading_x(self, tmp_path, monkeypatch):
        from anndata import AnnData, read_h5ad

        a = make_path()
        a.write_h5ad(tmp_path / "path.h5ad")
        backed = read_h5ad(tmp_path / "path.h5ad", backed="r")
        try:
            monkeypatch.setattr(
                AnnData,
                "X",
                property(lambda self: pytest.fail("Read backed expression")),
            )
            with pytest.raises(TypeError, match="backed/lazy"):
                gsc.pl.paga_path(backed, ["beta", "alpha"], ["g1", "g2"], show=False)
        finally:
            backed.file.close()

    @pytest.mark.parametrize("storage", ["dense", "csr", "csc"])
    @pytest.mark.parametrize("use_raw", [False, True])
    def test_path_storage_preserves_profiles_and_requested_source(
        self, storage, use_raw
    ):
        _, frame = gsc.pl.paga_path(
            make_path(storage),
            ["beta", "alpha"],
            ["g2", "g1"],
            n_avg=2,
            normalize_to_zero_one=False,
            use_raw=use_raw,
            return_data=True,
            show=False,
        )
        # Path order is cells 3, 0, 4, 1; each output averages two neighbors.
        expected = np.array([[5.5, 5], [8.5, 2.5], [4.5, 4.5]])
        np.testing.assert_allclose(
            frame[["g2", "g1"]], expected * (1 if use_raw else 3)
        )
        np.testing.assert_allclose(frame["groups"], [2, 2.5, 3])
        np.testing.assert_allclose(frame["distance"], [0.4, 0.45, 0.3])


PAGA_PATH_LINES_LINE_CASES = {
    "default": {},
    "smooth": {"n_avg": 2},
    "crop": {"n_avg": 2, "xlim": (1, None)},
    "negative_crop": {"xlim": (-3, -1)},
    "empty_crop": {"xlim": (3, 1)},
    "normalize": {"n_avg": 2, "normalize_to_zero_one": True},
    "repeat": {"nodes": ["beta", "alpha", "beta"]},
    "X": {"use_raw": False},
    "raw_fallback": {},
    "filtered": {},
    "single_key": {"keys": ["g1"]},
    "single_sample": {"n_avg": 4},
    "annotations": {"annotations": ("cluster", "score", "dpt_pseudotime"), "n_avg": 2},
    "missing": {},
    "obs_key": {"keys": ["g1", "score"], "n_avg": 2},
}


class TestPagaPathLines:
    """Native PAGA path lines against Scanpy's public data, limits and return values."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", PAGA_PATH_LINES_LINE_CASES)
    def test_line_values_domains_labels_and_order_match_public_scanpy(self, case):
        storage = "csr"
        import matplotlib.pyplot as plt
        import scanpy as sc

        options = PAGA_PATH_LINES_LINE_CASES[case].copy()
        nodes = options.pop("nodes", ["beta", "alpha"])
        keys = options.pop("keys", ["g1", "g2"])
        fixture_case = (
            case if case in {"missing", "raw_fallback", "filtered"} else "default"
        )
        a = make_path(storage, fixture_case)
        fig, ax = plt.subplots()
        try:
            sc.pl.paga_path(
                a, nodes, keys, as_heatmap=False, show=False, ax=ax, **options
            )
            expected = [line.get_xydata().copy() for line in ax.lines]
            domains = [ax.get_xlim(), ax.get_ylim()]
            xlabel = ax.get_xlabel()
            legend = (
                None
                if ax.get_legend() is None
                else [t.get_text() for t in ax.get_legend().texts]
            )
        finally:
            plt.close(fig)
        spec = gsc.pl.paga_path(
            a, nodes, keys, as_heatmap=False, show=False, **options
        ).to_dict()
        root = spec
        spec = root["spec"]
        frame = pd.DataFrame(
            root["datasets"][spec["data"]["name"]],
            columns=["_sample", "_value", "_key"],
        )
        for key, curve in zip(keys, expected, strict=True):
            actual = frame.loc[frame["_key"] == key]
            np.testing.assert_array_equal(actual["_sample"], curve[:, 0])
            np.testing.assert_allclose(
                actual["_value"].to_numpy(dtype=float), curve[:, 1], equal_nan=True
            )
        for axis, domain in zip(("x", "y"), domains, strict=True):
            np.testing.assert_allclose(
                spec["encoding"][axis]["scale"]["domain"], domain
            )
        assert spec["encoding"]["x"]["axis"]["title"] == xlabel
        assert spec["encoding"]["y"]["axis"]["title"] == (
            keys[0] if len(keys) == 1 else "Value"
        ) + (" (0–1)" if options.get("normalize_to_zero_one") else "")
        assert spec["encoding"]["color"]["scale"]["domain"] == keys
        assert (spec["encoding"]["color"]["legend"] is None) is (legend is None)
        if legend is not None:
            assert keys == legend
        assert spec["mark"]["type"] == "rule" and spec["mark"]["strokeCap"] == "round"
        assert spec["transform"][0]["ops"] == ["lead", "lead"]
        assert spec["transform"][0]["groupby"] == ["_key"]
        assert spec["transform"][1]["type"] == "filter"
        assert "bottom" in root["surround"]

    @pytest.mark.reference
    def test_line_return_data_is_uncropped_and_matches_working_public_case(
        self, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        a = make_path()
        options = dict(
            as_heatmap=False, n_avg=2, xlim=(1, None), return_data=True, show=False
        )
        try:
            _, expected = sc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options)
        finally:
            plt.close("all")
        for owner, name in [(sc.pl, "paga_path"), (sc.tl, "paga"), (sc.tl, "dpt")]:
            monkeypatch.setattr(
                owner,
                name,
                lambda *a, **k: pytest.fail("Ran upstream plotting/analysis"),
            )
        before = (a.obs.copy(deep=True), repr(a.uns), a.X.copy())
        chart, frame = gsc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options)
        pd.testing.assert_frame_equal(frame, expected)
        assert len(frame) == 3
        spec = chart.to_dict()
        assert len(spec["datasets"][spec["spec"]["data"]["name"]]) == 4
        pd.testing.assert_frame_equal(a.obs, before[0])
        assert repr(a.uns) == before[1]
        np.testing.assert_array_equal(a.X, before[2])
        shown = []
        monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: shown.append(self))
        options["show"] = True
        pd.testing.assert_frame_equal(
            gsc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options), expected
        )
        assert len(shown) == 1

    @pytest.mark.parametrize("bounds", [(0.5, 2), (True, None), (0,), "bad"])
    def test_invalid_line_crop_fails_clearly(self, bounds):
        with pytest.raises(TypeError, match="xlim"):
            gsc.pl.paga_path(
                make_path(),
                ["beta", "alpha"],
                ["g1", "g2"],
                as_heatmap=False,
                xlim=bounds,
                show=False,
            )

    def test_line_options_use_native_guides_and_ignore_inactive_heatmap_options(self):
        spec = gsc.pl.paga_path(
            make_path(),
            ["beta", "alpha"],
            ["g1", "g2"],
            as_heatmap=False,
            color_map=object(),
            color_maps_annotations=object(),
            palette_groups=["red", "gray", "blue", "green"],
            show_node_names=False,
            show_yticks=False,
            show_colorbar=False,
            legend_fontsize="large",
            legend_fontweight="bold",
            title="Profiles",
            hover=False,
            zoom="xy",
            show=False,
        ).to_dict()
        root = spec
        spec = root["spec"]
        assert spec["encoding"]["color"]["legend"]["orient"] == "bottom"
        assert root["title"]["text"] == "Profiles"
        assert spec["mark"]["tooltip"] is None
        assert "tooltip" not in spec["encoding"]
        assert all(
            (spec["encoding"][axis]["scale"]["zoom"] is True for axis in ("x", "y"))
        )
        assert all(
            ("name" not in spec["encoding"][axis]["scale"] for axis in ("x", "y"))
        )
        with pytest.raises(NotImplementedError, match="distinct keys"):
            gsc.pl.paga_path(
                make_path(),
                ["beta", "alpha"],
                ["g1", "g1"],
                as_heatmap=False,
                show=False,
            )
        with pytest.raises(ValueError, match="annotations must name distinct"):
            gsc.pl.paga_path(
                make_path(),
                ["beta", "alpha"],
                ["g1", "g2"],
                as_heatmap=False,
                annotations=("cluster", "cluster"),
                show=False,
            )
