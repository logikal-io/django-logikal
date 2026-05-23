<ul class="{{ error_class }}"
    {%- if errors and errors.field_id %} id="{{ errors.field_id }}_error"{% endif %}>
  {% for error in errors or [] %}
    <li>{{ error }}</li>
  {% endfor %}
</ul>
