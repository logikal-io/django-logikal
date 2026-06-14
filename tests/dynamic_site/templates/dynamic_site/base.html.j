{% extends 'django_logikal/base.html.j' %}
{% import 'django_logikal/components/commons.html.j' as commons %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}
  This is a dynamic site
  used for demonstration and testing purposes.
{% endblock %}

{% block component_head %}{{ component_head('commons') }}{% endblock %}
{% block head %}
  <link rel="icon" href="{{ static('favicon.png') }}">
  <link rel="stylesheet" href="{{ static('css/style.css') }}">
{% endblock %}

{% block body %}
  <header>
    <nav>
      <a href="{{ url('dynamic_site:home') }}" class="logo" aria-label="Go to home page">
        {{ include_static('logikal_logo.svg') }}
      </a>
      {# djlint:off T001 #} {# TODO: show a list of options for the error pages #}
      {% set menu_items = [
          MenuItem(title='Home', view_name='dynamic_site:home'),
          MenuItem(title='Errors',
            submenu=[
              MenuItem(title='Server Errors',
                submenu=[
                  MenuItem(title='400', view_name='error:400'),
                  MenuItem(title='500', view_name='error:500')
                ]
              ),
              MenuItem(title='Page Not Found Errors',
                submenu=[
                  MenuItem(title='403', view_name='error:403'),
                  MenuItem(title='404', view_name='error:404')
                ]
              ),
            ]
          ),
          MenuItem(title='Templates', view_name='dynamic_site:templates',
          view_kwargs={'arg': 'extensions'}),
          MenuItem(title='Partials', view_name='dynamic_site:partials'),
          MenuItem(title='Admin', view_name='admin:index'),
          MenuItem(title='API', view_name='api-root'),
      ]
      %}
      {{ commons.menu(menu_items, request=request|default(none)) }}
      {# djlint:on #}
      <aside>
        <a href="{{ url('dynamic_site_localized:localization') }}"
           class="button neutral">Localization</a>
        {% if request|default(none) and request.user.is_authenticated %}
          <a href="{{ url(settings.LOGIN_REDIRECT_URL) }}" class="button">Account</a>
        {% else %}
          <a href="{{ url(settings.LOGIN_URL) }}" class="button">Log in</a>
        {% endif %}
      </aside>
    </nav>
  </header>
  <main>
    {% if messages|default(none) %}
      <dialog id="messages" popover>
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
        <button id="id_messages_dismiss"
                popovertarget="messages" popovertargetaction="hide">Dismiss</button>
        <script nonce="{{ csp_nonce }}">document.getElementById('messages').showPopover();</script>
      </dialog>
    {% endif %}
    {% block main %}{% endblock %}
  </main>
{% endblock %}
