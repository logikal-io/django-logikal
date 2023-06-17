{% extends 'django_logikal/base.html.j' %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}Static Test Site{% endblock %}
{% block head %}
  <link rel="icon" href="{{ static('favicon.png') }}">
  <link rel="stylesheet" href="{{ static('style.css') }}">
{% endblock %}
