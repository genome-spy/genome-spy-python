"""Clustered heatmap with dendrograms.

Explore 72 genes across 60 DepMap cell lines with aligned clustering trees and
cell-line annotations. Pan and zoom to inspect individual expression values.
"""

import genome_spy as gs
from genome_spy.schema import Encoding, OverhangConfig, StyleConfig

META = {
    "category": "Expression and heatmaps",
    "order": 10,
    "height": 760,
    "max_width": 1100,
}
DATA = "https://data.genomespy.app/datasets/depmap-cell-line-rna-seq/v1/"
cell_lines = gs.Data(
    url=DATA + "cell-lines.csv", format=gs.data_format(parse={"row": "number"})
)
genes = gs.Data(
    url=DATA + "genes.csv", format=gs.data_format(parse={"column": "number"})
)

# Trees contain prepared merge heights; the browser computes link endpoints.
column_tree = (
    gs.Chart(gs.Data(url=DATA + "gene-tree.json"))
    .transform_lookup(from_=genes, key="feature", fields="id", values=["column"])
    .transform_dendrogram(
        key="id", parentKey="parent", height="height", leafIndex="column"
    )
    .mark_link(
        linkShape="orthogonal", orient="vertical", size=0.9, minPickingSize=5, clip=True
    )
    .encode(
        x=gs.X("sourceIndex:I", band=0.5).axis(None),
        x2=gs.X2("targetIndex", band=0.5),
        xOffset=gs.XOffset("sourceOffset:Q").scale(
            domain=[0, 1], range=[0, gs.expr("width * bandstep('x', width)")]
        ),
        x2Offset=gs.X2Offset(field="targetOffset"),
        y=gs.Y("sourceHeight:Q")
        .scale(
            domain=gs.ViewportDomainRef(source="viewport", mode="contain"),
            padding=0.02,
            zero=True,
            nice=False,
            zoom=False,
        )
        .axis(None),
        y2="targetHeight",
        color=gs.Color("cluster:N")
        .scale(
            domain=["C1", "C2", "C3", "C4", "C5", "C6", "Mixed"],
            range=[
                "#7c3aed",
                "#0ea5e9",
                "#f59e0b",
                "#e11d48",
                "#10b981",
                "#64748b",
                "#334155",
            ],
        )
        .legend(None),
    )
    .properties(name="columnDendrogram", height=gs.SizeDef(grow=0.2))
)
row_tree = (
    gs.Chart(gs.Data(url=DATA + "cell-line-tree.json"))
    .transform_lookup(from_=cell_lines, key="sample", fields="id", values=["row"])
    .transform_dendrogram(
        key="id", parentKey="parent", height="height", leafIndex="row"
    )
    .mark_link(
        linkShape="orthogonal",
        orient="horizontal",
        size=0.9,
        minPickingSize=5,
        clip=True,
    )
    .encode(
        x=gs.X("sourceHeight:Q")
        .scale(
            domain=gs.ViewportDomainRef(source="viewport", mode="contain"),
            padding=0.02,
            reverse=True,
            zero=True,
            nice=False,
            zoom=False,
        )
        .axis(None),
        x2="targetHeight",
        y=gs.Y("sourceIndex:I", band=0.5).axis(None),
        y2=gs.Y2("targetIndex", band=0.5),
        yOffset=gs.YOffset("sourceOffset:Q").scale(
            domain=[0, 1], range=[0, gs.expr("-height * bandstep('y', height)")]
        ),
        y2Offset=gs.Y2Offset(field="targetOffset"),
        color=gs.Color("cluster:N")
        .scale(
            domain=["R1", "R2", "R3", "R4", "Mixed"],
            range=["#3b82f6", "#ef4444", "#22a16d", "#a855f7", "#334155"],
        )
        .legend(None),
    )
    .properties(name="rowDendrogram", width=gs.SizeDef(grow=0.2))
)

lineage = (
    gs.Chart()
    .mark_rect(clip="y")
    .encode(
        color=gs.Color("lineage:N")
        .scale(
            domain=[
                "Bowel",
                "Breast",
                "CNS/Brain",
                "Kidney",
                "Lung",
                "Lymphoid",
                "Myeloid",
                "Ovary/Fallopian Tube",
                "Pancreas",
                "Skin",
            ],
            range=[
                "#bcbd22",
                "#e377c2",
                "#8c564b",
                "#2ca02c",
                "#1f77b4",
                "#17becf",
                "#d62728",
                "#ff7f0e",
                "#7f7f7f",
                "#9467bd",
            ],
        )
        .legend(title="Cancer lineage", columns=3)
    )
    .properties(
        name="cancerAnnotation",
        width=16,
        title=gs.Title(text="Lineage", style="metadata-column-title"),
    )
)
growth = (
    gs.Chart()
    .mark_rect(clip="y")
    .encode(
        color=gs.Color("growthPattern:N")
        .scale(
            domain=["Adherent", "Suspension", "Mixed"],
            range=["#33936b", "#8064a2", "#d78239"],
        )
        .legend(title="Growth pattern", direction="vertical", columns=1)
    )
    .properties(
        name="growthAnnotation",
        width=16,
        title=gs.Title(text="Growth pattern", style="metadata-column-title"),
    )
)
origin = (
    gs.Chart()
    .mark_rect(clip="y")
    .encode(
        color=gs.Color("sampleOrigin:N")
        .scale(
            domain=["Primary", "Metastatic", "Unknown"],
            range=["#3274a1", "#d1495b", "#cbd5e1"],
        )
        .legend(title="Sample origin", direction="vertical", columns=1)
    )
    .properties(
        name="originAnnotation",
        width=16,
        title=gs.Title(text="Sample origin", style="metadata-column-title"),
    )
)
sample_labels = (
    gs.Chart()
    .mark_text(
        align="left",
        baseline="middle",
        fitToBand=True,
        flushY=False,
        dx=4,
        size=9,
        color="#334155",
        clip="y",
        tooltip=None,
    )
    .encode(x=gs.value(0), y=gs.Y("row:I").axis(None), text="cellLine")
    .properties(
        name="sampleLabels",
        width=70,
        title=gs.Title(
            text="Cell line",
            orient="bottom",
            anchor="start",
            align="left",
            baseline="top",
            fontSize=8,
            fontWeight="normal",
            color="#334155",
            offset=8,
        ),
    )
)
annotations = gs.SurroundSideSpec(
    name="cellLineAnnotations",
    spacing=4,
    data=cell_lines,
    encoding=Encoding(
        y=gs.Y("row:I").axis(None),
        tooltip=[
            gs.Tooltip("cellLine", title="Cell line"),
            gs.Tooltip("sample", title="DepMap ModelID"),
            gs.Tooltip("lineage", title="Cancer lineage"),
            gs.Tooltip("primaryDisease", title="Primary disease"),
            gs.Tooltip("subtype", title="Cancer subtype"),
            gs.Tooltip("growthPattern", title="Growth pattern"),
            gs.Tooltip("sampleOrigin", title="Primary/metastatic origin"),
        ],
    ),
    views=[lineage, growth, origin, sample_labels],
    overhang=OverhangConfig(bottom=True),
)

hovered = gs.selection_point(
    "hovered",
    on="mousemove",
    clear="mouseleave",
    toggle=False,
    persist=False,
    empty=False,
)
cells = (
    gs.Chart(gs.Data(url=DATA + "expression-zscores.csv"))
    .transform_regex_fold(columnRegex=r"^(gene\d+)$", asKey="feature", asValue="value")
    .transform_lookup(
        from_=cell_lines, key="sample", values=["row", "cellLine", "lineage", "subtype"]
    )
    .transform_lookup(
        from_=gs.Data(
            url=DATA + "genes.csv",
            format=gs.data_format(
                parse={
                    "column": "number",
                    "entrezId": "number",
                    "meanLog2Tpm": "number",
                    "sdLog2Tpm": "number",
                }
            ),
        ),
        key="feature",
        values=["column", "symbol", "entrezId", "cluster", "meanLog2Tpm", "sdLog2Tpm"],
    )
    .transform_formula(
        expr="datum.value * datum.sdLog2Tpm + datum.meanLog2Tpm", as_="log2Tpm"
    )
    .add_params(hovered)
    .mark_rect(stroke="#0f172a")
    .encode(
        x=gs.X("column:I").axis(None),
        y=gs.Y("row:I").axis(None),
        color=gs.Color("value:Q")
        .scale(
            domain=[-2.5, 0, 2.5], range=["#2166ac", "#f7f7f7", "#b2182b"], clamp=True
        )
        .legend(title="Gene z score"),
        strokeWidth=gs.StrokeWidth(gs.value(0)).condition(gs.condition(hovered, 1.5)),
        order=gs.Order(0).condition(gs.condition(hovered, 1)),
        tooltip=[
            gs.Tooltip("cellLine", title="Cell line"),
            gs.Tooltip("sample", title="DepMap ModelID"),
            gs.Tooltip("lineage", title="Cancer lineage"),
            gs.Tooltip("subtype", title="Cancer subtype"),
            gs.Tooltip("symbol", title="Gene"),
            gs.Tooltip("entrezId", title="Entrez ID"),
            gs.Tooltip("cluster", title="Gene cluster"),
            gs.Tooltip("value:Q", title="Gene z score", format=".2f"),
            gs.Tooltip("log2Tpm:Q", title="log2(TPM + 1)", format=".3f"),
        ],
    )
    .properties(name="cells")
)
feature_labels = (
    gs.Chart(genes)
    .mark_text(
        align="right",
        baseline="middle",
        fitToBand=True,
        flushX=False,
        angle=-90,
        dx=-8,
        size=8,
        color="#334155",
        clip="x",
        tooltip=None,
    )
    .encode(x=gs.X("column:I").axis(None), y=gs.value(0), text="symbol")
    .properties(name="featureLabels")
)

chart = (
    gs.surround(
        (cells + feature_labels).properties(name="heatmap"),
        surround=gs.SurroundSides(
            top=[column_tree], left=[row_tree], right=annotations
        ),
        spacing=8,
    )
    .properties(
        title=gs.Title(
            text="DepMap cancer cell-line expression",
            subtitle="60 cell lines / 72 variable genes - Ward clustering - DepMap 24Q4",
            anchor="start",
            fontSize=22,
            subtitleFontSize=12,
            offset=16,
        ),
        scales=gs.scales(
            x=gs.Scale(
                name="featureColumns",
                type="index",
                domain=[0, 71],
                paddingInner=0.03,
                paddingOuter=0.08,
                gapPositions=[29, 36, 41, 46, 53],
                gapWidth=5,
            ),
            y=gs.Scale(
                name="sampleRows",
                type="index",
                domain=[0, 59],
                reverse=True,
                paddingInner=0.03,
                paddingOuter=0.08,
                gapPositions=[24, 42, 52],
                gapWidth=5,
            ),
        ),
    )
    .resolve_legend(color="collected")
    .configure_style(
        {
            "metadata-column-title": StyleConfig(
                orient="bottom",
                anchor="middle",
                angle=-90,
                align="right",
                baseline="middle",
                fontSize=8,
                fontWeight="normal",
                color="#334155",
                offset=8,
            )
        }
    )
    .configure_legend(
        orient="bottom",
        direction="horizontal",
        gradientLength=110,
        titleOrient="top",
        offset=8,
        labelFontSize=10,
        titleFontSize=11,
        titleFontWeight="bold",
        symbolSize=49,
        spacing=28,
        rowPadding=4,
        columnPadding=12,
        layout=gs.LegendLayout(
            bottom=gs.LegendRegionLayout(
                anchor="middle",
                direction="horizontal",
                wrap=True,
            )
        ),
    )
)
