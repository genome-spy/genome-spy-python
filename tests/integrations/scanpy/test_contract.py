"""The optional integration contract is independent of local research artifacts."""

import inspect
import json
from pathlib import Path
import subprocess
import sys

import pytest

import genome_spy as gs
from genome_spy.integrations.scanpy import pl
import genome_spy.integrations.scanpy as gsc

FIXTURES = Path(__file__).with_name("fixtures")


@pytest.mark.parametrize("family", pl.__all__)
@pytest.mark.parametrize(
    "show,autoshow", [(False, True), (True, False), (None, True), (None, False)]
)
def test_all_plots_share_native_display_and_autosave_rules(
    monkeypatch, family, show, autoshow
):
    sc = pytest.importorskip("scanpy")
    from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata

    a = make_tree_adata()
    a.obsm["X_umap"] = a.X[:, :2].copy()
    options = {"color": "group"} if family == "umap" else {"groupby": "group"}
    if family in ("dotplot", "matrixplot", "heatmap"):
        options["var_names"] = ["g1", "g2"]
    monkeypatch.setattr(sc.settings, "_autoshow", autoshow)
    monkeypatch.setattr(sc.settings, "_autosave", False)
    displayed = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: displayed.append(self))
    result = getattr(pl, family)(a, show=show, **options)
    should_show = autoshow if show is None else show
    if should_show:
        assert result is None and len(displayed) == 1
    else:
        assert isinstance(result, gs.TopLevelSpec) and not displayed
    monkeypatch.setattr(sc.settings, "_autosave", True)
    with pytest.raises(NotImplementedError, match="automatic image saving"):
        getattr(pl, family)(a, show=False, **options)
    assert isinstance(
        getattr(pl, family)(a, show=False, save=False, **options), gs.TopLevelSpec
    )


@pytest.mark.parametrize("family", pl.__all__)
@pytest.mark.parametrize(
    "options,error",
    [({"show": 1}, TypeError), ({"save": "figure.png"}, NotImplementedError)],
)
def test_shared_display_validation_precedes_optional_imports(
    monkeypatch, family, options, error
):
    monkeypatch.setattr(pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy"))
    args = (object(),)
    if family in ("dotplot", "matrixplot", "heatmap"):
        args += (["g1"], "group")
    elif family != "umap":
        args += ("group",)
    with pytest.raises(
        error, match=f"gsc.pl.{family}.*{'show' if 'show' in options else 'save'}"
    ):
        getattr(pl, family)(*args, **options)


@pytest.mark.parametrize(
    "namespace",
    ["genome_spy", "genome_spy.integrations", "genome_spy.integrations.scanpy"],
)
def test_namespace_import_keeps_optional_stack_unloaded(namespace: str) -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            f"import sys; import {namespace}; assert not set(['scanpy', 'anndata', 'numpy', 'pandas', 'scipy', 'matplotlib', 'pyarrow']) & sys.modules.keys()",
        ],
        check=True,
    )


def test_public_defaults_match_the_pinned_effective_signature() -> None:
    reference = json.loads((FIXTURES / "api.json").read_text())["entries"]["umap"][
        "parameters"
    ]
    native = inspect.signature(gsc.pl.umap).parameters
    for p in reference:
        name = p["name"]
        if name in {"ax", "return_fig"}:
            assert name not in native
        else:
            actual = native[name]
            assert actual.kind.name == p["kind"]
            default = (
                None
                if actual.default is inspect.Parameter.empty
                else repr(actual.default)
            )
            assert default == p["default"]
    assert set(native) - {p["name"] for p in reference} == {
        "hover",
        "zoom",
        "selection",
        "obs_id",
        "width",
        "height",
    }


@pytest.mark.parametrize(
    "options, error",
    [
        ({"ax": None}, TypeError),
        ({"return_fig": True}, TypeError),
        ({"projection": "3d"}, NotImplementedError),
        ({"edges": True}, NotImplementedError),
        ({"arrows": True}, NotImplementedError),
        ({"save": "plot.png"}, NotImplementedError),
        ({"norm": object()}, NotImplementedError),
        ({"vcenter": 0}, NotImplementedError),
        ({"legend_fontoutline": 2}, NotImplementedError),
        ({"legend_loc": "on data"}, NotImplementedError),
        ({"add_outline": True}, NotImplementedError),
        ({"selection": object()}, TypeError),
        ({"selection": gs.selection_point()}, NotImplementedError),
        ({"selection": gs.param("cells", value=1)}, NotImplementedError),
        ({"selection": gs.selection_interval()}, NotImplementedError),
        (
            {"selection": gs.selection_interval(encodings=["x", "y"], push="outer")},
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
    monkeypatch, options, error
) -> None:
    monkeypatch.setattr(
        pl, "_require_scanpy", lambda: pytest.fail("Validation loaded Scanpy")
    )
    with pytest.raises(error, match="gsc.pl.umap"):
        gsc.pl.umap(object(), **options)


def test_wrong_version_has_an_actionable_error(monkeypatch) -> None:
    monkeypatch.setattr(pl, "version", lambda _: "1.12.0")
    with pytest.raises(ImportError, match="supports Scanpy 1.11.5; found 1.12.0"):
        gsc.pl.umap(object(), show=False)


def test_missing_optional_dependency_has_an_actionable_error(monkeypatch) -> None:
    def missing(_):
        raise pl.PackageNotFoundError("scanpy")

    monkeypatch.setattr(pl, "version", missing)
    with pytest.raises(ImportError, match=r"genome-spy-python\[scanpy\]"):
        gsc.pl.umap(object(), show=False)
