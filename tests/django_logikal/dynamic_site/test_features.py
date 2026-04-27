import re
from pathlib import Path

from anymail.message import AnymailMessage
from django.template.loader import get_template
from django.test import Client
from django.urls import reverse
from pytest import mark
from pytest_django.live_server_helper import LiveServer
from pytest_logikal import Browser, LiveURL, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import factories, scenarios
from tests.django_logikal.conftest import app_url
from tests.dynamic_site import local_data
from tests.dynamic_site.models import User


@mark.django_db
def test_local_data() -> None:
    local_data.UserData.insert()
    assert User.objects.filter(username='user').exists()


def test_home_head(live_server: LiveServer, client: Client) -> None:
    response = client.get(live_server.url)
    source = response.content.decode()
    description = 'This is a dynamic site used for demonstration and testing purposes.'
    assert f'<meta name="description" content="{description}">' in source
    assert '<title>Home Page | Logikal</title>' in source

    # Content security policy
    assert "default-src 'self' 'nonce-" in response.headers['Content-Security-Policy']
    assert re.search('<script nonce="[^"]+">[\\s]+let test = 42;[\\s]+</script>', source)


@set_browser(scenarios.desktop)
def test_home(live_server: LiveServer, browser: Browser) -> None:
    browser.get(live_server.url)
    browser.check()


@set_browser(scenarios.desktop_all_languages)
def test_localization(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('dynamic_site_localized:localization'))
    browser.check()


@set_browser(scenarios.desktop)
def test_templates(live_app_url: LiveURL, browser: Browser) -> None:
    browser.get(live_app_url('templates', kwargs={'arg': 'test-arg'}) + '?next=/internal/')
    browser.check()


def test_internal(live_app_url: LiveURL, client: Client) -> None:
    response = client.get(live_app_url('internal'))
    assert response.status_code == 302
    assert response.url == f'{reverse("admin:login")}?next={app_url("internal")}'  # type: ignore


@set_browser(scenarios.desktop)
def test_invalid_html(live_app_url: LiveURL, browser: Browser, client: Client) -> None:
    response = client.get(live_app_url('invalid-html'))
    source = response.content.decode()
    assert response.status_code == 500
    assert 'HTML Validation Error' in source
    assert '<b class="error">Error:</b> Element “h” not allowed' in source
    assert '<b class="error">Error:</b> Unclosed element “h”' in source
    browser.get(live_app_url('invalid-html'))
    browser.check()


@set_browser(scenarios.desktop)
def test_models(live_app_url: LiveURL, browser: Browser) -> None:
    local_data.ProjectData.insert()
    browser.get(live_app_url('models'))
    browser.check()


def test_redirect(live_app_url: LiveURL, client: Client) -> None:
    args = '?key=value'
    response = client.get(live_app_url('redirect') + args)
    assert response.status_code == 302
    assert response.url == app_url('home') + args  # type: ignore[attr-defined]


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


@set_browser(scenarios.desktop)
def test_partials(
    live_app_url: LiveURL,
    browser: Browser,
) -> None:
    browser.get(live_app_url('partials'))
    browser.check('initial')
    button = browser.find_element(By.TAG_NAME, 'button')
    button.click()
    browser.check('updated')
