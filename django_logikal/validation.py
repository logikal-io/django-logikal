import re
from itertools import chain
from logging import getLogger
from typing import Any

import debug_toolbar
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from logikal_utils.imports import try_import
from logikal_utils.project import tool_config
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import HtmlLexer

from django_logikal.middleware import Middleware

logger = getLogger(__name__)


class ValidationMiddleware(Middleware):
    """
    Validate HTML responses for all requests.

    .. note:: Requires :ref:`pytest-logikal <pytest-logikal:index:Installation>` to be installed.
    """
    DEFAULT_SKIPPED_APPS = {'admin', debug_toolbar.APP_NAME, 'rest_framework'}

    def __init__(self, *args: Any, **kwargs: Any):
        from pytest_logikal.validator import Validator  # pylint: disable=import-outside-toplevel

        super().__init__(*args, **kwargs)
        config = tool_config('django_logikal').get('validate', {})
        self._skipped_apps = config.get('skipped_apps', self.DEFAULT_SKIPPED_APPS)
        self._skipped_routes = config.get('skipped_routes', {})
        self._api_view = getattr(try_import('rest_framework.views'), 'APIView', None)
        self._validator = Validator()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = super().__call__(request)
        resolver_match = getattr(request, 'resolver_match', None)
        app_name = getattr(resolver_match, 'app_name', None)
        view_class = getattr(getattr(resolver_match, 'func', None), 'cls', type(None))
        route = getattr(resolver_match, 'route', None)

        skipped_view_class = self._api_view and issubclass(view_class, self._api_view)
        skipped_route = (
            route
            and any(re.search(skipped_route, route) for skipped_route in self._skipped_routes)
        )
        if (  # pylint: disable=too-many-boolean-expressions
            not response.headers['Content-Type'].startswith('text/html')
            or (response.status_code != 200 and app_name != 'error')
            or app_name in self._skipped_apps
            or skipped_view_class
            or skipped_route
        ):
            return response

        logger.info(f'Validating HTML response for "{request.path}"')
        content = response.content.decode()
        if errors := self._validator.errors(content=content):
            template = 'django_logikal/validation_error.html.j'
            lines = list(chain.from_iterable(
                range(error.first_line, error.last_line + 1)
                for error in errors if error.first_line and error.last_line
            ))
            context = {
                # These are safe strings
                'code_styles': mark_safe(  # nosec
                    HtmlFormatter(style='manni').get_style_defs()  # type: ignore[no-untyped-call]
                ),
                'source': mark_safe(highlight(  # nosec
                    code=content,
                    formatter=HtmlFormatter(linenos=True, hl_lines=lines, wrapcode=True),
                    lexer=HtmlLexer(),
                )),
                'errors': errors,
            }
            response = render(request, template_name=template, context=context, status=500)
            response.reason_phrase = 'Invalid HTML'
        return response
