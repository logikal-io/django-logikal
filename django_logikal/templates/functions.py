import os
import re
from datetime import datetime, tzinfo as tzinfo_class
from pathlib import Path
from typing import Any

from babel import Locale
from babel.support import Format
from django.contrib.staticfiles import finders
from django.http.request import HttpRequest
from django.templatetags.static import static as django_static
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import get_language
from jinja2.runtime import Context
from jinja2.utils import pass_context

import django_logikal  # for type checking


@pass_context
def context(context: Context) -> Context:  # pylint: disable=redefined-outer-name
    # noqa: D400, D402, D415
    """
    context()

    Return the current template context.
    """
    return context


def static(path: str) -> str:
    """
    Return the absolute server URL path to a static asset.
    """
    return django_static(path)


def static_path(path: str) -> Path:
    """
    Return the local path to a static asset.
    """
    if not (file_path := finders.find(path)):
        raise RuntimeError(f'Static file "{path}" not found')
    return Path(file_path)


def include_static(path: str) -> SafeString:
    """
    Insert the contents of the given static file into the template.

    Useful for inlining CSS, SVG or JavaScript content.

    .. DANGER:: **Security risk: the contents of the referenced file are inserted unescaped.**

        Do not use this function to include non-trusted, user-generated or user-uploaded content,
        or content that can be in any way influenced by users.

    """
    file_path = static_path(path)
    content = file_path.read_text(encoding='utf-8').lstrip()
    if file_path.suffix == '.svg':
        content = re.sub(r'^<\?xml [^>]*\?>', '', content).lstrip()
    return mark_safe(content)  # nosec: danger is documented


def url(
    *args: Any,
    request: HttpRequest | None = None,
    request_get_update: dict[str, Any] | None = None,
    **kwargs: Any,
) -> str:
    """
    Return the absolute server URL path associated with the given view name.

    HTTP GET parameters are automatically appended when the request is provided.
    """
    path = reverse(*args, **kwargs)
    if request:
        request_get = request.GET.copy()
        request_get.update(request_get_update or {})
        if request_get:
            path = '?'.join([path, request_get.urlencode(safe='/')])
    return path


def url_name(request: HttpRequest) -> str:
    """
    Return the view name associated with the current request.
    """
    if not (url_match := request.resolver_match):
        raise RuntimeError('URL resolving has not taken place yet')
    return f'{url_match.app_name or ''}:{url_match.url_name or ''}'


def language() -> str:
    """
    Return the current language code.
    """
    return get_language()


def format(  # pylint: disable=redefined-builtin
    locale: Locale | None = None,
    language_code: str | None = None,
    tzinfo: tzinfo_class | None = None,
) -> Format:
    """
    Return a locale-aware and time zone-aware formatter.

    Defaults to deriving the locale from the current language and using the current time zone.

    .. tip:: Often times you can use a single formatter instance in a template as follows:

        .. code-block:: jinja

            {% set fmt = format() %}

            ... {{ fmt.decimal(number) }} ...
            ... {{ fmt.datetime(timestamp) }} ...

        Note that the current locale can be influenced with the ``language`` tag, while the current
        time zone can be influenced with the ``timezone`` tag:

        .. code-block:: jinja

            {% language 'en-us' %}
            {% timezone 'Europe/London' %}

            {{ format().datetime(timestamp, format='long') }}
            <!-- if timestamp is datetime(2023, 7, 1, 14, 34, 56, tzinfo=timezone.utc) -->
            <!-- displays 1 July 2023, 15:34:56 BST -->

            {% endtimezone %}
            {% endlanguage %}

    """
    return Format(
        locale=locale or Locale.parse(language_code or get_language(), sep='-'),
        tzinfo=tzinfo or timezone.get_current_timezone(),
    )


def cwd() -> Path:
    """
    Return the current working directory.
    """
    return Path(os.getcwd())


def now() -> datetime:
    """
    Return the current date and time.
    """
    return timezone.now()


def bibliography(name: str) -> 'django_logikal.bibliography.Bibliography':
    """
    Return a :class:`~django_logikal.bibliography.Bibliography` instance.

    Args:
        name: The name of the bibliography configuration to use.

    .. note:: Requires the :ref:`bibliography extra <index:Bibliography>`.

    Usage
    -----
    First, make sure that your bibliographies are in the appropriate template folders and that
    their paths are added to the Django settings file as follows:

    .. code-block::

        BIBLIOGRAPHIES = {'references': 'website/references.bib'}

    Once configured, you can use this function in templates as follows:

    .. code-block:: jinja

        {% set bib = bibliography('references') %}
        {% set cite = bib.cite %}

        ... {{ cite('entry') }} ...

        {{ bib.references() }}

    """
    from django_logikal.bibliography import Bibliography  # pylint: disable=import-outside-toplevel

    return Bibliography(name=name)
