import robots
from django.test import Client
from pytest_factoryboy import register
from pytest_logikal import Browser, LiveURL, set_browser

from django_logikal.views import ERROR_HANDLERS
from tests.django_logikal import factories, scenarios
from tests.dynamic_site.models import User

register(factories.RobotsUrlFactory, _name='robots_url')
register(factories.RobotsRuleFactory, _name='robots_rule')


@set_browser(scenarios.desktop)
def test_admin(
    live_url: LiveURL, browser: Browser, user: User, staff_user: User, super_user: User,
) -> None:
    browser.get(live_url('admin:index'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_url('admin:index'))
    browser.check('no_permission')

    browser.login(staff_user)
    browser.get(live_url('admin:index'))
    browser.check('staff_user_after_login')

    browser.login(super_user)
    browser.get(live_url('admin:index'))
    browser.check('super_user_after_login')


@set_browser(scenarios.desktop)
def test_error_pages(live_url: LiveURL, client: Client, browser: Browser) -> None:
    response_error_codes = {400: 500, 403: 404, 404: 404, 500: 500}
    for code in ERROR_HANDLERS:
        url = live_url(f'error:{code}')
        response = client.get(url)
        assert response.status_code == response_error_codes[code]
        browser.get(url)
        browser.check(str(code))


def test_sitemap(live_url: LiveURL, client: Client) -> None:
    factories.site_factory()
    response = client.get(live_url('sitemap'))
    source = response.content.decode()
    assert '<loc>http://logikal.io/</loc><priority>1</priority>' in source
    assert '<loc>http://logikal.io/models/</loc><priority>0.75</priority>' in source
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
