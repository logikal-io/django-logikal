{% extends 'django_logikal/base.html.j' %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}
  This is a dynamic site
  used for demonstration and testing purposes.
{% endblock %}
{% block head %}
  <link rel="icon" href="{{ static('favicon.png') }}">
  <link rel="stylesheet" href="{{ static('django_logikal/css/components/common.css') }}">
{% endblock %}
