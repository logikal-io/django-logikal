{% import 'django_logikal/components/commons.html.j' as commons %}

{% macro auth_form(csrf_input, form, header, provider_login_urls=none) %}
  {#
  Render an authentication form.

  Args:
    csrf_input (str): The CSRF input element to use.
    form (:py:class:`django_logikal.forms.account.AuthForm`): The authentication form to use.
    header (str): The text to use for the header.
    provider_login_urls (dict): The mapping of provider names to login URLs to use.

  .. jinja:example::

    {{ auth.auth_form(
      csrf_input=csrf_input,
      form=auth_form,
      header=_('Continue to access all content'),
      provider_login_urls={
        'Google': 'auth/google/',
        'Apple': 'auth/apple/',
        'Microsoft': 'auth/microsoft/',
      },
    ) }}

  #}
  <div class="form-group">
    {{ form.with_meta(header=header) }}
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
