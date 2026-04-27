{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Page Not Found{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text">
      <h1>Page Not Found</h1>
      <p>
        Page &ldquo;{{ request.path }}&rdquo; does not exist, or you may not have permission to
        access it.
      </p>
    </section>
  </div>
{% endblock %}
