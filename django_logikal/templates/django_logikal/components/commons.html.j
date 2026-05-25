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

{% macro icon_button(text, icon, id=none, classes=none) %}
  {#
  Render a link button with an icon.

  Args:
    text (str): The text to use.
    icon (str): The path for the icon to include.
    id (str): The ID to use.
    classes (str): The classes to use.

  #}
  <button
    {%- if id %} id="{{ id }}"{% endif %} class="icon{% if classes %} {{ classes }}{% endif %}">
    {{- include_static(icon) -}}
    <span>{{- text -}}</span><span class="counterweight"></span></button>
{% endmacro %}
