from collections.abc import Callable
from functools import wraps
from typing import Any

from django.forms.forms import BaseForm
from django.http import (
    HttpRequest, HttpResponse, HttpResponseBase, HttpResponseNotFound, HttpResponseServerError,
)
from django.shortcuts import render
from django.template.backends.utils import csrf_input
from django.views import View, defaults, generic

ViewFunction = Callable[..., HttpResponseBase]


class PublicViewMixin:
    """
    Mark a class-based view public.
    """


class PublicView(PublicViewMixin, View):
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Parent class for public views.
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


class FormView[Form: BaseForm](generic.FormView[Form]):
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Display an improved form and render a template response.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def get_form_kwargs(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        kwargs = super().get_form_kwargs()
        kwargs['render_context'] = {
            'request': self.request,
            'csrf_input': csrf_input(self.request),
        }
        return kwargs


class HTMXTemplateView(generic.TemplateView):
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Render a htmx-enabled template.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def render_block(self, name: str, context: dict[str, Any] | None = None) -> HttpResponse:
        """
        Render a given block of the template.
        """
        return render(
            request=self.request,
            template_name=f'{self.get_template_names()[0]}#{name}',
            context=context,
        )

    def get_context_data(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {'htmx': True, **super().get_context_data(*args, **kwargs)}


class HTMXFormView[Form: BaseForm](HTMXTemplateView, FormView[Form]):
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Display a htmx-enabled improved form and render a template response.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Process the form or validate the given form field.
        """
        if request.htmx:  # type: ignore[attr-defined]
            fields = list(request.POST)
            if len(fields) != 1:  # pragma: no cover, defensive line
                return HttpResponse(status=204)  # incorrect request, do nothing
            form = self.get_form()
            return HttpResponse(form[fields[0]].errors.render())
        return super().post(request, *args, **kwargs)


def redirect_to(viewname: str) -> Callable[..., HttpResponseBase]:
    """
    Redirect to the given view.
    """
    return generic.RedirectView.as_view(pattern_name=viewname, query_string=True)


@public
def page_not_found_view(*args: Any, **kwargs: Any) -> HttpResponseNotFound:
    """
    Render the ``404.html.j`` template.
    """
    kwargs.setdefault('template_name', '404.html.j')
    kwargs.setdefault('exception', None)
    return defaults.page_not_found(*args, **kwargs)


@public
def server_error_view(*args: Any, **kwargs: Any) -> HttpResponseServerError:
    """
    Render the ``500.html.j`` template.
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
