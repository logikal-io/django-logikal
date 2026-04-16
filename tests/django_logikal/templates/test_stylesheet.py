from pytest import raises

from django_logikal.templates.stylesheet import component_style_files


def test_component_style_files_error() -> None:
    with raises(ValueError, match='Invalid module'):
        component_style_files('non-existent')
