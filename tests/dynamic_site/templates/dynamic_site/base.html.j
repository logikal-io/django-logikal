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
        'Templates': {'view_name': 'dynamic_site:templates', 'kwargs': {'arg': 'extensions'}},
        'Partials': 'dynamic_site:partials',
        'API': 'api-root',
      }, request=request|default(none)) }}
      {# djlint:on #}
      <aside>
        <a href="{{ url('dynamic_site_localized:localization') }}"
           class="button neutral">Localization</a>
        <a href="{{ url('admin:index') }}" class="button">Admin</a>
      </aside>
    </nav>
  </header>
  <main>
    {% block main %}{% endblock %}
  </main>
{% endblock %}
