{% macro paragraph(faker, sentences=5) %}
  {#
  Generate a paragraph worth of fake text.

  .. jinja:example::
      :scheme: light

      {% set faker = faker_factory() %}
      <p>{{ text.paragraph(faker) }}</p>

  #}
  {{ faker.paragraph(nb_sentences=sentences, variable_nb_sentences=false)|wordwrap }}
{% endmacro %}
