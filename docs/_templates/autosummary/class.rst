{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :inherited-members:
   :show-inheritance:

   {% block methods %}
   {% set documented_methods = methods | reject("equalto", "__init__") | list %}
   {% if documented_methods %}
   .. rubric:: Methods

   .. autosummary::
   {% for item in documented_methods %}
      ~{{ objname }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: Attributes

   .. autosummary::
   {% for item in attributes %}
      ~{{ objname }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
