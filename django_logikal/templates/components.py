from functools import cache
from pathlib import Path

from logikal_utils.operators import unique

STATIC_PATH = Path(__file__).parents[1] / 'static'
COMPONENTS_CSS_PATH = Path('django_logikal/css')
COMPONENTS_JS_PATH = Path('django_logikal/js')

COMPONENT_DEPENDENCIES: dict[str, list[str]] = {
    'variables': [],
    'baseline': [],
    'fonts': [],
    'commons': ['variables', 'baseline'],
    'composition': ['commons'],
    'text': ['commons'],
    'forms': ['commons'],
    'auth': ['forms'],
    'validation': ['fonts', 'composition', 'text'],
}


@cache
def _component_style_dependencies() -> dict[str, list[str]]:
    module_files = {
        module: COMPONENTS_CSS_PATH / f'{module}.css'
        for module in COMPONENT_DEPENDENCIES
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
            for dependency in COMPONENT_DEPENDENCIES[target_module]:
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
def component_head_files(modules: list[str]) -> dict[str, list[Path]]:
    dependencies = _component_style_dependencies()
    for module in modules:
        if module not in dependencies:
            raise ValueError(f'Invalid module "{module}"')

    css_paths = list(unique(
        Path(dependency)
        for module in modules
        for dependency in dependencies[module]
    ))

    js_paths = []
    for path in css_paths:
        js_path = COMPONENTS_JS_PATH / path.relative_to(COMPONENTS_CSS_PATH).with_suffix('.mjs')
        if (STATIC_PATH / js_path).exists():
            js_paths.append(js_path)

    return {'css': css_paths, 'js': js_paths}
