---
html_theme.sidebar_secondary.remove: false
---

# API reference

The public API is intentionally small: chart construction, encoding channels,
composition, and notebook rendering.

Generated `configure(...)` and `configure_* (...)` methods on `Chart` and
composition specs are the preferred way to author top-level config. Helper
constructors such as `gs.config(...)` and `gs.view_config(...)` remain
available as lightweight schema wrappers.

## Chart

```{eval-rst}
.. currentmodule:: genome_spy

.. autoclass:: Chart
   :members:
   :undoc-members:
   :show-inheritance:
```

## Encoding channels

```{eval-rst}
.. autoclass:: X
.. autoclass:: Y
.. autoclass:: Color
.. autoclass:: Size
.. autoclass:: Text
.. autoclass:: Opacity
.. autofunction:: Locus
.. autofunction:: value
```

## Composition

```{eval-rst}
.. autofunction:: layer
.. autofunction:: hconcat
.. autofunction:: vconcat
.. autofunction:: concat
```

## Notebook rendering

```{eval-rst}
.. autoclass:: JupyterChart
   :members:
```
