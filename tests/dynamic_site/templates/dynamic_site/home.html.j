{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Home Page{% endblock %}
{% block main %}
  <article>
    <h1>Dynamic Site Home Page</h1>

    <div class="cards">
      <section class="text">
        <h2>Features</h2>
        <ul>
          <li><a href="{{ url('dynamic_site:models') }}">Models</a></li>
          <li><a href="{{ url('dynamic_site:invalid-html') }}">Invalid HTML</a></li>
          <li><a href="{{ url('dynamic_site:redirect') }}">Redirection</a></li>
          <li><a href="{{ url('dynamic_site:email') }}">Email Sending</a></li>
        </ul>
      </section>

      <section class="text">
        <h2>Error Pages</h2>
        <ul>
          {% for code in (400, 403, 404, 500) %}
            <li>
              <a href="{{ url('error:' ~ code) }}">{{ code }}</a>
            </li>
          {% endfor %}
        </ul>
      </section>

      <section class="text">
        <h2>Utilities</h2>
        <ul>
          <li><a href="{{ url('sitemap') }}">sitemap.xml</a></li>
          <li><a href="{{ url('robots') }}">robots.txt</a></li>
        </ul>
      </section>
    </div>
  </article>

  <script nonce="{{ csp_nonce }}">
    let test = 42;
  </script>
{% endblock %}
