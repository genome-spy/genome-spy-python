"""Contract behavior and regressions."""

import inspect
import json
import re
import warnings
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from packaging.version import Version

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import _guards, pl
from genome_spy.integrations.scanpy._expression.grouped_data import (
    expression_fractions,
    group_means,
    scale_values,
)
from tests.integrations.scanpy.embedding_fixtures import make_adata
from tests.integrations.scanpy.expression_fixtures import make_grouped_adata

sc = pytest.importorskip("scanpy")
CONTRACT_FIXTURES = Path(__file__).with_name("fixtures")


class TestContract:
    """The optional integration contract is independent of local research artifacts."""

    def test_progress_inventory_matches_the_pinned_api_and_available_exports(self):
        status = (
            Path(__file__).resolve().parents[3] / "integrations/scanpy/STATUS.md"
        ).read_text()
        inventory = status.split("## Public callable coverage\n", 1)[1].split(
            "## Parameter", 1
        )[0]
        rows = dict(
            re.findall("^\\| `([^`]+)` \\| ([^|]+) \\|", inventory, re.MULTILINE)
        )
        pinned = json.loads((CONTRACT_FIXTURES / "api.json").read_text())["entries"]
        assert rows.keys() == pinned.keys()
        available = {
            name
            for name, state in rows.items()
            if not state.startswith(("Not implemented", "External:"))
        }
        assert available == set(pl.__all__) - {"EmbeddingSummary"}
        assert inspect.isclass(pl.EmbeddingSummary)
        assert (
            f"{len(available)} plotting functions/builders are available as supported subsets; {len(rows) - len(available) - 2} plot/builder"
            in inventory
        )

    @pytest.mark.parametrize("family", ["matrix", "umap", "pca_overview"])
    def test_single_and_composed_charts_display_once(self, monkeypatch, family):
        from tests.integrations.scanpy.embedding_fixtures import make_pca_adata

        source = [[0, 1], [2, 3]] if family == "matrix" else make_pca_adata()
        if family == "umap":
            source.obsm["X_umap"] = source.obsm["X_pca"][:, :2].copy()
        options = {"color": ["group", "g1"]} if family != "matrix" else {}
        displayed = []
        monkeypatch.setattr(sc.settings, "_autosave", False)
        monkeypatch.setattr(
            gs.TopLevelSpec, "display", lambda self: displayed.append(self)
        )
        assert getattr(pl, family)(source, show=True, **options) is None
        assert len(displayed) == 1

    @pytest.mark.parametrize(
        "autosave,save,rejected",
        [(False, None, False), (True, None, True), (True, False, False)],
    )
    def test_shared_preparation_handles_automatic_saving(
        self, monkeypatch, autosave, save, rejected
    ):
        monkeypatch.setattr(sc.settings, "_autosave", autosave)
        if rejected:
            with pytest.raises(NotImplementedError, match="automatic image saving"):
                pl._prepare_plot(False, save, context="gsc.pl.matrix")
        else:
            assert pl._prepare_plot(False, save, context="gsc.pl.matrix") is sc

    @pytest.mark.parametrize(
        "family",
        [
            name
            for name in pl.__all__
            if name != "ranking" and inspect.isfunction(getattr(pl, name))
        ],
    )
    @pytest.mark.parametrize(
        "options,error",
        [({"show": 1}, TypeError), ({"save": "figure.png"}, NotImplementedError)],
    )
    def test_shared_display_validation_precedes_optional_imports(
        self, monkeypatch, family, options, error
    ):
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        required = [
            p
            for p in inspect.signature(getattr(pl, family)).parameters.values()
            if p.default is inspect.Parameter.empty
            and p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        args = (object(),) * len(required)
        context = {
            "pca_scatter": "pca",
            "filter_genes_dispersion": "highly_variable_genes",
        }.get(family, family)
        with pytest.raises(
            error,
            match=f"gsc.pl.{context}.*{('show' if 'show' in options else 'save')}",
        ):
            getattr(pl, family)(*args, **options)

    @pytest.mark.parametrize(
        "options, error",
        [
            ({"ax": None}, TypeError),
            ({"return_fig": True}, TypeError),
            ({"projection": "3d"}, NotImplementedError),
            ({"arrows": True}, NotImplementedError),
            ({"save": "plot.png"}, NotImplementedError),
            ({"norm": object()}, NotImplementedError),
            ({"legend_fontoutline": 2}, NotImplementedError),
            ({"legend_loc": "on data"}, NotImplementedError),
            ({"add_outline": "yes"}, TypeError),
            ({"selection": object()}, TypeError),
            ({"selection": gs.selection_point()}, NotImplementedError),
            ({"selection": gs.param("cells", value=1)}, NotImplementedError),
            ({"selection": gs.selection_interval()}, NotImplementedError),
            (
                {
                    "selection": gs.selection_interval(
                        encodings=["x", "y"], push="outer"
                    )
                },
                NotImplementedError,
            ),
            (
                {
                    "selection": gs.selection_interval(
                        encodings=["x", "y"], value={"x": [0, 1]}
                    )
                },
                NotImplementedError,
            ),
            ({"colro": "group"}, TypeError),
            ({"hover": "False"}, TypeError),
            ({"zoom": "yes"}, TypeError),
            ({"width": 0}, ValueError),
            ({"height": -1}, ValueError),
            ({"width": float("nan")}, ValueError),
            ({"height": float("inf")}, ValueError),
            ({"width": True}, ValueError),
            ({"height": "300"}, ValueError),
            ({"size": 2, "s": 3}, TypeError),
            ({"edgecolor": "red", "edgecolors": "blue"}, TypeError),
            ({"color_map": "viridis", "cmap": "Blues"}, ValueError),
            ({"mask_obs": [True], "groups": ["A"]}, ValueError),
        ],
    )
    def test_unsupported_arguments_fail_before_dependencies_or_data(
        self, monkeypatch, options, error
    ) -> None:
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda: pytest.fail("Validation loaded Scanpy")
        )
        with pytest.raises(error, match="gsc.pl.umap"):
            gsc.pl.umap(object(), **options)

    @pytest.mark.parametrize("context", ["umap", "DotPlot", "MatrixPlot"])
    @pytest.mark.parametrize("installed", ["1.11.4", "1.13.0", "1.12.4rc1"])
    def test_wrong_version_has_an_actionable_error(
        self, monkeypatch, context, installed
    ) -> None:
        monkeypatch.setattr(_guards, "version", lambda _: installed)
        with pytest.raises(
            ImportError,
            match=f"gsc.pl.{context} supports Scanpy >=1.11.5,<1.13; found {installed}",
        ):
            if context != "umap":
                getattr(gsc.pl, context)(object(), ["g1"], "group")
            else:
                gsc.pl.umap(object(), show=False)

    @pytest.mark.parametrize("installed", ["1.11.5", "1.11.6", "1.12.0", "1.12.4"])
    def test_supported_versions_return_the_scanpy_module(
        self, monkeypatch, installed
    ) -> None:
        sc = pytest.importorskip("scanpy")
        monkeypatch.setattr(_guards, "version", lambda _: installed)
        assert _guards._require_scanpy() is sc

    @pytest.mark.parametrize("family", ["dotplot", "DotPlot"])
    def test_new_scanpy_group_colormaps_are_rejected_explicitly(self, family) -> None:
        with pytest.raises(TypeError, match="unsupported option.*group_colors"):
            getattr(gsc.pl, family)(
                object(), ["g1"], "group", group_colors={"A": "red"}
            )

    @pytest.mark.parametrize(
        "show,autoshow", [(False, True), (True, False), (None, True), (None, False)]
    )
    def test_shared_finish_obeys_explicit_show_and_scanpy_default(
        self, monkeypatch, show, autoshow
    ):
        chart = gs.Chart([{"x": 1}]).mark_point()
        displayed = []
        monkeypatch.setattr(
            chart.__class__, "display", lambda self: displayed.append(self)
        )
        monkeypatch.setattr(sc.settings, "_autoshow", autoshow)
        result = pl._finish_plot(chart, show, sc)
        expected = autoshow if show is None else show
        assert displayed == ([chart] if expected else [])
        assert result is (None if expected else chart)

    def test_reference_inventory_matches_the_installed_public_api(self):
        reference = json.loads((CONTRACT_FIXTURES / "api.json").read_text())["entries"]
        current = {
            name: {"kind": "class" if inspect.isclass(value) else "function"}
            for name, value in vars(sc.pl).items()
            if not name.startswith("_")
            and callable(value)
            and getattr(value, "__module__", "").startswith("scanpy")
        }
        additions = (
            {"dogplot"} if Version(version("scanpy")) >= Version("1.12") else set()
        )
        assert current.keys() == reference.keys() | additions
        assert {name: current[name] for name in reference} == reference

    @pytest.mark.parametrize(
        "family", [name for name in pl.__all__ if name != "EmbeddingSummary"]
    )
    def test_public_signatures_preserve_scanpy_contract(self, family):
        upstream = inspect.signature(getattr(sc.pl, family)).parameters
        if "args" in upstream:
            # Scanpy 1.12 hides these deprecated signatures behind forwarding wrappers.
            reference = json.loads((CONTRACT_FIXTURES / "api.json").read_text())
            assert list(upstream) == [
                "args",
                "params" if family == "pca_scatter" else "kwargs",
            ]
            parameters = reference["legacy_parameters"][family]
        else:
            parameters = [
                {
                    "name": p.name,
                    "kind": p.kind.name,
                    "default": None
                    if p.default is inspect.Parameter.empty
                    else repr(p.default),
                }
                for p in upstream.values()
            ]
        native = inspect.signature(getattr(pl, family)).parameters
        presentation = (
            {
                "colorbar_title": repr("Mean expression"),
                "size_title": repr("Cells expressing (%)"),
            }
            if family == "dotplot"
            else {}
        )
        for parameter in parameters:
            name = parameter["name"]
            if name in {"ax", "cax", "return_fig"}:
                assert name not in native
                continue
            if name == "group_colors" and family in {"dotplot", "DotPlot"}:
                assert (
                    parameter["kind"] == "KEYWORD_ONLY"
                    and parameter["default"] == "None"
                )
                continue
            # Rejection is tested separately; no native group colormap support.
            actual = native[name]
            assert actual.kind.name == parameter["kind"]
            default = (
                None
                if actual.default is inspect.Parameter.empty
                else repr(actual.default)
            )
            assert default == presentation.get(name, parameter["default"]), (
                family,
                name,
            )
        # Only positional order changes how an existing call is interpreted.
        positional = {"POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"}
        expected_order = [p["name"] for p in parameters if p["kind"] in positional]
        assert [
            p.name for p in native.values() if p.kind.name in positional
        ] == expected_order
        upstream_names = {p["name"] for p in parameters}
        for name, parameter in native.items():
            if name not in upstream_names:
                assert parameter.kind in (
                    inspect.Parameter.KEYWORD_ONLY,
                    inspect.Parameter.VAR_KEYWORD,
                ), (family, name)


class TestUpstreamReuse:
    """Public data access and counterexamples to incompatible upstream shortcuts."""

    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    @pytest.mark.parametrize("options", [{}, {"layer": "counts"}])
    @pytest.mark.parametrize("interactive", [False, True])
    def test_grouped_plots_read_unique_keys_once_through_scanpy(
        self, monkeypatch, family, options, interactive
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            a = make_grouped_adata()
        original, calls = (sc.get.obs_df, [])

        def read(adata, **kwargs):
            calls.append((adata, kwargs))
            frame = original(adata, **kwargs)
            frame["g1"] += 100
            return frame

        monkeypatch.setattr(sc.get, "obs_df", read)
        flags = (
            {"zoom": True, "highlight" if family == "dotplot" else "show_values": True}
            if interactive
            else {}
        )
        chart = getattr(gsc.pl, family)(
            a, ["g2", "g1", "g2"], "group", show=False, **options, **flags
        )
        assert len(calls) == 1 and calls[0][0] is a
        assert calls[0][1] == {
            "keys": ["group", "g2", "g1"],
            "use_raw": not options,
            "layer": options.get("layer"),
            "gene_symbols": None,
        }
        spec = chart.to_dict()
        records = next(
            (rows for rows in spec["datasets"].values() if "_mean" in rows[0])
        )
        mean = next(
            (r["_mean"] for r in records if r["_group"] == "B" and r["_gene"] == "g1")
        )
        assert mean == pytest.approx(100 + (10 if options else 23 / 3))

    @pytest.mark.parametrize(
        "options,source,expected",
        [
            ({}, "raw", [i % 4 for i in range(8)]),
            ({"use_raw": False}, "X", [i % 3 for i in range(8)]),
            ({"layer": "counts"}, "counts", [10 * (i % 3) for i in range(8)]),
        ],
    )
    def test_umap_reuses_public_vector_access_once_and_retains_coordinates(
        self, monkeypatch, options, source, expected
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            a = make_adata()
        coordinates = a.obsm["X_umap"].copy()
        calls = []
        owner = type(a.raw) if source == "raw" else type(a)
        original = owner.obs_vector

        def read(self, key, **kwargs):
            calls.append((key, kwargs))
            return original(self, key, **kwargs).copy() + 100

        monkeypatch.setattr(owner, "obs_vector", read)
        chart = gsc.pl.umap(a, color=["g1", "g1"], show=False, **options)
        assert calls == [
            ("g1", {} if source == "raw" else {"layer": options.get("layer")})
        ]
        records = next(iter(chart.to_dict()["datasets"].values()))
        assert [r["_value_0"] for r in records] == [100 + v for v in expected]
        assert [r["_value_1"] for r in records] == [100 + v for v in expected]
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in records], coordinates[:, :2]
        )
        np.testing.assert_array_equal(a.obsm["X_umap"], coordinates)

    def test_aggregate_is_not_the_plotting_mean_or_expression_fraction(self):
        import anndata as ad

        values = pd.DataFrame(
            {"g1": [-1.0, 0, 1, 4], "g2": [np.nan, 2.0, 3, 4]},
            index=pd.CategoricalIndex(["A", "A", "B", "B"]),
        )
        a = ad.AnnData(
            values.to_numpy(),
            obs=pd.DataFrame({"group": values.index}, index=list("abcd")),
            var=pd.DataFrame(index=values.columns),
        )
        aggregated = sc.get.aggregate(a, by="group", func=["mean", "count_nonzero"])
        assert group_means(values).loc["A", "g2"] == 2
        assert np.isnan(aggregated.layers["mean"][0, 1])
        assert expression_fractions(values).loc["A", "g1"] == 0
        assert aggregated.layers["count_nonzero"][0, 0] / 2 == 0.5

    def test_plotting_standard_scale_is_not_scanpy_preprocessing_scale(self):
        values = pd.DataFrame({"g": [1.0, 3.0, 5.0]})
        assert scale_values(values, "var")["g"].tolist() == [0, 0.5, 1]
        np.testing.assert_allclose(
            sc.pp.scale(values.to_numpy(), copy=True).ravel(), [-1, 0, 1]
        )
