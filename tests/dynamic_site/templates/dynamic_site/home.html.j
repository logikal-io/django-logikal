{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Home Page{% endblock %}
{% block main %}
  <article class="text wide">
    <h1>Dynamic Site</h1>

    <div class="cards">
      <section class="stack">
        <h2>Features</h2>
        <h3>Rendering</h3>
        {% set view_args = {'url_path_arg': 'path'} %}
        <ul>
          <li><a href="{{ url('dynamic_site:templates', kwargs=view_args) }}">Templates</a></li>
          <li><a href="{{ url('dynamic_site:models') }}">Models</a></li>
          <li><a href="{{ url('dynamic_site:partials') }}">Partials</a></li>
          <li><a href="{{ url('dynamic_site_localized:localization') }}">Localization</a></li>
        </ul>
        <ul>
          <li><a href="{{ url('dynamic_site:internal') }}">Internal Page</a></li>
          <li><a href="{{ url('dynamic_site:invalid_html') }}">HTML Validation Error</a></li>
        </ul>
      </section>

      <section class="stack">
        <h2>Error Pages</h2>
        <h3>Server Errors</h3>
        <ul>
          <li><a href="{{ url('error:400') }}">400</a></li>
          <li><a href="{{ url('error:500') }}">500</a></li>
        </ul>

        <h3>Page Not Found Errors</h3>
        <ul>
          <li><a href="{{ url('error:403') }}">403</a></li>
          <li><a href="{{ url('error:404') }}">404</a></li>
        </ul>
      </section>

      <section class="stack">
        <h2>Utilities</h2>
        <h3>General</h3>
        <ul>
          <li><a href="{{ url('admin:index') }}">Admin</a></li>
          <li><a href="{{ url('api-root') }}">API</a></li>
          <li><a href="{{ url('dynamic_site:email') }}">Email Sending</a></li>
          <li><a href="{{ url('dynamic_site:redirect') }}">Redirection</a></li>
        </ul>

        <h3>Auxiliary Pages</h3>
        <ul>
          <li><a href="{{ url('sitemap') }}">sitemap.xml</a></li>
          <li><a href="{{ url('robots') }}">robots.txt</a></li>
        </ul>
      </section>
    </div>
  </article>

  <script nonce="{{ csp_nonce }}">let test = 42;</script>
{% endblock %}
