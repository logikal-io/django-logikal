{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Index Page{% endblock %}
{% block body %}
  <h1>Dynamic Index Page</h1>
  <h2>Features</h2>
  <ul>
    <li><a href="{{ url('dynamic_site_localized:localization') }}">Localization</a></li>
    <li><a href="{{ url('dynamic_site:models') }}">Models</a></li>
    <li><a href="{{ url('dynamic_site:jinja') }}">Jinja Extensions</a></li>
    <li><a href="{{ url('dynamic_site:internal') }}">Internal Page</a></li>
    <li><a href="{{ url('dynamic_site:invalid-html') }}">Invalid HTML</a></li>
    <li><a href="{{ url('dynamic_site:redirect') }}">Redirection</a></li>
    <li><a href="{{ url('dynamic_site:email') }}">Email Sending</a></li>
  </ul>

  <h2>Utilities</h2>
  <ul>
    <li><a href="{{ url('admin:index') }}">Admin</a></li>
    <li><a href="{{ url('sitemap') }}">sitemap.xml</a></li>
    <li><a href="{{ url('robots') }}">robots.txt</a></li>
    <li>
      Error Pages:
      {%- for code in (400, 403, 404, 500) +%}
        <a href="{{ url('error:' ~ code) }}">{{ code }}</a>{% if not loop.last %},{% endif %}
      {%- endfor +%}
    </li>
  </ul>

  {% script %}
    <script>
      let test = 42;
    </script>
  {% endscript %}
{% endblock %}
