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
{% endblock %}

{% block body %}
  <header>
    <nav>
      <a href="{{ url('dynamic_site:home') }}" class="logo" aria-label="Go to home page">
        {{ include_static('logikal_logo.svg') }}
      </a>
      {# djlint:off T001 #}
      {{ commons.menu({
        'Home': 'dynamic_site:home',
        'Errors': 'error:404',
        'Templates': {'view_name': 'dynamic_site:templates', 'kwargs': {'arg': 'extensions'}},
        'Partials': 'dynamic_site:partials',
        'Admin': 'admin:index',
        'API': 'api-root',
      }, request=request|default(none)) }}
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
        <button popovertarget="messages" popovertargetaction="hide">Dismiss</button>
        <script nonce="{{ csp_nonce }}">document.getElementById('messages').showPopover();</script>
      </dialog>
    {% endif %}
    {% block main %}{% endblock %}
  </main>
{% endblock %}
