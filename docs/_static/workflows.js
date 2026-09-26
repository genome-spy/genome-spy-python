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

// Preserve half-open brush boundaries: round both bounds up to base edges.
// Clip to the prepared table, not the current zoom domain.
export function squidInterval(snapshot, lower, upper) {
  const bounds = snapshot?.intervals?.x;
  if (!snapshot?.active || !bounds) throw new Error("Brush a region first.");
  if (bounds.length !== 2 || !bounds.every(Number.isFinite)) {
    throw new Error("The brush must contain two finite positions.");
  }
  const start = Math.max(lower, Math.ceil(Math.min(...bounds)));
  const end = Math.min(upper, Math.ceil(Math.max(...bounds)));
  if (start >= end) throw new Error("Select at least one available base.");
  return { start, end };
}

export function squidDraft(input, output) {
  const region = squidInterval(input, 15646649, 15647250);
  const context = output?.active ? squidInterval(output, 15646499, 15647400) : null;
  return { ...region, output_start: context?.start ?? "", output_end: context?.end ?? "" };
}

export function annotationCsv(rows) {
  const columns = ["id", "assembly", "chrom", "start", "end", "name", "note", "color",
    "follow_up", "output_start", "output_end", "source"];
  const quote = value => `"${String(value ?? "").replaceAll('"', '""')}"`;
  return [columns, ...rows.map(row => columns.map(key => row[key]))]
    .map(row => row.map(quote).join(",")).join("\r\n") + "\r\n";
}

export function mountSquid(root, api) {
  const input = api.views.get({scope: [], view: "importance"}).params.getSelection("contributionRegion");
  const output = api.views.get({scope: [], view: "prediction"}).params.getSelection("accessibilityRegion");
  const form = root.querySelector("form");
  const field = name => form.elements.namedItem(name);
  const status = root.querySelector("[data-status]");
  const menu = root.querySelector("[data-menu]");
  const dialog = root.querySelector("[data-dialog]");
  const errorText = root.querySelector("[data-error]");
  const menuButton = root.querySelector("[data-prepare]");
  const cancel = root.querySelector("[data-cancel]");
  const table = root.querySelector("[data-results]");
  const csv = root.querySelector("[data-download]");
  const bed = root.querySelector("[data-bed]");
  let annotations = [];
  let pending = null;
  let nextId = 1;
  const report = action => {
    try { action(); } catch (error) { (dialog.open ? errorText : status).textContent = error.message; }
  };
  const closeMenu = () => { menu.hidden = true; };
  const cancelDraft = () => {
    pending = null;
    closeMenu();
    dialog.close();
    form.reset();
    errorText.textContent = "";
  };
  const showDraft = () => {
    closeMenu();
    errorText.textContent = "";
    root.querySelector("#squid-dialog-title").textContent = pending.id ? "Edit annotation" : "Add annotation";
    dialog.showModal();
    field("name").focus();
  };
  const refresh = () => {
    renderTable(table, annotations, ["id", "name", "start", "end", "output_start", "output_end", "note", "color"]);
    table.querySelector("thead tr").insertCell().textContent = "Actions";
    [...table.querySelectorAll("tbody tr")].forEach((tr, index) => {
      const cell = tr.insertCell();
      for (const action of ["Edit", "Remove"]) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = action;
        button.dataset[action.toLowerCase()] = annotations[index].id;
        button.setAttribute("aria-label", `${action} ${annotations[index].name}`);
        cell.append(button);
      }
    });
    csv.disabled = bed.disabled = annotations.length === 0;
  };
  const showSelection = () => {
    closeMenu();
    status.textContent = input.getValue().active
      ? "Right-click the selected input region to add an annotation."
      : "Brush the contribution track, then right-click your selection.";
  };
  input.subscribe(showSelection, { delivery: "commit" });
  output.subscribe(showSelection, { delivery: "commit" });
  // Keep the right mouse button from starting a new brush before contextmenu.
  api.events.subscribe("mousedown", event => {
    if (event.sourceEvent.button === 2) event.preventViewDefault();
  });
  api.events.subscribe("contextmenu", event => {
    closeMenu();
    if (!input.contains(event.point)) return;
    event.sourceEvent.preventDefault();
    event.preventViewDefault();
    report(() => {
      pending = squidDraft(input.getValue(), output.getValue());
      form.reset();
      menu.hidden = false;
      const bounds = menu.getBoundingClientRect();
      menu.style.left = `${Math.max(8, Math.min(event.sourceEvent.clientX, innerWidth - bounds.width - 8))}px`;
      menu.style.top = `${Math.max(8, Math.min(event.sourceEvent.clientY, innerHeight - bounds.height - 8))}px`;
      menuButton.focus();
    });
  });
  document.addEventListener("pointerdown", event => {
    if (!menu.contains(event.target)) closeMenu();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu();
  });
  window.addEventListener("resize", closeMenu);
  document.addEventListener("scroll", closeMenu, true);
  menuButton.addEventListener("click", () => report(showDraft));
  cancel.addEventListener("click", cancelDraft);
  dialog.addEventListener("cancel", event => { event.preventDefault(); cancelDraft(); });
  form.addEventListener("submit", event => {
    event.preventDefault();
    report(() => {
      if (!pending) throw new Error("Freeze an input region first.");
      const name = field("name").value.trim();
      if (!name || /\s/.test(name)) throw new Error("Use a nonempty name without whitespace.");
      const color = field("color").value;
      const rgb = [1, 3, 5].map(i => parseInt(color.slice(i, i + 2), 16));
      const labelColor = rgb.reduce((sum, c, i) => sum + c * [0.299, 0.587, 0.114][i], 0) > 150 ? "#000000" : "#ffffff";
      const record = {
        ...pending, color, label_color: labelColor, id: pending.id ?? nextId, assembly: "dm6", chrom: "chrX",
        name, note: field("note").value.trim(), follow_up: "",
        source: "bpreveal-pisa/v3",
      };
      const rows = pending.id ? annotations.map(row => row.id === pending.id ? record : row) : [...annotations, record];
      api.datasets.set("annotations", rows);
      if (!pending.id) nextId++;
      annotations = rows;
      cancelDraft();
      refresh();
      form.reset();
      status.textContent = `Saved ${annotations.length} annotation(s) in application data. Double-click the track to clear its brush.`;
    });
  });
  table.addEventListener("click", event => report(() => {
    const button = event.target.closest("button");
    if (!button) return;
    const id = Number(button.dataset.edit ?? button.dataset.remove);
    const record = annotations.find(row => row.id === id);
    if (!record) return;
    if (button.dataset.edit) {
      pending = { ...record };
      for (const name of ["name", "note", "color"]) field(name).value = record[name];
      showDraft();
    } else {
      const rows = annotations.filter(row => row.id !== id);
      api.datasets.set("annotations", rows);
      annotations = rows;
      if (pending?.id === id) cancelDraft();
      refresh();
      status.textContent = `Removed annotation. ${annotations.length} saved.`;
    }
  }));
  csv.addEventListener("click", () => download(annotationCsv(annotations), "sog-review.dm6.csv", "text/csv;charset=utf-8"));
  bed.addEventListener("click", () => download(
    annotations.map(row => [row.chrom, row.start, row.end, row.name].join("\t")).join("\n") + "\n",
    "sog-review.dm6.bed", "text/plain;charset=utf-8"
  ));
  root.querySelector("fieldset").disabled = false;
  cancelDraft();
  refresh();
  showSelection();
}

export function volcanoRows(rows, snapshot) {
  const {x, y} = snapshot.intervals;
  if (!snapshot.active || !x || !y) return [];
  return rows.filter(row => row.log2fc >= Math.min(...x) && row.log2fc <= Math.max(...x)
    && row.neglog10_pvalue_plot >= Math.min(...y) && row.neglog10_pvalue_plot <= Math.max(...y));
}

export function mountVolcano(root, api, rows, samples) {
  const brush = api.params.getSelection("brush");
  const picked = api.views.get({scope: [], view: "volcano"}).params.getSelection("picked");
  const byId = new Map(rows.map(row => [row.gene_id, row]));
  const shortlist = new Map();
  let selected = [];
  let updating = false;
  const columns = ["gene_id", "symbol", "log2fc", "padj"];
  const format = value => typeof value === "number" ? (Math.abs(value) < 0.001 ? value.toExponential(2) : value.toFixed(3)) : value;
  const displayRows = records => records.map(row => Object.fromEntries(columns.map(key => [key, format(row[key])])));
  const button = (label, action) => {
    const element = document.createElement("button");
    element.type = "button"; element.textContent = label;
    element.addEventListener("click", action);
    return element;
  };
  const show = records => {
    selected = records;
    root.querySelector("[data-status]").textContent = `${records.length} selected · ${shortlist.size} saved to your application shortlist`;
    root.querySelector("[data-selection-count]").textContent = `${records.length} selected; showing up to 20. Exports include every selected gene.`;
    const table = root.querySelector("[data-selected]");
    renderTable(table, displayRows(records.slice(0, 20)), columns);
    ["Gene ID", "Symbol", "log₂ FC", "Adjusted p"].forEach((label, i) => {table.tHead.rows[0].cells[i].textContent = label;});
    root.querySelector("[data-save]").disabled = !records.length;
    root.querySelector("[data-download]").disabled = !records.length;
  };
  const updateShortlist = () => {
    const saved = [...shortlist.values()];
    const table = root.querySelector("[data-results]");
    renderTable(table, displayRows(saved), [...columns, "Note", ""]);
    ["Gene ID", "Symbol", "log₂ FC", "Adjusted p"].forEach((label, i) => {table.tHead.rows[0].cells[i].textContent = label;});
    [...table.tBodies[0].rows].forEach((tr, i) => {
      const row = saved[i];
      const note = document.createElement("input");
      note.value = row.note; note.placeholder = "Review note";
      note.setAttribute("aria-label", `Note for ${row.gene_id}`);
      note.addEventListener("input", () => { row.note = note.value; });
      tr.cells[4].replaceChildren(note);
      tr.cells[5].replaceChildren(button("Remove", () => {shortlist.delete(row.gene_id); updateShortlist();}));
    });
    root.querySelector("[data-export-shortlist]").disabled = !saved.length;
    root.querySelector("[data-status]").textContent = `${selected.length} selected · ${saved.length} saved to your application shortlist`;
  };
  brush.subscribe(snapshot => {
    if (updating || (!snapshot.active && picked.getValue().active)) return;
    updating = true;
    if (snapshot.active) picked.clear();
    show(volcanoRows(rows, snapshot));
    updating = false;
  }, {delivery: "commit"});
  picked.subscribe(snapshot => {
    if (updating || (!snapshot.active && brush.getValue().active)) return;
    updating = true;
    if (snapshot.active) brush.clear();
    show(snapshot.data.map(row => byId.get(row.gene_id)).filter(Boolean));
    updating = false;
  });
  root.querySelector("[data-clear]").addEventListener("click", () => {brush.clear(); picked.clear(); show([]);});
  root.querySelector("[data-save]").addEventListener("click", () => {
    for (const row of selected) if (!shortlist.has(row.gene_id)) shortlist.set(row.gene_id, {...row, note: ""});
    updateShortlist();
  });
  const exportRows = (records, filename) => {
    const keys = [...columns, "baseMean", "pvalue", ...samples.map(sample => sample.sample), "note"];
    const quote = value => `"${String(value ?? "").replaceAll('"', '""')}"`;
    const csv = [keys, ...records.map(row => keys.map(key => row[key]))].map(row => row.map(quote).join(",")).join("\r\n") + "\r\n";
    download(csv, filename, "text/csv;charset=utf-8");
  };
  root.querySelector("[data-download]").addEventListener("click", () => exportRows(selected, "airway-selection.csv"));
  root.querySelector("[data-export-shortlist]").addEventListener("click", () => exportRows([...shortlist.values()], "airway-shortlist.csv"));
  root.querySelector("[data-save]").closest("fieldset").disabled = false;
  show([]); updateShortlist();
}
