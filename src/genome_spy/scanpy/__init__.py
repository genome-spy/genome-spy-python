"""Short import path for the optional Scanpy plotting integration.

The implementation lives in :mod:`genome_spy.integrations.scanpy`.
Importing either namespace leaves the scientific stack unloaded.
"""

from genome_spy.integrations.scanpy import selection_mask
from genome_spy.scanpy import pl

__all__ = ["pl", "selection_mask"]
