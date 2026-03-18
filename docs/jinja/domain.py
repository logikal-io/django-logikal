from sphinx import domains

from docs.jinja.directives import (
    JinjaAutoCSSVariablesDirective, JinjaAutoModuleDirective, JinjaExampleDirective,
)
from docs.jinja.elements import JinjaMacro, JinjaModule


class JinjaDomain(domains.Domain):  # pylint: disable=abstract-method
    name = 'jinja'
    label = 'Jinja2'
    object_types = {
        'macro': domains.ObjType('macro', 'macro'),
        'module': domains.ObjType('module', 'module'),
    }
    directives = {
        'autocssvars': JinjaAutoCSSVariablesDirective,
        'macro': JinjaMacro,
        'module': JinjaModule,
        'automodule': JinjaAutoModuleDirective,
        'example': JinjaExampleDirective,
    }
