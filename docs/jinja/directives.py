import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache, partial
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import tinycss2
from docutils import nodes
from docutils.statemachine import StringList
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader, nodes as jinja_nodes
from pytest_logikal.validator import Validator
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.ext.napoleon.docstring import GoogleDocstring
from sphinx.util.docutils import SphinxDirective

from django_logikal.templates import functions, jinja, stylesheet
from docs.jinja.format import format_html

COMPONENTS_CSS_STATIC_PATH = Path('django_logikal/static') / stylesheet.COMPONENTS_CSS_PATH

DOCS_STATIC_ROOT = Path(__file__).parents[1] / 'build/_static'
DOCS_COMPONENTS_CSS_PATH = Path('../_static') / stylesheet.COMPONENTS_CSS_PATH
DOCS_THEMES_CSS_PATH = DOCS_COMPONENTS_CSS_PATH / 'themes'

THEME_MODES = ['light', 'dark']


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
            rst += f' Defaults to ``{re.sub(' +', ' ', self.value)}``.'
        return rst


@cache
def parsed_stylesheet(path: Path) -> Any:
    contents = (Path(__file__).parents[2] / path).read_text(encoding='utf-8')
    return tinycss2.parse_stylesheet(contents, skip_comments=False, skip_whitespace=True)


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
        request = SimpleNamespace(resolver_match=SimpleNamespace(view_name='main:components'))
        env = jinja.environment(**kwargs, **jinja.DEFAULT_OPTIONS)
        env.globals.update({
            'request': request,
            'static': self._static,
            'include_static': partial(
                functions.include_static,
                static_path_function=self._include_static_path,
            ),
            'url': self._url,
        })
        env.install_gettext_callables(  # type: ignore[attr-defined] # pylint: disable=no-member
            gettext=lambda text: text,
            ngettext=lambda text: text,
            newstyle=True,
            pgettext=lambda text: text,
            npgettext=lambda text: text,
        )
        return env

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
                or selector not in tinycss2.serialize(rule.prelude).strip()
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
                    if not value.startswith('_'):
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


class JinjaAutoCSSVariablesDirective(JinjaSphinxDirective):
    has_content = True
    required_arguments = 2

    def run(self) -> list[nodes.Node]:
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
        component_styles = f'{{{{ component_styles(\'{module}\') }}}}'
        blocks = [
            '  **Usage:**',
            '',
            '  .. code-block:: jinja',
            '',
            f'    {{% import \'{self._import_path(source_path)}\' as {module} %}}',
            f'    {{% block component_styles %}}{component_styles}{{% endblock %}}',
            '',
            '  **Components:**',
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

        node = cast(addnodes.desc, parent_nodes[1])
        node += self.parse_rst_blocks(blocks=blocks, source=source_path_str)
        return parent_nodes


class JinjaExampleDirective(JinjaSphinxDirective):
    has_content = True

    @staticmethod
    def _validate(content: str, source_path: str) -> None:
        if errors := Validator().errors(content=f"""
            <!DOCTYPE html>
            <html lang="en-us">
              <head>
                <meta charset="utf-8">
                <title>Example</title>
              </head>
              <body>{content}</body>
            </html>
        """):
            error_str = '\n'.join(error.message for error in errors)
            raise RuntimeError(f'Validation errors on "{source_path}":\n{error_str}')

    @staticmethod
    def _render_html(styles: str, rendered: str, container: nodes.Element) -> None:
        for index, mode in enumerate(THEME_MODES):
            rendered_block = f"""
                <template shadowrootmode="open">
                    <link rel="stylesheet" href="{DOCS_THEMES_CSS_PATH / f'standard-{mode}.css'}">
                    {styles}
                    {rendered}
                </template>
            """
            rendered_node = nodes.raw('', rendered_block, format='html')
            rendered_node['classes'].extend(['jinja-render-block', f'theme-{mode}'])
            if index > 0:
                container += nodes.raw('', '<hr>', format='html')
            container += rendered_node

    def run(self) -> list[nodes.Element]:
        if not (source_path := self.state.document.current_source):
            raise RuntimeError('Source path cannot be derived')

        css_module = self.block_text.splitlines()[0].partition('::')[2].strip()
        template_content = '\n'.join(self.content if not css_module else self.content[2:])
        if source_path.endswith('.html.j'):
            source_path = '/'.join(source_path.split('/')[2:])
            module = Path(source_path).stem.split('.')[0]
            template = f'{{% import \'{source_path}\' as {module} %}}\n{template_content}'
        else:
            module = None
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
            '    .. code-block:: jinja',
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
        component_styles = '\n'.join(
            f'<link rel="stylesheet" href="{DOCS_COMPONENTS_CSS_PATH / file.name}">'
            for file in stylesheet.component_style_files((css_module or module or 'commons',))
        )
        self._render_html(styles=component_styles, rendered=rendered, container=container)
        return [container]
