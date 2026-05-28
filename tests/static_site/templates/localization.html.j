{% extends 'base.html.j' %}

{% block subtitle %}{% trans %}Localized Page{% endtrans %}{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text">
      <h1>{% trans %}Localized{% endtrans %}</h1>
      <p>{{ _('This sentence is localized.') }}</p>
    </section>
  </div>
{% endblock %}
