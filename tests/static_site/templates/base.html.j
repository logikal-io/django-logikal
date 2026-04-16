{% extends 'django_logikal/base.html.j' %}
{% import 'django_logikal/components/commons.html.j' as commons %}

{% block title %}{% block subtitle required %}{% endblock %} | Logikal{% endblock %}
{% block description %}Static Test Site{% endblock %}
{% block component_styles %}{{ component_styles('commons') }}{% endblock %}
{% block head %}<link rel="icon" href="{{ static('favicon.png') }}">{% endblock %}

{% block body %}
  <main>
    {% block main %}{% endblock %}
  </main>
{% endblock %}
