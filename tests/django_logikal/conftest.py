from logging import getLogger
from subprocess import PIPE
from time import sleep
from typing import Iterator

from django.urls import reverse
from psutil import CONN_LISTEN, Popen
from pytest import fixture
from pytest_logikal.django import LiveURL

from tests.dynamic_site.urls import app_name

logger = getLogger(__name__)


def app_url(name: str) -> str:
    return reverse(f'{app_name}:{name}')


@fixture
def live_app_url(live_url: LiveURL) -> LiveURL:
    def live_app_url_path(name: str) -> str:
        return live_url(f'{app_name}:{name}')
    return live_app_url_path


@fixture
def live_server_subprocess() -> Iterator[str]:
    logger.info('Creating development server subprocess')
    with Popen(['run', '--noreload', '-t', '127.0.0.1:0'], text=True, stdout=PIPE) as process:
        for line in process.stdout:
            print(line.strip())
            if 'Quit the server' in line:
                break

        # Note: this can be removed once https://code.djangoproject.com/ticket/32813 is released
        # (make sure to also remove psutil as a dependency)
        sleep(1)
        logger.info('Retrieving subprocess connections')
        address = [
            connection for connection in process.connections()
            if connection.status == CONN_LISTEN
        ][0].laddr
        url = f'http://{address.ip}:{address.port}'

        logger.info(f'Using live server URL {url}')
        yield url
        logger.info(f'Terminating process {process}')
        process.terminate()

    logger.info('Teardown complete')
