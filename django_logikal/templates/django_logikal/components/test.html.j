{% macro test_namespaced(text, text_with_default=_('external namespaced flavor')) %}
  <p><b>{{ _('Content:') }}</b> {{ text }} {{ text_with_default }} &ndash;
    {{ _('external namespaced realize inside') }}</p>
{% endmacro %}

{% macro test_imported(text, text_with_default=_('external imported flavor')) %}
  <p><b>{{ _('Content:') }}</b> {{ text }} {{ text_with_default }} &ndash;
    {{ _('external imported realize inside') }}</p>
{% endmacro %}

{% macro test_aliased(text, text_with_default=_('external aliased flavor')) %}
  <p><b>{{ _('Content:') }}</b> {{ text }} {{ text_with_default }} &ndash;
    {{ _('external aliased realize inside') }}</p>
{% endmacro %}
