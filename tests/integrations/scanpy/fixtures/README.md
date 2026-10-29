# Scanpy reference fixtures

These JSON files contain deliberate numerical and geometry expectations. They
are not generated run reports. Tests never overwrite them. Review changes against
upstream behavior before accepting new expectations.

`api.json` keeps the public callable inventory and four legacy signatures that
Scanpy 1.12 hides behind forwarding wrappers. Other signatures are checked directly
against installed Scanpy.

Family input modules live in the parent directory. The browser image helper uses
the pinned Scanpy/scientific stack in `pyproject.toml` and `uv.lock`, with 100 DPI
display and 150 DPI export. Registered comparisons retain their original crops;
tests must not resize or fit images to hide differences.

Images, overlays, chart exports, recordings and logs stay in temporary directories.
There are no report writers, automatic fixture regenerators or manual benchmarks.
The small synthetic inputs use this project's MIT license. No downloaded dataset
or upstream tutorial image belongs here.
