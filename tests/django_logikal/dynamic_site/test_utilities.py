import re
from pathlib import Path

import robots
from anymail.message import AnymailMessage
from django.template.loader import get_template
from django.test import Client
from pytest_factoryboy import register
from pytest_logikal import Browser, LiveURL, set_browser

from django_logikal.views.generic import ERROR_HANDLERS
from tests.django_logikal import factories, scenarios
from tests.django_logikal.conftest import app_url
from tests.dynamic_site.models import User

register(factories.RobotsUrlFactory, _name='robots_url')
register(factories.RobotsRuleFactory, _name='robots_rule')


@set_browser(scenarios.desktop)
def test_error_pages(live_url: LiveURL, client: Client, browser: Browser) -> None:
    response_error_codes = {400: 500, 403: 404, 404: 404, 500: 500}
    for code in ERROR_HANDLERS:
        url = live_url(f'error:{code}')
        response = client.get(url)
        assert response.status_code == response_error_codes[code]
        browser.get(url)
        browser.check(str(code))


@set_browser(scenarios.desktop)
def test_admin(
    live_url: LiveURL, browser: Browser, user: User, admin_user: User, super_user: User,
) -> None:
    browser.get(live_url('admin:index'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_url('admin:index'))
    browser.check('no_permission')

    browser.login(admin_user)
    browser.get(live_url('admin:index'))
    browser.check('admin_user_after_login')

    browser.login(super_user)
    browser.get(live_url('admin:index'))
    browser.check('super_user_after_login')


def test_email(
    live_app_url: LiveURL,
    client: Client,
    mailoutbox: list[AnymailMessage],
) -> None:
    factories.site_factory()
    response = client.get(live_app_url('email'))
    source = response.content.decode()
    assert 'Email successfully sent' in source
    assert len(mailoutbox) == 1
    email = mailoutbox[0]
    html = email.alternatives[0][0]

    # Check metadata
    assert email.subject == '[Dynamic Site] Test Email Subject'

    # Check plain text version
    expected_file = 'dynamic_site/email/test_email.md'
    expected_path = Path(get_template(expected_file).origin.name)  # type: ignore[attr-defined]
    assert re.sub('cid:[0-9.]+', 'cid:1.', email.body) == expected_path.read_text(encoding='utf-8')

    # Check html version
    assert '<title>Test Email Subject</title>' in html
    assert '<body leftmargin="0" topmargin="0"' in html
    assert '<p style=\'font-family:"Roboto",' in html
    assert re.search(r'<img .* src="cid:.*\.img@inline"', html)

    # Check attachments
    assert email.attachments[1] == ('inline_attachment.txt', 'Inline Attachment', 'text/plain')
    assert email.attachments[2] == ('attachment.txt', 'Attachment\n', 'text/plain')


def test_redirect(live_app_url: LiveURL, client: Client) -> None:
    args = '?key=value'
    response = client.get(live_app_url('redirect') + args)
    assert response.status_code == 302
    assert response.url == app_url('home') + args  # type: ignore[attr-defined]


def test_sitemap(live_url: LiveURL, client: Client) -> None:
    factories.site_factory()
    response = client.get(live_url('sitemap'))
    source = response.content.decode()
    assert '<loc>http://logikal.io/</loc><priority>1</priority>' in source
    assert '<loc>http://logikal.io/rendering/models/</loc><priority>0.75</priority>' in source
    assert '<loc>http://logikal.io/en-us/localization/</loc><priority>0.5</priority>' in source
    assert (
        '<loc>http://logikal.io/en-gb/localisation/'  # codespell:ignore localisation
        '</loc><priority>0.5</priority>'
        in source
    )
    assert 'internal/' not in source


def test_robots(
    live_url: LiveURL,
    client: Client,
    robots_url_factory: robots.models.Url,
    robots_rule_factory: robots.models.Rule,
) -> None:
    site = factories.site_factory()

    # Clear existing data from migrations
    robots.models.Url.objects.all().delete()
    robots.models.Rule.objects.all().delete()

    # Add new data
    robots_rule_factory(
        id=1,
        disallowed=[robots_url_factory(id=1, pattern='/disallowed/')],
        sites=[site],
    )

    # Check robots.txt
    response = client.get(live_url('robots'))
    source = response.content.decode()
    assert 'User-agent: *\n' in source
    assert '\nDisallow: /disallowed/\n' in source
    assert '\nHost: logikal.io\n' in source
    assert '\nSitemap: http://logikal.io/sitemap.xml\n' in source
