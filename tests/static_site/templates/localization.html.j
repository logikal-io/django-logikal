{% extends 'base.html.j' %}

{% block subtitle %}{% trans %}Localized Page{% endtrans %}{% endblock %}
{% block body %}
  <h1>{% trans %}Localized{% endtrans %}</h1>
  <p>{{ _('This sentence is localized.') }}</p>
{% endblock %}
