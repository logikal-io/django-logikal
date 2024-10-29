from collections.abc import Callable
from functools import wraps
from typing import Any

from django.http import HttpResponseBase
from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.views import View, defaults, generic

ViewFunction = Callable[..., HttpResponseBase]


class PublicViewMixin:
    """
    Mark a class-based view public.
    """


class PublicView(PublicViewMixin, View):
    # Note: we re-define init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Represent a public view.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover


def public(view: ViewFunction) -> ViewFunction:
    """
    Mark a view function public.
    """
    @wraps(view)
    def view_wrapper(*args: Any, **kwargs: Any) -> HttpResponseBase:
        return view(*args, **kwargs)
    view_wrapper.public_view = True  # type: ignore[attr-defined]
    return view_wrapper


def redirect_to(viewname: str) -> Callable[..., HttpResponseBase]:
    """
    Redirect to the given view.
    """
    return generic.RedirectView.as_view(pattern_name=viewname, query_string=True)


@public
def page_not_found_view(*args: Any, **kwargs: Any) -> HttpResponseNotFound:
    """
    Public view rendered from the ``404.html.j`` template.
    """
    kwargs.setdefault('template_name', '404.html.j')
    kwargs.setdefault('exception', None)
    return defaults.page_not_found(*args, **kwargs)


@public
def server_error_view(*args: Any, **kwargs: Any) -> HttpResponseServerError:
    """
    Public view rendered from the ``500.html.j`` template.
    """
    kwargs.setdefault('template_name', '500.html.j')
    return defaults.server_error(*args, **kwargs)


#: Standard error handler views.
ERROR_HANDLERS = {
    400: server_error_view,
    403: page_not_found_view,
    404: page_not_found_view,
    500: server_error_view,
}
