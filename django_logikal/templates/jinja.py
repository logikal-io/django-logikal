# pylint: disable=import-outside-toplevel
import re
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.template import Origin, TemplateDoesNotExist
from django.template.backends.jinja2 import Jinja2, Template
from django.utils import translation
from jinja2.environment import Environment, Template as EnvironmentTemplate
from jinja2.runtime import StrictUndefined
from logikal_utils.imports import installed

from django_logikal.templates import filters, functions, tests

DEFAULT_OPTIONS = {
    'undefined': StrictUndefined,
    'trim_blocks': True,
    'lstrip_blocks': True,
    # See https://github.com/pallets/jinja/issues/178
    # 'indent_blocks': True,
    'extensions': [
        'jinja2.ext.i18n',
        'django_logikal.templates.extensions.LanguageExtension',
        'django_logikal.templates.extensions.TimeZoneExtension',
    ],
}

CONTEXT_PROCESSORS = [
    'django_logikal.templates.processors.add_messages',
    'django_logikal.templates.processors.add_csp_nonce',
]


class JinjaTemplate(Template):
    def __init__(
        self,
        template: EnvironmentTemplate,
        backend: Jinja2,
        block_name: str = '',
    ) -> None:
        self._block_name = block_name
        super().__init__(template=template, backend=backend)

    def render(
        self,
        context: dict[str, Any] | None = None,
        request: HttpRequest | None = None,
    ) -> str:
        if self._block_name:
            if self._block_name not in self.template.blocks:
                error = f'Block "{self._block_name}" not found in "{self.template.name}"'
                raise RuntimeError(error)
            context = self.template.new_context(context)
            blocks = self.template.blocks[self._block_name](context)
            return ''.join(block for block in blocks)

        return super().render(context=context, request=request)


class JinjaTemplates(Jinja2):
    app_dirname = 'templates'

    def __init__(self, params: dict[str, Any]) -> None:
        params = params.copy()
        self._extension = params['OPTIONS'].pop('match_extension', '.j')
        environment_path = f'{environment.__module__}.{environment.__qualname__}'
        params['OPTIONS'].setdefault('environment', environment_path)
        for option, value in DEFAULT_OPTIONS.items():
            params['OPTIONS'].setdefault(option, value)
        params['OPTIONS'].setdefault('context_processors', CONTEXT_PROCESSORS)
        super().__init__(params)

    def get_template(self, template_name: str) -> Any:
        template_name, _, block_name = template_name.partition('#')
        if template_name.endswith(self._extension):
            django_template = super().get_template(template_name)
            return JinjaTemplate(
                template=django_template.template,
                backend=django_template.backend,
                block_name=block_name,
            )

        origin = Origin(name=template_name, loader=self.env.loader)
        error = f'Skipping template search as the template extension is not "{self._extension}"'
        raise TemplateDoesNotExist(template_name, tried=[(origin, error)], backend=self)


def environment(**options: Any) -> Environment:
    options = {option: value for option, value in options.items() if option != 'autoescape'}
    env = Environment(**options, autoescape=True)
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
        'isinstance': isinstance,
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
        'exclude': filters.exclude,
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
        'faker_factory': functions.faker_factory,
        'component_head': functions.component_head,
    })
    if installed('django_htmx'):
        from django_htmx.jinja import django_htmx_script, htmx_script

        env.globals.update({
            'django_htmx_script': django_htmx_script,
            'htmx_script': htmx_script,
        })

    return env
