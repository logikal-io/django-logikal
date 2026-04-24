{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth') }}{% endblock %}

{% block subtitle %}Sign in{% endblock %}
{% block main %}
  <div class="spotlight">
    <section>
      {{ auth.action_form(
        csrf_input=csrf_input,
        action='login',
        action_url=url('account_login', request=request),
        back_url=url('account_auth'),
        header=_('Sign in to access all content'),
        email=request.session.get('email'),
      ) }}
    </section>
  </div>
{% endblock %}
