{% import 'django_logikal/components/commons.html.j' as commons %}

{% macro auth_form(csrf_input, form, header, provider_login_urls=none) %}
  {#
  Render an authentication form.

  Args:
    csrf_input (str): The CSRF input element to use.
    form (~django_logikal.forms.account.AuthForm): The authentication form to use.
    header (str): The text to use for the header.
    provider_login_urls (dict[str, str]): The mapping of provider names to login URLs to use.

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
            {% set sign_in_icon = 'django_logikal/icons/sign-in-with-' + provider|lower + '.svg' %}
            <button type="submit"
                    id="social-login-{{ provider|lower }}"
                    class="neutral icon icon-leading text {{ provider|lower }}-login">
              {{- include_static(sign_in_icon) -}}
              <span>{{ _('Continue with %(provider)s', provider=provider) }}</span>
            </button>
          </form>
        {% endfor %}
      </div>
    {% endif %}
  </div>
{% endmacro %}
