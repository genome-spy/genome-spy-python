{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:

   {% block methods %}
   {% set own_methods = methods | reject("equalto", "__init__") | list %}
   {% if own_methods %}
   .. rubric:: Methods

   .. autosummary::
   {% for item in own_methods %}
      ~{{ objname }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
