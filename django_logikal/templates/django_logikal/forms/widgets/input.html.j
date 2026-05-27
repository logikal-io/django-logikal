<input
  name="{{ widget.name }}"
  type="{{ widget.type }}"
  {% if widget.value is not none %}value="{{ widget.value }}"{% endif %}
  {%- if widget.attrs %}{% include 'django_logikal/forms/attrs.html.j' %}{% endif -%}
  >
