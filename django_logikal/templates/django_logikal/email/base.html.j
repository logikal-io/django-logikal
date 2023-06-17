{% extends 'django_logikal/base.html.j' %}

{% block title %}
  {% block subject required %}{% endblock %}
{% endblock %}

{% block bodyattributes %}
  leftmargin="0"
  topmargin="0"
  marginwidth="0"
  marginheight="0"
  offset="0"
{% endblock %}
