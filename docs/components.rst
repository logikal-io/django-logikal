.. role:: css(code)
    :language: css

Components
==========
We provide a standard set of styled components via macros. A macro module can be imported as
follows:

.. code-block:: jinja

    {% import 'django_logikal/components/auth.html.j' as auth %}

You must also import the relevant style sheets:

.. code-block:: html

    <link rel="stylesheet" href="{{ static('django_logikal/css/components/common.css') }}">
    <link rel="stylesheet" href="{{ static('django_logikal/css/components/auth.css') }}">

Style System
------------
You may configure the general component style system using the following CSS variables (either
globally on ``:root`` or on the specific object's level):

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/components/common.css :root


Authentication
--------------
.. jinja:automodule:: django_logikal/templates/django_logikal/components/auth.html.j
