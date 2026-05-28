import re

from docutils import nodes
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.util.docfields import TypedField


class JinjaComponentModule(ObjectDescription[str]):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> str:
        signode += addnodes.desc_annotation('', 'module ')
        signode += addnodes.desc_name(sig, sig)
        return sig

    def run(self) -> list[nodes.Node]:
        module = self.arguments[0]
        component_head = f'{{{{ component_head(\'{module}\') }}}}'
        self.content = StringList([
            '**Usage:**',
            '',
            '.. code-block:: jinja',
            '',
            f'  {{% block component_head %}}{component_head}{{% endblock %}}',
        ])
        return super().run()


class JinjaMacro(ObjectDescription[str]):
    has_content = True
    doc_field_types = [
        TypedField(
            'parameter',
            label='Parameters',
            names=('param',),
            typenames=('type',),
            can_collapse=True,
        ),
    ]

    def _toc_entry_name(self, sig_node: addnodes.desc_signature) -> str:
        return sig_node.children[1].astext()

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> str:
        if not (match := re.match(r'([^\(]+)\((.*)\)', sig)):
            signode += addnodes.desc_name(sig, sig)
            return sig

        name, args = match.groups()
        signode += addnodes.desc_annotation('macro ', 'macro ')
        signode += addnodes.desc_name(name, name)

        parameters = addnodes.desc_parameterlist()
        for arg in args.split(','):
            param = addnodes.desc_parameter()
            if '=' not in arg:
                param += nodes.Text(arg)
            else:
                param_name, param_default = arg.split('=', 1)
                param += nodes.Text(param_name.strip())
                param += addnodes.desc_sig_operator('', '=')
                value_node = nodes.inline(param_default.strip(), param_default.strip())
                value_node['classes'].append('default_value')
                param += value_node

            parameters += param
        signode += parameters
        return name

    def add_target_and_index(self, name: str, sig: str, signode: addnodes.desc_signature) -> None:
        macro = name.replace('.', '-')
        if (target_id := f'jinja-macro-{macro}') not in self.state.document.ids:
            signode['names'].append(target_id)
            signode['ids'].append(target_id)
            self.state.document.note_explicit_target(signode)

            domain = self.env.get_domain('jinja')
            domain.note_object(name, self.objtype, target_id)  # type: ignore[attr-defined]
