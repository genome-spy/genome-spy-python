"""Prepared paired analysis and chart semantics for the review showcase."""

from collections import Counter

from genome_spy.datasets import load_dataset
from tools.docs_workflows import load_spec


def test_paired_airway_analysis_and_sample_alignment():
    data = load_dataset("airway_review", as_format="json")
    from genome_spy.datasets._airway import airway_differential_expression

    gallery, domains = airway_differential_expression()
    assert data["domains"] == domains
    assert len(data["genes"]) == len(gallery) == 12000
    assert Counter(sample["cell"] for sample in data["samples"]) == {
        "N61311": 2,
        "N052611": 2,
        "N080611": 2,
        "N061011": 2,
    }
    counts = load_dataset("airway_scaledcounts").set_index("ensgene")
    for actual, expected in zip(data["genes"], gallery.to_dict("records"), strict=True):
        for field in [
            "ensgene",
            "log2fc",
            "pvalue",
            "padj",
            "neglog10_pvalue_plot",
            "direction",
        ]:
            assert actual[field] == expected[field]
        assert actual["gene_id"] == expected["ensgene"]
        for sample in data["samples"]:
            assert (
                actual[sample["sample"]]
                == counts.loc[actual["gene_id"], sample["sample"]]
            )


def test_volcano_uses_prepared_coordinates_and_distinct_gestures():
    spec = load_spec("volcano")
    points = spec["layer"][2]
    assert points["encoding"]["y"]["field"] == "neglog10_pvalue_plot"
    assert spec["params"][0]["select"]["on"] == "mousedown[event.shiftKey]"
    assert points["params"][0]["select"]["on"] == "click[!event.shiftKey]"
    assert len(spec["datasets"][spec["data"]["name"]]) == 12000
    assert len(spec["datasets"]["samples"]) == 8
    assert [param["name"] for param in spec["params"]] == [
        "brush",
        "airwayVolcanoEffectCutoff",
        "airwayVolcanoSignificanceCutoff",
    ]
    assert spec["params"][1]["bind"]["step"] == 0.1
    assert spec["params"][2]["bind"]["step"] == 0.25
    assert all(layer["mark"]["strokeDash"] == [4, 4] for layer in spec["layer"][:2])


def test_notebook_hooks_save_records_and_keep_notes(monkeypatch):
    import asyncio
    import json
    from pathlib import Path
    from types import SimpleNamespace

    import IPython.display
    import ipywidgets as widgets

    class Selection:
        async def subscribe(self, callback, options=None):
            self.callback = callback
            self.options = options
            return lambda: None

        async def clear(self):
            self.callback({"active": False, "data": []})

    handles = {name: Selection() for name in ("brush", "picked")}

    async def get_selection(name):
        return handles[name]

    async def get_view(selector):
        assert selector == {"scope": [], "view": "volcano"}
        return SimpleNamespace(params=SimpleNamespace(get_selection=get_selection))

    api = SimpleNamespace(
        params=SimpleNamespace(get_selection=get_selection),
        views=SimpleNamespace(get=get_view),
    )

    class Widget(widgets.HTML):
        async def get_embed_api(self):
            return api

    async def run():
        path = Path(__file__).resolve().parents[1] / "notebooks/review_volcano.ipynb"
        notebook = json.loads(path.read_text())
        data = load_dataset("airway_review", as_format="json")
        namespace = {
            "data": data,
            "chart": SimpleNamespace(widget=lambda **kwargs: Widget()),
        }
        monkeypatch.setattr(IPython.display, "display", lambda *args: None)
        exec("".join(notebook["cells"][2]["source"]), namespace)
        await namespace["connection_task"]
        assert handles["brush"].options == {"delivery": "commit"}
        gene = next(row for row in data["genes"] if row["symbol"] == "FKBP5")
        handles["picked"].callback({"active": True, "data": [gene]})
        await asyncio.sleep(0)
        assert namespace["selected_genes"].gene_id.tolist() == [gene["gene_id"]]
        namespace["note"].value = "Check paired response"
        namespace["save_selection"](None)
        namespace["note"].value = "Do not overwrite"
        namespace["save_selection"](None)
        await handles["picked"].clear()
        assert namespace["selected_genes"].empty
        assert len(namespace["shortlist"]) == 1
        assert (
            namespace["shortlist"][gene["gene_id"]]["note"] == "Check paired response"
        )
        namespace["widget"].close()

    asyncio.run(run())
