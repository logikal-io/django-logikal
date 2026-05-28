Views
=====
Base Classes & Utilities
------------------------
Public Views
~~~~~~~~~~~~
.. autoclass:: django_logikal.views.generic.PublicViewMixin

.. autoclass:: django_logikal.views.generic.PublicView
    :show-inheritance:
    :no-inherited-members:

.. autofunction:: django_logikal.views.generic.public

Form Views
~~~~~~~~~~
.. autoclass:: django_logikal.views.generic.FormView
    :show-inheritance:
    :no-inherited-members:

HTMX Views
~~~~~~~~~~
.. note:: The ``htmx`` extra needs to be installed for these views to function correctly.

.. autoclass:: django_logikal.views.generic.HTMXTemplateView
    :show-inheritance:
    :no-inherited-members:

.. autoclass:: django_logikal.views.generic.HTMXFormView
    :show-inheritance:
    :no-inherited-members:

Utilities
~~~~~~~~~
.. automodule:: django_logikal.views.generic
    :exclude-members: PublicView, PublicViewMixin, public, FormView, HTMXTemplateView, HTMXFormView

Authentication
--------------
.. note:: The ``auth`` extra needs to be installed for these views to function correctly.

.. note:: You need to define the following templates in your project:

    * ``account/account.html.j``
    * ``account/auth.html.j``
    * ``account/email_confirm.html.j``
    * ``account/login.html.j``
    * ``account/password_change.html.j``
    * ``account/password_reset_done.html.j``
    * ``account/password_reset_from_key.html.j``
    * ``account/password_reset.html.j``
    * ``account/password_set.html.j``
    * ``account/signup.html.j``
    * ``account/verification_sent.html.j``

    Note that you can use the pre-fabricated :ref:`auth components
    <components/auth:Authentication>` in your templates, which reduce the necessary boilerplate in
    these templates to the minimum.

Account
~~~~~~~
.. automodule:: django_logikal.views.account
    :show-inheritance:
    :no-inherited-members:

Allauth
~~~~~~~
.. automodule:: django_logikal.views.allauth
    :show-inheritance:
    :no-inherited-members:
