Components
==========
The ``django-logikal`` package provides a comprehensive library of styled components. You can
simply add the style sheets of the relevant component modules to the ``<head>`` element of the
given page template via the :func:`~django_logikal.templates.functions.component_styles` function:

.. code-block:: jinja

    {% block component_styles %}
      {{ component_styles('commons', 'auth') }}
    {% endblock %}

Many of the components are implemented via Jinja macros, which can be imported via their module as
follows:

.. code-block:: jinja

    {% import 'django_logikal/components/commons.html.j' as commons %}
    {% import 'django_logikal/components/auth.html.j' as auth %}
    ...

.. raw:: html

    <hr>

.. toctree::
    :caption: Introduction
    :glob:
    :maxdepth: 1

    style_system

.. raw:: html

    <hr>

.. toctree::
    :caption: Component Categories
    :glob:
    :maxdepth: 1

    components/commons
    components/*

.. raw:: html

    <hr>
