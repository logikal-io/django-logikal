{% macro test_localization(text, text_with_default=_('flavor')) %}
  <p><b>Content:</b> {{ text }} {{ text_with_default }}</p>
{% endmacro %}
