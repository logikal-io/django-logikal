from typing import Any, List, Mapping, Optional, Sequence, Tuple, Type, Union

import debug_toolbar
from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import URLPattern, URLResolver, include, path

from django_logikal.env import is_dev, option_is_set
from django_logikal.views import ERROR_HANDLERS, public

URLType = Union[URLResolver, URLPattern]
IncludeType = Tuple[Sequence[URLType], Optional[str], Optional[str]]


def admin_urls() -> IncludeType:
    """
    Return URLs for the :mod:`django.contrib.auth` app.
    """
    urls = admin.site.urls
    for url in urls[0]:
        if getattr(url, 'name', None) == 'login' and url.callback:
            url.callback = public(url.callback)
            break
    return urls


def error_urls() -> IncludeType:
    """
    Return URLs for the standard error handler pages.
    """
    return include(([
        path(f'{code}/', view, name=str(code))
        for code, view in ERROR_HANDLERS.items()
    ], 'error'))


def debug_toolbar_urls() -> IncludeType:  # pragma: no cover, tested in subprocess
    """
    Return URLs for the Django debug toolbar.
    """
    urls = list(debug_toolbar.toolbar.DebugToolbar.get_urls())
    for url in urls:
        for url_item in getattr(url, 'url_patterns', [url]):
            url_item.callback = public(url_item.callback)
    return include((urls, debug_toolbar.APP_NAME))


def utility_paths(
    sitemaps: Optional[Mapping[str, Union[Sitemap[Any], Type[Sitemap[Any]]]]],
    static: bool = False,
) -> List[URLType]:
    """
    Return the common utility paths.

    Includes the admin paths, sitemap and robots paths and the Django debug toolbar paths (when
    appropriate). Also includes the standard error paths when running locally.
    """
    # Note: we have to import late for documentation building to succeed
    from robots.views import rules_list  # pylint: disable=import-outside-toplevel

    paths: List[URLType] = []
    universal_path = path  # included for both static and dynamic sites
    if static:
        from django_distill import distill_path  # pylint: disable=import-outside-toplevel
        universal_path = distill_path
    else:
        paths.append(path('admin/', admin_urls()))
    if is_dev():
        paths.append(path('error/', error_urls()))
    if option_is_set('toolbar'):  # pragma: no cover, tested in subprocess
        paths.append(universal_path('__debug__/', debug_toolbar_urls()))
    if sitemaps:
        extra = {'sitemaps': sitemaps}
        paths.append(universal_path('sitemap.xml', public(sitemap), extra, name='sitemap'))
    paths.append(universal_path('robots.txt', public(rules_list), name='robots'))
    return paths
