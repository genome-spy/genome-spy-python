"""Build live documentation workflows from the notebooks' tagged chart cells."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    "volcano": ROOT / "notebooks" / "review_volcano.ipynb",
    "intervals": ROOT / "notebooks" / "annotate_genomic_intervals.ipynb",
    "genes": ROOT / "notebooks" / "select_genes.ipynb",
    "points": ROOT / "notebooks" / "pick_genes.ipynb",
    "sequence": ROOT / "notebooks" / "edit_sequence.ipynb",
    "squid": ROOT / "notebooks" / "annotate_squid.ipynb",
}


def load_spec(name: str) -> dict[str, Any]:
    """Execute only the notebook's chart cell, without opening a widget."""
    path = NOTEBOOKS[name]
    notebook = json.loads(path.read_text())
    cells = [
        cell
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and "workflow-chart" in cell.get("metadata", {}).get("tags", [])
    ]
    if len(cells) != 1:
        raise ValueError(f"{path.name} must have exactly one workflow-chart cell.")
    namespace: dict[str, Any] = {}
    exec(compile("".join(cells[0]["source"]), str(path), "exec"), namespace)
    return namespace["chart"].to_dict()


def embed_html(name: str, spec_url: str, bundle_url: str, script_url: str) -> str:
    """Render one direct embed and its small browser-side form."""
    if name not in NOTEBOOKS:
        raise ValueError(f"Unknown workflow: {name}")
    height = {
        "intervals": 446,
        "genes": 420,
        "points": 420,
        "sequence": 350,
        "squid": 530,
        "volcano": 570,
    }[name]
    fields = (
        """
      <label>Name <input name="name" required placeholder="e.g. GC-rich-region" autocomplete="off"></label>
      <label>Note <input name="note" placeholder="Optional" autocomplete="off"></label>
      <button type="submit" data-save disabled>Save annotation</button>
    """
        if name == "intervals"
        else ""
    )
    download = {
        "intervals": "Download BED",
        "sequence": "Download FASTA",
        "squid": "Download review CSV",
    }.get(name, "Download selected genes")
    title = {
        "intervals": "Genomic interval annotation",
        "sequence": "Sequence mutator",
        "squid": "Regulatory candidate review",
    }.get(name, "Gene selection")
    mount = {
        "intervals": "mountIntervals(root, api);",
        "genes": "mountGenes(root, api, spec.datasets[spec.data.name]);",
        "points": "mountPoints(root, api);",
        "sequence": "mountSequence(root, api, spec.datasets.reference);",
        "squid": "mountSquid(root, api);",
        "volcano": "mountVolcano(root, api, spec.datasets[spec.data.name], spec.datasets.samples);",
    }[name]
    controls = f"""<form><fieldset disabled>{fields}
      <button type="button" data-clear>Clear brush</button>
      <button type="button" data-download disabled>{download}</button>
    </fieldset></form>"""
    if name == "squid":
        controls = """
  <div data-menu class="gs-context-menu" role="menu" hidden>
    <button type="button" role="menuitem" data-prepare>Add annotation</button>
  </div>
  <dialog data-dialog aria-labelledby="squid-dialog-title">
    <form><fieldset disabled>
      <h3 id="squid-dialog-title">Add annotation</h3>
      <label>Name <input name="name" required autocomplete="off" autofocus></label>
      <label>Note <textarea name="note" rows="3"></textarea></label>
      <label>Color <input type="color" name="color" value="#d89632"></label>
      <p data-error role="alert"></p>
      <div class="gs-dialog-actions">
        <button type="button" data-cancel>Cancel</button>
        <button type="submit" data-save>Save annotation</button>
      </div>
    </fieldset></form>
  </dialog>
  <div class="gs-export-actions">
    <button type="button" data-download disabled>Download CSV</button>
    <button type="button" data-bed disabled>Download BED</button>
  </div>
"""
    if name == "volcano":
        controls = """
  <fieldset disabled>
    <button type="button" data-clear>Clear selection</button>
    <button type="button" data-save disabled>Add to shortlist</button>
    <button type="button" data-download disabled>Export selection CSV</button>
  </fieldset>
  <p>Shift-drag to brush · Click a gene to select · Scroll to zoom</p>
  <h3>Selected genes</h3><p data-selection-count></p>
  <div class="gs-workflow-table"><table data-selected></table></div>
  <h3>Application shortlist</h3>
  <p>Saved genes stay here when the plot selection changes. Notes are included in the export.</p>
  <button type="button" data-export-shortlist disabled>Export shortlist CSV</button>
"""
    return f"""
<section id="workflow-{name}" class="gs-workflow" aria-label="{title}">
  <div id="workflow-{name}-chart" class="gs-doc-embed" style="height:{height}px" aria-label="{title} chart"></div>
  {controls}
  <p data-status role="status" aria-live="polite">Loading chart…</p>
  {"<h3>Saved annotations</h3>" if name == "squid" else ""}
  <div class="gs-workflow-table" tabindex="0" aria-label="Results table"><table data-results></table></div>
  <noscript>Enable JavaScript to use this demo, or download the notebook below.</noscript>
</section>
<script type="module">
import {{ embed }} from {json.dumps(bundle_url)};
import {{ mountIntervals, mountGenes, mountPoints, mountSequence, mountSquid, mountVolcano }} from {json.dumps(script_url)};
const root = document.getElementById("workflow-{name}");
const c = document.getElementById("workflow-{name}-chart");
try {{
  const response = await fetch({json.dumps(spec_url)});
  if (!response.ok) throw new Error(`Could not load chart (${{response.status}})`);
  const spec = await response.json();
  spec.width = "container";
  const api = await embed(c, spec, {{ bare: true{", renderer: 'canvas'" if name == "squid" else ""} }});
  {mount}
}} catch (error) {{
  root.querySelector('[data-status]').textContent = `Unable to load demo: ${{error.message}}`;
}}
</script>
"""
