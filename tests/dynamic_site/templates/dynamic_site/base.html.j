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
      {# djlint:off T001 #} {# TODO: show a list of options for the error pages #}
      {% set menu_items = [
              MenuItem(title='Home', view_name='dynamic_site:home'),
              MenuItem(title='Errors',
                       submenu=[
                           MenuItem(title='400', view_name='error:400'),
                           MenuItem(title='403', view_name='error:403'),
                           MenuItem(title='404', view_name='error:404'),
                           MenuItem(title='500', view_name='error:500'),
                       ]
                       ),
              MenuItem(title='Templates', view_name='dynamic_site:templates',
                       view_kwargs={'arg': 'extensions'}),
              MenuItem(title='API', view_name='api-root'),
          ]
      %}
      {{ commons.menu(menu_items, request=request|default(none)) }}
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
