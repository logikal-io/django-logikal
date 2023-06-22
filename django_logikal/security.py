from typing import Any, Callable, Dict, List

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from django_logikal.middleware import Middleware
from django_logikal.views import PublicViewMixin


class LoginRequiredByDefaultMiddleware(Middleware):
    """
    Require login on all views by default.

    Public views must be marked explicitly via the :func:`~django_logikal.views.public` decorator
    or by inheriting from :class:`~django_logikal.views.PublicView` or
    :class:`~django_logikal.views.PublicViewMixin`.

    .. warning:: When this middleware is used, you must mark all public views explicitly, including
        views included from applications like :mod:`django.contrib.admin`. You may use the
        :ref:`URL utility functions <urls:URLs & Paths>` which provide such explicitly marked
        public views where necessary.

    .. note:: All :ref:`standard settings modules <settings:Settings>` include this middleware by
        default.
    """
    @staticmethod
    def process_view(
        request: HttpRequest,
        view_func: Callable[..., Any],
        view_args: List[Any],
        view_kwargs: Dict[str, Any],
    ) -> Any:
        if getattr(view_func, 'public_view', False):
            return None
        if issubclass(getattr(view_func, 'view_class', type(None)), PublicViewMixin):
            return None
        return login_required(view_func)(request, *view_args, **view_kwargs)
