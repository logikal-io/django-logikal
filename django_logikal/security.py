from collections.abc import Callable
from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from logikal_utils.imports import try_import

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
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._api_view = getattr(try_import('rest_framework.views'), 'APIView', None)

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., Any],
        view_args: list[Any],
        view_kwargs: dict[str, Any],
    ) -> Any:
        # The Django REST framework has its own separate authentication configuration
        # (see https://www.django-rest-framework.org/api-guide/authentication/)
        if self._api_view and issubclass(getattr(view_func, 'cls', type(None)), self._api_view):
            return None
        if getattr(view_func, 'public_view', False):
            return None
        if issubclass(getattr(view_func, 'view_class', type(None)), PublicViewMixin):
            return None
        return login_required(view_func)(request, *view_args, **view_kwargs)
