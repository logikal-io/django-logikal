{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Partials{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text center">
      <h1>Partial Loading</h1>
      {% block container %}
        <p id="container">{{ content }}</p>
      {% endblock %}
      <button data-hx-post="{{ url('dynamic_site:partials') }}"
              data-hx-target="#container" data-hx-swap="outerHTML">Load New Content</button>
    </section>
  </div>
{% endblock %}
