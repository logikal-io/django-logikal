from collections.abc import Callable, Sequence
from typing import Any

from django.http import HttpResponseBase
from django.urls import URLPattern, include, path
from django.views.generic import TemplateView
from django_stubs_ext import StrOrPromise

from django_logikal.sitemap import StaticSitemap
from django_logikal.urls import URLType
from django_logikal.views import public as mark_public


class Template:
    def __init__(
        self,
        app: str | None = None,
        public: bool = False,
        extra_context: dict[str, Any] | None = None,
    ):
        self.app = app
        self.public = public
        self.extra_context = extra_context
        self._path_priority: dict[str, str] = {}

    def _view(
        self,
        name: str,
        public: bool | None = None,
        extra_context: dict[str, Any] | None = None,
    ) -> Callable[..., HttpResponseBase]:
        get_context_data = self.__class__.get_context_data
        context = {**(self.extra_context or {}), **(extra_context or {})}

        class TemplateViewWithContext(TemplateView):
            def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
                return {**context, **get_context_data(self, **kwargs)}  # type: ignore[arg-type]

        template_name = f'{self.app + '/' if self.app else ''}{name}.html.j'
        view = TemplateViewWithContext.as_view(template_name=template_name)
        public = public if public is not None else self.public
        return mark_public(view) if public else view

    def _add_path_priority(self, name: str, priority: str | None) -> None:
        if priority:
            self._path_priority[name if not self.app else f'{self.app}:{name}'] = priority

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # pylint: disable=no-self-use
        return {}

    def path(  # pylint:disable=too-many-arguments
        self,
        route: StrOrPromise,
        *,
        name: str,
        public: bool | None = None,
        priority: str | None = None,
        extra_context: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> URLPattern:
        self._add_path_priority(name, priority)
        view = self._view(name, extra_context=extra_context, public=public)
        return path(route=route, view=view, name=name, **kwargs)

    def static_path(
        self,
        route: StrOrPromise,
        name: str,
        priority: str | None = None,
        **kwargs: Any,
    ) -> Any:
        self._add_path_priority(name, priority)
        from django_distill import distill_path  # pylint: disable=import-outside-toplevel
        return distill_path(route=route, view=self._view(name), name=name, **kwargs)

    def include(
        self, paths: list[URLPattern],
    ) -> tuple[Sequence[URLType], str | None, str | None]:
        if not self.app:
            raise RuntimeError('The app name must be specified')
        return include((paths, self.app))

    def sitemap(self) -> StaticSitemap:
        return StaticSitemap(path_priority=self._path_priority)
