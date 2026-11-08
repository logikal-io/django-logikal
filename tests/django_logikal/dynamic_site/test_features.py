import re

from django.test import Client
from django.urls import reverse
from pytest import mark
from pytest_django.live_server_helper import LiveServer
from pytest_logikal import Browser, LiveURL, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.django_logikal.conftest import app_url
from tests.dynamic_site import local_data
from tests.dynamic_site.models import User


@mark.django_db
def test_local_data() -> None:
    local_data.UserData.insert()
    assert User.objects.filter(email='admin-user@django-logikal.org').exists()


def test_home_head(live_server: LiveServer, client: Client) -> None:
    response = client.get(live_server.url)
    source = response.content.decode()
    description = 'This is a dynamic site used for demonstration and testing purposes.'
    assert f'<meta name="description" content="{description}">' in source
    assert '<title>Home Page | Logikal</title>' in source

    # Content security policy
    assert "default-src 'self' 'nonce-" in response.headers['Content-Security-Policy']
    assert re.search('<script nonce="[^"]+">let test = 42;</script>', source)


@set_browser(scenarios.desktop)
def test_home(live_server: LiveServer, browser: Browser) -> None:
    browser.get(live_server.url)
    browser.check()


@set_browser([scenarios.desktop, scenarios.mobile])
def test_menu(live_server: LiveServer, browser: Browser) -> None:
    variant = 'mobile' if browser.settings.mobile else 'desktop'

    # Check menu hover
    browser.get(live_server.url)
    if browser.settings.mobile:
        browser.find_element(By.ID, 'menu-mobile-toggle').click()

    menu = browser.find_element(By.ID, f'menu-{variant}-errors')
    browser.hover(menu)
    browser.check('menu_hover')

    menu.click()
    menu_item = browser.find_element(By.ID, f'menu-{variant}-submenu-404')
    browser.hover(menu_item)
    browser.check('menu_item_hover')

    # Check menu navigation
    menu_item.click()  # navigate forward
    browser.check('page_404')
    if browser.settings.mobile:
        browser.find_element(By.ID, 'menu-mobile-toggle').click()
    browser.find_element(By.ID, f'menu-{variant}-home').click()  # navigate back

    # Check submenu hover
    if browser.settings.mobile:
        browser.find_element(By.ID, 'menu-mobile-toggle').click()
    browser.find_element(By.ID, f'menu-{variant}-errors').click()
    submenu = browser.find_element(By.ID, f'menu-{variant}-page-not-found-errors')
    browser.hover(submenu)
    browser.check('submenu_hover')

    submenu.click()
    submenu_item = browser.find_element(By.ID, f'menu-{variant}-subsubmenu-404')
    browser.hover(submenu_item)
    browser.check('submenu_item_hover')

    # Check submenu navigation
    submenu_item.click()
    browser.check('page_404')


@set_browser(scenarios.desktop)
def test_templates(live_app_url: LiveURL, browser: Browser) -> None:
    browser.get(live_app_url('templates', kwargs={'url_path_arg': 'path'}) + '?next=/internal/')
    browser.check()


@set_browser(scenarios.desktop)
def test_models(live_app_url: LiveURL, browser: Browser) -> None:
    local_data.ProjectData.insert()
    browser.get(live_app_url('models'))
    browser.check()


@set_browser(scenarios.desktop)
def test_partials(
    live_app_url: LiveURL,
    browser: Browser,
) -> None:
    browser.get(live_app_url('partials'))
    browser.check('initial')
    button = browser.find_element(By.CSS_SELECTOR, 'main section button')
    button.click()
    browser.check('updated')


@set_browser(scenarios.desktop_all_languages)
def test_localization(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('dynamic_site_localized:localization'))
    browser.check()


@set_browser(scenarios.desktop)
def test_language_switcher(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('dynamic_site_localized:localization'))
    browser.check('english_us')

    # Check hover and open state
    language_switcher = browser.find_element(By.ID, 'language-switcher')
    browser.hover(language_switcher)
    browser.check('switcher_hover')
    language_switcher.click()
    browser.check('switcher_open')

    # Check interactions with menu
    browser.find_element(By.ID, 'menu-desktop-errors').click()
    browser.check('menu_open')
    language_switcher.click()
    browser.check('switcher_open')

    # Check language switching
    language_en_gb = language_switcher.find_element(By.CSS_SELECTOR, 'button[value="en-gb"]')
    browser.hover(language_en_gb)
    browser.check('switcher_item_hover')
    language_en_gb.click()
    browser.check('english_gb')


@set_browser(scenarios.desktop)
def test_internal(live_app_url: LiveURL, browser: Browser, client: Client, user: User) -> None:
    response = client.get(live_app_url('internal'))
    assert response.status_code == 302
    assert response.url == f'{reverse('account_auth')}?next={app_url('internal')}'  # type: ignore

    browser.get(live_app_url('internal'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_app_url('internal'))
    browser.check('after_login')


@set_browser(scenarios.desktop)
def test_invalid_html(live_app_url: LiveURL, browser: Browser, client: Client) -> None:
    response = client.get(live_app_url('invalid_html'))
    source = response.content.decode()
    assert response.status_code == 500
    assert 'HTML Validation Error' in source
    assert '<b class="error">Error:</b> Element “h” not allowed' in source
    assert '<b class="error">Error:</b> Unclosed element “h”' in source
    browser.get(live_app_url('invalid_html'))
    browser.check()
