{% extends 'dynamic_site/base.html.j' %}
{% import 'django_logikal/components/auth.html.j' as auth %}

{% block component_head %}{{ component_head('auth') }}{% endblock %}

{% block subtitle %}Authentication{% endblock %}
{% block main %}
  <div class="spotlight">
    <section>
      {{ auth.login_form_email(
        header=_('Continue to access all content'),
        provider_login_urls={
          'Google': 'auth/google/',
          'Apple': 'auth/apple/',
          'Microsoft': 'auth/microsoft/',
        },
      ) }}
    </section>
  </div>
{% endblock %}
