{% extends 'django_logikal/base.html.j' %}

{% block language %}en-us{% endblock %}
{% block title %}HTML Validation Error{% endblock %}
{% block description %}HTML Validation Error{% endblock %}

{% block component_styles %}{{ component_styles('fonts', 'commons') }}{% endblock %}

{% block head %}
  <style nonce="{{ csp_nonce }}">
    @media (prefers-color-scheme: light) {
      {{ code_styles['light'] }}
    }
    @media (prefers-color-scheme: dark) {
      {{ code_styles['dark'] }}
    }
  </style>
{% endblock %}

{% block body %}
  <header>
    <hgroup>
      <h1>HTML Validation Error</h1>
      <p>at {{ request.path }}</p>
    </hgroup>
  </header>

  <main class="validation-errors">
    <div class="split">
      <aside>
        <section class="text box">
          <h2>Validation Errors</h2>
          <ol>
            {% for error in errors %}
              <li>
                <b class="error">{{ error.severity.title() }}:</b> {{ error.message }}<br>
                {% if error.first_line %}
                  <b>Line {{ error.first_line }}
                    {%- if error.last_line != error.first_line %} to {{ error.last_line }}
                    {%- endif %}:</b>
                  <pre><code>{{ error.extract }}</code></pre>
                {% endif %}
              </li>
            {% endfor %}
          </ol>
        </section>
      </aside>

      <section class="text box">
        <h2>Page Source</h2>
        <div class="code">
          {{ source }}
        </div>
      </section>
    </div>
  </main>
{% endblock %}
