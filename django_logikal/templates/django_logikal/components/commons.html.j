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
  name, label, type='text', value=none, id=none, required=false, disabled=false, read_only=false,
  placeholder=none, error_text=none, min_length=none, max_length=none, autocomplete=none,
  spellcheck=none
) %}
  {#
  Render an input field.

  Args:
    name (str): The name to use.
    label (str): The label text to use.
    type (str): The input type to use.
    value (str): The initial values to use.
    id (str): The input ID to use. Defaults to the name.
    required (bool): Whether the input field is required.
    disabled (bool): Whether the input element is disabled.
    read_only (bool): Whether the input element is editable or not.
    placeholder (str): The placeholder string to use.
    error_text (str): The error message to show.
    min_length (int): The minimum length to use.
    max_length (int): The maximum length to use.
    autocomplete (str): The autocomplete attributes to use.
    spellcheck (bool): Whether the input element should be checked for spelling errors.

  .. jinja:example::

    {{ commons.input_field(
      name='username', label='Email address', type='email', required=True,
      placeholder=_('email@example.com'), error_text=_('This email is invalid.'),
    ) }}

  #}
  <div class="input-field">
    <label for="{{ id or name }}">{{ label or name|title }}</label>
    <input id="{{ id or name }}" name="{{ name }}" type="{{ type }}"
      {%- if value %} value="{{ value }}"{% endif -%}
      {%- if placeholder %} placeholder="{{ placeholder }}"{% endif -%}
      {%- if required %} required{% endif -%}
      {%- if min_length %} minlength="{{ min_length }}"{% endif -%}
      {%- if max_length %} maxlength="{{ max_length }}"{% endif -%}
      {%- if autocomplete %} autocomplete="{{ autocomplete }}"{% endif -%}
      {%- if spellcheck is not none %} spellcheck="{{ spellcheck|str|lower }}"{% endif -%}
      {%- if disabled %} disabled{% endif -%}
      {%- if read_only %} readonly{% endif -%}
    >
    {% if error_text %}<p class="error">{{ error_text }}</p>{% endif %}
  </div>
{% endmacro %}

{% macro icon_button(text, icon, classes=none) %}
  {#
  Render a link button with an icon.

  Args:
    text (str): The text to use.
    icon (str): The path for the icon to include.
    classes (str): The classes to use.

  #}
  <button class="icon{% if classes %} {{ classes }}{% endif %}">
    {{- include_static(icon) -}}
    <span>{{- text -}}</span><span class="counterweight"></span></button>
{% endmacro %}
