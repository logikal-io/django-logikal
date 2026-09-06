<!-- Theme styles -->
{% if theme_styles %}
  {% for style in theme_styles %}
    {% if style.media %}
      <link rel="stylesheet" href="{{ style.href }}" media="({{ style.media }})">
    {% else %}
      <link rel="stylesheet" href="{{ style.href }}">
    {% endif %}
  {% endfor %}
{% endif %}
<!-- End of theme styles -->

<!-- Component styles -->
{% for style in component_styles %}
  <link rel="stylesheet" href="{{ style.href }}">
{% endfor %}
<!-- End of component styles -->

<!-- Component scripts -->
{% if scripts %}
  {% for script in scripts %}
    <script src="{{ script.src }}"
            {%- if script.module %} type="module"{% endif -%}
            {%- if script.defer %} defer{% endif %}></script>
  {% endfor %}
{% endif %}
<!-- End of component scripts -->
