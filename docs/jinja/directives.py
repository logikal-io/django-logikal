import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

import tinycss2
from docutils import nodes
from docutils.statemachine import StringList
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader, nodes as jinja_nodes
from jinja2.runtime import StrictUndefined
from sphinx.ext.napoleon.docstring import GoogleDocstring
from sphinx.util.docutils import SphinxDirective

STATIC_PATH = Path('django_logikal/static')
COMPONENTS_CSS_PATH = STATIC_PATH / Path('django_logikal/css/components')


@dataclass
class CSSElement(ABC):
    @abstractmethod
    def as_rst(self) -> str:
        ...


@dataclass
class CSSSectionComment(CSSElement):
    level: int
    value: str

    def as_rst(self) -> str:
        return f'.. dropdown:: {self.value}'


@dataclass
class CSSVariable(CSSElement):
    name: str
    value: str
    description: str | None = None

    def as_rst(self) -> str:
        rst = f':css:`{self.name}`'
        if self.description or self.value:
            rst += ' --'
        if self.description:
            rst += f' {self.description.capitalize()}.'
        if self.value:
            rst += f' Defaults to ``{self.value}``.'
        return rst


@cache
def parsed_stylesheet(path: Path) -> Any:
    contents = (Path(__file__).parents[2] / path).read_text(encoding='utf-8')
    return tinycss2.parse_stylesheet(contents, skip_comments=False, skip_whitespace=True)


class ExtendedSphinxDirective(ABC, SphinxDirective):
    def parse_rst_blocks(
        self,
        blocks: list[str],
        source: str,
        node: nodes.Element | None = None,
    ) -> nodes.Element:
        parsed_blocks = StringList()
        for rst_block in blocks:
            parsed_blocks.append(rst_block, source=source)

        node = node or nodes.container()
        self.state.nested_parse(block=parsed_blocks, input_offset=0, node=node)
        return node

    @staticmethod
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
                    return value  # type: ignore[no-any-return]
            return None
        return None

    def get_css_variables(
        self,
        rules: list[Any],
        selector: str,
        with_sections: bool = False,
    ) -> list[CSSElement]:
        variables: list[CSSElement] = []
        for rule in rules:
            if (
                not hasattr(rule, 'prelude')
                or tinycss2.serialize(rule.prelude).strip() != selector
            ):
                continue

            inline = False
            declarations = tinycss2.parse_declaration_list(rule.content)
            for index, declaration in enumerate(declarations):
                if isinstance(declaration, tinycss2.ast.WhitespaceToken):
                    inline = '\n' not in declaration.value
                    continue
                if with_sections and isinstance(declaration, tinycss2.ast.Comment) and not inline:
                    value = declaration.value.strip()
                    variables.append(CSSSectionComment(
                        level=len(value) - len(value.lstrip('*')),
                        value=value.strip('*').strip(),
                    ))
                    continue
                if not isinstance(declaration, tinycss2.ast.Declaration):
                    continue
                name = declaration.name.strip()
                if not name.startswith('--'):
                    continue

                variables.append(CSSVariable(
                    name=declaration.name,
                    value=tinycss2.serialize(declaration.value).strip(),
                    description=(
                        self._next_comment(declarations[index + 1:])
                        if not with_sections else None
                    ),
                ))

        return variables


class JinjaAutoCSSVariablesDirective(ExtendedSphinxDirective):
    has_content = True
    required_arguments = 2

    def run(self) -> list[nodes.Element]:
        variables = self.get_css_variables(
            rules=parsed_stylesheet(Path(self.arguments[0])),
            selector=self.arguments[1],
            with_sections=True,
        )
        blocks = []
        indent = 0
        for variable in variables:
            if isinstance(variable, CSSSectionComment):
                indent = variable.level * 2
                blocks.extend(['', indent * ' ' + variable.as_rst()])
                if variable.level > 0:
                    blocks.append((indent + 1) * ' ' + ':open:')
                blocks.append('')
            else:
                blocks.append(f'{(indent + 1) * ' '}* {variable.as_rst()}')

        return [self.parse_rst_blocks(blocks=blocks, source=self.arguments[0])]


class JinjaAutoModuleDirective(ExtendedSphinxDirective):
    has_content = True
    required_arguments = 1

    def _get_docs(self, macro: jinja_nodes.Macro, source_lines: list[str]) -> str:
        first_line = source_lines[macro.lineno]
        indent = len(first_line) - len(first_line.lstrip())
        if not first_line[indent:].startswith('{#'):
            raise RuntimeError('Invalid macro documentation')
        if first_line.endswith('#}'):
            docs = [first_line[indent + 2:].replace('#}', '').strip()]
        else:
            docs = []
            for line in source_lines[macro.lineno + 1:]:
                if line.strip() != '#}':
                    docs.append(line[indent:])
                if '#}' in line:
                    break

        docstring = GoogleDocstring(docstring=docs, config=self.env.app.config, what='function')
        return re.sub(r':type (\w+): (\w+)', r':type \1: :py:obj:`\2`', str(docstring))

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

    def run(self) -> list[nodes.Element]:  # pylint: disable=too-many-locals
        # Load template file
        source_path_str = self.arguments[0]
        source_path = Path(source_path_str)
        module = source_path.name.split('.')[0]
        module_path = '/'.join(source_path_str.split('/')[2:])
        source = source_path.read_text(encoding='utf-8')
        source_lines = source.splitlines()
        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
            extensions=['jinja2.ext.i18n'],
        )
        env.install_gettext_callables(  # type: ignore[attr-defined] # pylint: disable=no-member
            gettext=lambda text: text,
            ngettext=lambda text: text,
            newstyle=True,
            pgettext=lambda text: text,
            npgettext=lambda text: text,
        )
        template = env.parse(source)
        stylesheet_path = COMPONENTS_CSS_PATH / f'{module}.css'

        blocks = [
            f'.. jinja:module:: {module_path}',
            '',
            f'  **Style sheet:** ``{stylesheet_path.relative_to(STATIC_PATH)}``',
        ]
        for macro in template.find_all(jinja_nodes.Macro):
            # Get CSS variables
            docs = self._get_docs(macro=macro, source_lines=source_lines)
            if variables := self.get_css_variables(
                rules=parsed_stylesheet(stylesheet_path),
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

        return [self.parse_rst_blocks(blocks=blocks, source=source_path_str)]


class JinjaExampleDirective(ExtendedSphinxDirective):
    has_content = True

    def run(self) -> list[nodes.Element]:
        if not self.state.document.current_source:
            raise RuntimeError('Source module cannot be derived')
        module_path = '/'.join(self.state.document.current_source.split('/')[2:])
        module = Path(module_path).stem.split('.')[0]

        # Rendering source
        jinja_content = '\n'.join(self.content)
        main_content = f'{{% import \'{module_path}\' as {module} %}}\n{jinja_content}'
        env = Environment(
            loader=ChoiceLoader([
                DictLoader({'main': main_content}),
                FileSystemLoader('django_logikal/templates/'),
            ]),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
            extensions=['jinja2.ext.i18n'],
        )
        env.install_gettext_callables(  # type: ignore[attr-defined] # pylint: disable=no-member
            gettext=lambda text: text,
            ngettext=lambda text: text,
            newstyle=True,
            pgettext=lambda text: text,
            npgettext=lambda text: text,
        )
        rendered = env.get_template('main').render()

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
        self.parse_rst_blocks(blocks=blocks, source=module_path, node=container)

        # Rendering HTML
        rendered_node = nodes.raw('', rendered, format='html')
        rendered_node['classes'].append('render-block')
        container += rendered_node

        return [container]
