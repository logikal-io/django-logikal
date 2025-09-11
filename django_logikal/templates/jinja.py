import re
from typing import Any

from django.conf import settings
from django.template import Origin, TemplateDoesNotExist
from django.template.backends.jinja2 import Jinja2
from django.utils import translation
from jinja2.environment import Environment
from jinja2.runtime import StrictUndefined

from django_logikal.templates import filters, functions, tests


class JinjaTemplates(Jinja2):
    app_dirname = 'templates'

    def __init__(self, params: dict[str, Any]):
        params = params.copy()
        self._extension = params['OPTIONS'].pop('match_extension', '.j')
        environment_path = f'{environment.__module__}.{environment.__qualname__}'
        params['OPTIONS'].setdefault('environment', environment_path)
        params['OPTIONS'].setdefault('undefined', StrictUndefined)
        params['OPTIONS'].setdefault('trim_blocks', True)
        params['OPTIONS'].setdefault('lstrip_blocks', True)
        # See https://github.com/pallets/jinja/issues/178
        # See https://github.com/pallets/jinja/pull/1456
        # params['OPTIONS'].setdefault('indent_blocks', True)
        params['OPTIONS'].setdefault('extensions', [
            'jinja2.ext.i18n',
            'csp.extensions.NoncedScript',
            'django_logikal.templates.extensions.LanguageExtension',
            'django_logikal.templates.extensions.TimeZoneExtension',
        ])
        params['OPTIONS'].setdefault('context_processors', [
            'django_logikal.templates.processors.add_messages',
        ])
        super().__init__(params)

    def get_template(self, template_name: str) -> Any:
        if template_name.endswith(self._extension):
            return super().get_template(template_name)
        origin = Origin(name=template_name, loader=self.env.loader)
        error = f'Skipping template search as the template extension is not "{self._extension}"'
        raise TemplateDoesNotExist(template_name, tried=[(origin, error)], backend=self)


def environment(**options: dict[str, Any]) -> Environment:
    options = {option: value for option, value in options.items() if option != 'autoescape'}
    env = Environment(**options, autoescape=True)  # type: ignore[arg-type]
    env.policies.update({'ext.i18n.trimmed': True})
    # Note: we might need to use a different gettext
    # (see https://code.djangoproject.com/ticket/34602)
    env.install_gettext_callables(  # type: ignore[attr-defined] # pylint: disable=no-member
        gettext=translation.gettext,
        ngettext=translation.ngettext,
        newstyle=True,
        pgettext=translation.pgettext,
        npgettext=translation.npgettext,
    )
    env.filters.update({
        # Built-in functions
        'dir': dir,
        'getattr': getattr,
        'hasattr': hasattr,
        'repr': repr,
        'type': type,
        # Built-in types
        'str': str,
        # Other utilities
        'upper_first': filters.upper_first,
        'join_lines': filters.join_lines,
        'slugify': filters.slugify,
        'unslugify': filters.unslugify,
        'wrap': filters.wrap,
        'nowrap': filters.nowrap,
        'truncate': filters.truncate,
    })
    env.tests.update({
        'startswith': tests.startswith,
    })
    env.globals.update({
        # Django objects
        'settings': settings,
        'filters': env.filters,
        'tests': env.tests,
        # Libraries
        're': re,
        # Django utilities
        'context': functions.context,
        'static': functions.static,
        'static_path': functions.static_path,
        'include_static': functions.include_static,
        'url': functions.url,
        'url_name': functions.url_name,
        'language': functions.language,
        'format': functions.format,
        # Other utilities
        'cwd': functions.cwd,
        'now': functions.now,
        'bibliography': functions.bibliography,
    })
    return env
