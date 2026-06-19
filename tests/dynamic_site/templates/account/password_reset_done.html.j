{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth', 'layout', 'text') }}{% endblock %}

{% block subtitle %}Password Reset{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text">
      <h1>Password Reset</h1>
      <p>
        We sent an email to <b>{{ request.session['email'] }}</b>.
        Follow the link in the email to complete the password reset process.
      </p>
    </section>
  </div>
{% endblock %}
