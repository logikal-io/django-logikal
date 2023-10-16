from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from django.http import HttpResponseBase
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView
from django_stubs_ext import StrOrPromise

from django_logikal.sitemap import StaticSitemap
from django_logikal.views import public as mark_public


class Template:
    def __init__(
        self,
        app: Optional[str] = None,
        public: bool = False,
        extra_context: Optional[Dict[str, Any]] = None,
    ):
        self.app = app
        self.public = public
        self.extra_context = extra_context
        self._path_priority: Dict[str, str] = {}

    def _view(
        self,
        name: str,
        public: Optional[bool] = None,
        extra_context: Optional[Dict[str, Any]] = None,
    ) -> Callable[..., HttpResponseBase]:
        extra_context = {**(self.extra_context or {}), **(extra_context or {})}
        template_name = f'{self.app + "/" if self.app else ""}{name}.html.j'
        view = TemplateView.as_view(template_name=template_name, extra_context=extra_context)
        public = public if public is not None else self.public
        return mark_public(view) if public else view

    def _add_path_priority(self, name: str, priority: Optional[str]) -> None:
        if priority:
            self._path_priority[name if not self.app else f'{self.app}:{name}'] = priority

    def path(  # pylint:disable=too-many-arguments
        self,
        route: StrOrPromise,
        name: str,
        public: Optional[bool] = None,
        priority: Optional[str] = None,
        extra_context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> URLPattern:
        self._add_path_priority(name, priority)
        view = self._view(name, extra_context=extra_context, public=public)
        return path(route=route, view=view, name=name, **kwargs)

    def static_path(
        self,
        route: StrOrPromise,
        name: str,
        priority: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        self._add_path_priority(name, priority)
        from django_distill import distill_path  # pylint: disable=import-outside-toplevel
        return distill_path(route=route, view=self._view(name), name=name, **kwargs)

    def include(
        self, paths: List[URLPattern],
    ) -> Tuple[Sequence[Union[URLResolver, URLPattern]], Optional[str], Optional[str]]:
        if not self.app:
            raise RuntimeError('The app name must be specified')
        return include((paths, self.app))

    def sitemap(self) -> StaticSitemap:
        return StaticSitemap(path_priority=self._path_priority)
