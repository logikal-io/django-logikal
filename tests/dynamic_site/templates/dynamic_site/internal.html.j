{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Internal Page{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text center">
      <h1>Internal Page</h1>
      <p>Hello {{ request.user.get_full_name() }}.</p>
    </section>
  </div>
{% endblock %}
