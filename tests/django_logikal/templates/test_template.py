from pytest import raises

from django_logikal.templates import Template


def test_template_error() -> None:
    with raises(RuntimeError, match='app name must be specified'):
        Template().include(paths=[])
