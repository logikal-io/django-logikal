{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Internal Page{% endblock %}
{% block body %}
  <h1>Dynamic Internal Page</h1>
  <p>Hello {{ request.user.first_name }}.</p>
  <p><a href="{{ url('admin:logout') }}">Log out</a></p>
{% endblock %}
