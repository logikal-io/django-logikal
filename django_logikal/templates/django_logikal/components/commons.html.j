{% macro _render_menu_items(
  items, request, dropdown_icon, id_postfix, horizontal=none, nested=false
) %}
  {% for item in items %}
    {% set current = (item.view_name == url_name(request)) if request|default(none) else false %}
    <li role="none">
      {% if item.submenu %}
        {% set render_horizontal = horizontal is true or (horizontal is none and nested) %}
        <button type="button"
                class="icon dropdown{% if render_horizontal %} horizontal{% endif %}"
                role="menuitem"
                id="{{ item.id }}-{{ id_postfix }}"
                aria-haspopup="menu"
                aria-expanded="false">
          {{ item.title }}
          {{ include_static(dropdown_icon) }}
        </button>
        <menu role="menu" class="popover">
          {{ _render_menu_items(
            items=item.submenu, request=request, dropdown_icon=dropdown_icon,
            id_postfix=id_postfix, horizontal=horizontal, nested=true
          ) }}
        </menu>
      {% else %}
        {% set menu_url = url(viewname=item.view_name, kwargs=item.view_kwargs) %}
        <a role="menuitem"
           id="{{ item.id }}-{{ id_postfix }}"
           class="button{% if current %} disabled{% endif %}"
           {% if current %}aria-current="page"{% else %}href="{{ menu_url }}"{% endif %}>
          {{ item.title }}
        </a>
      {% endif %}
    </li>
  {% endfor %}
{% endmacro %}

{% macro desktop_menu(
  items, request, id='menu-desktop', dropdown_icon='django_logikal/icons/chevron-down.svg'
) %}
  {#
  Render a desktop menu bar.

  Args:
    items (list[~django_logikal.components.commons.MenuItem]): The menu items to use.
    request (~django.http.HttpRequest | None): The HTTP request to use.
    id (str): The menu ID to use.
    dropdown_icon (str): The path for the dropdown icon to use.

  .. jinja:example::

    <nav>
      {{ commons.desktop_menu([
        menu_item(title='Home', view_name='main:home'),
        menu_item(title='Info', submenu=[
          menu_item(title='Home', id='submenu-home', view_name='main:home'),
          menu_item(title='About', view_name='main:about'),
          menu_item(title='Components', submenu=[
            menu_item(title='Home', id='subsubmenu-home', view_name='main:home'),
            menu_item(title='Buttons', view_name='main:buttons'),
          ]),
        ]),
        menu_item(title='Blog', submenu=[
          menu_item(title='Newest', view_name='main:blog', view_kwargs={'order': 'desc'}),
          menu_item(title='Oldest', view_name='main:blog', view_kwargs={'order': 'asc'}),
        ]),
      ], request=request) }}
    </nav>

  #}
  <menu role="menubar" id="{{ id }}" class="desktop">
    {{ _render_menu_items(
      items, request=request, dropdown_icon=dropdown_icon, id_postfix='desktop'
    ) }}
  </menu>
{% endmacro %}

{% macro mobile_menu(
  items, request,
  id='menu-mobile',
  dropdown_icon='django_logikal/icons/chevron-down.svg',
  menu_icon='django_logikal/icons/menu.svg',
  menu_close_icon='django_logikal/icons/x.svg'
) %}
  {#
  Render a mobile menu.

  Args:
    items (list[~django_logikal.components.commons.MenuItem]): The menu items to use.
    request (~django.http.HttpRequest | None): The HTTP request to use.
    id (str): The menu ID to use.
    dropdown_icon (str): The path for the dropdown icon to use.
    menu_icon (str): The path for the menu icon to use.
    menu_close_icon (str): The path for the menu close icon to use.

  .. jinja:example::

    <nav>
      {{ commons.mobile_menu([
        menu_item(title='Home', view_name='main:home'),
        menu_item(title='Info', submenu=[
          menu_item(title='Home', id='submenu-home', view_name='main:home'),
          menu_item(title='About', view_name='main:about'),
          menu_item(title='Components', submenu=[
            menu_item(title='Home', id='subsubmenu-home', view_name='main:home'),
            menu_item(title='Buttons', view_name='main:buttons'),
          ]),
        ]),
        menu_item(title='Blog', submenu=[
          menu_item(title='Newest', view_name='main:blog', view_kwargs={'order': 'desc'}),
          menu_item(title='Oldest', view_name='main:blog', view_kwargs={'order': 'asc'}),
        ]),
      ], request=request) }}
    </nav>

  #}
  <div class="menu-mobile-container">
    <button class="icon toggle"
            id="{{ id }}-toggle"
            type="button"
            title="{{ _('Show menu') }}"
            aria-label="{{ _('Show menu') }}"
            data-active-title="{{ _('Hide menu') }}"
            data-active-aria-label="{{ _('Hide menu') }}"
            aria-haspopup="true"
            aria-controls="menu-mobile"
            aria-expanded="false">
      <span class="inactive" aria-hidden="false">{{ include_static(menu_icon) }}</span>
      <span class="active" aria-hidden="true">{{ include_static(menu_close_icon) }}</span>
    </button>
    <menu id="{{ id }}" role="menubar" class="mobile popover">
      {{ _render_menu_items(
        items, request=request, dropdown_icon=dropdown_icon, id_postfix='mobile', horizontal=false
      ) }}
    </menu>
  </div>
{% endmacro %}

{% macro language_switcher(
  current_language_code, action_url, csrf_input, id='language-switcher',
  text=none, available_languages=none, dropdown_icon='django_logikal/icons/chevron-down.svg'
) %}
  {#
  Render a language switcher.

  Args:
    current_language_code (str): The current language code.
    action_url (str): The action URL to use.
    csrf_input (str): The CSRF input element to use.
    id (str): The ID to use for the menu element.
    text (str): The button text to use. Defaults to the current language name.
    available_languages (list[tuple[str, str]]): A list of available language code, language name
      pairs. Defaults to the configured languages.
    dropdown_icon (str): The path for the dropdown icon to use.

  .. jinja:example::

    <nav>
      {{ commons.language_switcher(
        current_language_code=language(),
        action_url=url('set_language'),
        csrf_input=csrf_input
      ) }}
    </nav>

  #}
  {% set available_languages = dict(available_languages or languages()) %}
  <menu class="language-switcher" id="{{ id }}" role="menu">
    <li role="none">
      <button type="button"
              id="{{ id }}-toggle"
              class="icon dropdown"
              role="menuitem"
              title="{{ _('Change language') }}"
              aria-label="{{ _('Change language') }}"
              aria-haspopup="menu"
              aria-expanded="false"
              aria-controls="form-language-menu">
        {{ text or available_languages[current_language_code] }}
        {{ include_static(dropdown_icon) }}
      </button>
      <form id="form-language-menu" action="{{ action_url }}" method="post">
        {{ csrf_input }}
        <menu role="menu" class="popover">
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
    </li>
  </menu>
{% endmacro %}

{% macro messages(messages, id='messages') %}
  {#
  Show messages as a popover notification.

  Args:
    messages (list[str] | None): A list of messages to show.
    id (str): The element ID to use.

  .. jinja:example::

    <div class="example-page">
      {{ commons.messages(messages|default(none)) }}
    </div>

  #}
  {% if messages %}
    <div id="{{ id }}" class="popover notification">
      <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
      </ul>
      <button id="{{ id }}-dismiss" type="button" class="active">{{ _('Dismiss') }}</button>
    </div>
  {% endif %}
{% endmacro %}
