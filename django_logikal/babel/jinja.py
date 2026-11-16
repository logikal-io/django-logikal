from collections import defaultdict
from collections.abc import Iterator, Sequence
from functools import cache
from importlib.util import find_spec
from pathlib import Path
from typing import Any, BinaryIO

from jinja2 import nodes
from jinja2.ext import babel_extract
from termcolor import colored

from django_logikal.templates.jinja import DEFAULT_OPTIONS, environment


@cache
def load_template(path: Path) -> Any:
    env = environment(**DEFAULT_OPTIONS)
    return env.parse(path.read_text(encoding='utf-8'))


def get_macro_file_names(template: nodes.Template) -> defaultdict[str, set[str]]:
    macro_module_files = {}
    macro_file_names = defaultdict(set)
    macro_alias_names = {}
    macro_alias_module_files = defaultdict(set)
    for node in template.find_all((nodes.Import, nodes.FromImport, nodes.Call)):
        # Processing imports
        if isinstance(node, nodes.Import):
            macro_module_files[node.target] = node.template.value  # type: ignore[attr-defined]
        elif isinstance(node, nodes.FromImport):
            for name in node.names:
                macro_name, macro_alias = (name, name) if isinstance(name, str) else name
                macro_alias_names[macro_alias] = macro_name
                macro_alias_module_files[macro_name] = (
                    node.template.value  # type: ignore[attr-defined]
                )

        # Processing calls
        elif isinstance(node, nodes.Call):
            call_target = node.node

            # Direct calls
            if hasattr(call_target, 'name') and call_target.name in macro_alias_names:
                macro_name = macro_alias_names[call_target.name]  # resolve to real macro name
                macro_module_file = macro_alias_module_files[macro_name]  # find module file
                macro_name_line = f'{macro_name}:{node.lineno}'
                macro_file_names[macro_module_file].add(macro_name_line)  # add real macro name
            # Scoped calls
            elif (
                hasattr(call_target, 'attr')
                and hasattr(call_target, 'node')
                and hasattr(call_target.node, 'name')
                and call_target.node.name in macro_module_files
            ):
                macro_file = macro_module_files[call_target.node.name]
                macro_file_names[macro_file].add(f'{call_target.attr}:{node.lineno}')

    return macro_file_names


def template_path(file: str) -> Path | None:
    module_name = file.split('/')[0]
    module = find_spec(module_name)
    if not module or not module.submodule_search_locations:
        warning = colored('WARNING:', color='red', attrs=['bold'])
        print(f'{warning} macro module "{module_name}" for file "{file}" not found')
        return None

    return Path(module.submodule_search_locations[0]) / 'templates' / file


def get_macro_caller_lines(macros: set[str]) -> dict[str, list[int]]:
    macro_caller_lines: dict[str, list[int]] = defaultdict(list)
    for macro in macros:
        macro_name, line_number_str = macro.split(':')
        macro_caller_lines[macro_name].append(int(line_number_str))
    return macro_caller_lines


def get_macro_to_caller_lines(macro_file_path: Path, macros: set[str]) -> dict[int, set[int]]:
    macro_template = load_template(macro_file_path)
    macro_caller_lines = get_macro_caller_lines(macros)
    macro_to_caller_lines: dict[int, set[int]] = defaultdict(set)
    for macro in macro_template.find_all(nodes.Macro):
        if macro.name not in macro_caller_lines:
            continue
        for child in macro.find_all(nodes.Call):
            macro_to_caller_lines[child.lineno].update(macro_caller_lines[macro.name])
    return macro_to_caller_lines


def babel_extract_extended(
    fileobj: BinaryIO,
    keywords: Sequence[str],
    comment_tags: Sequence[str],
    options: dict[str, Any],
) -> Iterator[tuple[int, str, str | None | tuple[str | None, ...], list[str]]]:
    # Load template messages
    fileobj.seek(0)
    yield from babel_extract(
        fileobj=fileobj,
        keywords=keywords,
        comment_tags=comment_tags,
        options=options,
    )

    # Load imported macros
    fileobj.seek(0)
    env = environment(**DEFAULT_OPTIONS)
    template = env.parse(fileobj.read().decode('utf-8'))
    macro_file_names = get_macro_file_names(template=template)

    # Load messages from imported macros
    for macro_file_name, macros in macro_file_names.items():
        if not (macro_file_path := template_path(macro_file_name)):
            continue

        print(f'extracting macro messages from {macro_file_name}')
        # Note: `macros` contains the `macro name:caller line number` pairs,
        # so we need to map the extracted macro line numbers back to the caller line number
        macro_to_caller_lines = get_macro_to_caller_lines(
            macro_file_path=macro_file_path, macros=macros,
        )
        with macro_file_path.open('rb') as macro_template_file:
            for message in babel_extract(
                fileobj=macro_template_file,
                keywords=keywords,
                comment_tags=comment_tags,
                options=options,
            ):
                for caller_line_number in sorted(macro_to_caller_lines.get(message[0], ())):
                    yield (caller_line_number, *message[1:])
