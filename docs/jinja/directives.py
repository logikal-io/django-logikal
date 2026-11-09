import re
from abc import ABC
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import cache, partial
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import tinycss2
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader, nodes as jinja_nodes
from pytest_logikal.validator import Validator
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.ext.napoleon.docstring import GoogleDocstring
from sphinx.util.docutils import SphinxDirective

from django_logikal.templates import components, functions, jinja
from docs.jinja.format import format_html

COMPONENTS_CSS_STATIC_PATH = Path('django_logikal/static') / components.COMPONENTS_CSS_PATH

DOCS_STATIC_ROOT = Path(__file__).parents[1] / 'build/_static'
DOCS_COMPONENTS_CSS_PATH = Path('../_static') / components.COMPONENTS_CSS_PATH
DOCS_COMPONENTS_JS_PATH = Path('../_static') / components.COMPONENTS_JS_PATH
DOCS_THEMES_CSS_PATH = DOCS_COMPONENTS_CSS_PATH / 'themes'

THEME_MODES = ['light', 'dark']


@dataclass
class CSSVariable:
    name: str
    value: str
    description: str | None = None

    @property
    def formatted_value(self) -> str:
        return re.sub(r'\s+', ' ', self.value).replace('( ', '(').replace(' )', ')')

    def as_rst(self, with_description: bool = True) -> str:
        description = self.description if with_description else None
        rst = f':css:`{self.name}`'
        if description or self.value:
            rst += ' --'
        if description:
            rst += f' {description.capitalize()}.'
        if self.value:
            rst += f' Defaults to ``{self.formatted_value}``.'
        return rst


@dataclass
class CSSSeparator:
    """A blank-line boundary between variable groups."""


@dataclass
class CSSSection:
    title: str
    level: int
    elements: list['CSSVariable | CSSSection | CSSSeparator']

    @property
    def variables(self) -> Iterator[CSSVariable]:
        for element in self.elements:
            if isinstance(element, CSSVariable):
                yield element
            elif isinstance(element, CSSSection):
                yield from element.variables


@dataclass
class CSSRule:
    selector: str
    elements: list[CSSVariable | CSSSection | CSSSeparator]


def _next_comment(declarations: list[Any]) -> str | None:
    for declaration in declarations:
        if (
            isinstance(declaration, tinycss2.ast.WhitespaceToken)
            and '\n' not in declaration.value
        ):
            continue
        if isinstance(declaration, tinycss2.ast.Comment):
            value = declaration.value.strip()
            if not value.startswith('_'):
                return value
        return None
    return None


@cache
def parsed_stylesheet(path: Path) -> Any:
    contents = (Path(__file__).parents[2] / path).read_text(encoding='utf-8')
    return tinycss2.parse_stylesheet(contents, skip_comments=False, skip_whitespace=True)


def _parse_css_elements(
    content: list[Any],
) -> list[CSSVariable | CSSSection | CSSSeparator]:
    elements: list[CSSVariable | CSSSection | CSSSeparator] = []
    headings: list[CSSSection] = []
    attached_depth = 0
    inline = False
    separator_pending = False
    declarations = tinycss2.parse_declaration_list(content)

    for index, declaration in enumerate(declarations):
        # Parse whitespace
        if isinstance(declaration, tinycss2.ast.WhitespaceToken):
            inline = '\n' not in declaration.value
            if declaration.value.count('\n') >= 2:
                separator_pending = True
            continue

        # Parse section headings
        if isinstance(declaration, tinycss2.ast.Comment):
            value = declaration.value.strip()
            if inline or value.startswith('_'):
                continue

            separator_pending = False
            level = len(value) - len(value.lstrip('*'))
            headings = [heading for heading in headings if heading.level < level]
            attached_depth = min(attached_depth, len(headings))
            headings.append(CSSSection(title=value.strip('*').strip(), level=level, elements=[]))
            continue

        # Parse variable declarations
        if not isinstance(declaration, tinycss2.ast.Declaration):
            continue
        if not declaration.name.strip().startswith('--'):
            continue

        target = headings[attached_depth - 1].elements if attached_depth else elements
        for section in headings[attached_depth:]:
            target.append(section)
            target = section.elements
        attached_depth = len(headings)

        # Separate variable groups
        if separator_pending and target and isinstance(target[-1], CSSVariable):
            target.append(CSSSeparator())
        separator_pending = False

        target.append(CSSVariable(
            name=declaration.name,
            value=tinycss2.serialize(declaration.value).strip(),
            description=_next_comment(declarations[index + 1:]),
        ))

    return elements


@cache
def parsed_css_rules(path: Path) -> list[CSSRule]:
    rules = []
    for rule in parsed_stylesheet(path):
        if not hasattr(rule, 'prelude') or rule.content is None:
            continue
        if elements := _parse_css_elements(rule.content):
            rules.append(CSSRule(
                selector=tinycss2.serialize(rule.prelude).strip(),
                elements=elements,
            ))
    return rules


class JinjaSphinxDirective(ABC, SphinxDirective):
    def parse_rst_blocks(
        self,
        blocks: list[str],
        source: str,
        node: nodes.Element | None = None,
    ) -> nodes.Node:
        parsed_blocks = StringList()
        for rst_block in blocks:
            parsed_blocks.append(rst_block, source=source)

        node = node or nodes.container()
        self.state.nested_parse(block=parsed_blocks, input_offset=0, node=node)
        return node

    @staticmethod
    def _static(path: str) -> Path:
        return DOCS_STATIC_ROOT / path

    @staticmethod
    def _url(viewname: str, **kwargs: Any) -> str:
        url = viewname.replace(':', '/') + '/'
        if kwargs:
            url += '/'.join(f'{key}/{value}' for key, value in kwargs['kwargs'].items()) + '/'
        return url

    @staticmethod
    def _include_static_path(path: str) -> Path:
        return Path(__file__).parents[2] / 'django_logikal/static' / path

    def get_environment(self, **kwargs: Any) -> Environment:
        from django_logikal.forms import (  # pylint: disable=import-outside-toplevel
            account, allauth,
        )

        request = SimpleNamespace(resolver_match=SimpleNamespace(view_name='main:home'))
        request.GET = {}
        render_context = {
            'request': request,
            'csrf_input': '',
            'messages': ['Notification message.'],
        }
        env = jinja.environment(**kwargs, **jinja.DEFAULT_OPTIONS)
        env.globals.update({
            **render_context,
            'static': self._static,
            'include_static': partial(
                functions.include_static,
                static_path_function=self._include_static_path,
            ),
            'url': self._url,
            # Forms
            'auth_form': account.AuthForm(render_context=render_context),
            'login_form': allauth.LoginForm(render_context=render_context),
        })
        env.install_gettext_callables(  # type: ignore[attr-defined] # pylint: disable=no-member
            gettext=lambda text: text,
            ngettext=lambda text: text,
            newstyle=True,
            pgettext=lambda text: text,
            npgettext=lambda text: text,
        )
        return env

    def get_css_variable_sections(
        self,
        path: Path,
        css_selector: str | None = None,
        section_selector: list[str] | None = None,
    ) -> Sequence[CSSVariable | CSSSection | CSSSeparator]:
        css_path = (Path(__file__).parents[2] / path).resolve()
        self.env.note_dependency(str(css_path))

        # Select rules
        rules = [
            rule for rule in parsed_css_rules(path)
            if css_selector is None or css_selector in rule.selector
        ]
        elements = [element for rule in rules for element in rule.elements]
        if section_selector is None:
            return elements

        # Select sections
        sections: list[CSSSection] = []
        for index, title in enumerate(section_selector):
            sections = [
                element for element in elements
                if isinstance(element, CSSSection) and element.title == title
            ]
            if index < len(section_selector) - 1:
                elements = [element for section in sections for element in section.elements]

        # Check matches
        if not sections:
            raise self.error(f'CSS section not found: {section_selector}')
        if len(sections) > 1:
            raise self.error(f'Ambiguous CSS section: {section_selector}')
        return sections

    def get_css_variables(self, path: Path, selector: str) -> list[CSSVariable]:
        variables: list[CSSVariable] = []
        for element in self.get_css_variable_sections(path=path, css_selector=selector):
            if isinstance(element, CSSVariable):
                variables.append(element)
            elif isinstance(element, CSSSection):
                variables.extend(element.variables)
        return variables


class JinjaAutoCSSVariablesDirective(JinjaSphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {
        'selector': directives.unchanged_required,
        'section': directives.unchanged_required,
        'open': directives.flag,
    }

    def _elements_as_rst(
        self,
        elements: Sequence[CSSVariable | CSSSection | CSSSeparator],
        indent: int = 0,
        open_sections: bool = False,
    ) -> list[str]:
        blocks = []
        for element in elements:
            if isinstance(element, CSSSection):
                blocks.extend(['', f'{indent * ' '}.. dropdown:: {element.title}'])
                if indent > 0 or open_sections:
                    blocks.append(f'{(indent + 1) * ' '}:open:')
                blocks.append('')
                blocks.extend(self._elements_as_rst(element.elements, indent + 2))
            elif isinstance(element, CSSSeparator):
                blocks.extend([
                    '',
                    f'{(indent + 1) * ' '}.. raw:: html',
                    '',
                    f'{(indent + 3) * ' '}<hr>',
                    '',
                ])
            else:
                variable = f':css-variable-name:`{element.name}`'
                if element.value:
                    variable += (
                        r'\ :css-variable-separator:`:`'
                        f' :css-variable-value:`{element.formatted_value};`'
                    )
                blocks.append(f'{(indent + 1) * ' '}* {variable}')
        return blocks

    def run(self) -> list[nodes.Node]:
        section_selector = [
            part.strip() for part in self.options.get('section', '').split('/') if part
        ]
        elements = self.get_css_variable_sections(
            path=Path(self.arguments[0]),
            css_selector=self.options.get('selector'),
            section_selector=section_selector or None,
        )
        return [self.parse_rst_blocks(
            blocks=[
                '.. role:: css-variable-name(literal)',
                '',
                '.. role:: css-variable-separator',
                '',
                '.. role:: css-variable-value(literal)',
                '',
                *self._elements_as_rst(elements, open_sections='open' in self.options),
            ],
            source=self.arguments[0],
        )]


class JinjaAutoModuleDirective(ObjectDescription[str], JinjaSphinxDirective):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> str:
        import_path = self._import_path(sig)
        signode += addnodes.desc_annotation('', 'template ')
        signode += addnodes.desc_name(import_path, import_path)
        return sig

    def add_target_and_index(self, name: str, sig: str, signode: addnodes.desc_signature) -> None:
        module = Path(name).stem.split('.')[0]
        if (target_id := f'jinja-module-{module}') not in self.state.document.ids:
            signode['names'].append(module)
            signode['ids'].append(target_id)
            self.state.document.note_explicit_target(signode)

            domain = self.env.get_domain('jinja')
            domain.note_object(name, self.objtype, target_id)  # type: ignore[attr-defined]

    @staticmethod
    def _import_path(path: str | Path) -> str:
        return '/'.join(str(path).split('/')[2:])  # remove first two directories

    def _get_docs(self, macro: jinja_nodes.Macro, source_lines: list[str]) -> str:
        docs = []
        indent = 0
        collect = False
        for line in source_lines[macro.lineno - 1:]:
            if line.lstrip().startswith('{#'):
                if line.endswith('#}'):
                    docs.append(line.replace('{#', '').replace('#}', '').strip())
                    break
                indent = len(line) - len(line.lstrip())
                collect = True
            elif line.endswith('#}'):
                break
            elif collect:
                docs.append(line[indent:])

        if not docs:
            raise RuntimeError(f'Invalid or missing macro documentation for "{macro.name}"')

        docstring = GoogleDocstring(docstring=docs, config=self.env.app.config, what='function')
        return str(docstring)

    def _render_node(self, node: jinja_nodes.Expr | None) -> str:
        rendered = '[complex expression]'
        if node is None:
            rendered = 'None'
        if isinstance(node, jinja_nodes.Name):
            rendered = node.name
        if isinstance(node, jinja_nodes.Const):
            rendered = repr(node.value)
        if isinstance(node, jinja_nodes.Call):
            name = self._render_node(node.node)
            args = [self._render_node(arg) for arg in node.args]
            kwargs = [f'{arg.key}={self._render_node(arg.value)}' for arg in node.kwargs]
            rendered = f'{name}({', '.join(args + kwargs)})'
        if isinstance(node, jinja_nodes.Getattr):
            rendered = f'{self._render_node(node.node)}.{node.attr}'
        if isinstance(node, jinja_nodes.Filter):
            rendered = f'{self._render_node(node.node)}|{node.name}'
        return rendered

    def run(self) -> list[nodes.Node]:  # pylint: disable=too-many-locals
        parent_nodes = super().run()

        # Load template file
        source_path_str = self.arguments[0]
        source_path = Path(source_path_str)
        module = source_path.name.split('.')[0]
        source = source_path.read_text(encoding='utf-8')
        source_lines = source.splitlines()
        env = self.get_environment(loader=FileSystemLoader('.'))
        template = env.parse(source)
        stylesheet_path = COMPONENTS_CSS_STATIC_PATH / f'{module}.css'

        # Mark file as a dependency
        self.state.document.settings.env.note_dependency(str(source_path.absolute()))

        # Build module documentation
        component_head = f'{{{{ component_head(\'{module}\') }}}}'
        blocks = [
            '  **Usage:**',
            '',
            '  .. code-block:: jinja',
            '',
            f'    {{% import \'{self._import_path(source_path)}\' as {module} %}}',
            f'    {{% block component_head %}}{component_head}{{% endblock %}}',
            '',
            '  **Components:**',
        ]
        for macro in template.find_all(jinja_nodes.Macro):
            if macro.name.startswith('_'):  # skip internal private macros
                continue

            # Get CSS variables
            docs = self._get_docs(macro=macro, source_lines=source_lines)
            if variables := self.get_css_variables(
                path=stylesheet_path,
                selector=f'.{macro.name.replace('_', '-')}',
            ):
                variables_str = '\n'.join([
                    ':CSS variables:',
                    *[f'  * {variable.as_rst()}' for variable in variables],
                ])
                docs = re.sub(
                    r'\.\. jinja:example::',
                    f'{variables_str}\n\n.. jinja:example::',
                    docs,
                )

            # Build text
            mandatory_args = len(macro.args) - len(macro.defaults)
            arg_specs = []
            for index, arg in enumerate(macro.args):
                if index < mandatory_args:
                    arg_specs.append(arg.name)
                else:
                    default_node = macro.defaults[index - mandatory_args]
                    default_value = self._render_node(default_node)
                    arg_specs.append(f'{arg.name}={default_value}')

            blocks.extend([
                '',
                f'  .. jinja:macro:: {module}.{macro.name}({', '.join(arg_specs)})',
                '',
                *[f'    {line}' for line in docs.splitlines()],
            ])

        node = cast(addnodes.desc, parent_nodes[1])
        node += self.parse_rst_blocks(blocks=blocks, source=source_path_str)
        return parent_nodes


class JinjaExampleDirective(JinjaSphinxDirective):
    has_content = True
    option_spec = {'scheme': partial(directives.choice, values=THEME_MODES)}

    @staticmethod
    def _validate(content: str, source_path: str) -> None:
        body = content
        if not re.match(r'\s*<body(?=[\s>])', content, flags=re.IGNORECASE):
            body = f'<body>{content}</body>'

        if errors := Validator().errors(content=f"""
            <!DOCTYPE html>
            <html lang="en-us">
              <head>
                <meta charset="utf-8">
                <title>Example</title>
              </head>
              {body}
            </html>
        """):
            error_str = '\n'.join(error.message for error in errors)
            raise RuntimeError(
                f'Validation errors on "{source_path}":\n{error_str} (content: {content})'
            )

    @staticmethod
    def _render_html(
        head: str,
        rendered: str,
        container: nodes.Element,
        scheme: str | None = None,
    ) -> None:
        modes = [scheme] if scheme else THEME_MODES
        for index, mode in enumerate(modes):
            rendered_block = f"""
                <template shadowrootmode="open">
                    <link rel="stylesheet" href="{DOCS_THEMES_CSS_PATH / f'standard-{mode}.css'}">
                    {head}
                    <link rel="stylesheet" href="../_static/css/components.css">
                    <div class="jinja-example-content">
                        {rendered}
                    </div>
                </template>
            """
            rendered_node = nodes.raw('', rendered_block, format='html')
            rendered_node['classes'].extend(['jinja-render-block', f'theme-{mode}'])
            if index > 0:
                container += nodes.raw('', '<hr>', format='html')
            container += rendered_node

    @staticmethod
    def _docs_css_path(path: Path) -> Path:
        return DOCS_COMPONENTS_CSS_PATH / path.relative_to(components.COMPONENTS_CSS_PATH)

    @staticmethod
    def _docs_js_path(path: Path) -> Path:
        relative_path = path.relative_to(components.COMPONENTS_JS_PATH).with_suffix('.js')
        return DOCS_COMPONENTS_JS_PATH / relative_path

    def run(self) -> list[nodes.Element]:
        if not (source_path := self.state.document.current_source):
            raise RuntimeError('Source path cannot be derived')

        css_module = self.block_text.splitlines()[0].partition('::')[2].strip()
        template_content = '\n'.join(self.content if not css_module else self.content[2:])
        module = Path(source_path).stem.split('.')[0]
        if source_path.endswith('.html.j'):
            source_path = '/'.join(source_path.split('/')[2:])
            template = f'{{% import \'{source_path}\' as {module} %}}\n{template_content}'
        else:
            template = template_content

        # Rendering source
        env = self.get_environment(
            loader=ChoiceLoader([
                DictLoader({'main': template}),
                FileSystemLoader('django_logikal/templates/'),
            ]),
        )
        rendered = env.get_template('main').render()
        self._validate(content=rendered, source_path=source_path)
        rendered_nice = format_html(rendered, source_file=source_path)

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
            '    .. code-block:: html+jinja',
            '',
            *[f'      {line}' for line in template_content.splitlines()],
            '',
            '  .. tab-item:: HTML',
            '    :sync: html',
            '',
            '    .. code-block:: html',
            '',
            *[f'      {line}' for line in rendered_nice.splitlines()],
        ]
        self.parse_rst_blocks(blocks=blocks, source=source_path, node=container)

        # Rendering HTML
        component_files = components.component_head_files((css_module or module or 'commons',))
        component_head = '\n'.join(
            f'<link rel="stylesheet" href="{self._docs_css_path(file)}">'
            for file in component_files['css']
        )
        if component_files['js']:
            on_load = 'window.initializeJinjaExample(this.getRootNode())'
            component_head += '\n' + '\n'.join(
                f'<script defer src="{self._docs_js_path(file)}" onload="{on_load}"></script>'
                for file in component_files['js']
            )
        self._render_html(
            head=component_head,
            rendered=rendered,
            container=container,
            scheme=self.options.get('scheme'),
        )
        return [container]
