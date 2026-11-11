{% extends 'django_logikal/base.html.j' %}
{% import 'django_logikal/components/commons.html.j' as commons %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}
  This is a dynamic site
  used for demonstration and testing purposes.
{% endblock %}

{% block component_head %}{{ component_head('composition', 'text') }}{% endblock %}
{% block head %}
  <link rel="icon" href="{{ static('favicon.png') }}">

  <!-- Preload mobile menu font to avoid FOUT -->
  <link rel="preload"
        href="{{ static('django_logikal/fonts/Lato-Bold.woff2') }}"
        as="font"
        type="font/woff2"
        crossorigin>

  <link rel="stylesheet" href="{{ static('django_logikal/css/fonts.css') }}">
  <link rel="stylesheet" href="{{ static('style.css') }}">
{% endblock %}

{% block body %}
  <header>
    <nav>
      <a href="{{ url('dynamic_site:home') }}" class="button logo" aria-label="Go to home page">
        {{ include_static('logikal_logo.svg') }}
      </a>
      {% set view_kwargs = {'url_path_arg': 'path'} %}
      {% set menu_items = [
        menu_item(title='Home', view_name='dynamic_site:home'),
        menu_item(title='Errors', submenu=[
          menu_item(title='404', view_name='error:404', id='submenu-404'),
          menu_item(title='500', view_name='error:500', id='submenu-500'),
          menu_item(title='Server Errors', submenu=[
            menu_item(title='400', view_name='error:400', id='subsubmenu-400'),
            menu_item(title='500', view_name='error:500', id='subsubmenu-500'),
          ]),
          menu_item(title='Page Not Found Errors', submenu=[
            menu_item(title='403', view_name='error:403', id='subsubmenu-403'),
            menu_item(title='404', view_name='error:404', id='subsubmenu-404'),
          ]),
        ]),
        menu_item(title='Components', submenu=[
          menu_item(title='Text', view_name='dynamic_site:components/text'),
        ]),
        menu_item(title='Templates', view_name='dynamic_site:templates', view_kwargs=view_kwargs),
      ] %}

      {{ commons.desktop_menu(menu_items, request=request|default(none)) }}

      <aside>
        {% if request|default(none)
          and request.resolver_match.view_name == 'dynamic_site_localized:localization' %}
          {{ commons.language_switcher(
            current_language_code=language(),
            action_url=url('set_language'),
            csrf_input=csrf_input,
            compact_button=true,
          ) }}
        {% endif %}
        {% if request|default(none) and request.user.is_authenticated %}
          <a href="{{ url('account') }}" class="button active">Account</a>
        {% else %}
          <a href="{{ url('account_auth') }}" class="button active">Log in</a>
        {% endif %}
      </aside>

      {{ commons.mobile_menu(menu_items, request=request|default(none)) }}
    </nav>
  </header>
  <main>
    {{ commons.messages(messages|default(none)) }}
    {% block main %}{% endblock %}
  </main>
{% endblock %}
