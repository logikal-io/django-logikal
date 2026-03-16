import importlib
import os
import re
import sys
from pathlib import Path

from docutils import nodes
from docutils.statemachine import StringList
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader
from jinja2.nodes import Macro
from logikal_utils.project import tool_config
from sphinx import addnodes, domains
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription
from sphinx.ext.napoleon.docstring import GoogleDocstring
from sphinx.util.docfields import TypedField
from sphinx.util.docutils import SphinxDirective

sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = tool_config('django_logikal')['DJANGO_SETTINGS_MODULE']


def strip_patch(package: str) -> str:
    return '.'.join(pkg_version(package).split('.')[0:2])  # major.minor (excluding patch)


def pkg_version(package_name: str) -> str:
    return importlib.metadata.version(package_name)


extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
]

intersphinx_mapping = {
    'python': (f'https://docs.python.org/{sys.version_info[0]}.{sys.version_info[1]}', None),
    'django': (
        f'https://docs.djangoproject.com/en/{strip_patch('django')}/',
        f'https://docs.djangoproject.com/en/{strip_patch('django')}/_objects/',
    ),
    'babel': ('https://babel.pocoo.org/en/latest/', None),
    'jinja2': (f'https://jinja.palletsprojects.com/en/{strip_patch('jinja2')}.x/', None),
    'django-robots': ('https://django-robots.readthedocs.io/en/latest/', None),
    'django-anymail': (f'https://anymail.dev/en/v{pkg_version('django-anymail')}/', None),
    'django-csp': ('https://django-csp.readthedocs.io/en/latest/', None),
    'factory-boy': (f'https://factoryboy.readthedocs.io/en/{pkg_version('factory-boy')}/', None),
    'stormware': (f'https://docs.logikal.io/stormware/{pkg_version('stormware')}/', None),
    'pytest-logikal': (
        f'https://docs.logikal.io/pytest-logikal/{pkg_version('pytest-logikal')}/', None,
    ),
}

nitpick_ignore = [
    ('py:func', 'type'),
    ('py:class', 'django.conf.LazySettings'),
    ('py:class', 'django.http.request.HttpRequest'),
    ('py:class', 'django.http.response.HttpResponse'),
    ('py:class', 'django.http.response.HttpResponseBase'),
    ('py:class', 'django.http.response.HttpResponseNotFound'),
    ('py:class', 'django.http.response.HttpResponseServerError'),
    ('py:class', 'django.urls.resolvers.URLResolver'),
    ('py:class', 'django.urls.resolvers.URLPattern'),
    ('py:class', 'django.core.management.base.CommandParser'),
]

html_static_path = ['static']

napoleon_custom_sections = [
    ('CSS variables', 'params_style'),
]


def strip_modules(
    app: Sphinx,  # pylint: disable=unused-argument
    doctree: nodes.document,
) -> None:  # pragma: no cover
    modules = set([
        'django_logikal.templates.filters',
        'django_logikal.templates.tests',
        'django_logikal.templates.functions',
    ])
    for signature in doctree.findall(addnodes.desc_signature):
        if signature.get('module') in modules:
            del signature[0]  # remove module text


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
            if arg_str := arg.strip():
                parameters += addnodes.desc_parameter(arg_str, arg_str)
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


class JinjaAutoModuleDirective(SphinxDirective):
    has_content = True
    required_arguments = 1

    def run(self) -> list[nodes.Element]:  # pylint: disable=too-many-locals
        # Load template file
        source_path_str = self.arguments[0]
        source_path = Path(source_path_str)
        module = source_path.name.split('.')[0]
        module_path = '/'.join(source_path_str.split('/')[2:])
        source = source_path.read_text(encoding='utf-8')
        source_lines = source.splitlines()
        environment = Environment(loader=FileSystemLoader('.'), autoescape=True)
        template = environment.parse(source)

        blocks = [f'.. jinja:module:: {module_path}']
        for macro in template.find_all(Macro):
            # Get documentation
            first_line = source_lines[macro.lineno]
            indent = len(first_line) - len(first_line.lstrip())
            if not first_line[indent:].startswith('{#'):
                raise RuntimeError('Invalid macro documentation')
            if first_line.endswith('#}'):
                doc = [first_line[indent + 2:].replace('#}', '').strip()]
            else:
                doc = []
                for line in source_lines[macro.lineno + 1:]:
                    if line.strip() != '#}':
                        doc.append(line[indent:])
                    if '#}' in line:
                        break

            config = self.env.app.config
            docstring = str(GoogleDocstring(doc, config, what='function'))
            docstring = re.sub(r':type (\w+): (\w+)', r':type \1: :py:obj:`\2`', docstring)
            docstring = re.sub(r'\* \*\*(--[^*]+)\*\*', r'* :css:`\1`', docstring)

            # Build text
            arguments = ', '.join(arg.name for arg in macro.args)
            blocks.extend([
                '',
                f'  .. jinja:macro:: {module}.{macro.name}({arguments})',
                '',
                *[f'    {line}' for line in docstring.splitlines()],
            ])

        # Parse blocks
        parsed_blocks = StringList()
        for block in blocks:
            parsed_blocks.append(block, source=source_path_str)

        container = nodes.container()
        self.state.nested_parse(block=parsed_blocks, input_offset=0, node=container)
        return [container]


class JinjaExampleDirective(SphinxDirective):
    has_content = True

    def run(self) -> list[nodes.Element]:
        if not self.state.document.current_source:
            raise RuntimeError('Source module cannot be derived')
        module_path = '/'.join(self.state.document.current_source.split('/')[2:])
        module = Path(module_path).stem.split('.')[0]

        # Rendering source
        jinja_content = '\n'.join(self.content)
        main_content = f'{{% import \'{module_path}\' as {module} %}}\n{jinja_content}'
        environment = Environment(loader=ChoiceLoader([
            DictLoader({'main': main_content}),
            FileSystemLoader('django_logikal/templates/'),
        ]), autoescape=True)
        rendered = environment.get_template('main').render()

        container = nodes.container()
        container['classes'].append('jinja-example-block')
        container += nodes.caption('', 'Example')
        blocks = [
            '.. tab-set::',
            '  :sync-group: type',
            '',
            '  .. tab-item:: Jinja',
            '    :sync: jinja',
            '',
            '    .. code-block:: jinja',
            '',
            *[f'      {line}' for line in jinja_content.splitlines()],
            '',
            '  .. tab-item:: HTML',
            '    :sync: html',
            '',
            '    .. code-block:: html',
            '',
            *[f'    {line}' for line in rendered.splitlines()],
        ]
        parsed_blocks = StringList()
        for block in blocks:
            parsed_blocks.append(block, source=module_path)

        self.state.nested_parse(block=parsed_blocks, input_offset=0, node=container)

        # Rendering HTML
        rendered_node = nodes.raw('', rendered, format='html')
        rendered_node['classes'].append('render-block')
        container += rendered_node

        return [container]


class JinjaDomain(domains.Domain):  # pylint: disable=abstract-method
    name = 'jinja'
    label = 'Jinja2'
    object_types = {
        'macro': domains.ObjType('macro', 'macro'),
        'module': domains.ObjType('module', 'module'),
    }
    directives = {
        'macro': JinjaMacro,
        'module': JinjaModule,
        'automodule': JinjaAutoModuleDirective,
        'example': JinjaExampleDirective,
    }


def setup(app: Sphinx) -> None:
    app.connect('doctree-read', strip_modules)
    app.add_domain(JinjaDomain)
    app.add_css_file('css/jinja.css')
    app.add_css_file('css/copybutton.css')
