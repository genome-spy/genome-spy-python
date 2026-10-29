"""Optional Scanpy-compatible plotting with native GenomeSpy charts.

Importing this namespace does not import Scanpy or the scientific stack.
Install ``genome-spy-python[scanpy]`` to call its plotting functions.
"""

from genome_spy.integrations.scanpy import pl
from genome_spy.integrations.scanpy._embedding.selection import selection_mask

__all__ = ["pl", "selection_mask"]
