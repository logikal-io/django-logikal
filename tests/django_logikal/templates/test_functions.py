from datetime import UTC, datetime
from pathlib import Path

from django.test import RequestFactory
from django.urls import ResolverMatch
from django.urls.exceptions import NoReverseMatch
from pytest import raises
from pytest_mock import MockerFixture
from time_machine import Traveller

from django_logikal.templates import functions as f


def test_static() -> None:
    assert f.static('favicon.png') == '/static/favicon.png'


def test_static_path_error() -> None:
    with raises(RuntimeError, match='not found'):
        f.static_path('non-existent')


def test_include_static() -> None:
    assert f.include_static('logikal_logo.svg').startswith('<svg')
    assert f.include_static('logikal_logo_xml.svg').startswith('<svg')


def test_url(rf: RequestFactory) -> None:
    name = 'dynamic_site:index'
    params = '?next=test'
    request = rf.get(f'/{params}')
    update_params = {'key': 'value'}

    assert f.url(name) == '/'
    assert f.url(name, request=request) == f'/{params}'
    assert f.url(name, request=request, request_get_update=update_params) == f'/{params}&key=value'
    with raises(NoReverseMatch):
        assert f.url('non-existent')


def test_url_name(rf: RequestFactory) -> None:
    request = rf.get('/')
    with raises(RuntimeError, match='URL resolving has not taken place'):
        f.url_name(request)

    request.resolver_match = ResolverMatch(
        func=lambda _: _, args=tuple(), kwargs={},
        app_names=['dynamic_site'], url_name='index',
    )
    assert f.url_name(request) == 'dynamic_site:index'


def test_language() -> None:
    assert f.language() == 'en-us'


def test_cwd(mocker: MockerFixture) -> None:
    cwd = '/test_dir'
    mocker.patch('django_logikal.templates.functions.os.getcwd', return_value=cwd)
    assert f.cwd() == Path(cwd)


def test_now(time_machine: Traveller) -> None:
    timestamp = datetime(2023, 3, 20, tzinfo=UTC)
    time_machine.move_to(timestamp)
    assert f.now() == timestamp


def test_bibliography() -> None:
    bib = f.bibliography('references')
    with raises(RuntimeError, match='Reference .* not found'):
        bib.cite('unknown')
    assert 'cite-django-logikal' in bib.cite('django-logikal')
    with raises(RuntimeError, match='Reference .* already been used'):
        bib.cite('django-logikal')
