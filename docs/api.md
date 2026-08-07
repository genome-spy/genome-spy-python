---
html_theme.sidebar_secondary.remove: false
---

# API reference

The public API covers chart construction, every schema-derived encoding
channel, composition, schema helpers, and notebook rendering.

Generated `configure(...)` and `configure_* (...)` methods on `Chart` and
composition specs are the preferred way to author top-level config. Helper
constructors such as `gs.config(...)` and `gs.view_config(...)` remain
available as lightweight schema wrappers.

For direct top-level schema properties, charts and compositions also expose
generated-style `with_* (...)` setters such as `chart.with_view(...)`,
`chart.with_config(...)`, and `chart.with_scales(...)`.

Small helper constructors such as `gs.expr(...)`, `gs.title(...)`,
`gs.step(...)`, `gs.parse(...)`, `gs.data_format(...)`, and
`gs.dynamic_opacity(...)` are still part of the intended ergonomic layer.
Helpers around top-level config or mapping-shaped schema surfaces such as
`gs.config(...)`, `gs.view_config(...)`, `gs.view(...)`, `gs.scales(...)`,
and `gs.param(...)` should stay small and are mainly compatibility wrappers
around the generated schema/config surface. In the example gallery, the
remaining uses of `gs.scales(...)` and `gs.param(...)` are intentional where
they keep the visualization code shorter and easier to read.

## Chart

```{eval-rst}
.. currentmodule:: genome_spy

.. autoclass:: Chart
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:
```

## Public exports

```{eval-rst}
.. automodule:: genome_spy.api
   :members:
   :imported-members:
   :exclude-members: Chart, JupyterChart
   :member-order: bysource
```

## Notebook rendering

```{eval-rst}
.. autoclass:: JupyterChart
   :members:
```
