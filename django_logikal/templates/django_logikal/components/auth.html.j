{% import 'django_logikal/components/commons.html.j' as commons %}

{% macro login_form_username(header, provider_login_urls=none) %}
  {#
  Render a username login form.

  Args:
    header (str): The text to use for the header.
    login_urls (dict): The mapping of provider names to login URLs to use.

  .. jinja:example::

    {{ auth.login_form_username(
      header=_('Continue to access all content'),
      provider_login_urls={
        'Google': 'auth/google/',
        'Apple': 'auth/apple/',
        'Microsoft': 'auth/microsoft/',
      },
    ) }}

  #}
  <form class="login-form-sign-up">
    <h1>{{ header }}</h1>
    {{ commons.input_field(
      name='email', label=_('Email address'), type='email', required=true,
      placeholder=_('email@example.com'), error_text=_('This email is invalid.'),
    ) }}
    <button>Next</button>
    {% if provider_login_urls %}
      <p>or</p>
      <div class="external-login">
        {% for provider, login_url in provider_login_urls.items() %}
          {{ commons.link_icon_button(
            text=_('Sign in with %(provider)s', provider=provider), href=login_url,
            icon='django_logikal/icons/sign_in_with_' + provider|lower + '.svg',
            classes='neutral ' + provider|lower + '-login',
          ) }}
        {% endfor %}
      </div>
    {% endif %}
  </form>
{% endmacro %}
