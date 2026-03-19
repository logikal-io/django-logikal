{% macro test(text, text_with_default=_('local flavor')) %}
  <p><b>{{ _('Content:') }}</b> {{ text }} {{ text_with_default }} &ndash;
    {{ _('local realize inside') }}</p>
{% endmacro %}
