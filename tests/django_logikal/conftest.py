from collections.abc import Callable
from logging import getLogger

from django.urls import reverse
from pytest import fixture
from pytest_logikal.django import LiveURL

from tests.dynamic_site.urls import app_name

logger = getLogger(__name__)


def app_url(name: str) -> str:
    return reverse(f'{app_name}:{name}')


@fixture
def live_app_url(live_url: LiveURL) -> Callable[[str], str]:
    def live_app_url_path(name: str) -> str:
        return live_url(name=f'{app_name}:{name}')
    return live_app_url_path
