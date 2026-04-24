{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth') }}{% endblock %}

{% block subtitle %}Continue{% endblock %}
{% block main %}
  <div class="spotlight">
    <section>
      {{ auth.login_form(
        csrf_input=csrf_input,
        action_url=url('account_auth', request=request),
        header=_('Continue to access all content'),
        provider_login_urls=provider_login_urls,
      ) }}
    </section>
  </div>
{% endblock %}
