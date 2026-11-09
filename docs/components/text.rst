Text
====
The text components provide styling for text elements.

.. note:: Most style definitions of this component are restricted to direct descendants.

.. jinja:automodule:: django_logikal/templates/django_logikal/components/text.html.j

Short-form Text
---------------
.. jinja:example::
    :scheme: light

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}

    <article class="text">
      <h1>Short-form Text</h1>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>Text Heading</h2>
      <p>{{ text.paragraph(faker) }}</p>

      <h3>Text Subheading</h3>
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
    :scheme: light

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}

    <article class="text long-form">
      <h1>Long-form Text</h1>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>

      <h2>Text Heading</h2>
      <p>{{ text.paragraph(faker) }}</p>
      <p>{{ text.paragraph(faker) }}</p>

      <h3>Text Subheading</h3>
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

Modifiers
---------
* The ``code`` modifier class increases the maximum width of the text block (which is calibrated
  for proportional text). This is useful for article blocks that only contain monospaced code.
* The ``wide`` modifier class removes the maximum width limitation from the text block entirely,
  which can be useful for sections that contain a mixed set of elements (e.g. cards). Nonetheless,
  text blocks should still be restricted in width by targeted application of the ``text`` class.
* The ``title``, ``subtitle``, ``heading`` and ``subheading`` classes can be used to format
  headings regardless of their HTML heading level.

Block Elements
--------------

Code Block
~~~~~~~~~~
.. jinja:example::
    :scheme: light

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}

    <article class="text">
      <h1>Code Block</h1>
      <p>{{ text.paragraph(faker) }}</p>

      <pre><code>def main():
         print('Hello World')</code></pre>

      <p>{{ text.paragraph(faker) }}</p>
    </article>

Block Quote
~~~~~~~~~~~
.. jinja:example::
    :scheme: light

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}

    <article class="text">
      <h1>Block Quote</h1>
      <p>{{ text.paragraph(faker) }}</p>

      <figure>
        <blockquote>
          <p>
            “And hast thou slain the Jabberwock?<br>
            Come to my arms, my beamish boy!<br>
            O frabjous day! Callooh! Callay!”
          </p>
        </blockquote>
        <figcaption>– <cite>Lewis Carroll</cite></figcaption>
      </figure>

      <p>{{ text.paragraph(faker) }}</p>
    </article>

Table
~~~~~
.. jinja:example::
    :scheme: light

    {% import 'django_logikal/components/text.html.j' as text %}
    {% set faker = faker_factory() %}

    <article class="text">
      <h1>Table</h1>
      <p>{{ text.paragraph(faker) }}</p>

      <table>
        <thead>
          <tr>
            <th>Status</th>
            <th>Name</th>
            <th>Start Date</th>
            <th>End Date</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Started</td>
            <td>Some project</td>
            <td>2026-07-01</td>
            <td>open-ended</td>
          </tr>
          <tr>
            <td>Completed</td>
            <td>Other project</td>
            <td>2026-07-01</td>
            <td>2026-08-31</td>
          </tr>
        </tbody>
      </table>

      <p>{{ text.paragraph(faker) }}</p>
    </article>
