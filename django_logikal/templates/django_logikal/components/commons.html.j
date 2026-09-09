{% macro menu(
  items, request,
  arrow_icon='django_logikal/icons/arrow.svg', menu_icon='django_logikal/icons/menu.svg'
) %}
  {#
  Render a menu bar.

  Args:
    items (:py:class:`list` of :py:class:`~django_logikal.components.commons.MenuItem`):
      The menu items to use.
    request (:py:class:`django.http.HttpRequest` | :py:data:`None`): The HTTP request to use.
    arrow_icon: The path for the arrow icon to use.
    menu_icon: THe path for the menu icon to use.

  .. jinja:example::

    <nav>
      {{ commons.menu([
        menu_item(title='About', view_name='main:about'),
        menu_item(title='Components', view_name='main:components'),
        menu_item(
          title='Blog',
          submenu=[menu_item(title='Post', view_name='main:post', view_kwargs={'year': '2000'})]
        ),
      ], request=request) }}
    </nav>

  #}
  {% macro _render_menu_items(items, request, type, nested=false) %}
    {% for item in items %}
      {% set active = (item.view_name == url_name(request)) if request|default(none) else false %}
      <li role="none"{% if active %} class="active"{% endif %}>
        {% if item.submenu %}
          <button type="button"
                  class="arrow-toggle{% if nested %} horizontal{% endif %}"
                  role="menuitem"
                  id="{{ item.id }}-{{ type }}"
                  aria-haspopup="menu"
                  aria-expanded="false">
            {{ item.title }}
            {{ include_static(arrow_icon) }}
          </button>
          <menu role="menu" class="group">
            {{ _render_menu_items(
              items=item.submenu, request=request, type=type, nested=true
            ) }}
          </menu>
        {% else %}
          {% set menu_url = url(viewname=item.view_name, kwargs=item.view_kwargs) %}
          <a role="menuitem"
             id="{{ item.id }}-{{ type }}"
             {%- if active %} aria-current="page"{% else %} href="{{ menu_url }}"{% endif %}>
            {{ item.title }}
          </a>
        {% endif %}
      </li>
    {% endfor %}
  {% endmacro %}

  {% for type in ['desktop', 'mobile'] %}
    <menu role="menubar" class="{{ type }}">
      {{ _render_menu_items(items=items, request=request, type=type) }}
    </menu>
  {% endfor %}

  <button id="menu-icon"
          class="mobile-menu-icon"
          type="button"
          aria-label="{{ _('Menu') }}"
          aria-haspopup="menu"
          aria-expanded="false">{{ include_static(menu_icon) }}</button>
{% endmacro %}

{% macro icon_button(
  text, icon, id=none, classes=none, title=none,
  aria_label=none, aria_haspopup=none, aria_expanded=none, aria_controls=none
) %}
  {#
  Render a link button with an icon.

  Args:
    text (str): The text to use.
    icon (str): The path for the icon to include.
    id (str): The ID to use.
    classes (str): The classes to use.
    title (str): The title to use.
    aria_label (str): The ARIA label to use.
    aria_haspopup (str | :py:class:`bool`): Whether the element can trigger a popup.
    aria_expanded (bool): Whether the controlled elements are expanded.
    aria_controls (str): The ID of the element which this button controls.

  #}
  <button type="button"
          class="icon{% if classes %} {{ classes }}{% endif %}"
          {%- if id %} id="{{ id }}"{% endif -%}
          {%- if title %} title="{{ title }}"{% endif -%}
          {%- if aria_label %} aria-label="{{ aria_label }}"{% endif -%}
          {%- if aria_haspopup %} aria-haspopup="{{ aria_haspopup|str|lower }}"{% endif -%}
          {%- if aria_expanded is not none %} aria-expanded="{{
            aria_expanded|str|lower
          }}"{% endif -%}
          {%- if aria_controls %} aria-controls="{{ aria_controls }}"{% endif %}>
    {{- include_static(icon) -}}
    <span>{{ text }}</span>
  </button>
{% endmacro %}

{% macro language_switcher(
  current_language_code,
  action_url,
  csrf_input,
  text=none,
  available_languages=none,
  arrow_icon='django_logikal/icons/arrow.svg'
) %}
  {#
  Render a language switcher.

  Args:
    current_language_code (str): The current language code.
    action_url (str): The action URL to use.
    csrf_input (str): The CSRF input element to use.
    text (str): The button text to use. Defaults to the current language name.
    available_languages (list): A list of a tuple of available language code, language name pairs.
      Defaults to the configured languages.
    arrow_icon (str): The path for the arrow icon to use.

  .. jinja:example::

    {{ commons.language_switcher(
      current_language_code=language(),
      action_url=url('set_language'),
      csrf_input=csrf_input
    ) }}

  #}
  {% set available_languages = dict(available_languages or languages()) %}
  <div id="language-switcher" class="dropdown-form-menu">
    <button type="button"
            id="language-switcher-toggle"
            class="arrow-toggle neutral light"
            title="{{ _('Change language') }}"
            aria-label="{{ _('Change language') }}"
            aria-haspopup="menu"
            aria-expanded="false"
            aria-controls="form-language-menu">
      {{ text or available_languages[current_language_code] }}
      {{ include_static(arrow_icon) }}
    </button>
    <form id="form-language-menu" class="subgroup" action="{{ action_url }}" method="post">
      {{ csrf_input }}
      <menu role="menu">
        {% for language_code, language_name in available_languages.items() %}
          {% if language_code != current_language_code %}
            <li role="none">
              <button name="language" value="{{ language_code }}" type="submit" role="menuitem">
                {% language language_code %}{{ language_name }}{% endlanguage %}
              </button>
            </li>
          {% endif %}
        {% endfor %}
      </menu>
    </form>
  </div>
{% endmacro %}
