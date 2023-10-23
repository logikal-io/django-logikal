import re
from logging import getLogger
from subprocess import PIPE, run
from typing import Iterator, Optional

from django.urls import reverse
from psutil import Popen
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
def live_server_subprocess() -> Iterator[Optional[str]]:
    logger.info('Creating development server subprocess')
    command = [
        'run', '--noreload', '--settings', 'tests.dynamic_site.settings.dev', '-t', '127.0.0.1:0',
    ]
    with Popen(command, text=True, stdout=PIPE) as process:
        url = None

        for line in process.stdout:
            if 'Quit the server' in line:
                break
            if match := re.search('development server at (?P<url>http://[^/]+)/', line):
                url = match.group('url')

        logger.info(f'Using live server URL {url}')
        run(['manage', 'syncdb', '--no-input'], check=True)  # nosec: trusted input in testing
        yield url
        logger.info(f'Terminating process {process}')
        process.terminate()

    logger.info('Teardown complete')
