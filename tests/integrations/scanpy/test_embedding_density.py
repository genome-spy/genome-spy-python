"""Stored density semantics and reuse of Scanpy-compatible embedding preparation."""

from copy import deepcopy
import inspect

import anndata as ad
import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_density_fixture import make_density
from tests.integrations.scanpy.helpers import points, units

sc = pytest.importorskip("scanpy")


def test_signature_preserves_scanpy_defaults_and_adds_native_controls():
    actual = inspect.signature(gsc.pl.embedding_density).parameters
    expected = inspect.signature(sc.pl.embedding_density).parameters
    for name, p in expected.items():
        if name in ("ax", "return_fig"):
            assert name not in actual
        else:
            assert actual[name].kind == p.kind and actual[name].default == p.default
    assert set(actual) - set(expected) == {"hover", "zoom", "obs_id", "width", "height"}
    assert all(
        actual[n].kind == inspect.Parameter.KEYWORD_ONLY
        for n in set(actual) - set(expected)
    )


CASES = [
    {},
    {"group": "A"},
    {"group": ["A", "B", "A"]},
    {"groupby": "condition"},
    {"title": "Density"},
    {"bg_dotsize": 3, "fg_dotsize": 8},
    {"vmin": None, "vmax": None},
    {"vmin": 0.2, "vmax": 0.7},
    {"vmin": "p10", "vmax": "p85"},
    {"vcenter": 0.3},
    {"vmin": lambda v: np.min(v), "vmax": lambda v: np.max(v)},
    {"basis": "PCA"},
    {"basis": "FA"},
    {"basis": "diffmap"},
    {"marker": "s"},
    {"marker": ["s"]},
    {"group": "unused"},
]


@pytest.mark.parametrize("options", CASES)
def test_coords_sizes_colors_bounds_order_and_titles_match_public_scanpy(options):
    import matplotlib.pyplot as plt

    a = make_density()
    if options.get("group") == "unused":
        a.obs["condition"] = a.obs["condition"].cat.add_categories(["unused"])
    if options.get("basis") == "PCA":
        a.uns["scores_params"]["components"] = [2, 3]
    reference = a.copy()
    result = (
        sc.pl.embedding_density(reference, key="scores", show=False, **options)
        if "groupby" not in options
        else sc.pl.embedding_density(reference, show=False, **options)
    )
    axes = result if isinstance(result, list) else [result]
    spec = (
        gsc.pl.embedding_density(a, key="scores", show=False, **options).to_dict()
        if "groupby" not in options
        else gsc.pl.embedding_density(a, show=False, **options).to_dict()
    )
    assert len(units(spec)) == len(axes)
    assert len(spec["datasets"]) == 1
    data = next(iter(spec["datasets"].values()))
    for i, (panel, ax) in enumerate(zip(units(spec), axes, strict=True)):
        mark = points(panel)
        projection = panel["transform"][0]
        assert projection["type"] == "project"
        assert projection["fields"] == [
            "_obs_id",
            "_obs_label",
            *[mark["encoding"][axis]["field"] for axis in ("x", "y")],
            f"_value_{i}",
            f"_color_{i}",
            f"_size_{i}",
            f"_order_{i}",
        ]
        rows = sorted(data, key=lambda r: r[f"_order_{i}"])
        fields = [mark["encoding"][axis]["field"] for axis in ("x", "y")]
        np.testing.assert_array_equal(
            [[r[field] for field in fields] for r in rows],
            ax.collections[0].get_offsets(),
        )
        np.testing.assert_array_equal(
            [r[f"_size_{i}"] for r in rows], ax.collections[0].get_sizes()
        )
        np.testing.assert_array_equal(
            [r[f"_color_{i}"] for r in rows], ax.collections[0].get_array()
        )
        domain = [ax.collections[0].norm.vmin, ax.collections[0].norm.vmax]
        if options.get("vcenter") is not None:
            domain.insert(1, 0.3)
        np.testing.assert_allclose(mark["encoding"]["color"]["scale"]["domain"], domain)
        for axis in ("x", "y"):
            np.testing.assert_allclose(
                mark["encoding"][axis]["scale"]["domain"],
                getattr(ax, f"get_{axis}lim")(),
            )
            assert (
                mark["encoding"][axis]["axis"]["title"]
                == getattr(ax, f"get_{axis}label")()
            )
        assert panel.get("title", {}).get("text", "") == ax.get_title()
        assert "condition" not in mark["encoding"]["color"]
    plt.close(axes[0].figure)


@pytest.mark.parametrize("group", [None, "all"])
def test_ungrouped_result_defaults_to_one_panel(group):
    a = make_density(False)
    spec = gsc.pl.embedding_density(a, group=group, show=False).to_dict()
    assert len(units(spec)) == 1 and "title" not in spec
    rows = next(iter(spec["datasets"].values()))
    np.testing.assert_array_equal([r["_color_0"] for r in rows], a.obs["umap_density"])
    assert {r["_size_0"] for r in rows} == {180}


def test_unsorted_points_keep_input_order_when_all_colors_are_in_range():
    a = make_density(False)
    spec = gsc.pl.embedding_density(a, sort_order=False, show=False).to_dict()
    rows = next(iter(spec["datasets"].values()))
    assert [r["_order_0"] for r in rows] == list(range(a.n_obs))


@pytest.mark.parametrize("options", [{}, {"group": "all", "vmin": 0.2, "vmax": 0.7}])
def test_unsorted_mixed_color_ranges_fail_instead_of_reordering_points(options):
    with pytest.raises(NotImplementedError, match="sort_order=False.*overlap order"):
        gsc.pl.embedding_density(
            make_density(), sort_order=False, show=False, **options
        )


def test_multiple_markers_fail_clearly():
    with pytest.raises(NotImplementedError, match="one marker"):
        gsc.pl.embedding_density(make_density(), marker=["s", "."], show=False)


def test_direct_basis_key_uses_the_shared_embedding_precedence():
    a = make_density()
    a.obsm["umap"] = a.obsm["X_umap"] + 10
    spec = gsc.pl.embedding_density(a, show=False).to_dict()
    rows = next(iter(spec["datasets"].values()))
    np.testing.assert_array_equal([r["_coord_0"] for r in rows], a.obsm["umap"][:, 0])


def test_density_key_defaults_stay_pinned_for_other_bases_and_params_are_authoritative():
    a = make_density()
    a.uns["umap_density_condition_params"]["covariate"] = "condition"
    chart = gsc.pl.embedding_density(a, basis="tsne", groupby="condition", show=False)
    assert (
        points(units(chart.to_dict())[0])["encoding"]["x"]["axis"]["title"] == "tSNE1"
    )
    a.uns["scores_params"]["covariate"] = None
    with pytest.raises(ValueError, match="explicit groups require"):
        gsc.pl.embedding_density(a, key="scores", group="A", show=False)


def test_no_density_analysis_expression_access_or_input_mutation(monkeypatch, tmp_path):
    a = make_density()
    path = tmp_path / "stored.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    snapshot = a.obs.copy(deep=True)
    params = deepcopy(a.uns)
    view = a[:8]
    monkeypatch.setattr(
        sc.tl, "embedding_density", lambda *a, **k: pytest.fail("Reran KDE")
    )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda *a: pytest.fail("Read expression"))
    )
    try:
        for data in (a, view, backed):
            chart = gsc.pl.embedding_density(data, key="scores", zoom=True, show=False)
            assert chart.to_dict()["datasets"]
        assert view.is_view and a.obs.equals(snapshot) and a.uns == params
        assert not any(str(k).startswith("_tmp_") for k in a.obs)
    finally:
        backed.file.close()


def test_shared_preparation_keeps_stable_ids_raw_hover_and_detached_values():
    a = make_density()
    a.obs_names = ["duplicate"] * 12
    chart = gsc.pl.embedding_density(a, key="scores", group="A", show=False)
    spec = chart.to_dict()
    snapshot = deepcopy(spec)
    rows = next(iter(spec["datasets"].values()))
    assert [r["_obs_id"] for r in rows] == [f"row-{i}" for i in range(12)]
    np.testing.assert_array_equal([r["_value_0"] for r in rows], a.obs.scores)
    assert rows[0]["_color_0"] == -1 and rows[0]["_value_0"] == 0
    a.obs["scores"] = 0
    a.obsm["X_umap"][:] = 0
    assert chart.to_dict() == snapshot


@pytest.mark.parametrize(
    "options,error",
    [
        ({"ax": None}, TypeError),
        ({"return_fig": False}, TypeError),
        ({"components": "1,2"}, TypeError),
        ({"norm": object()}, NotImplementedError),
        ({"key": "scores", "groupby": "condition"}, ValueError),
        ({"basis": 3}, ValueError),
        ({"key": 4}, TypeError),
        ({"group": 1}, TypeError),
        ({"title": []}, TypeError),
        ({"bg_dotsize": None}, ValueError),
        ({"fg_dotsize": -1}, ValueError),
        ({"bg_dotsize": float("inf")}, ValueError),
        ({"width": 0}, ValueError),
        ({"hover": 1}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"ncols": None}, NotImplementedError),
        ({"hspace": None}, NotImplementedError),
        ({"colorbar_loc": "bad"}, NotImplementedError),
        ({"size": 5}, TypeError),
        ({"edgecolor": "red", "edgecolors": "blue"}, TypeError),
    ],
)
def test_invalid_options_fail_before_optional_dependencies(monkeypatch, options, error):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
    )
    with pytest.raises(error, match="gsc.pl.embedding_density"):
        gsc.pl.embedding_density(object(), **options)


@pytest.mark.parametrize(
    "change,match",
    [
        (lambda a: a.uns.pop("scores_params"), "stored obs"),
        (lambda a: a.obs.pop("scores"), "stored obs"),
        (lambda a: a.uns["scores_params"].pop("components"), "components"),
        (lambda a: a.uns["scores_params"].update(components=[0, 2]), "valid 2D"),
        (lambda a: a.uns["scores_params"].update(components=[1, 99]), "valid 2D"),
        (lambda a: a.uns["scores_params"].update(components=[1.5, 2]), "one-based"),
        (
            lambda a: a.uns["scores_params"].update(covariate="absent"),
            "categorical obs",
        ),
        (
            lambda a: a.obs.__setitem__("condition", a.obs.condition.astype(str)),
            "categorical obs",
        ),
        (lambda a: a.obs.__setitem__("scores", np.nan), "finite values"),
        (lambda a: a.obs.__setitem__("scores", -1), "finite values"),
        (lambda a: a.obsm.pop("X_umap"), "missing obsm"),
    ],
)
def test_invalid_stored_results_fail_clearly(change, match):
    a = make_density()
    change(a)
    with pytest.raises(ValueError, match=match):
        gsc.pl.embedding_density(a, key="scores", show=False)


@pytest.mark.parametrize("group", [None, [], ["missing"]])
def test_invalid_group_selection(group):
    with pytest.raises(ValueError, match="group"):
        gsc.pl.embedding_density(make_density(), key="scores", group=group, show=False)
