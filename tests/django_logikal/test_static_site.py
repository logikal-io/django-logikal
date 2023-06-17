import os
import re
from pathlib import Path
from subprocess import run

from pytest import mark
from pytest_logikal.browser import Browser

from django_logikal.settings.static_site import DISTILL_DIR


@mark.django_db
def test_generate(tmp_path: Path, browser: Browser) -> None:
    output_path = tmp_path / DISTILL_DIR.name
    static_path = output_path / 'static'
    settings = 'tests.static_site.settings.local'
    command = ['manage', 'migrate', '--settings', settings]
    run(command, check=True)  # nosec: trusted input in testing
    command = ['manage', 'generate', '--no-input', '--settings', settings, str(output_path)]
    run(command, check=True)  # nosec: trusted input in testing

    # Make static paths relative
    for path in output_path.rglob('*.html'):
        replacement = os.path.relpath(static_path, path.parent)
        path.write_text(re.sub('/static/', f'{replacement}/', path.read_text()))

    browser.get(f'file://{output_path}/index.html')
    browser.check('index')
    browser.get(f'file://{output_path}/test/index.html')
    browser.check('test')
    browser.get(f'file://{output_path}/en-us/localization/index.html')
    browser.check('localization-en-us')
    # Note: other languages aren't generated currently
    # (see https://github.com/meeb/django-distill/issues/80)
    # browser.get(f'file://{output_path}/en-gb/localisation/index.html')
    # browser.check('localization-en-gb')
    robots = (output_path / 'robots.txt').read_text()
    assert 'User-agent: *\n' in robots
    assert '\nDisallow:\n' in robots
    sitemap = (output_path / 'sitemap.xml').read_text()
    assert '<loc>http://logikal.io/</loc><priority>1</priority>' in sitemap
    assert '<loc>http://logikal.io/en-us/localization/</loc><priority>0.5</priority>' in sitemap
    assert '<loc>http://logikal.io/en-gb/localisation/</loc><priority>0.5</priority>' in sitemap
