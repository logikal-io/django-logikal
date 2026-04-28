{% macro menu(items, request, icon='arrow.svg') %}
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
    {% for item in items %}
      {% set active = (item.view_name == url_name(request)) if request else none %}
      <li role="none"{% if active %} class="active"{% endif %}>
        <a role="menuitem"
           {%- if not active and not item.submenu %}
            href="{{ url(viewname=item.view_name, kwargs=item.view_kwargs) }}"
           {% endif -%}>
          {{ item.title }}
          {% if item.submenu %}
            {{ include_static(icon) }}
          {% endif %}
        </a>
        {%- if item.submenu -%}
          <ul role="menu" class="menu group">
            {% for sub in item.submenu %}
            {% set sub_active = (sub.view_name in url_name(request)) if request else none %}
            <li role="none" {% if sub_active %} class="active"{% endif %}>
              <a role="menuitem"
                 {%- if not sub_active %}
                  href="{{ url(viewname=sub.view_name, kwargs=sub.view_kwargs) }}"
                 {% endif -%}>
                {{ sub.title }}
              </a>
            </li>
            {% endfor %}
          </ul>
        {%- endif -%}
      </li>
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
