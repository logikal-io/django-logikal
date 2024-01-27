{% extends 'django_logikal/base.html.j' %}

{% block language %}en-us{% endblock %}
{% block title %}HTML Validation Error{% endblock %}
{% block description %}HTML Validation Error{% endblock %}
{% block head %}
  <link rel="stylesheet" href="{{ static('django_logikal/fonts.css') }}">
  <link rel="stylesheet" href="{{ static('django_logikal/validation_error.css') }}">
  <style nonce="{{ request.csp_nonce }}">
    {{ code_styles }}
  </style>
{% endblock %}

{% block body %}
  <h1>HTML Validation Error at {{ request.path }}</h1>
  <ol>
    {% for error in errors %}
      <li>
        <b>{{ error.severity.title() }}:</b> {{ error.message }}<br>
        {% if error.first_line %}
          <em>Line {{ error.first_line }}{%
            if error.last_line != error.first_line
          %} to {{ error.last_line }}{% endif %}:</em><br>
        <pre>{{ error.extract }}</pre>
      {% endif %}
      </li>
    {% endfor %}
  </ol>
  <h2>Page Source:</h2>
  {{ source }}
{% endblock %}
