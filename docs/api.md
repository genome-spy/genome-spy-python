---
html_theme.sidebar_secondary.remove: false
---

# API reference

The public API is intentionally small: chart construction, encoding channels,
composition, and notebook rendering.

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
