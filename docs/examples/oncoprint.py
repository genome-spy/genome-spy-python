"""Oncoprint (TCGA BRCA1/BRCA2).

A compact oncoprint: somatic alterations in BRCA1 and BRCA2 across a set of TCGA
tumour samples, one tile per altered sample coloured by alteration type. This is
the canonical cancer-genomics cohort view.

Data: real TCGA alterations from Plotly's Dash Bio datasets (MIT; upstream
cBioPortal/TCGA). See `docs/_static/data/README.md` for provenance.
"""

import json
from pathlib import Path

import pandas as pd

import genome_spy as gs
from genome_spy.schema import Scale

META = {
    "category": "Variants",
    "tags": ("rect", "cohort", "real-data"),
    "order": 20,
    "height": 220,
}

DATA = Path(__file__).parent.parent / "_static" / "data" / "tcga_oncoprint.json"


def alterations() -> pd.DataFrame:
    """Load TCGA alterations, keeping the records that carry a gene and type."""
    records = json.loads(DATA.read_text())
    data = pd.DataFrame(records)
    data = data[data["gene"].notna() & data["type"].notna()].copy()
    # Order samples so alterations cluster, as in a real oncoprint.
    order = data.sort_values(["gene", "type"])["sample"].drop_duplicates().tolist()
    data["sample"] = pd.Categorical(data["sample"], categories=order, ordered=True)
    return data.sort_values("sample")


data = alterations()

# --- Visualization -------------------------------------------------------------

alteration_colors = Scale(
    domain=["MISSENSE", "TRUNC"],
    range=["#3e8cb6", "#c53b2c"],
)

chart = (
    gs.Chart(data)
    .mark_rect(stroke="white", strokeWidth=1.5)
    .encode(
        x=gs.X("sample:N").axis(None).title("TCGA samples"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.2).title(None),
        color=gs.Color("type:N").scale(alteration_colors).legend(title="Alteration"),
    )
    .properties(
        title="BRCA1/BRCA2 alterations across TCGA samples",
        description="A compact oncoprint of somatic alterations in a TCGA cohort.",
    )
)
