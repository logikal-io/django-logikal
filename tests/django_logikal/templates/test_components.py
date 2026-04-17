from pytest import raises

from django_logikal.templates.components import component_head_files


def test_component_head_files_error() -> None:
    with raises(ValueError, match='Invalid module'):
        component_head_files('non-existent')
