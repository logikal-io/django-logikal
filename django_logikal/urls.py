from collections.abc import Sequence
from importlib import import_module
from typing import Any

import debug_toolbar
from django.conf import settings
from django.contrib import admin as django_admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import URLPattern, URLResolver, include, path

from django_logikal.env import is_dev_env, is_testing_env, option_is_set
from django_logikal.views.account import AccountView, AuthView
from django_logikal.views.generic import ERROR_HANDLERS, public

URLType = URLResolver | URLPattern
IncludeType = tuple[Sequence[URLType], str | None, str | None]


def auth_urls() -> IncludeType:
    """
    Return URLs for the :mod:`allauth` app.
    """
    from allauth import urls  # pylint: disable=import-outside-toplevel

    public_view_names = [
        # Login flow
        'account_login', 'account_logout', 'account_signup',
        # Email validation flow
        'account_email_verification_sent', 'account_confirm_email',
    ]
    for provider in settings.ALLAUTH_SOCIAL_PROVIDERS:
        provider_module = provider.lower()
        public_view_names.extend([f'{provider_module}_login', f'{provider_module}_callback'])

    for url in urls.urlpatterns:
        for url_item in getattr(url, 'url_patterns', [url]):
            url_name = getattr(url_item, 'name', None)
            if url_name in public_view_names and url_item.callback:
                url_item.callback = public(url_item.callback)

    # Views for the improved flow
    urls.urlpatterns.extend([
        path('', AccountView.as_view(), name='account'),
        path('auth/', AuthView.as_view(), name='account_auth'),
    ])
    return include(urls)


def admin_urls(admin_site: django_admin.AdminSite, use_allauth: bool) -> IncludeType:
    """
    Return URLs for the :mod:`django.contrib.admin` app.
    """
    urls = admin_site.urls
    for url in urls[0]:
        if getattr(url, 'name', None) == 'login' and url.callback:
            if use_allauth:
                from allauth.account.decorators import (  # pylint: disable=import-outside-toplevel
                    secure_admin_login
                )
                url.callback = secure_admin_login(url.callback)
            else:
                url.callback = public(url.callback)
            break
    return urls


def error_urls() -> IncludeType:
    """
    Return URLs for the standard error handler pages.
    """
    urlconf = import_module(settings.ROOT_URLCONF)  # type: ignore[misc]
    return include(([
        path(f'{code}/', getattr(urlconf, f'handler{code}', error_view), name=str(code))
        for code, error_view in ERROR_HANDLERS.items()
    ], 'error'))


def debug_toolbar_urls() -> IncludeType:  # pragma: no cover, tested in subprocess
    """
    Return URLs for the Django debug toolbar.
    """
    urls = debug_toolbar.toolbar.DebugToolbar.get_urls()
    for url in urls:
        for url_item in getattr(url, 'url_patterns', [url]):
            url_item.callback = public(url_item.callback)
    return include((urls, debug_toolbar.APP_NAME))


def utility_paths(
    sitemaps: dict[str, Sitemap[Any] | type[Sitemap[Any]]] | None = None,
    auth: bool = True,
    admin: bool = True,
    admin_site: django_admin.AdminSite | None = None,
    static: bool = False,
) -> list[URLType]:
    """
    Return the common utility paths.

    Includes the admin paths, auth paths, sitemap and robots paths and the Django debug toolbar
    paths (when appropriate). Also includes the standard error paths when running locally.
    """
    # Note: we have to import late for documentation building to succeed
    from robots.views import rules_list  # pylint: disable=import-outside-toplevel

    paths: list[URLType] = []
    universal_path = path  # included for both static and dynamic sites
    if static:
        from django_distill import distill_path  # pylint: disable=import-outside-toplevel

        universal_path = distill_path
    else:
        if auth:
            paths.append(path('account/', auth_urls()))
        if admin:
            admin_site = admin_site if admin_site is not None else django_admin.site
            paths.append(path('admin/', admin_urls(admin_site=admin_site, use_allauth=auth)))
    if is_dev_env() or is_testing_env():
        paths.append(path('error/', error_urls()))
    if option_is_set('toolbar'):  # pragma: no cover, tested in subprocess
        paths.append(universal_path('__debug__/', debug_toolbar_urls()))
    if sitemaps:
        extra = {'sitemaps': sitemaps}
        paths.append(universal_path('sitemap.xml', public(sitemap), extra, name='sitemap'))
    paths.append(universal_path('robots.txt', public(rules_list), name='robots'))
    return paths
