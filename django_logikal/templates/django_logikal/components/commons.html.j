{% macro menu(item_urls, request) %}
  {#
  Render a menu bar.

  Args:
    item_urls (dict): The mapping of menu items to URL names.
    request (:py:class:`django.http.HttpRequest` | :py:data:`None`): The HTTP request to use.

  .. jinja:example::

    {{ commons.menu({
      'About': 'main:about',
      'Components': 'main:components',
      'Blog': {'view_name': 'main:blog', 'kwargs': {'year': '2000'}},
    }, request=request) }}

  #}
  <menu role="menu" class="tabs">
    {% for item_title, item in item_urls.items() %}
      {% set view_name = item['view_name'] if item|isinstance(dict) else item %}
      {% set url_args = item|exclude('view_name') if item|isinstance(dict) else {} %}
      {% set active = (view_name == url_name(request)) if request else none %}
      <li role="none"{% if active %} class="active"{% endif %}><a role="menuitem"
        {%- if not active %} href="{{ url(viewname=view_name, **url_args) }}"{% endif -%}
        >{{ item_title }}</a></li>
    {% endfor %}
  </menu>
{% endmacro %}

{% macro paragraph(faker, sentences=5) %}
  {# Generate a paragraph worth of fake text. #}
  {{ faker.paragraph(nb_sentences=sentences, variable_nb_sentences=false)|wordwrap }}
{% endmacro %}

{% macro input_field(
  name, label, type='text', id=none, required=false, placeholder=none, error_text=none
) %}
  {#
  Render an input field.

  Args:
    name (str): The name to use.
    label (str): The label text to use.
    type (str): The input type to use.
    id (str): The input ID to use. Defaults to the name.
    required (bool): Whether the input field is required.
    placeholder (str): The placeholder string to use.
    error_text (str): The error message to show.

  .. jinja:example::

    {{ commons.input_field(
      name='username', label='Email address', type='email', required=True,
      placeholder=_('email@example.com'), error_text=_('This email is invalid.'),
    ) }}

  #}
  <div class="input-field">
    <label for="{{ id or name }}">{{ label or name|title }}</label>
    <input id="{{ id or name }}" name="{{ name }}" type="{{ type }}"
      {% if placeholder %} placeholder="{{ placeholder }}"{% endif %}
      {% if required %} required{% endif %}>
    {% if error_text %}<p class="error">{{ error_text }}</p>{% endif %}
  </div>
{% endmacro %}

{% macro link_icon_button(text, href, icon, classes=none) %}
  {#
  Render a link button with an icon.

  Args:
    text (str): The text to use.
    href (str): The link target to use.
    icon (str): The path for the icon to include.
    classes (str): The classes to use.

  #}
  <a href="{{ href }}" class="button icon{% if classes %} {{ classes }}{% endif %}">
    {{- include_static(icon) -}}
    <span>{{- text -}}</span><span class="counterweight"></span></a>
{% endmacro %}
