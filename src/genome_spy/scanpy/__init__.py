"""Optional Scanpy-compatible plotting with native GenomeSpy charts.

Importing this namespace does not import Scanpy or the scientific stack.
Install ``genome-spy-python[scanpy]`` to call its plotting functions.
"""

from genome_spy.scanpy import pl

__all__ = ["pl"]
