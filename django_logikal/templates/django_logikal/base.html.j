<!DOCTYPE html>
<html lang="{%- block language -%}{{ language() }}{%- endblock -%}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="
      {%- filter join_lines -%}
        {%- block description required -%}{%- endblock -%}
      {%- endfilter -%}">

    <title>{% filter join_lines %}{% block title required %}{% endblock %}{% endfilter %}</title>

    {% if htmx|default(false) %}
      <meta name="htmx-config"
            content='{{ htmx_config|default({
        'allowEval': false,
        'allowScriptTags': false,
        'inlineScriptNonce': csp_nonce|str,
        'inlineStyleNonce': csp_nonce|str,
      })|tojson }}'>
      {{ htmx_script(nonce=csp_nonce, version=2) }}
    {% endif %}
    {% block component_head %}{% endblock %}
    {% block head %}{% endblock %}
  </head>
  {# djlint: off #}
  <body
    {%- filter join_lines(spacer=true) -%}
      {%- block bodyattributes %}{% endblock -%}
    {%- endfilter -%}
    {%- if htmx|default(false) %} data-hx-headers='{"x-csrftoken": "{{ csrf_token }}"}'{% endif -%}
    >
    {% block body required %}{% endblock %}
  </body>
  {# djlint: on #}
</html>
