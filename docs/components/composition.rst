Composition
===========
The components in this category arrange content into common reusable layouts. They control spacing,
alignment and grouping without requiring their children to define their own external layout
characteristics.

You can import all composition components as follows:

.. code-block:: jinja

    {% block component_head %}{{ component_head('composition') }}{% endblock %}

Spotlight
---------
The ``spotlight`` component centers its contents horizontally and vertically, while filling the
whole surface area of its parent (“putting an element in the spotlight”):

.. jinja:example::
    :scheme: light

    <div class="example-page highlight">
      <div class="spotlight">
        <div class="example-block"></div>
      </div>
    </div>

Split
-----
The ``split`` component arranges an element’s contents into vertical groups.

.. jinja:example::
    :scheme: light

    <div class="example-page highlight">
      <div class="split">
        <div class="example-section"></div>
        <div class="example-section"></div>
      </div>
    </div>

Note that using an ``aside`` as the first or last inner element arranges the groups according to
the golden ratio:

.. jinja:example::
    :scheme: light

    <div class="example-page highlight">
      <div class="split">
        <div class="example-section"></div>
        <aside class="example-section"></aside>
      </div>
    </div>

Stack
-----
The ``stack`` component arranges its direct children vertically with consistent spacing.

.. jinja:example::
    :scheme: light

    <div class="example-page highlight">
      <div class="stack">
        <div class="example-section"></div>
        <div class="example-section"></div>
        <div class="example-section"></div>
      </div>
    </div>

The ``centered`` modifier centers the contents of the stack elements horizontally.

.. jinja:example::
    :scheme: light

    <div class="example-page highlight">
      <div class="stack centered">
        <div class="example-block">Text</div>
        <div class="example-block">Text</div>
        <div class="example-block">Text</div>
      </div>
    </div>

Cards
-----
The ``cards`` component arranges an arbitrary number of inner elements as fixed width cards.

.. jinja:example::
    :scheme: light

    <div class="example-page wide highlight">
      <div class="cards">
        <div class="example-section"></div>
        <div class="example-section"></div>
        <div class="example-section"></div>
      </div>
    </div>
