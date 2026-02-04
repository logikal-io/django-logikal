import os
import re
from collections.abc import Callable, Iterator
from logging import getLogger
from subprocess import PIPE, STDOUT, Popen, run

from django.urls import reverse
from pytest import fixture
from pytest_logikal import LiveURL

from tests.dynamic_site.urls import app_name as dynamic_site_app_name

logger = getLogger(__name__)


def app_name(name: str) -> str:
    return f'{dynamic_site_app_name}:{name}'


def app_url(name: str) -> str:
    return reverse(app_name(name))


@fixture
def live_app_url(live_url: LiveURL) -> Callable[[str], str]:
    def live_app_url_path(name: str) -> str:
        return live_url(name=app_name(name))
    return live_app_url_path


@fixture
def live_server_with_toolbar() -> Iterator[str]:
    logger.info('Running migrations')
    run(['manage', 'syncdb', '--no-input'], check=True)  # nosec: trusted input in testing

    logger.info('Creating development server subprocess')
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    command = [
        'run', '--noreload', '--settings', 'tests.dynamic_site.settings.dev',
        '--toolbar', '127.0.0.1:0',
    ]
    with Popen(  # nosec: trusted input in testing
        command, bufsize=1, text=True,
        stdout=PIPE, stderr=STDOUT, env=env,
    ) as process:
        try:
            url = None
            for line in process.stdout:  # type: ignore[union-attr]
                print(line, end='')
                if 'Quit the server' in line:
                    break
                if match := re.search('development server at (?P<url>http://[^/]+)/', line):
                    url = match.group('url')
            logger.info(f'Using development server URL {url}')
            if not url:  # pragma: no cover
                raise RuntimeError('Cannot start development server')
            yield url
        finally:
            logger.info(f'Terminating process {process}')
            process.terminate()

    logger.info('Teardown complete')


@fixture
def live_app_url_with_toolbar(
    live_server_with_toolbar: str,  # pylint: disable=redefined-outer-name
) -> Callable[[str], str]:
    def live_app_url_with_toolbar_path(name: str) -> str:
        return f'{live_server_with_toolbar}/{app_url(name)}'
    return live_app_url_with_toolbar_path
