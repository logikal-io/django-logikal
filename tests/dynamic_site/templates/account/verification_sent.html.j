{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth') }}{% endblock %}

{% block subtitle %}Email Verification{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text">
      <h1>Email Verification</h1>
      <p>
        We sent a sign-up link to <b>{{ request.session['email'] }}</b>.
        Follow the link in the email to complete the sign-up process.
      </p>
    </section>
  </div>
{% endblock %}
