{%- if use_tag -%}
  <{{ tag }}
    {%- if attrs %}{% include 'django_logikal/forms/attrs.html.j' %}{% endif -%}
    >{{ label }}</{{ tag }}>
{%- else -%}
  {{- label -}}
{%- endif -%}
