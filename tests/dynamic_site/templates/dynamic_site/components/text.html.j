{% extends 'dynamic_site/base.html.j' %}
{% import 'django_logikal/components/text.html.j' as text %}

{% block component_head %}{{ component_head('text') }}{% endblock %}
{% set faker = faker_factory() %}

{% block subtitle %}Text{% endblock %}
{% block main %}
  <div class="spotlight">
    <article class="text">
      <!-- Single-line headings -->
      <h1>Single-Line Title</h1>
      <p>{{ text.paragraph(faker) }}</p>

      <hgroup>
        <h2 class="title">Single-Line Title</h2>
        <p>Single-Line Subtitle</p>
      </hgroup>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>Single-Line Heading</h2>
      <p>{{ text.paragraph(faker) }}</p>

      <h3>Single-Line Subheading</h3>
      <p>{{ text.paragraph(faker) }}</p>

      <!-- Multi-line headings -->
      <h2 class="title">
        Multi-Line Title<br>
        Second Line
      </h2>
      <p>{{ text.paragraph(faker) }}</p>

      <hgroup>
        <h2 class="title">
          Multi-Line Title<br>
          Second Line
        </h2>
        <p>
          Multi-Line Subtitle<br>
          Second Line
        </p>
      </hgroup>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>
        Multi-Line Heading<br>
        Second Line
      </h2>
      <p>{{ text.paragraph(faker) }}</p>

      <h3>
        Multi-Line Subheading<br>
        Second Line
      </h3>
      <p>{{ text.paragraph(faker) }}</p>
    </article>
  </div>
{% endblock %}
