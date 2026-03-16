{% macro login_form(header, button) %}
  {#
  Render a login form.

  Args:
    header (str): The text to use for the header.
    button (str): The button to use.

  CSS variables:

    --something: The color to use.
    --something-else

  .. jinja:example::

    {% set header = 'Test' %}
    {{ auth.login_form(header='Test') }}

  #}
  <form class="login_form">
    <h1>{{ header }}</h1>
  </form>
{% endmacro %}
