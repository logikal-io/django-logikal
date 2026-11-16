{% if theme_styles %}
  <!-- Theme styles -->
  {% for style in theme_styles %}
    {% if style.media %}
      <link rel="stylesheet" href="{{ style.href }}" media="({{ style.media }})">
    {% else %}
      <link rel="stylesheet" href="{{ style.href }}">
    {% endif %}
  {% endfor %}
  <!-- End of theme styles -->
{% endif %}

{% if component_styles %}
  <!-- Component styles -->
  {% for style in component_styles %}
    <link rel="stylesheet" href="{{ style.href }}">
  {% endfor %}
  <!-- End of component styles -->
{% endif %}

{% if component_scripts %}
  <!-- Component scripts -->
  {% for script in component_scripts %}
    <script src="{{ script.src }}"
            {%- if script.module %} type="module"{% endif -%}
            {%- if script.defer %} defer{% endif %}></script>
  {% endfor %}
  <!-- End of component scripts -->
{% endif %}
