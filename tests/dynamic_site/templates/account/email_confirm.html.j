{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth', 'layout', 'text') }}{% endblock %}

{% block subtitle %}Email Verification{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text">
      <h1>Email Verification</h1>
      <p>
        This email confirmation link expired or is invalid. You can log in and request a
        <a href="{{ url('account_login') }}">new email verification link</a>.
      </p>
    </section>
  </div>
{% endblock %}
