"""Lollipop plot (PIK3CA).

Annotated sequence features along the PIK3CA protein drawn as a lollipop plot —
a stem and head per feature, coloured by feature type — over a band showing the
protein's functional domains. This is the standard "needle" layout for
positional annotations along a gene or protein.

Data: real PIK3CA UniProt sequence features and domains from Plotly's Dash Bio
datasets (MIT). See `docs/_static/data/README.md` for provenance.
"""

import json
from pathlib import Path

import pandas as pd

import genome_spy as gs
from genome_spy.schema import Scale

META = {
    "category": "Variants",
    "tags": ("lollipop", "layer", "real-data"),
    "order": 10,
    "height": 300,
}

DATA = Path(__file__).parent.parent / "_static" / "data" / "pik3ca_mutations.json"
PROTEIN_LENGTH = 1069
X_DOMAIN = [0, PROTEIN_LENGTH]
Y_DOMAIN = [-0.5, 1.5]
DOMAIN_TOP, DOMAIN_BOTTOM = -0.12, -0.4


def _midpoint(span: str) -> float:
    parts = span.split("-")
    if len(parts) == 2:
        return (float(parts[0]) + float(parts[1])) / 2
    return float(parts[0])


def pik3ca_features() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load PIK3CA features (as lollipops) and functional domains (as a band)."""
    raw = json.loads(DATA.read_text())
    features = pd.DataFrame(
        {
            "position": [_midpoint(x) for x in raw["x"]],
            "count": [int(y) for y in raw["y"]],
            "feature": raw["mutationGroups"],
        }
    )
    features["base"] = 0
    domains = pd.DataFrame(
        {
            "name": [d["name"] for d in raw["domains"]],
            "start": [float(d["coord"].split("-")[0]) for d in raw["domains"]],
            "end": [float(d["coord"].split("-")[1]) for d in raw["domains"]],
            "top": DOMAIN_TOP,
            "bottom": DOMAIN_BOTTOM,
            "mid": (DOMAIN_TOP + DOMAIN_BOTTOM) / 2,
        }
    )
    return features, domains


features, domains = pik3ca_features()

# --- Visualization -------------------------------------------------------------

stems = (
    gs.Chart(features)
    .mark_rule(color="#c9d1d9", size=1)
    .encode(
        x=gs.X("position:Q")
        .scale(domain=X_DOMAIN, zoom=True)
        .title("Amino-acid position"),
        y=gs.Y("base:Q").scale(reverse=False, domain=Y_DOMAIN).title("Features"),
        y2=gs.Y2("count"),
    )
)

heads = (
    gs.Chart(features)
    .mark_point(size=45, filled=True, opacity=0.85)
    .encode(
        x=gs.X("position:Q").scale(domain=X_DOMAIN, zoom=True),
        y=gs.Y("count:Q").scale(reverse=False, domain=Y_DOMAIN),
        color=gs.Color("feature:N")
        .scale(Scale(scheme="tableau10"))
        .legend(title="Feature type"),
    )
)

domain_blocks = (
    gs.Chart(domains)
    .mark_rect(cornerRadius=3, color="#5b8fd6")
    .encode(
        x=gs.X("start:Q").scale(domain=X_DOMAIN, zoom=True),
        x2=gs.X2("end"),
        y=gs.Y("bottom:Q").scale(reverse=False, domain=Y_DOMAIN),
        y2=gs.Y2("top"),
    )
)

domain_labels = (
    gs.Chart(domains)
    .mark_text(color="white", size=9)
    .encode(
        x=gs.X("start:Q").scale(domain=X_DOMAIN, zoom=True),
        x2=gs.X2("end"),
        y=gs.Y("mid:Q").scale(reverse=False, domain=Y_DOMAIN),
        text=gs.Text("name:N"),
    )
)

chart = (domain_blocks + domain_labels + stems + heads).properties(
    title="PIK3CA sequence features and domains",
    description="A lollipop plot of PIK3CA sequence features over its functional domains.",
)
