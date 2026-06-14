{% macro menu(items, request, arrow='django_logikal/icons/arrow.svg', menu='django_logikal/icons/menu.svg') %}
  {#
  Render a menu bar.

  Args:
    item_urls (dict): The mapping of menu items to URL names.
    request (:py:class:`django.http.HttpRequest` | :py:data:`None`): The HTTP request to use.

  .. jinja:example::

    {{ commons.menu([
      MenuItem(title='About', view_name='main:about'),
      MenuItem(title='Components', view_name='main:components'),
      MenuItem(
        title='Blog',
        view_kwargs={'year': '2000'},
        submenu=[
          MenuItem(title='Blog Post', view_name='main:blog_post')
        ]
      ),
    ], request=request) }}

  #}
  {% macro render_menu_items(items, request, type) %}
    {% for item in items %}
      {% set active = (item.view_name == url_name(request)) if request else none %}
      <li role="none"{% if active %} class="active"{% endif %}>
        <a role="menuitem" id="{{ type }}_{{ item.id }}"
           {%- if not active and not item.submenu %}
            href="{{ url(viewname=item.view_name, kwargs=item.view_kwargs) }}"
           {% endif -%}>
          {{ item.title }}
          {% if item.submenu %}
            {{ include_static(arrow) }}
          {% endif %}
        </a>
        {%- if item.submenu -%}
          <ul role="menu" class="menu group">
            {{ render_menu_items(item.submenu, request, type) }}
          </ul>
        {%- endif -%}
      </li>
    {% endfor %}
  {% endmacro %}

  {% for type in ['desktop', 'mobile'] %}
    <menu role="menu" class="tabs {{ type }}">
      {{ render_menu_items(items, request, type) }}
    </menu>
  {% endfor %}

  <button class="mobile-menu-icon" id="menu_icon" aria-label="Menu" aria-expanded="false">
    {{ include_static(menu) }}
  </button>
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
