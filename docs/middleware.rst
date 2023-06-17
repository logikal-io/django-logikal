Middleware
==========
Paranoid Mode
-------------
Views in Django are considered public until they are marked otherwise (for example, with the
:func:`~django.contrib.auth.decorators.login_required` decorator or the
:class:`~django.contrib.auth.mixins.LoginRequiredMixin`). This is somewhat unfortunate as it makes
it easier to accidentally expose pages that were intended to be used only by logged in users,
therefore we provide a middleware that makes all pages require login except when they are
explicitly marked as public.

.. autoclass:: django_logikal.security.LoginRequiredByDefaultMiddleware()
