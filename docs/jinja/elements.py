import re
from pathlib import Path

from docutils import nodes
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.util.docfields import TypedField


class JinjaModule(ObjectDescription[str]):
    has_content = True

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> str:
        module_path = Path(re.sub('.*\'([^\']+)\'.*', r'\1', sig))
        signode += addnodes.desc_annotation('', 'import ')
        signode += addnodes.desc_name(sig, f'\'{sig}\'')
        signode += addnodes.literal_emphasis('', ' as ')
        signode += addnodes.desc_addname('', module_path.stem.split('.')[0])
        return sig


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
        if (target := f'jinja-macro-{name}') not in self.state.document.ids:
            signode['names'].append(target)
            signode['ids'].append(target)
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)

            objects = self.env.domaindata['jinja'].setdefault('objects', {})
            if name in objects:
                raise RuntimeError(
                    f'Duplicate jinja macro description of {name}'
                    f' (other instance in "{self.env.doc2path(objects[name][0])}"'
                    f' at {self.lineno})'
                )
            objects[name] = (self.env.docname, 'macro')

        self.indexnode['entries'].append(('single', f'{name} (jinja macro)', target, '', None))
