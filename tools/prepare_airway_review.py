"""Prepare the volcano review using exactly the gallery's airway analysis.

Run with ``uv run python tools/prepare_airway_review.py``. Uses only packaged
Bioconnector workshop tables; no network or additional analysis is required.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from genome_spy.datasets import load_dataset
from genome_spy.datasets._airway import airway_differential_expression

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/genome_spy/datasets/data"


def main() -> None:
    genes, domains = airway_differential_expression()
    counts = load_dataset("airway_scaledcounts").set_index("ensgene")
    metadata = load_dataset("airway_metadata")
    # Host aliases leave every gallery statistic and plotting value unchanged.
    genes["gene_id"] = genes.ensgene
    genes["symbol"] = genes.gene_symbol.fillna("")
    genes["baseMean"] = genes.base_mean
    for sample in metadata.id:
        genes[sample] = genes.ensgene.map(counts[sample])
    genes = genes.astype(object).where(genes.notna(), None)
    bundle = {
        "provenance": {
            "analysis": "Same airway_differential_expression defaults as the gallery: paired log2(count+1) t-tests; Benjamini-Hochberg adjustment",
            "source": "Packaged Bioconnector workshop airway_scaledcounts.csv and airway_metadata.csv; Himes et al. 2014, GSE52778",
            "source_license": "CC-BY-NC-SA-4.0",
            "sha256": {
                name: hashlib.sha256((DATA / name).read_bytes()).hexdigest()
                for name in ("airway_scaledcounts.csv", "airway_metadata.csv")
            },
            "sample_values": "Rounded tximport lengthScaledTPM counts, identical to gallery input; not DESeq2-normalized counts",
        },
        "domains": domains,
        "samples": [
            {"sample": row.id, "cell": row.celltype, "condition": row.dex.capitalize()}
            for row in metadata.itertuples()
        ],
        "genes": genes.to_dict(orient="records"),
    }
    content = json.dumps(bundle, allow_nan=False, separators=(",", ":")).encode()
    (DATA / "airway_review.json.gz").write_bytes(gzip.compress(content, mtime=0))


if __name__ == "__main__":
    main()
