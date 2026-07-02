"""Schema wrapper generation helpers for GenomeSpy Python.

This package intentionally mirrors Altair's ``tools/schemapi`` layout and
maintainer workflow, but the implementation starts small and GenomeSpy-specific.
It gives us a local place to evolve schema inspection and wrapper generation
without editing generated package code by hand. The installed runtime is
maintained in ``src/genome_spy/schemapi.py``.
"""
