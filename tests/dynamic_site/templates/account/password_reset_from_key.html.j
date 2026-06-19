{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth', 'layout', 'text') }}{% endblock %}

{% block subtitle %}Reset password{% endblock %}
{% block main %}
  <div class="spotlight">
    {% if token_fail|default(false) %}
      <section class="text">
        <h1>Password Reset</h1>
        <p>
          The password reset link was invalid, possibly because it has already been used.
          Please request a <a href="{{ url('account_reset_password') }}">new password reset
          link</a>.
        </p>
      </section>
    {% else %}
      <section>
        {{ form }}
      </section>
    {% endif %}
  </div>
{% endblock %}
