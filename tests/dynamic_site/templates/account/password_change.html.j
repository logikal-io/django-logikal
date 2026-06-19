{% extends 'dynamic_site/base.html.j' %}

{% import 'django_logikal/components/auth.html.j' as auth %}
{% block component_head %}{{ component_head('auth', 'layout') }}{% endblock %}

{% block subtitle %}Change Password{% endblock %}
{% block main %}
  <div class="spotlight">
    <section>
      {{ form }}
    </section>
  </div>
{% endblock %}
