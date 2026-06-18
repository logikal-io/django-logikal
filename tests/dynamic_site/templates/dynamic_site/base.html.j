{% extends 'django_logikal/base.html.j' %}
{% import 'django_logikal/components/commons.html.j' as commons %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}
  This is a dynamic site
  used for demonstration and testing purposes.
{% endblock %}

{% block component_head %}{{ component_head('layout', 'text') }}{% endblock %}
{% block head %}
  <link rel="icon" href="{{ static('favicon.png') }}">
{% endblock %}

{% block body %}
  <header>
    <nav>
      <a href="{{ url('dynamic_site:home') }}" class="logo" aria-label="Go to home page">
        {{ include_static('logikal_logo.svg') }}
      </a>
      {{ commons.menu([
        menu_item(title='Home', view_name='dynamic_site:home'),
        menu_item(
          title='Errors',
          submenu=[
            menu_item(title='No Error', view_name='dynamic_site:home'),
            menu_item(
              title='Server Errors',
              submenu=[
                menu_item(title='400', view_name='error:400'),
                menu_item(title='500', view_name='error:500'),
              ],
            ),
            menu_item(
              title='Page Not Found Errors',
              submenu=[
                menu_item(title='403', view_name='error:403'),
                menu_item(title='404', view_name='error:404'),
              ],
            ),
          ],
        ),
        menu_item(
          title='Templates',
          submenu=[
            menu_item(
              title='Features',
              view_name='dynamic_site:templates', view_kwargs={'arg': 'extensions'},
            ),
            menu_item(title='Partials', view_name='dynamic_site:partials'),
          ],
        ),
        menu_item(title='Admin', view_name='admin:index'),
        menu_item(title='API', view_name='api-root'),
      ], request=request|default(none)) }}
      <aside>
        {% if request|default(none) and
              request.resolver_match.view_name == 'dynamic_site_localized:localization' %}
          {{ commons.language_switcher(
            current_language_code=language(),
            languages=settings.LANGUAGES,
            action_url=url('set_language'),
            csrf_input=csrf_input,
          ) }}
        {% endif %}
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
