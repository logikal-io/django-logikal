from django.shortcuts import render
from pytest import raises


def test_invalid_block() -> None:
    with raises(RuntimeError, match='Block .* not found'):
        render(request=None, template_name='dynamic_site/home.html.j#non-existent-block')
