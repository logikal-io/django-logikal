Text Elements
=============
.. jinja:automodule:: django_logikal/templates/django_logikal/components/text.html.j

Short-form Text
---------------
.. jinja:example::

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}
    <article class="text fixed">
      <h1>Short-form Article</h1>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>Article Subtitle</h2>
      <p>{{ text.paragraph(faker) }}</p>

      <h3>Article Sub-subtitle</h3>
      <p>{{ text.paragraph(faker) }}</p>
      <ul>
        <li>First item in an unordered list</li>
        <li>Second item</li>
      </ul>
      <p>{{ text.paragraph(faker) }}</p>
      <ol>
        <li>First item in an ordered list</li>
        <li>Second item</li>
      </ol>
      <p>{{ text.paragraph(faker) }}</p>
    </article>

Long-form Text
--------------
.. jinja:example::

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}
    <article class="text long-form fixed">
      <h1>Long-form Article</h1>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>Article Subtitle</h2>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>
      <ul>
        <li>First item in an unordered list</li>
        <li>Second item</li>
      </ul>
      <p>{{ text.paragraph(faker) }}</p>
      <ol>
        <li>First item in an ordered list</li>
        <li>Second item</li>
      </ol>
      <p>{{ text.paragraph(faker) }}</p>
    </article>
