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

{% macro icon_button(
  text, icon, id=none, classes=none, title=none,
  aria_label=none, aria_expanded=none, aria_controls=none
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
    aria_expanded (bool): Whether the controlled elements are expanded.
    aria_controls (str): The ID of the element which this button controls.

  #}
  <button
    {%- if id %} id="{{ id }}"{% endif %} class="icon{% if classes %} {{ classes }}{% endif %}"
    {%- if title %} title="{{ title }}"{% endif -%}
    {%- if aria_label %} aria-label="{{ aria_label }}"{% endif -%}
    {%- if aria_expanded is not none %} aria-expanded="{{ aria_expanded|str|lower }}"{% endif -%}
    {%- if aria_controls %} aria-controls="{{ aria_controls }}"{% endif -%}
    >
    {{- include_static(icon) -}}
    <span>{{ text }}</span></button>
{% endmacro %}

{% macro language_switcher(
  current_language_code,
  languages,
  action_url,
  csrf_input,
  text=none,
  icon='django_logikal/icons/globe.svg'
) %}
  {#
  Render a language switcher.

  Args:
    current_language_code (str): The current language code.
    languages (list): A list of a tuple of available language code, language name pairs.
    action_url (str): The action URL to use.
    csrf_input (str): The CSRF input element to use.
    text (str): The button text to use. Defaults to the current language name.
    icon (str): The path for the icon to include.

  .. jinja:example::

    {{ commons.language_switcher(
      current_language_code=language(),
      languages=settings.LANGUAGES,
      action_url=url('set_language'),
      csrf_input=csrf_input
    ) }}

  #}
  <div id="id_language_switcher" class="dropdown-form-menu">
    {{ icon_button(
      text=text or dict(languages)[current_language_code], icon=icon,
      id="id_language_switcher_toggle", classes='neutral',
      title=_('Change language'), aria_label=_('Change language'),
      aria_expanded=false, aria_controls='id_form_language_menu',
    ) }}
    <form id="id_form_language_menu" class="subgroup"
          action="{{ action_url }}" method="post" hidden>
      {{ csrf_input }}
      <menu>
        {% for language_code, language_name in languages %}
          {% if language_code != current_language_code %}
            <li>
              <button name="language" value="{{ language_code }}" type="submit">
                {% language language_code %}{{ language_name }}{% endlanguage %}
              </button>
            </li>
          {% endif %}
        {% endfor %}
      </menu>
    </form>
  </div>
{% endmacro %}
