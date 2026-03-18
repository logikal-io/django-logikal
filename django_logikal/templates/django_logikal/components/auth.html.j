{% macro login_form(header, button=_('Test')) %}
  {#
  Render a login form.

  Args:
    header (str): The text to use for the header.
    button (str): The button to use.

  .. jinja:example::

    {{ auth.login_form(header=_('Test')) }}

  #}
  <form class="login-form">
    <h1>{{ header }}</h1>
  </form>
{% endmacro %}
