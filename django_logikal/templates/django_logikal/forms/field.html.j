{% if field.use_fieldset %}
  {# djlint: off #}
  <fieldset
    {%- if field.aria_describedby %} aria-describedby="{{ field.aria_describedby }}"{% endif %}>
    {% if field.label %}{{ field.legend_tag() }}{% endif %}
  {# djlint: on #}
{% else %}
  {% if field.label %}{{ field.label_tag() }}{% endif %}
{% endif %}
{{ field }}
{{ field.errors }}
{% if field.help_text %}
  <div class="helptext"{% if field.auto_id %} id="{{ field.auto_id }}-helptext"{% endif %}>
    {{- field.help_text|safe -}}
  </div>
{% endif %}
{% if field.use_fieldset %}</fieldset>{% endif %}
