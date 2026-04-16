from collections.abc import Iterable

from sphinx import domains

from docs.jinja.directives import (
    JinjaAutoCSSVariablesDirective, JinjaAutoModuleDirective, JinjaExampleDirective,
)
from docs.jinja.elements import JinjaComponentModule, JinjaMacro


class JinjaDomain(domains.Domain):  # pylint: disable=abstract-method
    name = 'jinja'
    label = 'Jinja2'
    object_types = {
        'macro': domains.ObjType('macro', 'macro'),
        'component': domains.ObjType('component', 'component'),
        'automodule': domains.ObjType('automodule', 'automodule'),
    }
    directives = {
        'autocssvars': JinjaAutoCSSVariablesDirective,
        'macro': JinjaMacro,
        'component': JinjaComponentModule,
        'automodule': JinjaAutoModuleDirective,
        'example': JinjaExampleDirective,
    }
    initial_data = {'objects': {}}

    def note_object(self, name: str, objtype: str, node_id: str) -> None:
        self.data['objects'][name] = (self.env.docname, node_id, objtype)

    def get_objects(self) -> Iterable[tuple[str, str, str, str, str, int]]:
        for name, (docname, node_id, objtype) in self.data['objects'].items():
            yield (name, name, objtype, docname, node_id, 1)
