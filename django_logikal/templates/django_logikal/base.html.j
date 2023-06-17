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

    {% block head %}{% endblock %}
  </head>
  <body{% filter join_lines(spacer=true) %}{% block bodyattributes %}{% endblock %}{% endfilter %}>
    {% block body required %}{% endblock %}
  </body>
</html>
