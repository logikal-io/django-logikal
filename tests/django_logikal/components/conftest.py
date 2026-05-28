import subprocess
from collections.abc import Iterator
from logging import getLogger
from pathlib import Path

from pytest import FixtureRequest, fixture

from docs.jinja.directives import THEME_MODES

logger = getLogger(__name__)


@fixture(scope='session', autouse=True)
def build_docs() -> None:  # pragma: no cover, does not always run
    if Path('docs/build/').exists():
        logger.info('Skipping documentation building (the "docs/build/" folder already exists)')
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
