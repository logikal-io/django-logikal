{%- for name, value in (
  attrs if attrs is defined else (widget.attrs if widget is defined else {})
).items() -%}
  {%- if value is not false %} {{ name }}
    {%- if value is not true %}="{{ value }}"{% endif -%}
  {%- endif -%}
{%- endfor -%}
