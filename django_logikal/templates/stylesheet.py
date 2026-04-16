from functools import cache
from pathlib import Path

import tinycss2
from logikal_utils.operators import unique

STATIC_PATH = Path(__file__).parents[1] / 'static'
COMPONENTS_CSS_PATH = Path('django_logikal/css')


@cache
def _style_dependencies(file: Path) -> set[str]:
    dependencies = set()
    for rule in tinycss2.parse_stylesheet(file.read_text(encoding='utf-8')):
        if rule.type == 'at-rule' and rule.lower_at_keyword == 'import':
            for token in rule.prelude:
                if token.type == 'function':
                    dependencies.add(Path(token.arguments[0].value).stem)
    return dependencies


@cache
def _component_style_dependencies() -> dict[str, list[str]]:
    module_files = {
        file.stem: COMPONENTS_CSS_PATH / file.name
        for file in (STATIC_PATH / COMPONENTS_CSS_PATH).glob('*.css')
    }
    dependencies = {
        module: _style_dependencies(STATIC_PATH / file)
        for module, file in module_files.items()
    }

    def get_dependencies(module: str) -> list[str]:
        resolved: list[str] = []
        visited: set[str] = set()
        visiting: set[str] = set()

        def walk_dependencies(target_module: str) -> None:
            if target_module in visiting:
                raise ValueError(  # pragma: no cover, defensive line
                    f'Circular dependency for "{target_module}"'
                    f' when resolving component module "{module}"'
                )
            if target_module in visited:
                return  # pragma: no cover, also defensive line

            visiting.add(target_module)
            for dependency in dependencies[target_module]:
                walk_dependencies(dependency)

            visiting.remove(target_module)
            visited.add(target_module)
            resolved.append(target_module)

        walk_dependencies(module)
        return resolved

    return {
        module: [str(module_files[dependency]) for dependency in get_dependencies(module)]
        for module in module_files
    }


@cache
def component_style_files(modules: list[str]) -> list[Path]:
    dependencies = _component_style_dependencies()
    for module in modules:
        if module not in dependencies:
            raise ValueError(f'Invalid module "{module}"')
    return list(unique(
        Path(dependency)
        for module in modules
        for dependency in dependencies[module]
    ))
