from itertools import chain
from logging import getLogger
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
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
    def __init__(self, *args: Any, **kwargs: Any):
        from pytest_logikal.validator import Validator  # pylint: disable=import-outside-toplevel

        super().__init__(*args, **kwargs)
        self._validator = Validator()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = super().__call__(request)
        resolver_match = getattr(request, 'resolver_match', None)
        app_name = getattr(resolver_match, 'app_name', None)
        if (
            not response.headers['Content-Type'].startswith('text/html')
            or (response.status_code != 200 and app_name != 'error')
            or app_name in {'admin', 'djdt'}  # admin and Django debug toolbar responses
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
                'code_styles': mark_safe(HtmlFormatter(style='manni').get_style_defs()),  # nosec
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
