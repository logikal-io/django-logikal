Settings
========
The ``django-logikal`` library provides a set of opinionated standard settings modules for local
development, testing and production use.

You can simply import the appropriate settings module in your own settings files to benefit from
a highly improved Django experience:

.. code-block:: python

    from django_logikal.settings.dynamic_site import *

Common Features
---------------
All settings modules include the following:

- An appropriate logging, storage, localization and static file serving configuration
- `PostgreSQL <https://www.postgresql.org/>`_ as the default database engine (including for local
  development and testing)
- An :ref:`improved Jinja template backend <templates:Templates>`
- :ref:`HTML validation <middleware:HTML Validation>` support (via `v.Nu
  <https://validator.github.io/validator/>`_)
- Authentication support (via :mod:`django.contrib.auth`)
- Sitemap support (via :mod:`django.contrib.sitemaps`)
- Robots exclusion support (via :doc:`django-robots <django-robots:index>`)
- The improved :ref:`migration writer <migrations:Migrations>`
- The `Django migration linter <https://github.com/3YOURMIND/django-migration-linter>`_
- The `Django debug toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_

Local Development
-----------------
.. py:data:: django_logikal.settings.dynamic_site
    :noindexentry:

    Standard local settings for dynamic sites.

    .. note:: Requires the :ref:`dynamic extra <index:Dynamic Sites>`.

    Includes the following:

    - :ref:`Email sending <emails:Emails>` support (via :doc:`Anymail <django-anymail:index>` and
      `Amazon Simple Email Service <https://aws.amazon.com/ses/>`_)
    - The :ref:`paranoid middleware <middleware:Paranoid Mode>`

.. py:data:: django_logikal.settings.static_site
    :noindexentry:

    Standard local settings for static sites.

    .. note:: Requires the :ref:`static extra <index:Static Sites>`.

    Includes the following:

    - Static site generation support (via `django-distill <https://django-distill.com/>`_)

Testing
-------
.. py:data:: django_logikal.settings.testing
    :noindexentry:

    Standard settings for testing dynamic or static sites.

    .. note:: You must import the appropriate local settings file before importing this module:

        .. code-block:: python

            from project.settings.local import *
            from django_logikal.settings.testing import *

Production
----------
.. py:data:: django_logikal.settings.production
    :noindexentry:

    Standard production settings for dynamic sites.

    .. note:: Secrets will be loaded from Google Secret Manager during import time. In particular,
        the secret key is loaded from ``django-secret-key``, and the database configuration is
        loaded from ``django-database-secrets`` (which must be a JSON string with keys
        ``hostname``, ``port``, ``database``, ``username`` and ``password``).
