{% import 'django_logikal/components/commons.html.j' as commons %}

{% macro login_form(csrf_input, action_url, header, provider_login_urls=none) %}
  {#
  Render a login form.

  Args:
    csrf_input (str): The CSRF input element to use.
    action_url (str): The view name to use for processing the form submission.
    header (str): The text to use for the header.
    login_urls (dict): The mapping of provider names to login URLs to use.

  .. jinja:example::

    {{ auth.login_form_email(
      header=_('Continue to access all content'),
      provider_login_urls={
        'Google': 'auth/google/',
        'Apple': 'auth/apple/',
        'Microsoft': 'auth/microsoft/',
      },
    ) }}

  #}
  <div class="login-form">
    <form action="{{ action_url }}" method="post">
      <h1>{{ header }}</h1>
      {{ csrf_input }}
      {{ commons.input_field(
        name='email', label=_('Email address'), type='email', required=true,
        placeholder=_('email@example.com'), error_text=_('This email is not valid.'),
        max_length=254, autocomplete='username', spellcheck=false,
      ) }}
      <button>{{ _('Next') }}</button>
    </form>
    {% if provider_login_urls %}
      <p>{{ _('or') }}</p>
      <div class="actions">
        {% for provider, login_url in provider_login_urls.items() %}
          <form action="{{ login_url }}" method="post">
            {{ csrf_input }}
            {{ commons.icon_button(
              text=_('Continue with %(provider)s', provider=provider),
              icon='django_logikal/icons/sign_in_with_' + provider|lower + '.svg',
              classes='neutral ' + provider|lower + '-login',
            ) }}
          </form>
        {% endfor %}
      </div>
    {% endif %}
  </div>
{% endmacro %}

{% macro action_form(
  csrf_input, action, action_url, back_url, header, email=none, min_length=10, max_length=4096
) %}
  {#
  Render an action form.

  Args:
    csrf_input (str): The CSRF input element to use.
    action (str): One of 'login', 'set_password', 'change_password'.
    action_url (str): The view name to use for processing the form submission.
    back_url (str): The view name to use for going back to the previous page.
    header (str): The text to use for the header.
    email (str): The email address to use.
    min_length (int): The minimum password length to use.
    max_length (int): THe maximum password length to use.

  .. jinja:example::

    {{ auth.action_form(header=_('Continue to access all content')) }}

  #}
  <div class="login-form">
    <form action="{{ action_url }}" method="post">
      <h1>{{ header }}</h1>

      {{ csrf_input }}

      {{ commons.input_field(
        name='login' if action != 'signup' else 'email', value=email, label=_('Email address'),
        type='email', required=true,
        placeholder=_('email@example.com'), error_text=_('This email is not valid.'),
        max_length=254, autocomplete='username', spellcheck=false, read_only=(action != 'login'),
      ) }}

      {% if action == 'change_password' %}
        {{ commons.input_field(
          name='oldpassword', label=_('Current password'), type='password', required=true,
          error_text=_('This password is not valid.'),
          min_length=min_length, max_length=max_length, autocomplete='current-password',
          spellcheck=false,
        ) }}
      {% elif action != 'signup' %}
        {{ commons.input_field(
          name='password', label=_('Password'), type='password', required=true,
          error_text=_('This password is not valid.'),
          min_length=min_length, max_length=max_length, autocomplete='current-password',
          spellcheck=false,
        ) }}
      {% endif %}

      {% if action != 'login' %}
        {{ commons.input_field(
          name='password1', label=_('New password') if action != 'signup' else _('Password'),
          type='password', required=true,
          error_text=_('This password is not valid.'),
          min_length=min_length, max_length=max_length, autocomplete='new-password',
          spellcheck=false,
        ) }}
      {% endif %}

      <div class="actions">
        {% if action in ('login', 'signup') %}
          <button>{{ _('Next') }}</button>
        {% else %}
          <button>{{ header }}</button>
        {% endif %}
        {% if back_url %}
          <a href="{{ back_url }}" class="button neutral">{{ _('Back') }}</a>
        {% endif %}
      </div>
    </form>
  </div>
{% endmacro %}
