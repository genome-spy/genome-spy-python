"""The optional integration contract is independent of local research artifacts."""

import inspect
import json
import re
from importlib.metadata import version
from pathlib import Path

import pytest
from packaging.version import Version

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import _guards, pl

sc = pytest.importorskip("scanpy")

FIXTURES = Path(__file__).with_name("fixtures")


def test_progress_inventory_matches_the_pinned_api_and_available_exports():
    status = (
        Path(__file__).resolve().parents[3] / "integrations/scanpy/STATUS.md"
    ).read_text()
    inventory = status.split("## Public callable coverage\n", 1)[1].split(
        "## Parameter", 1
    )[0]
    rows = dict(re.findall(r"^\| `([^`]+)` \| ([^|]+) \|", inventory, re.MULTILINE))
    pinned = json.loads((FIXTURES / "api.json").read_text())["entries"]
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
def test_single_and_composed_charts_display_once(monkeypatch, family):
    from tests.integrations.scanpy.embedding_fixtures import make_pca_adata

    source = [[0, 1], [2, 3]] if family == "matrix" else make_pca_adata()
    if family == "umap":
        source.obsm["X_umap"] = source.obsm["X_pca"][:, :2].copy()
    options = {"color": ["group", "g1"]} if family != "matrix" else {}
    displayed = []
    monkeypatch.setattr(sc.settings, "_autosave", False)
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: displayed.append(self))
    assert getattr(pl, family)(source, show=True, **options) is None
    assert len(displayed) == 1


@pytest.mark.parametrize(
    "autosave,save,rejected",
    [(False, None, False), (True, None, True), (True, False, False)],
)
def test_shared_preparation_handles_automatic_saving(
    monkeypatch, autosave, save, rejected
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
    monkeypatch, family, options, error
):
    monkeypatch.setattr(pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy"))
    required = [
        p
        for p in inspect.signature(getattr(pl, family)).parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    args = (object(),) * len(required)
    context = {
        "pca_scatter": "pca",
        "filter_genes_dispersion": "highly_variable_genes",
    }.get(family, family)
    with pytest.raises(
        error, match=f"gsc.pl.{context}.*{'show' if 'show' in options else 'save'}"
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


@pytest.mark.parametrize("context", ["umap", "DotPlot", "MatrixPlot"])
@pytest.mark.parametrize("installed", ["1.11.4", "1.13.0", "1.12.4rc1"])
def test_wrong_version_has_an_actionable_error(monkeypatch, context, installed) -> None:
    monkeypatch.setattr(_guards, "version", lambda _: installed)
    with pytest.raises(
        ImportError,
        match=rf"gsc.pl.{context} supports Scanpy >=1.11.5,<1.13; found {installed}",
    ):
        if context != "umap":
            getattr(gsc.pl, context)(object(), ["g1"], "group")
        else:
            gsc.pl.umap(object(), show=False)


@pytest.mark.parametrize("installed", ["1.11.5", "1.11.6", "1.12.0", "1.12.4"])
def test_supported_versions_return_the_scanpy_module(monkeypatch, installed) -> None:
    sc = pytest.importorskip("scanpy")
    monkeypatch.setattr(_guards, "version", lambda _: installed)
    assert _guards._require_scanpy() is sc


@pytest.mark.parametrize("family", ["dotplot", "DotPlot"])
def test_new_scanpy_group_colormaps_are_rejected_explicitly(family) -> None:
    with pytest.raises(TypeError, match="unsupported option.*group_colors"):
        getattr(gsc.pl, family)(object(), ["g1"], "group", group_colors={"A": "red"})


@pytest.mark.parametrize(
    "show,autoshow", [(False, True), (True, False), (None, True), (None, False)]
)
def test_shared_finish_obeys_explicit_show_and_scanpy_default(
    monkeypatch, show, autoshow
):
    chart = gs.Chart([{"x": 1}]).mark_point()
    displayed = []
    monkeypatch.setattr(chart.__class__, "display", lambda self: displayed.append(self))
    monkeypatch.setattr(sc.settings, "_autoshow", autoshow)
    result = pl._finish_plot(chart, show, sc)
    expected = autoshow if show is None else show
    assert displayed == ([chart] if expected else [])
    assert result is (None if expected else chart)


def test_reference_inventory_matches_the_installed_public_api():
    reference = json.loads((FIXTURES / "api.json").read_text())["entries"]
    current = {
        name: {"kind": "class" if inspect.isclass(value) else "function"}
        for name, value in vars(sc.pl).items()
        if not name.startswith("_")
        and callable(value)
        and getattr(value, "__module__", "").startswith("scanpy")
    }
    additions = {"dogplot"} if Version(version("scanpy")) >= Version("1.12") else set()
    assert current.keys() == reference.keys() | additions
    assert {name: current[name] for name in reference} == reference


@pytest.mark.parametrize(
    "family", [name for name in pl.__all__ if name != "EmbeddingSummary"]
)
def test_public_signatures_preserve_scanpy_contract(family):
    upstream = inspect.signature(getattr(sc.pl, family)).parameters
    if "args" in upstream:
        # Scanpy 1.12 hides these deprecated signatures behind forwarding wrappers.
        reference = json.loads((FIXTURES / "api.json").read_text())
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
                parameter["kind"] == "KEYWORD_ONLY" and parameter["default"] == "None"
            )
            continue  # Rejection is tested separately; no native group colormap support.
        actual = native[name]
        assert actual.kind.name == parameter["kind"]
        default = (
            None if actual.default is inspect.Parameter.empty else repr(actual.default)
        )
        assert default == presentation.get(name, parameter["default"]), (family, name)
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
