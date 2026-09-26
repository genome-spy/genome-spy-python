// Browser-only hosts for the same charts used by the Python notebooks.
function renderTable(table, rows, columns) {
  const head = document.createElement("thead");
  const titles = head.insertRow();
  for (const column of columns) {
    const cell = document.createElement("th");
    cell.scope = "col";
    cell.textContent = column;
    titles.append(cell);
  }
  const body = document.createElement("tbody");
  for (const row of rows) {
    const tr = body.insertRow();
    for (const column of columns) {
      tr.insertCell().textContent = String(row[column] ?? "");
    }
  }
  table.replaceChildren(head, body);
}

function download(text, filename, type) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function bedInterval(snapshot) {
  const endpoints = snapshot.complexIntervals.x;
  if (!snapshot.active || !endpoints) throw new Error("Brush a region first.");
  const [left, right] = endpoints;
  if (left.chrom !== right.chrom) throw new Error("Choose a region within one chromosome.");
  if (!Number.isInteger(left.pos) || !Number.isInteger(right.pos) || left.pos < 0 || left.pos >= right.pos) {
    throw new Error("Select at least one whole base.");
  }
  // GenomeSpy supplies zero-based locus positions. Preserve the half-open end.
  return { chrom: left.chrom, start: left.pos, end: right.pos };
}

export function selectGenes(rows, snapshot) {
  const { x, y } = snapshot.intervals;
  if (!snapshot.active || !x || !y) return [];
  return rows.filter(row =>
    row.log2fc >= Math.min(...x) && row.log2fc <= Math.max(...x) &&
    row.neglog10_pvalue_plot >= Math.min(...y) && row.neglog10_pvalue_plot <= Math.max(...y)
  );
}

export function mountIntervals(root, api) {
  const brush = api.params.getSelection("brush");
  const form = root.querySelector("form");
  const status = root.querySelector("[data-status]");
  const save = root.querySelector("[data-save]");
  const exportButton = root.querySelector("[data-download]");
  const table = root.querySelector("[data-results]");
  const annotations = [];
  const showSelection = snapshot => {
    save.disabled = true;
    if (!snapshot.active) {
      status.textContent = "Brush the chart, enter a name, then save.";
      return;
    }
    try {
      const region = bedInterval(snapshot);
      status.textContent = `Selected ${region.chrom}:${region.start}–${region.end} (0-based).`;
      save.disabled = false;
    } catch (error) {
      status.textContent = error.message;
    }
  };
  brush.subscribe(showSelection, { delivery: "commit" });
  root.querySelector("[data-clear]").addEventListener("click", () => brush.clear());
  form.addEventListener("submit", event => {
    event.preventDefault();
    try {
      const name = form.elements.namedItem("name").value.trim();
      if (!name || /\s/.test(name)) throw new Error("Use a name without spaces (e.g. GC-rich-region).");
      const record = {
        ...bedInterval(brush.getValue()), name,
        note: form.elements.namedItem("note").value.trim(),
      };
      api.datasets.set("annotations", [...annotations, record]);
      annotations.push(record);
      renderTable(table, annotations, ["chrom", "start", "end", "name", "note"]);
      form.reset();
      brush.clear();
      exportButton.disabled = false;
      status.textContent = `Saved ${annotations.length} annotation(s). Brush another region to continue.`;
    } catch (error) {
      status.textContent = error.message;
    }
  });
  exportButton.addEventListener("click", () => {
    const bed = annotations.map(row => [row.chrom, row.start, row.end, row.name].join("\t")).join("\n") + "\n";
    download(bed, "annotations.hg38.bed", "text/plain;charset=utf-8");
  });
  root.querySelector("fieldset").disabled = false;
  showSelection(brush.getValue());
}

export function mountGenes(root, api, rows) {
  mountGeneSelection(root, api, "brush", snapshot => selectGenes(rows, snapshot));
}

export function mountPoints(root, api) {
  mountGeneSelection(root, api, "picked", snapshot => snapshot.data);
  root.querySelector("[data-clear]").textContent = "Clear selection";
}

function mountGeneSelection(root, api, name, getRows) {
  const brush = api.params.getSelection(name);
  const columns = ["ensgene", "log2fc", "pvalue", "padj"];
  const exportButton = root.querySelector("[data-download]");
  let selected = [];
  const showSelection = snapshot => {
    selected = getRows(snapshot);
    root.querySelector("[data-status]").textContent = `${selected.length} genes selected. Showing up to 20 rows.`;
    renderTable(root.querySelector("[data-results]"), selected.slice(0, 20), columns);
    exportButton.disabled = !selected.length;
  };
  brush.subscribe(showSelection);
  root.querySelector("[data-clear]").addEventListener("click", () => brush.clear());
  exportButton.addEventListener("click", () => {
    const quote = value => `"${String(value ?? "").replaceAll('"', '""')}"`;
    const csv = [columns, ...selected.map(row => columns.map(column => row[column]))]
      .map(row => row.map(quote).join(",")).join("\r\n") + "\r\n";
    download(csv, "selected-genes.csv", "text/csv;charset=utf-8");
  });
  root.querySelector("fieldset").disabled = false;
  showSelection(brush.getValue());
}

export function mountSequence(root, api, reference) {
  const view = api.views.get({scope: [], view: "base-cells"});
  const selection = view.params.getSelection("base_pick");
  const original = reference.map(row => row.base);
  const sequence = [...original];
  const status = root.querySelector("[data-status]");
  const update = () => {
    const edited = sequence.map((base, i) => ({position: i + 1, base, changed: base !== original[i]}));
    const matrix = edited.flatMap(row => ["A", "C", "G", "T"].map(base => ({
      ...row, base, value: Number(base === row.base), kind: "cell",
    })));
    api.datasets.set("matrix", matrix);
    api.datasets.set("edited", edited);
    const changes = edited.filter(row => row.changed).map(row => ({
      position: row.position, reference: original[row.position - 1], edited: row.base,
    }));
    renderTable(root.querySelector("[data-results]"), changes, ["position", "reference", "edited"]);
    status.textContent = `${changes.length} changed base(s). Edited: ${sequence.join("")}`;
  };
  selection.subscribe(snapshot => {
    const row = snapshot.data.at(-1);
    if (row?.kind !== "cell") return;
    selection.clear();
    sequence[row.position - 1] = row.base;
    update();
  });
  const reset = root.querySelector("[data-clear]");
  reset.textContent = "Reset to reference";
  reset.addEventListener("click", () => {
    selection.clear();
    sequence.splice(0, sequence.length, ...original);
    update();
  });
  const exportButton = root.querySelector("[data-download]");
  exportButton.disabled = false;
  exportButton.addEventListener("click", () => download(
    `>synthetic_reference\n${original.join("")}\n>edited_sequence\n${sequence.join("")}\n`,
    "edited-sequence.fasta", "text/plain;charset=utf-8"
  ));
  root.querySelector("fieldset").disabled = false;
  update();
}
