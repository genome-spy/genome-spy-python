"""Public package interface for genome_spy."""

from genome_spy.api import (
    Color,
    ConcatChart,
    HConcatChart,
    JupyterChart,
    LayerChart,
    Opacity,
    Size,
    Text,
    TopLevelSpec,
    VConcatChart,
    X,
    X2,
    Y,
    Y2,
    Chart,
    concat,
    hconcat,
    layer,
    value,
    vconcat,
)
from genome_spy import datasets

__all__ = [
    "__version__",
    "Chart",
    "Color",
    "ConcatChart",
    "HConcatChart",
    "JupyterChart",
    "LayerChart",
    "Opacity",
    "Size",
    "Text",
    "TopLevelSpec",
    "VConcatChart",
    "X",
    "X2",
    "Y",
    "Y2",
    "concat",
    "datasets",
    "hconcat",
    "layer",
    "value",
    "vconcat",
]

__version__ = "0.1.0"
