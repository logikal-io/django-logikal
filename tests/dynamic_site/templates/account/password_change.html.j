{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth') }}{% endblock %}

{% block subtitle %}Change password{% endblock %}
{% block main %}
  <div class="spotlight">
    <section>
      {{ auth.action_form(
        csrf_input=csrf_input,
        action='change_password',
        action_url=url('account_change_password'),
        back_url=url('account'),
        header=_('Change password'),
        email=request.user.email,
      ) }}
    </section>
  </div>
{% endblock %}
