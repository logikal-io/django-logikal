import json
import re
from importlib import import_module
from pathlib import Path

import robots
from anymail.message import AnymailMessage
from django.contrib.sites.models import Site
from django.core.management.base import CommandError
from django.template.loader import get_template
from django.test import Client
from django.urls import reverse
from pytest import mark, raises
from pytest_django.live_server_helper import LiveServer
from pytest_factoryboy import register
from pytest_logikal import Browser, LiveURL, set_browser
from pytest_mock import MockerFixture
from selenium.webdriver.common.by import By

from django_logikal.local_data import LocalData, SkipInsert
from django_logikal.management.commands import syncdb, translate
from django_logikal.views import ERROR_HANDLERS
from tests.django_logikal import factories, scenarios
from tests.django_logikal.conftest import app_url
from tests.dynamic_site import local_data
from tests.dynamic_site.models import SITE, User

register(factories.UserFactory)
register(factories.StaffUserFactory, _name='staff_user')
register(factories.SuperUserFactory, _name='super_user')
register(factories.RobotsUrlFactory, _name='robots_url')
register(factories.RobotsRuleFactory, _name='robots_rule')


def site_factory() -> Site:  # Note that the site is cleared for each test by pytest-django
    return Site.objects.update_or_create(id=1, defaults=SITE)[0]


def test_dev_settings() -> None:
    secret_key = 'dev'  # nosec: only used for this test
    dev = import_module('tests.dynamic_site.settings.dev')
    assert dev.SECRET_KEY == secret_key
    assert dev.DATABASES['default']['HOST'] == '127.0.0.1'
    assert 'django_logikal.validation.ValidationMiddleware' in dev.MIDDLEWARE
    assert 'console.EmailBackend' in dev.EMAIL_BACKEND


def test_production_settings(mocker: MockerFixture) -> None:
    mocker.patch('stormware.google.auth.GCPAuth')
    cloud_logging_client = mocker.patch('django_logikal.logging.cloud_logging.Client')
    database_secrets = {
        'hostname': 'test_hostname',
        'port': 'test_port',
        'database': 'test_database',
        'username': 'test_username',
        'password': 'test_password',  # nosec: only used for testing
    }
    secret_key = 'production'  # nosec: only used for this test
    secret_manager = mocker.patch('stormware.google.secrets.SecretManager')
    secret_manager.return_value.__enter__.return_value = {
        'website-secret-key': secret_key,
        'website-database-access': json.dumps(database_secrets),
    }
    production = import_module('tests.dynamic_site.settings.production')
    assert production.SECRET_KEY == secret_key
    assert production.DATABASES['default']['HOST'] == database_secrets['hostname']
    assert cloud_logging_client.called


def test_syncdb(mocker: MockerFixture) -> None:
    class TestLocalData(LocalData):
        @staticmethod
        def insert() -> None:
            pass

    class TestSkippedLocalData(LocalData):
        @staticmethod
        def insert() -> None:
            raise SkipInsert('Test')

    connection = mocker.Mock(settings_dict={'HOST': '127.0.0.1', 'PORT': '5432', 'NAME': 'test'})
    cursor = mocker.Mock()
    connection.cursor.return_value.__enter__ = cursor
    connection.cursor.return_value.__exit__ = mocker.Mock()
    call_command = mocker.patch('django_logikal.management.commands.syncdb.call_command')

    insert = mocker.spy(TestLocalData, 'insert')
    skipped_insert = mocker.spy(TestSkippedLocalData, 'insert')
    mocker.patch(
        'django_logikal.management.commands.syncdb.inspect.getmembers',
        return_value=[('test', TestLocalData), ('test_skipped', TestSkippedLocalData)],
    )

    command = syncdb.Command(connection=connection)
    command.add_arguments(parser=mocker.Mock())
    command.handle(no_input=True)

    assert cursor.called
    assert call_command.called
    assert insert.called
    assert skipped_insert.called


def test_syncdb_cancelled(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.management.commands.syncdb.input', return_value='no')
    with raises(CommandError, match='Cancelled'):
        syncdb.Command().handle()


def test_syncdb_disallowed_error(mocker: MockerFixture) -> None:
    connections = mocker.patch('django_logikal.management.commands.syncdb.connections')
    connections.__getitem__.return_value.settings_dict = {'HOST': 'disallowed'}
    with raises(CommandError, match='Disallowed database'):
        syncdb.Command().handle()


def test_translate(tmp_path: Path) -> None:
    command = translate.Command()
    common_args = ['manage', 'translate', '--output', str(tmp_path)]
    locale_path = tmp_path / 'locale'

    # Init
    command.run_from_argv([*common_args, '--init', '--locale', 'en_GB'])
    pot_file = (locale_path / 'django.pot').read_text()
    assert 'Project-Id-Version: dynamic-site' in pot_file
    assert 'msgid "Localization"\nmsgstr ""' in pot_file

    # Update
    command.run_from_argv([*common_args, '--update'])
    locale_path_en_gb = locale_path / 'en_GB/LC_MESSAGES'
    po_file = (locale_path_en_gb / 'django.po').read_text()
    assert 'Project-Id-Version: dynamic-site' in po_file
    assert 'msgid "Localization"\nmsgstr ""' in po_file
    assert re.search('PO-Revision-Date: [0-9]{4}-[0-9]{2}-[0-9]{2}', po_file)

    # Compile
    command.run_from_argv([*common_args, '--compile'])
    assert (locale_path_en_gb / 'django.mo').exists()


def test_translate_missing_app(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.management.commands.translate.tool_config', return_value={})
    with raises(CommandError, match='app name must be provided'):
        translate.Command().handle()


def test_translate_missing_action() -> None:
    with raises(CommandError, match='action must be provided'):
        translate.Command().handle()


def test_translate_init_overwrite(tmp_path: Path, mocker: MockerFixture) -> None:
    command = translate.Command()

    locale_path = tmp_path / 'locale/en_GB/LC_MESSAGES'
    locale_path.mkdir(parents=True)
    (locale_path / 'django.po').touch()
    (locale_path / 'djangojs.po').touch()

    input_obj = mocker.patch('django_logikal.management.commands.translate.input')
    input_obj.return_value = 'yes'
    command.handle(init=True, locale='en_GB', output=tmp_path, app=['admin', 'dynamic_site'])
    assert 'Project-Id-Version: dynamic-site' in (locale_path / 'django.po').read_text()

    input_obj.return_value = 'no'
    with raises(CommandError, match='Cancelled'):
        command.handle(init=True, locale='en_GB', output=tmp_path)


def test_translate_init_missing_locale() -> None:
    with raises(CommandError, match='locale must be provided'):
        translate.Command().handle(init=True)


@mark.django_db
def test_local_data() -> None:
    local_data.UserData.insert()
    assert User.objects.filter(username='user').exists()


def test_index_head(live_server: LiveServer, client: Client) -> None:
    response = client.get(live_server.url)
    source = response.content.decode()
    description = 'This is a dynamic site used for demonstration and testing purposes.'
    assert f'<meta name="description" content="{description}">' in source
    assert '<title>Index Page | Logikal</title>' in source

    # Content security policy
    assert "default-src 'self' 'nonce-" in response.headers['Content-Security-Policy']
    assert re.search('<script nonce="[^"]+">[\\s]+let test = 42;[\\s]+</script>', source)


@set_browser(scenarios.desktop)
def test_index(live_server: LiveServer, browser: Browser) -> None:
    browser.get(live_server.url)
    browser.check()


@set_browser(scenarios.desktop_all_languages)
def test_localization(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('dynamic_site_localized:localization'))
    browser.check()


@set_browser(scenarios.desktop)
def test_jinja(live_app_url: LiveURL, browser: Browser) -> None:
    browser.get(live_app_url('jinja') + '?next=/internal/')
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
    assert '<b>Error:</b> Element “h” not allowed' in source
    assert '<b>Error:</b> Unclosed element “h”' in source
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
    assert response.url == app_url('index') + args  # type: ignore[attr-defined]


@mark.django_db  # to ensure migrations are applied properly
def test_email(live_app_url: LiveURL, client: Client, mailoutbox: list[AnymailMessage]) -> None:
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
def test_browsable_api(live_url: LiveURL, browser: Browser, user: User) -> None:
    browser.get(live_url('api-root'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_url('api-root'))

    url = browser.find_element(By.CSS_SELECTOR, 'div.response-info a span.str')
    url_text = re.sub(':[0-9]+/', '/', url.text)  # remove the non-deterministic port number
    browser.execute_script(f'arguments[0].innerHTML = "{url_text}"', url)

    browser.check('after_login')


def test_json_api(live_url: LiveURL, client: Client, user: User) -> None:
    response = client.get(live_url('api-root'))
    assert response.status_code == 403

    client.force_login(user)
    root_response = client.get(live_url('api-root')).json()
    assert root_response == {'projects': 'http://testserver/api/projects/'}

    response = client.get(root_response['projects'])
    assert response.json() == []

    local_data.ProjectData.insert()
    response = client.get(root_response['projects'])
    assert response.json()[0] == {
        'end_date': '2023-02-10',
        'name': 'Benchmark Cutting-Edge Paradigms',
        'start_date': '2023-02-01',
        'status': 'planning',
        'url': 'http://testserver/api/projects/16419f82-8b9d-4434-a465-e150bd9c66b3/',
    }


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


def test_sitemap(live_url: LiveURL, client: Client) -> None:
    site_factory()
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
    # Clear existing data from migrations
    robots.models.Url.objects.all().delete()
    robots.models.Rule.objects.all().delete()

    # Add new data
    robots_rule_factory(
        id=1,
        disallowed=[robots_url_factory(id=1, pattern='/disallowed/')],
        sites=[site_factory()],
    )

    # Check robots.txt
    response = client.get(live_url('robots'))
    source = response.content.decode()
    assert 'User-agent: *\n' in source
    assert '\nDisallow: /disallowed/\n' in source
    assert '\nHost: logikal.io\n' in source
    assert '\nSitemap: http://logikal.io/sitemap.xml\n' in source


@set_browser(scenarios.desktop)
def test_error_pages(live_url: LiveURL, client: Client, browser: Browser) -> None:
    response_error_codes = {400: 500, 403: 404, 404: 404, 500: 500}
    for code in ERROR_HANDLERS:
        url = live_url(f'error:{code}')
        response = client.get(url)
        assert response.status_code == response_error_codes[code]
        browser.get(url)
        browser.check(str(code))
