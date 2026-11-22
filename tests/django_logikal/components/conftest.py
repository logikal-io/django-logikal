import subprocess
from collections.abc import Iterator
from logging import getLogger

from filelock import FileLock
from pytest import FixtureRequest, fixture

from docs import DOCS_BUILD_COMPLETE_PATH
from docs.jinja.directives import THEME_MODES

logger = getLogger(__name__)


@fixture(scope='session', autouse=True)
def build_docs() -> None:  # pragma: no cover, does not always run
    with FileLock('docs/.build.lock'):
        if DOCS_BUILD_COMPLETE_PATH.exists():
            logger.info('Skipping documentation building (a completed build already exists)')
            return

        logger.info('Building documentation')
        process = subprocess.run(  # nosec: secure, not using untrusted input
            ['docs', '--build', '--clear'], capture_output=True, text=True, check=False,
        )
        if process.returncode:
            logger.error('Documentation building failed')
            raise RuntimeError(process.stderr or process.stdout)


@fixture(params=THEME_MODES)
def theme(request: FixtureRequest) -> Iterator[str]:
    yield request.param
