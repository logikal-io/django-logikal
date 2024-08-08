Settings
========
The ``django-logikal`` library provides a set of opinionated standard settings modules for local
development, testing and production use.

You can simply import the appropriate settings module in your own settings files to benefit from
a highly improved Django experience:

.. code-block:: python

    from django_logikal.settings import Settings
    from django_logikal.settings.dynamic_site.dev import DevSettings

    Settings(globals()).update(DevSettings)

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

Settings Updates
----------------
Standard settings modules are provided as settings updates, which need to be applied to a
:class:`~django_logikal.settings.Settings` instance:

.. autoclass:: django_logikal.settings.Settings

You can specify your own settings updates by inheriting from the
:class:`~django_logikal.settings.SettingsUpdate` class:

.. autoclass:: django_logikal.settings.SettingsUpdate

.. tip:: Static configuration options can be simply specified as class attributes, but it is also
    possible to dynamically modify the settings by overriding the
    :meth:`~django_logikal.settings.SettingsUpdate.apply` class method as follows:

    .. code-block:: python

        from django_logikal.settings import Settings, SettingsUpdate

        class AppSettings(SettingsUpdate):
            ROOT_URLCONF = 'app.website.urls'

            @staticmethod
            def apply(settings: Settings) -> None:
                settings['INSTALLED_APPS'] += ['app.website']

.. tip:: Note that settings updates can be chained, which makes combining the standard settings
    updates with your own custom settings updates simple and straightforward:

    .. code-block:: python

        from django_logikal.settings import Settings
        from django_logikal.settings.dynamic_site.dev import DevSettings
        from app.settings.app import AppSettings

        Settings(globals()).update(DevSettings).update(AppSettings)

Dynamic Site Settings
---------------------
Provides :ref:`email sending <emails:Emails>` support (via :doc:`Anymail <django-anymail:index>`
and `Amazon Simple Email Service <https://aws.amazon.com/ses/>`_), the :ref:`paranoid middleware
<middleware:Paranoid Mode>` and a sensible content security policy (via :doc:`django-csp
<django-csp:index>`).

.. note:: Requires the :ref:`dynamic extra <index:Dynamic Sites>`.

.. note:: When using the optional :ref:`rest extra <index:REST API>`, the REST API endpoints are
    configured to be only accessible for session-authenticated users by default.

.. automodule:: django_logikal.settings.dynamic_site.dev
    :exclude-members: apply
.. automodule:: django_logikal.settings.dynamic_site.testing
    :exclude-members: apply
.. automodule:: django_logikal.settings.dynamic_site.production
    :exclude-members: apply

Static Site Settings
--------------------
Provides static site generation support (via `django-distill <https://django-distill.com/>`_).

.. note:: Requires the :ref:`static extra <index:Static Sites>`.

.. automodule:: django_logikal.settings.static_site.dev
    :exclude-members: apply
.. automodule:: django_logikal.settings.static_site.testing
    :exclude-members: apply
