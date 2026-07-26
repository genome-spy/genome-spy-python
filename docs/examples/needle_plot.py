"""Lollipop plot.

Mutation counts aggregated by amino-acid position and drawn above a protein
domain map. Color encodes the dominant mutation class at each site, making
hotspots easy to spot.
"""

from __future__ import annotations

import pandas as pd

import genome_spy as gs
from genome_spy.datasets import load_dataset
from genome_spy.schema import Legend, Scale

META = {
    "category": "Mutation position plots",
    "tags": ("lollipop", "layer", "real-data"),
    "order": 10,
    "height": 360,
    "max_width": 760,
}

CLASS_ORDER = [
    "Frame_Shift_Del",
    "Nonsense_Mutation",
    "Missense_Mutation",
    "Splice_Site",
]

CLASS_COLORS = (
    Scale().domain(CLASS_ORDER).range(["#5f9ed1", "#e15759", "#66b55f", "#f28e2b"])
)


def dnmt3a_lollipop_payload() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Load the curated DNMT3A lollipop payload."""
    payload = load_dataset("dnmt3a_lollipop", as_format="json")

    features = pd.DataFrame(payload["features"]).sort_values("position").copy()
    domains = pd.DataFrame(payload["domains"]).copy()
    backbone = pd.DataFrame([payload["backbone"]]).copy()

    domains["y0"] = -5.3
    domains["y1"] = -1.7
    domains["mid"] = (domains["y0"] + domains["y1"]) / 2
    domains["center"] = (domains["start"] + domains["end"]) / 2
    backbone["y0"] = -5.0
    backbone["y1"] = -2.2
    backbone["mid"] = (backbone["y0"] + backbone["y1"]) / 2
    features["base"] = float(domains["y1"].iloc[0])
    features["label_y"] = features["count"] + 1.2
    features["label_text"] = features["position"].map(
        lambda pos: f"R{pos}" if pos == 882 else ""
    )

    return features, domains, backbone, payload


features, domains, backbone, payload = dnmt3a_lollipop_payload()
DATA_PREVIEW = {"Mutation features": features, "Protein domains": domains}
protein_length = int(payload["protein_length"])
max_count = int(features["count"].max())
x_domain = [0, protein_length]
y_domain = [-6.2, max_count + 4]

mutation_legend = (
    Legend()
    .title("Mutation class")
    .orient("bottom")
    .direction("horizontal")
    .columns(2)
    .symbolSize(72)
)

# --- Visualization -------------------------------------------------------------

# The protein backbone and annotated domains form the baseline geometry for the
# lollipop marks.
backbone_band = (
    gs.Chart(backbone)
    .mark_rect(color="#a8b5b6", stroke="#111111", strokeWidth=1)
    .encode(
        x=gs.X("start:Q")
        .scale(domain=x_domain, zoom=True)
        .title("Amino-acid position"),
        x2=gs.X2("end"),
        y=gs.Y("y0:Q")
        .scale(reverse=False, domain=y_domain)
        .axis(values=[1, max_count], grid=False)
        .title(None),
        y2=gs.Y2("y1"),
    )
)

domain_layers = []
for domain in domains.to_dict(orient="records"):
    domain_layers.append(
        gs.Chart([domain])
        .mark_rect(
            color=domain["color"], cornerRadius=2, stroke="#111111", strokeWidth=1
        )
        .encode(
            x=gs.X("start:Q").scale(domain=x_domain, zoom=True),
            x2=gs.X2("end"),
            y=gs.Y("y0:Q").scale(reverse=False, domain=y_domain),
            y2=gs.Y2("y1"),
        )
    )

domain_blocks = domain_layers[0]
for layer in domain_layers[1:]:
    domain_blocks = domain_blocks + layer

domain_labels = (
    gs.Chart(domains)
    .mark_text(size=8, color="#111111")
    .encode(
        x=gs.X("center:Q").scale(domain=x_domain, zoom=True),
        y=gs.Y("mid:Q").scale(reverse=False, domain=y_domain),
        text=gs.Text("name:N"),
    )
)

# Stems carry counts from the protein backbone to each hotspot; points encode
# the dominant mutation class at that amino-acid position.
stems = (
    gs.Chart(features)
    .mark_rule(color="#c0c0c0", size=1)
    .encode(
        x=gs.X("position:Q").scale(domain=x_domain, zoom=True),
        y=gs.Y("base:Q").scale(reverse=False, domain=y_domain),
        y2=gs.Y2("count"),
    )
)

heads = (
    gs.Chart(features)
    .mark_point(size=88, filled=True, opacity=0.9)
    .encode(
        x=gs.X("position:Q").scale(domain=x_domain, zoom=True),
        y=gs.Y("count:Q").scale(reverse=False, domain=y_domain),
        color=gs.Color("class:N").scale(CLASS_COLORS).legend(mutation_legend),
    )
)

# The canonical R882 hotspot gets an explicit text label, echoing maftools.
hotspot_labels = (
    gs.Chart(features[features["is_hotspot"]].copy())
    .mark_text(dy=-12, size=11, color="#111111")
    .encode(
        x=gs.X("position:Q").scale(domain=x_domain, zoom=True),
        y=gs.Y("label_y:Q").scale(reverse=False, domain=y_domain),
        text=gs.Text("label_text:N"),
    )
)

# Compose the protein model and mutation marks into a single lollipop view.
chart = (
    backbone_band + domain_blocks + domain_labels + stems + heads + hotspot_labels
).properties(
    title=(
        f"{payload['gene']} : [Somatic Mutation Rate: {payload['mutation_rate']:.2f}%]"
    ),
    description=(
        "A DNMT3A lollipop plot derived from the maftools TCGA LAML example, "
        "with per-position mutation counts, protein domains, and the labeled "
        "R882 hotspot."
    ),
)
