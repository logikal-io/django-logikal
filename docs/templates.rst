Templates
=========
The Jinja template backend is extended with features that are generally missing from Django's
built-in Jinja template backend.

.. note:: The extended Jinja backend uses ``.j`` as a file extension by default, therefore you
    should make sure to name your template files accordingly.

.. note:: The :ref:`jinja2.ext.i18n <i18n-extension>` extension is added to the list of extensions
    by default.

Bases
-----
Standard HTML
~~~~~~~~~~~~~
We provide a standard HTML base template that can be used as follows:

.. code-block:: jinja

    {% extends 'django_logikal/base.html.j' %}

    {% block title %}Page Title{% endblock %}
    {% block description %}Page description.{% endblock %}
    {% block head %}
      <link rel="icon" href="{{ static('favicon.png') }}">
      <link rel="stylesheet" href="{{ static('style.css') }}">
    {% endblock %}

    {% block body %}
      <h1>Header</h1>
    {% endblock %}

Note that the ``title``, ``description`` and ``body`` blocks are required, the ``head`` block is
optional.

Optionally, you can override the ``lang`` global HTML attribute (it defaults to the value provided
by :func:`django.utils.translation.get_language`):

.. code-block:: jinja

    {% block language %}en-GB{% endblock %}

You may also add attributes to the body element via the ``bodyattributes`` tag:

.. code-block:: jinja

    {% block bodyattributes %}class="flex-cards"{% endblock %}

Email
~~~~~
We provide a standard email base template (which extends the :ref:`standard HTML template
<templates:Standard HTML>`) that can be used as follows:

.. code-block:: jinja

    {% extends 'django_logikal/email/base.html.j' %}

    {% block subject %}Email Subject{% endblock %}
    {% block description %}Email description.{% endblock %}
    {% block head %}
      <style>
        {{ include_static('email/style.css') }}
      </style>
    {% endblock %}

    {% block body %}
      <h1>Header</h1>
    {% endblock %}

Note that the ``subject``, ``description`` and ``body`` blocks are required, the ``head`` block is
optional.

Tags
-----
.. py:data:: language
    :noindexentry:

    Override the current language inside the block.

    .. code-block:: jinja

        {% language 'en-gb' %}
          British English: {{ _('localized') }}
        {% endlanguage %}

.. py:data:: timezone
    :noindexentry:

    Override the current time zone inside the block.

    .. code-block:: jinja

        {% timezone 'Europe/London' %}
          London time: {{ timestamp }}
        {% endtimezone %}

Objects
-------
.. py:data:: messages
    :noindexentry:
    :type: django.contrib.messages.storage.base.BaseStorage

    The current message storage backend instance.

    You may simply iterate over it to get the currently available messages:

    .. code-block:: jinja

        {% for message in messages %}
          {{ message }}
        {% endfor %}

.. py:data:: settings
    :noindexentry:
    :type: django.conf.LazySettings

    The current Django settings object.

.. py:data:: filters
    :noindexentry:
    :type: typing.Dict[str, typing.Any]

    The currently available filters.

.. py:data:: tests
    :noindexentry:
    :type: typing.Dict[str, typing.Any]

    The currently available tests.

Libraries
---------
.. py:data:: re
    :noindexentry:

    Python :ref:`regular expression operations <contents-of-module-re>`.

Filters
-------
The following Python built-in objects are exposed as filters:

- Functions: :func:`dir`, :func:`getattr`, :func:`hasattr`, :func:`repr`, :func:`type`
- Types: :obj:`str`

.. automodule:: django_logikal.templates.filters

Tests
-----
.. automodule:: django_logikal.templates.tests

Functions
---------
.. automodule:: django_logikal.templates.functions

Bibliography
------------
.. autoclass:: django_logikal.bibliography.Bibliography
