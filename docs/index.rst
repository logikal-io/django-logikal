.. Documentation structure
.. toctree::
    :caption: Documentation
    :hidden:

    self
    settings
    environment
    templates
    components
    middleware
    views
    urls
    emails
    migrations
    commands
    development
    license

.. toctree::
    :caption: External Links
    :hidden:

    Release Notes <https://github.com/logikal-io/django-logikal/releases>
    Issue Tracker <https://github.com/logikal-io/django-logikal/issues>
    Source Code <https://github.com/logikal-io/django-logikal>

Getting Started
===============
The ``django-logikal`` library provides a highly enhanced Django development experience via various
mighty utilities:

- Standard :ref:`settings modules <settings:Settings>`
- A greatly extended :ref:`Jinja template backend <templates:Templates>` and a standard
  :ref:`template component library <components:Components>`
- :ref:`Paranoid mode <middleware:Paranoid Mode>` to ensure private pages don't become public
  accidentally
- :ref:`HTML validation <middleware:HTML Validation>` during development and testing
- :ref:`Views <views:Views>`, :ref:`URLs and paths <urls:URLs & Paths>` for common utilities
- Simple :ref:`email sending <emails:Emails>`
- An improved :ref:`migration writer <migrations:Migrations>` for nicely formatted migration files
- :ref:`General commands <commands:General Commands>` for invoking management commands and starting
  a development server
- :ref:`Management commands <commands:Management Commands>` for working with synthetic data for
  local development and testing, translation file management and static site generation

Our goal is to make Django development simpler and more powerful at the same time.

Installation
------------
You can simply install ``django-logikal`` from `pypi <https://pypi.org/project/django-logikal/>`_:

.. code-block:: shell

    pip install django-logikal

Dynamic Sites
~~~~~~~~~~~~~
You may install the library with support for dynamic sites via the ``dynamic`` extra:

.. code-block:: shell

    pip install django-logikal[dynamic]

htmx
~~~~
If you are using `htmx <https://htmx.org/>`_ you should also install the ``htmx`` extra:

.. code-block:: shell

    pip install django-logikal[dynamic,htmx]

This will install and configure `django-htmx <https://django-htmx.readthedocs.io/en/latest/>`_.

REST API
~~~~~~~~
You can install the library with support for `Django REST framework
<https://www.django-rest-framework.org/>`_ APIs:

.. code-block:: shell

    pip install django-logikal[dynamic,rest]

Static Sites
~~~~~~~~~~~~
If you intend to generate static pages you should install the library with the ``static`` extra:

.. code-block:: shell

    pip install django-logikal[static]

Bibliography
~~~~~~~~~~~~
Additionally, you may also use the ``bibliography`` extra to install ``django-logikal`` with
support for :func:`bibliographies <django_logikal.templates.functions.bibliography>`:

.. code-block:: shell

    pip install django-logikal[bibliography]

Services
~~~~~~~~
The `PostgreSQL <https://hub.docker.com/_/postgres>`_ and `v.Nu
<https://validator.github.io/validator/>`_ `Docker Compose <https://docs.docker.com/compose/>`_
services must be available for local development and testing.  We recommend adding the following
services to your project's ``compose.yml`` file:

.. code-block:: yaml

    services:
      validator:
        image: ghcr.io/validator/validator@sha256:9449eb55d574144ea7a794a5d7e90c01f7d3f7196873171c2034df296478949a
        ports: [{target: 8888}]

      postgres:
        image: postgres:18.1
        environment:
          POSTGRES_DB: dev
          POSTGRES_USER: dev
          POSTGRES_PASSWORD: dev
        ports: [{target: 5432}]
        volumes:
          - type: volume
            source: postgres_data
            target: /var/lib/postgresql
        healthcheck:
          test: pg_isready --username local --host 127.0.0.1
          interval: 3s
          timeout: 3s
          retries: 5

    volumes:
      postgres_data:

Settings
~~~~~~~~
Once installed, you can simply import the appropriate :ref:`standard settings module
<Settings:Settings>` in your project:

.. code-block:: python

    from django_logikal.settings import Settings
    from django_logikal.settings.dynamic_site.dev import DevSettings

    Settings(globals()).update(DevSettings)

That's it! The included settings modules automatically activate all relevant features, so once your
project-specific settings and URL patterns are defined, you can start developing right away:

.. code-block:: console

    $ run
    ...
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
